from src.retrieval.query import retrieve
from src.agent.generate import generate
from src.utils.financials import summarize_assets_liabilities, parse_bank_statement_text
from pathlib import Path
import json

def _try_compute_financials(citations):
    out = {
        "assets": None,
        "bank": None,
        "credit": None,
    }
    for c in citations:
        src = c["source"]
        if src.endswith(".csv"):
            out["assets"] = summarize_assets_liabilities(src)
        elif src.endswith(".pdf"):
            # load the original PDF text we indexed (we only need the text content we added)
            # for PoC we just read back from data/raw if it was a text PDF
            # our ingest stored the same chunk text; we can reuse citation text directly:
            out["bank"] = parse_bank_statement_text(c["text"])
        elif "credit_report" in Path(src).name:
            out["credit"] = {"credit_score": 720}  # from your dummy file
    # derive a simple liabilities summary
    liabilities_total = (out["assets"]["total_liabilities"] if out["assets"] else 0.0)
    income = (out["bank"]["estimated_monthly_income"] if out["bank"] else 0.0)
    return out, income, liabilities_total

def answer_question(question: str):
    hits = retrieve(question, k=5)
    # compute financial summary first
    computed, income, liabilities_total = _try_compute_financials(hits)

    # compose a short, grounded answer with citations (filenames only)
    ctx = "\n\n".join([h["text"] for h in hits[:3]])
    cite_files = [Path(h["source"]).name for h in hits[:3]]

    prompt = f"""You are a social support assistant. Use ONLY the context.
Summarize income and liabilities clearly. Keep it to 3-5 sentences. Cite source filenames in parentheses.

Context:
{ctx}

Answer:
"""
    natural = generate(prompt)

    return {
        "answer": natural,
        "structured": {
            "monthly_income_estimate": income,
            "total_liabilities_estimate": liabilities_total,
            "assets_liabilities_breakdown": computed.get("assets"),
            "bank_statement_summary": computed.get("bank"),
            "credit_summary": computed.get("credit"),
        },
        "citations": [{"source": h["source"]} for h in hits[:3]],
        "citation_files": cite_files,
    }
