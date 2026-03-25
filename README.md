# Personal Finance Tracker CLI

A simple command-line app to track your money. Add transactions, set budgets, and see where your money's going.

## Quick Start

```bash
python main.py
```

That's it! The app creates folders for data and logs automatically.

---

## What It Does

- **Add transactions** - Record income and expenses with categories
- **Track budgets** - Set spending limits for each category
- **See your balance** - Check overall balance and breakdown by category
- **View history** - List all transactions with filtering options
- **Generate reports** - Get a summary of spending by category

---

## Project Files

```
finance_tracker/
├── main.py          # The app you run
├── manager.py       # The logic that handles money stuff
├── models.py        # Transaction and Budget classes
├── storage.py       # Saves/loads your data
├── utils.py         # Helpers for validation and formatting
├── reports.py       # Makes the reports
├── decorators.py    # Logs what you're doing
└── constants.py     # Constants like "income" and "expense"
```

---

## Commands

**Type these in the app:**

- `add` - Add a transaction
- `remove` - Delete a transaction
- `list` - See all transactions (with filters)
- `balance` - Check your balance
- `budget` - Manage budgets
- `report` - See spending by category
- `help` - Get help
- `exit` - Save and quit

---

## Example Session

```
> add
Title: Groceries
Type (income/expense): expense
Amount: $50
Category: food
Recurring? (y/n): n
✓ Transaction added

> balance
Overall Balance: -$50.00

> budget
1. Add budget
2. Update spent
3. View budgets
Choose: 1
Category: food
Budget limit ($): 100
✓ Budget added: food: 0.0 / 100.0

> report
Summary Report:
Food  0.00  50.00  -50.00  1
```

---

## How It's Built

### OOP & Design Patterns

The app uses real programming concepts:

- **Classes** - `Transaction`, `Budget`, `FinanceManager`
- **Inheritance** - `AbstractStorage` base class, `JSONStorage` extends it
- **Decorators** - `@log_action` automatically logs actions
- **Generators** - `list_transactions()` uses `yield` for efficiency
- **Dataclasses** - Clean, type-safe models

### SOLID Principles

- **Single Responsibility** - Each class does one thing
- **Open/Closed** - Easy to add new storage types
- **Liskov Substitution** - Storage implementations swap seamlessly
- **Interface Segregation** - Small, focused interfaces
- **Dependency Inversion** - Depends on abstractions

---

## Data Storage

Everything's saved in JSON in the `storage/` folder:

```json
// transactions.json
[
  {
    "id": 1,
    "title": "Groceries",
    "type": "expense",
    "amount": 50.0,
    "category": "food",
    "date": "2024-03-28T14:32:15",
    "recurring": false
  }
]
```

---

## Logging

The app automatically logs all actions to `logs/{date}.log`. Logs are automatically rotated when they get too big.

```
[2024-03-28 14:32:15] add_transaction() | Args: ('Groceries', 'expense', 50.0, 'food', False) | Result: Transaction added
```

---

## Validation

All input is validated:

- Amounts must be positive numbers
- Titles and categories can't be empty
- Transaction type must be "income" or "expense"
- IDs must be positive integers

---

## What You Learn Here

1. **Object-Oriented Programming** - How to structure code with classes
2. **Design Patterns** - Decorators, abstract classes, generators
3. **File I/O** - Reading and writing JSON
4. **Error Handling** - Validation and try/except blocks
5. **Clean Code** - SOLID principles and best practices
6. **Testing** - Unit tests in `tests/test_manager.py`

---

## Files Explained

| File            | Does                            |
| --------------- | ------------------------------- |
| `main.py`       | The CLI - handles user input    |
| `manager.py`    | The brain - all the money logic |
| `models.py`     | Transaction and Budget classes  |
| `storage.py`    | Saves/loads to JSON             |
| `utils.py`      | Helper functions for validation |
| `reports.py`    | Creates summaries               |
| `decorators.py` | Logs actions automatically      |

---

## Running Tests

```bash
python -m pytest tests/test_manager.py -v
```

---

## Learning Materials

These are all the articles and resources I read while building this:

### Week 1: Object-Oriented Programming

