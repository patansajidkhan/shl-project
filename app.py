from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(data: dict):

    messages = data["messages"]

    user_message = messages[-1]["content"].lower()

    recommendations = []

    # developer related
    if "developer" in user_message or "python" in user_message or "java" in user_message:

        recommendations.append({
            "name": "Coding Assessment",
            "url": "https://www.shl.com",
            "test_type": "Technical"
        })

        recommendations.append({
            "name": "Developer Ability Test",
            "url": "https://www.shl.com",
            "test_type": "Technical"
        })

    # manager related
    elif "manager" in user_message or "lead" in user_message:

        recommendations.append({
            "name": "Leadership Assessment",
            "url": "https://www.shl.com",
            "test_type": "Behavioral"
        })

    # personality related
    elif "personality" in user_message:

        recommendations.append({
            "name": "OPQ Personality Test",
            "url": "https://www.shl.com",
            "test_type": "Personality"
        })

    # no matches
    else:

        return {
            "reply": "Could you explain the role or required skills in more detail?",
            "recommendations": [],
            "end_of_conversation": False
        }

    return {
        "reply": f"I found {len(recommendations)} suitable SHL assessments.",
        "recommendations": recommendations,
        "end_of_conversation": False
    }
def chat(data: dict):

    messages = data["messages"]

    user_message = messages[-1]["content"].lower()

    # SHL catalog URL
    url = "https://www.shl.com/solutions/products/product-catalog/"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    recommendations = []

    # find links
    links = soup.find_all("a")

    for link in links:

        text = link.get_text(strip=True)

        href = link.get("href")

        # check if user word exists
        if text and href:

            if any(word in text.lower() for word in user_message.split()):

                recommendations.append({
                    "name": text,
                    "url": href if href.startswith("http")
                    else "https://www.shl.com" + href,
                    "test_type": "Assessment"
                })

    # if nothing found
    # if nothing found
    if len(recommendations) == 0:

        recommendations.append({
            "name": "General Ability Test",
            "url": "https://www.shl.com",
            "test_type": "Assessment"
        })

        return {
            "reply": "I found a sample assessment recommendation.",
            "recommendations": recommendations,
            "end_of_conversation": False
        }

    # top 5 only
    recommendations = recommendations[:5]

    return {
        "reply": f"I found {len(recommendations)} matching SHL assessments.",
        "recommendations": recommendations,
        "end_of_conversation": False
    }