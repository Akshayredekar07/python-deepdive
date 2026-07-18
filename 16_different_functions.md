# **Python Functions **

## **3.0 The One Big Idea**

Python treats functions as first-class citizens. A function is a regular value — the same kind of value as an `int`, a `str`, a `list`. That means you can:

1. Pass functions as arguments to other functions.
2. Return functions from other functions.
3. Assign functions to variables (aliasing).
4. Store functions in lists, dicts, sets.
5. Define functions inside other functions.

```python
def transform(values, fn):
    return [fn(v) for v in values]

def make_step():
    def step(x):
        return x + 1
    return step

square  = lambda x: x * x
results = map(square, [1, 2, 3])
evens   = filter(lambda n: n % 2 == 0, [1, 2, 3, 4])
```

If those lines feel natural, the rest of this file is mostly about pushing on the corners and seeing where the pattern shows up in real code.

---

## **3.1 Passing Functions As Arguments (Callbacks)**

A callback is a function you hand to another piece of code so that code can call it later, possibly many times. It is the most common practical use of first-class functions.

**Why this matters.** Most real systems have to react to events that happen at unpredictable times — a button click, a row arriving in a stream, an HTTP request, an LLM finishing a streaming token. In each case you write the reaction as a function and hand it to the framework; the framework calls it at the right moment.

### **3.1.1 The Basic Shape**

```python
def apply_twice(f, x):
    return f(f(x))

def inc(n):    return n + 1
def square(n): return n * n

print(apply_twice(inc, 5))      # 7,  inc(inc(5))
print(apply_twice(square, 3))   # 81, square(square(3))
```

### **3.1.2 Built-in Callbacks You Already Use**

| Function | Callback role | What gets passed |
| --- | --- | --- |
| `sorted(iter, key=fn)` | Per-element sort key | `fn(element)` |
| `min(iter, key=fn)` / `max(iter, key=fn)` | Per-element key | `fn(element)` |
| `map(fn, iter)` | Per-element transform | `fn(element)` |
| `filter(fn, iter)` | Per-element predicate | `fn(element)` returns bool |
| `functools.reduce(fn, iter)` | Pairwise combiner | `fn(acc, element)` |
| `list.sort(key=fn)` | Per-element sort key | `fn(element)` |
| `itertools.groupby(iter, key=fn)` | Group-by key | `fn(element)` |
| `threading.Thread(target=fn)` | The work to run | `fn()` |
| `asyncio.TaskGroup` / `asyncio.gather` | Concurrent coroutines | `coro()` |
| `concurrent.futures.ThreadPoolExecutor.map(fn, iter)` | Parallel transform | `fn(element)` |
| `aiohttp.ClientSession` middleware | Request/response hooks | `fn(req)` / `fn(resp)` |
| `pytest` fixtures / parametrize | Setup, per-test data | `fn()` |
| `FastAPI` dependencies | Per-request callable | `fn(request)` |
| `pydantic` validators | Field-level checks | `fn(value)` |
| `logging.Filter` | Per-record decision | `fn(record)` -> bool |

### **3.1.3 Multiple Callbacks — a Pipeline**

```python
def pipeline(value, *fns):
    for fn in fns:
        value = fn(value)
    return value

strip    = str.strip
title    = str.title
collapse = lambda s: " ".join(s.split())

result = pipeline("   hello   world  ", strip, title, collapse)
print(repr(result))   # 'Hello World'
```

A list of stages applied in sequence — the foundation of data ETL, model preprocessing, middleware chains, and LLM tool orchestration.

### **3.1.4 Callbacks That Return a Boolean — Predicates**

```python
def is_adult(user):   return user["age"] >= 18
def is_active(user):  return user.get("active", False)
def has_email(user):  return bool(user.get("email"))

users = [
    {"name": "Aarav", "age": 36, "active": True,  "email": "aarav@x.io"},
    {"name": "Priya", "age": 15, "active": True,  "email": "priya@x.io"},
    {"name": "Kenji", "age": 28, "active": False, "email": ""},
    {"name": "Yuki",  "age": 42, "active": True,  "email": "yuki@x.io"},
]

eligible = list(filter(lambda u: is_adult(u) and is_active(u) and has_email(u), users))
print([u["name"] for u in eligible])   # ['Aarav', 'Yuki']
```

### **3.1.5 Callbacks That Return a Transformed Value — Projections / Mappers**

```python
def get_name(user): return user["name"]
def get_age(user):  return user["age"]

names  = list(map(get_name, users))       # ['Aarav', 'Priya', 'Kenji', 'Yuki']
ages   = list(map(get_age, users))        # [36, 15, 28, 42]
oldest = max(users, key=get_age)
```

### **3.1.6 Callbacks That Aggregate**

```python
from functools import reduce

def add_to_set(acc, item):
    acc.add(item)
    return acc

unique_tags = reduce(add_to_set, ["py", "ml", "py", "ai", "ml"], set())
print(unique_tags)   # {'py', 'ml', 'ai'}
```

### **3.1.7 A Small Event System**

```python
class EventBus:
    def __init__(self):
        self._handlers = {}

    def on(self, event, handler):
        self._handlers.setdefault(event, []).append(handler)

    def emit(self, event, **payload):
        for handler in self._handlers.get(event, []):
            handler(**payload)

bus = EventBus()
bus.on("user_signup", lambda **kw: print(f"[log] new user: {kw}"))
bus.on("user_signup", lambda **kw: print(f"[mail] welcome email to {kw['name']}"))

bus.emit("user_signup", name="Aarav", email="aarav@x.io")
```

This is exactly how logging frameworks, GUI toolkits, and AI SDKs work internally.

### **3.1.8 Common Mistake — Signature Mismatch**

The framework expects a callback to accept a specific set of arguments. If your function's signature does not match, you get `TypeError` at call time, not at registration time.

```python
def safe_handler(token: str, **kwargs):
    ...
```

Accepting `**kwargs` is the defensive pattern — it lets the framework add new keyword arguments in future versions without breaking your handler. This is exactly why LangChain's callback methods are all defined as `(self, ..., **kwargs)`.

### **3.1.9 AI SDK — OpenAI's `event_hooks`**

```python
from openai import OpenAI
import httpx

def log_request(request):
    print(f"-> {request.method} {request.url}")

def log_response(response):
    print(f"<- {response.status_code}")

client = OpenAI(
    http_client=httpx.Client(
        event_hooks={"request": [log_request], "response": [log_response]}
    )
)
```

`event_hooks` maps `"request"` and `"response"` to lists of callback functions — the same `EventBus` pattern from §3.1.7, with the framework owning the dispatch.

### **3.1.10 AI SDK — OpenAI's Streaming Iterator**

```python
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Tell me a short joke."}],
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta.content or ""
    print(delta, end="", flush=True)
```

The `for` loop is consuming an iterator; each iteration is a callback the SDK is calling under the hood to push the next chunk.

### **3.1.11 AI SDK — LangChain's `BaseCallbackHandler`**

```python
from langchain_core.callbacks import BaseCallbackHandler

class TokenCounterHandler(BaseCallbackHandler):
    def __init__(self):
        self.tokens = 0

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.tokens += 1
        print(token, end="", flush=True)

    def on_llm_end(self, response, **kwargs) -> None:
        print(f"\nstreamed {self.tokens} tokens")
```

