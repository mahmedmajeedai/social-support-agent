from fastapi import FastAPI
from pydantic import BaseModel
from src.agent.simple_agent import answer_question

app = FastAPI(title="Social Support Agent (PoC)")

@app.get("/health")
def health():
    return {"ok": True}

class AskBody(BaseModel):
    question: str

@app.post("/ask")
def ask(body: AskBody):
    result = answer_question(body.question)
    return result
