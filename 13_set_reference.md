# **Python Sets**

## **What is a Set?**

A Set is a data structure that represents a collection of unique and unordered elements. It is designed to store only distinct items, and mathematical operations like union, intersection, and difference can be performed on it.

- Duplicates are not allowed — only unique elements are stored.
- Insertion order is not preserved (elements may appear in any order).
- Indexing and slicing are not supported due to the unordered nature.
- Heterogeneous elements are allowed (numbers, strings, tuples, etc.).
- Sets are mutable — elements can be added or removed after creation.
- Elements must be hashable — lists and dicts cannot be stored in a set.
- Elements are enclosed in curly braces `{}` and separated by commas.
- Supports mathematical operations: union, intersection, difference, symmetric difference.

---

## **Why Elements Must Be Hashable**

Sets use a hash table internally to store and look up items in O(1) time. For this to work, each element must have a stable, fixed hash value — which means only immutable types (int, str, float, tuple, frozenset) can be set members. Mutable types like lists and dicts are unhashable and will raise a `TypeError`.

```python
# Hashable types — these work fine
valid = {10, "admin", 3.14, (1, 2)}

# Unhashable type — this fails
invalid = {[1, 2], [3, 4]}  # TypeError: unhashable type: 'list'
```

---

## **Creating Set Objects**

### **Using Curly Braces**

```python
roles = {"admin", "editor", "viewer"}
print(roles)        # {'viewer', 'admin', 'editor'}  ← order not guaranteed
print(type(roles))  # <class 'set'>
```

Duplicates are automatically removed:

```python
scores = {10, 20, 30, 10, 20, 40}
print(scores)  # {40, 10, 20, 30}
```

### **Using `set()` Function**

From a list (common way to deduplicate):

```python
records = [10, 20, 30, 40, 10, 20, 10]
s = set(records)
print(s)  # {40, 10, 20, 30}
```

From a range:

```python
s = set(range(5))
print(s)  # {0, 1, 2, 3, 4}
```

From a string (each character becomes an element):

```python
s = set("durga")
print(s)  # {'u', 'g', 'r', 'd', 'a'}
```

### **Creating an Empty Set — Critical Rule**

`{}` creates an empty **dictionary**, not an empty set. Always use `set()` for an empty set.

```python
# WRONG — creates an empty dict
s = {}
print(type(s))  # <class 'dict'>

# CORRECT — creates an empty set
s = set()
print(s)        # set()
print(type(s))  # <class 'set'>
```

---

## **Important Set Functions**

### **`add(x)`**

Adds a single element to the set. Takes exactly one argument. If the element is already present, the set is unchanged.

```python
tags = {"python", "ml"}
tags.add("nlp")
print(tags)  # {'python', 'ml', 'nlp'}

# Duplicate is silently ignored
tags.add("python")
print(tags)  # {'python', 'ml', 'nlp'}
```

### **`update(*iterables)`**

Adds multiple elements from one or more iterables to the set. Every argument must be iterable.

```python
s = {10, 20, 30}
s.update([40, 50], range(3))
print(s)  # {0, 1, 2, 10, 20, 30, 40, 50}
```

### **`add()` vs `update()` — Comparison**

| Feature | `add()` | `update()` |
|---|---|---|
| Purpose | Adds a single element. | Adds all elements from one or more iterables. |
| Arguments | Exactly one. | One or more iterables. |
| Argument type | Any hashable value. | Must be iterable (list, set, range, etc.). |
| Common error | Passing multiple args raises `TypeError`. | Passing a non-iterable (e.g., int) raises `TypeError`. |

```python
s = {10, 20}

# These raise TypeError:
s.add(30, 40)     # TypeError: add() takes exactly one argument (2 given)
s.update(50)      # TypeError: 'int' object is not iterable

# Correct usage:
s.add(30)
s.update([40, 50])
print(s)  # {10, 20, 30, 40, 50}
```

### **`copy()`**

Returns an independent shallow copy of the set.

```python
original = {10, 20, 30}
cloned = original.copy()
cloned.add(99)
print(original)  # {10, 20, 30}  ← unchanged
print(cloned)    # {10, 20, 30, 99}
```

### **`pop()`**

