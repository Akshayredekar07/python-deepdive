# **Python Flow Control**

## **Introduction**

Flow control describes the order in which Python executes statements at runtime. By default Python runs line by line from top to bottom, but flow control structures let you branch, repeat, and skip logic based on conditions.

Python's flow control is divided into three categories:

| Category                  | Statements                          |
|---------------------------|-------------------------------------|
| Conditional Statements    | `if`, `if-else`, `if-elif-else`     |
| Iterative Statements      | `for`, `while`                      |
| Transfer Statements       | `break`, `continue`, `pass`         |

---

## **Conditional Statements**

Conditional statements execute different blocks of code depending on whether a condition evaluates to `True` or `False`.

---

### **`if` Statement**

The `if` block runs only when its condition is `True`. If the condition is `False`, the block is skipped entirely.

**Syntax:**
```python
if condition:
    statement
```

```python
name = input("Enter Name: ")
if name == "durga":
    print("Hello Durga Good Morning")
print("How are you!!!")

# Input: durga  → Hello Durga Good Morning \n How are you!!!
# Input: Ravi   → How are you!!!
```

---

### **`if-else` Statement**

The `if-else` statement always runs one of two branches — `Action-1` when the condition is `True`, and `Action-2` otherwise.

**Syntax:**
```python
if condition:
    Action-1
else:
    Action-2
```

```python
name = input("Enter Name: ")
if name == "durga":
    print("Hello Durga Good Morning")
else:
    print("Hello Guest Good Morning")
print("How are you!!!")
```

---

### **`if-elif-else` Statement**

Used when you have more than two possible branches. Python evaluates each condition in order and executes the first `True` block. The `else` block is optional and acts as a fallback.

**Syntax:**
```python
if condition1:
    Action-1
elif condition2:
    Action-2
elif condition3:
    Action-3
else:
    Default Action
```

```python
day = input("Enter day of the week: ")
if day.lower() == "monday":
    print("Start of the work week!")
elif day.lower() == "friday":
    print("Almost the weekend!")
elif day.lower() in ("saturday", "sunday"):
    print("It is the weekend!")
else:
    print("It is a regular workday.")
```

**Notes:**
- The `else` block in any `if-elif-else` chain is optional.
- Python does not have a `switch` statement — use `if-elif-else` for multiple branches, or `match-case` (Python 3.10+) for structural dispatch.
- Valid forms are: `if`, `if-else`, `if-elif`, and `if-elif-else`.

---

### **Practice Programs**

**Find the bigger of two numbers:**
```python
n1 = int(input("Enter First Number: "))
n2 = int(input("Enter Second Number: "))

if n1 > n2:
    print("Biggest Number is:", n1)
else:
    print("Biggest Number is:", n2)
```

**Find the biggest of three numbers:**
```python
n1 = int(input("Enter First Number: "))
n2 = int(input("Enter Second Number: "))
n3 = int(input("Enter Third Number: "))

if n1 > n2 and n1 > n3:
    print("Biggest Number is:", n1)
elif n2 > n3:
    print("Biggest Number is:", n2)
else:
    print("Biggest Number is:", n3)
```

**Check if a number is between 1 and 10:**
```python
n = int(input("Enter Number: "))
if 1 <= n <= 10:   # chained comparison — more readable than n >= 1 and n <= 10
    print(f"The number {n} is between 1 and 10")
else:
    print(f"The number {n} is not between 1 and 10")
```

**Convert a single digit to its English word:**
```python
n = int(input("Enter a digit from 0 to 9: "))

if n == 0:
    print("ZERO")
elif n == 1:
    print("ONE")
elif n == 2:
    print("TWO")
elif n == 3:
    print("THREE")
elif n == 4:
    print("FOUR")
elif n == 5:
    print("FIVE")
elif n == 6:
    print("SIX")
elif n == 7:
    print("SEVEN")
elif n == 8:
    print("EIGHT")
elif n == 9:
    print("NINE")
else:
    print("Please enter a digit from 0 to 9")
```

---

### **Modern Pattern — `match-case` (Python 3.10+)**

Python 3.10 introduced `match-case` via PEP 634 — structural pattern matching. It is more powerful than a switch statement because it can simultaneously match and destructure values, eliminating chains of `isinstance()` checks, dictionary key tests, and manual tuple unpacking.

