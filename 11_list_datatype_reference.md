# **Python Lists**

## **What is a List?**

If we want to represent a group of individual objects as a single entity where insertion order is preserved and duplicates are allowed, we should go for a List.

- Insertion order is preserved.
- Duplicate objects are allowed.
- Heterogeneous objects are allowed (numbers, strings, booleans, nested lists, etc.).
- Lists are dynamic — we can increase or decrease their size based on requirements.
- Elements are enclosed within square brackets `[]` and separated by commas.
- List objects are mutable, meaning their content can be changed after creation.

---

## **Indexing in Lists**

Duplicates can be differentiated using their index. Python supports both positive and negative indexing.

- Positive index: left to right, starting at `0`.
- Negative index: right to left, starting at `-1`.

For the list `[10, "A", "B", 20, 30, 10]`:

```
Element:        10    "A"   "B"   20    30    10
Positive Index:  0     1     2     3     4     5
Negative Index: -6    -5    -4    -3    -2    -1
```

---

## **Creating List Objects**

### **Empty List**

```python
items = []
print(items)        # []
print(type(items))  # <class 'list'>
```

### **List with Known Elements**

```python
scores = [85, 90, 78, 92]
print(scores)  # [85, 90, 78, 92]
```

### **List from a Range using Comprehension**

```python
evens = [i for i in range(0, 10, 2)]
print(evens)  # [0, 2, 4, 6, 8]
```

### **List from a String**

```python
name = "durga"
chars = [c for c in name]
print(chars)  # ['d', 'u', 'r', 'g', 'a']
```

### **List from split()**

`split()` breaks a string on whitespace (or a given separator) and returns each piece as a list element.

```python
sentence = "Python is easy to learn"
words = sentence.split()
print(words)       # ['Python', 'is', 'easy', 'to', 'learn']
print(type(words)) # <class 'list'>
```

> **Caution with `eval()`:** Using `eval(input(...))` to create a list from user input is an anti-pattern because it executes arbitrary code.
>
> ```python
> # WRONG — security risk
> items = eval(input("Enter list: "))
>
> # CORRECT — safe approach
> import ast
> items = ast.literal_eval(input("Enter list: "))
> ```

### **Nested Lists**

A list can contain another list as an element. Such lists are called nested lists.

```python
matrix = [10, 20, [30, 40]]
print(matrix[2])    # [30, 40]
print(matrix[2][0]) # 30
```

---

## **Accessing Elements of a List**

### **Using Index**

```python
marks = [88, 74, 95, 60]
print(marks[0])   # 88
print(marks[-1])  # 60
# print(marks[10])  # IndexError: list index out of range
```

### **Using Slice Operator**

Syntax: `list2 = list1[start:stop:step]`

- `start` — index where the slice begins (default `0`).
- `stop` — index where the slice ends, exclusive (default end of list).
- `step` — increment value (default `1`).

```python
n = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print(n[2:7:2])   # [3, 5, 7]
print(n[4::2])    # [5, 7, 9]
print(n[3:7])     # [4, 5, 6, 7]
print(n[8:2:-2])  # [9, 7, 5]
print(n[4:100])   # [5, 6, 7, 8, 9, 10]  — no IndexError for out-of-range stop
```

---

## **List Mutability**

Lists in Python are mutable, meaning their elements can be modified after creation.

```python
scores = [70, 80, 90, 65]
print(scores)  # [70, 80, 90, 65]

scores[1] = 95
print(scores)  # [70, 95, 90, 65]
```

---

## **Traversing a List**

### **Using a `while` Loop**

```python
cities = ["Pune", "Mumbai", "Nagpur", "Nashik"]
i = 0
while i < len(cities):
    print(cities[i])
    i += 1
```

### **Using a `for` Loop**

```python
cities = ["Pune", "Mumbai", "Nagpur", "Nashik"]
for city in cities:
    print(city)
```

### **Displaying Only Elements That Match a Condition**

```python
scores = [45, 88, 72, 55, 91, 38, 60]
for s in scores:
    if s >= 60:
        print(s)  # 88, 72, 91, 60
```

### **Displaying Elements with Both Index Types**

```python
subjects = ["Maths", "Science", "English"]
n = len(subjects)
for i in range(n):
    print(subjects[i], "— positive index:", i, "— negative index:", i - n)

# Maths — positive index: 0 — negative index: -3
# Science — positive index: 1 — negative index: -2
# English — positive index: 2 — negative index: -1
```

