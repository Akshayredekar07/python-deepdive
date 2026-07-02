# **Python Dictionaries**

## **What Is a Dictionary?**

A dictionary is a collection of key-value pairs. If you want to represent a group of related objects together — where each item has a label (key) and a piece of data (value) — a dictionary is the right choice.

Real-world examples of key-value relationships:

- Roll number → student name
- Phone number → contact address
- IP address → domain name
- Product code → price

In other languages, this same concept goes by different names: **Map** in C++ and Java, **Hash** in Perl and Ruby.

---

## **Key Properties**

- Duplicate keys are not allowed. If you assign a new value to an existing key, it overwrites the old one.
- Values can be duplicated freely.
- Both keys and values can be of heterogeneous types (different types in the same dictionary).
- Dictionaries are **mutable** — you can add, remove, or update entries at any time.
- Dictionaries are **dynamic** — they grow and shrink as needed.
- Indexing and slicing (like on lists) are not applicable.
- Keys must be **immutable** — strings, numbers, and tuples are valid keys. Lists and dictionaries cannot be used as keys.
- Values can be of any type: numbers, strings, lists, sets, or even another dictionary.
- As of Python 3.7+, dictionaries maintain **insertion order**. Before 3.7, order was not guaranteed.

---

## **Creating a Dictionary**

### **Method 1 — Curly Braces `{}`**

```python
# Simple beginner example
scores = {"math": 88, "science": 92, "english": 75}
print(scores)  # {'math': 88, 'science': 92, 'english': 75}
```

### **Method 2 — `dict()` Constructor**

```python
employee = dict(name="Tanvi", role="analyst", department="finance")
print(employee)  # {'name': 'Tanvi', 'role': 'analyst', 'department': 'finance'}
```

### **Method 3 — Empty Dictionary**

```python
d = {}        # using curly braces
d = dict()    # using constructor
```

### **Method 4 — `fromkeys()` with Default Values**

`fromkeys()` creates a dictionary from an iterable of keys and assigns every key the same default value.

```python
fields = ["name", "age", "city"]
profile = dict.fromkeys(fields, None)
print(profile)  # {'name': None, 'age': None, 'city': None}

# Useful for initialising score sheets
subjects = ["math", "science", "english"]
marks = dict.fromkeys(subjects, 0)
print(marks)  # {'math': 0, 'science': 0, 'english': 0}
```

### **Method 5 — Adding Entries Incrementally**

```python
d = {}
d[101] = "Arjun"
d[102] = "Harsha"
d[103] = "Drishya"
print(d)  # {101: 'Arjun', 102: 'Harsha', 103: 'Drishya'}
```

---

## **Accessing Dictionary Values**

### **Method 1 — Square Brackets `dict[key]`**

```python
student = {"name": "Karan", "age": 21, "city": "Pune"}
print(student["name"])  # Karan
print(student["age"])   # 21
```

If the key does not exist, Python raises a `KeyError`:

```python
print(student["grade"])  # KeyError: 'grade'
```

### **Method 2 — `get()` Method (Safer)**

`get()` returns `None` if the key is missing, instead of raising an error. You can also provide a custom default value.

```python
print(student.get("name"))             # Karan
print(student.get("grade"))            # None  (no error)
print(student.get("grade", "N/A"))     # N/A
```

Use `get()` whenever the key might not exist — it prevents your program from crashing unexpectedly.

---

## **Modifying a Dictionary**

Dictionaries are mutable, so you can update existing values and add new key-value pairs at any time.

```python
student = {"name": "Rohit", "age": 20}

# Update an existing key
student["age"] = 21

# Add a new key-value pair
student["city"] = "Mumbai"

print(student)  # {'name': 'Rohit', 'age': 21, 'city': 'Mumbai'}
```

---

## **Removing Elements**

### **`del` Statement**

Removes a specific key. Raises `KeyError` if the key does not exist.

```python
student = {"name": "Durga", "age": 22, "city": "Nagpur"}
del student["city"]
print(student)  # {'name': 'Durga', 'age': 22}
```

### **`pop(key, default)`**

Removes the key and **returns its value**. You can supply a default to avoid a `KeyError` for missing keys.