```python
# Old way — verbose if-elif chain
def http_label_old(code: int) -> str:
    if code == 200:
        return "OK"
    elif code == 201:
        return "Created"
    elif code == 404:
        return "Not Found"
    elif code == 500:
        return "Internal Server Error"
    else:
        return "Unknown"

# Modern way — match-case with guard and OR patterns
def http_label(code: int) -> str:
    match code:
        case 200:
            return "OK"
        case 201:
            return "Created"
        case 400 | 401 | 403:
            return "Client Error"
        case 404:
            return "Not Found"
        case code if code >= 500:
            return f"Server Error — {code}"
        case _:
            return "Unknown"

print(http_label(201))   # Created
print(http_label(403))   # Client Error
print(http_label(503))   # Server Error — 503
```

**Matching dictionary structure — common in API/event handling:**
```python
def handle_event(event: dict) -> str:
    match event:
        case {"type": "login", "user": str(name)}:
            return f"User {name} logged in"
        case {"type": "purchase", "item": str(item), "price": float(price)}:
            return f"Purchase — {item} at ₹{price:.2f}"
        case {"type": "error", "code": int(code)} if code >= 500:
            return f"Critical server error — code {code}"
        case {"type": "error", "code": int(code)}:
            return f"Client-side error — code {code}"
        case _:
            return "Unrecognized event"

print(handle_event({"type": "login", "user": "Harsha"}))
# User Harsha logged in

print(handle_event({"type": "error", "code": 503}))
# Critical server error — code 503
```

**Production note:** Always include a wildcard `case _:` as the last case. Unmatched values silently fall through with no error, which is almost never what you want in production code.

---

### **Production Example — FastAPI Route Handler with Conditional Logic**

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class InferenceRequest:
    model: str
    task: Literal["classify", "embed", "generate"]
    text: str

def route_request(req: InferenceRequest) -> dict:
    if req.model not in {"gpt-4o", "claude-sonnet", "gemini-pro"}:
        return {"error": f"Unsupported model: {req.model}"}

    if req.task == "classify":
        return {"task": "classify", "result": f"Running classifier on: {req.text[:30]}"}
    elif req.task == "embed":
        return {"task": "embed", "dims": 1536, "text_len": len(req.text)}
    elif req.task == "generate":
        return {"task": "generate", "output": f"Generated response for: {req.text[:30]}"}
    else:
        return {"error": "Unknown task"}

req = InferenceRequest(model="claude-sonnet", task="embed", text="What is RAG?")
print(route_request(req))
# {'task': 'embed', 'dims': 1536, 'text_len': 11}
```

---

## **Iterative Statements**

Iterative (loop) statements let you execute a block of code multiple times without rewriting it.

---

### **`for` Loop**

The `for` loop iterates over every element in a sequence (string, list, tuple, range, etc.) and executes the body once per element.

**Syntax:**
```python
for variable in sequence:
    body
```

**Iterate over a string:**
```python
for char in "durga":
    print(char)
# d u r g a  (each on its own line)
```

**Iterate with index using `enumerate` (modern, preferred over manual counter):**
```python
s = "Pune"
for i, char in enumerate(s):
    print(f"Index {i} — {char}")
# Index 0 — P
# Index 1 — u
# Index 2 — n
# Index 3 — e
```

**Using `range()`:**
```python
# Print Hello 10 times
for _ in range(10):
    print("Hello")

# Numbers 0 to 10
for x in range(11):
    print(x)

# Odd numbers from 1 to 19
for x in range(1, 20, 2):
    print(x)

# Countdown from 10 to 1
for x in range(10, 0, -1):
    print(x)
```

**`range(start, stop, step)` reference:**

| Call                 | Produces                      |
|----------------------|-------------------------------|
| `range(5)`           | 0, 1, 2, 3, 4                 |
| `range(1, 6)`        | 1, 2, 3, 4, 5                 |
| `range(0, 10, 2)`    | 0, 2, 4, 6, 8                 |
| `range(10, 0, -1)`   | 10, 9, 8, ..., 1              |

**Sum of a list:**
```python
totals = [10, 20, 30, 40]
total = 0
for item in totals:
    total += item
