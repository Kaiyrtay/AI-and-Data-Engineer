from typing import Any, Optional


class EmptyListError(Exception):
    pass


class InvalidPositionError(IndexError):
    pass


class Node:
    def __init__(self, value: Any) -> None:
        self.value = value
        self.next = None

    def __str__(self) -> str:
        return str(self.value)


class SinglyLinkedList:
    def __init__(self) -> None:
        self.head = None
        self.tail = None
        self._size = 0

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise ValueError("Size must be a non-negative integer")
        self._size = value

    def convert_to_node(self, value: Any) -> Node:
        if isinstance(value, Node):
            raise TypeError("Value cannot be a Node instance")
        return Node(value)

    def bounds_check(self, position: int, allow_end: bool = False) -> int:
        if not isinstance(position, int):
            raise TypeError("Position must be an integer")
        if position < 0:
            position += self.size
        max_position = self.size if allow_end else self.size - 1
        if position < 0 or position > max_position:
            raise InvalidPositionError(
                f"Position {position} out of bounds for list of size {self.size}")
        return position

    def get(self, position: int) -> Node:
        if self.is_empty():
            raise EmptyListError("Cannot get from empty list")
        position = self.bounds_check(position)
        current = self.head
        for _ in range(position):
            current = current.next
        return current

    def prepend(self, value: Any) -> None:
        new_node = self.convert_to_node(value)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.size += 1

    def append(self, value: Any) -> None:
        new_node = self.convert_to_node(value)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def add_at_position(self, value: Any, position: int) -> None:
        position = self.bounds_check(position, allow_end=True)
        if position == 0:
            self.prepend(value)
            return
        if position == self.size:
            self.append(value)
            return
        new_node = self.convert_to_node(value)
        prev_node = self.get(position - 1)
        new_node.next = prev_node.next
        prev_node.next = new_node
        self.size += 1

    def del_head(self) -> None:
        if self.is_empty():
            raise EmptyListError("Cannot delete from empty list")
        if self.size == 1:
            self.clear()
            return
        self.head = self.head.next
        self.size -= 1

    def del_tail(self) -> None:
        if self.is_empty():
            raise EmptyListError("Cannot delete from empty list")
        if self.size == 1:
            self.clear()
            return
        prev_node = self.get(self.size - 2)
        prev_node.next = None
        self.tail = prev_node
        self.size -= 1

    def del_at_position(self, position: int) -> None:
        if self.is_empty():
            raise EmptyListError("Cannot delete from empty list")
        position = self.bounds_check(position)
        if position == 0:
            self.del_head()
            return
        if position == self.size - 1:
            self.del_tail()
            return
        prev_node = self.get(position - 1)
        prev_node.next = prev_node.next.next
        self.size -= 1

    def search(self, value: Any) -> Optional[Node]:
        current = self.head
        while current:
            if current.value == value:
                return current
            current = current.next
        return None

    def display(self) -> None:
        print(self)

    def traverse(self) -> None:
        self.display()

    def __getitem__(self, position: int) -> Any:
        if self.is_empty():
            raise EmptyListError("Cannot index empty list")
        position = self.bounds_check(position)
        return self.get(position).value

    def __setitem__(self, position: int, value: Any) -> None:
        if self.is_empty():
            raise EmptyListError("Cannot set value in empty list")
        position = self.bounds_check(position)
        new_node = self.convert_to_node(value)
        node = self.get(position)
        node.value = new_node.value

    def __len__(self) -> int:
        return self.size

    def __iter__(self):
        if self.is_empty():
            return iter([])
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __contains__(self, value: Any) -> bool:
        return self.search(value) is not None

    def __eq__(self, other: 'SinglyLinkedList') -> bool:
        if not isinstance(other, SinglyLinkedList):
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
            return "[]"
        result = "["
        current = self.head
        while current:
            result += str(current.value)
            if current.next:
                result += " -> "
            current = current.next
        result += "]"
        return result

    def __repr__(self) -> str:
        if self.is_empty():
            return "SinglyLinkedList()"
        result = "SinglyLinkedList("
        current = self.head
        while current:
            result += str(current.value)
            if current.next:
                result += ", "
            current = current.next
        result += ")"
        return result

    def is_empty(self) -> bool:
        return self.size == 0

    def first(self) -> Any:
        if self.is_empty():
            raise EmptyListError("List is empty")
        return self.head.value

    def last(self) -> Any:
        if self.is_empty():
            raise EmptyListError("List is empty")
        return self.tail.value

    def clear(self) -> None:
        self.head = None
        self.tail = None
        self.size = 0

    def reverse(self) -> None:
        if self.size <= 1:
            return
        prev = None
        current = self.head
        self.tail = current
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def to_list(self) -> list:
        return list(self)

    def remove(self, value: Any) -> bool:
        if self.is_empty():
            return False
        if self.head.value == value:
            self.del_head()
            return True
        current = self.head
        while current.next:
            if current.next.value == value:
                current.next = current.next.next
                if current.next is None:
                    self.tail = current
                self.size -= 1
                return True
            current = current.next
        return False

    def remove_all(self, value: Any) -> int:
        count = 0
        while self.remove(value):
            count += 1
        return count

    def insert_before(self, target_value: Any, new_value: Any) -> bool:
        if self.is_empty():
            return False
        if self.head.value == target_value:
            self.prepend(new_value)
            return True
        current = self.head
        while current.next:
            if current.next.value == target_value:
                new_node = self.convert_to_node(new_value)
                new_node.next = current.next
                current.next = new_node
                self.size += 1
                return True
            current = current.next
        return False

    def insert_after(self, target_value: Any, new_value: Any) -> bool:
        node = self.search(target_value)
        if node is None:
            return False
        new_node = self.convert_to_node(new_value)
        new_node.next = node.next
        node.next = new_node
        if new_node.next is None:
            self.tail = new_node
        self.size += 1
        return True

    def find_index(self, value: Any) -> int:
        current = self.head
        index = 0
        while current:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return -1

    def count(self, value: Any) -> int:
        count = 0
        current = self.head
        while current:
            if current.value == value:
                count += 1
            current = current.next
        return count

    def is_circular(self) -> bool:
        if self.is_empty():
            return False
        slow = self.head
        fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False

    def get_middle(self) -> Any:
        if self.is_empty():
            raise EmptyListError("List is empty")
        slow = self.head
        fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow.value

    def has_duplicate(self) -> bool:
        if self.size <= 1:
            return False
        seen = set()
        current = self.head
        while current:
            if current.value in seen:
                return True
            seen.add(current.value)
            current = current.next
        return False

    def merge(self, other: 'SinglyLinkedList') -> None:
        if other.is_empty():
            return
        if self.is_empty():
            for value in other:
                self.append(value)
            return
        for value in other:
            self.append(value)


