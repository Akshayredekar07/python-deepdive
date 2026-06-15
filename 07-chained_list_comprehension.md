# **Chained List Comprehension**

## **What is a List Comprehension?**

A **list comprehension** is a concise way to create lists in Python using a single line of code instead of traditional `for` loops.

- Syntax: `[expression for item in iterable]`
- Introduced in Python 2.0; fully supported in all Python 3.x versions.
- Produces a new list without modifying the original iterable.

**Why list comprehensions are preferred:**

A traditional loop needs 4–5 lines to build a new list. A comprehension does the same in one line:

```python
# Traditional approach
squares = []
for n in range(1, 6):
    squares.append(n ** 2)

# List comprehension — same result
squares = [n ** 2 for n in range(1, 6)]
```

---

## Chaining in List Comprehension

### What is Chaining?

Chaining means nesting **multiple `for` clauses** inside a single list comprehension to iterate over more than one iterable at the same time — similar to writing nested `for` loops.

```python
# Syntax
[expression for var1 in iterable1 for var2 in iterable2]
```

This is equivalent to:

```python
result = []
for var1 in iterable1:
    for var2 in iterable2:
        result.append(expression)
```

---

## Examples

### Basic Example — Combining Two Lists

```python
# Traditional nested loop
colors = ["red", "green", "blue"]
sizes = ["S", "M", "L"]

combinations = []
for color in colors:
    for size in sizes:
        combinations.append((color, size))

# Chained list comprehension
combinations = [(color, size) for color in colors for size in sizes]

print(combinations)
# [('red', 'S'), ('red', 'M'), ('red', 'L'),
#  ('green', 'S'), ('green', 'M'), ('green', 'L'),
#  ('blue', 'S'), ('blue', 'M'), ('blue', 'L')]
```

---

### Flattening a Nested List

```python
# Traditional approach
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = []
for row in matrix:
    for num in row:
        flat.append(num)

# Chained list comprehension
flat = [num for row in matrix for num in row]

print(flat)
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

---

### Generating Coordinate Pairs

```python
# All (x, y) pairs where x and y are from 0 to 2
coords = [(x, y) for x in range(3) for y in range(3)]

print(coords)
# [(0, 0), (0, 1), (0, 2),
#  (1, 0), (1, 1), (1, 2),
#  (2, 0), (2, 1), (2, 2)]
```

---

### Chaining with a Condition (Filtered Pairs)

```python
# Pairs where x != y
pairs = [(x, y) for x in range(4) for y in range(4) if x != y]

print(pairs)
# [(0, 1), (0, 2), (0, 3),
#  (1, 0), (1, 2), (1, 3),
#  (2, 0), (2, 1), (2, 3),
#  (3, 0), (3, 1), (3, 2)]
```

---

### Multiplication Table

```python
# Traditional nested loop
table = []
for i in range(1, 4):
    for j in range(1, 4):
        table.append(i * j)

# Chained list comprehension
table = [i * j for i in range(1, 4) for j in range(1, 4)]

print(table)
# [1, 2, 3, 2, 4, 6, 3, 6, 9]
```

---

### Extracting Characters from Multiple Words

```python
words = ["Python", "Java", "C++"]

# Extract every character from every word
chars = [ch for word in words for ch in word]

print(chars)
# ['P', 'y', 't', 'h', 'o', 'n', 'J', 'a', 'v', 'a', 'C', '+', '+']
```

---

### Three-Level Chaining

```python
# 3D coordinates
points = [(x, y, z) for x in range(2) for y in range(2) for z in range(2)]

print(points)
# [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
#  (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
```

---

## Order of Execution

The `for` clauses in a chained comprehension execute **left to right**, just like nested `for` loops written top to bottom.

```python
# Reading order matches execution order
[expr for a in A for b in B for c in C]

# Equivalent to:
for a in A:
    for b in B:
        for c in C:
            result.append(expr)
```

**Quick reference — valid vs invalid chaining:**

| Expression | Valid? | Notes |
|---|---|---|
| `[x for x in range(5)]` | Yes | Single loop |
| `[x+y for x in A for y in B]` | Yes | Two-level chain |
| `[x for x in A for y in B if x != y]` | Yes | Chain with condition |
| `[x for x in A] for y in B` | No | Second `for` outside brackets |
| `[x+y for (x, y) in zip(A, B)]` | Yes | Unpacking inside comprehension |

---

## Chaining vs Nesting

Chaining uses multiple `for` in **one** comprehension (flat). Nesting uses a comprehension **inside** another comprehension (produces nested lists).

```python
A = [1, 2, 3]
B = [4, 5, 6]

# Chained — produces a flat list
flat = [x + y for x in A for y in B]
print(flat)   # [5, 6, 7, 6, 7, 8, 7, 8, 9]

# Nested — produces a list of lists
nested = [[x + y for y in B] for x in A]
print(nested)  # [[5, 6, 7], [6, 7, 8], [7, 8, 9]]
```

---

## Data Types Summary

| Concept | Description | Example |
|---|---|---|
| Single comprehension | One `for` clause | `[x**2 for x in range(5)]` |
| Chained comprehension | Multiple `for` clauses, flat output | `[x+y for x in A for y in B]` |
| Nested comprehension | Comprehension inside comprehension | `[[x+y for y in B] for x in A]` |
| Filtered chain | Chain with `if` condition | `[(x,y) for x in A for y in B if x!=y]` |
| Three-level chain | Three `for` clauses | `[(x,y,z) for x in X for y in Y for z in Z]` |

---

## Limitations of Chaining

- Too many chained `for` clauses reduce readability — prefer traditional nested loops beyond 2–3 levels.
- The inner iterable can reference the outer variable (e.g., `for j in row` where `row` comes from the outer `for`), but the reverse is not allowed.

```python
# Valid — inner iterable uses outer variable
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [num for row in matrix for num in row]   # OK

# Invalid — outer cannot reference inner
# flat = [num for num in row for row in matrix]  # NameError: row is not defined
```