print("Sum —", total)   # 100

# Modern one-liner with built-in
print("Sum —", sum(totals))  # 100
```

---

### **`while` Loop**

The `while` loop runs as long as its condition stays `True`. Use it when the number of iterations is not known in advance.

**Syntax:**
```python
while condition:
    body
```

**Print numbers 1 to 10:**
```python
x = 1
while x <= 10:
    print(x)
    x += 1
```

**Sum of first n numbers:**
```python
n = int(input("Enter number: "))
total = 0
i = 1
while i <= n:
    total += i
    i += 1
print(f"Sum of first {n} numbers — {total}")
```

**Retry until valid input:**
```python
name = ""
while name != "durga":
    name = input("Enter Name: ")
print("Thanks for confirmation")
```

**Infinite loop with manual break:**
```python
i = 0
while True:
    i += 1
    print(f"Heartbeat ping #{i}")
    if i == 5:
        break
```

---

### **`for` vs `while` — When to Use Which**

| Scenario                                      | Preferred Loop |
|-----------------------------------------------|----------------|
| Iterating over a list, string, or range       | `for`          |
| Unknown number of iterations (retry, polling) | `while`        |
| Reading input until a sentinel value          | `while`        |
| Processing each item in a batch               | `for`          |
| Infinite background loop (server, agent)      | `while True`   |

---

### **Nested Loops**

A loop inside another loop is called a nested loop. The inner loop completes all its iterations for every single iteration of the outer loop.

```python
for i in range(3):
    for j in range(3):
        print(f"i={i}  j={j}")
```

**Right-angled triangle of stars:**
```python
n = int(input("Enter number of rows: "))
for i in range(1, n + 1):
    print("* " * i)
```

**Pyramid of stars:**
```python
n = int(input("Enter number of rows: "))
for i in range(1, n + 1):
    print(" " * (n - i) + "* " * i)
```

Output for `n=5`:
```
*
* *
* * *
* * * *
* * * * *
```

---

## **Transfer Statements**

Transfer statements alter the normal execution flow of a loop.

---

### **`break`**

`break` immediately exits the loop, regardless of whether the loop condition is still `True`. Only the innermost loop is exited.

```python
for i in range(10):
    if i == 7:
        print("Reached 7 — stopping early")
        break
    print(i)
# Prints 0 through 6, then stops
```

---

### **`continue`**

`continue` skips the rest of the current iteration and moves to the next one. The loop itself does not stop.

**Print only odd numbers:**
```python
for i in range(10):
    if i % 2 == 0:
        continue
    print(i)   # 1 3 5 7 9
```

**Filter items above a threshold:**
```python
cart = [10, 20, 500, 700, 50, 60]
for item in cart:
    if item >= 500:
        print(f"Cannot process item: {item}")
        continue
    print(f"Processing: {item}")
```

---

### **`pass`**

`pass` is a no-op placeholder. Python requires at least one statement inside any block (`if`, `for`, `while`, function, class) — `pass` fills that requirement without doing anything.

```python
for i in range(100):
    if i % 9 == 0:
        print(i)
    else:
        pass   # nothing to do for non-multiples of 9
```

`pass` is also common when stubbing out functions or classes during development:

```python
class EmbeddingService:
    pass   # to be implemented later

def validate_token(token: str) -> bool:
    pass   # placeholder — will add JWT validation
```

---

### **`else` Clause on Loops**

Python's loops support an `else` block that runs only if the loop completed without hitting a `break`. This is a unique Python feature with no equivalent in most other languages.

```python
cart = [10, 20, 30, 40, 50]
for item in cart:
    if item >= 500:
        print("Cannot process — item too expensive")
        break
    print(f"Processed: {item}")
else:
    print("All items processed successfully")
# Since no item >= 500, the else block runs
```

**Practical use — search with fallback:**
```python
def find_admin(users: list[dict]) -> str:
    for user in users:
        if user["role"] == "admin":
            return f"Admin found — {user['name']}"
    else:
        return "No admin found in this group"

