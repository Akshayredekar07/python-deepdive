# **Python functools and itertools**

## **Why This Toolbox Exists**

`functools` and `itertools` are the standard library's collection of small, composable, first-class-function-based tools.

- `functools` is mostly about the function itself — caching its results, pre-filling some of its arguments, or dispatching to different implementations based on argument type.
- `itertools` is mostly about the data flowing through an iterator — combining, slicing, grouping, or generating sequences of values lazily.
- Once closures, decorators, `map`/`filter`/`reduce`, and generators feel natural, most of this toolbox reads as "oh, this is the same pattern, already built and optimized."

## **`functools.lru_cache` and `functools.cache`**

`lru_cache` memoizes a function automatically — caching each unique set of arguments' result so repeated calls skip recomputation.

```python
from functools import lru_cache, cache

@lru_cache(maxsize=128)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(30))                 # fast, thanks to caching
print(fib.cache_info())        # CacheInfo(hits=..., misses=..., maxsize=128, currsize=...)
fib.cache_clear()              # empties the cache
```

`lru_cache(maxsize=N)` keeps at most `N` most-recently-used results; once full, the least recently used entry is evicted to make room for a new one. `maxsize=None` makes it unbounded.

`cache`, added in Python 3.9, is simply `lru_cache(maxsize=None)` — a lightweight, unbounded memoization decorator with slightly less overhead, for cases where the cache will never need to evict anything.

```python
@cache
def factorial(n):
    return n * factorial(n - 1) if n else 1

print(factorial(10))   # 3628800
print(factorial(5))    # 120, already cached as part of computing factorial(10)
```

**When to reach for `lru_cache` vs `cache`.** Use `lru_cache(maxsize=...)` for functions called with a large or unbounded variety of arguments over a long-running process, where an unbounded cache would grow forever and leak memory. Use `cache` for a small, fixed set of possible arguments — recursive math functions, config lookups, small enum-like inputs — where unbounded growth is not a real risk.

**Caching an expensive lookup in a data pipeline**

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def normalize_country_code(raw_name):
    # imagine this calls a slow lookup service or does fuzzy matching
    return raw_name.strip().upper()[:2]

for row in ["  india", "IND ", "india "]:
    print(normalize_country_code(row))   # computed once, cached for the repeats
```

**Caching a config or model client as a lazy singleton**

```python
from functools import lru_cache

@lru_cache(maxsize=1)
def get_model_client():
    print("loading model, this happens only once")
    return {"model": "loaded-model-object"}

get_model_client()   # loads
get_model_client()   # returns the cached client instantly, no reload
```

`maxsize=1` here is an idiomatic way to lazily initialize and cache a single expensive object — a common pattern for database connections, model clients, and configuration objects in both web APIs and ML training scripts.

## **`functools.partial`**

`partial` takes a function and some arguments, and returns a new callable with those arguments already bound — pre-filling in part of a function's signature without writing a new `def` or lambda.

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))   # 25
print(cube(5))      # 125
```

**Positional binding vs keyword binding**

```python
def greet(greeting, name):
    return f"{greeting}, {name}"

hello = partial(greet, "Hello")             # binds the first positional argument
print(hello("Karan"))                        # Hello, Karan

for_karan = partial(greet, name="Karan")     # binds a keyword argument
print(for_karan("Hi"))                        # Hi, Karan
```

`partial` vs a lambda often do the same job:

```python
square_lambda = lambda x: power(x, 2)
square_partial = partial(power, exponent=2)
```

`partial` is generally preferred when simply binding arguments with no additional logic, since it preserves more introspection (`square_partial.func`, `square_partial.keywords` are inspectable), is slightly faster, and communicates intent more directly. A lambda is better once actual computation beyond filling in arguments is needed.

**Callback registration — solving the same late-binding problem closures ran into**

```python
from functools import partial

def handle_click(button_id):
    print(f"button {button_id} clicked")

buttons = ["save", "cancel", "delete"]
callbacks = [partial(handle_click, button_id) for button_id in buttons]

for cb in callbacks:
    cb()
# button save clicked
# button cancel clicked
# button delete clicked
```

**Pre-configuring a data pipeline step**

