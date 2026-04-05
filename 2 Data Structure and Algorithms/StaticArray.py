from typing import List, Any


class StaticArray:

    # ─────────────────────────────────────────────
    #  Initialization
    # ─────────────────────────────────────────────

    def __init__(self, capacity):
        self._data = [None] * capacity
        self._size = 0

    # ─────────────────────────────────────────────
    #  Properties
    # ─────────────────────────────────────────────

    @property
    def capacity(self):
        return len(self._data)

    @property
    def size(self) -> int:
        return self._size

    # ─────────────────────────────────────────────
    #  Magic Methods
    # ─────────────────────────────────────────────

    # len(array) will return the number of elements currently in the array, not the capacity
    def __len__(self) -> int:
        return self.size

    # array[index] will return the element at the specified index
    def __getitem__(self, index) -> Any:
        self._validate_index(index)
        return self._data[index]

    # array[index] = value will set the element at the specified index to the given value.
    def __setitem__(self, index, value) -> None:
        self._validate_index(index)
        self._data[index] = value

    # iter(array) will allow iteration over the elements in the array using a for loop or any other iterator context.
    def __iter__(self) -> Any:
        for i in range(self.size):
            yield self._data[i]

    # value in array will return True if the value is present in the array, and False otherwise.
    def __contains__(self, value) -> bool:
        return self.find(value) != -1

    # repr(array) will return a string representation of the array, showing its capacity and current size.
    def __repr__(self) -> str:
        return f"StaticArray(capacity={len(self._data)}, size={self.size})"

    # str(array) will return a more detailed string representation of the array, including its contents.
    def __str__(self) -> str:
        return f"Static Array (size: {self.size}, capacity: {self.capacity}): {self.to_list()} "

    # ─────────────────────────────────────────────
    #  Static Array Methods
    # ─────────────────────────────────────────────

    def _validate_index(self, index, allow_end=False) -> None:
        if self.is_empty():
            if allow_end:
                if index != 0:
                    raise IndexError(
                        "Array is empty, only index 0 is valid for insertion")
            else:
                raise IndexError("Array is empty, no valid indexes for access")
            return

        if allow_end:
            if index < 0 or index > self.size:
                raise IndexError("Index out of bounds")
        else:
            if index < 0 or index >= self.size:
                raise IndexError("Index out of bounds")

    def _ensure_not_full(self) -> None:
        if self.is_full():
            raise OverflowError("Array is full")

    def _left_shift(self, index) -> None:
        self._validate_index(index)
        for i in range(index, self.size - 1):
            self._data[i] = self._data[i + 1]
        self._data[self.size - 1] = None
        self._size -= 1

    def _right_shift(self, index) -> None:
        self._ensure_not_full()
        self._validate_index(index, allow_end=True)
        for i in range(self.size, index, -1):
            self._data[i] = self._data[i - 1]
        self._size += 1

    def append(self, value) -> None:
        self._ensure_not_full()
        self._data[self.size] = value
        self._size += 1

    def insert(self, index, value) -> None:
        self._validate_index(index, allow_end=True)
        self._ensure_not_full()
        self._right_shift(index)
        self._data[index] = value

    def pop(self, index=-1) -> Any:
        if index < 0:
            index += self.size
        self._validate_index(index)
        value = self._data[index]
        self._left_shift(index)
        return value

    def remove(self, value) -> int:
        index = self.index(value)
        self._left_shift(index)
        return index

    def clear(self) -> None:
        for i in range(self.size):
            self._data[i] = None
        self._size = 0

    def index(self, value: Any) -> int:
        index = self.find(value)
        if index == -1:
            raise ValueError(f"{value} not found in array")
        return index

    def find(self, value: Any) -> int:
        if self.is_empty():
            return -1
        for index in range(self.size):
            if self._data[index] == value:
                return index
        return -1

    def is_full(self) -> bool:
        return self.size == self.capacity

    def is_empty(self) -> bool:
        return self.size == 0

    def to_list(self) -> List[Any]:
        return self._data[:self.size]


# Simple StaticArray testing
arr = StaticArray(5)

# Append
arr.append(10)
arr.append(20)
print("After append:", arr.to_list())  # [10, 20]

# Insert
arr.insert(1, 15)
print("After insert:", arr.to_list())  # [10, 15, 20]

# Get/Set
print("Item at 1:", arr[1])  # 15
arr[1] = 50
print("After set:", arr.to_list())  # [10, 50, 20]

# Pop
popped = arr.pop()
print("Popped:", popped)  # 20
print("After pop:", arr.to_list())  # [10, 50]

# Remove
arr.remove(50)
print("After remove 50:", arr.to_list())  # [10]

# Find/Index
arr.append(30)
print("Find 30:", arr.find(30))  # 1
print("Index 10:", arr.index(10))  # 0

# Clear
arr.clear()
print("After clear:", arr.to_list())  # []

# Iteration
arr.append(1)
arr.append(2)
for v in arr:
    print("Iterate:", v)  # 1, 2
