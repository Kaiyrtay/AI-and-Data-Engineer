# StaticArray

## WHAT IS STATIC ARRAY?

Fixed-size container. Once created, size is locked forever. Can't grow or shrink.

```
Capacity = 5 (max items)
Size = current items
Example: [10, 20, 30, _, _]  (3 items in 5 slots)
```

---

## **init**(capacity) - CREATE ARRAY

```python
arr = StaticArray(5)
# Creates array with max size 5
# _data = [None, None, None, None, None]
# _size = 0
```

---

## METHODS (Magic + Regular)

| #   | Method                      | What It Does                   | Example                                |
| --- | --------------------------- | ------------------------------ | -------------------------------------- |
| 1   | `__init__(capacity)`        | Create array                   | `arr = StaticArray(5)`                 |
| 2   | `__len__()`                 | Get size with len()            | `len(arr)` returns 3                   |
| 3   | `__getitem__(index)`        | Get item with arr[i]           | `arr[1]` returns value                 |
| 4   | `__setitem__(index, value)` | Set item with arr[i] = x       | `arr[1] = 50`                          |
| 5   | `__iter__()`                | Loop with for x in arr         | `for x in arr: print(x)`               |
| 6   | `__contains__(value)`       | Check with x in arr            | `20 in arr` returns True/False         |
| 7   | `__repr__()`                | Debug print                    | `repr(arr)`                            |
| 8   | `__str__()`                 | Print with print()             | `print(arr)`                           |
| 9   | `capacity` (property)       | Get max size                   | `arr.capacity` returns 5               |
| 10  | `size` (property)           | Get current items              | `arr.size` returns 3                   |
| 11  | `append(value)`             | Add at end                     | `arr.append(10)`                       |
| 12  | `insert(index, value)`      | Add at position                | `arr.insert(1, 15)`                    |
| 13  | `pop(index=-1)`             | Remove and return item         | `arr.pop()` or `arr.pop(0)`            |
| 14  | `remove(value)`             | Remove by value                | `arr.remove(20)`                       |
| 15  | `clear()`                   | Delete all items               | `arr.clear()`                          |
| 16  | `find(value)`               | Search, return -1 if not found | `arr.find(20)` returns index or -1     |
| 17  | `index(value)`              | Search, error if not found     | `arr.index(20)` returns index or ERROR |
| 18  | `is_empty()`                | Check if no items              | `arr.is_empty()` returns True/False    |
| 19  | `is_full()`                 | Check if at capacity           | `arr.is_full()` returns True/False     |
| 20  | `to_list()`                 | Convert to Python list         | `arr.to_list()` returns [10, 20, 30]   |
| 21  | `_validate_index()`         | INTERNAL: Check valid index    | (don't use)                            |
| 22  | `_ensure_not_full()`        | INTERNAL: Check space left     | (don't use)                            |
| 23  | `_left_shift()`             | INTERNAL: Shift items left     | (don't use)                            |
| 24  | `_right_shift()`            | INTERNAL: Shift items right    | (don't use)                            |

---

## MATERIALS

**Static vs Dynamic Arrays:**

https://medium.com/@erkmenefe/a-comprehensive-guide-to-arrays-understanding-static-dynamic-arrays-and-ram-storage-255226aed0c7

https://www.geeksforgeeks.org/dsa/difference-between-static-arrays-and-dynamic-arrays/
