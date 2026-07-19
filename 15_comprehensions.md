# **Python Comprehensions**

Notes covering list, set, dict, and generator comprehensions, plus the chained and nested forms that combine them.

Comprehensions are Python's most-used syntax sugar. The list comprehension, dict comprehension, set comprehension, and generator expression are the same idea applied to four container types. The "chained" form (multiple `for` clauses) and the "nested" form (a comprehension inside another comprehension) are two different ways to build more complex results. Once the full mental map is in place, a four-line `for` loop turns into a one-liner that says exactly what is meant.

## **The One-Page Mental Map**

| Construct | Syntax | Output Type | Lazy? |
| --- | --- | --- | --- |
| List comprehension | `[expr for x in iter]` | `list` | no |
| Set comprehension | `{expr for x in iter}` | `set` | no |
| Dict comprehension | `{key: val for x in iter}` | `dict` | no |
| Generator expression | `(expr for x in iter)` | generator (lazy iterator) | yes |
| Chained comprehension | `[expr for a in A for b in B]` | one flat container | depends on the wrapping |
| Nested comprehension | `[[expr for y in Y] for x in X]` | nested containers | no |
| Filtered comprehension | `[expr for x in iter if cond]` | filtered container | depends |
| Walrus-in-comprehension | `[(y, x) for x in xs if (y := f(x)) > 0]` | filtered, with shared state | depends |

The expression on the left of `for` is the output. The `for` clauses are the iteration. The `if` clauses are the filter. Everything else is a combination of these four pieces.

## **List Comprehensions**

A list comprehension is a one-line way to build a new list by applying an expression to every element of an iterable.

```python
# Traditional approach
squares = []
for n in range(1, 6):
    squares.append(n ** 2)

# List comprehension -- same result, one line
squares = [n ** 2 for n in range(1, 6)]
print(squares)        # [1, 4, 9, 16, 25]
```

The list comprehension is at least as fast as the explicit loop, often a touch faster since the append happens in C, and is shorter — the idiomatic way to build a list from a `for` loop.

**The anatomy of a comprehension**

```
[ EXPR  for VAR in ITER  if COND ]
```

- `EXPR` is the output — any expression, and it can use `VAR`.
- `for VAR in ITER` is the iteration — required, and repeatable for chaining.
- `if COND` is the filter — optional, and repeatable — keeping only items for which `COND` is truthy.

**Basic transforms**

```python
[x * x for x in range(1, 6)]                          # [1, 4, 9, 16, 25]
[w.upper() for w in ["python", "java", "rust"]]         # ['PYTHON', 'JAVA', 'RUST']
[len(s) for s in ["hi", "hello", ""]]                    # [2, 5, 0]
[f"${p:.2f}" for p in [9.5, 19.99, 100]]                 # ['$9.50', '$19.99', '$100.00']
[s.strip().lower() for s in ["  Karan  ", " Lara "]]    # ['Karan', 'Lara']
[len(w) for w in "the quick brown fox".split()]          # [3, 5, 5, 3]

# Extra: turn a list of titles into URL-friendly slugs
titles = ["Hello World", "Python Comprehensions!", "Data  Science"]
[t.strip().lower().replace(" ", "-") for t in titles]
# ['hello-world', 'python-comprehensions!', 'data--science']
```

**Filtering with the `if` clause**

```python
[x for x in range(10) if x % 2 == 0]                    # [0, 2, 4, 6, 8]
[s for s in ["", "hi", "", "ok"] if s]                    # ['hi', 'ok']
[w for w in "the quick brown fox jumps".split() if len(w) > 3]
# ['quick', 'brown', 'jumps']

# Multiple filters -- multiples of 6
[x for x in range(50) if x % 2 == 0 if x % 3 == 0]
# [0, 6, 12, 18, 24, 30, 36, 42, 48]

# Filter with a custom function
adults = [u for u in users if u["age"] >= 18]

# Extra: fast membership filter using a set instead of a list
banned_ids = {4, 9, 15}
active_ids = [uid for uid in range(1, 20) if uid not in banned_ids]
```

**Conditional expression (ternary) in the output**

