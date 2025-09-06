# src/agent/simple_agent.py
from pathlib import Path
from src.retrieval.query import retrieve
from src.utils.financials import summarize_assets_liabilities, parse_bank_statement_text
from src.agent.generate import generate

def _try_compute_financials(citations):
    out = {"assets": None, "bank": None, "credit": None}
    for c in citations:
        src = c["source"]
        if src.endswith(".csv"):
            out["assets"] = summarize_assets_liabilities(src)
        elif src.endswith(".pdf"):
            # use the text already included in the citation
            out["bank"] = parse_bank_statement_text(c["text"])
        elif "credit_report" in Path(src).name:
            out["credit"] = {"credit_score": 720}  # from dummy file
    income = (out["bank"]["estimated_monthly_income"] if out["bank"] else 0.0)
    liabilities_total = (out["assets"]["total_liabilities"] if out["assets"] else 0.0)
    expenses = (out["bank"]["estimated_monthly_expenses"] if out["bank"] else 0.0)
    return out, income, liabilities_total, expenses

def answer_question(question: str):
    hits = retrieve(question, k=5)
    computed, income, liabilities_total, expenses = _try_compute_financials(hits)
    cite_files = [Path(h["source"]).name for h in hits[:3]]
    ctx = "\n\n".join([h["text"] for h in hits[:3]])

    prompt = f"""You are a social support assistant.

Write 3–5 concise sentences that summarize the applicant’s income and liabilities,
grounded ONLY in the context below. Use the computed values exactly. Cite filenames
in parentheses at the end (e.g., (bank_statement_sample.pdf, assets_liabilities_sample.csv)).

Context:
{ctx}

Computed facts (must use as-is):
- monthly_income_estimate = {income}
- total_liabilities_estimate = {liabilities_total}
- monthly_expenses_estimate = {expenses}
- credit_score = {(computed.get('credit') or {}).get('credit_score', 'unknown')}

Write the summary only. No headings, no 'Answer:' prefix, no code fences.
"""

    natural = generate(prompt, max_new_tokens=220, temperature=0.1)

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
