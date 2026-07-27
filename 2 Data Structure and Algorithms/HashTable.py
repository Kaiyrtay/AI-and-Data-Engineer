"""hash_table.py — four collision-handling techniques behind one interface.

Implements the hashing techniques from Noor Fatima's "Hashing in DSA":
separate chaining (open hashing) and open addressing (closed hashing) with
linear probing, quadratic probing, and double hashing.

The abstract base `HashTable` owns everything the techniques share — load
factor, resize policy, the public `insert`/`search`/`delete` API, and the
dunders. Each subclass supplies only what actually differs between the
techniques: how a key is placed, found, and removed. That is a real is-a
relationship (a linear-probing table *is* a hash table), so inheritance is
the right tool here rather than composition.

Design invariant: `self._count` always equals the number of live keys, and
`0 <= load_factor < MAX_LOAD_FACTOR` immediately after any public call.

Run `python hash_table.py` to execute the self-tests at the bottom.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Hashable, Iterator

INITIAL_CAPACITY = 7          # prime start — keeps probe strides coprime to size
MAX_LOAD_FACTOR = 0.75        # resize before the table gets slow
GROWTH_FACTOR = 2             # double, then round up to the next prime
DEFAULT_STEP_PRIME = 5        # secondary-hash modulus for double hashing


class HashTableError(Exception):
    """Base class for every hash-table error — lets callers catch precisely."""


class KeyNotFoundError(HashTableError):
    """Raised when deleting or locating a key that is not present."""


class TableFullError(HashTableError):
    """Raised when a probe sequence finds no free slot for a key."""


def _next_prime(lower_bound: int) -> int:
    """Smallest prime >= lower_bound. Time: O(g * sqrt(n)) over g candidates."""
    candidate = max(lower_bound, 2)
    while not _is_prime(candidate):
        candidate += 1
    return candidate


def _is_prime(number: int) -> bool:
    """Trial division up to sqrt(number). Time: O(sqrt(n)). Space: O(1)."""
    if number < 2:
        return False
    divisor = 2
    while divisor * divisor <= number:      # only test up to the square root
        if number % divisor == 0:
            return False
        divisor += 1
    return True


class HashTable(ABC):
    """Abstract hash set: shared API + resize policy; subclasses do placement."""

    def __init__(self, capacity: int = INITIAL_CAPACITY) -> None:
        if capacity < 1:                    # validate at construction — fail fast
            raise ValueError("capacity must be at least 1")
        self._capacity = capacity
        self._count = 0                     # private state (§3)
        self._allocate(capacity)

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def count(self) -> int:
        return self._count

    @property
    def load_factor(self) -> float:
        """Live keys / capacity. Time: O(1)."""
        return self.count / self.capacity

    def _home_index(self, key: Hashable) -> int:
        """Bucket a key hashes to before any probing. Time: O(1)."""
        return hash(key) % self.capacity

    def insert(self, key: Hashable) -> None:
        """Add a key (idempotent). Time: O(1) amortized; O(n) on a resize."""
        if self.search(key):                # duplicates are a no-op, not a bug
            return
        if self.load_factor >= MAX_LOAD_FACTOR:
            self._resize(_next_prime(self.capacity * GROWTH_FACTOR))
        try:
            self._store(key)
        except TableFullError:              # probing gave up — grow and retry
            self._resize(_next_prime(self.capacity * GROWTH_FACTOR))
            self._store(key)
        self._count += 1

    def delete(self, key: Hashable) -> None:
        """Remove a key. Time: O(1) average. Raises KeyNotFoundError if absent."""
        self._discard(key)                  # raises before we touch the count
        self._count -= 1

    def _resize(self, new_capacity: int) -> None:
        """Rehash every live key into a bigger table. Time: O(n)."""
        live_keys = list(self._live_keys())
        while True:
            self._capacity = new_capacity
            self._count = 0
            self._allocate(new_capacity)
            try:
                for key in live_keys:
                    self._store(key)
                    self._count += 1
            except TableFullError:          # rare: grow again and re-rehash
                new_capacity = _next_prime(new_capacity * GROWTH_FACTOR)
                continue
            return

    @abstractmethod
    def _allocate(self, capacity: int) -> None:
        """Allocate the underlying storage for a table of the given capacity."""
        raise NotImplementedError

    @abstractmethod
    def _store(self, key: Hashable) -> None:
        """Store a key in the table, assuming it is not already present."""
        raise NotImplementedError

    @abstractmethod
    def _discard(self, key: Hashable) -> None:
        """Remove a key from the table, assuming it is present."""
        raise NotImplementedError

    @abstractmethod
    def _live_keys(self) -> Iterator[Hashable]:
        """Yield all the live keys in the table."""
        raise NotImplementedError

    @abstractmethod
    def search(self, key: Hashable) -> bool:
        """Return True if the key is present in the table, False otherwise."""
        raise NotImplementedError

    def __len__(self) -> int:
        return self.count

    def __contains__(self, key: Hashable) -> bool:
        return self.search(key)

    def __iter__(self) -> Iterator[Hashable]:
        yield from self._live_keys()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HashTable):
            return NotImplemented            # let Python try the other side
        return self.capacity == other.capacity and set(self) == set(other)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(capacity={self.capacity}, count={self.count})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__} with {self.count} keys and capacity {self.capacity}"


class SeparateChainingHashTable(HashTable):
    """Open hashing: each bucket is a list; collisions chain. Time: O(1) avg."""

    _buckets: list[list[Hashable]]

    def _allocate(self, capacity: int) -> None:
        self._buckets = [[] for _ in range(capacity)]

    def _store(self, key: Hashable) -> None:
        """Append to the home bucket. Time: O(1)."""
        self._buckets[self._home_index(key)].append(key)

    def _discard(self, key: Hashable) -> None:
        """Remove from the home bucket. Time: O(1) avg. Raises if absent."""
        chain = self._buckets[self._home_index(key)]
        if key not in chain:
            raise KeyNotFoundError(f"Key {key} not found for deletion")
        chain.remove(key)

    def search(self, key: Hashable) -> bool:
        """Time: O(1) average, O(n) if everything collides into one bucket."""
        return key in self._buckets[self._home_index(key)]

    def _live_keys(self) -> Iterator[Hashable]:
        for chain in self._buckets:
            yield from chain                # each chain is a list — flatten it


class _Empty:
    """Sentinel for a slot that has never held a key."""


class _Deleted:
    """Sentinel (tombstone) for a slot whose key was removed.

    Probing must treat this as occupied when searching (so it does not stop
    early) but as free when inserting (so the slot can be reused).
    """


_EMPTY: _Empty = _Empty()
_DELETED: _Deleted = _Deleted()


class OpenAddressingHashTable(HashTable):
    """Closed hashing: keys live in the slot array itself; collisions probe."""

    _slots: list[Hashable | _Empty | _Deleted]

    def _allocate(self, capacity: int) -> None:
        self._slots = [_EMPTY] * capacity

    @abstractmethod
    def _probe_sequence(self, home: int, attempt: int, key: Hashable) -> int:
        """Index to probe on the given attempt (0-based). Time: O(1)."""
        raise NotImplementedError

    def _store(self, key: Hashable) -> None:
        """Place a key at the first free slot on its probe path. Time: O(1) avg."""
        home = self._home_index(key)
        first_free: int | None = None       # remember earliest reusable tombstone
        for attempt in range(self.capacity):
            index = self._probe_sequence(home, attempt, key)
            slot = self._slots[index]
            if slot is _EMPTY:
                if first_free is None:      # no earlier tombstone — use this slot
                    first_free = index
                self._slots[first_free] = key
                return
            if slot is _DELETED and first_free is None:
                first_free = index          # reuse the tombstone, shortens probes
        if first_free is None:              # probe path exhausted, no free slot
            raise TableFullError("No free slot found for key insertion")
        self._slots[first_free] = key

    def _discard(self, key: Hashable) -> None:
        """Tombstone the key's slot. Time: O(1) avg. Raises if absent."""
        home = self._home_index(key)
        for attempt in range(self.capacity):
            index = self._probe_sequence(home, attempt, key)
            slot = self._slots[index]
            if slot is _EMPTY:              # empty means the key was never past here
                raise KeyNotFoundError(f"Key {key} not found for deletion")
            if slot == key:
                # tombstone, not empty (§ sentinels)
                self._slots[index] = _DELETED
                return
        raise KeyNotFoundError(f"Key {key} not found for deletion")

    def search(self, key: Hashable) -> bool:
        """Walk the probe path until the key or a true gap. Time: O(1) avg."""
        home = self._home_index(key)
        for attempt in range(self.capacity):
            index = self._probe_sequence(home, attempt, key)
            slot = self._slots[index]
            if slot is _EMPTY:             # a real gap ends the search; tombstones don't
                return False
            if slot == key:
                return True
        return False

    def _live_keys(self) -> Iterator[Hashable]:
        for slot in self._slots:
            if slot is not _EMPTY and slot is not _DELETED:
                yield slot                # FIX: yield the key, not `yield from` it


