# DoublyLinkedList

## WHAT IS A DOUBLY LINKED LIST?

A linear data structure where each element (node) contains:

- A **value** (the data)
- A **next pointer** (link to the next node)
- A **prev pointer** (link to the previous node)
- No fixed size limit, grows dynamically

```
Visual:
None <- [10] <-> [20] <-> [30] <-> [40] -> None
         ↑                              ↑
       head                           tail
```

### Key Differences from Singly Linked List

| Feature     | Singly Linked      | Doubly Linked               |
| ----------- | ------------------ | --------------------------- |
| Traversal   | Forward only       | Forward & backward          |
| Navigation  | One direction      | Both directions             |
| Memory      | Less (one pointer) | More (two pointers)         |
| Performance | Faster for forward | Better bidirectional access |
| Reverse     | O(n) operation     | Built-in with `prev`        |

---

## \***\*init**()\*\* - CREATE LIST

```python
lst = DoublyLinkedList()
# Creates empty list
# head = None
# tail = None
# _size = 0
```

---

## ALL METHODS (Magic + Regular)

| #   | Method                         | What It Does                                | Example                                  |
| --- | ------------------------------ | ------------------------------------------- | ---------------------------------------- |
| 1   | `__init__()`                   | Create list                                 | `lst = DoublyLinkedList()`               |
| 2   | `__len__()`                    | Get size with len()                         | `len(lst)` returns 4                     |
| 3   | `__getitem__(index)`           | Get value with lst[i]                       | `lst[1]` returns 20                      |
| 4   | `__setitem__(index, value)`    | Set value with lst[i] = x                   | `lst[1] = 50`                            |
| 5   | `__iter__()`                   | Loop with for x in lst                      | `for x in lst: print(x)`                 |
| 6   | `__contains__(value)`          | Check with x in lst                         | `20 in lst` returns True/False           |
| 7   | `__eq__(other)`                | Compare with lst1 == lst2                   | `lst1 == lst2` returns True/False        |
| 8   | `__repr__()`                   | Debug print                                 | `repr(lst)`                              |
| 9   | `__str__()`                    | Print with print()                          | `print(lst)`                             |
| 10  | `size` (property)              | Get current items                           | `lst.size` returns 4                     |
| 11  | `prepend(value)`               | Add at beginning                            | `lst.prepend(5)`                         |
| 12  | `append(value)`                | Add at end                                  | `lst.append(50)`                         |
| 13  | `insert(index, value)`         | Add at specific position                    | `lst.insert(2, 25)`                      |
| 14  | `insert_before(target, value)` | Insert before target value                  | `lst.insert_before(20, 15)`              |
| 15  | `insert_after(target, value)`  | Insert after target value                   | `lst.insert_after(20, 25)`               |
| 16  | `del_head()`                   | Remove first node                           | `lst.del_head()`                         |
| 17  | `del_tail()`                   | Remove last node                            | `lst.del_tail()`                         |
| 18  | `del_at(index)`                | Remove at specific position                 | `lst.del_at(2)` returns bool             |
| 19  | `remove(value)`                | Remove first occurrence, return bool        | `lst.remove(20)` returns True/False      |
| 20  | `remove_all(value)`            | Remove all occurrences, return count        | `lst.remove_all(20)` returns 3           |
| 21  | `search(value)`                | Find node by value, return Node or None     | `lst.search(20)` returns Node/None       |
| 22  | `find_index(value)`            | Find index of value, return -1 if not found | `lst.find_index(20)` returns 1           |
| 23  | `count(value)`                 | Count occurrences of value                  | `lst.count(20)` returns 2                |
| 24  | `get(index)`                   | Get node at index                           | `lst.get(2)` returns Node                |
| 25  | `clear()`                      | Delete all, reset to empty                  | `lst.clear()`                            |
| 26  | `is_empty()`                   | Check if no items                           | `lst.is_empty()` returns True/False      |
| 27  | `is_circular()`                | Check if list is circular                   | `lst.is_circular()` returns True/False   |
| 28  | `has_duplicate()`              | Check for duplicate values                  | `lst.has_duplicate()` returns True/False |
| 29  | `first()`                      | Get first node                              | `lst.first()` returns Node               |
| 30  | `last()`                       | Get last node                               | `lst.last()` returns Node                |
| 31  | `reverse()`                    | Reverse list in-place                       | `lst.reverse()`                          |
| 32  | `traverse()`                   | Traverse forward and display                | `lst.traverse()` returns string          |
| 33  | `reverse_traverse()`           | Traverse backward and display               | `lst.reverse_traverse()` returns string  |
| 34  | `to_list()`                    | Convert to Python list                      | `lst.to_list()` returns [10,20,30]       |
| 35  | `from_list(lst)`               | Create from Python list                     | `dll.from_list([1,2,3])` returns bool    |
| 36  | `merge(other)`                 | Merge another DoublyLinkedList              | `lst1.merge(lst2)` returns self          |

---

## KEY CONCEPTS

### **Node Structure**

```python
Node:
  .value = 20
  .prev = Node(10)
  .next = Node(30)
```

