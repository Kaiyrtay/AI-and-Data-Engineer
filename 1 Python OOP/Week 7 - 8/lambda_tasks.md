# Lambda / Map / Filter / Reduce — 20 Tasks to Solve

> Rules: use ONLY `lambda`, `map`, `filter`, `reduce`. No loops. No list comprehensions.

---

### 1.

Given a nested list, flatten it, keep only odd numbers, return their squares.

```python
from functools import reduce
nested = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# expected: [1, 9, 25, 49, 81]
```

---

### 2.

Count how many times each word appears. Return a dict.

```python
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
# expected: {'apple': 3, 'banana': 2, 'cherry': 1}
```

---

### 3.

Apply a list of functions one after another to a starting value.

```python
fns = [lambda x: x * 2, lambda x: x + 10, lambda x: x ** 2]
start = 3
# expected: 256
```

---

### 4.

Group numbers by their remainder when divided by 3. Return a dict.

```python
nums = list(range(1, 16))
# expected: {1: [1,4,7,10,13], 2: [2,5,8,11,14], 0: [3,6,9,12,15]}
```

---

### 5.

Transpose a matrix (flip rows and columns).

```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# expected: [[1,4,7], [2,5,8], [3,6,9]]
```

---

### 6.

Keep only valid emails. Valid = has `@` and a `.` after the `@`.

```python
emails = ["user@mail.com", "bademail", "a@b.c", "noatsign.com", "x@y"]
# expected: ['user@mail.com', 'a@b.c']
```

---

### 7.

Return a running cumulative sum list.

```python
nums = [1, 2, 3, 4, 5]
# expected: [1, 3, 6, 10, 15]
```

---

### 8.

Flatten a list no matter how deeply nested it is.

```python
deep = [1, [2, [3, [4, [5]]]]]
# expected: [1, 2, 3, 4, 5]
```

---

### 9.

Shift every letter in a string by 3 positions forward. Leave spaces as-is.

```python
text = "hello world"
# expected: 'khoor zruog'
```

---

### 10.

From two lists, get all pairs where the product > 10 and both numbers are odd.

```python
a = [1, 3, 5, 7]
b = [2, 3, 4, 5]
# expected: [(3,5), (5,3), (5,5), (7,3), (7,5)]
```

---

### 11.

Swap all keys and values in a dict.

```python
d = {"a": 1, "b": 2, "c": 3}
# expected: {1: 'a', 2: 'b', 3: 'c'}
```

---

### 12.

Zip two lists into a dict without using `dict()`.

```python
keys = ["x", "y", "z"]
vals = [10, 20, 30]
# expected: {'x': 10, 'y': 20, 'z': 30}
```

---

### 13.

Find all numbers that appear more than once.

```python
nums = [1, 2, 3, 2, 4, 3, 5]
# expected: [2, 3]
```

---

### 14.

Normalize a list so all values are between 0 and 1.

```python
data = [10, 20, 30, 40, 50]
# expected: [0.0, 0.25, 0.5, 0.75, 1.0]
```

---

### 15.

Split a list into chunks of size n.

```python
lst = list(range(1, 11))
n = 3
# expected: [[1,2,3], [4,5,6], [7,8,9], [10]]
```

---

### 16.

Flatten a dict where every value is a list, into a single list.

```python
d = {"a": [1, 2], "b": [3, 4], "c": [5]}
# expected: [1, 2, 3, 4, 5]
```

---

### 17.

Find the longest word in a list.

```python
words = ["cat", "elephant", "dog", "rhinoceros", "ox"]
# expected: 'rhinoceros'
```

---

### 18.

Apply a list of filter conditions one after another to the same list.

```python
nums = list(range(1, 51))
conditions = [
    lambda x: x % 2 == 0,
    lambda x: x % 3 == 0,
    lambda x: x > 20
]
# expected: [24, 30, 36, 42, 48]
```

---

### 19.

Generate a multiplication table for n=4 as a flat list.

```python
n = 4
# expected: [1,2,3,4, 2,4,6,8, 3,6,9,12, 4,8,12,16]
```

---

### 20.

Count how many times each number appears. Return a dict. Use ONLY reduce.

```python
data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
# expected: {1: 1, 2: 2, 3: 3, 4: 4}
```

---

### BONUS

Filter primes, square them, sum everything — in one single expression.

```python
nums = list(range(2, 30))
# expected: 2397
```
