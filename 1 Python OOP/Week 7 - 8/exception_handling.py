import logging
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
log = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# Base Exception
# ─────────────────────────────────────────────


@dataclass
class AppError(Exception):
    msg: str
    code: int = 0
    context: dict = field(default_factory=dict)

    def __str__(self):
        ctx = f" | context={self.context}" if self.context else ""
        return f"{self.msg}{ctx}"

# ─────────────────────────────────────────────
# Exception Hierarchy
# ─────────────────────────────────────────────

# DB errors


class DatabaseError(AppError):
    pass


class ConnectionError(DatabaseError):
    def __init__(self, host, port, reason=""):
        super().__init__(f"Cannot connect to {host}:{port}" + (
            f" — {reason}" if reason else ""), 1001, {"host": host, "port": port})


class QueryError(DatabaseError):
    def __init__(self, query, reason):
        super().__init__(
            f"Query failed: {reason}", 1002, {"query": query[:120]})

# Network errors


class NetworkError(AppError):
    pass


class TimeoutError(NetworkError):
    def __init__(self, url, timeout):
        super().__init__(f"Request to {url} timed out after {timeout}s", 2001, {
            "url": url, "timeout": timeout})


class BadResponseError(NetworkError):
    def __init__(self, url, status):
        super().__init__(f"Unexpected HTTP {status} from {url}", 2002, {
            "url": url, "status": status})

# Validation errors


class ValidationError(AppError):
    pass


class MissingFieldError(ValidationError):
    def __init__(self, field, expected_type=""):
        super().__init__(f"Missing field '{field}'" + (
            f" (expected {expected_type})" if expected_type else ""), 3001, {"field": field})


class TypeMismatch(ValidationError):
    def __init__(self, field, expected, got):
        super().__init__(f"Field '{field}' expected {expected.__name__}, got {got.__name__}", 3002, {
            "field": field, "expected": expected.__name__, "got": got.__name__})


# ─────────────────────────────────────────────
# Demo
# ─────────────────────────────────────────────
try:
    raise MissingFieldError("age", "int")
except AppError as e:
    log.error(f"Caught {type(e).__name__}: {e} [code={e.code}]")


# ─────────────────────────────────────────────
# try/except/else/finally and build in Exceptions
# ─────────────────────────────────────────────

def risky_operation(n):
    if n == 0:
        raise ZeroDivisionError("Can't divide by zero")
    elif n < 0:
        raise ValueError("Negative number not allowed")
    return 10 / n


numbers = [5, 0, -3]

for num in numbers:
    try:
        print(f"Processing {num}...")
        result = risky_operation(num)
    except ZeroDivisionError as e:
        print(f"ZeroDivisionError caught: {e}")
    except ValueError as e:
        print(f"ValueError caught: {e}")
    except Exception as e:
        print(f"Some other error: {e}")
    else:
        print(f"Success! Result is {result}")
    finally:
        print(f"Finished attempt for {num}\n")
