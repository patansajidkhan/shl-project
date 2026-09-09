from typing import Any

import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="SHL Assessment Recommendation API",
    description="A lightweight API that recommends SHL assessments from role or skill queries.",
    version="1.0.0",
)

SHL_CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"
SHL_BASE_URL = "https://www.shl.com"
REQUEST_TIMEOUT = 10


def get_latest_user_message(data: dict[str, Any]) -> str:
    """Extract and validate the latest user message from the request payload."""
    messages = data.get("messages")

    if not isinstance(messages, list) or not messages:
        raise HTTPException(status_code=400, detail="Request must contain a non-empty 'messages' list.")

    latest_message = messages[-1]
    if not isinstance(latest_message, dict) or not isinstance(latest_message.get("content"), str):
        raise HTTPException(status_code=400, detail="The latest message must contain string 'content'.")

    message = latest_message["content"].strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message content cannot be empty.")

    return message.lower()


def fetch_catalog_links() -> list[dict[str, str]]:
    """Fetch assessment links from the public SHL product catalogue."""
    try:
        response = requests.get(SHL_CATALOG_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail="Unable to retrieve the SHL product catalogue.") from exc

    soup = BeautifulSoup(response.text, "html.parser")
    catalog_links = []

    for link in soup.find_all("a"):
        text = link.get_text(" ", strip=True)
        href = link.get("href")

        if not text or not href:
            continue

        full_url = href if href.startswith("http") else f"{SHL_BASE_URL}{href}"
        catalog_links.append({"name": text, "url": full_url})

    return catalog_links


def recommend_assessments(user_message: str) -> list[dict[str, str]]:
    """Match words in the user's query against SHL catalogue link text."""
    user_words = {
        word.strip(".,!?;:()[]{}")
        for word in user_message.split()
        if len(word.strip(".,!?;:()[]{}")) > 2
    }

    recommendations = []
    seen_urls = set()

    for item in fetch_catalog_links():
        name = item["name"]
        if any(word in name.lower() for word in user_words):
            if item["url"] in seen_urls:
                continue

            seen_urls.add(item["url"])
            recommendations.append({
                "name": name,
                "url": item["url"],
                "test_type": "Assessment",
            })

            if len(recommendations) == 5:
                break

    return recommendations


@app.get("/health")
def health() -> dict[str, str]:
    """Return a simple service health response."""
    return {"status": "ok"}


@app.post("/chat")
def chat(data: dict[str, Any]) -> dict[str, Any]:
    """Return up to five assessment recommendations for the latest message."""
    user_message = get_latest_user_message(data)
    recommendations = recommend_assessments(user_message)

    if not recommendations:
        return {
            "reply": "No matching SHL assessments were found. Try including the target role or required skills.",
            "recommendations": [],
            "end_of_conversation": False,
        }

    return {
        "reply": f"I found {len(recommendations)} matching SHL assessments.",
        "recommendations": recommendations,
        "end_of_conversation": False,
    }