```python
age = student.pop("age")
print(age)      # 22
print(student)  # {'name': 'Durga'}

# Safe removal with default
result = student.pop("grade", "not found")
print(result)   # not found
```

### **`popitem()`**

Removes and returns the **last inserted** key-value pair as a tuple. Useful when processing items from an ordered dictionary one at a time.

```python
product = {"id": "P001", "name": "notebook", "price": 120}
removed = product.popitem()
print(removed)   # ('price', 120)
print(product)   # {'id': 'P001', 'name': 'notebook'}
```

### **`clear()`**

Removes all key-value pairs from the dictionary, leaving it empty.

```python
product.clear()
print(product)  # {}
```

| Method | Returns | Raises KeyError? |
|---|---|---|
| `del d[key]` | Nothing | Yes, if key missing |
| `d.pop(key)` | Removed value | Yes, unless default given |
| `d.pop(key, default)` | Removed value or default | No |
| `d.popitem()` | `(key, value)` tuple | Yes, if dict is empty |
| `d.clear()` | Nothing | No |

---

## **Checking Key Existence**

```python
student = {"name": "Om", "age": 19}

print("name" in student)      # True
print("grade" in student)     # False
print("grade" not in student) # True
```

Always check key existence before accessing with `[]` if you are unsure whether the key is present.

---

## **Dictionary Length**

Use `len()` to count the number of key-value pairs.

```python
student = {"name": "Tanvi", "age": 22, "city": "Hyderabad"}
print(len(student))  # 3
```

---

## **Dictionary Methods**

### **`keys()`, `values()`, `items()`**

These three methods return **view objects** — they reflect changes to the dictionary in real time.

```python
student = {"name": "Harsha", "age": 23, "city": "Bangalore"}

print(student.keys())    # dict_keys(['name', 'age', 'city'])
print(student.values())  # dict_values(['Harsha', 23, 'Bangalore'])
print(student.items())   # dict_items([('name', 'Harsha'), ('age', 23), ('city', 'Bangalore')])
```

### **`update()`**

Merges another dictionary (or iterable of key-value pairs) into the current one. Existing keys are overwritten; new keys are added.

```python
profile = {"name": "Karan", "age": 25, "city": "Pune"}

# Add and update multiple keys at once
profile.update({"age": 26, "role": "engineer"})
print(profile)
# {'name': 'Karan', 'age': 26, 'city': 'Pune', 'role': 'engineer'}

# Update using a list of tuples
profile.update([("department", "backend"), ("city", "Chennai")])
print(profile)
# {'name': 'Karan', 'age': 26, 'city': 'Chennai', 'role': 'engineer', 'department': 'backend'}
```

### **`setdefault(key, default)`**

If the key exists, returns its current value without modifying the dictionary. If the key does not exist, inserts it with the given default value and returns that value.

```python
config = {"host": "localhost", "port": 5432}

# Key exists — returns existing value, no change
print(config.setdefault("host", "127.0.0.1"))  # localhost

# Key missing — inserts it and returns the default
print(config.setdefault("timeout", 30))        # 30
print(config)
# {'host': 'localhost', 'port': 5432, 'timeout': 30}
```

`setdefault()` is useful for building grouped structures — for example, grouping students by grade level without overwriting an existing group.

### **`copy()`**

Creates a **shallow copy** of the dictionary. Changes to the copy do not affect the original for top-level keys.

```python
original = {"name": "Arjun", "score": 88}
backup = original.copy()
backup["score"] = 95

print(original)  # {'name': 'Arjun', 'score': 88}
print(backup)    # {'name': 'Arjun', 'score': 95}
```

Note: For nested dictionaries, a shallow copy only copies the outer layer. Nested objects are still shared between original and copy. Use `copy.deepcopy()` when you need full independence.

---

## **Merging Dictionaries**

There are three main approaches. Modern code should prefer the `|` operator.

```python
defaults = {"theme": "light", "language": "en", "timeout": 30}
user_prefs = {"theme": "dark", "font_size": 14}

# Old approach — modifies defaults in place
defaults.update(user_prefs)

# Slightly better — unpacking (Python 3.5+)
merged = {**defaults, **user_prefs}

# Modern — union operator (Python 3.9+), returns a new dict, originals unchanged
merged = defaults | user_prefs
print(merged)
# {'theme': 'dark', 'language': 'en', 'timeout': 30, 'font_size': 14}

# In-place merge without creating a new dict
defaults |= user_prefs
```

