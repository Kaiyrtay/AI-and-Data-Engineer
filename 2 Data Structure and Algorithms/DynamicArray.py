from typing import List, Any

DEFAULT_CAPACITY_STRATEGY = 2


class DynamicArray:

    # ─────────────────────────────────────────────
    #  Initialization
    # ─────────────────────────────────────────────

    def __init__(self):
        self._size = 0
        self._capacity = 1
        self._data = [None] * self._capacity

    # ─────────────────────────────────────────────
    #  Properties
    # ─────────────────────────────────────────────

    @property
    def size(self) -> int:
        return self._size

    @property
    def capacity(self) -> int:
        return self._capacity

    # ─────────────────────────────────────────────
    #  Magic Methods
    # ─────────────────────────────────────────────

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, index) -> Any:
        self._validate_index(index)
        return self._data[index]

    def __setitem__(self, index, value) -> None:
        self._validate_index(index)
        self._data[index] = value

    def __iter__(self) -> Any:
        for i in range(self.size):
            yield self._data[i]

    def __contains__(self, value) -> bool:
        return self.find(value) != -1

    def __repr__(self) -> str:
        return f"DynamicArray(size={self.size}, capacity={self.capacity})"

    def __str__(self) -> str:
        return f"Dynamic Array (size: {self.size}, capacity: {self.capacity}): {self.to_list()} "

    # ─────────────────────────────────────────────
    #  Dynamic Array Methods
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

    def _size_balance(self) -> None:
        if self.is_full():
            self._capacity *= DEFAULT_CAPACITY_STRATEGY
            self._data = self._resize(self.capacity)
        elif self.size <= self.capacity // (DEFAULT_CAPACITY_STRATEGY * 2) and self.capacity > 1:
            self._capacity //= DEFAULT_CAPACITY_STRATEGY
            self._data = self._resize(self.capacity)

    def _resize(self, new_capacity) -> List[Any]:
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        return new_data

    def _left_shift(self, index) -> None:
        self._validate_index(index)
        for i in range(index, self.size - 1):
            self._data[i] = self._data[i+1]
        self._data[self.size - 1] = None
        self._size -= 1
        self._size_balance()

    def _right_shift(self, index) -> None:
        self._validate_index(index, allow_end=True)
        for i in range(self.size, index, -1):
            self._data[i] = self._data[i - 1]
        self._size += 1

    def append(self, value) -> None:
        self._size_balance()
        self._data[self.size] = value
        self._size += 1

    def insert(self, index, value) -> None:
        self._size_balance()
        self._validate_index(index, allow_end=True)
        self._right_shift(index)
        self._data[index] = value

    def remove(self, value) -> int:
        index = self.index(value)
        self._left_shift(index)
        return index

    def clear(self) -> None:
        self._size = 0
        self._capacity = 1
        self._data = [None] * self._capacity

    def pop(self, index=-1) -> Any:
        if index < 0:
            index += self.size
        self._validate_index(index)
        value = self._data[index]
        self._left_shift(index)
        return value

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
        return [self._data[i] for i in range(self.size)]


# Create a new dynamic array
arr = DynamicArray()
print(arr)  # Dynamic Array (size: 0, capacity: 1): []

# Append elements
arr.append(10)
arr.append(20)
arr.append(30)
print(arr)  # Dynamic Array (size: 3, capacity: 4): [10, 20, 30]

# Access elements
print(arr[0])  # 10
print(arr[2])  # 30

# Insert an element at a specific index
arr.insert(1, 15)
print(arr)  # Dynamic Array (size: 4, capacity: 4): [10, 15, 20, 30]

# Remove an element by value
arr.remove(20)
print(arr)  # Dynamic Array (size: 3, capacity: 4): [10, 15, 30]

# Pop the last element
last = arr.pop()
print(last)  # 30
print(arr)   # Dynamic Array (size: 2, capacity: 4): [10, 15]

# Check if a value is in the array
print(15 in arr)  # True
print(50 in arr)  # False

# Get index of a value
print(arr.index(15))  # 1

# Convert to a standard Python list
lst = arr.to_list()
print(lst)  # [10, 15]

# Clear the array
arr.clear()
print(arr)  # Dynamic Array (size: 0, capacity: 1): []
