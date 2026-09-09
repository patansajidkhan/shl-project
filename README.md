# SHL Assessment Recommendation API

A lightweight Python backend that recommends relevant SHL assessments based on a user's role or skill-related query.

## What it does

The application exposes a FastAPI service with two endpoints:

- `GET /health` — basic service health check.
- `POST /chat` — accepts conversation messages and returns assessment recommendations.

The recommendation logic can identify common role/skill keywords such as developer, Python, Java, manager, lead, and personality-related queries. The application also demonstrates retrieving the SHL product catalogue with HTTP requests and parsing catalogue links with BeautifulSoup.

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Requests
- BeautifulSoup4
- REST API

## Project Structure

```text
shl-project/
├── app.py
├── requirements.txt
├── runtime.txt
└── README.md
```

## How it works

```text
User request
    ↓
POST /chat
    ↓
Read latest message
    ↓
Match role/skill terms
    ↓
Generate assessment recommendations
    ↓
Return JSON response
```

## Run locally

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

The API can then be tested through FastAPI's interactive documentation at `/docs`.

## Notes

This project is a learning implementation demonstrating REST API development, request handling, keyword-based recommendation logic, and web-page parsing.
