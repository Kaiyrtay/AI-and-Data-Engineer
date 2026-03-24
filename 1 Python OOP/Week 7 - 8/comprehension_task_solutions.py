# ─────────────────────────────────────────────
#   Covers: dict, set, nested, conditional comprehensions.
# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
#  Task 1: From a list of words, build a dict of word → length. Skip words shorter than 4 letters.
#   words = ["cat", "elephant", "dog", "rhinoceros", "ox", "tiger"]
#   expected: {'elephant': 8, 'rhinoceros': 10, 'tiger': 5}
# ─────────────────────────────────────────────

words = ["cat", "elephant", "dog", "rhinoceros", "ox", "tiger"]
task_1 = {word: len(word) for word in words if len(word) >= 4}
print("Task 1: From a list of words, build a dict of word → length. Skip words shorter than 4 letters: ", task_1)

# ─────────────────────────────────────────────
#  Task 2: From two lists, build a dict of number → square but only for numbers that appear in both lists.
#   a = [1, 2, 3, 4, 5]
#   b = [2, 4, 6, 8]
#   expected: {2: 4, 4: 16}
# ─────────────────────────────────────────────

a = [1, 2, 3, 4, 5]
b = [2, 4, 6, 8]

is_a_shorten = len(a) < len(b)
if is_a_shorten:
    task_2 = {num: num ** 2 for num in a if num in b}
else:
    task_2 = {num: num ** 2 for num in b if num in a}
print("Task 2: From two lists, build a dict of number → square but only for numbers that appear in both lists:", task_2)

# ─────────────────────────────────────────────
#  Task 3: Flatten a matrix into a single set (no duplicates).
#   matrix = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
#   expected: {1, 2, 3, 4, 5}
# ─────────────────────────────────────────────

matrix = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
task_3 = {item for row in matrix for item in row}
print("Task 3: Flatten a matrix into a single set (no duplicates): ", task_3)

# ─────────────────────────────────────────────
#  Task 4: From a list of sentences, build a set of all unique words across all sentences. Lowercase everything.
#   sentences = ["Hello World", "world is great", "Hello Python"]
#   expected: {'hello', 'world', 'is', 'great', 'python'}
# ─────────────────────────────────────────────

sentences = ["Hello WorLd", "world is great", "Hello Python"]
task_4 = {word.lower() for sentence in sentences for word in sentence.split()}
print("Task 4: From a list of sentences, build a set of all unique words across all sentences. Lowercase everything: ", task_4)

# ─────────────────────────────────────────────
#  Task 5: Invert a dict but skip entries where the value is None.
#   d = {"a": 1, "b": None, "c": 3, "d": None}
#   expected: {1: "a", 3: "c"}
# ─────────────────────────────────────────────

d = {"a": 1, "b": None, "c": 3, "d": None}
task_5 = {v: k for k, v in d.items() if v is not None}
print("Task 5: Invert a dict but skip entries where the value is None:", task_5)

# ─────────────────────────────────────────────
#  Task 6: From a list of numbers, build a dict of number → "even" or number → "odd".
#   nums = [1, 2, 3, 4, 5]
#   expected: {1: 'odd', 2: 'even', 3: 'odd', 4: 'even', 5: 'odd'}
# ─────────────────────────────────────────────

nums = [1, 2, 3, 4, 5]
task_6 = {num: "odd" if num % 2 != 0 else "even" for num in nums}
print('Task 6: From a list of numbers, build a dict of number → "even" or number → "odd": ', task_6)

# ─────────────────────────────────────────────
#  Task 7: Given a string, build a dict of character → count but only for letters (no spaces, no punctuation).
#   text = "hello world!"
#   expected: {'h': 1, 'e': 1, 'l': 3, 'o': 2, 'w': 1, 'r': 1, 'd': 1}
# ─────────────────────────────────────────────

text = "hello world!"
task_7 = {ch: text.count(ch) for ch in text if ord(
    ch) in range(65, 90 + 1) or ord(ch) in range(97, 122 + 1)}
print('Given a string, build a dict of character → count but only for letters(no spaces, no punctuation): ', task_7)

# ─────────────────────────────────────────────
#  Task 8: From a nested list, get all numbers greater than 5 as a flat set.
#   data = [[1, 6, 3], [8, 2, 7], [4, 9, 5]]
#   expected: {6, 7, 8, 9}
# ─────────────────────────────────────────────

data = [[1, 6, 3], [8, 2, 7], [4, 9, 5]]
task_8 = {num for outer in data for num in outer if num > 5}
print("Task 8: From a nested list, get all numbers greater than 5 as a flat set: ", task_8)