Every method on `BaseCallbackHandler` (`on_chain_start`, `on_llm_new_token`, `on_tool_start`, `on_agent_action`, and so on) is a callback the framework calls on your behalf.

### **3.1.12 Modern Backend — FastAPI Dependency Injection**

FastAPI's `Depends` accepts a callable and runs it on every request — the dependency function is a callback the framework calls for you.

```python
from fastapi import FastAPI, Depends, Header, HTTPException

app = FastAPI()

def get_current_user(authorization: str = Header(...)) -> dict:
    # In a real app, decode the JWT here
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="bad token")
    return {"name": "Aarav", "role": "admin"}

@app.get("/me")
def read_me(user: dict = Depends(get_current_user)):
    return user
```

`get_current_user` is a function passed to `Depends`, which calls it on every request. The return value is injected into `read_me`.

### **3.1.13 Modern Backend — `concurrent.futures.Executor.map` (Parallel Map)**

`concurrent.futures` ships a parallel version of `map` — same callback shape, but across threads or processes.

```python
from concurrent.futures import ThreadPoolExecutor
import urllib.request

urls = [
    "https://example.com",
    "https://example.org",
    "https://example.net",
]

def fetch(url: str) -> tuple[str, int]:
    with urllib.request.urlopen(url) as r:
        return url, r.status

# Same shape as the built-in map, but runs across a thread pool
with ThreadPoolExecutor(max_workers=8) as ex:
    results = list(ex.map(fetch, urls))

print(results)
# [('https://example.com', 200), ('https://example.org', 200), ('https://example.net', 200)]
```

`fetch` is a function passed in; the executor calls it once per URL in parallel. Same Stage 3 first-class-function idea, just concurrent.

### **3.1.14 Modern Backend — `asyncio.TaskGroup` (Structured Concurrency)**

The async version of "run these callables in parallel":

```python
import asyncio

async def fetch_status(url: str) -> int:
    # pretend we use aiohttp here
    await asyncio.sleep(0.1)
    return 200

async def main():
    urls = ["https://example.com", "https://example.org", "https://example.net"]
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch_status(u)) for u in urls]
    print([t.result() for t in tasks])

asyncio.run(main())
```

Each `fetch_status` is a coroutine; `TaskGroup` schedules them concurrently and waits for all of them — same "function handed off to a scheduler" pattern as `ThreadPoolExecutor.map`, just on the event loop.

### **3.1.15 Modern Backend — `structlog` Processor Chain**

`structlog` builds log records by passing them through a chain of processor functions — each one is a callback.

```python
import structlog

def add_app_name(logger, method_name, event_dict):
    event_dict["app"] = "billing-service"
    return event_dict

def drop_debug(logger, method_name, event_dict):
    if event_dict.get("level") == "debug":
        raise structlog.DropEvent
    return event_dict

log = structlog.get_logger().bind(user="aarav")
log.info("payment charged", amount=99, level="info")
# app='billing-service' user='aarav' amount=99 event='payment charged'
```

A `structlog` processor is just a function with a known signature — same "first-class function in a chain" pattern as the pipeline in §3.1.3.

---

## **3.2 Returning Functions From Functions**

The other half of the first-class-functions idea. If functions can be passed in, they can also be returned out.

### **3.2.1 The Basic Shape**

```python
def make_logger(prefix):
    def logger(msg):
        print(f"[{prefix}] {msg}")
    return logger

info = make_logger("INFO")
warn = make_logger("WARN")

info("ready")     # [INFO] ready
warn("low disk")  # [WARN] low disk
```

`info` and `warn` are different function objects, each capturing a different `prefix`.

### **3.2.2 Function Factories**

```python
def make_power(exponent):
    def power(base):
        return base ** exponent
    return power

square = make_power(2)
cube   = make_power(3)

print(square(5))    # 25
print(cube(2))      # 8
```

The frozen value each factory produces is held in a closure — the full topic of Stage 4.

### **3.2.3 Conditional Return — Strategy / Dispatch**

```python
def make_printer(style):
    if style == "upper": return str.upper
    if style == "lower":  return str.lower
    if style == "title":  return str.title
    return str

p = make_printer("title")
print(p("hello world"))    # Hello World
```

### **3.2.4 Returning a Bound Method vs a Raw Function**

```python
class Greeter:
    def __init__(self, name):
        self.name = name
    def hello(self):
        return f"Hello, {self.name}"

g = Greeter("Aarav")
m = g.hello        # bound method, self is already wired up
print(m())          # Hello, Aarav
```

### **3.2.5 Pickling / Serialization Factories**

```python
import json
import pickle

def make_serializer(fmt="json"):
    if fmt == "json":
        def serialize(obj):   return json.dumps(obj).encode("utf-8")
        def deserialize(b):   return json.loads(b.decode("utf-8"))
    elif fmt == "pickle":
        def serialize(obj):   return pickle.dumps(obj)
        def deserialize(b):   return pickle.loads(b)
    else:
        raise ValueError(fmt)
    return serialize, deserialize

s_j, d_j = make_serializer("json")
s_p, d_p = make_serializer("pickle")

data = {"name": "Aarav", "scores": [99, 98, 100]}
print(d_j(s_j(data)))     # {'name': 'Aarav', 'scores': [99, 98, 100]}
print(d_p(s_p(data)))     # {'name': 'Aarav', 'scores': [99, 98, 100]}
```

### **3.2.6 AI SDK — Decorator Factories**

```python
def retry(max_attempts=3, on=Exception):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except on as e:
                    if attempt == max_attempts:
                        raise
                    print(f"  attempt {attempt} failed: {e!r}; retrying...")
        return wrapper
    return decorator

@retry(max_attempts=3, on=ValueError)
def flaky_llm_call(prompt):
    import random
    if random.random() < 0.6:
        raise ValueError("rate limited")
    return f"OK: {prompt}"
```

`@retry(max_attempts=3, on=ValueError)` is a factory call — `retry(...)` runs immediately and returns the actual decorator, which then wraps `flaky_llm_call`. Real SDKs use this exact shape: `tenacity`'s `@retry(...)`, LangChain's `@tool`, Pydantic's `@field_validator(...)`, and FastAPI's `@app.get(...)` are all "factory returns a decorator."