---

## **Important List Functions**

### **Getting Information**

#### `len()`

Returns the number of elements in a list.

```python
products = ["pen", "notebook", "eraser", "stapler"]
print(len(products))  # 4
```

#### `count()`

Returns the number of occurrences of a specified item.

```python
grades = ["A", "B", "A", "C", "A", "B"]
print(grades.count("A"))  # 3
print(grades.count("D"))  # 0
```

#### `index()`

Returns the index of the first occurrence of a specified item. Raises `ValueError` if the item is not found.

```python
grades = ["A", "B", "A", "C"]
print(grades.index("B"))  # 1
print(grades.index("A"))  # 0

# Always guard with `in` before calling index():
if "D" in grades:
    print(grades.index("D"))
else:
    print("D not found")
```

---

## **Manipulating Elements of a List**

### **`append()`**

Adds a single item to the end of the list.

```python
items = []
items.append("report_2025.pdf")
items.append("summary.docx")
items.append("data.csv")
print(items)  # ['report_2025.pdf', 'summary.docx', 'data.csv']
```

Build a list of multiples of 10:

```python
multiples = []
for i in range(101):
    if i % 10 == 0:
        multiples.append(i)
print(multiples)  # [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
```

### **`insert()`**

Inserts an item at a specified index position.

```python
ranks = [1, 2, 3, 4, 5]
ranks.insert(2, 99)   # inserts 99 at index 2
print(ranks)          # [1, 2, 99, 3, 4, 5]
```

Edge-case behaviour with out-of-range indices:

```python
n = [10, 20, 30]
n.insert(100, 999)   # index > max → appends to end
n.insert(-100, 111)  # index < min → inserts at beginning
print(n)             # [111, 10, 20, 30, 999]
```

### **`append()` vs `insert()` — Comparison**

| Feature | `append()` | `insert()` |
|---|---|---|
| Purpose | Adds an item to the end of the list. | Inserts an item at a specified index. |
| Parameters | Takes only one argument (the item). | Takes two arguments: index and item. |
| Positioning | Always adds at the end. | Can add an item anywhere in the list. |
| Use case | Extending the list at the end. | Precise positioning of elements. |

### **`extend()`**

Adds all items of one iterable to the end of the list. When a string is passed, each character is added individually.

```python
batch_a = ["Rohit", "Tanvi", "Karan"]
batch_b = ["Arjun", "Drishya"]
batch_a.extend(batch_b)
print(batch_a)  # ['Rohit', 'Tanvi', 'Karan', 'Arjun', 'Drishya']
```

```python
tags = ["python", "ml"]
tags.extend("nlp")       # string iterated character by character
print(tags)              # ['python', 'ml', 'n', 'l', 'p']

# CORRECT — use append or extend a list to add a word:
tags2 = ["python", "ml"]
tags2.append("nlp")
print(tags2)             # ['python', 'ml', 'nlp']
```

### **`remove()`**

Removes the first occurrence of a specified item. Raises `ValueError` if the item is not present.

```python
errors = ["404", "500", "404", "403"]
errors.remove("404")
print(errors)  # ['500', '404', '403']

# Guard before removing:
if "200" in errors:
    errors.remove("200")
```

### **`pop()`**

Removes and returns the last element by default, or an element at a specific index. Raises `IndexError` if the list is empty or the index is out of range.

```python
queue = [10, 20, 30, 40, 50]
print(queue.pop())   # 50
print(queue.pop(1))  # 20
print(queue)         # [10, 30, 40]
```

`append()` and `pop()` together implement a **stack (LIFO)**:

```python
stack = []
stack.append("task_a")
stack.append("task_b")
stack.append("task_c")
print(stack.pop())  # task_c  ← last in, first out
```

### **`remove()` vs `pop()` — Comparison**

| Feature | `remove()` | `pop()` |
|---|---|---|
| Removes by | Value (first occurrence). | Index (default: last element). |
| Return value | None. | The removed element. |
| Error raised | `ValueError` if element not found. | `IndexError` if list is empty or index out of range. |

### **`clear()`**

Removes all elements from the list, leaving it empty.

```python
session_data = ["user_id", "token", "cart"]
session_data.clear()
print(session_data)  # []
```

---

## **Ordering Elements**

### **`reverse()`**

Reverses the order of elements in place.

