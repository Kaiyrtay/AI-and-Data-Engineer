"""avl.py — a self-balancing binary search tree (AVL).

A BST that keeps every node's balance factor within [-1, 1] by rotating after
inserts and deletes, so its height stays ~log n and search / insert / delete
are all O(log n) even on already-sorted input. Each `Node` caches its own
height; the rotations and `_rebalance` keep that cache correct. Duplicate keys
are ignored
"""

from __future__ import annotations
from typing import Iterator


class Node:
    """An AVL cell: an integer value, a cached height, and up to two children."""

    def __init__(self, data: int) -> None:
        self.data = data
        self.height = 0
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
    def height(self) -> int:
        """This node's cached height (a leaf is 0)."""
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Height must be type integer")
        if value < 0:
            raise ValueError("Node height can not be negative")
        self._height = value

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


class AVL:
    """A self-balancing BST of integers; duplicates ignored, all core ops O(log n)."""

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

    def search(self, value: int) -> Node | None:
        """Find the node holding value using the ordering. Time: O(log n)."""
        if self.is_empty():
            return None
        if not isinstance(value, int):
            raise TypeError("Value must be type integer")
        temp = self.root
        while temp is not None:
            if temp.data == value:
                return temp
            temp = temp.left if temp.data > value else temp.right
        return None

    def DFS(self, value: int) -> Node | None:
        """Depth-first search for value; returns the node or None. Time: O(n)."""
        if self.is_empty():
            return None
        if not isinstance(value, int):
            raise TypeError("Value must be type integer")
        return self._DFS(self.root, value)

    def _DFS(self, node: Node | None, value: int) -> Node | None:
        if node is None:
            return None
        if node.data == value:
            return node
        found = self._DFS(node.left, value)
        return found if found is not None else self._DFS(node.right, value)

    def BFS(self, value: int) -> Node | None:
        """Breadth-first search for value; returns the node or None. Time: O(n)."""
        if self.is_empty():
            return None
        if not isinstance(value, int):
            raise TypeError("Value must be type integer")
        queue: list[Node] = [self.root]
        index = 0
        while index < len(queue):
            node = queue[index]
            index += 1
            if node.data == value:
                return node
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        return None

    def min_value(self) -> int | None:
        """Smallest value (leftmost node), or None if empty. Time: O(log n)."""
        if self.is_empty():
            return None
        temp = self.root
        while temp.left is not None:
            temp = temp.left
        return temp.data

    def max_value(self) -> int | None:
        """Largest value (rightmost node), or None if empty. Time: O(log n)."""
        if self.is_empty():
            return None
        temp = self.root
        while temp.right is not None:
            temp = temp.right
        return temp.data

    def preorder(self) -> list[int]:
        """Values in pre-order (node, left, right). Time: O(n)."""
        if self.is_empty():
            return []
        return self._preorder(self.root, result=[])

    def _preorder(self, node: Node | None, result: list[int]) -> list[int]:
        if node is not None:
            result.append(node.data)
            self._preorder(node.left, result)
            self._preorder(node.right, result)
        return result

    def inorder(self) -> list[int]:
        """Values in in-order (sorted on a BST). Time: O(n)."""
        if self.is_empty():
            return []
        return self._inorder(self.root, result=[])

    def _inorder(self, node: Node | None, result: list[int]) -> list[int]:
        if node is not None:
            self._inorder(node.left, result)
            result.append(node.data)
            self._inorder(node.right, result)
        return result

    def postorder(self) -> list[int]:
        """Values in post-order (left, right, node). Time: O(n)."""
        if self.is_empty():
            return []
        return self._postorder(self.root, result=[])

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
        index = 0
        while index < len(queue):
            node = queue[index]
            index += 1
            result.append(node.data)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        return result

    def height(self) -> int:
        """Edges on the longest root->leaf path; -1 for an empty tree. Time: O(n)."""
        return self._height(self.root)

    def _height(self, node: Node | None) -> int:
        if node is None:
            return -1
        if not isinstance(node, Node):
            raise TypeError("node needs to be type Node or None")
        return 1 + max(self._height(node.left), self._height(node.right))

    def depth(self, target: Node) -> int:
        """Edges from the root down to target; 0 at the root. Time: O(log n)."""
        if self.is_empty():
            raise ValueError("Empty tree")
        if not isinstance(target, Node):
            raise TypeError("Target needs to be type Node")
        return self._depth(self.root, target, 0)

    def _depth_general(self, node: Node | None, target: Node, d: int = 0) -> int:
        """Depth by searching both subtrees; works on any tree. Time: O(n)."""
        if not isinstance(target, Node):
            raise TypeError("Target needs to be type Node")
        if node is None:
            return -1
        if node is target:
            return d
        found = self._depth_general(node.left, target, d + 1)
        return found if found != -1 else self._depth_general(node.right, target, d + 1)

    def _depth(self, node: Node | None, target: Node, d: int = 0) -> int:
        if not isinstance(target, Node):
            raise TypeError("Target needs to be type Node")
        if node is None:
            return -1
        if node.data < target.data:
            return self._depth(node.right, target, d + 1)
        elif node.data > target.data:
            return self._depth(node.left, target, d + 1)
        else:
            return d

    def _node_height(self, node: Node | None) -> int:
        """Cached height of a node, or -1 for None. Time: O(1)."""
        if node is None:
            return -1
        if not isinstance(node, Node):
            raise TypeError("Target needs to be type Node")
        return node.height

    def _update_height(self, node: Node) -> None:
        """Refresh node.height from its children's cached heights. Time: O(1)."""
        if not isinstance(node, Node):
            raise TypeError("Target needs to be type Node")
        node.height = 1 + max(self._node_height(node.left),
                              self._node_height(node.right))

    def _balance_factor(self, node: Node) -> int | None:
        """Left height minus right height; +/- shows the lean. Time: O(1)."""
        if node is None:
            return None
        if not isinstance(node, Node):
            raise TypeError("Target needs to be type Node")
        return self._node_height(node.left) - self._node_height(node.right)

    def _rebalance(self, node: Node) -> Node | None:
        """Update height and rotate if |balance factor| > 1; return the new root. Time: O(1)."""
        if node is None:
            return None
        if not isinstance(node, Node):
            raise TypeError("Target needs to be type Node")
        self._update_height(node)
        balance = self._balance_factor(node)
        if balance > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def _rotate_left(self, node: Node) -> Node | None:
        """Left rotation — fixes a right-heavy node. Time: O(1)."""
        if node is None:
            return None
        if not isinstance(node, Node):
            raise TypeError("Target needs to be type Node")
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def _rotate_right(self, node: Node) -> Node | None:
        """Right rotation — fixes a left-heavy node. Time: O(1)."""
        if node is None:
            return None
        if not isinstance(node, Node):
            raise TypeError("Target needs to be type Node")
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        self._update_height(node)
        self._update_height(new_root)
        return new_root

    def insert(self, value: int) -> None:
        """Insert a value, rebalancing on the way up. Time: O(log n). Duplicates ignored."""
        if not isinstance(value, int):
            raise TypeError("Value needs to be type integer")
        if self.is_empty():
            self.root = Node(value)
            self.size += 1
            return
        if self.search(value) is not None:
            return
        self.root = self._insert(self.root, value)
        self.size += 1

    def _insert(self, node: Node | None, value: int) -> Node:
        if node is None:
            return Node(value)
        if value < node.data:
            node.left = self._insert(node.left, value)
        elif value > node.data:
            node.right = self._insert(node.right, value)
        return self._rebalance(node)

    def delete(self, value: int) -> None:
        """Delete a value, rebalancing on the way up. Time: O(log n)."""
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
        return self._rebalance(node)

    def __repr__(self) -> str:
        return f"AVL(size={self.size}, inorder={self.inorder()})"

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

    def build(values: list[int]) -> AVL:
        tree = AVL(None)
        for v in values:
            tree.insert(v)
        return tree

    def is_balanced(tree: AVL, node: Node | None) -> bool:
        if node is None:
            return True
        if abs(tree._balance_factor(node)) > 1:
            return False
        return is_balanced(tree, node.left) and is_balanced(tree, node.right)

    def test_ascending_stays_balanced():
        t = build(list(range(1, 16)))
        assert t.inorder() == list(range(1, 16))
        assert is_balanced(t, t.root)
        assert t.height() <= 4

    def test_descending_stays_balanced():
        t = build(list(range(15, 0, -1)))
        assert t.inorder() == list(range(1, 16))
        assert is_balanced(t, t.root)

    def test_insert_ignores_duplicates():
        t = build([5, 5, 5, 3, 3])
        assert t.inorder() == [3, 5] and len(t) == 2

    def test_search_dfs_bfs():
        t = build([5, 3, 8, 1, 4])
        assert t.search(4).data == 4 and t.search(99) is None
        assert t.DFS(8).data == 8 and t.DFS(99) is None
        assert t.BFS(1).data == 1 and t.BFS(99) is None

    def test_min_max():
        t = build([5, 3, 8, 1, 9])
        assert t.min_value() == 1 and t.max_value() == 9

    def test_delete_stays_balanced():
        t = build(list(range(1, 16)))
        for v in [1, 8, 15, 4, 12]:
            t.delete(v)
        assert t.inorder() == [2, 3, 5, 6, 7, 9, 10, 11, 13, 14]
        assert is_balanced(t, t.root) and len(t) == 10

    def test_delete_absent_is_noop():
        t = build([5, 3, 8])
        t.delete(99)
        assert t.inorder() == [3, 5, 8] and len(t) == 3

    def test_traversals():
        t = build([2, 1, 3])
        assert t.inorder() == [1, 2, 3]
        assert t.preorder() == [2, 1, 3]
        assert t.postorder() == [1, 3, 2]
        assert t.level_order() == [2, 1, 3]

    def test_empty_edges():
        t = AVL(None)
        assert t.is_empty() and len(t) == 0
        assert t.inorder() == [] and t.height() == -1
        assert t.search(1) is None and t.min_value() is None

    def test_type_guard():
        try:
            AVL(None).insert("x")
            assert False, "expected TypeError"
        except TypeError:
            pass

    print("AVL self-tests:")
    _check("ascending insert stays balanced", test_ascending_stays_balanced)
    _check("descending insert stays balanced", test_descending_stays_balanced)
    _check("insert ignores duplicates", test_insert_ignores_duplicates)
    _check("search / DFS / BFS", test_search_dfs_bfs)
    _check("min / max", test_min_max)
    _check("delete stays balanced", test_delete_stays_balanced)
    _check("delete absent is a no-op", test_delete_absent_is_noop)
    _check("traversals", test_traversals)
    _check("empty-tree edges", test_empty_edges)
    _check("insert type guard", test_type_guard)