Removes and returns an arbitrary element from the set. Since sets are unordered, the element removed is not predictable. Raises `KeyError` if the set is empty.

```python
s = {10, 20, 30, 40}
removed = s.pop()
print(removed)  # some element — order is not guaranteed
print(s)        # remaining elements
```

### **`remove(x)`**

Removes the specified element from the set. Raises `KeyError` if the element is not present. Guard with `in` before calling.

```python
roles = {"admin", "editor", "viewer"}
roles.remove("editor")
print(roles)  # {'admin', 'viewer'}

# Guard before removing:
if "superuser" in roles:
    roles.remove("superuser")
```

### **`discard(x)`**

Removes the specified element from the set. Does nothing if the element is not present — no error raised. This is the safer choice when you are unsure whether the element exists.

```python
s = {10, 20, 30}
s.discard(20)  # removes 20
s.discard(99)  # element not in set — no error
print(s)       # {10, 30}
```

### **`remove()` vs `discard()` — Comparison**

| Feature | `remove(x)` | `discard(x)` |
|---|---|---|
| Removes element | Yes. | Yes. |
| Raises error if absent | `KeyError`. | No error — does nothing. |
| Safe to call without checking | No — guard with `in`. | Yes — always safe. |

### **`clear()`**

Removes all elements from the set, leaving it empty.

```python
session_tags = {"auth", "cache", "active"}
session_tags.clear()
print(session_tags)  # set()
```

---

## **Mathematical Operations on Sets**

These operations mirror standard set theory and are one of the biggest advantages of using sets in Python.

### **Union (`|` or `union()`)**

Returns all elements from both sets — no duplicates.

```python
batch_a = {10, 20, 30, 40}
batch_b = {30, 40, 50, 60}

print(batch_a | batch_b)            # {10, 20, 30, 40, 50, 60}
print(batch_a.union(batch_b))       # {10, 20, 30, 40, 50, 60}
```

### **Intersection (`&` or `intersection()`)**

Returns only elements common to both sets.

```python
print(batch_a & batch_b)                  # {40, 30}
print(batch_a.intersection(batch_b))      # {40, 30}
```

### **Difference (`-` or `difference()`)**

Returns elements in the first set that are not in the second.

```python
print(batch_a - batch_b)               # {10, 20}
print(batch_a.difference(batch_b))     # {10, 20}
```

Direction matters — `a - b` and `b - a` give different results:

```python
print(batch_b - batch_a)  # {50, 60}
```

### **Symmetric Difference (`^` or `symmetric_difference()`)**

Returns elements in either set but not in both — the opposite of intersection.

```python
print(batch_a ^ batch_b)                          # {10, 20, 50, 60}
print(batch_a.symmetric_difference(batch_b))      # {10, 20, 50, 60}
```

### **Subset (`<=` or `issubset()`)**

Returns `True` if all elements of the first set are in the second set.

```python
required = {"Maths", "Science"}
enrolled  = {"Maths", "Science", "English", "History"}

print(required <= enrolled)            # True
print(required.issubset(enrolled))     # True
```

### **Superset (`>=` or `issuperset()`)**

Returns `True` if the first set contains all elements of the second set.

```python
print(enrolled >= required)             # True
print(enrolled.issuperset(required))    # True
```

### **Disjoint Sets (`isdisjoint()`)**

Returns `True` if two sets have no elements in common.

```python
morning_batch = {"Rohit", "Tanvi"}
evening_batch = {"Arjun", "Drishya"}

print(morning_batch.isdisjoint(evening_batch))  # True
```

### **In-Place Update Versions**

These methods update the left set in place rather than returning a new set.

| Method | Equivalent To | In-Place Version |
|---|---|---|
| `union()` | `a \| b` | `a.update(b)` or `a \|= b` |
| `intersection()` | `a & b` | `a.intersection_update(b)` or `a &= b` |
| `difference()` | `a - b` | `a.difference_update(b)` or `a -= b` |
| `symmetric_difference()` | `a ^ b` | `a.symmetric_difference_update(b)` or `a ^= b` |

```python
s = {10, 20, 30, 40}
s &= {20, 30, 50}    # keep only common elements
print(s)             # {20, 30}
```

---

## **Membership Operators**

