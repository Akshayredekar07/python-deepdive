# **Python Generators and Iterators**

Notes covering the iterator protocol, custom iterator classes, `yield`, generator expressions, `yield from`, and the memory-efficient pipeline patterns both are built for.

## **Iterables and Iterators**

An iterable is any object capable of returning its members one at a time — something that can appear after `in` in a `for` loop. An iterator is the object that actually does the work of producing those members, one at a time, on demand.

- An iterable implements `__iter__`, which returns an iterator.
- An iterator implements `__next__`, which returns the next value or raises `StopIteration` once there is nothing left.
- An iterator is also its own iterable — its `__iter__` simply returns itself — which is why an iterator can be used directly in a `for` loop too.

```python
numbers = [10, 20, 30]        # numbers is an iterable, not an iterator
it = iter(numbers)             # iter() asks the iterable for an iterator
print(type(it))                 # <class 'list_iterator'>

print(next(it))   # 10
print(next(it))   # 20
print(next(it))   # 30
print(next(it))   # raises StopIteration -- nothing left
```

A `for` loop does exactly this under the hood: it calls `iter()` once on the iterable to get an iterator, then calls `next()` on that iterator repeatedly, stopping automatically when `StopIteration` is raised.

```python
numbers = [10, 20, 30]
it = iter(numbers)
while True:
    try:
        value = next(it)
    except StopIteration:
        break
    print(value)
# 10
# 20
# 30
```

**Common mistake — treating an iterable as if it were already an iterator.** Calling `next()` directly on a list, a dict, or a string raises `TypeError`, since none of these are iterators themselves; `iter()` has to be called first to get an iterator out of them.

```python
numbers = [10, 20, 30]
# next(numbers)   # TypeError: 'list' object is not an iterator
next(iter(numbers))   # 10 -- works, because iter(numbers) is an iterator
```

## **Writing a Custom Iterator Class**

A class becomes an iterator by implementing both `__iter__` (returning `self`) and `__next__` (returning the next value or raising `StopIteration`).

```python
class Countdown:
    def __init__(self, start):
        self.n = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1

for value in Countdown(3):
    print(value)
# 3
# 2
# 1
```

This works, and it is an ordinary class — but writing `__iter__` and `__next__` by hand, and manually tracking state (`self.n`) between calls, is exactly the boilerplate that generator functions exist to remove.

**A custom iterator over a collection — separating the iterable from the iterator**

```python
class Roster:
    def __init__(self, students):
        self.students = students

    def __iter__(self):
        return RosterIterator(self.students)

class RosterIterator:
    def __init__(self, students):
        self.students = students
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.students):
            raise StopIteration
        student = self.students[self.index]
        self.index += 1
        return student

roster = Roster(["Durga", "Rohit", "Tanvi"])

for name in roster:
    print(name)

for name in roster:   # works again -- each __iter__() call builds a brand new RosterIterator
    print(name)
```

`Roster` is the iterable and `RosterIterator` is the iterator; keeping them as two separate classes, rather than making `Roster` its own iterator, means `roster` can be iterated multiple times, since each `for` loop calls `__iter__` fresh and gets a new `RosterIterator` starting back at index `0`. A single combined iterator class, like `Countdown` above, can only be iterated once — its internal state keeps counting down and never resets.

## **Built-in Iterators Already in Everyday Use**

Many familiar built-ins are themselves iterators, or return one, without it usually being labeled that way.

```python
names = ["Karan", "Om", "Tanvi"]

for i, name in enumerate(names):        # enumerate() returns an iterator of (index, value) pairs
    print(i, name)

scores = [91, 78, 85]
for name, score in zip(names, scores):   # zip() returns an iterator of paired-up tuples
    print(name, score)

for name in reversed(names):             # reversed() returns an iterator that walks backward
    print(name)

upper_names = map(str.upper, names)      # map() returns an iterator, not a list
print(next(upper_names))   # KARAN

passing = filter(lambda s: s >= 80, scores)   # filter() also returns an iterator
print(list(passing))       # [91, 85]
```

`map` and `filter` are exhaustible iterators, exactly like a hand-written one — once fully consumed with `list(...)` or a `for` loop, a second pass over the same object returns nothing.

## **Infinite Iterators**

`itertools` provides ready-made iterators that never raise `StopIteration` on their own, meant to be paired with something like `islice`, `zip`, or an explicit `break` on the consuming side.