team = [
    {"name": "Rohit", "role": "engineer"},
    {"name": "Tanvi", "role": "manager"},
]
print(find_admin(team))   # No admin found in this group
```

---

### **`del` Statement**

`del` removes a variable from the current scope. After deletion, accessing the variable raises a `NameError`.

```python
x = 10
print(x)   # 10
del x
# print(x)   # NameError: name 'x' is not defined
```

**`del` vs assigning `None`:**

```python
# del — removes the variable entirely from scope
s = "durgasoft"
del s
# s is gone — NameError if accessed

# None — variable still exists, object is eligible for garbage collection
s = "durgasoft"
s = None
print(s)   # None — variable still accessible
```

- Use `del` when you want to explicitly free a large object from memory (e.g., a big list or model weights dict) during a long-running process.
- You cannot delete individual characters from an immutable string: `del s[0]` raises a `TypeError`.

---

## **Production Patterns and Modern Idioms**

### **Early Return Pattern (Replaces Deep Nesting)**

Deeply nested `if-else` blocks are hard to read and maintain. The early return pattern checks for invalid states first and returns immediately, keeping the happy path at the lowest indentation level.

```python
# Hard to read — pyramid of doom
def process_embedding_request(payload: dict) -> dict:
    if payload:
        if "text" in payload:
            if len(payload["text"]) > 0:
                if len(payload["text"]) <= 8192:
                    return {"status": "ok", "length": len(payload["text"])}
                else:
                    return {"error": "Text too long"}
            else:
                return {"error": "Empty text"}
        else:
            return {"error": "Missing text field"}
    else:
        return {"error": "Empty payload"}

# Clean — early return / guard clause pattern
def process_embedding_request(payload: dict) -> dict:
    if not payload:
        return {"error": "Empty payload"}
    if "text" not in payload:
        return {"error": "Missing text field"}
    if not payload["text"]:
        return {"error": "Empty text"}
    if len(payload["text"]) > 8192:
        return {"error": "Text too long"}
    return {"status": "ok", "length": len(payload["text"])}
```

---

### **Iterating with `enumerate` and `zip`**

Avoid manual counter variables in loops. Python's built-ins handle this cleanly.

```python
# Manual counter — old style
documents = ["intro.pdf", "chapter1.pdf", "chapter2.pdf"]
i = 0
for doc in documents:
    print(i, doc)
    i += 1

# enumerate — idiomatic Python
for i, doc in enumerate(documents, start=1):
    print(f"{i}. {doc}")

# zip — iterate two lists together
chunks = ["chunk_a", "chunk_b", "chunk_c"]
scores = [0.91, 0.87, 0.75]

for chunk, score in zip(chunks, scores):
    print(f"Score {score:.2f} — {chunk}")
```

---

### **List Comprehension — Replacing Simple `for` Loops**

When a `for` loop builds a list, a list comprehension is more readable and faster.

```python
# Traditional for loop building a list
scores = [88, 45, 92, 61, 77, 55, 90]
passing = []
for s in scores:
    if s >= 60:
        passing.append(s)

# List comprehension — one line, same result
passing = [s for s in scores if s >= 60]
print(passing)   # [88, 92, 61, 77, 90]

# With transformation
normalized = [round(s / 100, 2) for s in scores]
print(normalized)   # [0.88, 0.45, 0.92, 0.61, 0.77, 0.55, 0.9]
```

---

### **Production Example — Batch Processing with `continue` and `break`**

This pattern appears in data ingestion pipelines, RAG document processors, and ETL jobs.

```python
from dataclasses import dataclass

@dataclass
class Document:
    doc_id: str
    text: str
    size_kb: float

def ingest_batch(docs: list[Document], max_size_kb: float = 100.0) -> dict:
    processed = []
    skipped = []
    errors = []

    for doc in docs:
        if not doc.text.strip():
            skipped.append(doc.doc_id)
            continue   # skip empty documents

        if doc.size_kb > max_size_kb:
            errors.append({"id": doc.doc_id, "reason": "exceeds size limit"})
            continue   # skip oversized documents

        processed.append(doc.doc_id)

    return {
        "processed": processed,
        "skipped": skipped,
        "errors": errors,
    }