The output expression can be a ternary — `X if cond else Y` — which is not the same as the `if` filter. A filter drops items; a ternary transforms them.

```python
[x if x >= 0 else 0 for x in [-1, 2, -3, 4]]             # [0, 2, 0, 4]
["even" if x % 2 == 0 else "odd" for x in range(6)]
# ['even', 'odd', 'even', 'odd', 'even', 'odd']
["pass" if s >= 0.5 else "fail" for s in [0.91, 0.45, 0.78]]
# ['pass', 'fail', 'pass']

# Compress / mask using a parallel iterable
nums = [1, 2, 3, 4, 5]
mask = [True, False, True, False, True]
[n if m else None for n, m in zip(nums, mask)]           # [1, None, 3, None, 5]

# Filter and transform in the same comprehension
["pass" if s >= 0.5 else "fail" for s in [0.91, 0.45, 0.78] if s > 0]
```

**Unpacking and tuples**

```python
pairs = [("Karan", 36), ("Lara", 22), ("Drishya", 41)]
[n for n, _ in pairs]                                     # ['Karan', 'Lara', 'Drishya']

# Transpose a matrix using zip
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed = [list(col) for col in zip(*matrix)]
# [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

# Swap keys and values
d = {"a": 1, "b": 2, "c": 3}
swap = [(v, k) for k, v in d.items()]                     # [(1, 'a'), (2, 'b'), (3, 'c')]

# Flatten one level of a list of pairs
pairs = [[1, 2], [3, 4], [5, 6]]
flat = [n for p in pairs for n in p]                       # [1, 2, 3, 4, 5, 6]

# Extra: pull a single field out of a list of dicts, paired with its index
users = [{"name": "Karan"}, {"name": "Lara"}, {"name": "Drishya"}]
[(i, u["name"]) for i, u in enumerate(users)]
# [(0, 'Karan'), (1, 'Lara'), (2, 'Drishya')]
```

**With function calls**

```python
[c.upper() for c in "Karan"]                              # ['A', 'A', 'R', 'A', 'V']

from math import sqrt
[sqrt(x) for x in [1, 4, 9, 16]]                           # [1.0, 2.0, 3.0, 4.0]

[line.split(",") for line in ["a,1,2", "b,3,4", "c,5,6"]]
# [['a', '1', '2'], ['b', '3', '4'], ['c', '5', '6']]

import re
[re.findall(r"\d+", s) for s in ["abc 12 def", "no digits"]]
# [['12'], []]

from pathlib import Path
[p.stat().st_size for p in Path(".").glob("*.py")]         # a list of byte sizes
```

**With the walrus operator (3.8+)**

The walrus operator `:=` binds a name inside the comprehension — useful when a value needs to be computed once and used in both the filter and the output.

```python
# Without walrus -- recomputes x * x inside the condition and the output
[x * x for x in range(10) if x * x > 50]

# With walrus -- compute once, reuse
[x * x for x in range(10) if (sq := x * x) > 50]           # [64, 81]

# Avoid a repeated call to an expensive function
[y for x in data if (y := f(x)) > 0]                        # f(x) runs once per element
```

The walrus can also leak the variable into the enclosing scope.

```python
[square for n in [3, 4, 5] if (square := n * n) > 10]
print(square)        # 25 -- the name is now in the outer scope
```

A regular `for` loop is the fix if that leak is not wanted.

**Modern library patterns**

```python
# Pandas -- column names matching a pattern
import pandas as pd
df = pd.DataFrame({"user_id": [1, 2], "user_name": ["a", "b"], "score": [0.9, 0.4]})
[c for c in df.columns if c.startswith("user_")]           # ['user_id', 'user_name']

# pathlib -- all .py files, eagerly materialized
from pathlib import Path
[p for p in Path(".").rglob("*.py") if p.is_file()]

# FastAPI -- list of HTTP method handler objects
methods = ["get", "post", "put", "delete"]
handlers = [getattr(app, m) for m in methods]               # [app.get, app.post, ...]

# Pydantic -- list of required field names
required = [name for name, field in MyModel.model_fields.items() if field.is_required()]

# asyncio -- list of scheduled tasks
tasks = [asyncio.create_task(coro) for coro in coros]
```

