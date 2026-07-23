# **Python Iterators and Generators**

## **1. Iterators — The Foundation**

Before generators make sense, the iterator protocol needs to be clear, because generators are just a shortcut for building iterators.

### 1.1 Iterable vs Iterator

- **Iterable**: any object you can loop over. It implements `__iter__()`, which returns an iterator. Examples: `list`, `tuple`, `dict`, `str`, `set`.
- **Iterator**: an object that implements both `__iter__()` (returns itself) and `__next__()` (returns the next value, or raises `StopIteration` when exhausted).

Every iterator is an iterable, but not every iterable is an iterator. A `list` is iterable but is not itself an iterator — calling `next()` directly on a list fails.

```python
nums = [1, 2, 3]
it = iter(nums)          # nums.__iter__() -> iterator object
print(next(it))          # 1
print(next(it))          # 2
print(next(it))          # 3
print(next(it))          # raises StopIteration
```

### 1.2 Writing a Custom Iterator Class

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

for n in Countdown(5):
    print(n)
# 5 4 3 2 1
```

This is verbose: you must manage state (`self.current`) manually and remember to raise `StopIteration` at the right time. Generators exist to remove this boilerplate.

### 1.3 How `for` Loops Actually Work

A `for x in obj:` loop is syntactic sugar for:

```python
_iterator = iter(obj)
while True:
    try:
        x = next(_iterator)
    except StopIteration:
        break
    # loop body
```

Understanding this matters because `next()` on an exhausted generator or iterator always raises `StopIteration`, and any manual iteration code (not using `for`) must handle that explicitly.

---

## 2. Generators

### 2.1 Definition

A generator is a function that produces a sequence of values lazily — one at a time, on demand — instead of computing and returning them all at once. It is written like a normal function but uses `yield` instead of (or alongside) `return`.

Calling a generator function does **not** execute its body. It returns a generator object immediately. Execution only happens when the generator is iterated (via `next()` or a `for` loop). Each `yield` pauses execution and remembers exactly where it left off — local variables, the instruction pointer, and the call stack frame are preserved.

```
Generator function called
        |
        v
Returns a generator object (nothing runs yet)
        |
        v
next() called --------> runs until first `yield` --------> value returned
        |                                                        |
        +--------------------------------------------------------+
        |
        v
next() called again --> resumes right after `yield` --> runs until next `yield`
        |
        v
   ... repeats until function returns / falls off the end ...
        |
        v
   raises StopIteration
```

### 2.2 Generator Functions vs Generator Expressions

Two ways to create a generator:

```python
# Generator function
def squares(n):
    for i in range(n):
        yield i * i

g = squares(5)

# Generator expression (like a list comprehension, but with parentheses)
g2 = (i * i for i in range(5))
```

Both produce a `generator` object with the same behavior. Generator expressions are best for simple, single-line transformations; generator functions are better when the logic needs branching, multiple `yield` points, or state across iterations.

```python
l = [x for x in range(200)]       # list comprehension -> builds full list in memory
g = (x for x in range(10))        # generator expression -> lazy, one value at a time

print(next(g))   # 0
print(next(g))   # 1
```

If you keep calling `next()` past the last value, Python raises `StopIteration`:

```python
g = (x for x in range(10))
for _ in range(10):
    print(next(g))
print(next(g))
# Traceback (most recent call last):
#   ...
# StopIteration
```

### 2.3 `type()` of a Generator

```python
def mygen():
    yield 'A'
    yield 'B'
    yield 'C'

g = mygen()
print(type(g))
# <class 'generator'>
```

A common mistake: iterating and printing the generator object itself instead of its values.

```python
for x in g:
    print(g)          # WRONG: prints <generator object mygen at 0x...> three times
```

Correct version:

```python
def mygen():
    yield 'A'
    yield 'B'
    yield 'C'

g = mygen()
print(next(g))   # A
print(next(g))   # B
print(next(g))   # C
next(g)           # raises StopIteration — the generator is exhausted
```

### 2.4 State Retention Between Calls

Local variables inside a generator keep their values across `yield` calls. This is the core mechanic that makes generators useful for stateful sequences like counters, running totals, or streaming parsers.

```python
def countdown(num):
    print("Start Countdown")
    while num > 0:
        yield num
        num -= 1