```python
rankings = [3, 1, 4, 1, 5, 9, 2, 6]
rankings.reverse()
print(rankings)  # [6, 2, 9, 5, 1, 4, 1, 3]
```

### **`sort()`**

Sorts elements in ascending order by default (numbers: ascending, strings: alphabetical). All elements must be of the same type.

```python
scores = [72, 55, 90, 38, 88]
scores.sort()
print(scores)  # [38, 55, 72, 88, 90]

cities = ["Pune", "Mumbai", "Delhi", "Bangalore"]
cities.sort()
print(cities)  # ['Bangalore', 'Delhi', 'Mumbai', 'Pune']
```

Sort in reverse order with `reverse=True`:

```python
scores = [72, 55, 90, 38, 88]
scores.sort(reverse=True)
print(scores)  # [90, 88, 72, 55, 38]
```

> **Note:** `sort()` requires all elements to be of the same type. Mixing types raises `TypeError`.
>
> ```python
> mixed = [10, "A", 20, "B"]
> mixed.sort()  # TypeError: '<' not supported between instances of 'str' and 'int'
> ```

---

## **Aliasing and Cloning**

### **Aliasing**

Assigning another reference variable to an existing list is called aliasing. Any change made through one reference reflects in the other because both point to the same object.

```python
original = [10, 20, 30, 40]
alias = original
print(id(original) == id(alias))  # True

alias[1] = 999
print(original)  # [10, 999, 30, 40]
print(alias)     # [10, 999, 30, 40]
```

### **Cloning**

Creating a duplicate independent object is called cloning. Changes to the clone do not affect the original.

**Using slice operator:**

```python
original = [10, 20, 30, 40]
clone = original[:]
clone[1] = 999
print(original)  # [10, 20, 30, 40]
print(clone)     # [10, 999, 30, 40]
```

**Using `copy()`:**

```python
original = [10, 20, 30, 40]
clone = original.copy()
clone[1] = 999
print(original)  # [10, 20, 30, 40]
print(clone)     # [10, 999, 30, 40]
```

> **Important — Shallow vs Deep Copy:**
> Both `[:]` and `copy()` are **shallow copies**. For nested lists, inner objects are still shared. Use `copy.deepcopy()` to fully decouple nested structures.
>
> ```python
> import copy
>
> original = [[1, 2], [3, 4]]
> shallow = original.copy()
> deep = copy.deepcopy(original)
>
> original[0][0] = 99
> print(shallow[0][0])  # 99  ← shared inner list
> print(deep[0][0])     # 1   ← fully independent
> ```

| Method | Type | Behaviour |
|---|---|---|
| `=` | Aliasing | Same object, changes reflected everywhere. |
| `[:]` or `.copy()` | Shallow clone | New outer list, inner objects still shared. |
| `copy.deepcopy()` | Deep clone | Fully independent copy at all nesting levels. |

---

## **Mathematical Operators on Lists**

### **Concatenation (`+`)**

Used to join two lists into a single new list. Both operands must be lists.

```python
part_a = [10, 20, 30]
part_b = [40, 50, 60]
combined = part_a + part_b
print(combined)  # [10, 20, 30, 40, 50, 60]

# WRONG — TypeError:
# combined = part_a + 40

# CORRECT:
combined = part_a + [40]
```

### **Repetition (`*`)**

Used to repeat a list's elements a specified number of times.

```python
template = [0, 0, 0]
row = template * 3
print(row)  # [0, 0, 0, 0, 0, 0, 0, 0, 0]
```

---

## **Comparing Lists**

### **Equality and Inequality (`==`, `!=`)**

Comparison checks the number of elements, their order, and their content (case-sensitive for strings).

```python
x = ["admin", "engineer", "analyst"]
y = ["admin", "engineer", "analyst"]
z = ["Admin", "Engineer", "Analyst"]

print(x == y)  # True
print(x == z)  # False  ← case-sensitive
print(x != z)  # True
```

### **Relational Operators (`<`, `<=`, `>`, `>=`)**

Lists are compared element by element from left to right. The result is determined at the first element that differs.

```python
x = [50, 20, 30]
y = [40, 50, 60]

print(x > y)   # True   ← 50 > 40, comparison stops here
print(x < y)   # False
```

String lists are compared lexicographically:

```python
a = ["banana", "apple"]
b = ["cherry", "apple"]
print(a < b)   # True  ← 'b' < 'c'
```

---

## **Membership Operators**

