# **Python Tuples**

## **What is a Tuple?**

A Tuple is exactly the same as a List except that it is immutable. Once a Tuple object is created, no changes can be performed on it. Think of it as the read-only version of a List.

If our data is fixed and never changes, we should go for a Tuple.

- Insertion order is preserved.
- Duplicate objects are allowed.
- Heterogeneous objects are allowed (numbers, strings, booleans, etc.).
- Index plays a very important role — it helps preserve insertion order and differentiate duplicates.
- Tuples support both positive (left to right) and negative (right to left) indexing.
- Elements are represented within parentheses `()` and separated by commas.
- Parentheses are optional but strongly recommended for readability.

---

## **Creating Tuple Objects**

### **Empty Tuple**

```python
t = ()
print(type(t))  # <class 'tuple'>
```

### **Tuple without Parentheses (packing)**

```python
t = 10, 20, 30, 40
print(t)        # (10, 20, 30, 40)
print(type(t))  # <class 'tuple'>
```

### **Tuple with Parentheses**

```python
t = (10, 20, 30, 40)
print(t)        # (10, 20, 30, 40)
print(type(t))  # <class 'tuple'>
```

### **Single-Valued Tuple — Trailing Comma is Mandatory**

This is the most common beginner mistake with tuples. Without the trailing comma, Python treats the expression as a plain value inside parentheses, not a tuple.

```python
# WRONG — treated as int, not a tuple
t = (10)
print(t)        # 10
print(type(t))  # <class 'int'>

# CORRECT — trailing comma makes it a tuple
t = (10,)
print(t)        # (10,)
print(type(t))  # <class 'tuple'>

# Also valid without parentheses
t = 10,
print(t)        # (10,)
print(type(t))  # <class 'tuple'>
```

### **Valid and Invalid Tuple Expressions**

| Expression | Valid? | Reason |
|---|---|---|
| `t = ()` | Valid | Empty tuple. |
| `t = 10, 20, 30` | Valid | Multiple values; parentheses optional. |
| `t = 10` | Invalid | Treated as an integer, not a tuple. |
| `t = 10,` | Valid | Single-valued tuple; no parentheses needed. |
| `t = (10)` | Invalid | Integer inside parentheses — no comma. |
| `t = (10,)` | Valid | Correct single-valued tuple. |
| `t = (10, 20, 30)` | Valid | Standard tuple with parentheses. |

### **Using `tuple()` Function**

From a list:

```python
scores = [85, 90, 78, 92]
t = tuple(scores)
print(t)  # (85, 90, 78, 92)
```

From a `range()`:

```python
t = tuple(range(10, 20, 2))
print(t)  # (10, 12, 14, 16, 18)
```

From a string (each character becomes an element):

```python
t = tuple("durga")
print(t)  # ('d', 'u', 'r', 'g', 'a')
```

---

## **Accessing Elements of a Tuple**

### **By Index**

```python
t = (10, 20, 30, 40, 50, 60)
print(t[0])    # 10
print(t[-1])   # 60
# print(t[100])  # IndexError: tuple index out of range
```

### **By Slicing**

Syntax: `t[start:stop:step]`

```python
t = (10, 20, 30, 40, 50, 60)

print(t[1:4])    # (20, 30, 40)
print(t[:])      # (10, 20, 30, 40, 50, 60)
print(t[::-1])   # (60, 50, 40, 30, 20, 10)  — reversed
print(t[2:5])    # (30, 40, 50)
print(t[2:100])  # (30, 40, 50, 60)  — no IndexError for out-of-range stop
print(t[::2])    # (10, 30, 50)      — every second element
```

---

## **Tuple Immutability**

Once a tuple is created, its content cannot be changed. Any attempt to modify, add, or remove an element raises a `TypeError`.

```python
t = (10, 20, 30, 40)
t[1] = 70  # TypeError: 'tuple' object does not support item assignment
```

```python
t = (10, 20, 30)
t.append(40)  # AttributeError: 'tuple' object has no attribute 'append'
```

> **Important distinction — mutable objects inside a tuple:** The tuple itself is immutable (you cannot replace its elements), but if an element is a mutable object like a list, that inner object can still be mutated.
>
> ```python
> t = (1, [2, 3], 4)
> t[1].append(99)   # WORKS — mutating the list inside the tuple
> print(t)          # (1, [2, 3, 99], 4)
>
> t[1] = [5, 6]     # TypeError — cannot replace the element itself
> ```

