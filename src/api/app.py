from fastapi import FastAPI
from pydantic import BaseModel
from src.agent.simple_agent import answer_rag

app = FastAPI(title="Customer Support Agent")

@app.get("/health")
def health():
    return {"ok": True}

class ChatBody(BaseModel):
    question: str

@app.post("/chat")
def chat(body: ChatBody):
    return answer_rag(body.question)