Used to check whether an element exists in a list.

- `in` returns `True` if the element is present.
- `not in` returns `True` if the element is absent.

```python
valid_roles = ["admin", "editor", "viewer"]

print("admin" in valid_roles)       # True
print("superuser" in valid_roles)   # False
print("superuser" not in valid_roles)  # True
```

Always use `in` before calling `index()` or `remove()` to avoid runtime errors.

---

## **Nested Lists as Matrices**

Nested lists can represent a 2D matrix where each inner list is a row.

```python
matrix = [[10, 20, 30], [40, 50, 60], [70, 80, 90]]

# Row-wise iteration:
for row in matrix:
    print(row)
# [10, 20, 30]
# [40, 50, 60]
# [70, 80, 90]

# Matrix-style iteration:
for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        print(matrix[i][j], end=" ")
    print()
# 10 20 30
# 40 50 60
# 70 80 90
```

Accessing a specific element uses double indexing `matrix[row][col]`:

```python
print(matrix[1][2])  # 60
```

---

## **List Comprehensions**

List comprehensions provide a concise way to create lists from iterables, optionally applying a filter condition.

**Syntax:**
```python
new_list = [expression for item in iterable if condition]
```

- `expression` — transformation applied to each item.
- `iterable` — source (range, list, string, etc.).
- `if condition` — optional filter.

### **Basic Examples**

```python
# Squares of 1 to 10
squares = [x * x for x in range(1, 11)]
print(squares)  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# Powers of 2
powers = [2 ** x for x in range(1, 6)]
print(powers)  # [2, 4, 8, 16, 32]

# Even squares only
even_sq = [x for x in squares if x % 2 == 0]
print(even_sq)  # [4, 16, 36, 64, 100]
```

### **Applied Examples**

```python
# First letter of each student name
students = ["Harsha", "Om", "Drishya", "Arjun"]
initials = [name[0] for name in students]
print(initials)  # ['H', 'O', 'D', 'A']
```

```python
# Elements in list_a that are NOT in list_b
batch_a = [10, 20, 30, 40]
batch_b = [30, 40, 50, 60]
only_in_a = [x for x in batch_a if x not in batch_b]
print(only_in_a)  # [10, 20]

# Common elements
common = [x for x in batch_a if x in batch_b]
print(common)  # [30, 40]
```

```python
# Uppercase word + its length
words = "the quick brown fox jumps over the lazy dog".split()
result = [[w.upper(), len(w)] for w in words]
print(result)
# [['THE', 3], ['QUICK', 5], ['BROWN', 5], ...]
```

---

## **Unique Vowels in a Word**

```python
vowels = ["a", "e", "i", "o", "u"]
word = input("Enter a word: ").lower()

found = []
for letter in word:
    if letter in vowels and letter not in found:
        found.append(letter)

print("Unique vowels —", found)
print(f"Count — {len(found)}")
```

---

## **Complete Method Reference**

| Method | Description |
|---|---|
| `append(item)` | Adds a single element to the end of the list. |
| `extend(iterable)` | Adds all elements of an iterable to the end of the list. |
| `insert(index, item)` | Inserts an element at the specified index. |
| `remove(item)` | Removes the first occurrence of the specified element. |
| `pop(index=-1)` | Removes and returns the element at the specified index (default last). |
| `clear()` | Removes all elements from the list. |
| `index(item)` | Returns the index of the first occurrence of the specified element. |
| `count(item)` | Returns how many times the specified element appears. |
| `sort(reverse=False)` | Sorts the list in ascending order (or descending if `reverse=True`). |
| `reverse()` | Reverses the elements of the list in place. |
| `copy()` | Returns a shallow copy of the list. |

```python
records = [10, 20, 30, 40, 50]

records.append(60)
print("append —", records)      # [10, 20, 30, 40, 50, 60]

records.extend([70, 80])
print("extend —", records)      # [10, 20, 30, 40, 50, 60, 70, 80]

records.insert(2, 25)
print("insert —", records)      # [10, 20, 25, 30, 40, 50, 60, 70, 80]

records.remove(40)
print("remove —", records)      # [10, 20, 25, 30, 50, 60, 70, 80]

popped = records.pop()
print("popped —", popped)       # 80
print("after pop —", records)   # [10, 20, 25, 30, 50, 60, 70]

print("index of 30 —", records.index(30))   # 3
print("count of 20 —", records.count(20))   # 1

records.sort()
print("sorted —", records)      # [10, 20, 25, 30, 50, 60, 70]

records.reverse()
print("reversed —", records)    # [70, 60, 50, 30, 25, 20, 10]

backup = records.copy()
print("copy —", backup)         # [70, 60, 50, 30, 25, 20, 10]

records.clear()
print("cleared —", records)     # []
```

