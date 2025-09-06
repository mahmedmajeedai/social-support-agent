from pathlib import Path
import re
import pandas as pd

def load_text(path: str) -> str:
    return Path(path).read_text(errors="ignore")

def summarize_assets_liabilities(csv_path: str):
    df = pd.read_csv(csv_path)
    # normalize
    df["Category"] = df["Category"].str.strip().str.lower()
    total_assets = df[df["Category"]=="asset"]["Value"].sum()
    total_liabilities = df[df["Category"]=="liability"]["Value"].sum()
    items = df.to_dict(orient="records")
    return {
        "total_assets": float(total_assets),
        "total_liabilities": float(total_liabilities),
        "items": items,
    }

def parse_bank_statement_text(txt: str):
    """
    Extract signed amounts like +5000 / -1500 and ignore year-like tokens (e.g., -2024).
    """
    import re

    # signed 2–6 digit numbers like +5000, -1500, +300.50
    raw = re.findall(r"([+-]\d{2,6}(?:\.\d{1,2})?)", txt)
    vals = []
    for token in raw:
        v = float(token.replace("+", ""))
        # ignore year-like values and absurdly large values
        if 1900 <= abs(v) <= 2100:
            continue
        if abs(v) > 1_000_000:
            continue
        vals.append(v if token.startswith("+") else -abs(v))

    positives = [x for x in vals if x > 0]
    negatives = [x for x in vals if x < 0]

    salary = max(positives, default=0.0)
    expenses = -sum(negatives)

    # try to capture a plausible ending balance (last 3–6 digit unsigned number)
    end_balance = None
    balances = re.findall(r"\b(\d{3,6})\b", txt)
    if balances:
        try:
            end_balance = float(balances[-1])
        except Exception:
            end_balance = None

    return {
        "estimated_monthly_income": float(salary),
        "estimated_monthly_expenses": float(expenses),
        "ending_balance_guess": end_balance,
    }