### **3.2.7 AI SDK — Turning a Function Into a Tool**

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get the current weather in a given city."""
    return f"Sunny, 22C in {city}"

print(get_weather.name)                       # get_weather
print(get_weather.invoke({"city": "Tokyo"}))  # Sunny, 22C in Tokyo
```

`@tool` reads the function's name, docstring, and annotations to build a description the model can use, then wraps the original function so the SDK can call it later by name.

### **3.2.8 AI SDK — Closure-Based Rate Limiter**

```python
import time

def make_rate_limiter(max_per_second):
    min_interval = 1.0 / max_per_second
    last_call = [0.0]

    def throttle():
        now = time.monotonic()
        wait = min_interval - (now - last_call[0])
        if wait > 0:
            time.sleep(wait)
        last_call[0] = time.monotonic()
    return throttle

limit = make_rate_limiter(5)   # at most 5 calls per second
```

`throttle` closes over `min_interval` and `last_call`. Every SDK rate limiter is some variant of this pattern.

### **3.2.9 Modern Backend — FastAPI / Flask Route Factories**

Web frameworks hand you back a callable (the route handler) that you can pass around, register, or wrap.

```python
from fastapi import FastAPI

app = FastAPI()

def make_user_router(prefix: str):
    router = APIRouter(prefix=prefix)

    @router.get("/")
    def list_users():
        return [{"name": "Aarav"}, {"name": "Priya"}]

    @router.get("/{uid}")
    def get_user(uid: int):
        return {"uid": uid, "name": "Aarav"}
    return router

app.include_router(make_user_router("/api/v1/users"))
app.include_router(make_user_router("/api/v2/users"))
```

`make_user_router` is a function factory that returns a configured `APIRouter`; same shape as `make_logger` in §3.2.1.

### **3.2.10 Modern Backend — Pydantic Field Validators**

`@field_validator` is a decorator factory that registers a function as a validator for a Pydantic model field.

```python
from pydantic import BaseModel, field_validator

class Signup(BaseModel):
    email: str
    handle: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator("handle")
    @classmethod
    def check_handle(cls, v: str) -> str:
        if not v.replace("_", "").isalnum():
            raise ValueError("handle must be alphanumeric")
        return v.lower()

Signup(email="  Aarav@X.io  ", handle="Aarav_Dev")
# Signup(email='aarav@x.io', handle='aarav_dev')
```

`normalize_email` and `check_handle` are functions; Pydantic calls them at validation time. Same first-class-function pattern as LangChain's callbacks.

### **3.2.11 Modern Backend — Celery Task Factories**

Celery's `@shared_task` is a decorator factory that turns a function into a queued background task.

```python
from celery import shared_task

@shared_task(bind=True, max_retries=3)
def send_welcome_email(self, user_id: int) -> str:
    # ... send the email ...
    return f"sent to {user_id}"

# Call it
send_welcome_email.delay(user_id=42)
```

`@shared_task(...)` is a factory call; the returned decorator wraps `send_welcome_email` and gives it a `.delay()` method.

---

## **3.3 Lambda Functions**

A lambda is a small anonymous function defined inline. It is a plain function — the body is a single expression whose value is returned automatically.

### **3.3.1 Syntax and Rules**

```python
square = lambda x: x * x
add    = lambda a, b: a + b
upper  = lambda s: s.upper()
always = lambda: 42               # zero-argument lambda
```

`lambda` is an expression, not a statement — it can appear anywhere an expression is valid. The body must be a single expression; you cannot use `return`, `if` as a statement, `for`, `while`, or `assert` inside one. There is no docstring.

```python
square = lambda x: x * x                                  # valid
sign   = lambda n: "positive" if n > 0 else "non-positive" # valid, ternary expression
point  = lambda x, y: (x, y)                                # valid, returns a tuple

# bad = lambda x: return x * 2      -- SyntaxError
# bad = lambda x: x = x + 1         -- SyntaxError, assignment not allowed
```

### **3.3.2 When to Use a Lambda**

All four should be true: the logic is trivial and doesn't deserve a name; the lambda genuinely reads better than a named function would; nothing built-in already does this; the team is comfortable reading lambdas.

```python
items.sort(key=lambda x: x.priority)
emails = list(map(lambda u: u.email, users))
adults = list(filter(lambda u: u.age >= 18, users))
button.on_click(lambda: print("clicked"))
handlers = {"json": lambda s: json.loads(s), "yaml": lambda s: yaml.safe_load(s)}
```

### **3.3.3 When Not to Use a Lambda**

PEP 8: "Always use a `def` statement instead of an assignment statement that binds a lambda expression directly to an identifier."

```python
square = lambda x: x * x     # PEP 8 violation

def square(x):                 # correct
    return x * x
```

Also avoid lambdas that are too long, nested (`lambda x: lambda y: x + y`), or that you find yourself wanting to comment — that is the signal to write a `def` instead.

### **3.3.4 Lambdas in the Wild**

```python
pairs = [("Aarav", 36), ("Priya", 22), ("Kenji", 41)]
print(sorted(pairs, key=lambda p: p[1]))
# [('Priya', 22), ('Aarav', 36), ('Kenji', 41)]

is_blank = lambda s: not s.strip()
print(is_blank("   "), is_blank("hi"))    # True False

cents_to_dollars = lambda c: c / 100
print(cents_to_dollars(199))               # 1.99

add_curried = lambda a: lambda b: a + b
print(add_curried(3)(4))                    # 7
```

### **3.3.5 `if/else` Inside a Lambda — Nested Ternaries**

```python
classify = lambda n: "big" if n > 100 else ("small" if n < 10 else "medium")
print(classify(5))     # small
print(classify(500))   # big
```

If the body needs more than one or two ternaries, write a `def` instead.

### **3.3.6 Lambdas in Dict / List / Set Literals — the Dispatch Table Again**

```python
operations = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b,
    "mul": lambda a, b: a * b,
    "div": lambda a, b: a / b if b != 0 else float("inf"),
}
print(operations["add"](2, 3))    # 5
```

### **3.3.7 Capturing Variables — a Closure Preview**

A lambda, like any nested function, references names from its enclosing scope by name, not by value — the name is looked up when the lambda runs, not when it is created.

```python
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])     # [2, 2, 2] -- all see the final value of i

funcs = [lambda i=i: i for i in range(3)]
print([f() for f in funcs])     # [0, 1, 2] -- fixed with a default argument
```

### **3.3.8 Modern Data — Pandas, sklearn, Polars**

```python
import pandas as pd

df = pd.DataFrame({"name": ["Aarav", "Priya", "Kenji"], "score": [0.91, 0.45, 0.78]})

df["grade"] = df["score"].map(lambda s: "pass" if s >= 0.5 else "fail")
high = df[df["score"].map(lambda s: s > 0.7)]
df_sorted = df.sort_values(by="score", key=lambda s: -s)
```

```python
from sklearn.preprocessing import FunctionTransformer
clean = FunctionTransformer(lambda X: X.fillna(0).clip(lower=0))
```

```python
import polars as pl
# Polars also accepts lambdas in many places
df = pl.DataFrame({"x": [1, 2, 3]})
out = df.with_columns(pl.col("x").map_elements(lambda v: v * 10, return_dtype=pl.Int64))
print(out)
# shape: (3, 1)
# ┌─────┐
# │ x   │
# │ --- │
# │ i64 │
# ╞═════╡
# │ 10  │
# │ 20  │
# │ 30  │
# └─────┘
```

`Series.map(...)`, `FunctionTransformer`, and Polars' `map_elements` are all the same "function handed to a library method" pattern.

### **3.3.9 Modern Backend — SQLAlchemy `column_property` and Hybrid Expressions**

SQLAlchemy's `column_property` accepts a callable that produces a SQL expression — same "function passed in to be called later" pattern.

```python
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, column_property

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first = Column(String)
    last  = Column(String)

    # A hybrid property: callable evaluated by SQLAlchemy
    full_name = column_property(lambda cls: cls.first + " " + cls.last)
```

### **3.3.10 Modern Backend — pytest `parametrize` and Fixtures**

`pytest.mark.parametrize` accepts a function for indirect parametrization; fixtures are callables that pytest calls per test.

```python
import pytest

@pytest.fixture
def user():
    return {"name": "Aarav", "role": "admin"}

@pytest.mark.parametrize("n,expected", [(1, 1), (2, 4), (3, 9)])
def test_square(n, expected, square):
    assert square(n) == expected
```

`square` would itself be a fixture returning a function — pure first-class-function plumbing all the way through.

---

## **3.4 `map`, `filter`, and `reduce`**

These three are the canonical "functional Python" toolkit. Each takes a function and an iterable and produces a result. All three are lazy in modern Python — they return iterators, not lists, so wrap them in `list(...)` to see the values.

| Function | Module | Returns | Mental model |
| --- | --- | --- | --- |
| `map(fn, iter)` | built-in | iterator of `fn(x)` | transform every element |
| `filter(fn, iter)` | built-in | iterator of `x` where `fn(x)` is truthy | keep elements that pass the test |
| `functools.reduce(fn, iter, init)` | `functools` | a single accumulated value | fold the iterable down to one value |
| `itertools.accumulate(iter, fn, initial)` | `itertools` | iterator of running values | reduce, but keep every intermediate step |

### **3.4.1 `map` — Apply a Function to Every Element**

```python
def square(x): return x * x

result = map(square, [1, 2, 3, 4, 5])
print(list(result))     # [1, 4, 9, 16, 25]
```

Without lambda, then with one:

```python
def doubleIt(x):
    return 2 * x

nums = [1, 2, 3, 4, 5]
print(list(map(doubleIt, nums)))            # [2, 4, 6, 8, 10]
print(list(map(lambda x: 2 * x, nums)))     # [2, 4, 6, 8, 10]
```

**`map` is lazy** — nothing is computed until you iterate:

```python
big = map(lambda x: x * x, range(10_000_000))
total = sum(big)     # one pass, no intermediate list ever built
```

**Common mistake — a `map` object can only be iterated once.**

```python
m = map(lambda x: x * x, [1, 2, 3])
print(list(m))   # [1, 4, 9]
print(list(m))   # []  -- already consumed
```

**`map` with multiple iterables** — `map(fn, iter1, iter2, ...)` calls `fn(a, b, ...)` taking one element from each in lockstep.

```python
l1 = [1, 2, 3, 4]
l2 = [2, 3, 4, 5]
l3 = list(map(lambda x, y: x * y, l1, l2))
print(l3)   # [2, 6, 12, 20]
```

### **3.4.2 `map` Examples — Basic Numeric Transforms**

```python
# 1. Square each number
list(map(lambda x: x * x, [1, 2, 3, 4]))                        # [1, 4, 9, 16]

# 2. Power of two for a range
list(map(lambda x: 2 ** x, range(5)))                              # [1, 2, 4, 8, 16]

# 3. Round to 2 decimals
list(map(lambda x: round(x, 2), [3.14159, 2.71828, 1.41421]))     # [3.14, 2.72, 1.41]

# 4. Convert a list of ints to floats
list(map(float, [1, 2, 3]))                                       # [1.0, 2.0, 3.0]
```

### **3.4.3 `map` Examples — String Operations**

```python
# 5. Uppercase a list of strings
list(map(str.upper, ["aarav", "priya", "kenji"]))                # ['AARAV', 'PRIYA', 'KENJI']

# 6. Get the length of each string
list(map(len, ["hi", "hello", ""]))                              # [2, 5, 0]

# 7. Strip and lowercase, chained
list(map(str.strip, map(str.lower, ["  AARAV  ", " Priya "])))   # ['aarav', 'priya']

# 8. Format a list of prices
prices = [9.5, 19.99, 100]
list(map(lambda p: f"${p:.2f}", prices))                         # ['$9.50', '$19.99', '$100.00']
```

### **3.4.4 `map` Examples — Type Conversions**

```python
# 9. Convert strings to int
list(map(int, ["1", "2", "3"]))                                 # [1, 2, 3]

# 10. Parse "key=value" strings
list(map(lambda kv: kv.split("="), ["a=1", "b=2", "c=3"]))       # [['a','1'], ['b','2'], ['c','3']]

# 11. Celsius to Fahrenheit for a whole list
celsius = [0, 20, 37, 100]
list(map(lambda c: c * 9 / 5 + 32, celsius))                     # [32.0, 68.0, 98.6, 212.0]
```

### **3.4.5 `map` Examples — Multi-Iterable / Parallel**

```python
# 12. Element-wise add across two lists
list(map(lambda a, b: a + b, [1, 2, 3], [10, 20, 30]))            # [11, 22, 33]

# 13. Combine three lists at once
names  = ["Aarav", "Priya"]
ages   = [36, 22]
cities = ["Mumbai", "Berlin"]
list(map(lambda n, a, c: f"{n} ({a}) - {c}", names, ages, cities))
# ['Aarav (36) - Mumbai', 'Priya (22) - Berlin']
```

### **3.4.6 `map` Examples — Function Composition**

```python
# 14. Compose two functions inside a lambda
f = lambda x: x + 1
g = lambda x: x * 2
list(map(lambda x: f(g(x)), [1, 2, 3]))                            # [3, 5, 7]

# 15. Map with enumerate, to keep track of position
words = ["a", "b", "c"]
list(map(lambda pair: f"{pair[0]}:{pair[1]}", enumerate(words)))   # ['0:a', '1:b', '2:c']
```

### **3.4.7 `map` Examples — Dictionary / Record Processing**

```python
# 16. Extract one field from a list of dicts
people = [{"name": "Aarav", "age": 36}, {"name": "Priya", "age": 22}]
list(map(lambda p: p["name"], people))                             # ['Aarav', 'Priya']

# 17. Build formatted strings from a list of dicts
list(map(lambda p: f"{p['name']} is {p['age']}", people))          # ['Aarav is 36', 'Priya is 22']
```

### **3.4.8 `map` Examples — Nested / Matrix Operations**

```python
# 18. Map over a matrix (list of lists) to double every value
matrix = [[1, 2], [3, 4], [5, 6]]
doubled = list(map(lambda row: list(map(lambda x: x * 2, row)), matrix))
print(doubled)   # [[2, 4], [6, 8], [10, 12]]
```

### **3.4.9 `map` Examples — Modern Library Patterns**

```python
# 19. Pandas DataFrame column transform
import pandas as pd
df = pd.DataFrame({"name": ["Aarav", "Priya"], "score": [0.9, 0.4]})
df["grade"] = df["score"].map(lambda s: "pass" if s >= 0.5 else "fail")
# Same idea as list(map(...)), but on a Series

# 20. Polars column map
import polars as pl
pl_df = pl.DataFrame({"x": [1, 2, 3]})
pl_df.with_columns(pl.col("x").map_elements(lambda v: v * 10, return_dtype=pl.Int64))

# 21. ThreadPoolExecutor for parallel map
from concurrent.futures import ThreadPoolExecutor
def double(x):  return x * 2
with ThreadPoolExecutor() as ex:
    out = list(ex.map(double, range(5)))      # [0, 2, 4, 6, 8], computed in parallel

# 22. Pathlib: read every file's contents
from pathlib import Path
files = [Path("a.txt"), Path("b.txt")]
contents = list(map(Path.read_text, files))

# 23. Built-in: tuple of lengths from a tuple of strings
list(map(len, ("hi", "hello", "hey")))    # [2, 5, 3]

# 24. Built-in: ord of every char (handy for checksums, hashing)
list(map(ord, "Aarav"))                   # [65, 97, 97, 114, 97, 118]
```

### **3.4.10 When to Prefer Comprehensions Over `map`/`filter`**

Prefer a comprehension when the logic is simple and fits on one clean line. Reach for `map`/`filter` when you already have a named function to pass in, when you need lazy or streaming behavior over a large or infinite iterator, or when functional style is the established convention in the codebase (pandas, Spark, some scientific code).

```python
[x * x for x in nums if x > 0]                                  # comprehension
list(map(lambda x: x * x, filter(lambda x: x > 0, nums)))        # equivalent, map+filter
```

---

## **3.5 `filter`**

`filter(fn, iterable)` keeps every element `x` for which `fn(x)` is truthy. It's the boolean sibling of `map`.

### **3.5.1 The Basic Shape**

```python
def is_even(n): return n % 2 == 0

print(list(filter(is_even, range(10))))          # [0, 2, 4, 6, 8]
print(list(filter(lambda n: n % 2 == 0, range(10))))   # same, with a lambda
```

Without lambda vs with lambda:

```python
def isEven(x):
    return x % 2 == 0

l = [0, 5, 10, 15, 20, 25, 30]
print(list(filter(isEven, l)))                  # [0, 10, 20, 30]
print(list(filter(lambda x: x % 2 == 0, l)))    # [0, 10, 20, 30]
```

### **3.5.2 `filter(None, ...)` — Drop the Falsy Values**

`filter` only needs a truthy or falsy return value, not literally `True`/`False`. `filter(None, iterable)` is a fast, idiomatic way to drop every falsy value (`0`, `""`, `None`, `[]`, and so on).

```python
list(filter(lambda s: s, ["", "a", "", "b"]))    # ['a', 'b'] -- empty strings are falsy
list(filter(None, ["", "a", "", "b"]))           # ['a', 'b']
list(filter(None, [0, 1, 2, 0, 3]))              # [1, 2, 3]
```

### **3.5.3 `itertools` Siblings — `filterfalse`, `dropwhile`, `takewhile`**

```python
from itertools import filterfalse, dropwhile, takewhile

list(filterfalse(lambda n: n % 2 == 0, range(10)))   # [1, 3, 5, 7, 9]
list(takewhile(lambda n: n < 5, range(10)))           # [0, 1, 2, 3, 4]
list(dropwhile(lambda n: n < 5, range(10)))           # [5, 6, 7, 8, 9]
```

### **3.5.4 `filter` Examples — Basic Numeric Predicates**

```python
# 1. Keep even numbers
list(filter(lambda n: n % 2 == 0, range(10)))                       # [0, 2, 4, 6, 8]

# 2. Keep odd numbers
list(filter(lambda n: n % 2 != 0, range(10)))                       # [1, 3, 5, 7, 9]

# 3. Keep only positive numbers
list(filter(lambda n: n > 0, [-2, -1, 0, 1, 2]))                    # [1, 2]

# 4. Keep only prime numbers
def is_prime(n):
    if n < 2: return False
    return all(n % i != 0 for i in range(2, int(n ** 0.5) + 1))

list(filter(is_prime, range(2, 30)))
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
```

### **3.5.5 `filter` Examples — String Predicates**

```python
# 5. Keep strings that start with a vowel
words = ["apple", "banana", "orange", "kiwi", "umbrella"]
list(filter(lambda w: w[0] in "aeiou", words))                      # ['apple', 'orange', 'umbrella']

# 6. Keep only non-empty strings
list(filter(None, ["", "hi", "", "ok", "no"]))                      # ['hi', 'ok', 'no']

# 7. Keep log lines that contain a keyword
lines = ["INFO start", "DEBUG x=1", "INFO ready", "ERROR oops"]
list(filter(lambda s: "INFO" in s, lines))                          # ['INFO start', 'INFO ready']

# 8. Filter using a regular expression
import re
emails = ["aarav@x.io", "not-an-email", "priya@y.com", "also bad"]
list(filter(lambda s: re.match(r"^[\w.]+@[\w.]+$", s), emails))    # ['aarav@x.io', 'priya@y.com']
```

### **3.5.6 `filter` Examples — Dict / Record Predicates**

```python
# 9. Keep only adults from a list of dicts
users = [{"name": "Aarav", "age": 36}, {"name": "Priya", "age": 15}]
list(filter(lambda u: u["age"] >= 18, users))                       # [{'name': 'Aarav', 'age': 36}]

# 10. Keep only active sessions
sessions = [{"active": True}, {"active": False}, {"active": True}]
list(filter(lambda s: s["active"], sessions))                        # two active sessions

# 11. Filter out None values from a list with missing data
raw = [1, None, 3, None, 5]
list(filter(lambda x: x is not None, raw))                          # [1, 3, 5]

# 12. Filter dicts by a computed field, not a stored one
products = [{"price": 10, "qty": 2}, {"price": 5, "qty": 0}, {"price": 20, "qty": 1}]
list(filter(lambda p: p["price"] * p["qty"] > 0, products))         # first and third
```

### **3.5.7 `filter` Examples — Chained With `map`**

```python
# 13. Keep items where a mapped/derived value passes a test
nums = [1, 2, 3, 4, 5, 6]
list(filter(lambda x: x > 10, map(lambda x: x * x, nums)))           # [16, 25, 36]
```

### **3.5.8 `filter` Examples — Dedupe and Grouping**

```python
# 14. Filter to keep the first occurrence of each key (dedupe)
seen = set()
def first_seen(x):
    if x in seen:
        return False
    seen.add(x)
    return True

list(filter(first_seen, [1, 2, 1, 3, 2, 4]))                         # [1, 2, 3, 4]

# 15. Filter rows of a matrix where the row sum exceeds a threshold
matrix = [[1, 2, 3], [0, 0, 0], [5, 5, 5]]
list(filter(lambda row: sum(row) > 5, matrix))                       # [[1, 2, 3], [5, 5, 5]]
```

### **3.5.9 `filter` Examples — Modern Library Patterns**

```python
# 16. Class method as the predicate
class Product:
    def __init__(self, name, in_stock):
        self.name, self.in_stock = name, in_stock
    def is_available(self):
        return self.in_stock > 0

products = [Product("Pen", 5), Product("Mug", 0), Product("Bag", 2)]
available = list(filter(lambda p: p.is_available(), products))
print([p.name for p in available])                                   # ['Pen', 'Bag']

# 17. Hugging Face datasets.filter
from datasets import load_dataset
ds = load_dataset("imdb", split="train")
ds_short = ds.filter(lambda ex: ex["label"] == 1)
# This is the exact same filter() pattern, just over a dataset.

# 18. SQLAlchemy-style filtering via the `in_` operator (handcrafted)
# (Not stdlib, but illustrates the same idea — filter by predicate.)
records = [{"city": "Mumbai", "active": True},
           {"city": "Berlin", "active": False},
           {"city": "Tokyo",  "active": True}]
active = list(filter(lambda r: r["active"], records))

# 19. pathlib: keep only files that exist
from pathlib import Path
candidates = [Path("a.py"), Path("missing.py"), Path("b.py")]
existing = list(filter(Path.exists, candidates))    # only existing files

# 20. logging.Filter subclass is *literally* a function-like predicate
import logging
class OnlyErrors(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.ERROR
```

---

## **3.6 `functools.reduce`**

`reduce` lives in `functools`, not the builtins, since Python 3. It applies a two-argument function cumulatively across the iterable:

```
reduce(fn, [a, b, c, d], init) = fn(fn(fn(fn(init, a), b), c), d)
```

### **3.6.1 The Basic Shape**

```python
from functools import reduce

reduce(lambda acc, x: acc + x, [1, 2, 3, 4], 0)   # 10
reduce(lambda acc, x: acc + x, [1, 2, 3, 4])      # 10, init defaults to the first element
```

**Why `init` matters.** `reduce(fn, [])` with no `init` raises `TypeError: reduce() of empty iterable with no initial value`. Always pass an `init` if the iterable might be empty.

### **3.6.2 `reduce` Examples — Basic Aggregations**

```python
from functools import reduce

# 1. Sum
reduce(lambda a, b: a + b, [1, 2, 3, 4, 5], 0)                 # 15

# 2. Product
reduce(lambda a, b: a * b, [1, 2, 3, 4], 1)                    # 24

# 3. Max, without using max()
reduce(lambda a, b: a if a > b else b, [3, 1, 4, 1, 5, 9, 2, 6])  # 9

# 4. Min, without using min()
reduce(lambda a, b: a if a < b else b, [3, 1, 4, 1, 5, 9, 2, 6])  # 1

# 5. Concatenate strings
reduce(lambda a, b: a + b, ["py", "th", "on"], "")               # 'python'

# 6. Compute a factorial using reduce instead of recursion
reduce(lambda a, b: a * b, range(1, 6), 1)                         # 120, same as factorial(5)
```

### **3.6.3 `reduce` Examples — Building Data Structures**

```python
# 7. Build a dict from key-value pairs
pairs = [("a", 1), ("b", 2), ("c", 3)]
reduce(lambda d, kv: {**d, kv[0]: kv[1]}, pairs, {})              # {'a': 1, 'b': 2, 'c': 3}

# 8. Flatten a list of lists, one level deep
nested = [[1, 2], [3, 4], [5, 6]]
reduce(lambda acc, xs: acc + xs, nested, [])                      # [1, 2, 3, 4, 5, 6]

# 9. Merge several dicts into one, later keys overwrite earlier ones
dicts = [{"a": 1}, {"b": 2}, {"a": 3, "c": 4}]
reduce(lambda acc, d: {**acc, **d}, dicts, {})                    # {'a': 3, 'b': 2, 'c': 4}

# 10. Group a list of records by a field, into a dict of lists
records = [
    {"category": "fruit", "name": "apple"},
    {"category": "veg",   "name": "carrot"},
    {"category": "fruit", "name": "banana"},
]
def group(acc, r):
    acc.setdefault(r["category"], []).append(r["name"])
    return acc

reduce(group, records, {})
# {'fruit': ['apple', 'banana'], 'veg': ['carrot']}
```

### **3.6.4 `reduce` Examples — Counting and Set Operations**

```python
# 11. Count occurrences of each word
words = ["the", "cat", "the", "dog", "the", "cat"]
reduce(lambda d, w: {**d, w: d.get(w, 0) + 1}, words, {})
# {'the': 3, 'cat': 2, 'dog': 1}

# 12. Find the greatest common divisor across a whole list
import math
reduce(math.gcd, [48, 18, 60, 24])                                # 6

# 13. Find the longest string in a list
words = ["hi", "hello", "hey", "greetings"]
reduce(lambda a, b: a if len(a) > len(b) else b, words)            # 'greetings'
```

### **3.6.5 `reduce` Examples — Multi-Field Accumulators**

```python
# 14. Track a running (count, sum) pair in a single pass
data = [10, 20, 30, 40]
count, total = reduce(lambda acc, x: (acc[0] + 1, acc[1] + x), data, (0, 0))
print(count, total)                                                # 4 100
```

### **3.6.6 `reduce` Examples — Modern Library Patterns**

```python
# 15. Compose a chain of functions (functional composition)
def compose2(f, g):
    return lambda x: f(g(x))

inc   = lambda x: x + 1
double = lambda x: x * 2
fns = [inc, double, inc]
composed = reduce(compose2, fns)
print(composed(5))    # double(5) = 10, inc(10) = 11, inc(11) = 12

# 16. Merge a list of SQLAlchemy session.add operations
# (illustrative; real code uses session.bulk_save_objects)
from sqlalchemy.orm import Session
def add_all(session: Session, objs):
    return reduce(lambda s, o: s + [o], objs, [])

# 17. functools.reduce is used inside Pydantic v2 for field merging
# (it powers the way model fields are resolved in inheritance)

# 18. Standard library: `os.path.join` via reduce
import os
parts = ["var", "log", "app.log"]
path = reduce(os.path.join, parts)        # 'var/log/app.log'

# 19. Standard library: `all` written via reduce
all_ok = reduce(lambda a, x: a and x, [True, True, False], True)  # False

# 20. Standard library: sum a list of Decimals without loss
from decimal import Decimal
reduce(lambda a, b: a + b, [Decimal("0.1"), Decimal("0.2")], Decimal("0"))
# Decimal('0.3')
```

### **3.6.7 `itertools.accumulate` — Reduce With the Running Trail**

Sometimes you want the running combination at every step, not just the final value.

```python
from itertools import accumulate
import operator

list(accumulate([1, 2, 3, 4, 5]))                       # [1, 3, 6, 10, 15]
list(accumulate([3, 1, 4, 1, 5, 9, 2, 6], max))          # [3, 3, 4, 4, 5, 9, 9, 9]
list(accumulate([1, 2, 3, 4], operator.mul))             # [1, 2, 6, 24]
list(accumulate([1, 2, 3], operator.add, initial=10))     # [10, 11, 13, 16]
```

This is the same shape as `reduce`, but it yields the accumulator after each step.

---

## **3.7 A Full `map` + `filter` + `reduce` Pipeline**

"Sum of squares of even numbers from 1 to 10," three different ways:

```python
nums = range(1, 11)

# 1. Comprehension -- usually the most Pythonic choice
sum(x * x for x in nums if x % 2 == 0)     # 220

# 2. map + filter + reduce, functional style
from functools import reduce
squares_of_evens = map(lambda x: x * x, filter(lambda x: x % 2 == 0, nums))
total = reduce(lambda a, b: a + b, squares_of_evens, 0)
print(total)                                # 220

# 3. Fully chained, no intermediate variables
print(reduce(lambda a, b: a + b,
             map(lambda x: x * x, filter(lambda x: x % 2 == 0, nums)),
             0))                            # 220
```

---

## **3.8 Sorting With `key=`**

`key=` is one of the most-used callback patterns in Python. `sorted`, `list.sort`, `min`, and `max` all use it: extract a sort key from each element first, then compare the keys.

### **3.8.1 The Basic Idea**

```python
words = ["banana", "pie", "Apple", "cherry"]

sorted(words)                                  # ['Apple', 'banana', 'cherry', 'pie'], case-sensitive
sorted(words, key=str.lower)                   # case-insensitive comparison
sorted(words, key=len)                         # ['pie', 'Apple', 'banana', 'cherry'], by length
sorted(words, key=lambda w: (len(w), w.lower())) # by length, then alphabetically
```

The `key` function is called exactly once per element to compute its sort key; the keys are then compared, not the original elements.

### **3.8.2 Multi-Key Sorting**

Tuples compare lexicographically, comparing the second element only if the first is equal:

```python
users = [
    {"name": "Aarav", "age": 36}, {"name": "Priya", "age": 22},
    {"name": "Kenji", "age": 41}, {"name": "Yuki",  "age": 36},
]

sorted(users, key=lambda u: (u["age"], u["name"]))     # age ascending, then name ascending
sorted(users, key=lambda u: (-u["age"], u["name"]))    # age descending, then name ascending
```

### **3.8.3 `operator.itemgetter` and `operator.attrgetter`**

Faster and more readable than a lambda for simple field access:

```python
from operator import itemgetter, attrgetter

sorted(users, key=itemgetter("age"))            # same as key=lambda u: u["age"]
sorted(users, key=itemgetter("age", "name"))     # tuple sort on two fields

class User:
    def __init__(self, name, age):
        self.name, self.age = name, age

people = [User("Aarav", 36), User("Priya", 22)]
sorted(people, key=attrgetter("age"))
```

### **3.8.4 `sorted` vs `list.sort`**

`sorted(iterable)` returns a new list, the original is untouched. `list.sort()` sorts in place and returns `None`. `xs = xs.sort()` is a classic real bug — `xs` ends up `None`.

### **3.8.5 Common Mistake — `key` Is Called Once per Element, Not Once per Comparison**

This is exactly why Python's sort is fast, but it also means side effects inside a `key` function run in the iterable's original order, not the sorted order, and a `key` that returns a mutable object can produce wrong results if that object changes after being returned. Always return an immutable value (or a tuple of immutable values) from a `key` function.

### **3.8.6 `sort` Examples — Basic Sorts**

```python
# 1. Sort by length
sorted(["bbb", "a", "cc"], key=len)                             # ['a', 'cc', 'bbb']

# 2. Sort by absolute value
sorted([-5, 2, -3, 1], key=abs)                                 # [1, 2, -3, -5]

# 3. Sort strings case-insensitively
sorted(["b", "A", "C"], key=str.lower)                          # ['A', 'b', 'C']

# 4. Sort by last character
sorted(["apple", "banana", "cherry"], key=lambda s: s[-1])
```

### **3.8.7 `sort` Examples — Tuple and Key Composition**

```python
# 5. Sort tuples by their second element
sorted([(1, 'b'), (1, 'a'), (2, 'c')], key=lambda p: p[1])

# 6. Sort by (priority, name), where "high" priority sorts first
tasks = [("low", "write docs"), ("high", "fix bug"), ("low", "refactor")]
sorted(tasks, key=lambda t: (t[0] != "high", t[1]))

# 7. Sort descending by negating the key
sorted([1, 2, 3, 4, 5], key=lambda n: -n)                        # [5, 4, 3, 2, 1]
```

### **3.8.8 `sort` Examples — Derived and Computed Keys**

```python
# 8. Sort by number of vowels
vowels = "aeiou"
sorted(["apple", "sky", "queue"], key=lambda s: sum(c in vowels for c in s))

# 9. Sort by a computed ratio, descending
results = [{"hits": 10, "misses": 5}, {"hits": 8, "misses": 1}, {"hits": 12, "misses": 8}]
sorted(results, key=lambda r: r["hits"] / max(r["misses"], 1), reverse=True)
```

### **3.8.9 `sort` Examples — Object Attributes**

```python
# 10. Sort by an attribute on objects
from operator import attrgetter
class Comment:
    def __init__(self, text, score):
        self.text, self.score = text, score

comments = [Comment("first", 3), Comment("second", 10), Comment("third", 7)]
sorted(comments, key=attrgetter("score"))
```

### **3.8.10 `sort` Examples — `min` / `max` Instead of `sorted`**

```python
# 11. Sort using min/max to get a single result
users = [{"name": "Aarav", "age": 36}, {"name": "Priya", "age": 22}]
min(users, key=lambda u: u["age"])   # youngest
max(users, key=lambda u: u["age"])   # oldest
```

### **3.8.11 `sort` Examples — Indexing Tricks**

```python
# 12. Find the index of the largest value in a list
nums = [3, 1, 4, 1, 5, 9, 2, 6]
i = max(range(len(nums)), key=lambda i: nums[i])
print(i, nums[i])   # 5 9
```

### **3.8.12 `sort` Examples — Modern Library Patterns**

```python
# 13. pathlib: sort files by size
from pathlib import Path
files = list(Path(".").glob("*.py"))
biggest = max(files, key=lambda f: f.stat().st_size)

# 14. os: sort directory entries by mtime
import os
entries = os.listdir(".")
newest = max(entries, key=lambda name: os.path.getmtime(name))

# 15. dict: sort keys by their value
d = {"aarav": 36, "priya": 22, "kenji": 41}
top = sorted(d, key=d.get)                  # by value
print(top)                                   # ['priya', 'aarav', 'kenji']

# 16. SQLAlchemy: sort by a hybrid expression
# session.query(User).order_by(User.full_name)

# 17. Pandas: DataFrame.sort_values with a custom key
import pandas as pd
df = pd.DataFrame({"name": ["Aarav", "Priya"], "score": [0.91, 0.45]})
df.sort_values(by="score", key=lambda s: -s, inplace=True)

# 18. Pydantic: sort models by a computed field
# sorted(users, key=lambda u: u.age) works the same on Pydantic models

# 19. statistics: median with a key (low+high trick)
import statistics
nums = [3, 1, 4, 1, 5, 9, 2, 6]
median = statistics.median_low(nums)        # 4

# 20. heapq: get the top-K without a full sort
import heapq
top3 = heapq.nlargest(3, nums)              # [9, 6, 5]
```

### **3.8.13 AI SDK — Ranking Retrieved Documents by Score (RAG Re-Ranking)**

```python
retrieved = [
    {"doc_id": 1, "vector_score": 0.71, "recency_days": 30},
    {"doc_id": 2, "vector_score": 0.85, "recency_days": 90},
    {"doc_id": 3, "vector_score": 0.92, "recency_days": 365},
    {"doc_id": 4, "vector_score": 0.78, "recency_days": 2},
]

def rerank_key(d):
    recency_bonus = 1.0 / (1 + d["recency_days"] / 30)
    return d["vector_score"] + 0.2 * recency_bonus

top = sorted(retrieved, key=rerank_key, reverse=True)[:3]
```

Real re-ranking SDKs (Cohere Rerank, LangChain's `CohereRerank`, Jina Rerank) do exactly this — the caller supplies a scoring function, and the library calls it through `key=`, just usually backed by a network call instead of local arithmetic.

### **3.8.14 Modern Backend — Sorting a FastAPI Response In Place**

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/users")
def list_users(sort_by: str = Query("name"), desc: bool = False):
    users = [
        {"name": "Aarav", "age": 36},
        {"name": "Priya", "age": 22},
        {"name": "Kenji", "age": 41},
    ]
    return sorted(users, key=lambda u: u[sort_by], reverse=desc)
```

The same `sorted(..., key=fn, reverse=...)` pattern from the built-in, just inside an HTTP handler. The `key=lambda u: u[sort_by]` lets the client choose the sort field at request time.

---

## **3.9 Putting It All Together — A Small Case Study**

Clean and rank a list of news headlines by importance, ready to feed to an LLM as context — using callbacks, factories, lambdas, `map`, `filter`, and sorting all in one pipeline.

```python
raw_headlines = [
    {"id": 1, "title": "  BREAKING: AI model achieves new SOTA on ImageNet  ", "ts": 1, "src": "wired"},
    {"id": 2, "title": "Local cat wins award",                          "ts": 4, "src": "blog"},
    {"id": 3, "title": "MARKET CRASH: Tech stocks down 30%",            "ts": 2, "src": "reuters"},
    {"id": 4, "title": "Weather: light rain expected",                  "ts": 5, "src": "weather"},
    {"id": 6, "title": "BREAKING: major vulnerability found in libX",   "ts": 1, "src": "hackernews"},
]

normalize = lambda h: {**h, "title": h["title"].strip().lower()}

import re
NEWS_KEYWORDS = re.compile(r"\b(ai|model|market|crash|breaking|vulnerability)\b")
is_news = lambda h: bool(NEWS_KEYWORDS.search(h["title"]))

def importance(h):
    score = 0
    if "breaking" in h["title"]:       score += 10
    if "crash" in h["title"]:          score += 8
    if "vulnerability" in h["title"]:  score += 8
    if h["src"] in {"reuters", "wired"}: score += 5
    if h["src"] == "blog":              score -= 5
    score -= h["ts"]
    return {**h, "score": score}

def chain_news_pipeline(headlines, k=3):
    step1 = map(normalize, headlines)                # normalize
    step2 = filter(is_news, step1)                    # drop non-news
    step3 = map(importance, step2)                    # score
    step4 = sorted(step3, key=lambda h: -h["score"])   # sort by score, descending
    return step4[:k]                                  # top k

top = chain_news_pipeline(raw_headlines, k=3)
for h in top:
    print(f"[{h['score']:>3}] ({h['src']:11s}) {h['title']}")
```

What is used from Stage 3: `normalize`, `is_news`, and `importance` are callbacks passed to `map`/`filter`/`sorted`; the pipeline itself is a `map` + `filter` + `map` + `sorted` chain; the final sort uses a lambda key. The entire thing is first-class functions, from top to bottom.

---

## **3.10 Cheat Sheet — Stage 3**

```python
# Callbacks
def apply(f, x): return f(x)
bus.on("login", lambda u: print(u))

# Modern callback surfaces
Depends(get_current_user)              # FastAPI
ex.map(fetch, urls)                     # ThreadPoolExecutor
await asyncio.gather(coro1(), coro2())  # asyncio
handler = TokenCounterHandler()         # LangChain
hooks = {"request": [log_request]}      # OpenAI / httpx

# Returning functions (factories)
def make_step(n):
    def step(x): return x + n
    return step
inc = make_step(1)

# Lambdas
square = lambda x: x * x                     # fine inline, avoid naming it directly
sorted(words, key=lambda w: w.lower())

# map / filter / reduce
list(map(str.strip, ["  a  ", " b "]))                     # ['a', 'b']
list(filter(lambda n: n > 0, [-1, 0, 1, 2]))                # [1, 2]
from functools import reduce
reduce(lambda a, b: a + b, [1, 2, 3], 0)                    # 6

# Sorting with key
sorted(users, key=lambda u: u["age"])
sorted(users, key=itemgetter("age"))
sorted(users, key=lambda u: (-u["score"], u["name"]))        # multi-key
max(items, key=lambda x: x.score)
```

**One-line mental model.** If you have a function and an iterable, you can transform it (`map`), filter it (`filter`), fold it (`reduce`), or order it (`sorted(..., key=...)`). If you have a function and some configuration, you can produce a configured function (a factory). That covers the entire stage.

---

## **3.11 Quick Self-Test**

1. What is the difference between a callback, a predicate, a projection, and a reducer?
2. Why can a `map` object only be iterated once, and what is the fix if you need to use the result twice?
3. What is the difference between `filter(lambda s: s, items)` and `filter(None, items)`?
4. Why does `reduce(fn, [])` with no initial value raise an error, and how do you avoid it?
5. Why does `key=` in `sorted` get called once per element rather than once per comparison, and why does that matter for functions with side effects?
6. When should you prefer a list comprehension over `map`/`filter`, and when should you reach for `map`/`filter` instead?
7. In the AI SDK examples, what do LangChain's `@tool` decorator and OpenAI's raw tool dict both have in common as far as first-class functions are concerned?
8. Where in modern backend Python do you see the "callback pattern" outside of AI SDKs? (FastAPI, pytest, structlog, executor.map, asyncio.gather, etc.)
9. What does a "decorator factory" look like at the call site, and which real libraries use that exact shape?
10. Why is `xs = xs.sort()` a real bug, and what is the equivalent fix using `sorted`?

If you can answer all ten, Stage 3 is solid — Stage 4 (closures) will formalize exactly why the factories and lambdas above remember the values they capture.

---

## **3.12 Source Notes**

Cross-references used while writing these notes (June 2026 snapshot):

- Real Python — Python Lambda Functions — https://realpython.com/python-lambda/
- Trey Hunner — Overusing lambda expressions — https://treyhunner.com/2018/09/stop-writing-lambda-expressions/
- GeeksforGeeks — Map Reduce and Filter Operations in Python — https://www.geeksforgeeks.org/python/map-reduce-and-filter-operations-in-python/
- GeeksforGeeks — First-Class Functions — https://www.geeksforgeeks.org/python/first-class-functions-python/
- GeeksforGeeks — Higher-Order Functions in Python — https://www.geeksforgeeks.org/python/higher-order-functions-in-python/
- freeCodeCamp — First-Class Functions, Higher-Order Functions, and Closures — https://www.freecodecamp.org/news/first-class-functions-and-closures-in-python/
- LearnPython.org — Map, Filter, Reduce — https://www.learnpython.org/en/Map,_Filter,_Reduce
- introcs-python (Loyola) — Higher-Order Functions — https://introcs-python.cs.luc.edu/functional/higher_order.html
- OxRSE Training — Higher-Order Functions — https://train.rse.ox.ac.uk/material/HPCu/software_architecture_and_design/functional/higher_order_functions_python
- StackOverflow — Function as callback argument — https://stackoverflow.com/questions/6289646/
- LangChain Reference — https://reference.langchain.com/python/langchain
- LangChain Middleware Study Guide — https://colinmcnamara.com/blog/langchain-middleware-study-guide/
- LangChain Cycles integration (callback + middleware) — https://runcycles.io/how-to/integrating-cycles-with-langchain
- PEP 8 — Programming Recommendations (lambda guidance) — https://peps.python.org/pep-0008/

End of Stage 3.
