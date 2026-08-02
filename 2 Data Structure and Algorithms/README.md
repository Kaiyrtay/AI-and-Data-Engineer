# Data Structures & Algorithms

Eight structures, built from scratch in pure Python — no wrapping `list`, `dict`, or `collections` internally. The first five are containers; then `Stack` and `Queue` are abstract data types with two backings each, and `Tree` is a binary tree with its traversals as strategy classes. Each implements the Python dunder methods that fit its shape (`__len__`, `__iter__`, `__contains__`, `__eq__`, `__str__`, `__repr__`, plus `__getitem__`/`__setitem__` on the indexed sequences) so it behaves like a native container, not a toy class.

## Contents

| File                  | Structure                            | Backing                               | Grows?                                      |
| --------------------- | ------------------------------------ | ------------------------------------- | ------------------------------------------- |
| `StaticArray.py`      | Static array                         | Fixed-capacity slot list              | No — raises once full                       |
| `DynamicArray.py`     | Dynamic array                        | Resizable buffer                      | Yes — doubles/halves, amortized O(1) append |
| `SinglyLinkedList.py` | Singly linked list                   | `Node` with `.next` only              | Yes — unbounded                             |
| `DoublyLinkedList.py` | Doubly linked list                   | `Node` with `.next` and `.prev`       | Yes — unbounded                             |
| `HashTable.py`        | Hash table (set of keys)             | Prime-sized slot array / bucket lists | Yes — rehashes at 0.75 load factor          |
| `Stack.py`            | Stack (LIFO), array- & linked-backed | Resizable buffer / singly linked list | Yes — array doubles; linked is unbounded    |
| `Queue.py`            | Queue (FIFO), array- & linked-backed | Resizable buffer / singly linked list | Yes — array grows; linked is unbounded      |
| `trees/Tree.py`       | Binary tree + traversals             | `Node` with `.left` / `.right`        | Yes — unbounded                             |

---

## StaticArray

Fixed capacity set at construction (`StaticArray(capacity)`). `append`/`insert` raise `IndexError`-style errors once full instead of growing.

**Methods:** `append`, `insert`, `pop`, `remove`, `clear`, `index`, `find`, `is_full`, `is_empty`, `to_list`, plus `capacity`/`size` properties and full dunder support. Internally, `insert`/`pop` shift elements left/right (`_left_shift` / `_right_shift`) to keep the array contiguous.

## DynamicArray

Same public interface as `StaticArray`, but never raises on overflow — `_size_balance` / `_resize` double the backing buffer when full and halve it when usage drops, so `append` is amortized O(1) instead of a hard error.

## SinglyLinkedList