---

## **Mathematical Operators on Tuples**

### **Concatenation (`+`)**

Used to join two tuples into a new tuple. Both operands must be tuples.

```python
t1 = (10, 20, 30)
t2 = (40, 50, 60)
t3 = t1 + t2
print(t3)  # (10, 20, 30, 40, 50, 60)
```

### **Repetition (`*`)**

Used to repeat a tuple's elements a specified number of times.

```python
t = (0,) * 5
print(t)  # (0, 0, 0, 0, 0)

t1 = (10, 20, 30)
t2 = t1 * 3
print(t2)  # (10, 20, 30, 10, 20, 30, 10, 20, 30)
```

---

## **Important Functions of Tuple**

### **`len()`**

Returns the number of elements in the tuple.

```python
t = (10, 20, 30, 40)
print(len(t))  # 4
```

### **`count()`**

Returns the number of occurrences of a specified element.

```python
grades = ("A", "B", "A", "C", "A", "B")
print(grades.count("A"))  # 3
print(grades.count("D"))  # 0
```

### **`index()`**

Returns the index of the first occurrence of a specified element. Raises `ValueError` if the element is not found.

```python
t = (10, 20, 10, 10, 20)
print(t.index(10))  # 0
print(t.index(20))  # 1

# Guard with `in` before calling index() to avoid ValueError:
if 30 in t:
    print(t.index(30))
else:
    print("30 not found")
```

### **`sorted()`**

Returns a new **list** sorted in ascending order. The original tuple is unchanged. This is a built-in function, not a tuple method, because tuples cannot be modified in place.

```python
t = (40, 10, 30, 20)

sorted_asc = sorted(t)
print(sorted_asc)  # [10, 20, 30, 40]  ← returns a list
print(t)           # (40, 10, 30, 20)  ← original unchanged

sorted_desc = sorted(t, reverse=True)
print(sorted_desc) # [40, 30, 20, 10]
```

### **`min()` and `max()`**

```python
t = (40, 10, 30, 20)
print(min(t))  # 10
print(max(t))  # 40
```

### **`sum()`**

```python
t = (10, 20, 30, 40)
print(sum(t))  # 100
```

---

## **Tuple Packing and Unpacking**

### **Packing**

Grouping multiple variables into a single tuple.

```python
name = "Rohit"
age = 22
role = "analyst"

record = name, age, role       # packing
print(record)                  # ('Rohit', 22, 'analyst')
```

### **Unpacking**

Extracting tuple elements into individual variables. The number of variables must exactly match the number of elements, otherwise a `ValueError` is raised.

```python
t = ("Tanvi", 88, "engineer")
name, score, role = t
print(f"{name} — {score} — {role}")  # Tanvi — 88 — engineer
```

Mismatch raises a `ValueError`:

```python
t = (10, 20, 30, 40)
a, b, c = t  # ValueError: too many values to unpack (expected 3)
```

### **Extended Unpacking with `*` (Python 3+)**

Use `*variable` to capture remaining elements into a list. This is a very useful pattern that the original notes did not cover.

```python
first, *middle, last = (10, 20, 30, 40, 50)
print(first)   # 10
print(middle)  # [20, 30, 40]  ← captured as a list
print(last)    # 50
```

```python
# Practical: split head from tail in a data pipeline
top, *rest = (95, 88, 72, 60, 45)
print(f"Top score — {top}")
print(f"Remaining — {rest}")
```

### **Swapping Variables with Tuple Unpacking**

```python
a, b = 10, 20
a, b = b, a   # no temporary variable needed
print(a, b)   # 20 10
```

---

## **Tuple Comprehension — Does Not Exist**

Python does not support tuple comprehension. Using `(expression for ...)` creates a **generator object**, not a tuple.

```python
gen = (x ** 2 for x in range(1, 6))
print(type(gen))  # <class 'generator'>

for val in gen:
    print(val)  # 1, 4, 9, 16, 25
```

To get a tuple from a comprehension, wrap with `tuple()`:

```python
t = tuple(x ** 2 for x in range(1, 6))
print(t)        # (1, 4, 9, 16, 25)
print(type(t))  # <class 'tuple'>
```

---

## **Sum and Average of Tuple Elements**

