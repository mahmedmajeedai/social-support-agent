from pathlib import Path
from src.retrieval.query import retrieve
from src.utils.financial import summarize_assets_liabilities, parse_bank_statement_text
from src.agent.generate import generate
from src.agent.eligibility import assess_eligibility

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
    credit_score = (out.get("credit") or {}).get("credit_score", None)
    return out, income, liabilities_total, expenses, credit_score

def _deterministic_paragraph(income, expenses, liabilities_total, credit_score, decision, cite_files):
    parts = [
        f"Monthly income is {income:,.0f}",
        f"expenses are about {expenses:,.0f}",
        f"total liabilities are {liabilities_total:,.0f}",
    ]
    if credit_score is not None:
        parts.append(f"credit score is {int(credit_score)}")
    parts.append(f"decision: {decision['status']}")
    if decision["reasons"]:
        parts.append(f"reasons: {', '.join(decision['reasons'])}")
    paragraph = "; ".join(parts) + "."
    return f"{paragraph} (sources: {', '.join(cite_files)})"

def answer_question(question: str):
    hits = retrieve(question, k=5)
    computed, income, liabilities_total, expenses, credit_score = _try_compute_financials(hits)

    # unique citation filenames
    cite_files = []
    for h in hits[:3]:
        fn = Path(h["source"]).name
        if fn not in cite_files:
            cite_files.append(fn)

    ctx = "\n\n".join([h["text"] for h in hits[:3]])

    # deterministic decision
    decision = assess_eligibility(income, expenses, liabilities_total, credit_score)

    # ask LLM for a clean paragraph
    prompt = f"""Use ONLY the context and computed facts to summarize finances in one short paragraph.

Context:
{ctx}

Computed facts:
- monthly_income = {income}
- monthly_expenses = {expenses}
- total_liabilities = {liabilities_total}
- credit_score = {credit_score}
- decision = {decision['status']}
- decision_reasons = {', '.join(decision['reasons']) if decision['reasons'] else 'None'}

Return a single plain-text paragraph."""
    paragraph = generate(prompt, max_new_tokens=220, temperature=0.1).strip()

    # fallback if LLM output is too short or looks like an echo
    if len(paragraph) < 60 or paragraph.lower().startswith(("return ", "reasons", "context", "computed")):
        final_answer = _deterministic_paragraph(income, expenses, liabilities_total, credit_score, decision, cite_files)
    else:
        final_answer = f"{paragraph} (sources: {', '.join(cite_files)})"

    return {
        "answer": final_answer,
        "structured": {
            "monthly_income_estimate": income,
            "total_liabilities_estimate": liabilities_total,
            "assets_liabilities_breakdown": computed.get("assets"),
            "bank_statement_summary": computed.get("bank"),
            "credit_summary": computed.get("credit"),
            "decision": decision,
        },
        "citations": [{"source": h["source"]} for h in hits[:3]],
        "citation_files": cite_files,
    }

# ---------- NEW: freeform answer for /ask ----------
def answer_freeform(question: str):
    hits = retrieve(question, k=5)

    # sort by similarity when present
    TOP = [h for h in hits if h.get("similarity") is not None]
    if TOP:
        TOP.sort(key=lambda x: x["similarity"], reverse=True)
    else:
        TOP = hits  # if distances are unavailable, just use the order

    # LOWER threshold to accept small docs (from 0.25 -> 0.05)
    if not TOP or (TOP[0].get("similarity") is not None and TOP[0]["similarity"] < 0.05):
        return {
            "answer": "I couldn’t find relevant information in the uploaded documents for that query.",
            "structured": {},
            "citations": [],
            "citation_files": [],
        }

    # build citations + context
    from pathlib import Path
    cite_files, ctx_parts = [], []
    for h in TOP[:3]:
        fn = Path(h["source"]).name
        if fn not in cite_files:
            cite_files.append(fn)
        ctx_parts.append(h["text"])
    ctx = "\n\n".join(ctx_parts)

    from src.agent.generate import generate
    prompt = f"""Answer the user's question using only the context.
Write one concise paragraph in plain text.

Question: {question}

Context:
{ctx}
"""
    paragraph = generate(prompt, max_new_tokens=220, temperature=0.2).strip()
    final_answer = f"{paragraph} (sources: {', '.join(cite_files)})"

    return {
        "answer": final_answer,
        "structured": {},
        "citations": [{"source": h["source"]} for h in TOP[:3]],
        "citation_files": cite_files,
    }