When the same key appears in both dictionaries, the **right-hand operand wins** with `|`, just as with `update()`.

---

## **Iterating Over a Dictionary**

### **Iterating Over Keys**

```python
student = {"name": "Drishya", "age": 20, "city": "Kolkata"}

for key in student:
    print(key)
# name
# age
# city
```

### **Iterating Over Values**

```python
for value in student.values():
    print(value)
# Drishya
# 20
# Kolkata
```

### **Iterating Over Key-Value Pairs**

This is the most commonly used pattern when you need both keys and values.

```python
for key, value in student.items():
    print(f"{key}: {value}")
# name: Drishya
# age: 20
# city: Kolkata
```

### **Iterating with `enumerate()`**

Use `enumerate()` when you need a numbered list or need to track position.

```python
for index, (key, value) in enumerate(student.items(), start=1):
    print(f"{index}. {key} -> {value}")
# 1. name -> Drishya
# 2. age -> 20
# 3. city -> Kolkata
```

---

## **Dictionary Comprehension**

Dictionary comprehension is a concise way to build a dictionary from any iterable in a single line.

**Syntax:**

```python
new_dict = {key_expr: value_expr for item in iterable}
new_dict = {key_expr: value_expr for item in iterable if condition}
```

### **Basic Example**

```python
squares = {x: x**2 for x in range(1, 6)}
print(squares)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

### **With a Condition**

```python
even_squares = {x: x**2 for x in range(1, 11) if x % 2 == 0}
print(even_squares)  # {2: 4, 4: 16, 6: 36, 8: 64, 10: 100}
```

### **Transforming Values**

```python
roles = {"tanvi": "student", "rohit": "analyst", "arjun": "engineer"}
upper_roles = {name: role.upper() for name, role in roles.items()}
print(upper_roles)
# {'tanvi': 'STUDENT', 'rohit': 'ANALYST', 'arjun': 'ENGINEER'}
```

### **Swapping Keys and Values**

This works correctly only when all values are unique.

```python
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}
print(swapped)  # {1: 'a', 2: 'b', 3: 'c'}
```

### **Applied Example — Exam Score Lookup**

```python
names = ["Durga", "Karan", "Harsha", "Om"]
scores = [78, 92, 85, 61]

result = {name: score for name, score in zip(names, scores) if score >= 70}
print(result)  # {'Durga': 78, 'Karan': 92, 'Harsha': 85}
```

### **Nested Dictionary Comprehension**

```python
# Multiplication table using nested comprehension
tables = {x: {y: x * y for y in range(1, 6)} for x in range(1, 4)}
print(tables)
# {1: {1: 1, 2: 2, 3: 3, 4: 4, 5: 5},
#  2: {1: 2, 2: 4, 3: 6, 4: 8, 5: 10},
#  3: {1: 3, 2: 6, 3: 9, 4: 12, 5: 15}}
```

The above is equivalent to the more verbose loop version:

```python
tables = {}
for x in range(1, 4):
    inner = {}
    for y in range(1, 6):
        inner[y] = x * y
    tables[x] = inner
