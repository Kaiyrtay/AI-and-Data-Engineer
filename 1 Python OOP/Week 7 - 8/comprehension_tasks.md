# Comprehensions — 15 Tasks to Solve

> Covers: dict, set, nested, conditional comprehensions.

---

### 1.

From a list of words, build a dict of `word → length`. Skip words shorter than 4 letters.

```python
words = ["cat", "elephant", "dog", "rhinoceros", "ox", "tiger"]
# expected: {'elephant': 8, 'rhinoceros': 10, 'tiger': 5}
```

---

### 2.

From two lists, build a dict of `number → square` but only for numbers that appear in both lists.

```python
a = [1, 2, 3, 4, 5]
b = [2, 4, 6, 8]
# expected: {2: 4, 4: 16}
```

---

### 3.

Flatten a matrix into a single set (no duplicates).

```python
matrix = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
# expected: {1, 2, 3, 4, 5}
```

---

### 4.

From a list of sentences, build a set of all unique words across all sentences. Lowercase everything.

```python
sentences = ["Hello World", "world is great", "Hello Python"]
# expected: {'hello', 'world', 'is', 'great', 'python'}
```

---

### 5.

Invert a dict but skip entries where the value is `None`.

```python
d = {"a": 1, "b": None, "c": 3, "d": None}
# expected: {1: "a", 3: "c"}
```

---

### 6.

From a list of numbers, build a dict of `number → "even"` or `number → "odd"`.

```python
nums = [1, 2, 3, 4, 5]
# expected: {1: 'odd', 2: 'even', 3: 'odd', 4: 'even', 5: 'odd'}
```

---

### 7.

Given a string, build a dict of `character → count` but only for letters (no spaces, no punctuation).

```python
text = "hello world!"
# expected: {'h': 1, 'e': 1, 'l': 3, 'o': 2, 'w': 1, 'r': 1, 'd': 1}
```

---

### 8.

From a nested list, get all numbers greater than 5 as a flat set.

```python
data = [[1, 6, 3], [8, 2, 7], [4, 9, 5]]
# expected: {6, 7, 8, 9}
```

---

### 9.

Build a multiplication table as a dict of `(i, j) → i*j` for i and j from 1 to 4.

```python
# expected: {(1,1):1, (1,2):2, ..., (4,4):16}
```

---

### 10.

From a list of dicts, build a new dict of `name → score` but only where score >= 50.

```python
students = [
    {"name": "Alice", "score": 82},
    {"name": "Bob", "score": 45},
    {"name": "Charlie", "score": 91},
    {"name": "Dave", "score": 38},
]
# expected: {'Alice': 82, 'Charlie': 91}
```

---

### 11.

Find all pairs `(a, b)` from the same list where `a < b` and `a + b` is even. Return as a set.

```python
nums = [1, 2, 3, 4, 5, 6]
# expected: {(1,3), (1,5), (2,4), (2,6), (3,5), (4,6)}
```

---

### 12.

From a dict of `country → population`, build a new dict with only countries over 100 million, and round the population to the nearest million.

```python
data = {
    "Germany": 83_200_000,
    "USA": 331_000_000,
    "Brazil": 214_300_000,
    "Iceland": 370_000,
}
# expected: {'USA': 331000000, 'Brazil': 214300000}
```

---

### 13.

Transpose a matrix using a nested comprehension (no `zip`).

```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# expected: [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
```

---

### 14.

From a list of strings, build a dict of `word → reversed word` but only for words that are NOT palindromes.

```python
words = ["level", "hello", "racecar", "world", "madam", "python"]
# expected: {'hello': 'olleh', 'world': 'dlrow', 'python': 'nohtyp'}
```

---

### 15.

Given two dicts, build a new dict that contains only the keys that exist in BOTH, with the value being the sum of both values.

```python
a = {"x": 10, "y": 20, "z": 30}
b = {"y": 5, "z": 15, "w": 25}
# expected: {'y': 25, 'z': 45}
```
