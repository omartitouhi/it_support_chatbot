from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Optional
from rag.generate import generate_response

app = FastAPI(title="IT Support Chatbot")

class ChatRequest(BaseModel):
    query: str
    chat_history: Optional[List[Dict[str, str]]] = None

@app.get("/")
async def root():
    return {"message": "Welcome to the IT Support Chatbot!"}

@app.post("/chat")
async def chat(request: ChatRequest):
    response = generate_response(request.query, chat_history=request.chat_history)
    return {"response": response}