```python
from functools import partial

def resize_image(image, width, height):
    return f"resized to {width}x{height}"

thumbnail = partial(resize_image, width=128, height=128)
banner = partial(resize_image, width=1200, height=300)

images = ["photo1.png", "photo2.png"]
thumbnails = [thumbnail(img) for img in images]
```

**Pre-configuring an API call**

```python
import functools
import requests   # illustrative -- not actually executed here

get_json = functools.partial(requests.get, headers={"Accept": "application/json"})
# get_json("https://api.example.com/reports")  -- headers are already filled in every time
```

## **`functools.reduce` — Where It Fits**

`reduce` folds an entire iterable down into a single accumulated value.

```python
from functools import reduce

total = reduce(lambda acc, x: acc + x, [1, 2, 3, 4], 0)
print(total)   # 10
```

`reduce` is the "fold everything down to one result" tool, `map` is "transform every element," `filter` is "keep a subset of elements," and `lru_cache`/`partial` are about the function itself — caching it or pre-configuring it — rather than about processing a sequence at all. Keeping that distinction in mind is usually enough to know which tool a given problem calls for.

## **`functools.singledispatch`**

Python does not support traditional function overloading — defining the same function name multiple times with different parameter types. `singledispatch` gives the closest equivalent: one generic function, with type-specific implementations registered separately, and Python picks the right one automatically based on the type of the first argument.

```python
from functools import singledispatch

@singledispatch
def describe(value):
    return f"value: {value!r}"

@describe.register
def _(value: int):
    return f"an integer: {value}"

@describe.register
def _(value: str):
    return f"a string of length {len(value)}: {value!r}"

@describe.register
def _(value: list):
    return f"a list with {len(value)} items"

print(describe(42))            # an integer: 42
print(describe("hello"))       # a string of length 5: 'hello'
print(describe([1, 2, 3]))     # a list with 3 items
print(describe(3.14))          # value: 3.14 -- falls back to the generic implementation
```

`@describe.register` reads the type hint on the function it decorates to know which type it handles. Without a matching registered type, `describe` falls back to the original, undecorated implementation.

**Why this beats a chain of `isinstance` checks**

```python
# Without singledispatch -- an isinstance ladder that grows unpleasantly
def describe(value):
    if isinstance(value, int):
        return f"an integer: {value}"
    elif isinstance(value, str):
        return f"a string of length {len(value)}: {value!r}"
    elif isinstance(value, list):
        return f"a list with {len(value)} items"
    else:
        return f"value: {value!r}"
```

Both do the same job. `singledispatch` scales better as the number of types grows, since each type's logic lives in its own small function that can be defined anywhere — even in a different module, registered later — rather than all being crammed into one growing `if/elif` chain.

**`singledispatchmethod` — the same idea inside a class**

```python
from functools import singledispatchmethod

class Formatter:
    @singledispatchmethod
    def format(self, value):
        return str(value)

    @format.register
    def _(self, value: int):
        return f"{value:,}"

    @format.register
    def _(self, value: float):
        return f"{value:.2f}"

f = Formatter()
print(f.format(1000000))   # 1,000,000
print(f.format(3.14159))   # 3.14
```

**Handling different payload shapes in an API or pipeline**

```python
from functools import singledispatch

@singledispatch
def normalize_record(record):
    raise TypeError(f"unsupported record type: {type(record)}")

@normalize_record.register
def _(record: dict):
    return {"id": record.get("id"), "source": "dict"}

@normalize_record.register
def _(record: str):
    return {"id": record, "source": "raw_id_string"}

print(normalize_record({"id": 42}))     # {'id': 42, 'source': 'dict'}
print(normalize_record("student_88"))    # {'id': 'student_88', 'source': 'raw_id_string'}
```

Real data pipelines frequently receive records in more than one shape — a raw ID, a full dict, a database row object — depending on the upstream source. `singledispatch` keeps each shape's handling isolated and independently testable, instead of one function with a growing pile of type checks at the top.

## **`functools.cached_property`**

`cached_property` is a descriptor that turns a method into a property computed once per instance, then cached directly on that instance for the rest of its life. Unlike `lru_cache` on a method, which caches globally across every instance and keeps every instance reachable forever, `cached_property` is scoped to one object and is naturally cleared when that object is garbage collected.

