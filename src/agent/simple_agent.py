from src.retrieval.query import retrieve
from src.agent.generate import generate

def answer_question(question: str):
    hits = retrieve(question, k=3)
    ctx = "\n\n".join([h["text"] for h in hits])
    prompt = f"""You are a helpful assistant. Answer ONLY using the context below.
Question: {question}

Context:
{ctx}

Return a concise answer (3-6 sentences). Cite sources as filenames in parentheses if possible.
Answer:
"""
    ans = generate(prompt)
    return {"answer": ans, "citations": hits}
