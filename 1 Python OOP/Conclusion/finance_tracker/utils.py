# ─────────────────────────────────────────────
#  utils.py
# ─────────────────────────────────────────────

from datetime import datetime
from constants import ALLOWED_TRANSACTION_TYPES


def validate_transaction_type(type: str) -> str:
    validate_str(type, "Transaction type")
    type_lower = type.lower()
    if type_lower not in ALLOWED_TRANSACTION_TYPES:
        raise ValueError(
            f"Invalid transaction type: {type_lower}. Allowed types: {', '.join(ALLOWED_TRANSACTION_TYPES)}"
        )
    return type_lower


def validate_float_not_negative(value: float, attr_name: str = "") -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError(f"{attr_name or 'Value'} must be a number")
    if value < 0:
        raise ValueError(f"{attr_name or 'Value'} cannot be negative")
    return float(value)


def validate_str(value: str, attr_name: str = "") -> str:
    if not isinstance(value, str):
        raise TypeError(f"{attr_name or 'Value'} must be string")
    if not value.strip():
        raise ValueError(f"{attr_name or 'Value'} cannot be empty.")
    return value


def validate_id(value: int, attr_name: str = "") -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{attr_name or 'Value'} must be a number")
    if value <= 0:
        raise ValueError(f"{attr_name or 'Value'} cannot be negative nor 0")
    return value


def validate_date(value, attr_name: str = "") -> datetime:
    if not isinstance(value, datetime):
        raise TypeError(f"{attr_name or 'Value'} must be a datetime")
    return value


def validate_bool(value, attr_name: str = "") -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{attr_name or 'Value'} must be boolean")
    return value


def parse_float(value: str) -> float:
    value = validate_str(value, "Value")

    try:
        return float(value.strip())
    except ValueError:
        raise ValueError(f"Cannot parse '{value}' to float")


def parse_date(date_str: str) -> datetime:
    date_str = validate_str(date_str, "Date")

    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            f"Invalid date format: '{date_str}'. Expected format: YYYY-MM-DD"
        )


def format_amount(value: float) -> str:
    value = validate_float_not_negative(value)
    return f"${value:,.2f}"


def format_date(value: datetime) -> str:
    validate_date(value, "Date")
    return value.strftime("%Y-%m-%d %H:%M:%S")