```python
import functools

class Student:
    def __init__(self, student_id):
        self.student_id = student_id

    @functools.cached_property
    def transcript(self):
        print(f"loading transcript for {self.student_id}...")
        return {"gpa": 8.7, "credits": 120}   # imagine an expensive database call here

s = Student("student_88")
s.transcript   # loading transcript for student_88...
s.transcript   # no print -- read straight from s.__dict__

del s.transcript   # clear the cached value
s.transcript        # loading transcript for student_88... -- recomputed
```

**When to prefer `cached_property` over `lru_cache`.** Use `cached_property` for a value that belongs to one specific object and should live and die with it — a parsed config, a loaded model, a computed report for one user. Use `lru_cache` when the same function is called with many different argument combinations across the whole program and a shared cache keyed by those arguments is wanted.

## **`functools.partialmethod` and Supporting Tools**

`partialmethod` is the version of `partial` that works correctly as a method on a class — unlike a plain `partial`, it correctly waits to bind `self` until the method is actually called on an instance.

```python
import functools

class ApiClient:
    def _request(self, method, path, **kwargs):
        return f"{method} {path} {kwargs}"

    get = functools.partialmethod(_request, "GET")
    post = functools.partialmethod(_request, "POST")
    delete = functools.partialmethod(_request, "DELETE")

client = ApiClient()
print(client.get("/students"))                 # GET /students {}
print(client.post("/students", name="Om"))      # POST /students {'name': 'Om'}
```

`total_ordering` fills in the remaining comparison methods automatically once `__eq__` and one ordering method are defined.

```python
import functools

@functools.total_ordering
class Version:
    def __init__(self, major, minor):
        self.major, self.minor = major, minor
    def __eq__(self, other):
        return (self.major, self.minor) == (other.major, other.minor)
    def __lt__(self, other):
        return (self.major, self.minor) < (other.major, other.minor)

v1 = Version(1, 2)
v2 = Version(1, 5)
print(v1 < v2, v1 <= v2, v1 > v2, v1 >= v2)   # True True False False
```

`total_ordering` fills in `__le__`, `__gt__`, and `__ge__` automatically from `__eq__` and `__lt__` — the same "provide a little, the rest gets built" shape as the rest of `functools`.

| Tool | Purpose |
| --- | --- |
| `lru_cache(maxsize=128, typed=False)` | Memoize with LRU eviction |
| `cache` | Unbounded memoization (3.9+) |
| `cached_property` | Per-instance memoization (3.8+) |
| `partial(func, *args, **kwargs)` | Pre-fill arguments on a function |
| `partialmethod` | `partial` that works correctly as a class method |
| `reduce` | Fold an iterable to a single value |
| `singledispatch` / `singledispatchmethod` | Generic function dispatch by first-argument type |
| `total_ordering` | Fill in the rest of the comparison methods from `__eq__` and one other |
| `wraps(func)` | Decorator that copies metadata from one function onto another |
| `update_wrapper` | The plain function-call form of `wraps`, used inside class-based decorators |
| `cmp_to_key` | Convert an old-style two-argument comparison function into a `key=` function for `sorted` |

## **Combining and Generating with `itertools`**

`itertools` provides fast, memory-efficient building blocks for working with iterators — everything returns a lazy iterator, so wrap the result in `list(...)` to materialize it, exactly like `map` and `filter`.

**Combining iterables**

```python
from itertools import chain

a = [1, 2, 3]
b = [4, 5, 6]
print(list(chain(a, b)))                    # [1, 2, 3, 4, 5, 6]
print(list(chain.from_iterable([a, b])))     # same, useful when starting with a list of lists
```

**Counting and cycling**

```python
from itertools import count, cycle, repeat

ids = count(start=1000, step=1)
print(next(ids), next(ids), next(ids))     # 1000 1001 1002 -- an infinite counter

colors = cycle(["red", "green", "blue"])
print([next(colors) for _ in range(7)])    # ['red', 'green', 'blue', 'red', 'green', 'blue', 'red']

print(list(repeat("x", 4)))                 # ['x', 'x', 'x', 'x']
```