```

Both produce the same result. Comprehension is more readable for straightforward transformations.

---

## **Nested Dictionaries**

A nested dictionary is a dictionary where one or more values are themselves dictionaries.

### **Creating a Nested Dictionary**

```python
students = {
    "student1": {"name": "Tanvi", "age": 22, "city": "Pune"},
    "student2": {"name": "Rohit", "age": 21, "city": "Mumbai"},
}
print(students)
```

### **Accessing Nested Values**

Use multiple keys in sequence to drill down.

```python
print(students["student1"]["name"])  # Tanvi
print(students["student2"]["city"])  # Mumbai
```

### **Modifying a Nested Value**

```python
students["student1"]["city"] = "Nagpur"
print(students["student1"])
# {'name': 'Tanvi', 'age': 22, 'city': 'Nagpur'}
```

### **Adding a New Nested Entry**

```python
students["student3"] = {"name": "Arjun", "age": 23, "city": "Delhi"}
```

### **Removing a Nested Entry**

```python
del students["student2"]
print(students.keys())  # dict_keys(['student1', 'student3'])
```

### **Safely Accessing Deep Keys**

When you are not sure if a nested key exists, chain `get()` calls to avoid `KeyError`.

```python
grade = students.get("student1", {}).get("grade", "not set")
print(grade)  # not set
```

---

## **Dictionary vs Other Data Structures**

| Feature | List | Tuple | Set | Dictionary |
|---|---|---|---|---|
| Ordered | Yes (3.7+) | Yes | No | Yes (3.7+) |
| Mutable | Yes | No | Yes | Yes |
| Duplicates allowed | Yes | Yes | No | Keys: No, Values: Yes |
| Access by | Index | Index | Value | Key |
| Use when | Sequence of items | Fixed data | Unique items | Labeled data |

**When to choose a dictionary:**

- When data has a natural label (name, id, code) rather than a positional index.
- When you need fast lookups by a known key — dictionary access is O(1) on average.
- When you are modelling real-world records: users, products, configurations, API responses.

---

## **Modern Python Patterns**

### **`match-case` on Dictionaries (3.10+)**

Pattern matching lets you branch on the shape and content of a dictionary, which is much cleaner than long `if/elif` chains when handling structured data.

```python
def process_request(request: dict) -> str:
    match request:
        case {"method": "GET", "path": str(path)}:
            return f"Fetching resource at {path}"
        case {"method": "POST", "path": str(path), "body": dict(body)}:
            return f"Creating resource at {path} with {len(body)} fields"
        case {"method": "DELETE", "path": str(path)}:
            return f"Deleting resource at {path}"
        case _:
            return "Unknown request format"

print(process_request({"method": "GET", "path": "/students"}))
# Fetching resource at /students

print(process_request({"method": "POST", "path": "/students", "body": {"name": "Durga"}}))
# Creating resource at /students with 1 fields
```

### **`dataclass` as a Typed Alternative**

When a dictionary's keys are always the same and known at design time, a `dataclass` gives you type safety, IDE autocompletion, and cleaner access.

```python
from dataclasses import dataclass, asdict

@dataclass
class ExamResult:
    student: str
    subject: str
    score: int
    passed: bool = True

result = ExamResult(student="Harsha", subject="math", score=84)
print(result.student)         # Harsha
print(asdict(result))
# {'student': 'Harsha', 'subject': 'math', 'score': 84, 'passed': True}
```

`asdict()` converts the dataclass back to a plain dictionary, which is useful for serialisation.

### **`TypedDict` for Typed Dictionaries**

When you must use plain dictionaries (for example, JSON serialisation or API payloads), `TypedDict` adds type annotations without changing runtime behaviour.

```python
from typing import TypedDict

class StudentRecord(TypedDict):
    name: str
    age: int
    score: float

def process_record(record: StudentRecord) -> str:
    return f"{record['name']} scored {record['score']}"

data: StudentRecord = {"name": "Karan", "age": 20, "score": 91.5}
print(process_record(data))  # Karan scored 91.5
```

### **Walrus Operator `:=` in Lookups (3.8+)**

The walrus operator lets you assign and test a value in a single expression.

```python
config = {"retries": 5, "host": "db.internal"}

# Assign and check in one step
if timeout := config.get("timeout"):
    print(f"Timeout set to {timeout}s")
else:
    print("No timeout configured, using default")
# No timeout configured, using default
```

### **f-string Debug with `=` (3.8+)**

```python
product = {"id": "P042", "stock": 0}
stock = product.get("stock", -1)
print(f"{stock=}")  # stock=0  — prints the variable name alongside its value
```

### **Older vs Modern Comparison**

| Task | Older Style | Modern Style |
|---|---|---|
| Merge two dicts | `{**d1, **d2}` or `d1.update(d2)` | `d1 \| d2` (3.9+) |
| In-place merge | `d1.update(d2)` | `d1 \|= d2` (3.9+) |
| Branch on dict shape | `if "key" in d and isinstance(d["key"], ...)` | `match d: case {"key": type(val)}:` (3.10+) |
| Type hint value type | `Dict[str, int]` from `typing` | `dict[str, int]` natively (3.9+) |
| Structured dict | Plain dict with manual checks | `TypedDict` or `dataclass` |
| Debug print | `print("score =", score)` | `print(f"{score=}")` (3.8+) |

---

## **Common Mistakes**

### **1 — Using `[]` Instead of `get()` for Uncertain Keys**

```python
# Wrong — crashes if "grade" is absent
student = {"name": "Om", "age": 19}
print(student["grade"])  # KeyError: 'grade'