Sets provide O(1) average-time membership testing — far faster than lists (O(n)) for large collections.

```python
valid_statuses = {"active", "pending", "suspended"}

print("active" in valid_statuses)      # True
print("deleted" in valid_statuses)     # False
print("deleted" not in valid_statuses) # True
```

---

## **Iterating Over a Set**

Sets are iterable, but the order of iteration is not guaranteed.

```python
permissions = {"read", "write", "execute"}
for perm in permissions:
    print(perm)
```

If you need a consistent order, sort first:

```python
for perm in sorted(permissions):
    print(perm)
# execute, read, write
```

---

## **Sets and Indexing**

Sets do not support indexing or slicing. To access elements by position, convert to a list or tuple first.

```python
s = {10, 20, 30, 40}
print(s[0])    # TypeError: 'set' object is not subscriptable

# CORRECT — convert first
lst = list(s)
print(lst[0])  # some element (order depends on hashing)

# For a predictable order:
lst = sorted(s)
print(lst[0])  # 10
```

---

## **Set Comprehension**

Set comprehensions work like list comprehensions but produce a set (no duplicates, no guaranteed order).

```python
squares = {x * x for x in range(6)}
print(squares)  # {0, 1, 4, 9, 16, 25}

# With filter condition
even_squares = {x * x for x in range(10) if x % 2 == 0}
print(even_squares)  # {0, 4, 16, 36, 64}
```

Normalise and deduplicate strings in one shot:

```python
raw_tags = ["Python", "python", "ML", "ml", "NLP"]
unique_tags = {tag.lower() for tag in raw_tags}
print(unique_tags)  # {'python', 'ml', 'nlp'}
```

---

## **`frozenset` — Immutable Sets**

A `frozenset` is an immutable version of a set. Once created, elements cannot be added or removed. Because it is immutable, it is hashable and can be used as a dictionary key or as an element of another set.

```python
fs = frozenset(["admin", "editor", "viewer"])
print(fs)  # frozenset({'viewer', 'admin', 'editor'})

fs.add("superuser")     # AttributeError: 'frozenset' object has no attribute 'add'
fs.discard("editor")    # AttributeError
```

### **`frozenset` as a Dictionary Key**

```python
ALLOWED_METHODS = frozenset({"GET", "POST", "PUT", "DELETE"})

route_config = {
    ALLOWED_METHODS: "standard REST",
}

print("GET" in ALLOWED_METHODS)  # True
```

### **`frozenset` as an Element of a Set**

Regular sets cannot contain other sets (unhashable), but they can contain frozensets.

```python
# Set of frozensets — representing groups of students
groups = {
    frozenset({"Rohit", "Tanvi"}),
    frozenset({"Arjun", "Drishya"}),
}
print(len(groups))  # 2
```

### **`set` vs `frozenset` — Comparison**

| Feature | `set` | `frozenset` |
|---|---|---|
| Mutable | Yes. | No. |
| Hashable | No. | Yes. |
| Dictionary key | No. | Yes. |
| Set member | No. | Yes. |
| Supports `add`, `remove` | Yes. | No. |
| Supports set operations | Yes. | Yes (returns frozenset). |

---

## **Practical Programs Using Sets**

### **Eliminate Duplicates from a List**

```python
# Method 1 — fastest
records = [10, 20, 30, 10, 20, 40]
unique = list(set(records))
print(unique)  # order not preserved

# Method 2 — preserves order (use dict trick from the Lists notes)
from dict import fromkeys
ordered_unique = list(dict.fromkeys(records))
```

```python
# Method 2 — manual loop, preserves order
records = [10, 20, 30, 10, 20, 40]
seen = []
for x in records:
    if x not in seen:
        seen.append(x)
print(seen)  # [10, 20, 30, 40]
```

### **Find Vowels in a Word**

```python
vowels = {"a", "e", "i", "o", "u"}
word = input("Enter a word: ").lower()

found = set(word) & vowels
print(f"Unique vowels in '{word}' — {sorted(found)}")
```

### **Count Unique Elements in a Collection**

```python
data_stream = [1, 2, 3, 2, 1, 5, 6, 5]
unique_count = len(set(data_stream))
print(f"Unique elements — {unique_count}")  # 5
```

---

## **DSA and Algorithmic Use Cases**

