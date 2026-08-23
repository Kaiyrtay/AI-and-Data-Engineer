# System Design

Working through system design from the core concepts up, building the pieces from scratch in pure Python — same bar as the rest of the repo: one job per class, type hints, a docstring with Big-O, fail fast on bad input. The reading list in `__materials.txt` sets the scope (scalability, availability, reliability, load balancers, load-balancing algorithms); the code so far covers the load balancers.

## Contents

| File                           | Topic                     | Picks a backend by…                            |
| ------------------------------ | ------------------------- | ---------------------------------------------- |
| `load-balancing-algorithms.py` | Load-balancing algorithms | Round robin — fixed rotation, O(1) per request |

## Load-balancing algorithms

A load balancer sits in front of a pool of backend servers and decides which one handles each incoming request. Each algorithm is a small class that owns the backend list and exposes one method, `pick()`, returning the backend for the next request — so the algorithms are interchangeable behind the same interface.

### Round Robin

Hands requests to backends in a fixed cyclic order — server 1, 2, 3, 1, 2, 3, … — looping back to the start after the last. It keeps an index counter and returns `backends[index % len(backends)]`, then advances; the modulo is what makes it wrap. Even distribution with no per-request state to inspect, so every `pick()` is O(1). An empty backend list raises `ValueError` at construction.

## Complexity

| Operation | Round Robin                 |
| --------- | --------------------------- |
| pick      | O(1)                        |
| Space     | O(n) backends + O(1) state  |

## Background reading

Reference links for this topic live in `__materials.txt` — the system design overview and the top-30 concepts list, then the core concepts: scalability, availability, reliability, load balancers, and load-balancing algorithms.
