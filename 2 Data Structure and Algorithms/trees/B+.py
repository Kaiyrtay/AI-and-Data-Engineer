"""bplus.py — a B+ tree over integer keys.

A B+ tree is a B-tree tuned for range scans, and it is what most database
indexes and filesystems actually run on. Two changes from the plain B-tree in
`b.py`:

1. **All keys live in the leaves.** Internal nodes hold only *separators* —
   routing keys that say "everything >= this goes right" — never the data
   itself. A separator is a copy of the smallest key in the subtree to its
   right, so the same value can appear once as a leaf key and again as a router
   above it.
2. **The leaves form a linked list.** Each leaf points to the next, so once you
   descend to the start of a range you walk the leaf chain straight through
   instead of climbing back up the tree. That is why `range_query` and a full
   in-order iteration are simple left-to-right scans here.

Parametrized by `order` (>= 3), the maximum number of children an internal node
may have. A leaf holds up to ``order - 1`` keys; on overflow a node splits and
pushes a separator up. Deletes borrow from a sibling or merge, keeping every
non-root leaf at >= ``order // 2`` keys and every non-root internal node at
>= ``ceil(order / 2)`` children. Duplicate keys are ignored.
"""

from __future__ import annotations
from typing import Iterator


class Node:
    """A B+ tree cell. A leaf holds data keys and a `next` link; an internal node holds separators and children."""

    def __init__(self, leaf: bool) -> None:
        self.leaf = leaf
        self.keys: list[int] = []
        self.children: list[Node] = []
        self.next: Node | None = None

    @property
    def leaf(self) -> bool:
        """True when this node stores data keys (rather than separators)."""
        return self._leaf

    @leaf.setter
    def leaf(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("leaf must be type bool")
        self._leaf = value

    @property
    def next(self) -> Node | None:
        """Next leaf in the left-to-right chain (leaves only), else None."""
        return self._next

    @next.setter
    def next(self, value: Node | None) -> None:
        if value is not None and not isinstance(value, Node):
            raise TypeError("next must be a Node or None")
        self._next = value

    def __len__(self) -> int:
        """Number of keys held in this node. Time: O(1)."""
        return len(self.keys)

    def __eq__(self, other: object) -> bool:
        """Structural equality: same keys and same child subtrees, in order."""
        if not isinstance(other, Node):
            return False
        return self.leaf == other.leaf and self.keys == other.keys and self.children == other.children

    def __repr__(self) -> str:
        kind = "leaf" if self.leaf else "internal"
        return f"Node({kind}, keys={self.keys})"

    def __str__(self) -> str:
        return repr(self)


class BPlusTree:
    """A B+ tree of integers with a given order; data in linked leaves, duplicates ignored."""

    def __init__(self, order: int = 4) -> None:
        self.order = order
        self.root: Node | None = None
        self.size = 0

    @property
    def order(self) -> int:
        """Maximum children per internal node (max keys per leaf is order - 1)."""
        return self._order

    @order.setter
    def order(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("order must be type integer")
        if value < 3:
            raise ValueError("order must be >= 3")
        self._order = value

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

    @property
    def _max_leaf_keys(self) -> int:
        """A leaf may hold at most this many keys before it splits."""
        return self.order - 1

    @property
    def _min_leaf_keys(self) -> int:
        """A non-root leaf must hold at least this many keys."""
        return self.order // 2

    @property
    def _min_children(self) -> int:
        """A non-root internal node must hold at least this many children."""
        return (self.order + 1) // 2

    def __len__(self) -> int:
        """Number of keys in the tree. Time: O(1)."""
        return self.size

    def is_empty(self) -> bool:
        """True when the tree holds no keys. Time: O(1)."""
        return self.root is None

    def _child_index(self, node: Node, key: int) -> int:
        """Index of the child to descend into for key (>= separator goes right). Time: O(order)."""
        index = 0
        while index < len(node.keys) and key >= node.keys[index]:
            index += 1
        return index

    # --- search -------------------------------------------------------------

    def search(self, key: int) -> bool:
        """True if key is stored in a leaf. Time: O(order·log n)."""
        if not isinstance(key, int):
            raise TypeError("Key must be type integer")
        leaf = self._find_leaf(key)
        return leaf is not None and key in leaf.keys

    def _find_leaf(self, key: int) -> Node | None:
        """Descend to the leaf that would hold key. Time: O(order·log n)."""
        node = self.root
        while node is not None and not node.leaf:
            node = node.children[self._child_index(node, key)]
        return node

    # --- insert -------------------------------------------------------------

    def insert(self, key: int) -> None:
        """Insert a key; overflowing nodes split and push a separator up. Time: O(order·log n). Duplicates ignored."""
        if not isinstance(key, int):
            raise TypeError("Key must be type integer")
        if self.root is None:
            self.root = Node(leaf=True)
            self.root.keys.append(key)
            self.size += 1
            return
        if self.search(key):
            return
        split = self._insert(self.root, key)
        if split is not None:
            separator, right_node = split
            new_root = Node(leaf=False)
            new_root.keys.append(separator)
            new_root.children.extend([self.root, right_node])
            self.root = new_root
        self.size += 1

    def _insert(self, node: Node, key: int) -> tuple[int, Node] | None:
        """Insert into the subtree; return (separator, new_right_node) if it split. Time: O(order·log n)."""
        if node.leaf:
            index = 0
            while index < len(node.keys) and node.keys[index] < key:
                index += 1
            node.keys.insert(index, key)
            if len(node.keys) > self._max_leaf_keys:
                return self._split_leaf(node)
            return None
        index = self._child_index(node, key)
        split = self._insert(node.children[index], key)
        if split is None:
            return None
        separator, right_node = split
        node.keys.insert(index, separator)
        node.children.insert(index + 1, right_node)
        if len(node.children) > self.order:
            return self._split_internal(node)
        return None

    def _split_leaf(self, node: Node) -> tuple[int, Node]:
        """Split an overfull leaf; the right half's first key is copied up. Time: O(order)."""
        middle = len(node.keys) // 2
        right_node = Node(leaf=True)
        right_node.keys = node.keys[middle:]
        node.keys = node.keys[:middle]
        right_node.next = node.next
        node.next = right_node
        return right_node.keys[0], right_node

    def _split_internal(self, node: Node) -> tuple[int, Node]:
        """Split an overfull internal node; the median separator moves up. Time: O(order)."""
        middle = len(node.keys) // 2
        separator = node.keys[middle]
        right_node = Node(leaf=False)
        right_node.keys = node.keys[middle + 1:]
        right_node.children = node.children[middle + 1:]
        node.keys = node.keys[:middle]
        node.children = node.children[: middle + 1]
        return separator, right_node

    # --- delete -------------------------------------------------------------

    def delete(self, key: int) -> None:
        """Delete a key from its leaf, then borrow/merge to repair underflow. Time: O(order·log n). No-op if absent."""
        if not isinstance(key, int):
            raise TypeError("Key must be type integer")
        if self.root is None or not self.search(key):
            return
        self._delete(self.root, key)
        self.size -= 1
        if not self.root.leaf and len(self.root.children) == 1:
            self.root = self.root.children[0]
        elif self.root.leaf and len(self.root.keys) == 0:
            self.root = None

    def _delete(self, node: Node, key: int) -> None:
        if node.leaf:
            if key in node.keys:
                node.keys.remove(key)
            return
        index = self._child_index(node, key)
        child = node.children[index]
        self._delete(child, key)
        if self._is_underfull(child):
            self._repair(node, index)

    def _is_underfull(self, node: Node) -> bool:
        """True when a node has dropped below its minimum occupancy. Time: O(1)."""
        if node.leaf:
            return len(node.keys) < self._min_leaf_keys
        return len(node.children) < self._min_children

    def _repair(self, parent: Node, index: int) -> None:
        """Fix an underfull parent.children[index] by borrowing from or merging with a sibling. Time: O(order)."""
        if index > 0 and self._can_spare(parent.children[index - 1]):
            self._borrow_from_prev(parent, index)
        elif index < len(parent.children) - 1 and self._can_spare(parent.children[index + 1]):
            self._borrow_from_next(parent, index)
        elif index > 0:
            self._merge(parent, index - 1)
        else:
            self._merge(parent, index)

    def _can_spare(self, node: Node) -> bool:
        """True when a sibling can give up a key/child and stay legal. Time: O(1)."""
        if node.leaf:
            return len(node.keys) > self._min_leaf_keys
        return len(node.children) > self._min_children

    def _borrow_from_prev(self, parent: Node, index: int) -> None:
        """Move one key/child from the left sibling into children[index]. Time: O(1)."""
        child = parent.children[index]
        left_sibling = parent.children[index - 1]
        if child.leaf:
            child.keys.insert(0, left_sibling.keys.pop())
            parent.keys[index - 1] = child.keys[0]
        else:
            child.keys.insert(0, parent.keys[index - 1])
            parent.keys[index - 1] = left_sibling.keys.pop()
            child.children.insert(0, left_sibling.children.pop())

    def _borrow_from_next(self, parent: Node, index: int) -> None:
        """Move one key/child from the right sibling into children[index]. Time: O(1)."""
        child = parent.children[index]
        right_sibling = parent.children[index + 1]
        if child.leaf:
            child.keys.append(right_sibling.keys.pop(0))
            parent.keys[index] = right_sibling.keys[0]
        else:
            child.keys.append(parent.keys[index])
            parent.keys[index] = right_sibling.keys.pop(0)
            child.children.append(right_sibling.children.pop(0))

    def _merge(self, parent: Node, index: int) -> None:
        """Merge children[index] and children[index+1] into one, dropping separator keys[index]. Time: O(order)."""
        left_child = parent.children[index]
        right_child = parent.children[index + 1]
        if left_child.leaf:
            left_child.keys.extend(right_child.keys)
            left_child.next = right_child.next
        else:
            left_child.keys.append(parent.keys[index])
            left_child.keys.extend(right_child.keys)
            left_child.children.extend(right_child.children)
        parent.keys.pop(index)
        parent.children.pop(index + 1)

    # --- structural queries -------------------------------------------------

    def min_value(self) -> int:
        """Smallest key (first key of the leftmost leaf). Time: O(log n). Raises on an empty tree."""
        if self.root is None:
            raise ValueError("min_value from an empty tree")
        node = self.root
        while not node.leaf:
            node = node.children[0]
        return node.keys[0]

    def max_value(self) -> int:
        """Largest key (last key of the rightmost leaf). Time: O(log n). Raises on an empty tree."""
        if self.root is None:
            raise ValueError("max_value from an empty tree")
        node = self.root
        while not node.leaf:
            node = node.children[-1]
        return node.keys[-1]

    def height(self) -> int:
        """Edges from root to a leaf (all leaves share it); -1 for an empty tree. Time: O(log n)."""
        if self.root is None:
            return -1
        edges = 0
        node = self.root
        while not node.leaf:
            node = node.children[0]
            edges += 1
        return edges

    # --- scans --------------------------------------------------------------

    def range_query(self, low: int, high: int) -> list[int]:
        """Sorted keys k with low <= k <= high, walking the leaf chain. Time: O(log n + hits)."""
        if not isinstance(low, int) or not isinstance(high, int):
            raise TypeError("Range bounds must be type integer")
        if low > high:
            raise ValueError("low must be <= high")
        result: list[int] = []
        node = self._find_leaf(low)
        while node is not None:
            for key in node.keys:
                if key > high:
                    return result
                if key >= low:
                    result.append(key)
            node = node.next
        return result

    def keys(self) -> list[int]:
        """All keys in sorted order via the leaf chain. Time: O(n)."""
        return list(self)

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
        """True if key is in the tree. Time: O(order·log n)."""
        return isinstance(key, int) and self.search(key)

    def __iter__(self) -> Iterator[int]:
        """Iterate keys in sorted order along the leaf chain. Time: O(n)."""
        node = self.root
        if node is None:
            return
        while not node.leaf:
            node = node.children[0]
        while node is not None:
            yield from node.keys
            node = node.next

    def __eq__(self, other: object) -> bool:
        """Two B+ trees are equal when they share an order and identical node structure."""
        if not isinstance(other, BPlusTree):
            return NotImplemented
        return self.order == other.order and self.root == other.root

    def __repr__(self) -> str:
        return f"BPlusTree(order={self.order}, size={self.size}, keys={list(self)})"

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

    def build(values: list[int], order: int = 4) -> BPlusTree:
        tree = BPlusTree(order)
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

    def leaf_chain_keys(tree: BPlusTree) -> list[int]:
        node = tree.root
        if node is None:
            return []
        while not node.leaf:
            node = node.children[0]
        out: list[int] = []
        while node is not None:
            out.extend(node.keys)
            node = node.next
        return out

    def assert_invariants(tree: BPlusTree) -> None:
        """All B+ tree properties: uniform leaf depth, occupancy bounds, separators, and a sorted leaf chain."""
        if tree.root is None:
            return
        depths: set[int] = set()
        leaf_depths(tree.root, 0, depths)
        assert len(depths) == 1, f"leaves at differing depths: {depths}"
        chain = leaf_chain_keys(tree)
        assert chain == sorted(chain), "leaf chain not sorted"
        assert chain == list(tree), "__iter__ disagrees with leaf chain"

        def subtree_keys(node: Node) -> list[int]:
            if node.leaf:
                return node.keys
            collected: list[int] = []
            for child in node.children:
                collected.extend(subtree_keys(child))
            return collected

        def walk(node: Node, is_root: bool) -> None:
            assert node.keys == sorted(node.keys), f"unsorted keys {node.keys}"
            if node.leaf:
                assert len(node.keys) <= tree._max_leaf_keys, f"overfull leaf {node.keys}"
                if not is_root:
                    assert len(node.keys) >= tree._min_leaf_keys, f"underfull leaf {node.keys}"
                return
            assert len(node.children) == len(node.keys) + 1, "child/key count mismatch"
            assert len(node.children) <= tree.order, "too many children"
            if not is_root:
                assert len(node.children) >= tree._min_children, "too few children"
            for position, separator in enumerate(node.keys):
                assert max(subtree_keys(node.children[position])) < separator, "left subtree >= separator"
                assert min(subtree_keys(node.children[position + 1])) >= separator, "right subtree < separator"
            for child in node.children:
                walk(child, False)

        walk(tree.root, True)

    def test_insert_sorted_and_len():
        tree = build([10, 20, 5, 6, 12, 30, 7, 17], order=4)
        assert list(tree) == [5, 6, 7, 10, 12, 17, 20, 30] and len(tree) == 8
        assert_invariants(tree)

    def test_insert_ignores_duplicates():
        tree = build([5, 5, 5, 3, 3], order=4)
        assert list(tree) == [3, 5] and len(tree) == 2

    def test_search_and_contains():
        tree = build([10, 20, 5, 6, 12, 30, 7, 17])
        assert tree.search(12) and not tree.search(99)
        assert 17 in tree and 99 not in tree and "x" not in tree

    def test_leaf_chain_sorted():
        tree = build(list(range(50, 0, -1)), order=5)
        assert leaf_chain_keys(tree) == list(range(1, 51))
        assert_invariants(tree)

    def test_range_query():
        tree = build(list(range(1, 100)), order=4)
        assert tree.range_query(20, 30) == list(range(20, 31))
        assert tree.range_query(0, 5) == [1, 2, 3, 4, 5]
        assert tree.range_query(97, 200) == [97, 98, 99]
        assert tree.range_query(1000, 2000) == []

    def test_height_and_minmax():
        tree = build(list(range(1, 100)), order=5)
        assert tree.height() <= 4
        assert tree.min_value() == 1 and tree.max_value() == 99

    def test_delete_borrow_and_merge():
        tree = build(list(range(1, 20)), order=4)
        for value in [1, 2, 3, 10, 19, 11]:
            tree.delete(value)
        assert list(tree) == [4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 18]
        assert_invariants(tree)

    def test_delete_all_down_to_empty():
        tree = build(list(range(1, 40)), order=4)
        for value in range(1, 40):
            tree.delete(value)
        assert tree.is_empty() and len(tree) == 0 and list(tree) == []

    def test_delete_absent_is_noop():
        tree = build([5, 3, 8])
        tree.delete(99)
        assert list(tree) == [3, 5, 8] and len(tree) == 3

    def test_equality():
        assert build([5, 3, 8]) == build([8, 5, 3])
        assert build([5, 3, 8]) != build([5, 3, 9])

    def test_empty_edges():
        tree = BPlusTree(4)
        assert tree.is_empty() and len(tree) == 0 and list(tree) == []
        assert tree.height() == -1 and not tree.search(1) and 1 not in tree
        assert tree.range_query(0, 10) == []

    def test_type_and_order_guards():
        try:
            BPlusTree(4).insert("x")
            assert False, "expected TypeError"
        except TypeError:
            pass
        try:
            BPlusTree(2)
            assert False, "expected ValueError"
        except ValueError:
            pass

    def test_random_stress_invariants():
        rng = random.Random(7)
        for _ in range(30):
            order = rng.randint(3, 6)
            tree = BPlusTree(order)
            reference: set[int] = set()
            for _ in range(400):
                key = rng.randint(0, 200)
                if rng.random() < 0.6:
                    tree.insert(key)
                    reference.add(key)
                else:
                    tree.delete(key)
                    reference.discard(key)
                assert list(tree) == sorted(reference)
                assert_invariants(tree)
            low, high = sorted((rng.randint(0, 200), rng.randint(0, 200)))
            assert tree.range_query(low, high) == sorted(k for k in reference if low <= k <= high)

    print("B+ tree self-tests:")
    _check("insert -> sorted, correct length", test_insert_sorted_and_len)
    _check("insert ignores duplicates", test_insert_ignores_duplicates)
    _check("search / __contains__", test_search_and_contains)
    _check("leaf chain stays sorted (reverse insert)", test_leaf_chain_sorted)
    _check("range_query over leaf chain", test_range_query)
    _check("height shallow + min/max", test_height_and_minmax)
    _check("delete with borrow + merge", test_delete_borrow_and_merge)
    _check("delete everything down to empty", test_delete_all_down_to_empty)
    _check("delete absent is a no-op", test_delete_absent_is_noop)
    _check("B+ tree equality", test_equality)
    _check("empty-tree edges", test_empty_edges)
    _check("type + order guards", test_type_and_order_guards)
    _check("randomized insert/delete keeps invariants", test_random_stress_invariants)