# ─────────────────────────────────────────────
#  Task 9: Build a multiplication table as a dict of (i, j) → i*j for i and j from 1 to 4.
#   expected: {(1,1):1, (1,2):2, ..., (4,4):16}
# ─────────────────────────────────────────────
task_9 = {(i, j): i*j for i in range(1, 4 + 1) for j in range(1, 4+1)}
print("Task 9: Build a multiplication table as a dict of (i, j) → i*j for i and j from 1 to 4: ", task_9)

# ─────────────────────────────────────────────
#  Task 10: From a list of dicts, build a new dict of name → score but only where score >= 50.
#   students = [
#   {"name": "Alice", "score": 82},
#   {"name": "Bob", "score": 45},
#   {"name": "Charlie", "score": 91},
#   {"name": "Dave", "score": 38},
#   ]
#   expected: {'Alice': 82, 'Charlie': 91}
# ─────────────────────────────────────────────

students = [
    {"name": "Alice", "score": 82},
    {"name": "Bob", "score": 45},
    {"name": "Charlie", "score": 91},
    {"name": "Dave", "score": 38},
]
task_10 = {student["name"]: student["score"]
           for student in students if student["score"] >= 50}
print("Task 10: From a list of dicts, build a new dict of name → score but only where score >= 50: ", task_10)

# ─────────────────────────────────────────────
#  Task 11: Find all pairs (a, b) from the same list where a < b and a + b is even. Return as a set.
#   nums = [1, 2, 3, 4, 5, 6]
#   expected: {(1,3), (1,5), (2,4), (2,6), (3,5), (4,6)}
# ─────────────────────────────────────────────

nums = [1, 2, 3, 4, 5, 6]
task_11 = {(a, b) for a in nums for b in nums if a < b and (a+b) % 2 == 0}
print("Task 11: Find all pairs (a, b) from the same list where a < b and a + b is even. Return as a set: ", task_11)

# ─────────────────────────────────────────────
#  Task 12: From a dict of country → population, build a new dict with only countries over 100 million, and round the population to the nearest million.
#   data = {
#    "Germany": 83_200_000,
#    "USA": 331_000_000,
#    "Brazil": 214_300_000,
#    "Iceland": 370_000,
#   }
#  expected: {'USA': 331000000, 'Brazil': 214300000}
# ─────────────────────────────────────────────

data = {
    "Germany": 83_200_000,
    "USA": 331_000_000,
    "Brazil": 214_300_000,
    "Iceland": 370_000,
}

task_12 = {key: round(value, -6)
           for key, value in data.items() if value > 100_000_000}
print("Task 12: From a dict of country → population, build a new dict with only countries over 100 million, and round the population to the nearest million: ", task_12)

# ─────────────────────────────────────────────
#  Task 13: Transpose a matrix using a nested comprehension (no zip).
#   matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
#   expected: [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
# ─────────────────────────────────────────────

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
task_13 = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
print("Task 13: Transpose a matrix using a nested comprehension (no zip): ", task_13)

# ─────────────────────────────────────────────
#  Task 14: From a list of strings, build a dict of word → reversed word but only for words that are NOT palindromes.
#   words = ["level", "hello", "racecar", "world", "madam", "python"]
#   expected: {'hello': 'olleh', 'world': 'dlrow', 'python': 'nohtyp'}
# ─────────────────────────────────────────────

words = ["level", "hello", "racecar", "world", "madam", "python"]
task_14 = {word: word[::-1] for word in words if word != word[::-1]}
print("Task 14: From a list of strings, build a dict of word → reversed word but only for words that are NOT palindromes: ", task_14)

# ─────────────────────────────────────────────
#  Task 15: Given two dicts, build a new dict that contains only the keys that exist in BOTH, with the value being the sum of both values.
#   a = {"x": 10, "y": 20, "z": 30}
#   b = {"y": 5, "z": 15, "w": 25}
#   expected: {'y': 25, 'z': 45}
# ─────────────────────────────────────────────

a = {"x": 10, "y": 20, "z": 30}
b = {"y": 5, "z": 15, "w": 25}
is_a_shorten = len(a) < len(b)
if is_a_shorten:
    task_15 = {key: value + b[key] for key, value in a.items() if b.get(key)}
else:
    task_15 = {key: value + a[key] for key, value in b.items() if a.get(key)}
print("Task 15: Given two dicts, build a new dict that contains only the keys that exist in BOTH, with the value being the sum of both values: ", task_15)