### **Fast Membership Testing — O(1) vs O(n)**

Checking membership in a set is O(1) on average. In a list it is O(n). For large datasets this difference is significant.

```python
# Slow — linear scan for every lookup
valid_ids_list = list(range(1_000_000))
print(999_999 in valid_ids_list)   # O(n) — slow

# Fast — hash-based lookup
valid_ids_set = set(range(1_000_000))
print(999_999 in valid_ids_set)    # O(1) — fast
```

### **Finding Common Elements Across Multiple Lists**

```python
def common_across_all(groups: list[list]) -> set:
    result = set(groups[0])
    for group in groups[1:]:
        result.intersection_update(group)
    return result

data = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 6, 7]]
print(common_across_all(data))  # {3, 4}
```

### **Two-Sum — Finding Pairs with a Given Sum**

```python
def find_pairs(arr: list[int], target: int) -> set[tuple[int, int]]:
    seen = set()
    pairs = set()
    for num in arr:
        complement = target - num
        if complement in seen:
            pairs.add((min(num, complement), max(num, complement)))
        seen.add(num)
    return pairs

print(find_pairs([1, 5, 7, -1, 5], target=6))  # {(1, 5), (-1, 7)}
```

### **Graph Traversal — Tracking Visited Nodes**

```python
def dfs(graph: dict, start: str) -> set:
    visited = set()

    def explore(node: str) -> None:
        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                explore(neighbor)

    explore(start)
    return visited

graph = {"A": ["B", "C"], "B": ["D"], "C": [], "D": []}
print(dfs(graph, "A"))  # {'A', 'B', 'C', 'D'}
```

### **Cycle Detection in a Directed Graph (DFS + Recursion Stack)**

```python
def has_cycle(graph: dict) -> bool:
    visited = set()
    rec_stack = set()

    def dfs(node: str) -> bool:
        if node in rec_stack:
            return True
        if node in visited:
            return False
        visited.add(node)
        rec_stack.add(node)
        for neighbor in graph.get(node, []):
            if dfs(neighbor):
                return True
        rec_stack.remove(node)
        return False

    return any(dfs(node) for node in graph if node not in visited)

graph = {0: [1], 1: [2], 2: [0]}
print(has_cycle(graph))  # True
```

### **Power Set — All Subsets of a Set**

```python
def power_set(s: set) -> set:
    subsets = {frozenset()}
    for elem in s:
        subsets = subsets | {subset | frozenset({elem}) for subset in subsets}
    return subsets

result = power_set({1, 2, 3})
print(len(result))  # 8 (2^3 subsets)
```

### **Disjoint Set / Union-Find**

Used in graph algorithms like Kruskal's MST and connected components detection.

```python
class DisjointSet:
    def __init__(self, vertices: list) -> None:
        self.parent = {v: v for v in vertices}
        self.rank   = {v: 0 for v in vertices}

    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])  # path compression
        return self.parent[item]

    def union(self, x, y) -> None:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1

ds = DisjointSet([1, 2, 3, 4])
ds.union(1, 2)
ds.union(3, 4)
print(ds.find(1) == ds.find(2))  # True  ← same component
print(ds.find(1) == ds.find(3))  # False ← different components
```

---

## **Common Mistakes**

### **1. Using `{}` to create an empty set**

```python
# WRONG — creates an empty dictionary
s = {}
print(type(s))  # <class 'dict'>

# CORRECT
s = set()
print(type(s))  # <class 'set'>
```

### **2. Trying to add an unhashable type to a set**

```python
# WRONG — lists are unhashable
s = {[1, 2], [3, 4]}  # TypeError: unhashable type: 'list'

# CORRECT — convert inner lists to tuples
s = {(1, 2), (3, 4)}
print(s)  # {(1, 2), (3, 4)}
```

### **3. Calling `remove()` without checking membership**

```python
s = {"admin", "editor"}

# WRONG — raises KeyError if element is absent
s.remove("superuser")

# CORRECT — use discard() or guard with `in`
s.discard("superuser")      # safe, no error
if "superuser" in s:
    s.remove("superuser")   # also fine
```

### **4. Passing multiple arguments to `add()`**

