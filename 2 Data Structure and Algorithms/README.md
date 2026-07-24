# Data Structures & Algorithms

Four core data structures, built from scratch in pure Python — no wrapping `list` or `collections` internally. Each one implements the full set of Python dunder methods (`__len__`, `__getitem__`, `__setitem__`, `__iter__`, `__contains__`, `__eq__`, `__str__`, `__repr__`) so it behaves like a native container, not a toy class.

## Contents

| File | Structure | Backing | Grows? |
| --- | --- | --- | --- |
| `StaticArray.py` | Static array | Fixed-capacity slot list | No — raises once full |
| `DynamicArray.py` | Dynamic array | Resizable buffer | Yes — doubles/halves, amortized O(1) append |
| `SinglyLinkedList.py` | Singly linked list | `Node` with `.next` only | Yes — unbounded |
| `DoublyLinkedList.py` | Doubly linked list | `Node` with `.next` and `.prev` | Yes — unbounded |

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

---

## Complexity

| Operation | StaticArray | DynamicArray | SinglyLinkedList | DoublyLinkedList |
| --- | --- | --- | --- | --- |
| Access by index | O(1) | O(1) | O(n) | O(n) — O(n/2) avg via `get()` |
| Append | O(1) (or error if full) | O(1) amortized | O(1) (tail tracked) | O(1) |
| Prepend | O(n) shift | O(n) shift | O(1) | O(1) |
| Insert at index | O(n) shift | O(n) shift | O(n) | O(n) |
| Delete head | O(n) shift | O(n) shift | O(1) | O(1) |
| Delete tail | O(1) | O(1) | O(n) — no back-pointer | O(1) |
| Search by value | O(n) | O(n) | O(n) | O(n) |
| Space overhead | none (fixed) | unused capacity | 1 pointer/node | 2 pointers/node |

## Background reading

Reference links used while building these live in `__materials.txt` — arrays (static vs. dynamic, RAM storage) and linked list fundamentals.