for x in countdown(5):
    print(x)
# Start Countdown
# 5
# 4
# 3
# 2
# 1
```

Note that `"Start Countdown"` only prints once, the first time the generator is advanced — not each time `countdown()` is called, because the function body only runs when iteration begins.

```python
def firstn(num):
    n = 1
    while n <= num:
        yield n
        n += 1

values = firstn(10)
print(list(values))
# [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

`list()` (like `for`) drains a generator completely by repeatedly calling `next()` until `StopIteration`. A generator can only be consumed once — after that, `list()` on the same object returns `[]`.

### 2.5 Infinite Generators

Because a generator only computes a value when asked, it can represent an infinite sequence without ever running out of memory. Termination is controlled by the consumer (`break`, a bounded `for`, or a count in the caller), not by the generator itself.

```python
def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

for f in fib():
    if f > 100:
        break
    print(f)
# 0 1 1 2 3 5 8 13 21 34 55 89
```

```python
def infinite_even_numbers():
    i = 0
    while True:
        if i % 2 == 0:
            yield i
        i += 1

gen = infinite_even_numbers()
for _ in range(10):
    print(next(gen))
# 0 2 4 6 8 10 12 14 16 18
```

### 2.6 Bounded Generators With Parameters

```python
def fibonacci_sequence(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci_sequence(8):
    print(num)
# 0 1 1 2 3 5 8 13
```

Generators can take a range of parameters to control the window of values produced, not just a count:

```python
def fibonacci_in_range(start, end):
    a, b = 0, 1
    while a <= end:
        if a >= start:
            yield a
        a, b = b, a + b

for num in fibonacci_in_range(25, 99):
    print(num)
# 34 55 89
```

### 2.7 Generators With `if/else` on `for` Loops (the `for...else` Pattern)

This is unrelated to generator syntax directly but shows up constantly when writing filtering generators. The `else` clause on a `for` loop runs only if the loop completes without hitting `break`.

```python
def prime_numbers(limit):
    for num in range(2, limit + 1):
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                break
        else:
            yield num          # only reached if the inner loop never broke

for prime in prime_numbers(10):
    print(prime)
# 2 3 5 7
```

### 2.8 Word Variant Generator (String Processing Example)

```python
def word_variants(word):
    """Yield the word with exactly one letter capitalized, for each position."""
    for i in range(len(word)):
        yield word[:i] + word[i].upper() + word[i + 1:]

for variant in word_variants("hello"):
    print(variant)
# Hello
# hEllo
# heLlo
# helLo
# hellO
```

---

## 3. Memory and Performance Behavior

### 3.1 Why Generators Avoid `MemoryError`

A list comprehension builds the entire sequence in memory before you can use any of it. A generator expression builds nothing until you ask for a value.

```python
# List comprehension — attempts to allocate ~10^16 elements immediately
l = [x * x for x in range(10_000_000_000_000_000)]
print(l[0])
# MemoryError

# Generator expression — allocates one value at a time
g = (x * x for x in range(10_000_000_000_000_000))
print(next(g))
# 0
```

The generator never materializes the full range; each call to `next()` computes exactly one `x * x` and discards the loop state until the next call.

### 3.2 Generator Creation Is (Effectively) O(1)

Creating a generator does not iterate anything, so it is fast regardless of how large the logical sequence is. The cost is paid incrementally, per `next()` call, not up front.

```python
import random
import time

def people_generator(num_people):
    for i in range(num_people):
        yield {
            'id': i,
            'name': random.choice(['Karan', 'Rohit', 'Drishya', 'Tanvi']),
            'subject': random.choice(['Python', 'Java', 'Blockchain']),
        }

t1 = time.time()
people = people_generator(1_000_000)   # nothing has run yet
t2 = time.time()
print(f"Took {t2 - t1:.6f}s")          # ~0.0s — no records were generated

for _ in range(10):
    print(next(people))                # NOW each dict is built, one per call
```

A second `for _ in range(10)` loop on the same `people` generator continues from `id: 10` onward — it does not restart, because the generator remembers exactly where it stopped.

### 3.3 Streaming Data From Disk Without Loading It All

```python
def read_chunks(file_path, chunk_size=1024):
    """Yield a file's contents in fixed-size chunks instead of reading it whole."""
    with open(file_path, 'r') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk

for chunk in read_chunks('large_file.txt'):
    print(f"Processing chunk: {chunk[:50]}...")
```