```python
s = {10, 20}
s.add(30, 40)   # TypeError: add() takes exactly one argument (2 given)

# CORRECT
s.add(30)
s.update([40])
```

### **5. Passing a non-iterable to `update()`**

```python
s = {10, 20}
s.update(30)   # TypeError: 'int' object is not iterable

# CORRECT
s.update([30])    # list
s.update({30})    # set
s.update((30,))   # tuple
```

### **6. Expecting a consistent order from a set**

```python
# WRONG assumption
s = {3, 1, 2}
print(list(s)[0])  # may not be 1 — order is not guaranteed

# CORRECT — sort explicitly when order matters
print(sorted(s)[0])  # 1
```

### **7. Trying to use a list as a set element or dictionary key**

```python
# WRONG
d = {[1, 2]: "pair"}   # TypeError: unhashable type: 'list'

# CORRECT — use a tuple
d = {(1, 2): "pair"}
print(d[(1, 2)])  # pair
```

---

## **Production Patterns**

### **Permission and Role Validation in an API**

Sets are the natural fit for permission checking — O(1) lookup and built-in operations for comparing permission sets.

```python
ADMIN_PERMISSIONS: frozenset[str] = frozenset({"read", "write", "delete", "manage"})
EDITOR_PERMISSIONS: frozenset[str] = frozenset({"read", "write"})

def can_perform(user_permissions: set[str], required: set[str]) -> bool:
    return required.issubset(user_permissions)

user_perms = {"read", "write"}
print(can_perform(user_perms, {"read"}))          # True
print(can_perform(user_perms, {"delete"}))        # False
```

### **Deduplication in a Data Pipeline**

```python
def deduplicate_records(records: list[dict], key: str) -> list[dict]:
    seen_ids: set = set()
    unique = []
    for record in records:
        rid = record[key]
        if rid not in seen_ids:
            seen_ids.add(rid)
            unique.append(record)
    return unique

students = [
    {"id": 1, "name": "Rohit"},
    {"id": 2, "name": "Tanvi"},
    {"id": 1, "name": "Rohit"},   # duplicate
]
print(deduplicate_records(students, key="id"))
```

### **Tag Normalization for a Content System**

```python
def normalize_tags(raw_tags: list[str]) -> set[str]:
    return {tag.strip().lower() for tag in raw_tags if tag.strip()}

tags = ["  Python ", "python", "ML", "ml ", "NLP"]
print(normalize_tags(tags))  # {'python', 'ml', 'nlp'}
```

### **Feature Flag Intersection in a Config System**

```python
ENABLED_FEATURES: frozenset[str] = frozenset({"dark_mode", "beta_search", "export_pdf"})

def get_active_features(requested: set[str]) -> set[str]:
    return requested & ENABLED_FEATURES

user_requests = {"dark_mode", "ai_chat", "export_pdf"}
print(get_active_features(user_requests))  # {'dark_mode', 'export_pdf'}
```

### **Collection Type Comparison**

| Type | Ordered | Duplicates | Mutable | Hashable | Indexing | Best Use Case |
|---|---|---|---|---|---|---|
| `list` | Yes | Yes | Yes | No | Yes | General ordered sequence. |
| `tuple` | Yes | Yes | No | Yes | Yes | Immutable records, dict keys. |
| `set` | No | No | Yes | No | No | Unique items, membership testing, set math. |
| `frozenset` | No | No | No | Yes | No | Immutable unique items, dict keys, set elements. |
| `dict` | Yes (3.7+) | Keys: No | Yes | No | By key | Key-value mapping. |

---

## **Modern Python Patterns**

### **Type Hints with Built-in `set` and `frozenset` (3.9+)**

Before Python 3.9, you had to import `Set` and `FrozenSet` from `typing`.

```python
# Old style (pre-3.9)
from typing import Set, FrozenSet
def get_unique(items: list) -> Set[int]:
    return set(items)

# Modern style (3.9+)
def get_unique(items: list) -> set[int]:
    return set(items)

ALLOWED: frozenset[str] = frozenset({"GET", "POST"})
```

### **`set` with `|` Union Type Syntax (3.10+)**

The `|` operator now works for both set union and type unions in the same codebase — be careful not to confuse them.

