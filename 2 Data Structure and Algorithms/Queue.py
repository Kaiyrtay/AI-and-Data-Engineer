"""queue.py — one Queue contract, two backings: array and linked list.

Defines an abstract `Queue` (the FIFO contract every queue obeys) and two
concrete implementations:

- `ArrayQueue`      — a resizable buffer. `enqueue` is amortized O(1), but
  `dequeue` shifts every remaining item down one slot, so it is O(n).
- `LinkedListQueue` — a singly linked list with head and tail pointers, so
  both `enqueue` (at the tail) and `dequeue` (at the head) are true O(1).

Items enter at the back and leave from the front; neither queue accepts
`None`, so a `None` slot always means "empty". Errors are specific
(`QueueEmptyError`) so callers can catch precisely instead of a bare `except`.
"""

from abc import ABC, abstractmethod
import math
from typing import Iterator


class QueueError(Exception):
    """Base class for queue errors — lets callers catch precisely."""


class QueueEmptyError(QueueError):
    """Raised by dequeue/peek on an empty queue."""


class Queue(ABC):
    """The FIFO contract every queue obeys, whatever its backing store."""

    @abstractmethod
    def enqueue(self, item):
        """Add `item` at the back of the queue."""

    @abstractmethod
    def dequeue(self):
        """Remove and return the front item. Raises if empty."""

    @abstractmethod
    def peek(self):
        """Return the front item without removing it. Raises if empty."""

    @abstractmethod
    def is_empty(self):
        """True when the queue holds no items."""

    @abstractmethod
    def size(self):
        """Number of items currently in the queue."""

    @abstractmethod
    def clear(self):
        """Remove every item."""

    @abstractmethod
    def to_array(self):
        """Return the items front -> back as a list."""

    @abstractmethod
    def __str__(self):
        """Human-facing text."""