This pattern is the standard way to process log files, large CSVs, or scraped HTML dumps that do not fit comfortably in RAM.

---

## 4. Generator Methods: `send()`, `throw()`, `close()`

Beyond `next()`, generators support three additional methods that make them two-way communication channels, not just producers.

### 4.1 `send()` — Push a Value Into a Paused Generator

`yield` is an expression, not just a statement — it can receive a value from outside.

```python
def running_average():
    total = 0
    count = 0
    average = None
    while True:
        value = yield average     # pauses here, returns `average`, waits for send()
        total += value
        count += 1
        average = total / count

avg = running_average()
next(avg)                 # prime the generator (advances to the first `yield`)
print(avg.send(10))       # 10.0
print(avg.send(20))       # 15.0
print(avg.send(30))       # 20.0
```

`send()` cannot be called on a fresh, unstarted generator — it must first be advanced once with `next()` (or `send(None)`), otherwise Python raises `TypeError`.

### 4.2 `throw()` — Raise an Exception Inside the Generator

```python
def safe_divider():
    result = None
    while True:
        try:
            x = yield result
            result = 100 / x
        except ZeroDivisionError:
            result = "cannot divide by zero"

g = safe_divider()
next(g)
print(g.send(5))              # 20.0
print(g.throw(ZeroDivisionError))   # cannot divide by zero
```

### 4.3 `close()` — Stop a Generator Early

```python
def logger():
    try:
        while True:
            msg = yield
            print(f"LOG: {msg}")
    except GeneratorExit:
        print("Logger shutting down cleanly")

g = logger()
next(g)
g.send("service started")
g.close()
# LOG: service started
# Logger shutting down cleanly
```

`close()` raises `GeneratorExit` inside the generator at the point it is paused. Catching it lets you run cleanup code (closing files, flushing buffers) before the generator dies.

---

## 5. `yield from` — Delegating to a Sub-Generator

`yield from` forwards every value produced by an inner iterable/generator to the caller, and also forwards `send()`/`throw()` calls down to it. It replaces manual `for ... yield` loops.

```python
def inner():
    yield 1
    yield 2
    yield 3

def outer():
    yield 'start'
    yield from inner()      # equivalent to: for v in inner(): yield v
    yield 'end'

print(list(outer()))
# ['start', 1, 2, 3, 'end']
```

Practical use: flattening nested structures, such as recursively walking a directory tree or a nested JSON document.

```python
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

data = [1, [2, 3, [4, 5]], 6, [7, [8, [9]]]]
print(list(flatten(data)))
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

---

## 6. Real-World Applications (AI/ML and Backend Engineering)

### 6.1 Batching Data for Model Training

Feeding a model batch-by-batch instead of holding the full dataset in memory.

```python
def batch_generator(dataset, batch_size):
    batch = []
    for item in dataset:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:            # yield the final partial batch, if any
        yield batch

dataset = range(23)
for batch in batch_generator(dataset, batch_size=8):
    print(batch)
# [0, 1, 2, 3, 4, 5, 6, 7]
# [8, 9, 10, 11, 12, 13, 14, 15]
# [16, 17, 18, 19, 20, 21, 22]
```

### 6.2 Streaming Tokenized Text for NLP / LLM Pipelines

Reading a large corpus line by line and yielding tokenized, length-capped chunks — the same pattern used for feeding text into embedding models or chunking documents for a RAG pipeline.

```python
def tokenized_line_stream(file_path, max_tokens=256):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            tokens = line.strip().split()
            for i in range(0, len(tokens), max_tokens):
                yield tokens[i:i + max_tokens]

for chunk in tokenized_line_stream('corpus.txt'):
    embed_chunk(chunk)   # placeholder for an embedding call
```

### 6.3 Data Augmentation Pipeline for Computer Vision

Applying random transformations on demand, rather than pre-generating and storing every augmented image.

```python
import random

def augment_images(image_paths):
    transforms = ['rotate', 'flip', 'scale', 'none']
    for path in image_paths:
        transform = random.choice(transforms)
        yield (path, transform)   # actual image processing would happen here