## **Grouping — `itertools.groupby`**

```python
from itertools import groupby

scores = [
    {"student": "Karan", "grade": "A"},
    {"student": "Om", "grade": "A"},
    {"student": "Tanvi", "grade": "B"},
    {"student": "Rohit", "grade": "B"},
    {"student": "Harsha", "grade": "A"},
]

# groupby only groups CONSECUTIVE matching items -- sort first if that matters
scores.sort(key=lambda s: s["grade"])
for grade, group in groupby(scores, key=lambda s: s["grade"]):
    names = [s["student"] for s in group]
    print(grade, "->", names)
# A -> ['Karan', 'Om', 'Harsha']
# B -> ['Tanvi', 'Rohit']
```

`groupby` groups only runs of consecutive matching elements — it is not a full "group by key across the whole collection" the way SQL's `GROUP BY` is. Skipping the sort produces multiple separate groups for the same key instead of one combined group.

## **Combinatorics — `product`, `permutations`, `combinations`**

```python
from itertools import product, permutations, combinations

sizes = ["S", "M", "L"]
colors = ["red", "blue"]
print(list(product(sizes, colors)))
# [('S', 'red'), ('S', 'blue'), ('M', 'red'), ('M', 'blue'), ('L', 'red'), ('L', 'blue')]

print(list(permutations([1, 2, 3], 2)))
# [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

print(list(combinations([1, 2, 3], 2)))
# [(1, 2), (1, 3), (2, 3)]
```

`product` gives every combined pairing (order matters, repeats across inputs allowed), `permutations` gives every ordered arrangement from one input (order matters, no repeats), and `combinations` gives every unordered selection from one input (order does not matter, no repeats).

## **Slicing and Batching Lazily**

```python
from itertools import islice

def natural_numbers():
    n = 1
    while True:
        yield n
        n += 1

first_ten = list(islice(natural_numbers(), 10))
print(first_ten)   # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

`islice` works on infinite generators the way regular slicing `[:10]` cannot, since a plain generator does not support indexing.

**Batching for API calls or ML training**

```python
from itertools import islice

def batched(iterable, size):
    it = iter(iterable)
    while batch := list(islice(it, size)):
        yield batch

student_ids = list(range(1, 23))
for batch in batched(student_ids, size=5):
    print(f"sending batch of {len(batch)}: {batch}")
```

Since Python 3.12, `itertools.batched` does this natively.

```python
from itertools import batched   # Python 3.12+

for batch in batched(student_ids, 5):
    print(batch)
```

`itertools.batched(iterable, n, strict=False)` groups the source into tuples of length `n`; the last group may be shorter unless `strict=True`, in which case a mismatched final group raises `ValueError` instead of silently returning a short tuple.

**Overlapping pairs — `pairwise` (3.10+)**

```python
from itertools import pairwise

readings = [10, 12, 15, 11, 9]
print(list(pairwise(readings)))            # [(10, 12), (12, 15), (15, 11), (11, 9)]

changes = [b - a for a, b in pairwise(readings)]
print(changes)                              # [2, 3, -4, -2]
```

`pairwise` is the direct tool for "compare each element to the one before it" — computing deltas, detecting consecutive duplicates, or checking a sequence is sorted.

## **More Filtering and Combining Tools**

**Selecting by a matching boolean mask — `compress`**

```python
from itertools import compress

data = ["report_2025.pdf", "notes.txt", "invoice.pdf", "draft.docx"]
is_pdf = [True, False, True, False]
print(list(compress(data, is_pdf)))         # ['report_2025.pdf', 'invoice.pdf']
```

**Padding the shorter iterable — `zip_longest`**

```python
from itertools import zip_longest

names = ["Karan", "Om", "Tanvi"]
scores = [91, 78]
print(list(zip_longest(names, scores, fillvalue="-")))
# [('Karan', 91), ('Om', 78), ('Tanvi', '-')]
```

Regular `zip` silently stops at the shorter iterable; `zip_longest` keeps going and fills the gaps, which matters whenever a missing value should be visible rather than silently dropped.

**Filtering variants — `filterfalse`, `takewhile`, `dropwhile`**

```python
from itertools import filterfalse, takewhile, dropwhile