```python
# WRONG — eval() is a security risk and fragile
t = eval(input("Enter tuple: "))  # DO NOT use this

# CORRECT — construct tuple safely
raw = input("Enter numbers separated by commas: ")  # "10,20,30"
t = tuple(int(x.strip()) for x in raw.split(","))
total = sum(t)
average = total / len(t)
print(f"Sum — {total}")
print(f"Average — {average:.2f}")
```

---

## **List vs Tuple — Comparison**

| Feature | List | Tuple |
|---|---|---|
| Syntax | `[10, 20, 30]` | `(10, 20, 30)` |
| Mutability | Mutable — elements can be changed. | Immutable — elements cannot be changed. |
| Use case | Dynamic content that changes over time. | Fixed content that should not change. |
| Dictionary key | Cannot be used (unhashable). | Can be used (hashable). |
| Set member | Cannot be used (unhashable). | Can be used (hashable). |
| Memory | Slightly more memory (dynamic resizing overhead). | More memory-efficient for fixed data. |
| Methods available | `append`, `extend`, `insert`, `remove`, `pop`, `sort`, `reverse`, `copy`, `clear` | `count`, `index` only. |
| Iteration speed | Slightly slower. | Slightly faster. |
| Insertion order | Preserved. | Preserved. |
| Duplicates | Allowed. | Allowed. |
| Heterogeneous types | Allowed. | Allowed. |
| Indexing and slicing | Supported. | Supported. |

---

## **Tuples as Dictionary Keys and Set Members**

Because tuples are immutable, they are hashable and can be used as dictionary keys or set members — a feature lists do not have.

```python
# Tuple as dictionary key
location_data = {
    (28.6139, 77.2090): "Delhi",
    (19.0760, 72.8777): "Mumbai",
    (18.5204, 73.8567): "Pune",
}
print(location_data[(18.5204, 73.8567)])  # Pune

# Tuple as set member
visited = {(28.6139, 77.2090), (18.5204, 73.8567)}
print((18.5204, 73.8567) in visited)  # True
```

```python
# List fails as dictionary key
coords = [18.52, 73.85]
d = {coords: "Pune"}  # TypeError: unhashable type: 'list'
```

---

## **`namedtuple` — Named Tuples**

A `namedtuple` is a tuple subclass with field names. Elements can be accessed by name (dot notation) as well as by index. This is the bridge between a plain tuple and a full class.

```python
from collections import namedtuple

Student = namedtuple("Student", ["name", "roll", "score"])

s1 = Student(name="Harsha", roll=101, score=92)
print(s1.name)   # Harsha  ← by name
print(s1[2])     # 92      ← by index
print(s1)        # Student(name='Harsha', roll=101, score=92)
```

Named tuples are still immutable:

```python
s1.score = 95  # AttributeError: can't set attribute
```

### **`typing.NamedTuple` — Modern Syntax with Type Hints**

`typing.NamedTuple` gives the same class-syntax feel as a `dataclass` and works better with type checkers. Prefer this over `collections.namedtuple` in new code.

```python
from typing import NamedTuple

class ExamResult(NamedTuple):
    student: str
    subject: str
    marks: int
    grade: str = "B"   # default value supported

r = ExamResult(student="Tanvi", subject="Maths", marks=88)
print(r)         # ExamResult(student='Tanvi', subject='Maths', marks=88, grade='B')
print(r.marks)   # 88
print(r[2])      # 88  ← index access still works
```

### **`namedtuple` vs `dataclass` — When to Use What**

| Feature | `namedtuple` / `NamedTuple` | `@dataclass` | `@dataclass(frozen=True)` |
|---|---|---|---|
| Mutability | Immutable. | Mutable. | Immutable. |
| Iterable | Yes (like a tuple). | No (not by default). | No (not by default). |
| Hashable | Yes. | No (unless frozen). | Yes. |
| Dict/set key | Yes. | No. | Yes. |
| Memory | Lighter. | Slightly heavier. | Slightly heavier. |
| Type hints | With `NamedTuple`. | Yes. | Yes. |
| Best for | Read-only records, CSV rows, DB results, dict keys. | Internal mutable data objects. | Immutable data with full class features. |

```python
# Immutable dataclass — alternative to NamedTuple with more flexibility
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    host: str
    port: int
    debug: bool = False

cfg = Config(host="localhost", port=8080)
print(cfg.host)  # localhost
cfg.port = 9090  # FrozenInstanceError: cannot assign to field 'port'
```

---

## **Common Mistakes**