class LinearProbing(OpenAddressingHashTable):
    """Probe home, home+1, home+2, ... Simple; prone to primary clustering."""

    def _probe_sequence(self, home: int, attempt: int, key: Hashable) -> int:
        return (home + attempt) % self.capacity


class QuadraticProbing(OpenAddressingHashTable):
    """Probe home + 1, +4, +9, ... Breaks up clustering; may skip free slots."""

    def _probe_sequence(self, home: int, attempt: int, key: Hashable) -> int:
        return (home + attempt ** 2) % self.capacity


class DoubleHashing(OpenAddressingHashTable):
    """Stride set by a second hash, so colliding keys diverge onto different paths."""

    def __init__(self, capacity: int = INITIAL_CAPACITY,
                 step_prime: int = DEFAULT_STEP_PRIME) -> None:
        if step_prime < 2:                  # validate — a 0/1 stride never advances
            raise ValueError("step_prime must be at least 2")
        self._step_prime = step_prime
        super().__init__(capacity)

    @property
    def step_prime(self) -> int:
        return self._step_prime

    def _secondary_step(self, key: Hashable) -> int:
        """Stride in 1..step_prime — never 0, so the probe always moves. Time: O(1)."""
        return self.step_prime - (hash(key) % self.step_prime)

    def _probe_sequence(self, home: int, attempt: int, key: Hashable) -> int:
        # FIX: was named `_probe`, so it never satisfied the ABC's `_probe_sequence`
        # and DoubleHashing stayed abstract (couldn't be instantiated).
        return (home + attempt * self._secondary_step(key)) % self.capacity


