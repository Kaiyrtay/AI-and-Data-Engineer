from functools import reduce

# ─────────────────────────────────────────────
#   Rules: use ONLY `lambda`, `map`, `filter`, `reduce`. No loops. No list comprehensions.
# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
#  Task 1: Given a nested list, flatten it, keep only odd numbers, return their squares.
#   nested = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
#   expected: [1, 9, 25, 49, 81]
# ─────────────────────────────────────────────

nested = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
task_1 = list(map(lambda x: x**2, filter(lambda x: x %
                                         2 != 0, reduce(lambda a, b: a + b, nested))))
print("Task 1: Given a nested list, flatten it, keep only odd numbers, return their squares: ", task_1)


# ─────────────────────────────────────────────
#  Task 2: Count how many times each word appears. Return a dict.
#   words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
#   expected: {'apple': 3, 'banana': 2, 'cherry': 1}
# ─────────────────────────────────────────────

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
task_2 = reduce(lambda acc, w: {**acc, w: acc.get(w, 0)+1}, words, {})
print("Task 2: Count how many times each word appears. Return a dict: ", task_2)

# ─────────────────────────────────────────────
#  Task 3: Apply a list of functions one after another to a starting value.
#   fns = [lambda x: x * 2, lambda x: x + 10, lambda x: x ** 2]
#   start = 3
#   expected: 256
# ─────────────────────────────────────────────
fns = [lambda x: x * 2, lambda x: x + 10, lambda x: x ** 2]
start = 3
task_3 = reduce(lambda v, f: f(v), fns, start)
print("Task 3: Apply a list of functions one after another to a starting value: ", task_3)

# ─────────────────────────────────────────────
#  Task 4: Group numbers by their remainder when divided by 3. Return a dict.
#   nums = list(range(1, 16))
#   expected: {1: [1,4,7,10,13], 2: [2,5,8,11,14], 0: [3,6,9,12,15]}
# ─────────────────────────────────────────────
nums = list(range(1, 16))
task_4 = reduce(lambda acc, x: {**acc, x %
                3: acc.get(x % 3, []) + [x]}, nums, {})
print("Task 4: Group numbers by their remainder when divided by 3. Return a dict: ", task_4)

# ─────────────────────────────────────────────
#  Task 5: Transpose a matrix (flip rows and columns).
#   matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
#   expected: [[1,4,7], [2,5,8], [3,6,9]]
# ─────────────────────────────────────────────
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
task_5 = list(map(lambda col: list(col), zip(*matrix)))
print("Task 5: Transpose a matrix (flip rows and columns): ", task_5)

# ─────────────────────────────────────────────
#  Task 6: Keep only valid emails. Valid = has `@` and a `.` after the `@`.
#   emails = ["user@mail.com", "bademail", "a@b.c", "noatsign.com", "x@y"]
#   expected: ['user@mail.com', 'a@b.c']
# ─────────────────────────────────────────────
emails = ["user@mail.com", "bademail", "a@b.c", "noatsign.com", "x@y", "x@y."]
task_6 = list(filter(lambda x: "@" in x and "." in x.split("@")
              [-1] and not x.endswith("."), emails))
print("Task 6: Keep only valid emails. Valid = has `@` and a `.` after the `@`: ", task_6)

# ─────────────────────────────────────────────
#  Task 7: Return a running cumulative sum list.
#   nums = [1, 2, 3, 4, 5]
#   expected: [1, 3, 6, 10, 15]
# ─────────────────────────────────────────────
nums = [1, 2, 3, 4, 5]
task_7 = reduce(lambda acc, x: acc + [x if not acc else acc[-1] + x], nums, [])
print("Task 7: Return a running cumulative sum list: ", task_7)

# ─────────────────────────────────────────────
#  Task 8: Flatten a list no matter how deeply nested it is.
#   deep = [1, [2, [3, [4, [5]]]]]
#   expected: [1, 2, 3, 4, 5]
# ─────────────────────────────────────────────
deep = [1, [2, [3, [4, [5]]]]]


def flatten(lst): return reduce(lambda acc, x: acc +
                                (flatten(x) if isinstance(x, list) else [x]), lst, [])


task_8 = flatten(deep)
print("Task 8: Flatten a list no matter how deeply nested it is: ", task_8)

# ─────────────────────────────────────────────
#  Task 9: Shift every letter in a string by 3 positions forward. Leave spaces as - is (ONLY LOWER CASE LETTERS, similar to Caesar Cipher)
#   text = "hello world"
#   expected: 'khoor zruog'
# ─────────────────────────────────────────────
text = "hello world"
task_9 = "".join(map(lambda ch: chr((ord(ch)+3 - 97) %
                                    26 + 97) if ch.islower() else ch, text))
print("Task 9: Shift every letter in a string by 3 positions forward. Leave spaces as - is (ONLY LOWER CASE LETTERS, similar to Caesar Cipher): ", task_9)

# ─────────────────────────────────────────────
#  Task 10: From two lists, get all pairs where the product > 10 and both numbers are odd.
#   a = [1, 3, 5, 7]
#   b = [2, 3, 4, 5]
#   expected: [(3,5), (5,3), (5,5), (7,3), (7,5)]
# ─────────────────────────────────────────────
a = [1, 3, 5, 7]
b = [2, 3, 4, 5]
task_10 = list(filter(lambda l: l[0]*l[1] >
               10 and l[0] % 2 != 0 and l[1] % 2 != 0,
               [(x, y) for x in a for y in b]))
print("Task 10: From two lists, get all pairs where the product > 10 and both numbers are odd: ", task_10)

# ─────────────────────────────────────────────
#  Task 11: Swap all keys and values in a dict.
#   d = {"a": 1, "b": 2, "c": 3}
#   expected: {1: 'a', 2: 'b', 3: 'c'}
# ─────────────────────────────────────────────

d = {"a": 1, "b": 2, "c": 3}
task_11 = reduce(lambda acc, k: {**acc, d[k]: k}, d, {})
print("Task 11: Swap all keys and values in a dict: ", task_11)

# ─────────────────────────────────────────────
#  Task 12: Zip two lists into a dict without using `dict()`.
#   keys = ["x", "y", "z"]
#   vals = [10, 20, 30]
#   expected: {'x': 10, 'y': 20, 'z': 30}
# ─────────────────────────────────────────────
keys = ["x", "y", "z"]
vals = [10, 20, 30]
task_12 = reduce(lambda acc, index: {
                 **acc, keys[index]: vals[index]}, range(len(keys)), {})
print("Task 12: Zip two lists into a dict without using `dict()`:", task_12)

# ─────────────────────────────────────────────
#  Task 13: Find all numbers that appear more than once.
#   nums = [1, 2, 3, 2, 4, 3, 5]
#   expected: [2, 3]
# ─────────────────────────────────────────────
nums = [1, 2, 3, 2, 4, 3, 5]
task_13 = reduce(
    lambda acc, x: acc + [x] if (nums.count(x) > 1 and x not in acc) else acc,
    nums,
    []
)
print("Task 13: Find all numbers that appear more than once: ", task_13)