```python
# Set union
a = {1, 2, 3}
b = {3, 4, 5}
print(a | b)  # {1, 2, 3, 4, 5}

# Type union (in a function signature)
def process(value: int | str) -> set[int | str]:
    return {value}
```

### **`match-case` with Set-Like Membership (3.10+)**

`match-case` doesn't directly pattern-match sets, but you can combine it with set membership for clean dispatch:

```python
ADMIN_ROLES = frozenset({"admin", "superuser"})
EDITOR_ROLES = frozenset({"editor", "contributor"})

def describe_access(role: str) -> str:
    match role:
        case r if r in ADMIN_ROLES:
            return "full access"
        case r if r in EDITOR_ROLES:
            return "write access"
        case _:
            return "read-only"

print(describe_access("admin"))       # full access
print(describe_access("contributor")) # write access
print(describe_access("viewer"))      # read-only
```

### **Walrus Operator `:=` in Set Filtering (3.8+)**

```python
records = [{"id": 1, "score": 88}, {"id": 2, "score": 45}, {"id": 3, "score": 72}]
passed_ids = {r["id"] for r in records if (s := r["score"]) >= 60}
print(passed_ids)  # {1, 3}
```

### **Older vs Modern Comparison**

| Pattern | Old Style | Modern Style (3.9–3.14) |
|---|---|---|
| Type hint | `Set[int]` from `typing` | `set[int]` built-in |
| Frozenset hint | `FrozenSet[str]` | `frozenset[str]` |
| Empty set mistake | Common — `s = {}` | Use `s = set()` always |
| Membership guard | `if x in list: ...` O(n) | Convert to `set` first for O(1) |
| Dedup a list | Manual loop | `set(lst)` or `dict.fromkeys(lst)` |
| Union operator | `set1.union(set2)` | `set1 \| set2` (same, but more readable) |
| In-place intersection | `set1.intersection_update(set2)` | `set1 &= set2` |

---

## **Quick Reference**

| Operation | Syntax | Notes |
|---|---|---|
| Create with elements | `s = {1, 2, 3}` | Duplicates auto-removed. |
| Create empty set | `s = set()` | Never `s = {}` — that's a dict. |
| From list | `set([1, 2, 2, 3])` | Deduplicates automatically. |
| Add one element | `s.add(x)` | One arg only; silent if duplicate. |
| Add from iterable | `s.update(iter)` | All args must be iterable. |
| Remove (strict) | `s.remove(x)` | `KeyError` if absent — guard with `in`. |
| Remove (safe) | `s.discard(x)` | No error if absent. |
| Remove arbitrary | `s.pop()` | Random element; `KeyError` if empty. |
| Clear all | `s.clear()` | Empties the set. |
| Copy | `s.copy()` | Independent shallow copy. |
| Length | `len(s)` | — |
| Membership | `x in s` | O(1) average. |
| Union | `a \| b` or `a.union(b)` | All unique elements. |
| Intersection | `a & b` or `a.intersection(b)` | Common elements. |
| Difference | `a - b` or `a.difference(b)` | In `a` but not `b`. |
| Symmetric diff | `a ^ b` or `a.symmetric_difference(b)` | In either, not both. |
| Subset check | `a <= b` or `a.issubset(b)` | Is `a` contained in `b`? |
| Superset check | `a >= b` or `a.issuperset(b)` | Does `a` contain all of `b`? |
| Disjoint check | `a.isdisjoint(b)` | No common elements. |
| In-place union | `a \|= b` or `a.update(b)` | Updates `a` in place. |
| In-place intersect | `a &= b` or `a.intersection_update(b)` | Updates `a` in place. |
| In-place diff | `a -= b` or `a.difference_update(b)` | Updates `a` in place. |
| Set comprehension | `{expr for x in iter if cond}` | No duplicates in result. |
| Iterate (sorted) | `for x in sorted(s):` | Consistent order. |
| Convert to list | `list(s)` | Order not guaranteed. |
| Convert to tuple | `tuple(s)` | Order not guaranteed. |
| Frozenset | `frozenset(iter)` | Immutable, hashable, usable as dict key. |
| Type hint (3.9+) | `set[int]`, `frozenset[str]` | No import needed. |
| Union of many sets | `s1.union(s2, s3, ...)` | Accepts multiple args. |