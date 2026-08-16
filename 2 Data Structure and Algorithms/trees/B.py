"""b.py — a B-tree over integer keys.

A B-tree is the multi-way generalization of a BST: instead of one key and two
children per node, a node holds many keys and many children, so the tree stays
short and wide. That high fan-out is what makes it the structure databases and
filesystems use — fewer, larger nodes mean fewer expensive reads.

Parametrized by a *minimum degree* (>= 2), named `minimum_degree` throughout.
Every node except the root holds between ``minimum_degree - 1`` and
``2 * minimum_degree - 1`` keys; every internal node has between
``minimum_degree`` and ``2 * minimum_degree`` children; all leaves sit at the
same depth. Keys are kept sorted inside each node. Duplicate keys are ignored.

`Node` is the internal cell — a sorted key array plus a child array (empty on a
leaf). `BTree` owns the root and the public API: insert (proactive split on the
way down), search, delete (CLRS borrow/merge so a child always has at least
`minimum_degree` keys before we descend), the structural queries (min, max,
height), an in-order walk that yields keys sorted, a level-order walk grouped by
node, and the container dunders so it reads like a native set of keys.
"""

from __future__ import annotations
from typing import Iterator


class Node:
    """A B-tree cell: a sorted list of keys and, unless a leaf, one more child than keys."""

    def __init__(self, minimum_degree: int, leaf: bool) -> None:
        self.minimum_degree = minimum_degree
        self.leaf = leaf
        self.keys: list[int] = []
        self.children: list[Node] = []

    @property
    def minimum_degree(self) -> int:
        """The owning tree's minimum degree (>= 2)."""
        return self._minimum_degree

    @minimum_degree.setter
    def minimum_degree(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("minimum_degree must be type integer")
        if value < 2:
            raise ValueError("minimum_degree must be >= 2")
        self._minimum_degree = value

    @property
    def leaf(self) -> bool:
        """True when this node has no children."""
        return self._leaf

    @leaf.setter
    def leaf(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("leaf must be type bool")
        self._leaf = value

    def is_full(self) -> bool:
        """True when the node holds the maximum 2*minimum_degree - 1 keys. Time: O(1)."""
        return len(self.keys) == 2 * self.minimum_degree - 1

    def __len__(self) -> int:
        """Number of keys held in this node. Time: O(1)."""
        return len(self.keys)

    def __eq__(self, other: object) -> bool:
        """Structural equality: same keys and same child subtrees, in order."""
        if not isinstance(other, Node):
            return False
        return self.keys == other.keys and self.children == other.children

    def __repr__(self) -> str:
        kind = "leaf" if self.leaf else "internal"
        return f"Node({kind}, keys={self.keys})"

    def __str__(self) -> str:
        return repr(self)


class BTree:
    """A B-tree of integers with a minimum degree; duplicates ignored, core ops O(minimum_degree·log n)."""

    def __init__(self, minimum_degree: int = 2) -> None:
        self.minimum_degree = minimum_degree
        self.root: Node | None = None
        self.size = 0

    @property
    def minimum_degree(self) -> int:
        """Minimum degree: nodes hold minimum_degree-1..2*minimum_degree-1 keys, and one more child than keys."""
        return self._minimum_degree

    @minimum_degree.setter
    def minimum_degree(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("minimum_degree must be type integer")
        if value < 2:
            raise ValueError("minimum_degree must be >= 2")
        self._minimum_degree = value

    @property
    def size(self) -> int:
        """Number of keys in the tree."""
        return self._size

    @size.setter
    def size(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Size needs to be int type")
        if value < 0:
            raise ValueError("Size can not be negative")
        self._size = value

    def __len__(self) -> int:
        """Number of keys in the tree. Time: O(1)."""
        return self.size

    def is_empty(self) -> bool:
        """True when the tree holds no keys. Time: O(1)."""
        return self.root is None

    # --- search -------------------------------------------------------------

    def search(self, key: int) -> tuple[Node, int] | None:
        """Return (node, position) of the cell holding key, or None. Time: O(minimum_degree·log n)."""
        if not isinstance(key, int):
            raise TypeError("Key must be type integer")
        return self._search(self.root, key)

    def _search(self, node: Node | None, key: int) -> tuple[Node, int] | None:
        if node is None:
            return None
        position = 0
        while position < len(node.keys) and key > node.keys[position]:
            position += 1
        if position < len(node.keys) and node.keys[position] == key:
            return (node, position)
        if node.leaf:
            return None
        return self._search(node.children[position], key)

    # --- insert -------------------------------------------------------------

    def insert(self, key: int) -> None:
        """Insert a key, splitting full nodes on the way down. Time: O(minimum_degree·log n). Duplicates ignored."""
        if not isinstance(key, int):
            raise TypeError("Key must be type integer")
        if self.root is None:
            self.root = Node(self.minimum_degree, leaf=True)
            self.root.keys.append(key)
            self.size += 1
            return
        if self.search(key) is not None:
            return
        root = self.root
        if root.is_full():
            new_root = Node(self.minimum_degree, leaf=False)
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
            self._insert_non_full(new_root, key)
        else:
            self._insert_non_full(root, key)
        self.size += 1

    def _split_child(self, parent: Node, child_index: int) -> None:
        """Split parent.children[child_index] (which is full) around its median. Time: O(minimum_degree)."""
        degree = self.minimum_degree
        full_child = parent.children[child_index]
        new_sibling = Node(degree, leaf=full_child.leaf)
        median_key = full_child.keys[degree - 1]
        new_sibling.keys = full_child.keys[degree:]
        full_child.keys = full_child.keys[: degree - 1]
        if not full_child.leaf:
            new_sibling.children = full_child.children[degree:]
            full_child.children = full_child.children[:degree]
        parent.keys.insert(child_index, median_key)
        parent.children.insert(child_index + 1, new_sibling)

    def _insert_non_full(self, node: Node, key: int) -> None:
        """Insert key into a node guaranteed not to be full. Time: O(minimum_degree·log n)."""
        position = len(node.keys) - 1
        if node.leaf:
            node.keys.append(key)
            while position >= 0 and key < node.keys[position]:
                node.keys[position + 1] = node.keys[position]
                position -= 1
            node.keys[position + 1] = key
        else:
            while position >= 0 and key < node.keys[position]:
                position -= 1
            position += 1
            if node.children[position].is_full():
                self._split_child(node, position)
                if key > node.keys[position]:
                    position += 1
            self._insert_non_full(node.children[position], key)

    # --- delete -------------------------------------------------------------

    def delete(self, key: int) -> None:
        """Delete a key, keeping every descended child at >= minimum_degree keys. Time: O(minimum_degree·log n). No-op if absent."""
        if not isinstance(key, int):
            raise TypeError("Key must be type integer")
        if self.root is None or self.search(key) is None:
            return
        self._delete(self.root, key)
        self.size -= 1
        if len(self.root.keys) == 0:
            self.root = None if self.root.leaf else self.root.children[0]

    def _find_key_index(self, node: Node, key: int) -> int:
        """Smallest index where node.keys[index] >= key. Time: O(minimum_degree)."""
        index = 0
        while index < len(node.keys) and node.keys[index] < key:
            index += 1
        return index

    def _delete(self, node: Node, key: int) -> None:
        index = self._find_key_index(node, key)
        if index < len(node.keys) and node.keys[index] == key:
            if node.leaf:
                node.keys.pop(index)
            else:
                self._delete_internal(node, index)
        else:
            if node.leaf:
                return
            key_beyond_last_separator = index == len(node.keys)
            if len(node.children[index].keys) < self.minimum_degree:
                self._fill(node, index)
            if key_beyond_last_separator and index > len(node.keys):
                self._delete(node.children[index - 1], key)
            else:
                self._delete(node.children[index], key)

    def _delete_internal(self, node: Node, index: int) -> None:
        key = node.keys[index]
        if len(node.children[index].keys) >= self.minimum_degree:
            predecessor = self._get_predecessor(node, index)
            node.keys[index] = predecessor
            self._delete(node.children[index], predecessor)
        elif len(node.children[index + 1].keys) >= self.minimum_degree:
            successor = self._get_successor(node, index)
            node.keys[index] = successor
            self._delete(node.children[index + 1], successor)
        else:
            self._merge(node, index)
            self._delete(node.children[index], key)

    def _get_predecessor(self, node: Node, index: int) -> int:
        """Rightmost key of the left subtree of node.keys[index]. Time: O(log n)."""
        current = node.children[index]
        while not current.leaf:
            current = current.children[-1]
        return current.keys[-1]

    def _get_successor(self, node: Node, index: int) -> int:
        """Leftmost key of the right subtree of node.keys[index]. Time: O(log n)."""
        current = node.children[index + 1]
        while not current.leaf:
            current = current.children[0]
        return current.keys[0]

    def _fill(self, node: Node, index: int) -> None:
        """Grow node.children[index] to >= minimum_degree keys by borrowing or merging. Time: O(minimum_degree)."""
        if index != 0 and len(node.children[index - 1].keys) >= self.minimum_degree:
            self._borrow_from_prev(node, index)
        elif index != len(node.keys) and len(node.children[index + 1].keys) >= self.minimum_degree:
            self._borrow_from_next(node, index)
        elif index != len(node.keys):
            self._merge(node, index)
        else:
            self._merge(node, index - 1)

    def _borrow_from_prev(self, node: Node, index: int) -> None:
        """Rotate a key from the left sibling through the parent into children[index]. Time: O(minimum_degree)."""
        child = node.children[index]
        left_sibling = node.children[index - 1]
        child.keys.insert(0, node.keys[index - 1])
        if not child.leaf:
            child.children.insert(0, left_sibling.children.pop())
        node.keys[index - 1] = left_sibling.keys.pop()

    def _borrow_from_next(self, node: Node, index: int) -> None:
        """Rotate a key from the right sibling through the parent into children[index]. Time: O(minimum_degree)."""
        child = node.children[index]
        right_sibling = node.children[index + 1]
        child.keys.append(node.keys[index])
        if not child.leaf:
            child.children.append(right_sibling.children.pop(0))
        node.keys[index] = right_sibling.keys.pop(0)

    def _merge(self, node: Node, index: int) -> None:
        """Merge children[index], separator keys[index], and children[index+1] into one node. Time: O(minimum_degree)."""
        child = node.children[index]
        right_sibling = node.children[index + 1]
        child.keys.append(node.keys[index])
        child.keys.extend(right_sibling.keys)
        if not child.leaf:
            child.children.extend(right_sibling.children)
        node.keys.pop(index)
        node.children.pop(index + 1)

    # --- structural queries -------------------------------------------------

    def min_value(self) -> int:
        """Smallest key (leftmost leaf, first slot). Time: O(log n). Raises on an empty tree."""
        if self.root is None:
            raise ValueError("min_value from an empty tree")
        current = self.root
        while not current.leaf:
            current = current.children[0]
        return current.keys[0]

    def max_value(self) -> int:
        """Largest key (rightmost leaf, last slot). Time: O(log n). Raises on an empty tree."""
        if self.root is None:
            raise ValueError("max_value from an empty tree")
        current = self.root
        while not current.leaf:
            current = current.children[-1]
        return current.keys[-1]

    def height(self) -> int:
        """Edges from root to a leaf (all leaves share it); -1 for an empty tree. Time: O(log n)."""
        if self.root is None:
            return -1
        edges = 0
        current = self.root
        while not current.leaf:
            current = current.children[0]
            edges += 1
        return edges

    # --- traversals ---------------------------------------------------------

    def inorder(self) -> list[int]:
        """All keys in sorted order (in-order over the multi-way tree). Time: O(n)."""
        return self._inorder(self.root, [])

    def _inorder(self, node: Node | None, result: list[int]) -> list[int]:
        if node is None:
            return result
        for position, key in enumerate(node.keys):
            if not node.leaf:
                self._inorder(node.children[position], result)
            result.append(key)
        if not node.leaf:
            self._inorder(node.children[-1], result)
        return result

    def level_order(self) -> list[list[int]]:
        """Keys breadth-first, grouped one list per node. Time: O(n)."""
        if self.root is None:
            return []
        result: list[list[int]] = []
        queue: list[Node] = [self.root]
        cursor = 0
        while cursor < len(queue):
            node = queue[cursor]
            cursor += 1
            result.append(list(node.keys))
            queue.extend(node.children)
        return result

    # --- dunders ------------------------------------------------------------

    def __contains__(self, key: object) -> bool:
        """True if key is in the tree. Time: O(minimum_degree·log n)."""
        return isinstance(key, int) and self.search(key) is not None

    def __iter__(self) -> Iterator[int]:
        """Iterate keys in sorted order. Time: O(n)."""
        yield from self.inorder()

    def __eq__(self, other: object) -> bool:
        """Two B-trees are equal when they share a minimum degree and have identical node structure."""
        if not isinstance(other, BTree):
            return NotImplemented
        return self.minimum_degree == other.minimum_degree and self.root == other.root

    def __repr__(self) -> str:
        return f"BTree(minimum_degree={self.minimum_degree}, size={self.size}, keys={self.inorder()})"

    def __str__(self) -> str:
        return repr(self)


if __name__ == "__main__":
    import random

    def _check(name: str, case) -> None:
        try:
            case()
            print(f"  PASS   {name}")
        except AssertionError as exc:
            print(f"  FAIL   {name}: {exc}")
        except Exception as exc:
            print(f"  ERROR  {name}: {type(exc).__name__}: {exc}")

    def build(values: list[int], minimum_degree: int = 2) -> BTree:
        tree = BTree(minimum_degree)
        for value in values:
            tree.insert(value)
        return tree

    def leaf_depths(node: Node | None, depth: int, out: set[int]) -> None:
        if node is None:
            return
        if node.leaf:
            out.add(depth)
            return
        for child in node.children:
            leaf_depths(child, depth + 1, out)

    def assert_invariants(tree: BTree) -> None:
        """Every B-tree property: sorted keys, key/child counts, uniform leaf depth."""
        if tree.root is None:
            return
        degree = tree.minimum_degree
        depths: set[int] = set()
        leaf_depths(tree.root, 0, depths)
        assert len(depths) == 1, f"leaves at differing depths: {depths}"

        def walk(node: Node, is_root: bool) -> None:
            assert node.keys == sorted(node.keys), f"unsorted keys {node.keys}"
            assert len(node.keys) <= 2 * degree - 1, f"overfull node {node.keys}"
            if not is_root:
                assert len(node.keys) >= degree - 1, f"underfull node {node.keys}"
            if not node.leaf:
                assert len(node.children) == len(node.keys) + 1, "child/key count mismatch"
                for position, key in enumerate(node.keys):
                    assert node.children[position].keys[-1] < key < node.children[position + 1].keys[0], "separator order broken"
                for child in node.children:
                    walk(child, False)

        walk(tree.root, True)

    def test_insert_sorted_and_len():
        tree = build([10, 20, 5, 6, 12, 30, 7, 17], minimum_degree=2)
        assert tree.inorder() == [5, 6, 7, 10, 12, 17, 20, 30]
        assert len(tree) == 8
        assert_invariants(tree)

    def test_insert_ignores_duplicates():
        tree = build([5, 5, 5, 3, 3], minimum_degree=2)
        assert tree.inorder() == [3, 5] and len(tree) == 2

    def test_search_and_contains():
        tree = build([10, 20, 5, 6, 12, 30, 7, 17])
        node, position = tree.search(12)
        assert node.keys[position] == 12
        assert tree.search(99) is None
        assert 17 in tree and 99 not in tree and "x" not in tree

    def test_height_grows_slowly():
        tree = build(list(range(1, 100)), minimum_degree=3)
        assert tree.inorder() == list(range(1, 100))
        assert tree.height() <= 4
        assert_invariants(tree)

    def test_min_max():
        tree = build([10, 20, 5, 6, 12, 30, 7, 17])
        assert tree.min_value() == 5 and tree.max_value() == 30

    def test_level_order_grouped():
        tree = build([1, 2, 3, 4, 5], minimum_degree=2)
        levels = tree.level_order()
        assert levels[0] == [2] and [1] in levels

    def test_delete_leaf_and_internal():
        tree = build([10, 20, 5, 6, 12, 30, 7, 17], minimum_degree=2)
        for value in [6, 20, 10]:
            tree.delete(value)
        assert tree.inorder() == [5, 7, 12, 17, 30]
        assert_invariants(tree)

    def test_delete_all_down_to_empty():
        tree = build(list(range(1, 40)), minimum_degree=2)
        for value in range(1, 40):
            tree.delete(value)
        assert tree.is_empty() and len(tree) == 0 and tree.inorder() == []

    def test_delete_absent_is_noop():
        tree = build([5, 3, 8])
        tree.delete(99)
        assert tree.inorder() == [3, 5, 8] and len(tree) == 3

    def test_equality():
        assert build([5, 3, 8]) == build([8, 5, 3])
        assert build([5, 3, 8]) != build([5, 3, 9])

    def test_empty_edges():
        tree = BTree(2)
        assert tree.is_empty() and len(tree) == 0 and tree.inorder() == []
        assert tree.height() == -1 and tree.search(1) is None and 1 not in tree

    def test_type_guard():
        try:
            BTree(2).insert("x")
            assert False, "expected TypeError"
        except TypeError:
            pass

    def test_bad_degree():
        try:
            BTree(1)
            assert False, "expected ValueError"
        except ValueError:
            pass

    def test_random_stress_invariants():
        rng = random.Random(42)
        for _ in range(30):
            degree = rng.randint(2, 5)
            tree = BTree(degree)
            reference: set[int] = set()
            for _ in range(400):
                key = rng.randint(0, 200)
                if rng.random() < 0.6:
                    tree.insert(key)
                    reference.add(key)
                else:
                    tree.delete(key)
                    reference.discard(key)
                assert tree.inorder() == sorted(reference)
                assert_invariants(tree)

    print("B-tree self-tests:")
    _check("insert -> sorted, correct length", test_insert_sorted_and_len)
    _check("insert ignores duplicates", test_insert_ignores_duplicates)
    _check("search / __contains__", test_search_and_contains)
    _check("height stays shallow (99 keys, minimum_degree=3)", test_height_grows_slowly)
    _check("min_value / max_value", test_min_max)
    _check("level_order grouped by node", test_level_order_grouped)
    _check("delete leaf + internal keys", test_delete_leaf_and_internal)
    _check("delete everything down to empty", test_delete_all_down_to_empty)
    _check("delete absent is a no-op", test_delete_absent_is_noop)
    _check("B-tree equality", test_equality)
    _check("empty-tree edges", test_empty_edges)
    _check("insert type guard", test_type_guard)
    _check("minimum_degree < 2 rejected", test_bad_degree)
    _check("randomized insert/delete keeps invariants", test_random_stress_invariants)