```python
from itertools import count, cycle, repeat, islice

counter = count(start=1, step=2)
print(list(islice(counter, 5)))   # [1, 3, 5, 7, 9]

colors = cycle(["red", "green", "blue"])
print(list(islice(colors, 7)))    # ['red', 'green', 'blue', 'red', 'green', 'blue', 'red']

pings = repeat("ping", times=3)
print(list(pings))                 # ['ping', 'ping', 'ping']
```

`count` produces an unending arithmetic sequence, `cycle` repeats a fixed sequence forever, and `repeat` repeats a single value, either forever or a fixed number of times — all three are iterators built exactly the same way a hand-written `__next__` would be, just already written and optimized in the standard library.

## **What Is a Generator**

A generator is a function responsible for generating a sequence of values — and, in practice, the easiest way to build a custom iterator without writing a class at all.

- A generator function is written just like an ordinary function, but it uses the `yield` keyword instead of (or alongside) `return`.
- Calling a generator function does not run its body immediately — it returns a generator object, and the body only executes as that object is iterated, one `yield` at a time.
- Each call to `next()` resumes the function exactly where it left off, runs until the next `yield`, and pauses again, so the function's local variables persist between calls.
- A generator object automatically implements both `__iter__` and `__next__`, which is exactly why it satisfies the iterator protocol from the section above without any class being written at all.

```python
def mygen():
    yield 'A'
    yield 'B'
    yield 'C'

g = mygen()
print(type(g))   # <class 'generator'>

print(next(g))   # A
print(next(g))   # B
print(next(g))   # C
print(next(g))   # raises StopIteration -- nothing left to yield
```

Once every `yield` has been consumed, calling `next()` again raises `StopIteration` rather than looping back to the start.

## **Writing Generator Functions with `yield`**

A generator function that counts down, using a `while` loop and `yield` instead of a hand-written class.

```python
def countdown(num):
    print("Start Countdown")
    while num > 0:
        yield num
        num = num - 1

values = countdown(5)
for x in values:
    print(x)
```

Output:

```
Start Countdown
5
4
3
2
1
```

A generator that produces the first `n` positive integers.

```python
def firstn(num):
    n = 1
    while n <= num:
        yield n
        n = n + 1

values = firstn(5)
for x in values:
    print(x)
```

Output:

```
1
2
3
4
5
```

A generator can be converted into a list at any point by passing it to `list()`, which pulls every remaining value out at once.

```python
values = firstn(10)
l1 = list(values)
print(l1)   # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

A generator producing an infinite Fibonacci sequence, where each number is the sum of the previous two.

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
```

Output:

```
0
1
1
2
3
5
8
13
21
34
55
89
```

`fib()` never finishes on its own — the `while True` loop would run forever. The `for` loop above only stops because of the explicit `if f > 100: break` check on the consuming side, which is a common shape for generators that model an unbounded stream.

**A generator with a `return` — ending the sequence early**

```python
def limited_range(n, cutoff):
    i = 0
    while i < n:
        if i >= cutoff:
            return
        yield i
        i += 1

print(list(limited_range(10, 4)))   # [0, 1, 2, 3]
```

`return` inside a generator simply ends the iteration — it raises `StopIteration` rather than returning a value the way it does in a normal function.

**Common mistake — a generator is exhausted after one full pass**

```python
def gen():
    yield 1
    yield 2
    yield 3

g = gen()
print(list(g))   # [1, 2, 3]
print(list(g))   # [] -- already exhausted, nothing left to yield
```

The fix is to call `gen()` again to get a fresh generator, or to materialize the values into a list once and reuse that list.

## **Generator Expressions**

A generator expression looks exactly like a list comprehension, but with parentheses instead of square brackets, and it produces items lazily instead of building the whole list in memory.

```python
squares_list = [x * x for x in range(1_000_000)]     # builds the entire list in memory immediately
squares_gen  = (x * x for x in range(1_000_000))       # builds nothing yet -- lazy

print(type(squares_gen))    # <class 'generator'>
print(next(squares_gen))    # 0
print(next(squares_gen))    # 1
```

A generator expression can be passed directly into a function without extra parentheses.

