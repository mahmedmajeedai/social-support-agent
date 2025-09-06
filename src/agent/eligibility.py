# src/agent/eligibility.py
from typing import Dict, Any

def _safe(v, default=0.0):
    try:
        return float(v)
    except Exception:
        return float(default)

def estimate_monthly_debt_payment(liabilities_total: float, bank_summary: Dict[str, Any]) -> float:
    """
    PoC heuristic:
    - If 'EMI' style payments detected in the bank summary (we don't have itemized here),
      assume 500 as a monthly installment (from our dummy data).
    - Otherwise fall back to 3% of total outstanding liabilities, capped at 1000 for PoC.
    """
    if bank_summary:
        # If you later parse actual 'EMI' occurrences, sum them here.
        return 500.0
    return min(0.03 * _safe(liabilities_total), 1000.0)

def assess_eligibility(income: float,
                       expenses: float,
                       liabilities_total: float,
                       credit_score: float | int | None) -> Dict[str, Any]:
    income = _safe(income)
    expenses = _safe(expenses)
    liabilities_total = _safe(liabilities_total)
    credit_score = _safe(credit_score or 0)

    monthly_debt = estimate_monthly_debt_payment(liabilities_total, {})
    dti = monthly_debt / max(income, 1.0)

    reasons: list[str] = []
    status = "approve"

    # Simple, transparent PoC rules
    if income < 3000:
        status = "soft-decline"; reasons.append("Income below threshold (3000)")
    if credit_score < 680:
        status = "soft-decline"; reasons.append("Credit score below threshold (680)")
    if dti > 0.40:
        status = "soft-decline"; reasons.append("Debt-to-income ratio above 40%")
    if expenses > income * 0.80:
        status = "soft-decline"; reasons.append("Expenses exceed 80% of income")

    return {
        "status": status,
        "reasons": reasons,
        "metrics": {
            "monthly_income": income,
            "monthly_expenses": expenses,
            "liabilities_total": liabilities_total,
            "estimated_monthly_debt_payment": monthly_debt,
            "dti": dti,
            "credit_score": credit_score,
        },
        # Lightweight recommendations to show "enablement"
        "recommendations": [] if status == "approve" else [
            "Offer financial counseling",
            "Consider restructuring high-interest debt",
            "Enroll in upskilling / job matching program",
        ],
    }