## **Set Comprehensions**

A set comprehension builds a set — an unordered collection of unique elements. The syntax matches a list comprehension, but with curly braces.

```python
{len(w) for w in "the quick brown fox".split()}             # {3, 5, 4}
{w[0] for w in ["apple", "banana", "apricot", "blueberry"]}  # {'a', 'b'}
{x for x in range(20) if x % 2 == 0}                          # {0, 2, ..., 18}
```

**Dedupe and membership**

```python
# Dedupe a list, order not preserved
names = ["Karan", "Lara", "Karan", "Drishya", "Lara", "Tanvi"]
unique = {n for n in names}                                  # {'Karan', 'Lara', 'Drishya', 'Tanvi'}

# Unique lowercase tokens from messy input
{line.strip().lower() for line in ["  Karan  ", "Lara", "Karan", ""] if line.strip()}
# {'Karan', 'Lara'}

# Unique file extensions in a directory
from pathlib import Path
{p.suffix for p in Path(".").iterdir() if p.suffix}          # {'.py', '.md', '.json'}

# Extra: unique email domains from a list of addresses
emails = ["Karan@x.io", "Lara@y.com", "Drishya@x.io"]
{e.split("@")[1] for e in emails}                             # {'x.io', 'y.com'}
```

**Set operations**

Set comprehensions are well suited to feeding set operations.

```python
admins = {u["name"] for u in users if u["role"] == "admin"}
banned = {u["name"] for u in users if u["status"] == "banned"}

admins - banned    # admin, but not banned
admins | banned    # admin, or banned, or both
admins & banned     # both
admins ^ banned     # exactly one of the two (symmetric difference)
```

**Pitfalls**

The output must be hashable — `{[1, 2, 3] for x in range(3)}` raises `TypeError: unhashable type: 'list'`, since a set can only hold hashable elements; a list comprehension is the right tool if the output is itself mutable.

A set comprehension has no colon: `{x for x in range(5)}` is a set comprehension producing `{0, 1, 2, 3, 4}`, while `{x: x * x for x in range(5)}` is a dict comprehension. A bare `{1, 2, 3}` is a set literal, `{1: 2}` is a dict literal, and the presence or absence of the colon is what tells them apart.

## **Dict Comprehensions**

A dict comprehension builds a dict of key-value pairs. The output expression is `key: value`, separated by a colon.

```python
{s: s * s for s in range(5)}                                 # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
{w: len(w) for w in "the quick brown fox".split()}
# {'the': 3, 'quick': 5, 'brown': 5, 'fox': 3}
```

**Mapping and indexing**

```python
users = [
    {"name": "Karan", "age": 36},
    {"name": "Lara", "age": 22},
    {"name": "Drishya", "age": 41},
]

# name -> age
by_name = {u["name"]: u["age"] for u in users}

# Index a list of records by a field
by_id = {u.get("id", i): u for i, u in enumerate(users)}

# Swap keys and values
{v: k for k, v in {"a": 1, "b": 2}.items()}                    # {1: 'a', 2: 'b'}

# Filter a dict by a value condition
prices = {"apple": 1.5, "bread": 3.0, "cheese": 8.0, "egg": 0.5}
cheap = {k: v for k, v in prices.items() if v < 5}
# {'apple': 1.5, 'bread': 3.0, 'egg': 0.5}

# Compute a derived value
scores = {"Karan": 0.91, "Lara": 0.45, "Drishya": 0.78}
grades = {k: ("pass" if v >= 0.5 else "fail") for k, v in scores.items()}

# Convert two parallel lists into a dict
keys = ["a", "b", "c"]
vals = [1, 2, 3]
{k: v for k, v in zip(keys, vals)}                             # {'a': 1, 'b': 2, 'c': 3}
```

**Counting and indexing**

