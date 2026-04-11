# SinglyLinkedList

## WHAT IS SINGLY LINKED LIST?

A linear data structure where each element (node) contains:

- A **value** (the data)
- A **next pointer** (link to the next node)
- No fixed size limit, grows dynamically

```
Visual:
[10] -> [20] -> [30] -> [40] -> None

head = Node(10)
tail = Node(40)
size = 4
```

---

## ****init**()** - CREATE LIST

```python
lst = SinglyLinkedList()
# Creates empty list
# head = None
# tail = None
# size = 0
```

---

## ALL METHODS (Magic + Regular)

| #   | Method                         | What It Does                                 | Example                                  |
| --- | ------------------------------ | -------------------------------------------- | ---------------------------------------- |
| 1   | `__init__()`                   | Create list                                  | `lst = SinglyLinkedList()`               |
| 2   | `__len__()`                    | Get size with len()                          | `len(lst)` returns 4                     |
| 3   | `__getitem__(index)`           | Get value with lst[i]                        | `lst[1]` returns 20                      |
| 4   | `__setitem__(index, value)`    | Set value with lst[i] = x                    | `lst[1] = 50`                            |
| 5   | `__iter__()`                   | Loop with for x in lst                       | `for x in lst: print(x)`                 |
| 6   | `__contains__(value)`          | Check with x in lst                          | `20 in lst` returns True/False           |
| 7   | `__eq__(other)`                | Compare with lst1 == lst2                    | `lst1 == lst2` returns True/False        |
| 8   | `__repr__()`                   | Debug print                                  | `repr(lst)`                              |
| 9   | `__str__()`                    | Print with print()                           | `print(lst)`                             |
| 10  | `size` (property)              | Get current items                            | `lst.size` returns 4                     |
| 11  | `capacity` (property)          | Not applicable (unlimited)                   | -                                        |
| 12  | `prepend(value)`               | Add at beginning                             | `lst.prepend(5)`                         |
| 13  | `append(value)`                | Add at end                                   | `lst.append(50)`                         |
| 14  | `add_at_position(value, i)`    | Add at specific position                     | `lst.add_at_position(25, 2)`             |
| 15  | `del_head()`                   | Remove first node                            | `lst.del_head()`                         |
| 16  | `del_tail()`                   | Remove last node                             | `lst.del_tail()`                         |
| 17  | `del_at_position(index)`       | Remove at specific position                  | `lst.del_at_position(2)`                 |
| 18  | `search(value)`                | Find node by value, return None if not found | `lst.search(20)` returns Node or None    |
| 19  | `find(value)` (alias)          | Find value, return index or -1               | (same as search)                         |
| 20  | `index(value)` (alias)         | Find value, error if not found               | (same as search)                         |
| 21  | `remove(value)`                | Remove first occurrence, return bool         | `lst.remove(20)` returns True/False      |
| 22  | `remove_all(value)`            | Remove all occurrences, return count         | `lst.remove_all(20)` returns 3           |
| 23  | `clear()`                      | Delete all, reset to empty                   | `lst.clear()`                            |
| 24  | `is_empty()`                   | Check if no items                            | `lst.is_empty()` returns True/False      |
| 25  | `is_full()` (N/A)              | Not applicable (unlimited size)              | -                                        |
| 26  | `first()`                      | Get first value                              | `lst.first()` returns 10                 |
| 27  | `last()`                       | Get last value                               | `lst.last()` returns 40                  |
| 28  | `reverse()`                    | Reverse list in-place                        | `lst.reverse()`                          |
| 29  | `to_list()`                    | Convert to Python list                       | `lst.to_list()` returns [10,20,30]       |
| 30  | `display()`                    | Print list                                   | `lst.display()`                          |
| 31  | `traverse()`                   | Traverse and display (alias)                 | `lst.traverse()`                         |
| 32  | `get(index)`                   | Get node at index (INTERNAL)                 | (don't use, use lst[i] instead)          |
| 33  | `convert_to_node(value)`       | INTERNAL: Convert to Node                    | (don't use)                              |
| 34  | `bounds_check(pos, allow_end)` | INTERNAL: Validate index                     | (don't use)                              |
| 35  | `insert_before(target, value)` | Insert before target value                   | `lst.insert_before(20, 15)`              |
| 36  | `insert_after(target, value)`  | Insert after target value                    | `lst.insert_after(20, 25)`               |
| 37  | `find_index(value)`            | Find index of value, return -1 if not found  | `lst.find_index(20)` returns 1           |
| 38  | `count(value)`                 | Count occurrences of value                   | `lst.count(20)` returns 2                |
| 39  | `is_circular()`                | Check if list is circular                    | `lst.is_circular()` returns True/False   |
| 40  | `get_middle()`                 | Get middle element value                     | `lst.get_middle()` returns 25            |
| 41  | `has_duplicate()`              | Check for duplicate values                   | `lst.has_duplicate()` returns True/False |
| 42  | `merge(other)`                 | Merge another list (deep copy)               | `lst1.merge(lst2)`                       |

---

## KEY CONCEPTS

### **Node Structure**

```python
Node:
  .value = 20
  .next = Node(30)
```

### **Head & Tail**

```
head points to first node
tail points to last node

[10] -> [20] -> [30]
 ↑                ↑
head            tail
```

### **Traversal**

```python
current = head
while current:
    print(current.value)
    current = current.next
```

### **Negative Indexing**

- `lst[-1]` = last element
- `lst[-2]` = second-to-last
- `lst[-size]` = first element

---

## EXAMPLE USAGE

```python
lst = SinglyLinkedList()

lst.append(10)
lst.append(20)
lst.append(30)
print(lst)  # [10 -> 20 -> 30]

lst.prepend(5)
print(lst)  # [5 -> 10 -> 20 -> 30]

lst.insert_before(20, 15)
print(lst)  # [5 -> 10 -> 15 -> 20 -> 30]

lst[1] = 99
print(lst)  # [5 -> 99 -> 15 -> 20 -> 30]

lst.remove(15)
print(lst)  # [5 -> 99 -> 20 -> 30]

lst.reverse()
print(lst)  # [30 -> 20 -> 99 -> 5]

print(len(lst))         # 4
print(20 in lst)        # True
print(lst.find_index(20))  # 1
print(lst.get_middle()) # 99
```