batch = [
    Document("doc_001", "Introduction to RAG systems", 12.5),
    Document("doc_002", "", 0.1),                          # empty
    Document("doc_003", "LangGraph multi-agent design", 250.0),  # too large
    Document("doc_004", "Milvus vector indexing guide", 45.0),
]

result = ingest_batch(batch)
print(result)
# {
#   'processed': ['doc_001', 'doc_004'],
#   'skipped': ['doc_002'],
#   'errors': [{'id': 'doc_003', 'reason': 'exceeds size limit'}]
# }
```

---

### **Production Example — Polling Loop with `while` and Exponential Backoff**

Retry loops with backoff are standard in API clients, health checks, and async job polling.

```python
import time

def poll_job_status(job_id: str, max_retries: int = 5) -> str:
    attempt = 0
    wait = 1   # start with 1 second

    while attempt < max_retries:
        # Simulate API call — replace with real HTTP call
        status = "pending" if attempt < 3 else "complete"
        print(f"Attempt {attempt + 1} — status: {status}")

        if status == "complete":
            return f"Job {job_id} finished successfully"
        if status == "failed":
            return f"Job {job_id} failed — aborting"

        time.sleep(wait)
        wait *= 2          # exponential backoff: 1s, 2s, 4s, 8s...
        attempt += 1

    return f"Job {job_id} — timed out after {max_retries} attempts"

print(poll_job_status("embed_job_42"))
```

---

### **Production Example — Generator with `for` Loop (Memory-Efficient Streaming)**

Instead of loading all records into a list, a generator yields one item at a time. This is essential when processing large datasets or chunking documents for vector stores.

```python
from typing import Generator

def chunk_text(text: str, chunk_size: int = 512) -> Generator[str, None, None]:
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i : i + chunk_size])

document = "word " * 2000   # simulate a large document

for idx, chunk in enumerate(chunk_text(document, chunk_size=512)):
    print(f"Chunk {idx} — {len(chunk.split())} words")
    # In production: send each chunk to embedding model here
```

---

## **Common Mistakes**

### **Mistake 1 — Mutating a List While Iterating Over It**

```python
items = [1, 2, 3, 4, 5]

# Wrong — skips elements unpredictably
for item in items:
    if item % 2 == 0:
        items.remove(item)

# Correct — iterate over a copy
for item in items[:]:
    if item % 2 == 0:
        items.remove(item)

# Most Pythonic — list comprehension
items = [item for item in items if item % 2 != 0]
print(items)   # [1, 3, 5]
```

### **Mistake 2 — Using `range(len(...))` Instead of Direct Iteration**

```python
models = ["llama3", "mistral", "gemma"]

# Old style — unnecessary index access
for i in range(len(models)):
    print(models[i])

# Idiomatic Python — iterate directly
for model in models:
    print(model)

# When you need the index — use enumerate
for i, model in enumerate(models):
    print(f"{i}: {model}")
```

### **Mistake 3 — Forgetting `break` Makes the `else` Block Not Run**

```python
items = [10, 20, 600, 30]

for item in items:
    if item > 500:
        print(f"Rejected — {item}")
        break
else:
    # This does NOT run because break was hit
    print("All items OK")
```

The `else` block only executes when the loop finishes naturally (without `break`). This is a common source of logic bugs for developers coming from other languages.

---

## **Quick Reference — Flow Control Summary**

| Statement         | Purpose                                                       |
|-------------------|---------------------------------------------------------------|
| `if`              | Run a block only when a condition is `True`.                  |
| `if-else`         | Choose between two branches based on a condition.             |
| `if-elif-else`    | Choose between multiple branches in sequence.                 |
| `match-case`      | Structural dispatch on the shape or value of data (3.10+).   |
| `for`             | Iterate over every item in a sequence.                        |
| `while`           | Repeat as long as a condition stays `True`.                   |
| `break`           | Exit the loop immediately.                                    |
| `continue`        | Skip the current iteration and proceed to the next.           |
| `pass`            | Placeholder — does nothing, satisfies block syntax.           |
| `else` on loop    | Run a block only if the loop completed without `break`.       |
| `del`             | Remove a variable from the current scope.                     |
| `enumerate()`     | Iterate with automatic index tracking.                        |
| `zip()`           | Iterate over two or more sequences in parallel.               |