if __name__ == "__main__":
    # Self-tests (Handbook §9 / §17): for every technique cover the empty, one,
    # and many cases, plus invalid input, a boundary, and a deliberate failure
    # whose exception we predict. "Ran it once" is one data point — this is proof.

    TABLES = {
        "SeparateChaining": SeparateChainingHashTable,
        "LinearProbing": LinearProbing,
        "QuadraticProbing": QuadraticProbing,
        "DoubleHashing": DoubleHashing,
    }

    def test_empty(make) -> None:
        # Edge: a fresh table holds nothing and finds nothing.
        table = make()
        assert len(table) == 0
        assert 42 not in table
        assert list(table) == []

    def test_single_key(make) -> None:
        # Happy path: insert one, find it, delete it, it's gone.
        table = make()
        table.insert("solo")
        assert "solo" in table and len(table) == 1
        table.delete("solo")
        assert "solo" not in table and len(table) == 0

    def test_many_forces_resize(make) -> None:
        # Many: insert well past the load factor to force at least one resize,
        # then every key must still be present and round-trip through iteration.
        table = make()
        keys = list(range(50))
        for key in keys:
            table.insert(key)
        assert len(table) == 50
        assert all(key in table for key in keys)
        # _live_keys must be faithful
        assert set(table) == set(keys)
        assert table.load_factor < MAX_LOAD_FACTOR  # invariant held after growth

    def test_duplicates_ignored(make) -> None:
        # Boundary: re-inserting a key is a no-op, never a double count.
        table = make()
        table.insert(7)
        table.insert(7)
        assert len(table) == 1

    def test_delete_and_reinsert(make) -> None:
        # Tombstone handling: a deleted key is gone but the slot is reusable,
        # and a later key on the same path is still found past the tombstone.
        table = make()
        for key in range(10):
            table.insert(key)
        table.delete(3)
        assert 3 not in table and len(table) == 9
        table.insert(3)
        assert 3 in table and len(table) == 10

    def test_delete_missing_raises(make) -> None:
        # Deliberate failure: deleting an absent key raises KeyNotFoundError.
        table = make()
        table.insert(1)
        try:
            table.delete(999)
        except KeyNotFoundError:
            pass
        else:
            raise AssertionError(
                "expected KeyNotFoundError deleting a missing key")

    def test_equality(make) -> None:
        # Dunder: two tables built identically compare equal.
        left, right = make(), make()
        for key in range(5):
            left.insert(key)
            right.insert(key)
        assert left == right

    PER_TABLE_TESTS = [
        test_empty, test_single_key, test_many_forces_resize,
        test_duplicates_ignored, test_delete_and_reinsert,
        test_delete_missing_raises, test_equality,
    ]

    def test_invalid_construction() -> None:
        # Invalid input: constructors validate and fail loud, not silently.
        try:
            LinearProbing(0)
        except ValueError:
            pass
        else:
            raise AssertionError("capacity < 1 must raise ValueError")
        try:
            DoubleHashing(step_prime=1)
        except ValueError:
            pass
        else:
            raise AssertionError("step_prime < 2 must raise ValueError")

    passed = 0
    for name, factory in TABLES.items():
        for test in PER_TABLE_TESTS:
            test(factory)
            passed += 1
        print(f"  {name:18s} {len(PER_TABLE_TESTS)} tests passed")

    test_invalid_construction()
    passed += 1
    print(f"  {'construction':18s} 1 test passed")
    print(f"All {passed} tests passed.")