```python
text = "the quick brown fox"
{ch: text.count(ch) for ch in set(text) if ch != " "}

words = "the cat sat on the mat the".split()
{word: words.count(word) for word in set(words)}
# {'the': 3, 'cat': 1, 'sat': 1, 'on': 1, 'mat': 1}

# Build an index: word -> first position in text
{word: i for i, word in enumerate(words) if word not in words[:i]}

# Extra: build a per-user count of failed logins from an event log
events = [
    {"user": "Karan", "type": "login_fail"},
    {"user": "Lara", "type": "login_ok"},
    {"user": "Karan", "type": "login_fail"},
]
fail_counts = {u: sum(1 for e in events if e["user"] == u and e["type"] == "login_fail")
               for u in {e["user"] for e in events}}
# {'Karan': 2, 'Lara': 0}
```

**String and path manipulation**

```python
raw_dict = {"  Name ": "Karan", "AGE": 36}

{k.strip().lower(): v for k, v in raw_dict.items()}            # normalize keys
{k.removeprefix("user_"): v for k, v in raw_dict.items()}      # strip a prefix

# Map filenames to file sizes
from pathlib import Path
{p.name: p.stat().st_size for p in Path(".").glob("*.py") if p.is_file()}

# Map status code -> description, then invert it
status = {200: "OK", 201: "Created", 404: "Not Found"}
{v: k for k, v in status.items()}                               # {'OK': 200, 'Created': 201, 'Not Found': 404}
```

**Configuration and FastAPI patterns**

```python
# Build config from env vars, with type coercion
import os
{key.removeprefix("APP_"): int(value)
 for key, value in os.environ.items()
 if key.startswith("APP_") and value.isdigit()}

# Pydantic -- {field_name: default_value} for optional fields
{name: field.default
 for name, field in SettingsModel.model_fields.items()
 if field.default is not None}
```

**Pitfalls**

Dict keys must be hashable — `{[1, 2]: "list"}` raises `TypeError: unhashable type: 'list'`; lists, sets, and dicts cannot be keys, but tuples are hashable if their own elements are.

Duplicate keys silently overwrite each other: `{a: 1 for a in ["x", "x", "y"]}` gives `{'x': 1, 'y': 1}`, keeping only the last `"x"`.

A dict comprehension cannot do true one-key-to-many-values grouping directly — `{cat: [r for r in records if r["category"] == cat] for cat in categories}` works, but rescans `records` once per category, an `O(N × M)` cost. Real grouping belongs to `collections.defaultdict` or `itertools.groupby`.

```python
from collections import defaultdict

groups = defaultdict(list)
for r in records:
    groups[r["category"]].append(r["name"])
# O(N), one pass
```

## **Generator Expressions**

A generator expression looks like a list comprehension with parentheses instead of brackets. It returns a generator object — a lazy iterator that computes each value on demand.

```python
squares_list = [n * n for n in range(1_000_000)]      # builds the full list -- several MB
squares_gen  = (n * n for n in range(1_000_000))       # a small generator object -- lazy
```

```python
gen = (x * x for x in range(5))
type(gen)            # <class 'generator'>

for sq in gen:
    print(sq)          # 0, 1, 4, 9, 16

list(gen)              # [] -- already consumed, a generator only iterates once
```

Parentheses around a generator expression can be omitted when it is the sole argument to a function call — the more idiomatic form.

```python
sum(x * x for x in range(10))         # preferred
sum((x * x for x in range(10)))        # equivalent, but the extra parens are unnecessary
```

**Lazy pipelines**

```python
total = sum(x * x for x in range(1, 11) if x % 2 == 0)   # 220

any(x % 2 == 0 for x in [1, 3, 5, 7, 9])                   # False
any(x % 2 == 0 for x in [1, 3, 5, 7, 8])                   # True -- stops as soon as 8 is seen

all(x > 0 for x in [1, 2, 3])                               # True
next(x for x in [1, 3, 5, 8, 9] if x % 2 == 0)              # 8
next((x for x in [1, 3, 5] if x % 2 == 0), "no match")      # 'no match'

min(users, key=lambda u: u["age"])
max(items, key=lambda x: x.priority, default=None)

# Length of a stream without loading it fully
line_count = sum(1 for _ in open("huge.log"))
```

**Chained generator expressions**