### **Head & Tail**

```
head points to first node
tail points to last node

None <- [10] <-> [20] <-> [30] -> None
         ↑                  ↑
       head               tail
```

### **Forward Traversal**

```python
current = head
while current:
    print(current.value)
    current = current.next
```

### **Backward Traversal**

```python
current = tail
while current:
    print(current.value)
    current = current.prev
```

### **Negative Indexing**

- `lst[-1]` = last element
- `lst[-2]` = second-to-last
- `lst[-size]` = first element

### **Bidirectional Access**

DoublyLinkedList optimizes access by choosing the closest end:

```python
def get(self, index):
    if index < self.size // 2:
        return self._from_head(index)  # Traverse from head
    else:
        return self._from_tail(index)   # Traverse from tail
```

---

## EXAMPLE USAGE

```python
lst = DoublyLinkedList()

# Append values
lst.append(10)
lst.append(20)
lst.append(30)
print(lst)  # [10, 20, 30]

# Prepend value
lst.prepend(5)
print(lst)  # [5, 10, 20, 30]

# Insert at specific position
lst.insert(2, 15)
print(lst)  # [5, 10, 15, 20, 30]

# Insert before/after value
lst.insert_before(20, 17)
print(lst)  # [5, 10, 15, 17, 20, 30]

lst.insert_after(20, 25)
print(lst)  # [5, 10, 15, 17, 20, 25, 30]

# Access by index
print(lst[1])      # 10
print(lst[-1])     # 30

# Modify by index
lst[1] = 99
print(lst)  # [5, 99, 15, 17, 20, 25, 30]

# Check membership
print(20 in lst)   # True
print(999 in lst)  # False

# Find operations
print(lst.find_index(20))  # 4
print(lst.search(20))      # Node(20)
print(lst.count(5))        # 1

# Delete operations
lst.del_head()
print(lst)  # [99, 15, 17, 20, 25, 30]

lst.del_tail()
print(lst)  # [99, 15, 17, 20, 25]

lst.del_at(1)
print(lst)  # [99, 17, 20, 25]

lst.remove(17)
print(lst)  # [99, 20, 25]

# List properties
print(len(lst))             # 3
print(lst.is_empty())       # False
print(lst.has_duplicate())  # False

# Traversal operations
print(lst.traverse())          # [99, 20, 25]
print(lst.reverse_traverse())  # [25, 20, 99]

# Reverse list
lst.reverse()
print(lst)  # [25, 20, 99]

# Convert to Python list
print(lst.to_list())  # [25, 20, 99]

# Merge lists
lst1 = DoublyLinkedList()
lst1.append(1)
lst1.append(2)

lst2 = DoublyLinkedList()
lst2.append(3)
lst2.append(4)

lst1.merge(lst2)
print(lst1)  # [1, 2, 3, 4]
```

## PERFORMANCE CHARACTERISTICS

| Operation           | Time | Space | Notes                     |
| ------------------- | ---- | ----- | ------------------------- |
| append              | O(1) | O(1)  | Constant time             |
| prepend             | O(1) | O(1)  | Constant time             |
| insert (at index)   | O(n) | O(1)  | Linear traversal          |
| insert_before/after | O(n) | O(1)  | Must search for target    |
| delete (by index)   | O(n) | O(1)  | Optimized from ends       |
| delete (head/tail)  | O(1) | O(1)  | Direct removal            |
| remove (by value)   | O(n) | O(1)  | Linear search             |
| search              | O(n) | O(1)  | Linear search             |
| reverse             | O(n) | O(1)  | Pointer swapping          |
| get (index)         | O(n) | O(1)  | Optimized via closest end |
| Space               | -    | O(n)  | n nodes in list           |

---

## IMPLEMENTATION NOTES

### **Bidirectional Optimization**

The `get()` method intelligently chooses traversal direction:

```python
if index < self.size // 2:
    # Index closer to head - traverse forward
    return self._from_head(index)
else:
    # Index closer to tail - traverse backward
    return self._from_tail(index)
```

This reduces average traversal distance to O(n/2).

### **Merge Operation**

The `merge()` method connects two lists by linking the tail of the first to the head of the second:

```python
lst1.tail.next = lst2.head
lst2.head.prev = lst1.tail
lst1.tail = lst2.tail
lst1.size += lst2.size
```

### **Reverse Implementation**

In-place reversal by swapping `next` and `prev` pointers:

```python
def reverse(self):
    current = self.head
    self.head, self.tail = self.tail, self.head

    while current:
        current.next, current.prev = current.prev, current.next
        current = current.prev
```

## WHEN TO USE DOUBLY LINKED LIST

✅ **Use when:**

- You need bidirectional traversal
- Frequent insertions/deletions at both ends
- You need reverse iteration without recalculation
- Cache line friendly is less important than flexibility

❌ **Avoid when:**

- Need fast random access by index (use List/Array)
- Memory is extremely constrained (use SinglyLinkedList)
- Search performance is critical (use HashSet/Dict)
- Working with sorted data at scale (use balanced BST)

---