for path, transform in augment_images(['img1.jpg', 'img2.jpg', 'img3.jpg']):
    print(f"{path} -> {transform}")
```

### 6.4 Simulated Sensor / Time-Series Stream

Useful for testing forecasting models or streaming ingestion code without a live data source.

```python
import random
import time

def sensor_stream(interval_seconds=1.0):
    reading = 20.0
    while True:
        reading += random.uniform(-0.5, 0.5)
        yield round(reading, 2)
        time.sleep(interval_seconds)

stream = sensor_stream(interval_seconds=0)
for _ in range(5):
    print(next(stream))
```

### 6.5 Paginated API Client

Wrapping a paginated REST API so callers can iterate over every record without manually tracking page numbers or `next_page` tokens.

```python
def fetch_all_records(api_call, page_size=100):
    page = 1
    while True:
        response = api_call(page=page, page_size=page_size)
        if not response['results']:
            break
        yield from response['results']
        if not response.get('has_next'):
            break
        page += 1

# for record in fetch_all_records(my_api_client.list_users):
#     process(record)
```

### 6.6 Chained Processing Pipeline

Generators compose cleanly: each stage pulls from the previous stage lazily, so nothing downstream waits for the whole upstream sequence to finish.

```python
def read_lines(path):
    with open(path) as f:
        for line in f:
            yield line.rstrip('\n')

def filter_non_empty(lines):
    for line in lines:
        if line.strip():
            yield line

def to_upper(lines):
    for line in lines:
        yield line.upper()

pipeline = to_upper(filter_non_empty(read_lines('notes.txt')))
for line in pipeline:
    print(line)
```

---

## 7. Advantages and Limitations

### 7.1 Advantages

| Advantage | Why it matters |
|---|---|
| Memory efficiency | Only one item exists in memory at a time, regardless of total sequence length |
| Lazy evaluation | Computation happens only when a value is actually requested |
| Supports infinite sequences | Sequences with no natural end (counters, streams, simulations) are representable |
| Cleaner code than manual iterators | No need to hand-write `__iter__`/`__next__` and manage state manually |
| Composable pipelines | Generators can be chained; each stage stays lazy end-to-end |
| Early termination is cheap | `break` or a bounded loop stops work immediately — nothing extra was computed |

### 7.2 Limitations

| Limitation | Why it matters |
|---|---|
| Single pass only | Once exhausted, a generator cannot be reset or reused — you must call the generator function again |
| No indexing or slicing | `gen[3]` or `gen[1:5]` do not work; there is no random access |
| Harder to debug | Execution state is implicit and paused mid-function, which complicates breakpoints and stack traces |
| No `len()` | The total length is generally unknown until fully consumed (unless tracked separately) |
| Not reversible | There is no built-in way to iterate backwards |
| State management complexity | Long-lived generators with `send()`/`throw()` can become hard to reason about |
| Slight per-call overhead | For small, fixed-size sequences that fit comfortably in memory, a plain list is often faster |

---

## 8. Generators vs Lists — Quick Decision Guide

| Situation | Prefer |
|---|---|
| Sequence is small and reused multiple times | List |
| Sequence is huge or unbounded | Generator |
| Need random access / slicing / `len()` | List |
| Only need to iterate once, top to bottom | Generator |
| Streaming from disk, network, or a sensor | Generator |
| Data must be sorted or the same items accessed twice | List |
| Building an ML input pipeline / batching | Generator |

---

## 9. Quick Reference

| Construct | Syntax | Notes |
|---|---|---|
| Generator function | `def f(): yield x` | Returns a generator object when called; body runs on iteration |
| Generator expression | `(x for x in iterable)` | Lazy equivalent of a list comprehension |
| Advance manually | `next(g)` | Raises `StopIteration` when exhausted |
| Drain fully | `list(g)`, `for x in g:` | Consumes the generator completely |
| Send a value in | `g.send(value)` | Must call `next(g)` once first to prime it |
| Raise inside generator | `g.throw(ExcType)` | Injects an exception at the paused `yield` |
| Stop early with cleanup | `g.close()` | Raises `GeneratorExit` inside the generator |
| Delegate to sub-generator | `yield from other_gen()` | Forwards values, `send()`, and `throw()` |
| Custom iterator class | `__iter__` + `__next__` | The manual, verbose alternative to a generator function |