"""bst.py — a binary search tree over integer keys.

`Node` holds a value and left/right children. `BST` maintains the ordering
invariant (left subtree < node < right subtree) and supports insert, search,
delete (iterative and recursive), in-order successor/predecessor, the three
depth-first traversals, breadth-first level-order, and the structural queries
(height, depth, min, max). Duplicate keys are ignored.
"""

from __future__ import annotations
from typing import Iterator


class Node:
    """A single BST cell: an integer value plus up to two children."""

    def __init__(self, data: int) -> None:
        self.data = data
        self.left = None
        self.right = None

    @property
    def data(self) -> int:
        """The value stored in this node."""
        return self._data

    @data.setter
    def data(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Value must be type integer")
        self._data = value

    @property
    def left(self) -> Node | None:
        """The left child, or None."""
        return self._left

    @left.setter
    def left(self, value: Node | None) -> None:
        if not isinstance(value, Node) and value is not None:
            raise TypeError("Value must be type Node or None")
        self._left = value

    @property
    def right(self) -> Node | None:
        """The right child, or None."""
        return self._right

    @right.setter
    def right(self, value: Node | None) -> None:
        if not isinstance(value, Node) and value is not None:
            raise TypeError("Value must be type Node or None")
        self._right = value

    def __hash__(self) -> int:
        return hash(self.data)

    def __eq__(self, other: object) -> bool:
        """Structural equality: same value and same left/right subtrees."""
        if not isinstance(other, Node):
            return False
        return self.data == other.data and self.left == other.left and self.right == other.right

    def __repr__(self) -> str:
        return f"Node(data={self.data})"

    def __str__(self) -> str:
        return repr(self)


class BST:
    """A binary search tree of integers; duplicates are ignored."""

    def __init__(self, root: Node | None) -> None:
        self.root = root
        self.size = int(root is not None)

    @property
    def root(self) -> Node | None:
        """The topmost node, or None when the tree is empty."""
        return self._root

    @root.setter
    def root(self, value: Node | None) -> None:
        if value is not None and not isinstance(value, Node):
            raise TypeError("root must be a Node or None")
        self._root = value

    @property
    def size(self) -> int:
        """Number of nodes in the tree."""
        return self._size

    @size.setter
    def size(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Size needs to be int type")
        if value < 0:
            raise ValueError("Size can not be negative")
        self._size = value

    def __len__(self) -> int:
        """Number of nodes. Time: O(1)."""
        return self.size

    def is_empty(self) -> bool:
        """True when the tree has no nodes. Time: O(1)."""
        return self.root is None

    def insert(self, value: int) -> None:
        """Insert a value iteratively; duplicates are ignored. Time: O(h)."""
        if not isinstance(value, int):
            raise TypeError("Value must be type of integer")
        if self.size == 0:
            self.root = Node(value)
            self.size += 1
            return
        temp = self.root
        while temp:
            if temp.data < value:
                if temp.right is None:
                    temp.right = Node(value)
                    self.size += 1
                    break
                temp = temp.right
            elif temp.data > value:
                if temp.left is None:
                    temp.left = Node(value)
                    self.size += 1
                    break
                temp = temp.left
            else:
                break

    def insert_recursive(self, value: int, node: Node | None = None) -> None:
        """Insert a value recursively; duplicates are ignored. Time: O(h)."""
        if not isinstance(value, int):
            raise TypeError("Value must be type of integer")
        if node is None:
            node = self.root
        if self.size == 0:
            self.root = Node(value)
            self.size += 1
            return
        if node.data < value:
            if node.right is None:
                node.right = Node(value)
                self.size += 1
                return
            self.insert_recursive(value, node.right)
        elif node.data > value:
            if node.left is None:
                node.left = Node(value)
                self.size += 1
                return
            self.insert_recursive(value, node.left)
        else:
            return

    def delete(self, value: int) -> None:
        """Delete a value iteratively. Time: O(h). Two-child case uses the in-order successor."""
        if not isinstance(value, int):
            raise TypeError("Value must be type of integer")
        parent = None
        current = self.root
        while current is not None and current.data != value:
            parent = current
            current = current.left if value < current.data else current.right
        if current is None:
            return

        if current.left is not None and current.right is not None:
            successor_parent = current
            successor = current.right
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left
            current.data = successor.data
            current, parent = successor, successor_parent

        child = current.left if current.left is not None else current.right
        if parent is None:
            self.root = child
        elif parent.left is current:
            parent.left = child
        else:
            parent.right = child
        self.size -= 1

    def delete_recursive(self, value: int) -> None:
        """Delete a value recursively. Time: O(h). Two-child case uses the in-order successor."""
        if not isinstance(value, int):
            raise TypeError("Value must be type of integer")
        if self.search(value) is None:
            return
        self.root = self._delete(self.root, value)
        self.size -= 1

    def _delete(self, node: Node | None, value: int) -> Node | None:
        if node is None:
            return None
        if value < node.data:
            node.left = self._delete(node.left, value)
        elif value > node.data:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.data = successor.data
            node.right = self._delete(node.right, successor.data)
        return node

    def search(self, value: int) -> Node | None:
        """Return the node holding value, or None. Time: O(h)."""
        if not isinstance(value, int):
            raise TypeError("Value must be type of integer")
        temp = self.root
        while temp:
            if temp.data == value:
                return temp
            temp = temp.right if temp.data < value else temp.left
        return None

    def _successor_node(self, node: Node) -> list[Node | None] | None:
        """[parent, successor] within the right subtree, or None. Time: O(h)."""
        if not isinstance(node, Node):
            raise TypeError("Given value needs to be type of Node")
        parent = None
        child = node
        if child.right is not None:
            parent = child
            child = child.right
            while child.left is not None:
                parent = child
                child = child.left
        return [parent, child] if child is not node else None

    def _predecessor_node(self, node: Node) -> list[Node | None] | None:
        """[parent, predecessor] within the left subtree, or None. Time: O(h)."""
        if not isinstance(node, Node):
            raise TypeError("Given value needs to be type of Node")
        parent = None
        child = node
        if child.left is not None:
            parent = child
            child = child.left
            while child.right is not None:
                parent = child
                child = child.right
        return [parent, child] if child is not node else None

    def height(self) -> int:
        """Edges on the longest root->leaf path; -1 for an empty tree. Time: O(n)."""
        return self._height(self.root)

    def _height(self, node: Node | None) -> int:
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    def depth(self, target: Node) -> int:
        """Edges from the root down to target; 0 at the root, -1 if absent. Time: O(n)."""
        return self._depth(self.root, target, 0)

    def _depth(self, node: Node | None, target: Node, d: int) -> int:
        if node is None:
            return -1
        if node is target:
            return d
        found = self._depth(node.left, target, d + 1)
        return found if found != -1 else self._depth(node.right, target, d + 1)

    def min_value(self) -> int:
        """Smallest value (leftmost node). Time: O(h). Raises on an empty tree."""
        if self.root is None:
            raise ValueError("min_value from an empty tree")
        temp = self.root
        while temp.left is not None:
            temp = temp.left
        return temp.data

    def max_value(self) -> int:
        """Largest value (rightmost node). Time: O(h). Raises on an empty tree."""
        if self.root is None:
            raise ValueError("max_value from an empty tree")
        temp = self.root
        while temp.right is not None:
            temp = temp.right
        return temp.data

    def preorder(self) -> list[int]:
        """Values in pre-order (node, left, right). Time: O(n)."""
        return self._preorder(self.root, [])

    def _preorder(self, node: Node | None, result: list[int]) -> list[int]:
        if node is not None:
            result.append(node.data)
            self._preorder(node.left, result)
            self._preorder(node.right, result)
        return result

    def inorder(self) -> list[int]:
        """Values in in-order (left, node, right) — sorted on a BST. Time: O(n)."""
        return self._inorder(self.root, [])

    def _inorder(self, node: Node | None, result: list[int]) -> list[int]:
        if node is not None:
            self._inorder(node.left, result)
            result.append(node.data)
            self._inorder(node.right, result)
        return result

    def postorder(self) -> list[int]:
        """Values in post-order (left, right, node). Time: O(n)."""
        return self._postorder(self.root, [])

    def _postorder(self, node: Node | None, result: list[int]) -> list[int]:
        if node is not None:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.data)
        return result

    def level_order(self) -> list[int]:
        """Values breadth-first, level by level. Time: O(n)."""
        if self.is_empty():
            return []
        result: list[int] = []
        queue: list[Node] = [self.root]
        i = 0
        while i < len(queue):
            node = queue[i]
            i += 1
            result.append(node.data)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        return result

    def __contains__(self, value: object) -> bool:
        """True if value is in the tree. Time: O(h)."""
        return isinstance(value, int) and self.search(value) is not None

    def __iter__(self) -> Iterator[int]:
        """Iterate values in sorted (in-order) order. Time: O(n)."""
        yield from self.inorder()

    def __eq__(self, other: object) -> bool:
        """Two BSTs are equal when their trees have identical shape and values."""
        if not isinstance(other, BST):
            return NotImplemented
        return self.root == other.root

    def __repr__(self) -> str:
        return f"BST(size={self.size}, inorder={self.inorder()})"

    def __str__(self) -> str:
        return repr(self)


if __name__ == "__main__":
    def _check(name: str, case) -> None:
        try:
            case()
            print(f"  PASS   {name}")
        except AssertionError as exc:
            print(f"  FAIL   {name}: {exc}")
        except Exception as exc:
            print(f"  ERROR  {name}: {type(exc).__name__}: {exc}")

    def build(values: list[int]) -> BST:
        tree = BST(None)
        for v in values:
            tree.insert(v)
        return tree

    def test_insert_inorder_sorted():
        t = build([5, 3, 8, 2, 4, 7, 9])
        assert t.inorder() == [2, 3, 4, 5, 7, 8, 9]
        assert len(t) == 7

    def test_insert_ignores_duplicates():
        t = build([5, 5, 5])
        assert t.inorder() == [5] and len(t) == 1

    def test_insert_recursive_matches():
        t = BST(None)
        for v in [5, 3, 8, 2, 4]:
            t.insert_recursive(v)
        assert t.inorder() == [2, 3, 4, 5, 8]

    def test_search():
        t = build([5, 3, 8])
        assert t.search(3).data == 3
        assert t.search(99) is None

    def test_contains():
        t = build([5, 3, 8])
        assert 3 in t
        assert 99 not in t
        assert "x" not in t

    def test_traversals():
        t = build([5, 3, 8, 2, 4])
        assert t.preorder() == [5, 3, 2, 4, 8]
        assert t.inorder() == [2, 3, 4, 5, 8]
        assert t.postorder() == [2, 4, 3, 8, 5]
        assert t.level_order() == [5, 3, 8, 2, 4]

    def test_height_and_depth():
        t = build([5, 3, 8, 2])
        assert t.height() == 2
        assert t.depth(t.root) == 0
        assert t.depth(t.search(2)) == 2

    def test_min_max():
        t = build([5, 3, 8, 2, 9])
        assert t.min_value() == 2
        assert t.max_value() == 9

    def test_delete_leaf():
        t = build([5, 3, 8])
        t.delete(3)
        assert t.inorder() == [5, 8] and len(t) == 2

    def test_delete_one_child():
        t = build([5, 3, 8, 2])
        t.delete(3)
        assert t.inorder() == [2, 5, 8]

    def test_delete_two_children():
        t = build([5, 3, 8, 2, 4])
        t.delete(3)
        assert t.inorder() == [2, 4, 5, 8]

    def test_delete_root():
        t = build([5, 3, 8])
        t.delete(5)
        assert t.inorder() == [3, 8] and len(t) == 2

    def test_delete_absent_is_noop():
        t = build([5, 3, 8])
        t.delete(99)
        assert t.inorder() == [3, 5, 8] and len(t) == 3

    def test_delete_recursive():
        t = build([5, 3, 8, 2, 4])
        t.delete_recursive(3)
        assert t.inorder() == [2, 4, 5, 8]

    def test_iter_sorted():
        assert list(build([5, 3, 8, 2])) == [2, 3, 5, 8]

    def test_equality():
        assert build([5, 3, 8]) == build([5, 3, 8])
        assert build([5, 3, 8]) != build([5, 3, 9])

    def test_empty_tree_edges():
        t = BST(None)
        assert t.is_empty() and len(t) == 0
        assert t.inorder() == [] and t.level_order() == []
        assert t.height() == -1
        assert t.search(1) is None
        assert 1 not in t

    def test_min_on_empty_raises():
        try:
            BST(None).min_value()
            assert False, "expected ValueError"
        except ValueError:
            pass

    def test_insert_type_guard():
        try:
            BST(None).insert("x")
            assert False, "expected TypeError"
        except TypeError:
            pass

    print("BST self-tests:")
    _check("insert -> inorder sorted", test_insert_inorder_sorted)
    _check("insert ignores duplicates", test_insert_ignores_duplicates)
    _check("insert_recursive matches", test_insert_recursive_matches)
    _check("search found / not found", test_search)
    _check("__contains__ (incl. non-int)", test_contains)
    _check("preorder / inorder / postorder / level_order", test_traversals)
    _check("height and depth", test_height_and_depth)
    _check("min_value / max_value", test_min_max)
    _check("delete leaf", test_delete_leaf)
    _check("delete node with one child", test_delete_one_child)
    _check("delete node with two children", test_delete_two_children)
    _check("delete root", test_delete_root)
    _check("delete absent value is a no-op", test_delete_absent_is_noop)
    _check("delete_recursive", test_delete_recursive)
    _check("iterate in sorted order", test_iter_sorted)
    _check("BST equality", test_equality)
    _check("empty-tree edge cases", test_empty_tree_edges)
    _check("min_value on empty raises", test_min_on_empty_raises)
    _check("insert type guard", test_insert_type_guard)
