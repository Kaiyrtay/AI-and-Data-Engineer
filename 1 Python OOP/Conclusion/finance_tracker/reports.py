# ─────────────────────────────────────────────
#  reports.py
# ─────────────────────────────────────────────

from typing import List, Dict
from models import Transaction, Budget
from datetime import datetime
from utils import validate_date


def report_by_category(transactions: List[Transaction]) -> Dict[str, Dict[str, float]]:
    if not isinstance(transactions, list) or not all(isinstance(t, Transaction) for t in transactions):
        raise TypeError("transactions must be a list of Transaction objects")

    grouped: Dict[str, Dict[str, float]] = {}

    for transaction in transactions:
        key = transaction.category.lower()

        if not key in grouped:
            grouped[key] = {"income": 0.0, "expense": 0.0}

        if transaction.type == "income":
            grouped[key]["income"] += transaction.amount
        elif transaction.type == "expense":
            grouped[key]["expense"] += transaction.amount

    return grouped


def report_by_period(transactions: List[Transaction], start_date: datetime, end_date: datetime) -> List[Transaction]:
    if not isinstance(transactions, list) or not all(isinstance(t, Transaction) for t in transactions):
        raise TypeError("transactions must be a list of Transaction objects")

    start_date = validate_date(start_date)
    end_date = validate_date(end_date)
    filtered: List[Transaction] = []

    for transaction in transactions:
        if start_date <= transaction.date <= end_date:
            filtered.append(transaction)

    return filtered


def summary_report(transactions: List[Transaction]) -> Dict[str, Dict[str, float | int]]:
    if not isinstance(transactions, list) or not all(isinstance(t, Transaction) for t in transactions):
        raise TypeError("transactions must be a list of Transaction objects")

    reports: Dict[str, Dict[str, float | int]] = {}

    for transaction in transactions:
        key = transaction.category.lower()
        if not key in reports:
            reports[key] = {
                "total_income": 0.0,
                "total_expenses": 0.0,
                "balance": 0.0,
                "transaction_count": 0
            }

        if transaction.type == "income":
            reports[key]["total_income"] += transaction.amount
            reports[key]["balance"] += transaction.amount
            reports[key]["transaction_count"] += 1
        elif transaction.type == "expense":
            reports[key]["total_expenses"] += transaction.amount
            reports[key]["balance"] -= transaction.amount
            reports[key]["transaction_count"] += 1

    return reports


def print_category_report(transactions: List[Transaction]) -> str:
    grouped = report_by_category(transactions)
    lines = ["Category Report:", "-" * 40]

    for category, amounts in grouped.items():
        lines.append(
            f"{category.title():<15} Income: {amounts['income']:>10.2f}  Expense: {amounts['expense']:>10.2f}")

    lines.append("-" * 40)
    return "\n".join(lines)


def print_summary_report(transactions: List[Transaction]) -> str:
    summary = summary_report(transactions)
    lines = ["Summary Report:", "-" * 50]
    header = f"{'Category':<15} {'Income':>10} {'Expense':>10} {'Balance':>10} {'Count':>6}"
    lines.append(header)
    lines.append("-" * 50)

    for category, data in summary.items():
        lines.append(
            f"{category.title():<15} "
            f"{data['total_income']:>10.2f} "
            f"{data['total_expenses']:>10.2f} "
            f"{data['balance']:>10.2f} "
            f"{data['transaction_count']:>6}"
        )

    lines.append("-" * 50)
    return "\n".join(lines)
