# ─────────────────────────────────────────────
#  manager.py
# ─────────────────────────────────────────────
from typing import Generator
from datetime import datetime

from models import Transaction, Budget
from utils import validate_id, validate_str, validate_float_not_negative
from decorators import log_action
from reports import summary_report, print_summary_report


class FinanceManager:

    def __init__(self):
        self.__transactions = []
        self.__budgets = {}
        self.__current_id = 1

    @property
    def transactions(self) -> list[Transaction]:
        return self.__transactions

    @property
    def current_id(self) -> int:
        return self.__current_id

    @property
    def budgets(self) -> dict[str, Budget]:
        return self.__budgets

    @log_action
    def add_transaction(self, title: str, transaction_type: str, amount: int | float, category: str, recurring=False) -> Transaction:
        if not self.__can_add_transaction(title):
            raise ValueError(
                f"Can not create transaction, transaction with that title {title!r} already exists")
        holder = Transaction(_id=self.current_id,
                             _title=title,
                             _type=transaction_type,
                             _amount=amount,
                             _category=category,
                             _date=datetime.now(),
                             _recurring=recurring
                             )
        self.transactions.append(holder)
        self.__current_id += 1
        return holder

    @log_action
    def remove_transaction(self, transaction_id: int) -> bool:
        try:
            holder = self.__find_transaction(transaction_id)
            self.transactions.remove(holder)
            return True
        except ValueError:
            return False

    def list_transactions(self, filter_type=None, category=None) -> Generator["Transaction", None, None]:
        for transaction in self.transactions:
            if filter_type and transaction.type != filter_type:
                continue
            if category and transaction.category != category.lower():
                continue
            yield transaction

    @log_action
    def mark_recurring(self, transaction_id: int) -> Transaction | None:
        try:
            holder = self.__find_transaction(transaction_id)
            holder.recurring = True
            return holder
        except ValueError:
            return None

    @log_action
    def __find_transaction(self, transaction_id: int) -> Transaction:
        transaction_id = validate_id(transaction_id, "Transaction id")
        for transaction in self.transactions:
            if transaction.id == transaction_id:
                return transaction
        else:
            raise ValueError(f"Transaction not found: {transaction_id}")

    def __can_add_transaction(self, title: str) -> bool:
        for transaction in self.transactions:
            if transaction.title.lower() == title.lower():
                return False
        else:
            return True

    def get_balance(self) -> float:
        holder = self.get_balance_by_category(all=True)
        return holder["net"]

    def get_balance_by_category(self, category: str | None = None, all=False) -> dict:
        if not all:
            category = validate_str(category, "Budget category").lower()
        sum_income = 0
        sum_expenses = 0
        for transaction in self.transactions:
            if all or transaction.category == category:
                if transaction.type == 'income':
                    sum_income += transaction.amount
                if transaction.type == 'expense':
                    sum_expenses += transaction.amount

        return {
            "category": category if not all else "All",
            "income": sum_income,
            "expenses": sum_expenses,
            "net": sum_income - sum_expenses
        }

    @log_action
    def add_budget(self, category: str, limit: int | float) -> Budget:
        if not self.__can_add_budget(category):
            raise ValueError(
                f"Can not create budget, budget with that category {category!r} already exists")
        holder = Budget(_category=category, _limit=limit, _spent=0.0)
        self.__budgets[category.lower()] = holder
        return holder

    @log_action
    def update_budget_spent(self, category: str, amount: int | float) -> bool:
        category_lower = category.lower()
        if category_lower in self.budgets:
            self.budgets[category_lower].spent = validate_float_not_negative(
                amount, "Budget amount")
            return True
        else:
            raise ValueError(f"Budget not found: {category!r}")

    def generate_report(self):
        print_summary_report(self.transactions)

    def __can_add_budget(self, category: str) -> bool:
        return category.lower() not in self.budgets
