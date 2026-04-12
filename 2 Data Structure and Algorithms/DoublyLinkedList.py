from typing import Optional, Any


class EmptyListError(Exception):
    pass


class Node:

    def __init__(self, value: Any) -> None:
        self.value: Optional[Any] = value
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"Node({self.value})"


class DoublyLinkedList:

    def __init__(self) -> None:
        self.head = None
        self.tail = None
        self._size = 0

    # ─────────────────────────────────────────────
    # Properties
    # ─────────────────────────────────────────────

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("Size must be an integer")
        if value < 0:
            raise ValueError("Size cannot be negative")
        self._size = value

    # ─────────────────────────────────────────────
    # Magic Methods
    # ─────────────────────────────────────────────

    def __len__(self) -> int:
        return self._size

    def __getitem__(self, index: int) -> Optional[Any]:
        if self.is_empty():
            raise EmptyListError("Cannot index empty list")
        index = self._boundary_check(index)
        return self.get(index).value

    def __setitem__(self, index: int, value: Any) -> None:
        if isinstance(value, Node):
            raise TypeError("Value cannot be instance of Node")
        if self.is_empty():
            raise EmptyListError("Cannot index empty list")
        index = self._boundary_check(index)
        node = self.get(index)
        node.value = value

    def __iter__(self) -> Any:
        if self.is_empty():
            return iter([])
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __contains__(self, value: Any) -> bool:
        return self.search(value) is not None

    def __eq__(self, other: 'DoublyLinkedList') -> bool:
        if not isinstance(other, DoublyLinkedList):
            return False
        if self.size != other.size:
            return False
        current1 = self.head
        current2 = other.head
        while current1 and current2:
            if current1.value != current2.value:
                return False
            current1 = current1.next
            current2 = current2.next
        return True

    def __str__(self) -> str:
        if self.is_empty():
            return f"[]"
        result = "["
        current = self.head
        while current:
            result += str(current.value)
            if current.next:
                result += ", "
            current = current.next
        result += "]"
        return result

    def __repr__(self) -> str:
        if self.is_empty():
            return f"DoublyLinkedList()"
        result = "DoublyLinkedList("
        current = self.head
        while current:
            result += str(current.value)
            if current.next:
                result += ", "
            current = current.next
        result += ")"
        return result

    # ─────────────────────────────────────────────
    # Insert Operations
    # ─────────────────────────────────────────────

    def prepend(self, value: Any) -> None:
        new_node = self._convert_to_node(value)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1

    def append(self, value: Any) -> None:
        new_node = self._convert_to_node(value)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def insert(self, index: int, value: Any) -> bool:
        index = self._boundary_check(index, allow_end=True)
        if index == 0:
            self.prepend(value)
            return True
        if index == self.size:
            self.append(value)
            return True
        node = self.get(index)
        if node is None:
            return False
        new_node = self._convert_to_node(value)
        prev_node = node.prev
        new_node.next = node
        new_node.prev = prev_node
        node.prev = new_node
        if prev_node:
            prev_node.next = new_node
        else:
            self.head = new_node
        self.size += 1
        return True

    def insert_after(self, target_value: Any, value: Any) -> bool:
        if self.is_empty():
            return False
        current = self.head
        while current:
            if current.value == target_value:
                new_node = self._convert_to_node(value)
                next_node = current.next
                current.next = new_node
                new_node.prev = current
                new_node.next = next_node
                if next_node:
                    next_node.prev = new_node
                else:
                    self.tail = new_node

                self.size += 1
                return True
            current = current.next
        return False

    def insert_before(self, target_value: Any, value: Any) -> bool:
        if self.is_empty():
            return False
        current = self.head
        while current:
            if current.value == target_value:
                new_node = self._convert_to_node(value)
                prev_node = current.prev
                new_node.next = current
                current.prev = new_node
                if prev_node:
                    prev_node.next = new_node
                    new_node.prev = prev_node
                else:
                    self.head = new_node
                self.size += 1
                return True
            current = current.next
        return False

    # ─────────────────────────────────────────────
    # Delete Operations
    # ─────────────────────────────────────────────

    def del_head(self) -> None:
        if self.is_empty():
            raise EmptyListError("Cannot delete from empty list")
        if self.size == 1:
            self.clear()
        else:
            next_node = self.head.next
            next_node.prev = None
            self.head = next_node
            self.size -= 1

    def del_tail(self) -> None:
        if self.is_empty():
            raise EmptyListError("Cannot delete from empty list")
        if self.size == 1:
            self.clear()
        else:
            prev_node = self.tail.prev
            prev_node.next = None
            self.tail = prev_node
            self.size -= 1

    def del_at(self, index: int) -> bool:
        index = self._boundary_check(index)
        if index == 0:
            self.del_head()
            return True
        if index == self.size - 1:
            self.del_tail()
            return True
        node = self.get(index)
        if not node:
            return False
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
        self.size -= 1
        return True

    def remove(self, value: Any) -> bool:
        if isinstance(value, Node):
            raise TypeError("Value cannot be instance of Node")
        if self.is_empty():
            return False
        if self.head.value == value:
            self.del_head()
            return True
        if self.tail.value == value:
            self.del_tail()
            return True
        current = self.head
        while current:
            if current.value == value:
                next_node = current.next
                prev_node = current.prev
                if next_node:
                    next_node.prev = prev_node
                if prev_node:
                    prev_node.next = next_node
                self.size -= 1
                return True
            current = current.next
        return False

    def remove_all(self, value: Any) -> int:
        counter = 0
        if self.is_empty():
            return 0
        while self.remove(value):
            counter += 1
        return counter

    # ─────────────────────────────────────────────
    # Search & Query Operations
    # ─────────────────────────────────────────────

    def count(self, value: Any) -> int:
        if isinstance(value, Node):
            raise TypeError("Value cannot be instance of Node")
        if self.is_empty():
            return 0
        counter = 0
        current = self.head
        while current:
            if current.value == value:
                counter += 1
            current = current.next
        return counter

    def find_index(self, value: Any) -> int:
        if isinstance(value, Node):
            raise TypeError("Value cannot be instance of Node")
        if self.is_empty():
            return -1
        index = 0
        current = self.head
        while current:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return -1

    def search(self, value: Any) -> Optional[Node]:
        if isinstance(value, Node):
            raise TypeError("Value cannot be instance of Node")
        if self.is_empty():
            return None
        current = self.head
        while current:
            if current.value == value:
                return current
            current = current.next
        return None

    def get(self, index: int) -> Optional[Any]:
        index = self._boundary_check(index)
        if index < self.size // 2:
            return self._from_head(index)
        else:
            return self._from_tail(index)

    # ─────────────────────────────────────────────
    # Traversal Operations
    # ─────────────────────────────────────────────

    def traverse(self) -> str:
        return str(self)

    def reverse_traverse(self) -> str:
        if self.is_empty():
            return f"[]"
        result = "["
        current = self.tail
        while current:
            result += str(current.value)
            if current.prev:
                result += ", "
            current = current.prev
        result += "]"
        return result

    # ─────────────────────────────────────────────
    # Conversion Operations
    # ─────────────────────────────────────────────

    def to_list(self) -> Optional[list]:
        if self.is_empty():
            return []
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result

    def from_list(self, lst: list) -> bool:
        if not isinstance(lst, list):
            raise TypeError("Provided value needs to be list")
        if not self.is_empty():
            raise ValueError("To create the list, needs to be empty")
        for i in lst:
            self.append(i)
        return True

    # ─────────────────────────────────────────────
    # State & Check Operations
    # ─────────────────────────────────────────────

    def is_empty(self) -> bool:
        return self.size == 0

    def is_circular(self) -> bool:
        if self.is_empty():
            return False
        return self.head.prev == self.tail and self.tail.next == self.head

    def has_duplicate(self) -> bool:
        if self.size <= 1:
            return False
        unique = set()
        current = self.head
        while current:
            if current.value in unique:
                return True
            unique.add(current.value)
            current = current.next
        return False

    # ─────────────────────────────────────────────
    # Utility Operations
    # ─────────────────────────────────────────────

    def clear(self) -> None:
        self.head = None
        self.tail = None
        self.size = 0

    def reverse(self) -> None:
        current = self.head
        self.head, self.tail = self.tail, self.head

        while current:
            current.next, current.prev = current.prev, current.next
            current = current.prev

    def first(self) -> Optional['Node']:
        return self.head

    def last(self) -> Optional['Node']:
        return self.tail

    def merge(self, other: 'DoublyLinkedList') -> 'DoublyLinkedList':
        if not isinstance(other, DoublyLinkedList):
            raise TypeError("Must be DoublyLinkedList")
        if other.is_empty():
            return self
        if self.is_empty():
            self.head = other.head
            self.tail = other.tail
            self.size = other.size
            return self
        self.tail.next = other.head
        other.head.prev = self.tail
        self.tail = other.tail
        self.size += other.size
        return self

    # ─────────────────────────────────────────────
    # Private Helpers
    # ─────────────────────────────────────────────

    def _convert_to_node(self, value: Any) -> Node:
        if isinstance(value, Node):
            raise TypeError("Value cannot be instance of Node")
        return Node(value)

    def _boundary_check(self, index: int, allow_end: bool = False) -> int:
        if not isinstance(index, int):
            raise TypeError("Index must be an integer")
        if index < 0:
            index += self.size
        max_index = self.size if allow_end else self.size - 1
        if index < 0 or index > max_index:
            raise IndexError(
                f"Index {index} out of bounds for list of size {self.size}")
        return index

    def _from_head(self, index: int = 0) -> Node:
        index = self._boundary_check(index)
        current = self.head
        for _ in range(index):
            current = current.next
        return current

    def _from_tail(self, index: int) -> Node:
        index = self._boundary_check(index)
        current = self.tail
        for _ in range(self.size - index - 1):
            current = current.prev
        return current


