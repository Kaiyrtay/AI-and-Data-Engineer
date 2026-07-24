# Python OOP

Progression from core object-oriented Python to SOLID design under pressure, ending in two capstone projects. Later folders assume everything covered before them.

## Foundations

### `Week 2 - 3/`
Abstract base classes and polymorphism (`Vehicle` → `Car`/`Motorcycle`/`Truck`), then multiple inheritance and MRO (`Printable`/`Serializable`/`Report`, including a deliberately reordered version to see how resolution order changes). Includes a small hand-rolled test harness (`check`/`expect_error`) used before `unittest` shows up later.

### `Week 4 - 5/`
- `decorators.py` / `custom_list.py` — validation decorators (`not_negative`, `index_validation`) applied to a hand-built `CustomList`, covered by real `unittest` cases.
- `generators.py` — `is_prime`, an infinite `prime_numbers()` generator, `fibonacci()`, and a lazy `filereader`.
- `magic_methods.py` — a `BankAccount` class exercising `__eq__`, `__lt__`, `__add__`, `__iadd__`, `__hash__`.
- `context-manager.py` — `FileManager` implementing `__enter__`/`__exit__` by hand.

### `Week 7 - 8/`
- `comprehension_tasks.md` / `comprehension_task_solutions.py` — 15 dict/set/nested/conditional comprehension drills.
- `lambda_tasks.md` / `lambda_task_solutions.py` — 20 drills restricted to `lambda`/`map`/`filter`/`reduce` only (no loops, no comprehensions).
- `exception_handling.py` — a custom exception hierarchy (`AppError` → `DatabaseError`/`NetworkError`/`ValidationError`, each with specific subtypes like `ConnectionError`, `TimeoutError`, `MissingFieldError`).
- `function_arguments_mastery.py` — positional / `*args` / `**kwargs` combinations.

## Applied mini-projects

- **`Log Analysis Tool/`** — parses real Android system logs (Loghub dataset) through a `LogEntry` class, with `timer`/`memory_tracker` decorators and a generator-based reader benchmarked against a list-based one.
- **`Student Grade Management System/`** — `Student` → `Course` → `University`, grade averaging and reporting (pre-SOLID version — compare against the SOLID Level 2 rebuild below).
- **`University Personnel Management System/`** — `Person` (ABC) branching into `Staff` → `Teacher`/`Administrator`/`Security` and `Student` → `UndergraduateStudent`/`GraduateStudent`, each with role-specific salary/tuition logic.

## SOLID principles — three-level capstone

Three console apps of increasing difficulty, each split strictly into `backend.py` (zero `print()`/`input()`) and `frontend.py` (zero business logic), judged against the written specs in `task.txt` / `final.txt`:

1. **Library Management System** (Level 1) — add/remove/save/load books; swappable storage (JSON/CSV) and notifiers (email/SMS) via injected abstractions.
2. **Task 2 – Student Grade Management System** (Level 2) — same domain as the mini-project above, rebuilt so `Student` holds no calculation logic; `GradeCalculator` and `PassFailEvaluator` are separate injected classes; export format swappable in one line.
3. **Task 3 – E-Commerce Order Processing System** (Level 3, final) — the hardest of the three: `Product`/`Customer`/`Order` are pure data holders, `DiscountStrategy`/`ShippingStrategy`/`PaymentProcessor` are all swappable ABCs, and `OrderService` orchestrates everything through constructor injection with zero logic of its own. `final.txt` lists the specific traps (discount logic leaking into `Order`, validation leaking into `OrderService`, stock updates leaking into `Product`, etc.) this had to avoid.

## Capstone: `Conclusion/finance_tracker/`

A CLI personal finance tracker that ties everything together, split cleanly across modules:

| File | Responsibility |
| --- | --- |
| `models.py` | `Transaction` / `Budget` dataclasses with validated properties |
| `manager.py` | `FinanceManager` — add/remove transactions, budgets, balances |
| `storage.py` | `AbstractStorage` → `JSONStorage` |
| `reports.py` | category / period / summary reports |
| `decorators.py` | `log_action` — logs every mutating call |
| `utils.py` | validation and formatting helpers |
| `main.py` | `FinanceTrackerCLI` — the console loop |

Open item: `tests/test_manager.py` exists but is currently an empty stub — no test coverage yet despite the rest of the project being solid.

## Reference material

Built against the reading list in `materials.txt` (classes, inheritance, ABCs, decorators, SOLID, generators, magic methods, `*args`/`**kwargs`, comprehensions, `mypy`, and more) — pure standard library throughout, no third-party dependencies.