---

## **Common Interview Questions and Answers**

### **Remove duplicates while preserving order**

```python
# Method 1 — dict.fromkeys() (fastest, preserves order from Python 3.7+)
original = [1, 2, 2, 3, 4, 4, 5]
unique = list(dict.fromkeys(original))
print(unique)  # [1, 2, 3, 4, 5]

# Method 2 — manual loop (more explicit)
seen = []
for item in original:
    if item not in seen:
        seen.append(item)
print(seen)  # [1, 2, 3, 4, 5]
```

### **Merge two lists into a list of tuples**

```python
ids = [101, 102, 103]
names = ["Rohit", "Tanvi", "Karan"]

paired = list(zip(ids, names))
print(paired)  # [(101, 'Rohit'), (102, 'Tanvi'), (103, 'Karan')]
```

`zip()` stops at the shorter list. Use `itertools.zip_longest()` to fill missing values:

```python
from itertools import zip_longest

ids = [101, 102, 103, 104]
names = ["Rohit", "Tanvi", "Karan"]

paired = list(zip_longest(ids, names, fillvalue="unknown"))
print(paired)
# [(101, 'Rohit'), (102, 'Tanvi'), (103, 'Karan'), (104, 'unknown')]
```

### **Sort a list of dictionaries by a key**

```python
employees = [
    {"name": "Harsha", "score": 88},
    {"name": "Om",     "score": 72},
    {"name": "Drishya","score": 95},
]

# Using lambda
sorted_emp = sorted(employees, key=lambda x: x["score"])
print(sorted_emp)

# Using operator.itemgetter (more efficient for large datasets)
from operator import itemgetter
sorted_emp = sorted(employees, key=itemgetter("score"), reverse=True)
print(sorted_emp)
```

Sort by multiple keys (name first, then score):

```python
sorted_multi = sorted(employees, key=itemgetter("name", "score"))
```

### **Flatten a nested list**

```python
nested = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]

# Method 1 — list comprehension
flat = [item for sublist in nested for item in sublist]
print(flat)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Method 2 — itertools.chain
from itertools import chain
flat = list(chain.from_iterable(nested))
print(flat)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### **Split a list into chunks**

```python
def chunked(lst, size):
    return [lst[i:i + size] for i in range(0, len(lst), size)]

data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print(chunked(data, 3))  # [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
```

### **Transpose a matrix (list of lists)**

```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed = [list(row) for row in zip(*matrix)]
print(transposed)
# [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
```

### **Find the most frequent element**

```python
from collections import Counter

grades = ["A", "B", "A", "C", "A", "B", "A"]
counter = Counter(grades)
print(counter.most_common(1))  # [('A', 4)]
```

### **Iterate over multiple lists simultaneously**

```python
names = ["Rohit", "Tanvi", "Arjun"]
marks = [85, 92, 78]

for name, mark in zip(names, marks):
    print(f"{name} scored {mark}")
```

### **Check if a list is empty**

```python
pending_tasks = []

# Pythonic way:
if not pending_tasks:
    print("No pending tasks.")

# Explicit way:
if len(pending_tasks) == 0:
    print("No pending tasks.")
```

### **Difference between `del`, `remove()`, and `pop()`**

| Operation | Removes by | Returns value | Raises on failure |
|---|---|---|---|
| `del lst[i]` | Index, no return. | No. | `IndexError`. |
| `remove(val)` | First matching value. | No. | `ValueError`. |
| `pop(i)` | Index, returns element. | Yes. | `IndexError`. |

---

## **Common Mistakes**

### **1. Shadowing the built-in `list` name**

```python
# WRONG
list = [10, 20, 30]
# list() built-in is now inaccessible

# CORRECT
items = [10, 20, 30]
```

### **2. Using `append()` to add a list (creates nesting instead of extending)**

```python
batch = [1, 2, 3]

# WRONG — adds the whole list as one element
batch.append([4, 5])
print(batch)  # [1, 2, 3, [4, 5]]