class ArrayQueue(Queue):
    """FIFO queue over a resizable buffer.

    Items sit contiguously in `_array[0:size]`, so the front is always index
    0. `enqueue` writes at index `size` (amortized O(1), doubling when full);
    `dequeue` removes index 0 and shifts the rest down, so it is O(n). Every
    setter validates, so `capacity`, `size`, and `index_resize_factor` can
    never hold a nonsense value.
    """

    def __init__(self, capacity: int = 8, index_resize_factor: float = 2.0) -> None:
        """Start with an empty buffer of `capacity` slots. Time: O(n)."""
        self.capacity = capacity                    # routed through setters so they validate
        self.index_resize_factor = index_resize_factor
        self._array = [None] * capacity
        self.size = 0

    @property
    def capacity(self) -> int:
        """Total slots in the buffer (not the item count). Time: O(1)."""
        return self._capacity

    @capacity.setter
    def capacity(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Capacity must be an integer")
        if value <= 0:
            raise ValueError("Capacity must be a positive integer")
        self._capacity = value

    @property
    def index_resize_factor(self) -> float:
        """Multiplier applied to capacity on each resize. Time: O(1)."""
        return self._index_resize_factor

    @index_resize_factor.setter
    def index_resize_factor(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("Index resize factor must be a number")
        if value <= 1:                              # a multiplier must actually grow
            raise ValueError("Index resize factor must be greater than 1")
        self._index_resize_factor = value

    @property
    def size(self) -> int:
        """Live item count. Time: O(1)."""
        return self._size

    @size.setter
    def size(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Size must be an integer")
        if value < 0:                               # size can never go negative
            raise ValueError("Size cannot be negative")
        self._size = value

    @property
    def array(self) -> list:
        """The backing buffer itself — internal; exposed for inspection only."""
        return self._array

    def enqueue(self, item) -> None:
        """Add at the back, growing the buffer if full. Time: amortized O(1). Rejects None."""
        if item is None:
            raise ValueError("Cannot enqueue None value")
        if self.size == self.capacity:             # full -> grow first
            self._resize()
        self._array[self.size] = item              # back slot is index `size`
        self.size += 1

    def dequeue(self) -> object:
        """Remove and return the front. Time: O(n) — shifts the rest down. Raises if empty."""
        if self.is_empty():
            raise QueueEmptyError("Cannot dequeue from an empty queue")
        item = self._array[0]                       # front is always index 0
        for i in range(1, self.size):               # shift everything left one slot
            self._array[i - 1] = self._array[i]
        self._array[self.size - 1] = None           # clear the duplicated tail slot
        self.size -= 1
        return item

    def peek(self) -> object:
        """Return the front without removing it. Time: O(1). Raises if empty."""
        if self.is_empty():
            raise QueueEmptyError("Cannot peek at an empty queue")
        return self._array[0]

    def is_empty(self) -> bool:
        """True when no items. Time: O(1)."""
        return self.size == 0

    def is_full(self) -> bool:
        """True when the buffer has no free slot. Time: O(1)."""
        return self.size == self.capacity

    def clear(self) -> None:
        """Drop all items and reset to an empty buffer. Time: O(n)."""
        self._array = [None] * self.capacity
        self.size = 0

    def _resize(self) -> None:
        """Copy live items into a larger buffer. Time: O(n). Private — called when full."""
        new_capacity = math.ceil(self.capacity * self.index_resize_factor)
        new_array = [None] * new_capacity
        for i in range(self.size):                  # carry over live items only
            new_array[i] = self._array[i]
        self._array = new_array
        self.capacity = new_capacity

    def to_array(self) -> list:
        """Live items, front -> back, as a new list. Time: O(n)."""
        return self._array[:self.size]

    def __len__(self) -> int:
        """Live item count. Time: O(1)."""
        return self.size

    def __iter__(self) -> Iterator:
        """Yield items front -> back. Time: O(n)."""
        for i in range(self.size):
            yield self._array[i]

    def __repr__(self) -> str:
        return f"ArrayQueue(capacity={self.capacity}, size={self.size}, array={self._array})"

    def __str__(self) -> str:
        return repr(self)


class Node:
    """A single linked-list cell: a value plus a link to the next cell."""

    def __init__(self, data: object) -> None:
        self.data = data                            # routed through setters
        self.next = None

    @property
    def data(self) -> object:
        """The value stored in this node."""
        return self._data

    @data.setter
    def data(self, value: object) -> None:
        self._data = value

    @property
    def next(self) -> 'Node' | None:
        """The following node, or None at the tail."""
        return self._next

    @next.setter
    def next(self, value: 'Node' | None) -> None:
        if value is not None and not isinstance(value, Node):
            raise TypeError("Next must be a Node or None")
        self._next = value


class LinkedListQueue(Queue):
    """FIFO queue backed by a singly linked list with head and tail pointers.

    The head is the front (dequeue end) and the tail is the back (enqueue
    end), so both operations are true O(1) and the queue can never be "full".
    `dequeue`/`peek` hand back the `Node`; `peek_value` returns just the
    stored value.
    """

    def __init__(self) -> None:
        """Start empty. Time: O(1)."""
        self._head = None
        self._tail = None
        self.size = 0

    @property
    def size(self) -> int:
        """Number of nodes. Time: O(1)."""
        return self._size

    @size.setter
    def size(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Size must be an integer")
        if value < 0:                               # size can never go negative
            raise ValueError("Size cannot be negative")
        self._size = value

    @property
    def head(self) -> Node | None:
        """The front node, or None when empty. Time: O(1)."""
        return self._head

    @property
    def tail(self) -> Node | None:
        """The back node, or None when empty. Time: O(1)."""
        return self._tail

    def enqueue(self, item: object) -> None:
        """Add at the back (tail). Time: O(1). Rejects None."""
        if item is None:
            raise ValueError("Cannot enqueue None value")
        new_node = Node(item)
        if self.is_empty():                         # first item is both head and tail
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node              # link old tail to the new node
            self._tail = new_node
        self.size += 1

    def dequeue(self) -> "Node" | None:
        """Remove and return the front node. Time: O(1). Raises if empty."""
        if self.is_empty():
            raise QueueEmptyError("Cannot dequeue from an empty queue")
        item = self.head
        self._head = self._head.next                # front advances to the next node
        if self._head is None:                      # queue just emptied -> clear tail too
            self._tail = None
        self.size -= 1
        return item

    def peek(self) -> "Node":
        """Return the front node without removing it. Time: O(1). Raises if empty."""
        if self.is_empty():
            raise QueueEmptyError("Cannot peek at an empty queue")
        return self.head

    def peek_value(self) -> object:
        """Return the front value without removing it. Time: O(1). Raises if empty."""
        if self.is_empty():
            raise QueueEmptyError("Cannot peek at an empty queue")
        return self.head.data

    def is_full(self) -> bool:
        """Always False — a linked queue is never full. Time: O(1)."""
        return False

    def clear(self) -> None:
        """Drop every node. Time: O(1)."""
        self._head = None
        self._tail = None
        self.size = 0

    def to_array(self) -> list:
        """Values, front -> back, as a new list. Time: O(n)."""
        array = []
        if self.is_empty():
            return array
        current = self.head
        while current:                              # walk head -> tail
            array.append(current.data)
            current = current.next
        return array

    def is_empty(self) -> bool:
        """True when no nodes. Time: O(1)."""
        return self.size == 0

    def __len__(self) -> int:
        """Number of nodes. Time: O(1)."""
        return self.size

    def __iter__(self) -> Iterator:
        """Yield values front -> back. Time: O(n)."""
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __repr__(self) -> str:
        return f"LinkedListQueue(size={self.size}, head={self.head}, tail={self.tail})"

    def __str__(self) -> str:
        return repr(self)
