# DynamicArray

## WHAT IS DYNAMIC ARRAY?

Array that GROWS automatically. When it's full, it doubles in size. When it's mostly empty, it shrinks. No fixed size limit.

```
Starts: [_]  (capacity = 1, size = 0)

Add 10: [10]  (capacity = 1, size = 1) - FULL

Add 20: DOUBLE to 2
        [10, 20, _, _]  (capacity = 2, size = 2) - FULL

Add 30: DOUBLE to 4
        [10, 20, 30, _]  (capacity = 4, size = 3)

Add 40: [10, 20, 30, 40]  (capacity = 4, size = 4) - FULL

Add 50: DOUBLE to 8
        [10, 20, 30, 40, 50, _, _, _]  (capacity = 8, size = 5)
```

---

## **init**() - CREATE ARRAY

```python
arr = DynamicArray()
# Creates array that auto-grows
# _data = [None]
# _size = 0
# _capacity = 1
```

---

## ALL METHODS (Magic + Regular)

| #   | Method                      | What It Does                        | Example                                |
| --- | --------------------------- | ----------------------------------- | -------------------------------------- |
| 1   | `__init__()`                | Create array                        | `arr = DynamicArray()`                 |
| 2   | `__len__()`                 | Get size with len()                 | `len(arr)` returns 3                   |
| 3   | `__getitem__(index)`        | Get item with arr[i]                | `arr[1]` returns value                 |
| 4   | `__setitem__(index, value)` | Set item with arr[i] = x            | `arr[1] = 50`                          |
| 5   | `__iter__()`                | Loop with for x in arr              | `for x in arr: print(x)`               |
| 6   | `__contains__(value)`       | Check with x in arr                 | `20 in arr` returns True/False         |
| 7   | `__repr__()`                | Debug print                         | `repr(arr)`                            |
| 8   | `__str__()`                 | Print with print()                  | `print(arr)`                           |
| 9   | `size` (property)           | Get current items                   | `arr.size` returns 3                   |
| 10  | `capacity` (property)       | Get current max                     | `arr.capacity` returns 8               |
| 11  | `append(value)`             | Add at end, auto-grow               | `arr.append(10)`                       |
| 12  | `insert(index, value)`      | Add at position, auto-grow          | `arr.insert(1, 15)`                    |
| 13  | `pop(index=-1)`             | Remove and return item, auto-shrink | `arr.pop()` or `arr.pop(0)`            |
| 14  | `remove(value)`             | Remove by value, auto-shrink        | `arr.remove(20)`                       |
| 15  | `clear()`                   | Delete all, reset to capacity 1     | `arr.clear()`                          |
| 16  | `find(value)`               | Search, return -1 if not found      | `arr.find(20)` returns index or -1     |
| 17  | `index(value)`              | Search, error if not found          | `arr.index(20)` returns index or ERROR |
| 18  | `is_empty()`                | Check if no items                   | `arr.is_empty()` returns True/False    |
| 19  | `is_full()`                 | Check if size == capacity           | `arr.is_full()` returns True/False     |
| 20  | `to_list()`                 | Convert to Python list              | `arr.to_list()` returns [10, 20, 30]   |
| 21  | `_validate_index()`         | INTERNAL: Check valid index         | (don't use)                            |
| 22  | `_size_balance()`           | INTERNAL: Auto-grow or shrink       | (don't use)                            |
| 23  | `_resize()`                 | INTERNAL: Create new size           | (don't use)                            |
| 24  | `_left_shift()`             | INTERNAL: Shift items left          | (don't use)                            |
| 25  | `_right_shift()`            | INTERNAL: Shift items right         | (don't use)                            |

---

## KEY DIFFERENCE: AUTO-GROW vs AUTO-SHRINK

**Auto-Grow:**

- When `size == capacity`, doubles capacity
- Strategy: `capacity *= 2`

**Auto-Shrink:**

- When `size <= capacity // 4` (size uses 1/4 or less of capacity), halves capacity
- Strategy: `capacity //= 2`
- Example: capacity = 8, shrink when size <= 2

```python
arr = DynamicArray()
arr.append(1)         # size=1, capacity=1 (FULL - triggers double BEFORE add)
arr.append(2)         # DOUBLE to 2 first → size=2, capacity=2 (FULL)
arr.append(3)         # DOUBLE to 4 first → size=3, capacity=4
arr.append(4)         # size=4, capacity=4 (FULL)
arr.append(5)         # DOUBLE to 8 first → size=5, capacity=8
arr.pop()             # size=4, capacity=8
arr.pop()             # size=3, capacity=8
arr.pop()             # size=2, capacity=8 (2 <= 8//4? YES) → SHRINK to 4
                      # size=2, capacity=4
```

---

## MATERIALS

**Static vs Dynamic Arrays:**

https://medium.com/@erkmenefe/a-comprehensive-guide-to-arrays-understanding-static-dynamic-arrays-and-ram-storage-255226aed0c7

https://www.geeksforgeeks.org/dsa/difference-between-static-arrays-and-dynamic-arrays/

**Key Difference:**

- Static = Fixed size (locked, no growth)
- Dynamic = Auto-grows/shrinks (unlimited, flexible)