```python
total = sum(x * x for x in range(10))
print(total)   # 285

names = ["Karan", "Om", "Tanvi", "Rohit"]
print(any(len(n) > 4 for n in names))       # True
print(all(n[0].isupper() for n in names))    # True
```

**Generator expression vs list comprehension — when to use which.** Use a list comprehension when the values are needed more than once, when `len()` or random access by index is required, or when the collection is small. Use a generator expression when iterating only once, when the collection could be very large or infinite, or when piping straight into `sum`, `any`, `all`, `max`, or `min`, since materializing the intermediate list would waste memory for no benefit.

```python
# Wasteful -- builds a full list just to sum it once and discard it
total = sum([x * x for x in range(10_000_000)])

# Better -- never builds the intermediate list at all
total = sum(x * x for x in range(10_000_000))
```

## **`yield from`**

`yield from` delegates iteration to another iterable or generator, yielding each of its values in turn, and correctly forwards `.send()`, `.throw()`, and the final return value between nested generators.

```python
def inner():
    yield 1
    yield 2
    yield 3

def outer():
    yield from inner()
    yield 4

print(list(outer()))   # [1, 2, 3, 4]
```

**Flattening a nested structure recursively**

```python
def flatten(items):
    for item in items:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

nested = [1, [2, 3, [4, 5]], 6, [7, [8, [9, 10]]]]
print(list(flatten(nested)))   # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

`yield from flatten(item)` recursively delegates to another call of the same generator, and every value it yields bubbles straight up through each level of nesting — this is the cleanest way to flatten an arbitrarily nested structure in Python.

## **Two-Way Generators — `send`, `throw`, and `close`**

A generator can also receive values while it runs, not just produce them, using `.send()`.

```python
def running_average():
    total = 0
    count = 0
    average = None
    while True:
        value = yield average
        total += value
        count += 1
        average = total / count

avg = running_average()
next(avg)                   # prime the generator -- advances to the first yield
print(avg.send(10))         # 10.0
print(avg.send(20))         # 15.0
print(avg.send(30))         # 20.0
```

`value = yield average` is a two-way channel: `yield average` pauses and sends `average` out to the caller, and `.send(value)` resumes the generator, injecting `value` back in as the result of that `yield` expression.

```python
gen = running_average()
next(gen)
gen.send(10)

# gen.throw(ValueError, "something went wrong")   # raises ValueError at the paused yield point

gen2 = running_average()
next(gen2)
gen2.close()   # raises GeneratorExit at the paused yield point, then the generator stops
```

`gen.throw(exc_type, value)` raises an exception exactly at the point where the generator is currently paused. `gen.close()` raises `GeneratorExit` at that same paused point and is how Python cleans up a generator that will never be fully iterated, giving any `finally` block inside the generator a chance to run.

## **Generators vs Hand-Written Iterators**

Every generator is an iterator, but not every iterator is a generator — a generator is simply the shortcut Python provides for building one.

| | Hand-written iterator class | Generator function |
| --- | --- | --- |
| Definition | A class implementing `__iter__` and `__next__` | An ordinary function using `yield` |
| State tracking | Stored manually in instance attributes (`self.n`, `self.index`) | Tracked automatically by the paused function frame |
| Boilerplate | `__init__`, `__iter__`, `__next__` all written out | A single function body |
| Restarting iteration | Requires a fresh instance, or a separate iterable/iterator split | Requires calling the generator function again |
| Extra abilities | Can expose any custom method or attribute (`roster.students`) | Also supports `.send()`, `.throw()`, `.close()` for two-way communication |
| When to prefer | The object needs extra methods, multiple independent iteration passes with shared configuration, or non-sequential access patterns | The logic is a straightforward one-item-at-a-time sequence — the common case |

## **Advantages of Generator Functions**

- Generators are much easier to write and read than a hand-written class-level iterator with `__iter__` and `__next__`.
- Generators improve memory utilization and performance, since values are produced one at a time instead of all at once.
- Generators are well suited to reading data from a large number of large files, since each file can be processed without loading it fully into memory.
- Generators work well for web scraping and crawling, where results arrive one page or one record at a time.

## **Generators vs Normal Collections — Performance**

```python
import random
import time

names = ["Durga", "Rohit", "Tanvi", "Karan"]
subjects = ["Python", "Java", "Blockchain"]

def people_list(num_people):
    results = []
    for i in range(num_people):
        person = {
            "id": i,
            "name": random.choice(names),
            "subject": random.choice(subjects),
        }
        results.append(person)
    return results

