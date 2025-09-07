from src.retrieval.query import retrieve_uploads
from src.agent.generate import generate
import re

SMALL_TALK_PATTERNS = [r"^\s*hi\s*$", r"^\s*hello\s*$", r"^\s*hey\s*$",
                       r"who\s+are\s+you", r"what\s+are\s+you", r"help\s*"]

def _is_small_talk(q: str) -> bool:
    return any(re.search(p, (q or "").lower()) for p in SMALL_TALK_PATTERNS)

def answer_rag(question: str):
    # small talk → canned response
    if _is_small_talk(question):
        return {"answer": "I’m your Customer Support Agent. Upload a document and I’ll answer questions strictly from it."}

    # retrieve from uploads
    hits = retrieve_uploads(question, k=5)
    if not hits:
        return {"answer": "Sorry, I couldn’t find that information in the documents you uploaded."}

    # join top chunks
    ctx = "\n\n".join([h["text"] for h in hits])

    # strict prompt
    prompt = f"""You are a precise assistant.
Answer the user’s question ONLY using the context below.
If the context does not contain the answer, reply exactly:
"Sorry, I couldn’t find that information in the documents you uploaded."

Question: {question}

Context:
{ctx}

Answer in plain text. No headings. No 'Answer:' prefix. No citations.
"""
    reply = generate(prompt, max_new_tokens=200, temperature=0.1).strip()

    return {"answer": reply}
