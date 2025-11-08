from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests, os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

GEMINI_KEY = os.getenv("GEMINI_API_KEY")

@app.get("/flywise")
def get_flight_suggestion(query: str = Query(..., description="User query")):
    payload = {
        "contents": [{"role": "user", "parts": [{"text": f"Find flight recommendations: {query}"}]}]
    }
    r = requests.post(
        "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent",
        headers={"Content-Type": "application/json"},
        params={"key": GEMINI_KEY},
        json=payload
    )
    return r.json()
