# Data Structures & Algorithms

Twelve structures, built from scratch in pure Python — no wrapping `list`, `dict`, or `collections` internally. The first five are containers; then `Stack` and `Queue` are abstract data types with two backings each; `Tree`, `BST`, and `AVL` are binary trees — `Tree` centered on traversals, `BST` on ordered insert/search/delete, and `AVL` a self-balancing BST; and `BTree` and `BPlusTree` are multi-way search trees, where each node holds many keys and many children so the tree stays short and wide — the shape databases and filesystems index with. Each implements the Python dunder methods that fit its shape (`__len__`, `__iter__`, `__contains__`, `__eq__`, `__str__`, `__repr__`, plus `__getitem__`/`__setitem__` on the indexed sequences) so it behaves like a native container, not a toy class.

## Contents

| File                  | Structure                            | Backing                               | Grows?                                      |
| --------------------- | ------------------------------------ | ------------------------------------- | ------------------------------------------- |
| `StaticArray.py`      | Static array                         | Fixed-capacity slot list              | No — raises once full                       |
| `DynamicArray.py`     | Dynamic array                        | Resizable buffer                      | Yes — doubles/halves, amortized O(1) append |
| `SinglyLinkedList.py` | Singly linked list                   | `Node` with `.next` only              | Yes — unbounded                             |
| `DoublyLinkedList.py` | Doubly linked list                   | `Node` with `.next` and `.prev`       | Yes — unbounded                             |
| `HashTable.py`        | Hash table (set of keys)             | Prime-sized slot array / bucket lists | Yes — rehashes at 0.75 load factor          |
| `Stack.py`            | Stack (LIFO), array- & linked-backed | Resizable buffer / singly linked list | Yes — array doubles; linked is unbounded    |
| `Queue.py`            | Queue (FIFO), array- & linked-backed | Resizable buffer / singly linked list | Yes — array grows; linked is unbounded      |
| `trees/Tree.py`       | Binary tree + traversals             | `Node` with `.left` / `.right`        | Yes — unbounded                             |
| `trees/BST.py`        | Binary search tree                   | `Node` with `.left` / `.right`        | Yes — unbounded                             |
| `trees/AVL.py`        | Self-balancing BST (AVL)             | `Node` with `.left` / `.right` + height | Yes — unbounded                           |
| `trees/B.py`          | B-tree (multi-way search tree)       | Node of sorted keys + child links       | Yes — splits/merges, all leaves one depth |
| `trees/B+.py`         | B+ tree (keys in linked leaves)      | Internal separators + linked leaf chain | Yes — splits/merges, leaves chained       |

---

## StaticArray

Fixed capacity set at construction (`StaticArray(capacity)`). `append`/`insert` raise `IndexError`-style errors once full instead of growing.

**Methods:** `append`, `insert`, `pop`, `remove`, `clear`, `index`, `find`, `is_full`, `is_empty`, `to_list`, plus `capacity`/`size` properties and full dunder support. Internally, `insert`/`pop` shift elements left/right (`_left_shift` / `_right_shift`) to keep the array contiguous.

## DynamicArray

Same public interface as `StaticArray`, but never raises on overflow — `_size_balance` / `_resize` double the backing buffer when full and halve it when usage drops, so `append` is amortized O(1) instead of a hard error.

## SinglyLinkedList

