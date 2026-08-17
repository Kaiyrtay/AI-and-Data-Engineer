"""Binary heap — a complete binary tree stored in a flat array.

One heap contract, two orderings. `Heap` (an ABC) owns all the machinery —
the array backing, sift-up / sift-down, push / pop / peek, heapify, and the
dunders — and each subclass supplies only `_higher`: which of two items belongs
closer to the root. `MinHeap` roots the smallest, `MaxHeap` the largest.

The array *is* the structure here (a heap is a complete tree with no gaps), so
a Python list is used as the backing on purpose — the same structural use of a
list justified for the B-tree node, not a wrapped container. Swap in your own
DynamicArray if you want zero stdlib containers.
"""

from abc import ABC, abstractmethod
from typing import Iterable, Iterator, List


class HeapError(Exception):
    """Base class for all heap errors."""


class HeapEmptyError(HeapError):
    """Raised on peek/pop against an empty heap."""


class Heap(ABC):
    """Array-backed binary heap. Subclasses fix the ordering via `_higher`."""

    def __init__(self, items: Iterable[int] | None = None) -> None:
        # Copy in, then heapify in O(n) rather than n pushes at O(n log n).
        self._data: List[int] = list(items) if items is not None else []
        if self._data:
            self._heapify()

    # --- the one thing subclasses define ---------------------------------
    @abstractmethod
    def _higher(self, a: int, b: int) -> bool:
        """True if `a` should sit closer to the root than `b`."""
        raise NotImplementedError

    # --- public API ------------------------------------------------------
    def push(self, value: int) -> None:
        """Insert a value. O(log n) — one sift-up along the tree height."""
        self._data.append(value)
        self._sift_up(len(self._data) - 1)

    def pop(self) -> int:
        """Remove and return the root (min or max). O(log n)."""
        if not self._data:
            raise HeapEmptyError("pop from empty heap")
        root = self._data[0]
        last = self._data.pop()          # remove the final leaf
        if self._data:                   # if items remain, reseat and sift down
            self._data[0] = last
            self._sift_down(0)
        return root

    def peek(self) -> int:
        """Return the root without removing it. O(1)."""
        if not self._data:
            raise HeapEmptyError("peek at empty heap")
        return self._data[0]

    # --- internals -------------------------------------------------------
    def _heapify(self) -> None:
        """Build-heap in O(n): sift-down every parent, last parent first."""
        for i in range(len(self._data) // 2 - 1, -1, -1):
            self._sift_down(i)

    def _sift_up(self, i: int) -> None:
        while i > 0:
            parent = (i - 1) // 2
            if self._higher(self._data[i], self._data[parent]):
                self._data[i], self._data[parent] = self._data[parent], self._data[i]
                i = parent
            else:
                break

    def _sift_down(self, i: int) -> None:
        n = len(self._data)
        while True:
            left, right, best = 2 * i + 1, 2 * i + 2, i
            if left < n and self._higher(self._data[left], self._data[best]):
                best = left
            if right < n and self._higher(self._data[right], self._data[best]):
                best = right
            if best == i:                # heap property restored
                break
            self._data[i], self._data[best] = self._data[best], self._data[i]
            i = best

    # --- container dunders ----------------------------------------------
    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)

    def __contains__(self, value: int) -> bool:
        return value in self._data      # O(n) — heaps don't index by value

    def __iter__(self) -> Iterator[int]:
        # NOTE: array order, NOT sorted order. Drain with pop() for sorted.
        return iter(self._data)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._data})"


class MinHeap(Heap):
    """Smallest value at the root."""

    def _higher(self, a: int, b: int) -> bool:
        return a < b


class MaxHeap(Heap):
    """Largest value at the root."""

    def _higher(self, a: int, b: int) -> bool:
        return a > b


def heapsort(values: Iterable[int]) -> List[int]:
    """Ascending sort via an in-place max-heap. O(n log n), not stable.

    Build a max-heap so the largest is at index 0, then repeatedly swap it to
    the end and sift-down the shrinking prefix — the sorted tail grows leftward.
    """
    a = list(values)
    n = len(a)

    def sift_down(root: int, size: int) -> None:
        while True:
            left, right, best = 2 * root + 1, 2 * root + 2, root
            if left < size and a[left] > a[best]:
                best = left
            if right < size and a[right] > a[best]:
                best = right
            if best == root:
                break
            a[root], a[best] = a[best], a[root]
            root = best

    for i in range(n // 2 - 1, -1, -1):   # build max-heap, O(n)
        sift_down(i, n)
    for end in range(n - 1, 0, -1):       # extract max to the tail, n times
        a[0], a[end] = a[end], a[0]
        sift_down(0, end)
    return a


if __name__ == "__main__":
    # min-heap pops in ascending order
    h = MinHeap([5, 3, 8, 1, 9, 2])
    assert h.peek() == 1
    assert [h.pop() for _ in range(len(h))] == [1, 2, 3, 5, 8, 9]

    # max-heap pops in descending order
    m = MaxHeap()
    for x in [5, 3, 8, 1, 9, 2]:
        m.push(x)
    assert m.peek() == 9
    assert [m.pop() for _ in range(len(m))] == [9, 8, 5, 3, 2, 1]

    # empty-heap edges
    for empty in (MinHeap(), MaxHeap()):
        try:
            empty.pop()
        except HeapEmptyError:
            pass
        else:
            raise AssertionError("expected HeapEmptyError")

    # heapsort matches sorted()
    import random
    data = [random.randint(-50, 50) for _ in range(200)]
    assert heapsort(data) == sorted(data)

    print("all heap self-tests passed")
