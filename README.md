# Error Handling Demo

This project shows structured error handling in Python using **custom exceptions** and `try/except/else/finally`.

## Features

- Custom exceptions with codes & context:
  - **Database**: `ConnectionError`, `QueryError`
  - **Network**: `TimeoutError`, `BadResponseError`
  - **Validation**: `MissingFieldError`, `TypeMismatch`
- Catch specific or generic errors.
- Works with built-in exceptions like `ZeroDivisionError` and `ValueError`.

## Usage

```python
try:
    raise MissingFieldError("age", "int")
except AppError as e:
    log.error(f"Caught {type(e).__name__}: {e} [code={e.code}]")
```

## Example Output

```
ERROR | Caught MissingFieldError: Missing field 'age' (expected int) [code=3001]
Processing 5... Success! Result is 2.0
Processing 0... ZeroDivisionError caught: Can't divide by zero
Processing -3... ValueError caught: Negative number not allowed
```