Forward-only list with a tracked `head` **and** `tail`. Beyond the basics (`prepend`, `append`, `add_at_position`, `del_head`, `del_tail`, `del_at_position`, `search`), it includes `reverse`, `merge`, `insert_before`/`insert_after`, `find_index`, `count`, `remove`/`remove_all`, and a couple of interview-staple extras: `is_circular` (Floyd's cycle detection), `get_middle` (fast/slow pointer), and `has_duplicate`.

## DoublyLinkedList

The most complete of the four — 36 methods, `prev`/`next` on every node. Same feature set as `SinglyLinkedList` plus `insert`(at index), `reverse_traverse`, and `from_list`. Its `get(index)` is the standout: it picks whichever end (head or tail) is closer to the target index and traverses from there, so average lookup cost is O(n/2) rather than O(n):

```python
def get(self, index):
    if index < self.size // 2:
        return self._from_head(index)   # closer to head
    else:
        return self._from_tail(index)   # closer to tail
```

Negative indexing (`lst[-1]`), in-place `reverse()` via pointer-swap, and `merge()` (splicing one list onto the tail of another) are also implemented.

## HashTable

Four collision-handling techniques behind one abstract interface. `HashTable` (an ABC) owns the shared machinery — load factor, resize policy, the `insert`/`search`/`delete` API, and the dunders — and each subclass supplies only how a key is placed, found, and removed:

- `SeparateChainingHashTable` — open hashing; each bucket is a list, collisions chain.
- `LinearProbing` — closed hashing; probe `home, home+1, home+2, …` (simple, but clusters).
- `QuadraticProbing` — probe `home + 1, +4, +9, …` to break up that clustering.
- `DoubleHashing` — a second hash sets the stride, so colliding keys diverge onto different paths.

Deletion uses tombstones (a `_DELETED` sentinel) so removing a key never severs a probe chain: search treats a tombstone as occupied and keeps going, while insert is free to reuse it. The table holds a **prime** capacity and rehashes every live key into the next prime once the load factor reaches 0.75, which keeps operations near O(1). Being a set of keys, it supports the container dunders except `__getitem__`/`__setitem__`, which don't apply to unordered keys. Run `python HashTable.py` to execute the built-in self-tests — empty / one / many-with-resize / duplicate / delete-and-reinsert / invalid input / deliberate failure, across all four techniques.

## Stack

One LIFO contract, two backings. `Stack` (an ABC) fixes the interface — `push`, `pop`, `peek`, `__len__`, `__repr__`, plus a shared `is_empty` and `__str__` — and two classes fill it in differently:

- `ArrayStack` — a contiguous, resizable buffer. `_count` does double duty as the item count **and** the index of the next free slot, so the top always sits at `_count - 1`. `push` fills the free slot and doubles the buffer (`_resize`) when it runs out, making append amortized O(1); `pop` clears the vacated slot so its reference can be garbage-collected.
- `LinkedStack` — composition over a hand-rolled `Node`/`LinkedList`, pushing and popping at the head. Every operation is true O(1) with no resize, and it can never be "full". `pop`/`peek` hand back the `Node`; `pop_value`/`peek_value` return just the stored value.

Errors are specific — `StackEmptyError` on an empty `pop`/`peek`, `StackFullError` reserved for a fixed-capacity variant — all under a `StackError` base, so callers catch precisely instead of a bare `except`. Because both stacks satisfy the same interface, any caller that depends on the contract works with either; swapping `ArrayStack` for `LinkedStack` changes nothing else.

## Queue

One FIFO contract, two backings. `Queue` (an ABC) fixes the interface — `enqueue`, `dequeue`, `peek`, `is_empty`, `size`, `clear`, `to_array`, `__str__` — and two classes implement it differently:

- `ArrayQueue` — a resizable buffer with the front pinned at index 0. `enqueue` writes at index `size` and doubles the buffer when full (amortized O(1)); `dequeue` removes the front and shifts every remaining item down one slot, so it is O(n). Neither operation accepts `None`, so a `None` slot always means "empty".
- `LinkedListQueue` — a singly linked list holding both `head` (front) and `tail` (back) pointers. `enqueue` links onto the tail and `dequeue` unlinks the head, both true O(1); it can never be "full". `dequeue`/`peek` hand back the `Node`; `peek_value` returns just the stored value.

Errors are specific — `QueueEmptyError` on an empty `dequeue`/`peek` — under a `QueueError` base. Because both queues satisfy the same interface, any caller depending on the contract works with either: the array one trades an O(n) dequeue for cache-friendly contiguity, the linked one trades a pointer per node for true O(1) at both ends.

## Tree

A binary tree whose four traversals are swappable strategy classes. `Node` holds a value and `left`/`right` children; `Tree` owns the root and answers the structural questions — `height` (edges on the longest root→leaf path, −1 when empty), `depth` (edges from the root down to a given node, 0 at the root), and `degree` (a node's child count, 0–2).

`Tree` also classifies its own shape (each O(n)):

- `is_full` — every node has 0 or 2 children, never exactly 1.
- `is_perfect` — full **and** every leaf sits at the same depth.
- `is_complete` — every level full except the last, which fills left to right (tested with the array-index trick: a node at `i` has children at `2i+1`/`2i+2`).
- `is_balanced` — left/right subtree heights differ by ≤ 1 at every node (one O(n) pass, using `-2` as an "unbalanced" sentinel).
- `is_degenerate` — every node has at most one child; a chain that may switch sides (also called *pathological*).
- `is_skewed` — a degenerate tree leaning entirely one way, i.e. `is_left_skewed` or `is_right_skewed`.

The traversals sit behind a `TreeTraversal` ABC, so an order is chosen by picking a class rather than passing a flag, and a new order can be added without touching the tree:

- `InorderTraversal` — left → node → right (yields sorted order on a BST).
- `PreorderTraversal` — node → left → right (parent before its children).
- `PostorderTraversal` — left → right → node (parent after both children).

All three are recursive: O(n) time and O(h) call-stack space for height h. Node equality is structural (same value and same subtrees). Run `python Tree.py` for the built-in self-tests across the traversals, `height`/`depth`/`degree`, and the shape predicates.

## BST

A binary search tree of integers holding the ordering invariant *left subtree < node < right subtree*; duplicate keys are ignored. `Node` carries a value and validated `left`/`right` children; `BST` tracks `root` and `size`.

The core operations — `insert`, `search`, `delete` — come in both iterative and recursive forms, each O(h). `delete` covers the three cases: a leaf (unlinked), one child (spliced out), and two children (the value is replaced by its in-order successor, which is then removed). Alongside them are `_successor_node`/`_predecessor_node` (each returning `[parent, node]` for the two-child delete), `min_value`/`max_value`, and `height`/`depth`.

All four traversals are built in — `preorder`, `inorder` (sorted output on a BST), `postorder` (depth-first), and `level_order` (breadth-first). It behaves like a native container via `__len__`, `__contains__`, `__iter__` (in-order), `__eq__` (structural tree equality), and `__repr__`/`__str__`. Run `python BST.py` for the built-in self-tests covering insert/search, all three delete shapes, the traversals, min/max, height/depth, equality, and empty-tree edges.

## AVL

A **self-balancing** BST — the answer to the plain BST's flaw, where sorted input skews it into a linked list and everything degrades to O(n). An `AVL` holds the same ordering as a BST but adds one invariant: **every node's balance factor stays within [−1, 1]**. After each insert or delete it rebalances on the way back up, so its height stays ~log n and search / insert / delete are all O(log n) *even on already-sorted input*.

The machinery:

- Each `Node` **caches its own height**, so a balance-factor check is O(1) (`_node_height`, `_update_height`, `_balance_factor`).
- `_rotate_left` / `_rotate_right` are the two primitive fixes; `_rebalance` picks the right one of the four cases (LL / RR / LR / RL) from a node's balance factor and its heavy child's.
- `insert` and `delete` are recursive — the call stack *is* the path back up, so `return self._rebalance(node)` fires at every ancestor, updating heights and rotating where needed. Delete reuses the in-order successor for the two-child case, same as the BST.

It carries the full BST surface too — `search` (O(log n)), `DFS`/`BFS` search, `min_value`/`max_value`, all four traversals, `height`/`depth`. Run `python AVL.py` for the self-tests, which insert 1…15 ascending *and* descending (the exact input that skews a plain BST) and assert the tree stays balanced with height ≤ 4, plus balanced-through-deletes, duplicates ignored, and empty-tree edges.

## B-tree

A **B-tree** is the multi-way generalization of the BST: instead of one key and two children per node, each node holds a sorted run of keys and one more child than it has keys, so the tree grows wide and stays shallow. That high fan-out is the whole point — on disk or across a cache line, lookup cost is dominated by how many *nodes* you touch, and a fat node means far fewer touches. `BTree` is parametrized by a **minimum degree** `minimum_degree` (≥ 2): every node except the root holds between `minimum_degree − 1` and `2·minimum_degree − 1` keys, every internal node has between `minimum_degree` and `2·minimum_degree` children, and — the invariant that makes it a B-tree — **all leaves sit at exactly the same depth**. Duplicate keys are ignored. (A node's keys and child links live in plain Python lists; a B-tree node *is* a small sorted array by definition, so this is the one place a list is used structurally rather than as a scratch buffer.)

Growth happens top-down by **proactive splitting**: on the way down to insert, any full child is split first — its median key rises into the parent and the node halves — so a parent is never full when its child splits, and the tree grows only by pushing a key up, occasionally lifting the root by one level. Deletion is the mirror image and the fiddly part: before descending into a child that holds only the minimum `minimum_degree − 1` keys, `_fill` first **borrows** a key from a neighbouring sibling (rotating it through the parent) or, if neither sibling can spare one, **merges** the child, a separator, and a sibling back into a single node. Deleting a key that sits in an internal node replaces it with its in-order predecessor or successor drawn from a child that can spare one, falling back to a merge — the same three cases as the BST delete, one level richer.

Beyond `insert` / `search` (returning `(node, position)`) / `delete`, it carries `min_value`, `max_value`, `height` (all leaves share it, so it's a single walk down the left spine), an `inorder` that yields every key sorted, a `level_order` grouped one list per node, and the container dunders (`__len__`, `__contains__`, `__iter__` in sorted order, structural `__eq__`, `__repr__`/`__str__`). Run `python B.py` for the self-tests — sorted inserts, duplicate handling, both delete shapes, shallow height on 99 keys, empty-tree edges, and a randomized 30 × 400-operation stress test that re-checks every B-tree invariant after each op.

## B+ tree

A **B+ tree** is a B-tree tuned for range scans, and it is what most database indexes and filesystems actually run on. Two changes from `B.py`: **all keys live in the leaves** — internal nodes hold only *separators*, routing keys that say "≥ this goes right," never the data itself, so a value can appear once as a leaf key and again as a separator above it; and **the leaves are chained** — each leaf points to the next, so once you descend to the start of a range you walk the leaf list straight through instead of climbing back up. That chain is exactly why `range_query(low, high)` and a full in-order iteration are simple left-to-right scans here, running in O(log n + k) for k hits.

`BPlusTree` is parametrized by `order` (≥ 3), the maximum children an internal node may have (so a leaf holds up to `order − 1` keys). Insert is recursive and **bottom-up**: it walks to the correct leaf, drops the key in, and if the node overflows it splits and hands a separator back up to the parent, which may split in turn — a leaf split *copies* its middle key up (the key still lives in the leaf), while an internal split *moves* its median up (as in a plain B-tree). Delete removes from the leaf, then repairs underflow on the way back up by borrowing from a sibling or merging — keeping every non-root leaf at ≥ `order // 2` keys, every non-root internal node at ≥ ⌈`order` ∕ 2⌉ children, and the leaf chain intact across a merge.

The surface mirrors the B-tree — `search` (always descends to a leaf), `min_value`, `max_value`, `height`, `level_order`, `__iter__` walking the leaf chain in sorted order — plus `range_query` and a `keys()` convenience. The behavioural contrast worth internalizing: in a B-tree a search can stop early at an internal node, but in a B+ tree every search runs all the way to a leaf; you trade that for dramatically cheaper ranges. Run `python "B+.py"` for the self-tests — sorted inserts, reverse-insert leaf-chain order, `range_query` cases, borrow-and-merge deletes, empty-tree edges, and the same randomized 30 × 400-operation invariant stress test, with random range queries checked against a reference set.

---

## Complexity

| Operation       | StaticArray             | DynamicArray    | SinglyLinkedList       | DoublyLinkedList              |
| --------------- | ----------------------- | --------------- | ---------------------- | ----------------------------- |
| Access by index | O(1)                    | O(1)            | O(n)                   | O(n) — O(n/2) avg via `get()` |
| Append          | O(1) (or error if full) | O(1) amortized  | O(1) (tail tracked)    | O(1)                          |
| Prepend         | O(n) shift              | O(n) shift      | O(1)                   | O(1)                          |
| Insert at index | O(n) shift              | O(n) shift      | O(n)                   | O(n)                          |
| Delete head     | O(n) shift              | O(n) shift      | O(1)                   | O(1)                          |
| Delete tail     | O(1)                    | O(1)            | O(n) — no back-pointer | O(1)                          |
| Search by value | O(n)                    | O(n)            | O(n)                   | O(n)                          |
| Space overhead  | none (fixed)            | unused capacity | 1 pointer/node         | 2 pointers/node               |

`HashTable` is a set of keys, not an indexed sequence, so its operations don't map onto the columns above — it gets its own table:

| Operation | Average | Worst case                                                              |
| --------- | ------- | ----------------------------------------------------------------------- |
| Insert    | O(1)    | O(n) — clustering or a resize                                           |
| Search    | O(1)    | O(n) — every key on one probe path / in one bucket                      |
| Delete    | O(1)    | O(n)                                                                    |
| Space     | O(n)    | O(n) — chaining adds per-node list overhead; probing stays in one array |

The 0.75 resize threshold and prime sizing are what keep the average at O(1); adversarial hashing or a pathological load is what pushes any of the four to O(n).

`Stack` is an ADT, not an indexed sequence, so like `HashTable` it gets its own line — every operation touches only the top:

| Operation      | ArrayStack                         | LinkedStack    |
| -------------- | ---------------------------------- | -------------- |
| push           | O(1) amortized — doubles when full | O(1)           |
| pop            | O(1)                               | O(1)           |
| peek           | O(1)                               | O(1)           |
| Space overhead | unused buffer capacity             | 1 pointer/node |

`Queue` is an ADT too — items enter at the back and leave from the front:

| Operation      | ArrayQueue                         | LinkedListQueue |
| -------------- | ---------------------------------- | --------------- |
| enqueue        | O(1) amortized — doubles when full | O(1)            |
| dequeue        | O(n) — shifts the rest down        | O(1)            |
| peek           | O(1)                               | O(1)            |
| Space overhead | unused buffer capacity             | 1 pointer/node  |

`Tree`'s traversals visit every node, and its structural queries walk the tree:

| Operation               | Binary tree           |
| ----------------------- | --------------------- |
| Traversal (in/pre/post) | O(n) time, O(h) stack |
| height                  | O(n)                  |
| depth                   | O(n)                  |
| degree                  | O(1)                  |

`BST` operations follow the tree's height h — O(log n) when balanced, O(n) when skewed:

| Operation                | Average  | Worst case (skewed) |
| ------------------------ | -------- | ------------------- |
| insert / search / delete | O(log n) | O(n)                |
| min / max                | O(log n) | O(n)                |
| Traversal (any order)    | O(n)     | O(n)                |

`AVL` is a BST whose balancing removes the worst case — the height is bounded at ~1.44·log n, so there is no "skewed" column:

| Operation                | Guaranteed |
| ------------------------ | ---------- |
| insert / search / delete | O(log n)   |
| min / max                | O(log n)   |
| rotation / balance check | O(1)       |
| Traversal (any order)    | O(n)       |

`BTree`'s height is Θ(log n) *guaranteed* — every leaf sits at the same depth — and the cost inside each node is a scan of up to `2·minimum_degree − 1` keys:

| Operation                | Guaranteed                  |
| ------------------------ | --------------------------- |
| search / insert / delete | O(minimum_degree · log n)   |
| min / max                | O(log n)                    |
| split / borrow / merge   | O(minimum_degree)           |
| inorder / level_order    | O(n)                        |

`BPlusTree` matches it and adds the operation it exists for — a range scan that pays log n to find the start, then walks the leaf chain:

| Operation                 | Guaranteed       |
| ------------------------- | ---------------- |
| search / insert / delete  | O(order · log n) |
| range_query (k hits)      | O(log n + k)     |
| min / max                 | O(log n)         |
| split / borrow / merge    | O(order)         |
| iterate all / level_order | O(n)             |

## Background reading

Reference links used while building these live in `__materials.txt` — from arrays (static vs. dynamic, RAM storage) and linked-list fundamentals through to the B-tree, the B+ tree, and a B-tree-vs-B+-tree comparison.
