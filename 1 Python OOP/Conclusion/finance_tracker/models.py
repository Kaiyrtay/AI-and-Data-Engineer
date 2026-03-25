# ─────────────────────────────────────────────
#  models.py
# ─────────────────────────────────────────────

from dataclasses import dataclass
from typing import Literal
from datetime import datetime

# from constants import ALLOWED_TRANSACTION_TYPES

from utils import validate_str, validate_float_not_negative, validate_transaction_type, validate_id, validate_bool, validate_date


@dataclass
class Transaction:
    # ─────────────────────────────────────────────
    #  initialization
    # ─────────────────────────────────────────────
    _id: int
    _title: str
    # must be the same as ALLOWED_TRANSACTION_TYPES
    _type: Literal["income", "expense"]
    _amount: float
    _category: str
    _date: datetime
    _recurring: bool

    def __post_init__(self) -> None:
        self.id = self._id
        self.title = self._title
        self.type = self._type
        self.amount = self._amount
        self.category = self._category
        self.date = self._date
        self.recurring = self._recurring

    # ─────────────────────────────────────────────
    #  getters
    # ─────────────────────────────────────────────

    @property
    def id(self) -> int:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def type(self) -> Literal["income", "expense"]:
        return self._type

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def category(self) -> str:
        return self._category

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def recurring(self) -> bool:
        return self._recurring

    # ─────────────────────────────────────────────
    #  setters
    # ─────────────────────────────────────────────

    @id.setter
    def id(self, value) -> None:
        self._id = validate_id(value)

    @title.setter
    def title(self, value) -> None:
        self._title = validate_str(value, "Transaction title")

    @type.setter
    def type(self, value) -> None:
        self._type = validate_transaction_type(value)

    @amount.setter
    def amount(self, value) -> None:
        self._amount = validate_float_not_negative(
            value, "Transaction amount")

    @category.setter
    def category(self, value) -> None:
        self._category = validate_str(value, "Transaction category").lower()

    @date.setter
    def date(self, value) -> None:
        self._date = validate_date(value, "Transaction date")

    @recurring.setter
    def recurring(self, value) -> None:
        self._recurring = validate_bool(value, "Transaction recurring")

    # ─────────────────────────────────────────────
    #  methods
    # ─────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type,
            "amount": self.amount,
            "category": self.category,
            "date": self.date.isoformat(),
            "recurring": self.recurring
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        return cls(
            _id=data["id"],
            _title=data["title"],
            _type=data["type"],
            _amount=data["amount"],
            _category=data["category"],
            _date=datetime.fromisoformat(data["date"]),
            _recurring=data["recurring"]
        )

    def __str__(self) -> str:
        return f"{self.id}: {self.type.upper()} | {self.amount} | {self.category}"


@dataclass
class Budget:
    # ─────────────────────────────────────────────
    #  initialization
    # ─────────────────────────────────────────────
    _category: str
    _limit: float
    _spent: float

    def __post_init__(self) -> None:
        self.category = self._category
        self.limit = self._limit
        self.spent = self._spent

    # ─────────────────────────────────────────────
    #  getters
    # ─────────────────────────────────────────────

    @property
    def category(self) -> str:
        return self._category

    @property
    def limit(self) -> float:
        return self._limit

    @property
    def spent(self) -> float:
        return self._spent

    # ─────────────────────────────────────────────
    #  setters
    # ─────────────────────────────────────────────

    @category.setter
    def category(self, value: str) -> None:
        self._category = validate_str(value, "Budget category").lower()

    @limit.setter
    def limit(self, value: int | float) -> None:
        self._limit = validate_float_not_negative(value, "Budget limit")

    @spent.setter
    def spent(self, value: int | float) -> None:
        self._spent = validate_float_not_negative(value, "Budget spent")

    # ─────────────────────────────────────────────
    #  methods
    # ─────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "limit": self.limit,
            "spent": self.spent
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Budget":
        return cls(
            _category=data["category"],
            _limit=data["limit"],
            _spent=data["spent"]
        )

    def __str__(self) -> str:
        return f"{self.category}: {self.spent} / {self.limit}"
