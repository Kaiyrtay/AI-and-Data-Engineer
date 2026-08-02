"""tree.py — a binary tree with its traversals as swappable strategy classes.

`Node` is a single cell (`data` plus `left`/`right` links); `Tree` owns the
root and the structural queries (`height`, `depth`, `degree`). The four
traversals live behind a `TreeTraversal` ABC — `InorderTraversal`,
`PreorderTraversal`, `PostorderTraversal` — so a caller chooses an order by
picking a class, and a new order can be added without touching the tree.

The depth-first orders (in/pre/post) are recursive: each is O(n) time and
O(h) call-stack space, where h is the tree's height.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


class Node:
    """A single binary-tree cell: an integer value plus up to two children."""

    def __init__(self, data: int):
        self.data = data
        self._left = None
        self._right = None

    @property
    def data(self) -> int:
        """The value stored in this node."""
        return self._data

    @data.setter
    def data(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Data must be an integer")
        self._data = value

    @property
    def left(self) -> 'Node' | None:
        """The left child, or None."""
        return self._left

    @property
    def right(self) -> "Node" | None:
        """The right child, or None."""
        return self._right

    def __hash__(self):
        return hash(self.data)

    def __eq__(self, other: Node) -> bool:
        """Structural equality: same value and same left/right subtrees."""
        if not isinstance(other, Node):
            return False
        return self.data == other.data and self.left == other.left and self.right == other.right

    def __repr__(self) -> str:
        return f"Node({self.data})"

    def __str__(self) -> str:
        return repr(self)


class Tree:
    """Owns the root node and answers structural questions about the tree."""

    def __init__(self, root: Node | None = None):
        self.root = root

    @property
    def root(self) -> Node | None:
        """The topmost node, or None when the tree is empty."""
        return self._root

    @root.setter
    def root(self, value: Node | None) -> None:
        if value is not None and not isinstance(value, Node):
            raise TypeError("Root must be a Node or None")
        self._root = value

    def height(self) -> int:
        """Edges on the longest root->leaf path; -1 for an empty tree. Time: O(n)."""
        return self._height(self.root)

    def _height(self, node: Node | None) -> int:
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    def depth(self, target: Node = None) -> int:
        """Edges from the root down to `target`; 0 at the root, -1 if absent. Time: O(n)."""
        return self._depth(self.root, target, 0)

    def _depth(self, node: Node | None, target: Node, d: int) -> int:
        if node is None:
            return -1
        if node is target:
            return d
        found = self._depth(node.left, target, d + 1)
        return found if found != -1 else self._depth(node.right, target, d + 1)

    @staticmethod
    def degree(node: Node) -> int:
        """Number of branches (children) of a node: 0, 1, or 2. Time: O(1)."""
        if not isinstance(node, Node):
            raise TypeError("node must be a Node")
        return (node.left is not None) + (node.right is not None)


class TreeTraversal(ABC):
    """The contract for a traversal strategy — one order per subclass."""

    def __init__(self, tree: Tree):
        self.tree = tree

    @property
    def tree(self) -> Tree:
        """The tree being traversed."""
        return self._tree

    @tree.setter
    def tree(self, value: Tree) -> None:
        if not isinstance(value, Tree):
            raise TypeError("Tree must be an instance of Tree class")
        self._tree = value

    @abstractmethod
    def traverse(self) -> list[int]:
        """Return the node values in this strategy's order."""

    def is_empty(self) -> bool:
        """True when the tree has no root. Time: O(1)."""
        return self.tree.root is None


class InorderTraversal(TreeTraversal):
    """Left -> node -> right. On a BST this yields values in sorted order."""

    def traverse(self) -> list[int]:
        """Values in in-order. Time: O(n), space O(h)."""
        if self.is_empty():
            return []
        return self._inorder(self.tree.root, result=[])

    def _inorder(self, node: Node | None, result: list[int]) -> list[int]:
        if node is not None:
            self._inorder(node.left, result)
            result.append(node.data)
            self._inorder(node.right, result)
        return result


class PreorderTraversal(TreeTraversal):
    """Node -> left -> right. Visits a parent before its children."""

    def traverse(self) -> list[int]:
        """Values in pre-order. Time: O(n), space O(h)."""
        if self.is_empty():
            return []
        return self._preorder(self.tree.root, result=[])

    def _preorder(self, node: Node | None, result: list[int]) -> list[int]:
        if node is not None:
            result.append(node.data)
            self._preorder(node.left, result)
            self._preorder(node.right, result)
        return result


class PostorderTraversal(TreeTraversal):
    """Left -> right -> node. Visits a parent only after both children."""

    def traverse(self) -> list[int]:
        """Values in post-order. Time: O(n), space O(h)."""
        if self.is_empty():
            return []
        return self._postorder(self.tree.root, result=[])

    def _postorder(self, node: Node | None, result: list[int]) -> list[int]:
        if node is not None:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.data)
        return result


if __name__ == "__main__":
    def _check(name: str, case) -> None:
        try:
            case()
            print(f"  PASS   {name}")
        except AssertionError as exc:
            print(f"  FAIL   {name}: {exc}")
        except Exception as exc:
            print(f"  ERROR  {name}: {type(exc).__name__}: {exc}")

    def build_tree() -> Tree:
        #         1
        #        / \
        #       2   3
        #      / \
        #     4   5
        n1, n2, n3, n4, n5 = (Node(i) for i in (1, 2, 3, 4, 5))
        n1._left, n1._right = n2, n3
        n2._left, n2._right = n4, n5
        return Tree(n1)

    def test_inorder():
        assert InorderTraversal(build_tree()).traverse() == [4, 2, 5, 1, 3]

    def test_preorder():
        assert PreorderTraversal(build_tree()).traverse() == [1, 2, 4, 5, 3]

    def test_postorder():
        assert PostorderTraversal(build_tree()).traverse() == [4, 5, 2, 3, 1]

    def test_empty():
        assert InorderTraversal(Tree()).traverse() == []

    def test_height():
        assert build_tree().height() == 2
        assert Tree().height() == -1

    def test_degree():
        t = build_tree()
        assert Tree.degree(t.root) == 2
        assert Tree.degree(t.root.left) == 2
        assert Tree.degree(t.root.left.left) == 0

    def test_degree_validates():
        try:
            Tree.degree(5)
            assert False, "expected TypeError"
        except TypeError:
            pass

    def test_depth():
        t = build_tree()
        assert t.depth(t.root) == 0
        assert t.depth(t.root.right) == 1
        assert t.depth(t.root.left.left) == 2

    print("Tree self-tests:")
    _check("inorder   = [4,2,5,1,3]", test_inorder)
    _check("preorder  = [1,2,4,5,3]", test_preorder)
    _check("postorder = [4,5,2,3,1]", test_postorder)
    _check("empty tree -> []", test_empty)
    _check("height = 2 (empty = -1)", test_height)
    _check("degree: root=2, node2=2, leaf=0", test_degree)
    _check("degree rejects non-Node", test_degree_validates)
    _check("depth: root=0, node3=1, node4=2", test_depth)