### **1. Forgetting the trailing comma for a single-valued tuple**

```python
# WRONG
t = (42)
print(type(t))  # <class 'int'>

# CORRECT
t = (42,)
print(type(t))  # <class 'tuple'>
```

### **2. Trying to modify a tuple element**

```python
t = ("admin", "editor", "viewer")
t[0] = "superuser"  # TypeError: 'tuple' object does not support item assignment

# CORRECT — convert to list, modify, convert back
lst = list(t)
lst[0] = "superuser"
t = tuple(lst)
print(t)  # ('superuser', 'editor', 'viewer')
```

### **3. Expecting tuple comprehension to work**

```python
# WRONG — creates a generator, not a tuple
t = (x * 2 for x in range(5))
print(type(t))  # <class 'generator'>

# CORRECT
t = tuple(x * 2 for x in range(5))
print(t)  # (0, 2, 4, 6, 8)
```

### **4. Using `eval()` to accept tuple input from users**

```python
# WRONG — security risk
t = eval(input("Enter tuple: "))

# CORRECT
import ast
t = ast.literal_eval(input("Enter tuple: "))
```

### **5. Unpacking with wrong variable count**

```python
t = (10, 20, 30, 40)

# WRONG
a, b, c = t   # ValueError: too many values to unpack

# CORRECT — match count exactly
a, b, c, d = t

# OR — use extended unpacking
first, *rest = t
print(first)  # 10
print(rest)   # [20, 30, 40]
```

### **6. Assuming `sorted()` returns a tuple**

```python
t = (30, 10, 20)
result = sorted(t)
print(type(result))  # <class 'list'>  ← not a tuple

# Convert back if needed
result = tuple(sorted(t))
print(type(result))  # <class 'tuple'>
```

### **7. Thinking an inner mutable object is also protected**

```python
t = (1, [2, 3], 4)
t[1].append(99)  # Works — the list inside is still mutable
print(t)         # (1, [2, 3, 99], 4)
```

---

## **Production Patterns**

### **Returning Multiple Values from a Function**

Functions in Python return tuples when they return multiple values. This is one of the most common uses of tuples in real code.

```python
def get_stats(data: list[float]) -> tuple[float, float, float]:
    return min(data), max(data), sum(data) / len(data)

low, high, avg = get_stats([85, 90, 72, 88, 60])
print(f"Min — {low}, Max — {high}, Avg — {avg:.1f}")
```

### **Tuples as Immutable Config / Constants**

```python
# Allowed HTTP methods — should never change at runtime
ALLOWED_METHODS = ("GET", "POST", "PUT", "DELETE", "PATCH")

def validate_method(method: str) -> bool:
    return method.upper() in ALLOWED_METHODS
```

### **Processing CSV / DB Rows**

Database cursors and CSV readers often return rows as tuples. `namedtuple` gives those rows readable field names.

```python
from collections import namedtuple
import csv

Record = namedtuple("Record", ["name", "score", "grade"])

def load_results(filepath: str) -> list[Record]:
    results = []
    with open(filepath) as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            results.append(Record(name=row[0], score=int(row[1]), grade=row[2]))
    return results
```

### **Using Tuples as Dictionary Keys (Composite Keys)**

```python
# Student scores per subject — (student_id, subject) as composite key
score_map: dict[tuple[int, str], int] = {
    (1001, "Maths"):   88,
    (1001, "Science"): 74,
    (1002, "Maths"):   91,
}

print(score_map[(1001, "Maths")])  # 88
```

### **Coordinate / Point Data in ML Pipelines**

```python
from typing import NamedTuple

class DataPoint(NamedTuple):
    feature_a: float
    feature_b: float
    label: int

dataset: list[DataPoint] = [
    DataPoint(1.2, 3.4, 0),
    DataPoint(5.6, 7.8, 1),
    DataPoint(2.1, 0.9, 0),
]

positives = [p for p in dataset if p.label == 1]
print(positives)  # [DataPoint(feature_a=5.6, feature_b=7.8, label=1)]
```

### **Structured Data Comparison Table**

| Structure | Mutable | Hashable | Type Hints | Best Use Case |
|---|---|---|---|---|
| `tuple` | No | Yes | No | Simple fixed records, dict keys, multi-return. |
| `namedtuple` | No | Yes | No | Named fields, CSV/DB rows, lightweight records. |
| `NamedTuple` | No | Yes | Yes | Same as above, with full type-checker support. |
| `@dataclass` | Yes | No | Yes | Internal mutable data objects. |
| `@dataclass(frozen=True)` | No | Yes | Yes | Immutable objects needing full class features. |
| `Pydantic BaseModel` | No (by default) | No | Yes | API request/response validation and parsing. |