# Correct — returns a safe default
print(student.get("grade", "N/A"))  # N/A
```

### **2 — Mutating a Dictionary While Iterating Over It**

```python
scores = {"math": 45, "science": 72, "english": 38, "history": 80}

# Wrong — raises RuntimeError: dictionary changed size during iteration
for subject in scores:
    if scores[subject] < 50:
        del scores[subject]

# Correct — iterate over a copy of the keys
for subject in list(scores.keys()):
    if scores[subject] < 50:
        del scores[subject]

print(scores)  # {'science': 72, 'history': 80}
```

### **3 — Using a Mutable Type as a Key**

```python
# Wrong — lists are mutable and cannot be dictionary keys
lookup = {[1, 2]: "pair"}  # TypeError: unhashable type: 'list'

# Correct — use a tuple instead
lookup = {(1, 2): "pair"}
print(lookup[(1, 2)])  # pair
```

### **4 — Confusing Shallow Copy with Deep Copy**

```python
import copy

original = {"name": "Tanvi", "scores": [88, 92, 79]}

# Shallow copy — nested list is still shared
shallow = original.copy()
shallow["scores"].append(95)
print(original["scores"])  # [88, 92, 79, 95]  — original was changed!

# Correct — use deepcopy for nested structures
original = {"name": "Tanvi", "scores": [88, 92, 79]}
deep = copy.deepcopy(original)
deep["scores"].append(95)
print(original["scores"])  # [88, 92, 79]  — original is safe
```

### **5 — Assuming `dict.keys()` Returns a List**

```python
student = {"name": "Arjun", "age": 21}

keys = student.keys()

# Wrong assumption — dict_keys is not a list
keys.append("city")  # AttributeError: 'dict_keys' object has no attribute 'append'

# Correct — convert to list first if you need list behaviour
keys_list = list(student.keys())
keys_list.append("city")
print(keys_list)  # ['name', 'age', 'city']
```

### **6 — Overwriting an Existing Key Accidentally**

```python
# Wrong — both "id" keys resolve to the last value; first is silently lost
record = {"id": 101, "name": "Drishya", "id": 202}
print(record["id"])  # 202  — the first value is gone

# Correct — use distinct key names, or check before assigning
```

### **7 — Using `update()` When You Need a New Dict**

```python
base = {"theme": "light", "lang": "en"}
overrides = {"theme": "dark"}

# Wrong — modifies base in place, which may be unintended
base.update(overrides)

# Correct — use | to produce a new dictionary without touching the originals
merged = base | overrides
```

---

## **Production Patterns**

### **Counting Word Occurrences**

A classic use of `setdefault()` or `get()` with a default to build frequency maps.

```python
text = "the quick brown fox jumps over the lazy dog the fox"
frequency = {}

for word in text.split():
    frequency[word] = frequency.get(word, 0) + 1

print(frequency)
# {'the': 3, 'quick': 1, 'brown': 1, 'fox': 2, ...}
```

For larger volumes, `collections.Counter` is the production-grade tool:

```python
from collections import Counter

word_count = Counter(text.split())
print(word_count.most_common(3))
# [('the', 3), ('fox', 2), ('quick', 1)]
```

### **Grouping Records with `setdefault()`**

```python
students = [
    {"name": "Durga",  "grade": "A"},
    {"name": "Karan",  "grade": "B"},
    {"name": "Harsha", "grade": "A"},
    {"name": "Tanvi",  "grade": "C"},
    {"name": "Rohit",  "grade": "B"},
]

grouped = {}
for s in students:
    grouped.setdefault(s["grade"], []).append(s["name"])