- [Python Classes](https://realpython.com/python-classes/) - Core OOP concepts
- [Python Inheritance](https://www.datacamp.com/tutorial/python-inheritance) - Class hierarchies
- [Abstract Classes](https://medium.com/@prashampahadiya9228/abstract-classes-and-abstract-methods-in-python-e632ea34bc79) - Interface contracts
- [Python Decorators](https://www.thepythoncodingstack.com/p/demystifying-python-decorators) - Function wrapping
- [Decorators Primer](https://realpython.com/primer-on-python-decorators/) - Deep dive
- [The Zen of Python](https://pep20.org/) - Design philosophy

### Week 2: Advanced Concepts

- [File Management in Python](https://medium.com/@ayushkalathiya50/file-management-in-python-6613c0b57a85)
- [SOLID Principles](https://realpython.com/solid-principles-python/#the-solid-design-principles-in-python) - Design patterns
- [SOLID Video](https://www.youtube.com/watch?v=pTB30aXS77U)
- [SOLID Video 2](https://www.youtube.com/watch?v=k9u40DxhTTk)
- [Garbage Collection](https://www.geeksforgeeks.org/python/garbage-collection-python/)
- [Memory Management](https://www.geeksforgeeks.org/python/memory-management-in-python/)
- [Python Variables & Pointers](https://nedbatchelder.com/blog/202403/does_python_have_pointers)
- [Python Variables Explained](https://medium.com/analytics-vidhya/python-variables-are-pointers-not-containers-608644af9131)
- [Big O Notation](https://towardsdatascience.com/what-is-big-o-notation-and-why-you-should-care-5638895a1693/)
- [Big O Guide](https://medium.com/@rozy.sinha2711/understanding-big-o-notation-a-practical-guide-for-developers-45fcbbb5e84b)

### Week 3: Advanced Features & Testing

- [Magic Methods](https://www.tutorialsteacher.com/python/magic-methods-in-python)
- [Magic Methods Deep Dive](https://realpython.com/python-magic-methods/)
- [Iterators & Iterables](https://www.youtube.com/watch?v=hgQD2znCc_I)
- [Iterators Discussion](https://discuss.python.org/t/what-is-iterators-and-generators/105762/3)
- [Generators](https://www.w3schools.com/python/python_generators.asp)
- [Generators Guide](https://realpython.com/introduction-to-python-generators/)
- [SOLID Design](https://www.youtube.com/watch?v=Dx2SE4hYy4g)
- [Unit Testing](https://realpython.com/python-unittest/)

### Week 4: Functional Programming & Data Structures

- [Prime Numbers](https://www.geeksforgeeks.org/maths/prime-numbers/)
- [Prime Numbers Guide](https://brilliant.org/wiki/prime-numbers/)
- [Fibonacci Sequence](https://en.wikipedia.org/wiki/Fibonacci_sequence)
- [Context Managers](https://levelup.gitconnected.com/decoding-python-magic-enter-and-exit-bef77457606f)
- [Context Managers with Statement](https://realpython.com/python-with-statement/)
- [Dataclasses](https://realpython.com/ref/stdlib/dataclasses/)
- [Classmethod Reference](https://realpython.com/ref/builtin-functions/classmethod/)

### Week 5: Functional Programming & Type Hints

- [\*args and \*\*kwargs](https://www.w3schools.com/python/python_args_kwargs.asp)
- [args/kwargs Glossary](https://mimo.org/glossary/python/args-kwargs)
- [Lambda Functions](https://www.thepythoncodingstack.com/p/whats-all-the-fuss-about-python-lambda-functions)
- [Lambda Functions Codecademy](https://www.codecademy.com/article/python-lambda-function)
- [Map Function](https://thecode.media/funktsiya-map-v-python/)
- [Map Reference](https://realpython.com/ref/builtin-functions/map/)
- [Map Guide](https://realpython.com/python-map-function/)
- [Reduce Function](https://www.geeksforgeeks.org/python/reduce-in-python/)
- [MapReduce](https://en.wikipedia.org/wiki/MapReduce)
- [List Comprehensions](https://pyneng.readthedocs.io/ru/latest/book/08_useful_basics/x_comprehensions.html)
- [Comprehensions Guide](https://medium.com/@vinodkumargr/list-dictionary-and-set-comprehension-in-python-9823719a67da)
- [Set Comprehensions](https://realpython.com/python-set-comprehension/)
- [Dictionary Comprehensions](https://realpython.com/python-dictionary-comprehension/?utm_source=realpython&utm_medium=web&utm_campaign=related-post&utm_content=python-set-comprehension)
- [Tuples](https://www.w3schools.com/python/python_tuples.asp)
- [Choosing Data Structures](https://www.mygreatlearning.com/blog/choose-right-python-data-structure/)
- [Try Except](https://serveracademy.com/blog/python-try-except/)
- [Try Except Russian](https://pythonchik.ru/osnovy/python-try-except)
- [Mypy Type Checking](https://hrekov.com/blog/what-is-mypy-how-to-use-it)

---

## Requirements

- Python 3.8+
- No external libraries needed

---

**That's it!** This is how i tried to apply everything i learned about OOP and design patterns in a real project. It's not perfect, but it's a solid foundation to build on. Happy coding!
