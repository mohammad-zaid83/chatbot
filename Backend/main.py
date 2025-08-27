import os
from urllib import response
import cohere
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# load .env
load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN")

co = cohere.ClientV2(COHERE_API_KEY)

app = FastAPI()

# ✅ allow only your frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN, "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: list | None = None

@app.post("/chat")
async def chat(req: ChatRequest):
    if not req.message.strip():
        return {"reply": "⚠️ Please type something."}

    try:
        messages = [
    {"role": "system", "content": "You are a friendly portfolio chatbot. Answer briefly."},
    *([*req.history] if req.history else []),
    {"role": "user", "content": req.message}
]

        reply = response.message.content[0].text.strip()
        return {"reply": reply}
    except Exception as e:
        print("Error:", e)
        return {"reply": "⚠️ Error connecting to AI."}