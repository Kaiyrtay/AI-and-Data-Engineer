"""load_balancing_algorithms.py — backend selection strategies for a load balancer.

Each strategy owns a list of backend servers and decides which one the next
request goes to. They share a single method, pick(), so they are
interchangeable behind the same interface.
"""

from __future__ import annotations


class RoundRobin:
    """Distribute requests evenly by cycling through backends in order.

    Single responsibility: return the next backend in a fixed rotation,
    looping back to the first after the last one.
    """

    def __init__(self, backends: list[str]) -> None:
        if not backends:                        # fail fast on empty input
            raise ValueError("backends cannot be empty")
        self._backends = backends               # private state
        self._index = 0

    def pick(self) -> str:
        """Return the next backend in rotation. Time: O(1). Space: O(1)."""
        backend = self._backends[self._index % len(self._backends)]
        self._index += 1
        return backend


if __name__ == "__main__":
    backends = ["server-1", "server-2", "server-3"]
    lb = RoundRobin(backends)

    print("===== Round Robin =====")
    n = 1
    while n <= 6:
        print(f"iter {n} -> {lb.pick()}")
        n += 1
