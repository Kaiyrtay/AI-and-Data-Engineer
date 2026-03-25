# ─────────────────────────────────────────────
#  models.py
# ─────────────────────────────────────────────

import os
from datetime import datetime
from functools import wraps

os.makedirs("logs", exist_ok=True)

MAX_LOG_SIZE = 10 * 1024 * 1024     # 10MB per log file
MAX_ARGS_LENGTH = 200               # truncate args if too long


def truncate_str(s, max_len=MAX_ARGS_LENGTH):
    s = str(s)
    if len(s) > max_len:
        return s[:max_len] + "..."
    return s


def get_log_file():
    base_log = os.path.join("logs", f"{datetime.now().date()}.log")

    if not os.path.exists(base_log):
        open(base_log, "a", encoding="utf-8").close()

    if os.path.getsize(base_log) > MAX_LOG_SIZE:
        timestamp = datetime.now().strftime("%H%M%S")
        rotated = os.path.join(
            "logs", f"{datetime.now().date()}_{timestamp}.log")
        os.rename(base_log, rotated)

    return base_log


def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        timestamp = datetime.now().isoformat(sep=" ", timespec="seconds")
        log_file = get_log_file()

        try:
            result = func(*args, **kwargs)
            logged_args = args[1:] if args and hasattr(
                args[0], '__dict__') else args
            log_entry = f"[{timestamp}] {func_name}() | Args: {truncate_str(logged_args)} | Kwargs: {truncate_str(kwargs)} | Result: {truncate_str(result)}"
        except Exception as e:
            logged_args = args[1:] if args and hasattr(
                args[0], '__dict__') else args
            log_entry = f"[{timestamp}] {func_name}() | Args: {truncate_str(logged_args)} | Kwargs: {truncate_str(kwargs)} | ERROR: {truncate_str(e)}"
            raise
        finally:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")

        return result

    return wrapper