def people_generator(num_people):
    for i in range(num_people):
        person = {
            "id": i,
            "name": random.choice(names),
            "subject": random.choice(subjects),
        }
        yield person

t1 = time.perf_counter()
people = people_generator(10_000_000)
t2 = time.perf_counter()

print("Took —", t2 - t1)
```

`time.clock()` was removed in Python 3.8; `time.perf_counter()` is the modern replacement for measuring elapsed time. Running both versions and comparing `t2 - t1` shows that building `people_generator(...)` returns almost immediately, since no work happens until the generator is actually iterated, while `people_list(...)` does all ten million iterations up front before returning anything.

## **Generators vs Normal Collections — Memory Utilization**

**Normal collection**

```python
l = [x * x for x in range(10_000_000_000_000_000)]
print(l[0])
```

This raises `MemoryError`, because every one of those values would need to be stored in memory before the list comprehension could finish building the list.

**Generator**

```python
g = (x * x for x in range(10_000_000_000_000_000))
print(next(g))   # 0
```

No `MemoryError` occurs here, because generator values are never stored up front — each value is computed only at the moment it is requested.

## **Common Mistakes**

- Calling `next()` directly on an iterable such as a list, dict, or string instead of on an iterator obtained from it with `iter(...)` — this raises `TypeError`, since the iterable itself has no `__next__`.
- Making a class both its own iterable and its own iterator (like `Countdown`) when multiple independent passes are needed; a single combined class can only be iterated once before its internal state runs out, so it needs a separate iterable/iterator split, like `Roster` and `RosterIterator`, when more than one pass is required.
- Treating a generator like a list — calling `len(g)` or indexing `g[0]` — fails, since a generator supports only forward iteration, not random access or a known length.
- Reusing an already-exhausted generator and expecting values again; once every `yield` has been consumed, a fresh call to the generator function is required to iterate it again.
- Calling `.send(value)` before priming the generator with an initial `next(gen)` raises `TypeError`, since the generator has not yet reached its first `yield` to receive a sent value.
- Assuming a `return value` inside a generator behaves like `return` in a normal function; it actually ends iteration and only becomes accessible through the `StopIteration` payload picked up by `yield from`.
- Building a full list with a list comprehension purely to iterate it once and discard it, where a generator expression would use far less memory for the same result.
- Iterating an infinite generator, such as `fib()`, without an explicit stopping condition on the consuming side, which causes the loop to run forever.
- Opening a file inside a generator without a `with` block; if the generator is never fully iterated, the file handle may stay open until garbage collection closes it, rather than being closed deterministically.

## **Production Patterns**

**Reading a huge file line by line without loading it all into memory**

```python
def read_large_file(path):
    with open(path) as f:
        for line in f:
            yield line.strip()

def parse_log_lines(lines):
    for line in lines:
        if "ERROR" in line:
            yield line

# error_lines = parse_log_lines(read_large_file("app.log"))
# for line in error_lines:
#     print(line)
```

Even if `app.log` is 50 gigabytes, this pipeline never holds more than a handful of lines in memory at once.

**A lazy ETL-style pipeline, entirely generator-based**

```python
def extract(records):
    for r in records:
        yield r

def transform(records):
    for r in records:
        r = {**r, "score": r["score"] / 100}
        yield r

def load_filter(records, threshold=0.5):
    for r in records:
        if r["score"] >= threshold:
            yield r

raw_records = [
    {"student": "Karan", "score": 91},
    {"student": "Tanvi", "score": 42},
    {"student": "Om", "score": 78},
]

pipeline = load_filter(transform(extract(raw_records)), threshold=0.5)
for record in pipeline:
    print(record)
# {'student': 'Karan', 'score': 0.91}
# {'student': 'Om', 'score': 0.78}
```

Each stage of this pipeline is itself lazy — nothing runs until the final `for` loop starts pulling values, and each record flows through `extract -> transform -> load_filter` one at a time rather than in three separate full passes.

**Batching a dataset lazily for an ML training loop**

```python
def data_loader(dataset, batch_size):
    batch = []
    for item in dataset:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

training_examples = list(range(1, 27))   # imagine feature vectors, not plain ints

for step, batch in enumerate(data_loader(training_examples, batch_size=8)):
    print(f"step {step} — training on batch of {len(batch)}")