nums = range(10)
print(list(filterfalse(lambda n: n % 2 == 0, nums)))   # [1, 3, 5, 7, 9] -- opposite of filter
print(list(takewhile(lambda n: n < 5, nums)))            # [0, 1, 2, 3, 4] -- stops at first failure
print(list(dropwhile(lambda n: n < 5, nums)))            # [5, 6, 7, 8, 9] -- skips until first pass, then keeps the rest
```

**`starmap` — `map`, but unpacking each element as arguments**

```python
from itertools import starmap

pairs = [(2, 3), (4, 5), (10, 2)]
print(list(starmap(pow, pairs)))   # [8, 1024, 100] -- pow(2,3), pow(4,5), pow(10,2)
```

Equivalent to `[pow(*p) for p in pairs]` — useful when each element of the iterable is already a tuple of arguments.

**Splitting one iterator into several — `tee`**

```python
from itertools import tee

source = (x * x for x in range(5))
first_pass, second_pass = tee(source, 2)

print(list(first_pass))    # [0, 1, 4, 9, 16]
print(list(second_pass))   # [0, 1, 4, 9, 16] -- an independent second read over the same source
```

A generator can normally only be consumed once. `tee` gives `n` independent iterators drawn from the same source, useful whenever the same stream needs to be processed two different ways. `tee` buffers whatever one branch has produced but the other hasn't consumed yet, so tee-ing a very large or infinite source and reading one branch far ahead of the other can use a surprising amount of memory — it is not free duplication.

## **A Mental Map of `itertools`**

| Category | Tools |
| --- | --- |
| Reshaping | `chain`, `chain.from_iterable`, `islice`, `batched`, `pairwise`, `groupby` |
| Filtering | `filterfalse`, `takewhile`, `dropwhile`, `compress` |
| Combinatorial | `product`, `permutations`, `combinations`, `combinations_with_replacement` |
| Infinite | `count`, `cycle`, `repeat` |
| Combining with other tools | `accumulate`, `starmap`, `zip_longest` |
| Forks | `tee` |

## **Common Mistakes**

- Caching a function with side effects or non-deterministic output using `lru_cache` or `cache` — the same arguments will always return the first cached result, so a function that reads the current time, generates a random number, or performs an action that should genuinely happen every time silently returns stale data after the first call.
- Passing a mutable argument such as a list or dict to a function decorated with `lru_cache` — the cache uses arguments as a dict key internally, so unhashable arguments raise `TypeError: unhashable type`; pass a tuple instead.
- Forgetting to sort the data before `itertools.groupby`, which only groups consecutive matching elements rather than performing a true SQL-style group-by across the whole collection.
- Confusing `functools.partial` with a lambda when actual computation is needed — `partial` can only pre-fill arguments, not add new logic; a lambda or full function is required once any transformation beyond argument-filling happens.
- Forgetting to wrap an `itertools` result in `list(...)` (or otherwise iterate it) and then being surprised that printing it shows a generic iterator object instead of the actual values.
- Using `lru_cache` on a method for per-instance caching, which keeps every instance alive indefinitely since the cache is shared and keyed globally; `cached_property` is the correct tool when the cached value belongs to one specific object.
- Reading far ahead on one branch of a `tee`-split iterator while barely touching the other, which causes `tee` to buffer a large number of unconsumed items internally, using far more memory than expected.

## **Production Patterns**

**Caching a config lookup and batching student records for grading — combining both modules**

```python
from functools import lru_cache
from itertools import batched

@lru_cache(maxsize=256)
def get_grade_boundary(subject):
    # imagine this calls a slow lookup service
    return {"Python": 40, "Java": 45, "Blockchain": 50}[subject]

student_ids = list(range(1, 23))
for batch in batched(student_ids, 5):
    print(f"grading batch: {batch}")
```

**Dispatching handling logic by payload type in an API**

```python
from functools import singledispatch

@singledispatch
def handle_upload(payload):
    raise TypeError(f"unsupported payload: {type(payload)}")

@handle_upload.register
def _(payload: dict):
    return f"processed structured payload with keys {list(payload.keys())}"

