"""stack.py — one Stack contract, two backings: array and linked list.

Defines an abstract `Stack` (the LIFO contract every stack obeys) and two
concrete implementations that differ only in how they store elements:

- `ArrayStack`  — a contiguous, resizable buffer. Fast and cache-friendly;
  `push` is amortized O(1) because the buffer occasionally doubles.
- `LinkedStack` — a singly linked list, pushed and popped at the head. Every
  operation is true O(1) with no resize, at the cost of one node per item.

Because both satisfy the same `Stack` interface, any caller that depends on
the contract works with either — swap one for the other and nothing else
changes. Errors are specific (`StackEmptyError`, `StackFullError`) so callers
can catch precisely instead of guarding on a bare `except`.
"""

from abc import ABC, abstractmethod
from typing import Iterator


class StackError(Exception):
    """Base class for stack errors — lets callers catch precisely."""


class StackEmptyError(StackError):
    """Raised by pop/peek on an empty stack."""


class StackFullError(StackError):
    """Raised by push when a fixed-capacity stack is full."""


class Stack(ABC):
    """The LIFO contract every stack obeys, whatever its backing store.

    Subclasses supply the five abstract methods; `is_empty` and `__str__` are
    defined once here in terms of that contract, so no subclass repeats them.
    """

    @abstractmethod
    def push(self, item: object) -> None:
        """Add `item` to the top of the stack."""

    @abstractmethod
    def pop(self) -> object:
        """Remove and return the top item. Raises if the stack is empty."""

    @abstractmethod
    def peek(self) -> object:
        """Return the top item without removing it. Raises if empty."""

    @abstractmethod
    def __len__(self) -> int:
        """Number of items currently on the stack."""

    @abstractmethod
    def __repr__(self) -> str:
        """Unambiguous, developer-facing representation."""

    def __str__(self) -> str:
        """Human-facing text; defaults to the repr unless a subclass overrides."""
        return repr(self)

    def is_empty(self) -> bool:
        """True when the stack holds no items. Time: O(1)."""
        return len(self) == 0


class ArrayStack(Stack):
    """LIFO stack over a contiguous, resizable buffer.

    `_count` does double duty: it is both the live-item count and the index of
    the next free slot, so the top always sits at `_count - 1`. The buffer
    carries spare `None` slots past the top; `push` fills the next one and
    doubles the buffer when it runs out, which makes append amortized O(1).
    """

    def __init__(self, capacity: int = 8) -> None:
        """Start with a fixed-size buffer. Raises ValueError if capacity < 1."""
        if capacity < 1:                          # fail fast on a nonsense size
            raise ValueError("Capacity must be at least 1")
        self._capacity = capacity
        self._buffer: list = [None] * capacity    # pre-allocated slots
        self._count = 0                           # live items == next free slot

    @property
    def capacity(self) -> int:
        """Total slots in the buffer (not the item count). Time: O(1)."""
        return self._capacity

    @property
    def buffer(self) -> list:
        """The backing buffer itself — internal; exposed for inspection only."""
        return self._buffer

    @property
    def count(self) -> int:
        """Live item count. Time: O(1)."""
        return self._count

    def push(self, item: object) -> None:
        """Add to the top, growing the buffer if full. Time: amortized O(1)."""
        if self.count == self.capacity:           # no room left -> grow first
            self._resize()
        self.buffer[self.count] = item            # top goes in the free slot
        self._count += 1

    def pop(self) -> object:
        """Remove and return the top. Time: O(1). Raises StackEmptyError if empty."""
        if self.is_empty():
            raise StackEmptyError
        self._count -= 1                          # top is now at the new _count
        item = self.buffer[self.count]
        # drop the reference so it can be GC'd
        self.buffer[self.count] = None
        return item

    def peek(self) -> object:
        """Return the top without removing it. Time: O(1). Raises if empty."""
        if self.is_empty():
            raise StackEmptyError
        # top sits one below the free slot
        return self.buffer[self.count - 1]

    def _resize(self, resize_multiplier: int = 2) -> None:
        """Copy into a larger buffer. Time: O(n). Private — called only when full."""
        if not isinstance(resize_multiplier, int):
            raise TypeError("resize_multiplier must be an integer")
        if resize_multiplier <= 1:                # a multiplier must actually grow
            raise ValueError("resize_multiplier must be greater than 1")
        new_buffer = [None] * self._capacity * resize_multiplier
        for i in range(self._count):              # carry over the live items only
            new_buffer[i] = self._buffer[i]
        self._buffer = new_buffer
        self._capacity *= resize_multiplier

    def __iter__(self) -> Iterator:
        """Yield items top -> bottom, live slots only. Time: O(n)."""
        for i in range(self.count - 1, -1, -1):
            yield self.buffer[i]

    def __len__(self) -> int:
        """Live item count. Time: O(1)."""
        return self.count

    def __repr__(self) -> str:
        return f"ArrayStack(capacity={self._capacity}, items={list(self)})"