Forward-only list with a tracked `head` **and** `tail`. Beyond the basics (`prepend`, `append`, `add_at_position`, `del_head`, `del_tail`, `del_at_position`, `search`), it includes `reverse`, `merge`, `insert_before`/`insert_after`, `find_index`, `count`, `remove`/`remove_all`, and a couple of interview-staple extras: `is_circular` (Floyd's cycle detection), `get_middle` (fast/slow pointer), and `has_duplicate`.

## DoublyLinkedList

The most complete of the four — 36 methods, `prev`/`next` on every node. Same feature set as `SinglyLinkedList` plus `insert`(at index), `reverse_traverse`, and `from_list`. Its `get(index)` is the standout: it picks whichever end (head or tail) is closer to the target index and traverses from there, so average lookup cost is O(n/2) rather than O(n):

```python
def get(self, index):
    if index < self.size // 2:
        return self._from_head(index)   # closer to head
    else:
        return self._from_tail(index)   # closer to tail
```

Negative indexing (`lst[-1]`), in-place `reverse()` via pointer-swap, and `merge()` (splicing one list onto the tail of another) are also implemented.

## HashTable

Four collision-handling techniques behind one abstract interface. `HashTable` (an ABC) owns the shared machinery — load factor, resize policy, the `insert`/`search`/`delete` API, and the dunders — and each subclass supplies only how a key is placed, found, and removed:

- `SeparateChainingHashTable` — open hashing; each bucket is a list, collisions chain.
- `LinearProbing` — closed hashing; probe `home, home+1, home+2, …` (simple, but clusters).
- `QuadraticProbing` — probe `home + 1, +4, +9, …` to break up that clustering.
- `DoubleHashing` — a second hash sets the stride, so colliding keys diverge onto different paths.

Deletion uses tombstones (a `_DELETED` sentinel) so removing a key never severs a probe chain: search treats a tombstone as occupied and keeps going, while insert is free to reuse it. The table holds a **prime** capacity and rehashes every live key into the next prime once the load factor reaches 0.75, which keeps operations near O(1). Being a set of keys, it supports the container dunders except `__getitem__`/`__setitem__`, which don't apply to unordered keys. Run `python HashTable.py` to execute the built-in self-tests — empty / one / many-with-resize / duplicate / delete-and-reinsert / invalid input / deliberate failure, across all four techniques.

## Stack

One LIFO contract, two backings. `Stack` (an ABC) fixes the interface — `push`, `pop`, `peek`, `__len__`, `__repr__`, plus a shared `is_empty` and `__str__` — and two classes fill it in differently:

- `ArrayStack` — a contiguous, resizable buffer. `_count` does double duty as the item count **and** the index of the next free slot, so the top always sits at `_count - 1`. `push` fills the free slot and doubles the buffer (`_resize`) when it runs out, making append amortized O(1); `pop` clears the vacated slot so its reference can be garbage-collected.
- `LinkedStack` — composition over a hand-rolled `Node`/`LinkedList`, pushing and popping at the head. Every operation is true O(1) with no resize, and it can never be "full". `pop`/`peek` hand back the `Node`; `pop_value`/`peek_value` return just the stored value.

Errors are specific — `StackEmptyError` on an empty `pop`/`peek`, `StackFullError` reserved for a fixed-capacity variant — all under a `StackError` base, so callers catch precisely instead of a bare `except`. Because both stacks satisfy the same interface, any caller that depends on the contract works with either; swapping `ArrayStack` for `LinkedStack` changes nothing else.

## Queue

One FIFO contract, two backings. `Queue` (an ABC) fixes the interface — `enqueue`, `dequeue`, `peek`, `is_empty`, `size`, `clear`, `to_array`, `__str__` — and two classes implement it differently:

- `ArrayQueue` — a resizable buffer with the front pinned at index 0. `enqueue` writes at index `size` and doubles the buffer when full (amortized O(1)); `dequeue` removes the front and shifts every remaining item down one slot, so it is O(n). Neither operation accepts `None`, so a `None` slot always means "empty".
- `LinkedListQueue` — a singly linked list holding both `head` (front) and `tail` (back) pointers. `enqueue` links onto the tail and `dequeue` unlinks the head, both true O(1); it can never be "full". `dequeue`/`peek` hand back the `Node`; `peek_value` returns just the stored value.

Errors are specific — `QueueEmptyError` on an empty `dequeue`/`peek` — under a `QueueError` base. Because both queues satisfy the same interface, any caller depending on the contract works with either: the array one trades an O(n) dequeue for cache-friendly contiguity, the linked one trades a pointer per node for true O(1) at both ends.

## Tree

A binary tree whose four traversals are swappable strategy classes. `Node` holds a value and `left`/`right` children; `Tree` owns the root and answers the structural questions — `height` (edges on the longest root→leaf path, −1 when empty), `depth` (edges from the root down to a given node, 0 at the root), and `degree` (a node's child count, 0–2).

`Tree` also classifies its own shape (each O(n)):

- `is_full` — every node has 0 or 2 children, never exactly 1.
- `is_perfect` — full **and** every leaf sits at the same depth.
- `is_complete` — every level full except the last, which fills left to right (tested with the array-index trick: a node at `i` has children at `2i+1`/`2i+2`).
- `is_balanced` — left/right subtree heights differ by ≤ 1 at every node (one O(n) pass, using `-2` as an "unbalanced" sentinel).
- `is_degenerate` — every node has at most one child; a chain that may switch sides (also called *pathological*).
- `is_skewed` — a degenerate tree leaning entirely one way, i.e. `is_left_skewed` or `is_right_skewed`.

The traversals sit behind a `TreeTraversal` ABC, so an order is chosen by picking a class rather than passing a flag, and a new order can be added without touching the tree:

- `InorderTraversal` — left → node → right (yields sorted order on a BST).
- `PreorderTraversal` — node → left → right (parent before its children).
- `PostorderTraversal` — left → right → node (parent after both children).

All three are recursive: O(n) time and O(h) call-stack space for height h. Node equality is structural (same value and same subtrees). Run `python Tree.py` for the built-in self-tests across the traversals, `height`/`depth`/`degree`, and the shape predicates.

---

## Complexity

| Operation       | StaticArray             | DynamicArray    | SinglyLinkedList       | DoublyLinkedList              |
| --------------- | ----------------------- | --------------- | ---------------------- | ----------------------------- |
| Access by index | O(1)                    | O(1)            | O(n)                   | O(n) — O(n/2) avg via `get()` |
| Append          | O(1) (or error if full) | O(1) amortized  | O(1) (tail tracked)    | O(1)                          |
| Prepend         | O(n) shift              | O(n) shift      | O(1)                   | O(1)                          |
| Insert at index | O(n) shift              | O(n) shift      | O(n)                   | O(n)                          |
| Delete head     | O(n) shift              | O(n) shift      | O(1)                   | O(1)                          |
| Delete tail     | O(1)                    | O(1)            | O(n) — no back-pointer | O(1)                          |
| Search by value | O(n)                    | O(n)            | O(n)                   | O(n)                          |
| Space overhead  | none (fixed)            | unused capacity | 1 pointer/node         | 2 pointers/node               |

`HashTable` is a set of keys, not an indexed sequence, so its operations don't map onto the columns above — it gets its own table:

| Operation | Average | Worst case                                                              |
| --------- | ------- | ----------------------------------------------------------------------- |
| Insert    | O(1)    | O(n) — clustering or a resize                                           |
| Search    | O(1)    | O(n) — every key on one probe path / in one bucket                      |
| Delete    | O(1)    | O(n)                                                                    |
| Space     | O(n)    | O(n) — chaining adds per-node list overhead; probing stays in one array |

The 0.75 resize threshold and prime sizing are what keep the average at O(1); adversarial hashing or a pathological load is what pushes any of the four to O(n).

`Stack` is an ADT, not an indexed sequence, so like `HashTable` it gets its own line — every operation touches only the top:

| Operation      | ArrayStack                         | LinkedStack    |
| -------------- | ---------------------------------- | -------------- |
| push           | O(1) amortized — doubles when full | O(1)           |
| pop            | O(1)                               | O(1)           |
| peek           | O(1)                               | O(1)           |
| Space overhead | unused buffer capacity             | 1 pointer/node |

`Queue` is an ADT too — items enter at the back and leave from the front:

| Operation      | ArrayQueue                         | LinkedListQueue |
| -------------- | ---------------------------------- | --------------- |
| enqueue        | O(1) amortized — doubles when full | O(1)            |
| dequeue        | O(n) — shifts the rest down        | O(1)            |
| peek           | O(1)                               | O(1)            |
| Space overhead | unused buffer capacity             | 1 pointer/node  |

`Tree`'s traversals visit every node, and its structural queries walk the tree:

| Operation               | Binary tree           |
| ----------------------- | --------------------- |
| Traversal (in/pre/post) | O(n) time, O(h) stack |
| height                  | O(n)                  |
| depth                   | O(n)                  |
| degree                  | O(1)                  |

## Background reading

Reference links used while building these live in `__materials.txt` — arrays (static vs. dynamic, RAM storage) and linked list fundamentals.
