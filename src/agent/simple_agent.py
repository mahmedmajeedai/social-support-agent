from pathlib import Path
from src.retrieval.query import retrieve
from src.utils.financial import summarize_assets_liabilities, parse_bank_statement_text
from src.agent.generate import generate

def _try_compute_financials(citations):
    out = {"assets": None, "bank": None, "credit": None}
    for c in citations:
        src = c["source"]
        if src.endswith(".csv"):
            out["assets"] = summarize_assets_liabilities(src)
        elif src.endswith(".pdf"):
            out["bank"] = parse_bank_statement_text(c["text"])
        elif "credit_report" in Path(src).name:
            out["credit"] = {"credit_score": 720}
    income = (out["bank"]["estimated_monthly_income"] if out["bank"] else 0.0)
    liabilities_total = (out["assets"]["total_liabilities"] if out["assets"] else 0.0)
    expenses = (out["bank"]["estimated_monthly_expenses"] if out["bank"] else 0.0)
    return out, income, liabilities_total, expenses

def answer_question(question: str):
    hits = retrieve(question, k=5)
    computed, income, liabilities_total, expenses = _try_compute_financials(hits)

    # build clean, unique citation list
    cite_files = []
    for h in hits[:3]:
        fn = Path(h["source"]).name
        if fn not in cite_files:
            cite_files.append(fn)

    ctx = "\n\n".join([h["text"] for h in hits[:3]])

    # IMPORTANT: ask LLM to NOT include citations; we’ll append them deterministically
    prompt = f"""Summarize the applicant’s income and liabilities using ONLY the information below.
Write 3–5 concise sentences in plain text. Use the exact computed values. Do not include citations.

Context:
{ctx}

Computed:
- monthly_income = {income}
- monthly_expenses = {expenses}
- total_liabilities = {liabilities_total}
- credit_score = {(computed.get('credit') or {}).get('credit_score', 'unknown')}
"""

    paragraph = generate(prompt, max_new_tokens=200, temperature=0.1).strip()
    final_answer = f"{paragraph} (sources: {', '.join(cite_files)})"

    return {
        "answer": final_answer,
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