```python
# Flatten a nested list, lazily
nested = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat_gen = (n for row in nested for n in row)               # generator, not a list

# Cartesian product as a generator
gen = ((x, y) for x in range(3) for y in range(3))

# Filtered cartesian product
pairs = ((x, y) for x in range(10) for y in range(10) if x < y)
```

**With built-ins and files**

```python
count = sum(1 for _ in open("big.txt") if "TODO" in _)

import json

def records(path):
    with open(path) as f:
        for line in f:
            yield json.loads(line)

ids = [r["id"] for r in records("users.jsonl")]              # a list comp fed by a generator function
```

**Pitfalls**

A generator, like any iterator, can only be consumed once — `list(gen)` a second time returns `[]`. If multiple passes are needed, materialize it with `list()` or `tuple()`.

A generator expression with an always-false filter is empty, not infinite: `(x for x in range(10) if False)` produces zero items on iteration.

A generator cannot be indexed — `gen[0]` raises `TypeError`. Indexing, slicing, or `len()` requires materializing it first.

Forgetting to parenthesize a generator when it is not the sole argument to a call is a real trap:

```python
sum(x * x for x in range(10))                 # correct -- the generator, no extra argument
sum((x * x for x in range(10)), 0)             # correct -- the generator plus an explicit start value
sum(x * x for x in range(10), 0)               # SyntaxError -- ambiguous without the extra parens
```

## **Chained Comprehensions**

Chaining means using more than one `for` clause inside the same comprehension. Each `for` clause adds a level of iteration, and the result is a single flat container.

```python
# Traditional nested loop
pairs = []
for color in ["red", "green", "blue"]:
    for size in ["S", "M", "L"]:
        pairs.append((color, size))

# Chained comprehension -- one line
pairs = [(color, size) for color in ["red", "green", "blue"] for size in ["S", "M", "L"]]
```

**Cartesian products**

```python
[(c, s) for c in ["red", "blue"] for s in [1, 2, 3]]
# [('red', 1), ('red', 2), ('red', 3), ('blue', 1), ('blue', 2), ('blue', 3)]

[i * j for i in range(1, 4) for j in range(1, 4)]           # multiplication table, flattened
# [1, 2, 3, 2, 4, 6, 3, 6, 9]

[(x, y, z) for x in range(2) for y in range(2) for z in range(2)]   # 8 triples

# Extra: all 8-directional neighbor offsets for a grid algorithm, excluding the center
[(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0)]
# [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
```

**Flattening**

```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [n for row in matrix for n in row]                    # [1, 2, ..., 9]

# Flatten a list of dicts into (key, value) tuples
records = [{"a": 1, "b": 2}, {"c": 3}, {"d": 4, "e": 5}]
flat = [(k, v) for r in records for k, v in r.items()]

# Flatten a 3D structure
cube = [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
flat = [n for layer in cube for row in layer for n in row]
# [1, 2, 3, 4, 5, 6, 7, 8]

# Flatten only certain rows
rows = [[1, 2], [], [3, 4, 5], [], [6]]
flat = [n for row in rows if row for n in row]                # skips empty rows
```

**With filters and conditions**

```python
[(x, y) for x in range(5) for y in range(5) if x != y]

# Multiple `if` filters -- equivalent to combining them with `and`
[x for x in range(100) for y in [1, 2] if x % y == 0 if x < 50]

# The inner iterable can depend on the outer variable
[(a, b) for a in range(5) for b in range(a)]
# (1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (4, 3)

# Build all valid (user, role, permission) triples from a permission map
users = ["Karan", "Lara", "Drishya"]
role_perms = {"admin": ["read", "write", "delete"], "user": ["read", "write"]}
[(u, r, p) for u in users for r, perms in role_perms.items() for p in perms]
```

**Real library patterns**

```python
# Pandas -- collect all (col, value) pairs from a DataFrame
import pandas as pd
df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
[(c, v) for c in df.columns for v in df[c]]
# [('a', 1), ('a', 2), ('b', 3), ('b', 4)]

# All (filename, size) pairs for every file in every subdirectory
from pathlib import Path
[(p.name, p.stat().st_size)
 for d in Path(".").iterdir() if d.is_dir()
 for p in d.rglob("*") if p.is_file()]

# Cartesian product for a small test matrix
inputs = [{"user_id": 1, "name": "Karan"}, {"user_id": 2, "name": "Lara"}]
methods = ["GET", "POST"]
[(i, m) for i in inputs for m in methods]
```