if __name__ == "__main__":
    lst = SinglyLinkedList()
    lst.append(1)
    lst.append(2)
    lst.append(3)
    print("After append(1,2,3):", lst)

    lst.prepend(0)
    print("After prepend(0):", lst)

    lst.add_at_position(1.5, 2)
    print("After add_at_position(1.5, 2):", lst)

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

    lst.del_at_position(1)
    print("After del_at_position(1):", lst)

    lst2 = SinglyLinkedList()
    lst2.append(99)
    lst2.append(2)
    print("lst == lst2:", lst == lst2)

    lst3 = SinglyLinkedList()
    lst3.append(2)
    lst3.append(99)
    print("lst == lst3:", lst == lst3)

    lst4 = SinglyLinkedList()
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

    lst5 = SinglyLinkedList()
    lst5.append(5)
    lst5.append(10)
    lst5.append(5)
    lst5.append(15)
    lst5.append(5)
    print("List:", lst5)

    print("remove(5):", lst5.remove(5))
    print("After remove(5):", lst5)

    lst6 = SinglyLinkedList()
    lst6.append(7)
    lst6.append(7)
    lst6.append(7)
    print("List with duplicates:", lst6)
    print("remove_all(7):", lst6.remove_all(7))
    print("After remove_all(7):", lst6)

    lst7 = SinglyLinkedList()
    lst7.append(1)
    lst7.append(2)
    lst7.append(3)
    print("List:", lst7)
    print("insert_before(2, 99):", lst7.insert_before(2, 99))
    print("After insert_before(2, 99):", lst7)

    lst8 = SinglyLinkedList()
    lst8.append(1)
    lst8.append(2)
    lst8.append(3)
    print("List:", lst8)
    print("insert_after(2, 99):", lst8.insert_after(2, 99))
    print("After insert_after(2, 99):", lst8)

    lst9 = SinglyLinkedList()
    lst9.append(10)
    lst9.append(20)
    lst9.append(30)
    print("List:", lst9)
    print("find_index(20):", lst9.find_index(20))
    print("find_index(999):", lst9.find_index(999))

    lst10 = SinglyLinkedList()
    lst10.append(5)
    lst10.append(3)
    lst10.append(5)
    lst10.append(7)
    lst10.append(5)
    print("List:", lst10)
    print("count(5):", lst10.count(5))
    print("count(3):", lst10.count(3))

    lst11 = SinglyLinkedList()
    lst11.append(1)
    lst11.append(2)
    lst11.append(3)
    print("List:", lst11)
    print("is_circular():", lst11.is_circular())

    lst12 = SinglyLinkedList()
    lst12.append(1)
    lst12.append(2)
    lst12.append(3)
    lst12.append(4)
    lst12.append(5)
    print("List:", lst12)
    print("get_middle():", lst12.get_middle())

    lst13 = SinglyLinkedList()
    lst13.append(1)
    lst13.append(2)
    lst13.append(1)
    lst13.append(3)
    print("List:", lst13)
    print("has_duplicate():", lst13.has_duplicate())

    lst14 = SinglyLinkedList()
    lst14.append(1)
    lst14.append(2)
    print("List1:", lst14)

    lst15 = SinglyLinkedList()
    lst15.append(3)
    lst15.append(4)
    print("List2:", lst15)

    lst14.merge(lst15)
    print("After merge:", lst14)

    lst15.append(999)
    print("List2 after append(999):", lst15)
    print("List1 after lst2.append(999):", lst14)
    print("Lists are independent (FIXED):", lst14.to_list() == [1, 2, 3, 4])