print(grouped)
# {'A': ['Durga', 'Harsha'], 'B': ['Karan', 'Rohit'], 'C': ['Tanvi']}
```

### **API Response Handling (FastAPI Pattern)**

Dictionaries are the natural representation of JSON data received from or returned by an API. Using `TypedDict` makes the contract explicit.

```python
from typing import TypedDict

class ProductPayload(TypedDict):
    product_id: str
    name: str
    price: float
    in_stock: bool

def build_product_response(raw: dict) -> ProductPayload:
    return {
        "product_id": raw.get("id", "unknown"),
        "name": raw.get("name", "").strip(),
        "price": float(raw.get("price", 0)),
        "in_stock": raw.get("stock", 0) > 0,
    }

raw_data = {"id": "P101", "name": " Notebook ", "price": "149.99", "stock": 50}
response = build_product_response(raw_data)
print(response)
# {'product_id': 'P101', 'name': 'Notebook', 'price': 149.99, 'in_stock': True}
```

### **Configuration Layering**

A common pattern in CLIs and data pipelines: start with defaults, layer in environment-specific settings, then apply user overrides.

```python
defaults = {"log_level": "INFO", "max_retries": 3, "timeout": 30, "output": "stdout"}
env_config = {"log_level": "WARNING", "timeout": 60}
user_config = {"output": "report_2025.pdf"}

# Each layer overrides the previous one
final_config = defaults | env_config | user_config
print(final_config)
# {'log_level': 'WARNING', 'max_retries': 3, 'timeout': 60, 'output': 'report_2025.pdf'}
```

### **Pydantic v2 — Validated Dictionaries**

When dictionaries represent structured input (API bodies, config files), Pydantic adds runtime validation.

```python
from pydantic import BaseModel

class StudentModel(BaseModel):
    name: str
    age: int
    score: float

data = {"name": "Om", "age": 19, "score": 87.5}
student = StudentModel(**data)
print(student.model_dump())
# {'name': 'Om', 'age': 19, 'score': 87.5}
```

`model_dump()` (Pydantic v2) converts the model back to a plain dictionary for storage or serialisation.

### **Library Comparison**

When structured dictionaries grow complex, several libraries help manage them in production:

| Library | Key Feature | Best Use Case |
|---|---|---|
| `collections.Counter` | Frequency counting with `most_common()` | Word counts, event tallies, histograms |
| `collections.defaultdict` | Auto-initialises missing keys | Grouping, accumulating, graph adjacency lists |
| `collections.OrderedDict` | Explicit ordering and `move_to_end()` | LRU cache implementations, ordered queues |
| `Pydantic v2` | Runtime type validation from dict | API request/response models, config parsing |
| `dataclasses` | Type-safe struct with `asdict()` | Internal data records, pipeline stages |
| `TypedDict` | Type hints only, no runtime cost | Annotating existing dict-heavy code |

---

## **Quick Reference**

| Task | Code |
|---|---|
| Create with literals | `d = {"key": value}` |
| Create with constructor | `d = dict(key=value)` |
| Create from keys | `dict.fromkeys(keys, default)` |
| Access safely | `d.get("key", default)` |
| Add or update | `d["key"] = value` |
| Update many keys | `d.update(other_dict)` |
| Merge (new dict) | `d1 \| d2` |
| Merge in place | `d1 \|= d2` |
| Remove and return | `d.pop("key", default)` |
| Remove last item | `d.popitem()` |
| Remove key | `del d["key"]` |
| Clear all | `d.clear()` |
| Check key exists | `"key" in d` |
| All keys | `d.keys()` |
| All values | `d.values()` |
| All pairs | `d.items()` |
| Length | `len(d)` |
| Shallow copy | `d.copy()` |
| Deep copy | `copy.deepcopy(d)` |
| Default if missing | `d.setdefault("key", default)` |
| Loop keys | `for k in d:` |
| Loop values | `for v in d.values():` |
| Loop both | `for k, v in d.items():` |
| Comprehension | `{k: v for k, v in iterable}` |
| Comprehension + filter | `{k: v for k, v in iterable if condition}` |
| Pattern match dict | `match d: case {"key": val}:` |
| Type-annotate | `d: dict[str, int]` |
| Typed structure | `class R(TypedDict): field: type` |
| Debug print | `print(f"{value=}")` |