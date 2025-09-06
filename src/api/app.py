from fastapi import FastAPI
from pydantic import BaseModel
from src.agent.simple_agent import answer_question

app = FastAPI(title="Social Support Agent (PoC)")

@app.get("/")
def home():
    return {
        "message": "Social Support Agent API is running.",
        "try": ["/health", "/docs", "POST /ask"],
        "example": {
            "POST /ask": {"question": "What are the applicant’s income and liabilities based on the documents?"}
        }
    }

@app.get("/health")
def health():
    return {"ok": True}

class AskBody(BaseModel):
    question: str

@app.post("/ask")
def ask(body: AskBody):
    return answer_question(body.question)