class Node:
    """A single linked-list cell: a value plus a link to the next cell."""

    def __init__(self, data: object, next: 'Node' = None) -> None:
        self._data = data
        self._next = next

    @property
    def data(self) -> object:
        """The value stored in this node."""
        return self._data

    @property
    def next(self) -> 'Node' | None:
        """The following node, or None at the tail."""
        return self._next

    @data.setter
    def data(self, value: object) -> None:
        if value is None:                         # a node must hold a real value
            raise ValueError("Data cannot be None")
        self._data = value

    @next.setter
    def next(self, value: 'Node' | None) -> None:
        if not isinstance(value, Node) and value is not None:
            raise ValueError("Next must be a Node or None")
        self._next = value

    def __repr__(self) -> str:
        return f"Node(data={self.data}, next={repr(self.next)})"

    def __str__(self) -> str:
        return repr(self)


class LinkedList:
    """A minimal singly linked list — just enough to back a stack.

    Tracks only `head` and `size`; all growth happens at the head, so both
    `insert_at_head` and `remove_from_head` are O(1).
    """

    def __init__(self) -> None:
        self._head = None
        self._size = 0

    @property
    def head(self) -> 'Node':
        """The first node, or None when empty. Time: O(1)."""
        return self._head

    @property
    def size(self) -> int:
        """Number of nodes. Time: O(1)."""
        return self._size

    @head.setter
    def head(self, value: 'Node' | None) -> None:
        if not isinstance(value, Node) and value is not None:
            raise ValueError("Head must be a Node or None")
        self._head = value

    @size.setter
    def size(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:   # size can never go negative
            raise ValueError("Size must be a non-negative integer")
        self._size = value

    def insert_at_head(self, data: object) -> None:
        """Prepend a new node. Time: O(1). Raises ValueError if data is None."""
        if data is None:
            raise ValueError("Data cannot be None")
        # new node points at the old head
        new_head = Node(data, self.head)
        self.head = new_head
        self.size += 1

    def remove_from_head(self) -> 'Node':
        """Unlink and return the head node. Time: O(1). Raises if empty."""
        if self.head is None:
            raise ValueError("LinkedList is empty")
        removed_node = self.head
        self.head = self.head.next                # head advances to the next node
        self.size -= 1
        return removed_node

    def __len__(self) -> int:
        return self.size

    def __str__(self) -> str:
        nodes = []
        current = self.head
        while current is not None:                # walk head -> tail
            nodes.append(str(current))
            current = current.next
        return f"LinkedList(size={self.size}, nodes=[{', '.join(nodes)}])"


class LinkedStack(Stack):
    """LIFO stack backed by a linked list (composition, not inheritance).

    The list's head is the stack's top, so push/pop/peek are all O(1) and the
    stack can never be "full". `pop`/`peek` return the Node itself;
    `pop_value`/`peek_value` return just the stored value.
    """

    def __init__(self) -> None:
        self._list = LinkedList()

    @property
    def list(self) -> LinkedList:
        """The backing linked list — internal detail."""
        return self._list

    @list.setter
    def list(self, value: LinkedList) -> None:
        if not isinstance(value, LinkedList):
            raise StackEmptyError("Value must be a LinkedList")
        self._list = value

    def push(self, item: object) -> None:
        """Add to the top (the list head). Time: O(1)."""
        self.list.insert_at_head(item)

    def pop(self) -> object:
        """Remove and return the top Node. Time: O(1). Raises if empty."""
        removed_node = self.list.remove_from_head()
        return removed_node

    def pop_value(self) -> object:
        """Remove and return the top value. Time: O(1). Raises if empty."""
        removed_node = self.list.remove_from_head()
        return removed_node.data

    def peek(self) -> object:
        """Return the top Node without removing it. Time: O(1). Raises if empty."""
        if self.is_empty():
            raise StackEmptyError
        return self.list.head

    def peek_value(self) -> object:
        """Return the top value without removing it. Time: O(1). Raises if empty."""
        if self.is_empty():
            raise StackEmptyError
        return self.list.head.data

    def __len__(self) -> int:
        return self.list.size

    def __repr__(self) -> str:
        return f"LinkedStack(size={self.list.size}, items={list(self)})"

    def is_empty(self) -> bool:
        """True when the stack holds no items. Time: O(1)."""
        return self.list.size == 0
