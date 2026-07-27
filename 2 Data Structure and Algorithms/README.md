# Data Structures & Algorithms

Five data structures, built from scratch in pure Python — no wrapping `list`, `dict`, or `collections` internally. Each implements the Python dunder methods that fit its shape (`__len__`, `__iter__`, `__contains__`, `__eq__`, `__str__`, `__repr__`, plus `__getitem__`/`__setitem__` on the indexed sequences) so it behaves like a native container, not a toy class.

## Contents

| File                  | Structure                | Backing                               | Grows?                                      |
| --------------------- | ------------------------ | ------------------------------------- | ------------------------------------------- |
| `StaticArray.py`      | Static array             | Fixed-capacity slot list              | No — raises once full                       |
| `DynamicArray.py`     | Dynamic array            | Resizable buffer                      | Yes — doubles/halves, amortized O(1) append |
| `SinglyLinkedList.py` | Singly linked list       | `Node` with `.next` only              | Yes — unbounded                             |
| `DoublyLinkedList.py` | Doubly linked list       | `Node` with `.next` and `.prev`       | Yes — unbounded                             |
| `HashTable.py`        | Hash table (set of keys) | Prime-sized slot array / bucket lists | Yes — rehashes at 0.75 load factor          |

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

## Background reading

Reference links used while building these live in `__materials.txt` — arrays (static vs. dynamic, RAM storage) and linked list fundamentals.
