"""trie.py — a prefix tree (trie) over strings, usable as a set or a word->value map.

`TrieNode` holds a children map (next-character -> node), an end-of-word flag,
an optional attached value, and a cached count of the complete words in its
subtree. It never stores its own character (that is the key in its parent's
dict) or its word (that is the path from the root), so every node is reached by
walking one dict lookup per character from the root — which is why retrieval
always starts there. Words that begin the same share nodes (desk / desktop);
words that only end the same do not (desktop / stop split at the root).

`Trie` supports insert, search, prefix test, prefix count, longest-prefix match,
autocomplete listing, value get/put, delete with pruning, sorted iteration, and
full dunder support. Every core operation is O(L) in the key length L, and
independent of how many words are stored. Run `python Trie.py` for the tests.
"""

from __future__ import annotations
from typing import Any, Iterable, Iterator

# Sentinel meaning "no value was passed", so a plain set-style insert(word)
# never overwrites data attached by an earlier insert(word, value).
_UNSET = object()


class TrieNode:
    """A single trie cell: child links, an end flag, attached data, a subtree count."""

    def __init__(self) -> None:
        self.children = {}
        self.is_end = False
        self.count = 0
        self.value: Any = None

    @property
    def children(self) -> dict[str, TrieNode]:
        """Child links, keyed by the next character."""
        return self._children

    @children.setter
    def children(self, value: dict[str, TrieNode]) -> None:
        if not isinstance(value, dict):
            raise TypeError("children must be a dict")
        self._children = value

    @property
    def is_end(self) -> bool:
        """True when a complete word ends at this node."""
        return self._is_end

    @is_end.setter
    def is_end(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise TypeError("is_end must be a bool")
        self._is_end = value

    @property
    def count(self) -> int:
        """Number of complete words stored in this node's subtree."""
        return self._count

    @count.setter
    def count(self, value: int) -> None:
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError("count must be an int")
        if value < 0:
            raise ValueError("count cannot be negative")
        self._count = value

    def __repr__(self) -> str:
        return f"TrieNode(children={list(self.children)}, is_end={self.is_end}, count={self.count})"

    def __str__(self) -> str:
        return repr(self)


class Trie:
    """A prefix tree over strings; a set of words, or a word -> value map."""

    def __init__(self, words: Iterable[str] | None = None) -> None:
        self._root = TrieNode()
        if words is not None:
            for word in words:
                self.insert(word)

    @staticmethod
    def _validate_key(key: object) -> None:
        """Reject anything that is not a non-empty string. Time: O(1)."""
        if not isinstance(key, str):
            raise TypeError("key must be a string")
        if key == "":
            raise ValueError("key must not be empty")

    def _find(self, text: str) -> TrieNode | None:
        """Walk the path spelling text from the root; return its node or None. Time: O(L)."""
        node = self._root
        for character in text:
            node = node.children.get(character)
            if node is None:
                return None
        return node

    @property
    def size(self) -> int:
        """Number of complete words stored. Time: O(1)."""
        return self._root.count

    def is_empty(self) -> bool:
        """True when no words are stored. Time: O(1)."""
        return self._root.count == 0

    def insert(self, word: str, value: Any = _UNSET) -> None:
        """Store word, optionally attaching value as its data. Time: O(L).

        Creates a node for any character whose key is missing, then marks the
        final node as a word end. Re-inserting an existing word does not
        double-count it; passing value updates the data, while a plain
        insert(word) leaves any existing data untouched.
        """
        self._validate_key(word)
        path: list[TrieNode] = [self._root]
        node = self._root
        for character in word:
            node = node.children.setdefault(character, TrieNode())
            path.append(node)

        is_new = not node.is_end
        if is_new:
            node.is_end = True
            for ancestor in path:
                ancestor.count += 1

        if value is not _UNSET:
            node.value = value
        elif is_new:
            node.value = None

    def __setitem__(self, word: str, value: Any) -> None:
        """t[word] = value — store word mapped to value. Time: O(L)."""
        self.insert(word, value)

    def search(self, word: str) -> bool:
        """True only if word was inserted as a complete word. Time: O(L)."""
        self._validate_key(word)
        node = self._find(word)
        return node is not None and node.is_end

    def get(self, word: str, default: Any = None) -> Any:
        """Data stored for word, or default when word is absent. Time: O(L)."""
        self._validate_key(word)
        node = self._find(word)
        if node is None or not node.is_end:
            return default
        return node.value

    def __getitem__(self, word: str) -> Any:
        """t[word] — data stored for word; raises KeyError when absent. Time: O(L)."""
        self._validate_key(word)
        node = self._find(word)
        if node is None or not node.is_end:
            raise KeyError(word)
        return node.value

    def starts_with(self, prefix: str) -> bool:
        """True if any stored word begins with prefix. Time: O(L)."""
        self._validate_key(prefix)
        return self._find(prefix) is not None

    def count_prefix(self, prefix: str) -> int:
        """How many stored words begin with prefix. Time: O(L)."""
        self._validate_key(prefix)
        node = self._find(prefix)
        return node.count if node is not None else 0

    def longest_prefix_of(self, text: str) -> str | None:
        """Longest stored word that is a prefix of text, or None. Time: O(len(text))."""
        self._validate_key(text)
        node = self._root
        best: str | None = None
        seen: list[str] = []
        for character in text:
            node = node.children.get(character)
            if node is None:
                break
            seen.append(character)
            if node.is_end:
                best = "".join(seen)
        return best

    def _walk(self, node: TrieNode, prefix: str) -> Iterator[tuple[str, TrieNode]]:
        """Yield (word, end_node) for every word in node's subtree, sorted. Time: O(chars)."""
        if node.is_end:
            yield prefix, node
        for character in sorted(node.children):
            yield from self._walk(node.children[character], prefix + character)

    def keys(self) -> Iterator[str]:
        """Every stored word, in sorted order. Time: O(chars)."""
        for word, _ in self._walk(self._root, ""):
            yield word

    def values(self) -> Iterator[Any]:
        """The data of every stored word, in sorted-key order. Time: O(chars)."""
        for _, node in self._walk(self._root, ""):
            yield node.value

    def items(self) -> Iterator[tuple[str, Any]]:
        """(word, data) for every stored word, in sorted-key order. Time: O(chars)."""
        for word, node in self._walk(self._root, ""):
            yield word, node.value

    def words_with_prefix(self, prefix: str) -> list[str]:
        """Every stored word under prefix, sorted — the autocomplete list. Time: O(chars)."""
        self._validate_key(prefix)
        start = self._find(prefix)
        if start is None:
            return []
        return [word for word, _ in self._walk(start, prefix)]

    def items_with_prefix(self, prefix: str) -> list[tuple[str, Any]]:
        """(word, data) for every stored word under prefix, sorted. Time: O(chars)."""
        self._validate_key(prefix)
        start = self._find(prefix)
        if start is None:
            return []
        return [(word, node.value) for word, node in self._walk(start, prefix)]

    def delete(self, word: str) -> bool:
        """Remove word and prune now-dead nodes. Time: O(L). False if absent.

        Clears the end flag and its value, decrements the cached count along the
        path, then removes every node that has become a dead end — no children
        and no word of its own — stopping at the first node that still carries a
        branch or another word. Deleting 'desktop' while 'desk' exists prunes
        't o p' but stops at 'k', keeping 'desk' alive.
        """
        self._validate_key(word)
        path: list[TrieNode] = [self._root]
        node = self._root
        for character in word:
            next_node = node.children.get(character)
            if next_node is None:
                return False
            path.append(next_node)
            node = next_node
        if not node.is_end:
            return False

        node.is_end = False
        node.value = None
        for ancestor in path:
            ancestor.count -= 1

        for i in range(len(word) - 1, -1, -1):
            child = path[i + 1]
            if not child.children and not child.is_end:
                del path[i].children[word[i]]
            else:
                break
        return True

    def clear(self) -> None:
        """Drop every word. Time: O(1)."""
        self._root = TrieNode()

    def pretty(self) -> str:
        """Indented text view of every node — '*' marks a word end. Time: O(nodes)."""
        lines = ["(root)"]

        def render(node: TrieNode, depth: int) -> None:
            for character in sorted(node.children):
                child = node.children[character]
                mark = " *" if child.is_end else ""
                shown_value = child.is_end and child.value is not None
                val = f" = {child.value!r}" if shown_value else ""
                lines.append("  " * depth + f"{character}{mark}{val}")
                render(child, depth + 1)

        render(self._root, 1)
        return "\n".join(lines)

    def __contains__(self, word: object) -> bool:
        """True if word is stored. Time: O(L)."""
        return isinstance(word, str) and word != "" and self.search(word)

    def __len__(self) -> int:
        """Number of complete words. Time: O(1)."""
        return self._root.count

    def __iter__(self) -> Iterator[str]:
        """Iterate stored words in sorted order. Time: O(chars)."""
        return self.keys()

    def __eq__(self, other: object) -> bool:
        """Two tries are equal when they store the same words and data."""
        if not isinstance(other, Trie):
            return NotImplemented
        return dict(self.items()) == dict(other.items())

    def __repr__(self) -> str:
        return f"Trie(size={self.size}, words={list(self.keys())})"

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

    def build(words: list[str]) -> Trie:
        trie = Trie()
        for word in words:
            trie.insert(word)
        return trie

    def test_insert_and_search():
        trie = build(["desktop", "stop", "desk"])
        assert len(trie) == 3
        assert trie.search("desktop") and trie.search("stop") and trie.search("desk")
        assert not trie.search("des")                    # path exists, not a word

    def test_membership_including_non_str():
        trie = build(["desk"])
        assert "desk" in trie
        assert "top" not in trie                         # shares prefixes, not suffixes
        assert 123 not in trie and "" not in trie           # bad_key membership never raises

    def test_starts_with():
        trie = build(["desktop", "stop", "desk"])
        assert trie.starts_with("des") and trie.starts_with("sto")
        assert not trie.starts_with("dex")

    def test_count_prefix():
        trie = build(["desktop", "stop", "desk"])
        assert trie.count_prefix("des") == 2
        assert trie.count_prefix("d") == 2
        assert trie.count_prefix("s") == 1
        assert trie.count_prefix("z") == 0

    def test_words_and_items_with_prefix():
        trie = build(["desktop", "stop", "desk"])
        assert trie.words_with_prefix("des") == ["desk", "desktop"]
        assert trie.words_with_prefix("s") == ["stop"]
        assert trie.words_with_prefix("xyz") == []
        trie["desk"] = "a table"
        assert ("desk", "a table") in trie.items_with_prefix("des")

    def test_value_map_get_and_setitem():
        trie = Trie()
        trie["desk"] = "a table"
        trie.insert("desktop", "a computer")
        assert trie["desk"] == "a table"
        assert trie.get("desktop") == "a computer"
        assert trie.get("missing") is None
        assert trie.get("missing", 0) == 0

    def test_getitem_missing_raises_keyerror():
        trie = build(["desk"])
        try:
            _ = trie["nope"]
            assert False, "expected KeyError"
        except KeyError:
            pass

    def test_reinsert_keeps_value_and_count():
        trie = Trie()
        trie["desk"] = "a table"
        trie.insert("desk")                              # plain re-insert
        assert trie["desk"] == "a table"                 # data preserved
        assert len(trie) == 1                            # not double-counted

    def test_longest_prefix_of():
        trie = build(["desk", "desktop", "stop"])
        assert trie.longest_prefix_of("desktopper") == "desktop"
        assert trie.longest_prefix_of("desks") == "desk"
        assert trie.longest_prefix_of("desalinate") is None
        assert trie.longest_prefix_of("stopping") == "stop"

    def test_delete_prunes_to_shared_branch():
        trie = build(["desk", "desktop"])
        assert trie.delete("desktop")
        assert not trie.search("desktop")
        assert trie.search("desk")                       # survives the prune
        assert trie.words_with_prefix("des") == ["desk"]

    def test_delete_internal_word_keeps_children():
        trie = build(["desk", "desktop"])
        assert trie.delete("desk")                       # 'desk' ends inside 'desktop'
        assert not trie.search("desk")
        assert trie.search("desktop")                    # children untouched
        assert len(trie) == 1

    def test_delete_leaf_and_absent():
        trie = build(["desktop", "stop", "desk"])
        assert trie.delete("stop") and len(trie) == 2
        assert not trie.delete("stop")                   # already gone
        assert not trie.delete("missing")                # never stored

    def test_iterate_sorted():
        assert list(build(["desktop", "stop", "desk"])) == ["desk", "desktop", "stop"]

    def test_equality():
        assert build(["desk", "stop"]) == build(["stop", "desk"])
        assert build(["desk"]) != build(["desktop"])

    def test_empty_trie_edges():
        trie = Trie()
        assert trie.is_empty() and len(trie) == 0
        assert list(trie) == [] and trie.words_with_prefix("a") == []
        assert not trie.search("a") and trie.count_prefix("a") == 0
        assert trie.longest_prefix_of("anything") is None

    def test_invalid_key_type_guard():
        trie = Trie()
        for bad_key, error in ((123, TypeError), (None, TypeError), ("", ValueError)):
            try:
                trie.insert(bad_key)
                assert False, f"expected {error.__name__}"
            except error:
                pass

    def test_pretty_smoke():
        trie = build(["desk", "desktop", "stop"])
        text = trie.pretty()
        assert "(root)" in text and "k *" in text

    def test_randomized_stress_vs_dict():
        import random

        random.seed(20260819)
        alphabet = "abcde"
        for _ in range(30):
            trie = Trie()
            reference: dict[str, int] = {}
            for _ in range(400):
                word = "".join(
                    random.choice(alphabet) for _ in range(random.randint(1, 6))
                )
                if random.random() < 0.62:
                    value = random.randint(0, 10_000)
                    trie.insert(word, value)
                    reference[word] = value
                else:
                    if word in reference:
                        assert trie.delete(word)
                        del reference[word]
                    else:
                        assert not trie.delete(word)
                assert len(trie) == len(reference)
            assert dict(trie.items()) == reference
            assert sorted(trie) == sorted(reference)
            for prefix in alphabet:
                expected = sum(1 for word in reference if word.startswith(prefix))
                assert trie.count_prefix(prefix) == expected

    print("Trie self-tests:")
    _check("insert -> search", test_insert_and_search)
    _check("__contains__ (incl. non-str, suffix)", test_membership_including_non_str)
    _check("starts_with", test_starts_with)
    _check("count_prefix", test_count_prefix)
    _check("words_with_prefix / items_with_prefix", test_words_and_items_with_prefix)
    _check("value map: get / __setitem__", test_value_map_get_and_setitem)
    _check("__getitem__ missing raises KeyError", test_getitem_missing_raises_keyerror)
    _check("re-insert keeps value and count", test_reinsert_keeps_value_and_count)
    _check("longest_prefix_of", test_longest_prefix_of)
    _check("delete prunes to shared branch", test_delete_prunes_to_shared_branch)
    _check("delete internal word keeps children", test_delete_internal_word_keeps_children)
    _check("delete leaf / absent no-op", test_delete_leaf_and_absent)
    _check("iterate in sorted order", test_iterate_sorted)
    _check("trie equality", test_equality)
    _check("empty-trie edge cases", test_empty_trie_edges)
    _check("invalid key type guard", test_invalid_key_type_guard)
    _check("pretty() text view", test_pretty_smoke)
    _check("randomized stress vs dict", test_randomized_stress_vs_dict)