# CORRECT — adds individual elements
batch.extend([4, 5])
print(batch)  # [1, 2, 3, 4, 5]
```

### **3. Calling `index()` or `remove()` without checking membership first**

```python
scores = [80, 90, 70]

# WRONG — raises ValueError if element is missing
scores.remove(50)

# CORRECT
if 50 in scores:
    scores.remove(50)
```

### **4. Aliasing instead of cloning when a copy is needed**

```python
original = [10, 20, 30]

# WRONG — both point to the same object
backup = original
backup[0] = 999
print(original)  # [999, 20, 30]  ← unintended mutation

# CORRECT
backup = original.copy()
backup[0] = 999
print(original)  # [10, 20, 30]  ← original unchanged
```

### **5. Mutating a list while iterating over it**

```python
scores = [45, 88, 55, 72, 30, 91]

# WRONG — skips elements due to index shifting
for s in scores:
    if s < 60:
        scores.remove(s)
print(scores)  # [88, 72, 91]  ← may skip some elements silently

# CORRECT — iterate over a copy
for s in scores[:]:
    if s < 60:
        scores.remove(s)

# OR — build a new list with comprehension
scores = [s for s in scores if s >= 60]
```

### **6. Using `sort()` on a mixed-type list**

```python
mixed = [10, "A", 20, "B"]
mixed.sort()  # TypeError: '<' not supported between 'str' and 'int'

# CORRECT — ensure homogeneous types before sorting
numbers = [10, 20, 5, 1]
numbers.sort()  # [1, 5, 10, 20]
```

### **7. Forgetting that `sort()` and `reverse()` return `None`**

```python
items = [3, 1, 2]

# WRONG
sorted_items = items.sort()
print(sorted_items)  # None

# CORRECT — use sorted() if you need a new list
sorted_items = sorted(items)
print(sorted_items)  # [1, 2, 3]
print(items)         # [3, 1, 2]  ← unchanged
```

---

## **Production Patterns**

### **Collecting and Filtering Records in a Data Pipeline**

Lists are the default container when collecting rows from a CSV, database cursor, or API response before handing them off to a DataFrame or model.

```python
import csv

def load_valid_records(filepath: str, min_score: int = 50) -> list[dict]:
    records = []
    with open(filepath) as f:
        for row in csv.DictReader(f):
            score = int(row["score"])
            if score >= min_score:
                records.append({"name": row["name"], "score": score})
    return records

results = load_valid_records("exam_results.csv", min_score=60)
```

### **Batch Processing in ML Training**

```python
def create_batches(dataset: list, batch_size: int) -> list[list]:
    return [dataset[i:i + batch_size] for i in range(0, len(dataset), batch_size)]

samples = list(range(100))
batches = create_batches(samples, batch_size=16)
print(f"Total batches — {len(batches)}")
```

### **Using a List as a Task Queue in a CLI**

```python
task_queue: list[str] = []

def enqueue(task: str) -> None:
    task_queue.append(task)

def dequeue() -> str | None:
    return task_queue.pop(0) if task_queue else None
```

### **API Response Aggregation**

```python
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float
    in_stock: bool

def filter_available(products: list[Product], max_price: float) -> list[Product]:
    return [p for p in products if p.in_stock and p.price <= max_price]
```

### **Library Comparison for List-Like Collections**

| Library / Type | Key Feature | Best Use Case |
|---|---|---|
| `list` (built-in) | Ordered, mutable, general purpose. | Default container for most tasks. |
| `collections.deque` | O(1) append and pop from both ends. | Queues, sliding windows, BFS. |
| `numpy.ndarray` | Vectorised math, fixed type. | Numerical computation, ML features. |
| `pandas.Series` | Labelled 1-D array with rich indexing. | Tabular data columns and analysis. |
| `tuple` | Immutable sequence. | Fixed records, dict keys, unpacking. |

---

## **Modern Python Patterns**

### **Type Hints with Built-in Generics (3.9+)**

Before Python 3.9, you had to import `List` from `typing`. From 3.9 onwards, the built-in `list` supports type parameters directly.

```python
# Old style (pre-3.9)
from typing import List
def process(items: List[int]) -> List[str]:
    return [str(i) for i in items]

# Modern style (3.9+)
def process(items: list[int]) -> list[str]:
    return [str(i) for i in items]
```

### **Union Types with `|` (3.10+)**

```python
# Old style
from typing import Union, Optional
def find(items: list, target: Union[int, str]) -> Optional[int]:
    return items.index(target) if target in items else None