`for` clauses read left to right and execute in the same order — the first `for` is the outermost loop, and the last is the innermost.

```python
[expr for a in A for b in B for c in C]

# Equivalent nested loop
for a in A:
    for b in B:
        for c in C:
            result.append(expr)
```

**Pitfalls**

The inner `for` can reference the outer variable, since it runs after the outer has bound its value, but the reverse is a `NameError`.

```python
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [n for row in matrix for n in row]                # OK -- inner uses outer variable
# flat = [n for n in row for row in matrix]              # NameError -- 'row' is not defined yet
```

Two chained `for` clauses read easily; three is about the limit before a plain loop, or a generator function, is more readable.

```python
def triple_iter():
    for x in A:
        for y in B:
            for z in C:
                if x + y + z > 0:
                    yield (x, y, z)
```

A chained generator expression can only be iterated once, just like any other generator.

## **Nested Comprehensions**

A nested comprehension has one or more comprehensions as the output expression of an outer comprehension, producing a nested structure such as a list of lists.

```python
# Traditional nested loop
matrix = []
for x in range(3):
    row = []
    for y in range(3):
        row.append(x + y)
    matrix.append(row)

# Nested list comprehension
matrix = [[x + y for y in range(3)] for x in range(3)]
# [[0, 1, 2], [1, 2, 3], [2, 3, 4]]
```

**Matrix operations**

```python
# 3x3 identity matrix
[[1 if i == j else 0 for j in range(3)] for i in range(3)]
# [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

# Multiplication table
[[i * j for j in range(1, 5)] for i in range(1, 5)]

# Transpose a matrix
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed = [[row[i] for row in matrix] for i in range(3)]
# [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

# Add two matrices element-wise
a = [[1, 2], [3, 4]]
b = [[5, 6], [7, 8]]
c = [[a[i][j] + b[i][j] for j in range(2)] for i in range(2)]
# [[6, 8], [10, 12]]

# Extra: build a labeled grid for a board game
board_size = 3
[[f"{chr(65 + row)}{col + 1}" for col in range(board_size)] for row in range(board_size)]
# [['A1', 'A2', 'A3'], ['B1', 'B2', 'B3'], ['C1', 'C2', 'C3']]
```

**Grouping into a list of lists**

```python
# Bucket numbers by parity
buckets = [[n for n in range(6) if n % 2 == p] for p in [0, 1]]
# [[0, 2, 4], [1, 3, 5]]

# Group words by length
words = ["the", "quick", "brown", "fox", "jumps"]
buckets = [[w for w in words if len(w) == n] for n in [3, 4, 5]]
# [['the', 'fox'], [], ['quick', 'brown', 'jumps']]

# Chunks of size n
data = list(range(10))
n = 3
chunks = [data[i:i + n] for i in range(0, len(data), n)]
# [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
# (equivalent to list(itertools.batched(data, n)) in 3.12+)

# Adjacent pairs -- a sliding window of size 2
pairs = [[data[i], data[i + 1]] for i in range(len(data) - 1)]
# (equivalent to list(itertools.pairwise(data)))
```

**Nested dict comprehensions — two-level mappings**

```python
# (a, b) -> value
{(a, b): a * b for a in range(3) for b in range(3)}

# Per-user, per-day log
days = ["mon", "tue", "wed"]
users = ["Karan", "Lara"]
{user: {day: 0 for day in days} for user in users}
# {'Karan': {'mon': 0, 'tue': 0, 'wed': 0}, 'Lara': {...}}

# Group records by a key
records = [
    {"category": "fruit", "name": "apple"},
    {"category": "fruit", "name": "banana"},
    {"category": "veg", "name": "carrot"},
]
{cat: [r["name"] for r in records if r["category"] == cat]
 for cat in {r["category"] for r in records}}
# {'fruit': ['apple', 'banana'], 'veg': ['carrot']}

# Extra: nested dict describing which required fields are missing per record
required_fields = {"name", "age", "email"}
incoming = [{"name": "Karan", "age": 36}, {"name": "Lara", "email": "Lara@y.com"}]
{i: sorted(required_fields - r.keys()) for i, r in enumerate(incoming)}
# {0: ['email'], 1: ['age']}
```

