from fastapi import FastAPI
from pydantic import BaseModel
from src.agent.simple_agent import answer_question

app = FastAPI(title="Social Support Agent (PoC)")

@app.get("/")
def home():
    return {
        "message": "Social Support Agent API is running.",
        "try": ["/health", "/docs", "POST /ask", "POST /assess"],
        "example": {
            "POST /assess": {"question": "Assess eligibility and summarize the applicant’s finances."}
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

@app.post("/assess")
def assess(body: AskBody):
    return answer_question(body.question)
