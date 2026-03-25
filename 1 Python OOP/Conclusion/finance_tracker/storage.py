# ─────────────────────────────────────────────
#  storage.py
# ─────────────────────────────────────────────

from abc import ABC, abstractmethod
from typing import List, Dict
from models import Transaction, Budget
import json
import os


class AbstractStorage(ABC):
    @abstractmethod
    def save(self, transactions: List[Transaction], budgets: Dict[str, Budget]) -> None:
        pass

    @abstractmethod
    def load(self) -> tuple[List[Transaction], Dict[str, Budget]]:
        pass


class JSONStorage(AbstractStorage):

    def __init__(self, transactions_file="transactions.json", budgets_file="budgets.json"):
        self.transactions_file = transactions_file
        self.budgets_file = budgets_file
        os.makedirs("storage", exist_ok=True)

    def save(self, transactions: List[Transaction], budgets: Dict[str, Budget]) -> None:
        path_transactions = os.path.join("storage", self.transactions_file)
        path_budgets = os.path.join("storage", self.budgets_file)

        with open(path_transactions, "w") as file:
            json.dump(
                [transaction.to_dict() for transaction in transactions],
                file,
                indent=2
            )

        with open(path_budgets, "w") as file:
            json.dump(
                [budget.to_dict() for budget in budgets.values()],
                file,
                indent=2
            )

    def load(self) -> tuple[List[Transaction], Dict[str, Budget]]:
        transactions = []
        budgets = {}
        path_transactions = os.path.join("storage", self.transactions_file)
        path_budgets = os.path.join("storage", self.budgets_file)

        try:
            with open(path_transactions, "r") as file:
                data = json.load(file)
                transactions = [Transaction.from_dict(item) for item in data]
        except FileNotFoundError:
            pass

        try:
            with open(path_budgets, "r") as file:
                data = json.load(file)
                for item in data:
                    budget = Budget.from_dict(item)
                    budgets[budget.category.lower()] = budget
        except FileNotFoundError:
            pass

        return transactions, budgets