**Nested set and generator forms**

```python
# A list of sets works; a set of sets does not, since sets are unhashable
[[(i, j) for j in range(3)] for i in range(3)]

# Nested generator expression -- a stream of streams, lazily
gen = ((i * j for j in range(3)) for i in range(3))
for row in gen:
    print(list(row))         # [0, 1, 2] / [0, 2, 4] / [0, 3, 6]
```

**Pitfalls**

A nested list comprehension reads inside-out: `[[x * y for y in range(3)] for x in range(3)]` — the inner comprehension is the row builder, and the outer comprehension is the structure that holds each row.

Using a nested comprehension to filter and group at scale is an `O(N × M)` scan, the same trap as the dict-comprehension version above; `itertools.groupby` after sorting, or `collections.defaultdict`, does the real grouping in one pass.

A nested list comprehension over a large range is a real memory spike: `[[i * j for j in range(1000)] for i in range(1000)]` builds a million-element list. Making the outer comprehension a generator expression instead streams row by row.

```python
big_gen = ([i * j for j in range(1000)] for i in range(1000))   # streams, far less memory
```

## **Reading Order vs Execution Order**

| Construct | Reading Direction | Execution Direction |
| --- | --- | --- |
| `[expr for x in X]` | left to right | left to right |
| `[expr for x in X if c]` | filter reads last | filters items as they are produced |
| `[expr for a in A for b in B]` | left to right | outer first, then inner |
| `[[expr for y in Y] for x in X]` | outer first in syntax | inner is rebuilt for every outer iteration |

The comprehension reads top-to-bottom, and that is also how Python evaluates it.

## **Comprehensions in Real Codebases**

```python
# Pandas -- select numeric columns and build a derived column
import pandas as pd
df = pd.DataFrame({"name": ["Karan", "Lara", "Drishya"], "score": [0.91, 0.45, 0.78]})
numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
df["grade"] = [("pass" if s >= 0.5 else "fail") for s in df["score"]]

# FastAPI / Pydantic -- introspecting a model
optional_fields = {name: field.default
                    for name, field in User.model_fields.items()
                    if field.default is not None}
paths = [r.path for r in app.routes if hasattr(r, "path")]

# pathlib -- files modified in the last 24 hours
from pathlib import Path
import time
now = time.time()
recent = [p for p in Path(".").rglob("*") if p.is_file() and (now - p.stat().st_mtime) < 86400]

# asyncio / httpx -- scheduling concurrent requests
import asyncio
import httpx

async def fetch_all(urls):
    async with httpx.AsyncClient() as client:
        tasks = [client.get(u) for u in urls]     # list comprehension of coroutines
        return await asyncio.gather(*tasks)

# pytest -- building parametrized test cases
[(n, n * n) for n in range(5)]
# [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)]
```

| Library / Tool | Key Feature | Best Use Case |
| --- | --- | --- |
| Pandas | Column and row selection via comprehension | Building derived columns, filtering by dtype |
| FastAPI / Pydantic | `model_fields` introspection | Extracting required fields and defaults |
| pathlib | `glob`/`rglob` combined with a filter | File discovery and reporting |
| httpx / asyncio | Comprehension of coroutines fed to `gather` | Concurrent outbound requests |
| pytest | Comprehension of `(input, expected)` tuples | Parametrized test case generation |

## **Common Mistakes**