---

## **Modern Python Patterns**

### **Type Hints with Built-in `tuple` (3.9+)**

Before Python 3.9, you had to import `Tuple` from `typing`. From 3.9 onwards, the built-in `tuple` supports type parameters directly.

```python
# Old style (pre-3.9)
from typing import Tuple
def get_range(data: list) -> Tuple[int, int]:
    return min(data), max(data)

# Modern style (3.9+)
def get_range(data: list) -> tuple[int, int]:
    return min(data), max(data)
```

For a variable-length tuple of a single type:

```python
def process(scores: tuple[int, ...]) -> float:
    return sum(scores) / len(scores)
```

### **`match-case` with Tuple Patterns (3.10+)**

```python
def describe_point(point: tuple) -> str:
    match point:
        case (0, 0):
            return "origin"
        case (x, 0):
            return f"on x-axis at {x}"
        case (0, y):
            return f"on y-axis at {y}"
        case (x, y):
            return f"point at ({x}, {y})"

print(describe_point((0, 0)))    # origin
print(describe_point((5, 0)))    # on x-axis at 5
print(describe_point((3, 4)))    # point at (3, 4)
```

### **f-string Debug Mode (3.8+)**

```python
t = (85, 90, 78)
print(f"{t=}")        # t=(85, 90, 78)
print(f"{min(t)=}")   # min(t)=78
```

### **Older vs Modern Comparison**

| Pattern | Old Style | Modern Style (3.9–3.14) |
|---|---|---|
| Type hint | `Tuple[int, str]` from `typing` | `tuple[int, str]` built-in |
| Variable-length hint | `Tuple[int, ...]` | `tuple[int, ...]` |
| Named tuple | `collections.namedtuple(...)` | `class X(NamedTuple):` with type hints |
| Swap variables | `temp = a; a = b; b = temp` | `a, b = b, a` |
| Multi-return | `return (x, y)` | `return x, y` with `-> tuple[T, T]` hint |
| Structural match | `if isinstance(...)` chains | `match point: case (x, y):` |
| Immutable dataclass | Manual `__setattr__` | `@dataclass(frozen=True)` |

---

## **Quick Reference**

| Operation | Syntax | Notes |
|---|---|---|
| Create empty | `t = ()` | — |
| Create with elements | `t = (10, 20, 30)` | Parentheses recommended. |
| Create without parentheses | `t = 10, 20, 30` | Valid — packing. |
| Single element | `t = (10,)` | Trailing comma is mandatory. |
| From list | `tuple([1, 2, 3])` | — |
| From range | `tuple(range(0, 10, 2))` | — |
| Access by index | `t[i]`, `t[-1]` | `IndexError` if out of range. |
| Slice | `t[start:stop:step]` | No `IndexError` for out-of-range stop. |
| Length | `len(t)` | — |
| Count occurrences | `t.count(x)` | Returns `0` if not found. |
| Find index | `t.index(x)` | `ValueError` if absent — guard with `in`. |
| Min / Max | `min(t)`, `max(t)` | Built-in functions. |
| Sum | `sum(t)` | Built-in function. |
| Sort (returns list) | `sorted(t)` | Original tuple unchanged. |
| Concatenate | `t1 + t2` | Returns new tuple. |
| Repeat | `t * n` | Returns new tuple. |
| Unpack | `a, b, c = t` | Count must match. |
| Extended unpack | `first, *rest = t` | `rest` is a list. |
| Swap | `a, b = b, a` | Classic tuple trick. |
| As dict key | `d[(x, y)] = val` | Works because tuples are hashable. |
| Check membership | `x in t` | O(n) linear scan. |
| Convert to list | `list(t)` | To make it mutable. |
| Convert from list | `tuple(lst)` | To make it immutable. |
| Named tuple (typed) | `class X(NamedTuple): ...` | Preferred over `collections.namedtuple`. |
| Immutable dataclass | `@dataclass(frozen=True)` | Richer alternative to `NamedTuple`. |
| Tuple comprehension | `tuple(expr for x in it)` | No native syntax; wrap generator with `tuple()`. |