```

This is a simplified version of what PyTorch's `DataLoader` and TensorFlow's `tf.data.Dataset` do internally.

**Streaming a large file for download in a web API**

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

def file_stream(path, chunk_size=8192):
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            yield chunk

@app.get("/download")
def download():
    return StreamingResponse(
        file_stream("report_2025.pdf"),
        media_type="application/pdf",
    )
```

Memory use stays bounded by `chunk_size`, regardless of how large the underlying file is.

| Tool | Key Feature | Best Use Case |
| --- | --- | --- |
| Plain generator function (`yield`) | Pauses and resumes function state automatically | File and log processing, ETL pipelines |
| Generator expression | Lazy version of a list comprehension | Feeding a single-pass reduction like `sum` or `any` |
| `fastapi.responses.StreamingResponse` | Streams a generator's output as an HTTP response body | Large file downloads, server-sent events |
| PyTorch `DataLoader` / `tf.data.Dataset` | Lazily batches a dataset for training | ML training loops over data too large for memory |
| `itertools` (`islice`, `batched`, `tee`) | Standard-library helpers for slicing and splitting iterators | Chunking, batching, and forking generator streams |

## **Modern Python Patterns**

Chunking a stream into fixed-size batches used to require a hand-written generator with `itertools.islice`.

```python
from itertools import islice

def batched(iterable, size):
    it = iter(iterable)
    while batch := list(islice(it, size)):
        yield batch
```

Since Python 3.12, `itertools.batched` provides this natively.

```python
from itertools import batched   # Python 3.12+

student_ids = list(range(1, 23))
for batch in batched(student_ids, 5):
    print(batch)
```

Type-hinting a generator function used to be written with a bare `Iterator` or `Iterable`, which does not capture what the generator can receive via `.send()` or return at the end.

```python
from typing import Generator

def running_average() -> Generator[float, float, None]:
    total = 0
    count = 0
    average = 0.0
    while True:
        value = yield average
        total += value
        count += 1
        average = total / count
```

`Generator[YieldType, SendType, ReturnType]` (available from `typing`, or from `collections.abc.Generator` for runtime checks) documents all three roles of a generator in one type — what it yields, what it can accept through `.send()`, and what it returns when exhausted.

| Older Style | Modern Style (3.10+) |
| --- | --- |
| Hand-written `batched()` generator using `itertools.islice` in a loop | `itertools.batched(iterable, n)`, built into the standard library since 3.12 |
| `Iterator[float]` type hint, which hides send and return behavior | `Generator[float, float, None]` type hint, documenting yield, send, and return types together |
| `time.clock()` for timing generator performance | `time.perf_counter()`, the supported replacement since 3.8 |

## **Quick Reference**

| Pattern | Syntax | Purpose |
| --- | --- | --- |
| Get an iterator from an iterable | `it = iter(obj)` | Obtain the object that `__next__` can be called on |
| Pull one value from an iterator | `next(it)` | Advance to the next value, or raise `StopIteration` |
| Custom iterator class | `class X: def __iter__(self): return self` `def __next__(self): ...` | Hand-written, class-based iteration |
| Separate iterable/iterator | Iterable's `__iter__` returns a fresh iterator instance | Allow multiple independent iteration passes |
| Infinite iterator | `itertools.count`, `cycle`, `repeat` | Unending sequences, paired with `islice` or a `break` |
| Basic generator | `def gen(): yield value` | Produce a sequence lazily |
| Pull one value | `next(gen)` | Advance the generator to its next `yield` |
| Consume fully | `for x in gen:` or `list(gen)` | Iterate until `StopIteration` |
| Generator expression | `(expr for x in iterable)` | Lazy, memory-light version of a list comprehension |
| Delegate to another generator | `yield from other_gen()` | Forward values, `.send()`, and return value |
| Two-way communication | `value = yield out` then `gen.send(value)` | Build stateful stream processors |
| Stop a generator early | `gen.close()` | Raise `GeneratorExit` at the paused point |
| Inject an error | `gen.throw(exc_type, value)` | Raise an exception at the paused point |
| Fixed-size batching | `itertools.batched(iterable, n)` (3.12+) | Chunk a stream for APIs or ML training |
| Type hint | `Generator[YieldType, SendType, ReturnType]` | Document a generator's full contract |