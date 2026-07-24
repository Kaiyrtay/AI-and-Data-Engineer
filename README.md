# AI and Data Engineer

A self-directed path toward AI/data engineering that starts from solid software engineering fundamentals instead of jumping straight into ML or data tooling — the reasoning being that pipelines and systems built on shaky fundamentals don't hold up.

## Structure

| Folder                                                                                    | Focus                                                        |
| ----------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| [`1 Python OOP/`](./1%20Python%20OOP/README.md)                                           | Classes → inheritance → SOLID design → two capstone projects |
| [`2 Data Structure and Algorithms/`](./2%20Data%20Structure%20and%20Algorithms/README.md) | Arrays and linked lists, built from scratch                  |

Each folder has its own README with a full breakdown of what's inside.

## Approach

Weekly cadence, project-based — every topic ends in working code, not just notes. The SOLID capstones (`1 Python OOP/SOLID principles/`) were designed and judged against a written spec across three escalating difficulty levels, specifically to test whether the principles hold up under pressure and not just in the easy cases. Two full capstones tie the fundamentals together: a personal finance tracker CLI, and four data structures with complete Python dunder-method support. Everything runs on the standard library — no third-party dependencies.

## Rules

Every project here is held to the same bar — the full version lives in `Python_Engineering_Handbook.docx`. The core:

- One responsibility per function and per class; compose over inherit.
- Type hints and a docstring — with Big-O where it matters — on everything public.
- Fail fast with specific exceptions; never a bare `except` or a silent `None`.
- Cross-cutting behavior (logging, timing, validation) lives in decorators, not method bodies.
- Backend holds logic, frontend holds I/O; dependencies are injected, data holders stay dumb.
- `ruff`, `mypy`, and `pytest` enforce the mechanical half before every commit.
- Nothing is done until a test proves it, and every commit message says what changed and why.

The whole thing in one line: **know the cost and failure modes before you write the body, split by responsibility from the first line, let tools enforce the mechanical rules, and nothing ships until the test proves it.**

## Guiding philosophy

`The Zen of Python.txt` sits at the root as a reminder of the principles behind the code style used throughout: explicit over implicit, simple over complex, readable over clever...