- Using a comprehension purely for its side effect, such as `[print(x) for x in items]` or `[cache.set(k, v) for k, v in items]` — this builds and discards a throwaway list of `None`s; a plain `for` loop is the correct tool when there is no list to build.
- Relying on the pre-3.13 comprehension scope leak in a class body, where the loop variable was accessible after the comprehension finished; PEP 709 and PEP 3186 (Python 3.13) fixed this leak inside both functions and class bodies, so code depending on the old leaking behavior breaks on upgrade.
- Reusing an already-consumed generator expression and expecting values again, since a generator — like any iterator — can only be iterated once.
- Passing an unhashable value, such as a list, as a set element or a dict key, which raises `TypeError: unhashable type` at the point the comprehension tries to insert it.
- Assuming duplicate keys in a dict comprehension merge or error — they silently overwrite, keeping only the last value written for that key.
- Reaching for a nested or dict comprehension to group many items into a few buckets, which rescans the whole source once per bucket; `collections.defaultdict` or `itertools.groupby` (after sorting) does the same job in a single pass.
- Chaining four or more `for` clauses in one comprehension, or nesting comprehensions three levels deep, which becomes far harder to read than the equivalent `for` loop or a small generator function.
- Forgetting the extra parentheses around a generator expression when it is not the sole argument to a function call, producing a `SyntaxError` instead of the intended call.

## **Modern Python Patterns**

| Older Style | Modern Style |
| --- | --- |
| Hand-written chunking with `data[i:i+n]` inside a comprehension | `itertools.batched(data, n)` (3.12+) |
| Hand-written sliding-window pairs with `[data[i], data[i+1]]` | `itertools.pairwise(data)` (3.10+) |
| Comprehension loop variables leaking into a class body or enclosing function | Fixed by default since Python 3.13 (PEP 709, PEP 3186) |
| Manual `if key not in seen: seen.add(key)` dedupe loop | A set comprehension, `{expr for x in iterable}` |
| Repeating an expensive call in both the filter and the output of a comprehension | The walrus operator, `(y := f(x))`, computing it once |

```python
from itertools import batched, pairwise

data = list(range(10))

# Chunking
list(batched(data, 3))          # [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9,)]

# Sliding window pairs
list(pairwise(data))             # [(0, 1), (1, 2), ..., (8, 9)]
```

## **The Comprehension Decision Table**

| Want to... | Use |
| --- | --- |
| Build a list from a loop, possibly filtered | List comprehension |
| Build a list from a loop, but the data is large or unbounded | Generator expression |
| Build a set of unique items | Set comprehension |
| Build a mapping | Dict comprehension |
| Iterate a cartesian product, possibly filtered | Chained comprehension |
| Build a nested structure (list of lists, and similar) | Nested comprehension |
| Build a sequence of unknown size | Generator expression |
| Compute one value from a sequence (`sum`, `any`, `all`, `min`, `max`) | Generator expression, no need to materialize |
| Group many items into a few buckets | `defaultdict`, `Counter`, or `itertools.groupby` — not a comprehension |
| Run a side effect for each item | `for` loop, not a comprehension |
| Break out of the iteration early | A generator function with `return`, or a `for` loop |

## **Quick Reference**

```python
# List
[x * x for x in range(5)]                    # [0, 1, 4, 9, 16]
[x for x in xs if x > 0]                      # filter
[x * 2 if x > 0 else 0 for x in xs]           # ternary in the output
[(x, y) for x in A for y in B]                # chained / cartesian
[[x * y for y in B] for x in A]               # nested

# Set
{x % 10 for x in xs}                          # unique
{x for x in xs if x > 0}                       # filtered unique

# Dict
{x: x * x for x in range(5)}                  # key -> value
{k: v for k, v in d.items() if v}             # filter
{v: k for k, v in d.items()}                  # invert
{name: idx for idx, name in enumerate(names)}  # index

# Generator
(x * x for x in range(10))                    # one at a time
sum(x * x for x in range(10) if x % 2 == 0)   # feeds a builtin

# Chained
[(x, y) for x in A for y in B]                # cartesian
[(x, y) for x in A for y in B if x != y]      # filtered cartesian
[n for row in matrix for n in row]            # flatten

# Nested
[[x * y for y in range(3)] for x in range(3)]  # matrix
{(a, b): a * b for a in A for b in B}          # 2D dict

# Walrus
[y for x in xs if (y := f(x)) > 0]             # compute once, reuse
```