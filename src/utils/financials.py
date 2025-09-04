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
    # very simple rules: pick the largest positive as "salary", count negatives as expenses
    # matches "+5000" or "-1500" etc.
    amts = [float(a.replace("+","")) if "+" in a else -float(a.replace("-",""))
            for a in re.findall(r"([+-]\d+(?:\.\d+)?)", txt)]
    # salary ~= max positive
    salary = max([x for x in amts if x>0], default=0.0)
    expenses = -sum([x for x in amts if x<0])
    end_balance = None
    # try to capture the last balance number on a line
    balances = re.findall(r"\b(\d{3,})\b", txt)
    if balances:
        try: end_balance = float(balances[-1])
        except: end_balance = None
    return {
        "estimated_monthly_income": float(salary),
        "estimated_monthly_expenses": float(expenses),
        "ending_balance_guess": end_balance,
    }