# Modern style
def find(items: list, target: int | str) -> int | None:
    return items.index(target) if target in items else None
```

### **Walrus Operator `:=` in List Processing (3.8+)**

The walrus operator assigns and tests in the same expression, which is useful when building lists from filtered computations.

```python
# Filter and capture scores that pass the threshold
raw = [45, 88, None, 72, None, 91, 38]
valid = [s for item in raw if (s := item) is not None and s >= 60]
print(valid)  # [88, 72, 91]
```

### **`match-case` for Dispatching on List Structure (3.10+)**

```python
def describe_batch(batch: list) -> str:
    match batch:
        case []:
            return "empty batch"
        case [single]:
            return f"single item — {single}"
        case [first, *rest]:
            return f"batch of {len(batch)}, starting with {first}"

print(describe_batch([]))             # empty batch
print(describe_batch([42]))           # single item — 42
print(describe_batch([10, 20, 30]))   # batch of 3, starting with 10
```

### **f-string Debug Mode (3.8+)**

```python
scores = [85, 92, 78]
total = sum(scores)
print(f"{scores=}")  # scores=[85, 92, 78]
print(f"{total=}")   # total=255
```

### **`dataclass` with List Fields**

```python
from dataclasses import dataclass, field

@dataclass
class ExamResult:
    student: str
    marks: list[int] = field(default_factory=list)

    @property
    def average(self) -> float:
        return sum(self.marks) / len(self.marks) if self.marks else 0.0

result = ExamResult(student="Harsha", marks=[85, 90, 78])
print(result.average)  # 84.33...
```

### **Older vs Modern Comparison**

| Pattern | Old Style | Modern Style (3.9–3.14) |
|---|---|---|
| Type hint | `List[int]` from `typing` | `list[int]` built-in |
| Optional type | `Optional[str]` | `str \| None` |
| Flatten | Manual nested loop | `list(chain.from_iterable(...))` |
| Dedup preserving order | Custom loop | `list(dict.fromkeys(...))` |
| Dispatch on structure | `if/elif` chains | `match-case` with sequence patterns |
| Debug printing | `print("scores:", scores)` | `print(f"{scores=}")` |
| Mutable default | `def f(items=[]):` (bug) | `def f(items=None): items = items or []` |

---

## **Quick Reference**

| Operation | Syntax | Notes |
|---|---|---|
| Create empty list | `items = []` | — |
| Create from range | `[x for x in range(n)]` | List comprehension |
| Access by index | `lst[i]`, `lst[-1]` | `IndexError` if out of range |
| Slice | `lst[start:stop:step]` | No `IndexError` for out-of-range stop |
| Add to end | `lst.append(x)` | Single element only |
| Add all from iterable | `lst.extend(iterable)` | Strings are iterated char by char |
| Insert at position | `lst.insert(i, x)` | Out-of-range index is silently clamped |
| Remove by value | `lst.remove(x)` | First occurrence, `ValueError` if absent |
| Remove by index | `lst.pop(i)` | Returns the removed element |
| Remove last | `lst.pop()` | Default index is `-1` |
| Clear | `lst.clear()` | Equivalent to `del lst[:]` |
| Length | `len(lst)` | — |
| Count occurrences | `lst.count(x)` | Returns `0` if not found |
| Find index | `lst.index(x)` | `ValueError` if not found — guard with `in` |
| Sort in place | `lst.sort()` | Returns `None` |
| Return sorted copy | `sorted(lst)` | Original unchanged |
| Reverse in place | `lst.reverse()` | Returns `None` |
| Shallow copy | `lst.copy()` or `lst[:]` | Inner objects still shared |
| Deep copy | `copy.deepcopy(lst)` | Fully independent |
| Check membership | `x in lst` | O(n) linear scan |
| Concatenate | `a + b` | Returns new list |
| Repeat | `lst * n` | Returns new list |
| Zip two lists | `list(zip(a, b))` | Stops at shorter list |
| Flatten nested | `[x for sub in lst for x in sub]` | One level deep |
| Deduplicate (ordered) | `list(dict.fromkeys(lst))` | Preserves insertion order |
| Most frequent | `Counter(lst).most_common(1)` | From `collections` |
| Chunked batches | `[lst[i:i+n] for i in range(0,len(lst),n)]` | — |
| Transpose matrix | `[list(r) for r in zip(*matrix)]` | — |