@handle_upload.register
def _(payload: str):
    return f"processed raw text payload of length {len(payload)}"
```

**Grouping log entries by severity for a report**

```python
from itertools import groupby

log_entries = [
    {"level": "INFO", "message": "startup complete"},
    {"level": "ERROR", "message": "connection refused"},
    {"level": "ERROR", "message": "timeout"},
    {"level": "INFO", "message": "shutdown"},
]

log_entries.sort(key=lambda e: e["level"])
for level, group in groupby(log_entries, key=lambda e: e["level"]):
    print(level, "->", [g["message"] for g in group])
```

| Library / Tool | Key Feature | Best Use Case |
| --- | --- | --- |
| `functools.lru_cache` / `cache` | Automatic memoization by argument | Expensive lookups, config caching, singleton clients |
| `functools.partial` | Pre-fills arguments on a function | Callback registration, pipeline step configuration |
| `functools.singledispatch` | Type-based dispatch without `isinstance` chains | Handling multiple payload shapes in APIs and pipelines |
| `functools.cached_property` | Per-instance memoization | Expensive attributes tied to one object's lifetime |
| `itertools.batched` | Fixed-size chunking of a stream | Bulk API requests, ML training batches |
| `itertools.groupby` | Groups consecutive matching elements | Reports and summaries over sorted data |
| `itertools.tee` | Splits one iterator into several independent reads | Processing the same stream in more than one way |

## **Modern Python Patterns**

Manually chunking an iterable used to require a hand-written generator wrapped around `itertools.islice`.

```python
from itertools import islice

def batched(iterable, size):
    it = iter(iterable)
    while batch := list(islice(it, size)):
        yield batch
```

Since Python 3.12, `itertools.batched` provides this directly from the standard library, with an optional `strict=True` to catch incomplete final batches.

```python
from itertools import batched   # Python 3.12+

for batch in batched(range(1, 23), 5, strict=False):
    print(batch)
```

Overload-style dispatch used to mean a growing `if isinstance(...)` chain; `functools.singledispatch` replaces it with independently registered, independently testable functions per type.

| Older Style | Modern Style |
| --- | --- |
| Hand-written `batched()` generator using `itertools.islice` | `itertools.batched(iterable, n, strict=False)`, built in since 3.12 |
| A growing `if isinstance(...)` ladder for type-based behavior | `@singledispatch` with `@func.register` per type |
| `functools.partial` combined with a manually written wrapper for method binding | `functools.partialmethod`, which correctly waits to bind `self` |

## **Quick Reference**

| Pattern | Syntax | Purpose |
| --- | --- | --- |
| Memoize, bounded | `@lru_cache(maxsize=128)` | Cache results, evicting least-recently-used entries |
| Memoize, unbounded | `@cache` | Cache results with no eviction (3.9+) |
| Per-instance cache | `@cached_property` | Cache a computed attribute on one object |
| Pre-fill arguments | `partial(func, *args, **kwargs)` | Build a specialized callable from a general one |
| Fold to one value | `reduce(func, iterable, initial)` | Accumulate an iterable down to a single result |
| Type-based dispatch | `@singledispatch` + `@func.register` | Replace an `isinstance` chain with per-type functions |
| Fill in comparisons | `@total_ordering` | Derive `<=`, `>`, `>=` from `__eq__` and `__lt__` |
| Combine iterables | `chain(a, b)` | Treat several iterables as one sequence |
| Infinite sequence | `count()`, `cycle(seq)`, `repeat(value)` | Generate unending sequences |
| Group consecutive items | `groupby(sorted_iterable, key=fn)` | Bucket sorted data by key |
| All pairings | `product(a, b)` | Every combination across inputs |
| Ordered arrangements | `permutations(seq, r)` | Every ordered selection of length `r` |
| Unordered selections | `combinations(seq, r)` | Every unordered selection of length `r` |
| Lazy slice | `islice(iterable, n)` | Take the first `n` items without materializing the rest |
| Fixed-size batches | `batched(iterable, n)` (3.12+) | Chunk a stream for APIs or ML training |
| Fork a stream | `tee(iterable, n)` | Create `n` independent reads over one source |