if __name__ == "__main__":
    lst = DoublyLinkedList()
    lst.append(1)
    lst.append(2)
    lst.append(3)
    print("After append(1,2,3):", lst)

    lst.prepend(0)
    print("After prepend(0):", lst)

    lst.insert(2, 1.5)
    print("After insert(2, 1.5):", lst)

    print("lst[2]:", lst[2])
    print("lst[-1]:", lst[-1])

    lst[2] = 99
    print("After lst[2] = 99:", lst)

    print("1.5 in lst:", 1.5 in lst)
    print("999 in lst:", 999 in lst)

    print("first():", lst.first())
    print("last():", lst.last())
    print("len(lst):", len(lst))

    lst.del_head()
    print("After del_head():", lst)

    lst.del_tail()
    print("After del_tail():", lst)

    lst.del_at(1)
    print("After del_at(1):", lst)

    lst2 = DoublyLinkedList()
    lst2.append(99)
    lst2.append(2)
    print("lst == lst2:", lst == lst2)

    lst3 = DoublyLinkedList()
    lst3.append(2)
    lst3.append(99)
    print("lst == lst3:", lst == lst3)

    lst4 = DoublyLinkedList()
    lst4.append(2)
    lst4.append(99)
    lst4.reverse()
    print("After reverse():", lst4)

    print("to_list():", lst4.to_list())

    lst4.clear()
    print("After clear():", lst4)

    try:
        lst4.first()
    except EmptyListError as e:
        print(f"Exception caught: {e}")

    try:
        lst4[0]
    except EmptyListError as e:
        print(f"Exception caught: {e}")

    try:
        lst4.del_head()
    except EmptyListError as e:
        print(f"Exception caught: {e}")

    print("\n--- EDGE CASE TESTS ---")

    lst5 = DoublyLinkedList()
    lst5.append(5)
    lst5.append(10)
    lst5.append(5)
    lst5.append(15)
    lst5.append(5)
    print("List:", lst5)

    print("remove(5):", lst5.remove(5))
    print("After remove(5):", lst5)

    lst6 = DoublyLinkedList()
    lst6.append(7)
    lst6.append(7)
    lst6.append(7)
    print("List with duplicates:", lst6)
    print("remove_all(7):", lst6.remove_all(7))
    print("After remove_all(7):", lst6)

    lst7 = DoublyLinkedList()
    lst7.append(1)
    lst7.append(2)
    lst7.append(3)
    print("List:", lst7)
    print("insert_before(2, 99):", lst7.insert_before(2, 99))
    print("After insert_before(2, 99):", lst7)

    lst8 = DoublyLinkedList()
    lst8.append(1)
    lst8.append(2)
    lst8.append(3)
    print("List:", lst8)
    print("insert_after(2, 99):", lst8.insert_after(2, 99))
    print("After insert_after(2, 99):", lst8)

    lst9 = DoublyLinkedList()
    lst9.append(10)
    lst9.append(20)
    lst9.append(30)
    print("List:", lst9)
    print("find_index(20):", lst9.find_index(20))
    print("find_index(999):", lst9.find_index(999))

    lst10 = DoublyLinkedList()
    lst10.append(5)
    lst10.append(3)
    lst10.append(5)
    lst10.append(7)
    lst10.append(5)
    print("List:", lst10)
    print("count(5):", lst10.count(5))
    print("count(3):", lst10.count(3))

    lst11 = DoublyLinkedList()
    lst11.append(1)
    lst11.append(2)
    lst11.append(3)
    print("List:", lst11)
    print("is_circular():", lst11.is_circular())

    lst13 = DoublyLinkedList()
    lst13.append(1)
    lst13.append(2)
    lst13.append(1)
    lst13.append(3)
    print("List:", lst13)
    print("has_duplicate():", lst13.has_duplicate())

    lst14 = DoublyLinkedList()
    lst14.append(1)
    lst14.append(2)
    print("List1:", lst14)

    lst15 = DoublyLinkedList()
    lst15.append(3)
    lst15.append(4)
    print("List2:", lst15)

    lst14.merge(lst15)
    print("After merge:", lst14)

    lst15.append(999)
    print("List2 after append(999):", lst15)
    print("List1 after lst2.append(999):", lst14)
    print("Lists are independent (FIXED):", lst14.to_list() == [1, 2, 3, 4])

    print("\n--- DOUBLY LINKED LIST SPECIFIC TESTS ---")

    lst16 = DoublyLinkedList()
    lst16.append(1)
    lst16.append(2)
    lst16.append(3)
    print("List:", lst16)
    print("traverse():", lst16.traverse())
    print("reverse_traverse():", lst16.reverse_traverse())

    lst17 = DoublyLinkedList()
    lst17.append(10)
    lst17.append(20)
    lst17.append(30)
    lst17.append(40)
    print("List:", lst17)
    print("search(20):", lst17.search(20))
    print("search(999):", lst17.search(999))

    lst18 = DoublyLinkedList()
    for i in range(1, 11):
        lst18.append(i)
    print("List (1-10):", lst18)
    print("from_list([100, 200, 300]):")
    lst19 = DoublyLinkedList()
    lst19.from_list([100, 200, 300])
    print("List created from list:", lst19)
