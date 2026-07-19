# **Python Modern Type Hinting, Error Handling, and Real-Codebase Patterns**

## **Quick Map of What's Coming**

| Topic | Core Idea | One-Liner |
| --- | --- | --- |
| Modern type hinting | `Callable`, generics, `Protocol`, `ParamSpec` | Make function types a contract, not a comment |
| Error handling | Exceptions, custom hierarchies, validation | Raise low, catch high, tell the truth about what went wrong |
| Real codebases | Recursion, purity, async, dataclasses, `__call__`, `__wrapped__` | The habits that keep you unstuck reading someone else's code |

## **Modern Type Hinting for Functions**

Every parameter and return value has a type. The function itself is also a type (`Callable`). A function can be generic over a `TypeVar`. A function can be typed against a protocol — duck typing, made explicit. A decorator can preserve the wrapped function's signature using `ParamSpec` and `Concatenate`.

### **`Callable`, `Optional`, and `Union` / `|`**

`Callable[[Arg1Type, Arg2Type, ...], ReturnType]` types a function. The argument list is positional only, and the return type is a single type.

```python
from typing import Callable

IntBinop = Callable[[int, int], int]

def apply(f: IntBinop, a: int, b: int) -> int:
    return f(a, b)

apply(lambda x, y: x + y, 2, 3)        # 5
apply(pow, 2, 8)                       # 256
```

`Callable[..., ReturnType]`, with a literal ellipsis, types a callable that takes any arguments and returns `ReturnType`.

```python
from typing import Callable

Handler = Callable[..., None]   # any signature, returns None
```

Python 3.10+ allows `X | Y` instead of `Union[X, Y]`, and `X | None` instead of `Optional[X]`.

```python
# 3.10+
def find_user(user_id: int) -> dict | None:
    return db.get(user_id) or None

# Pre-3.10 equivalent, still valid everywhere
from typing import Optional

def find_user(user_id: int) -> Optional[dict]:
    return db.get(user_id) or None
```

A parameter with a default of `None` whose annotation is not `Optional[X]` or `X | None` is almost always a bug — type checkers will flag it.

PEP 604 also lets the pipe syntax work directly in `isinstance` and `issubclass` on 3.10+.

```python
isinstance(42, int | str)             # True
isinstance("hi", int | str)           # True
isinstance(3.14, int | str)           # False
issubclass(bool, int | float)         # True
```

On Python 3.8 and 3.9, `int | None` inside an annotation only works if annotations are stored as strings rather than evaluated. `from __future__ import annotations` (PEP 563) does that. On 3.10+ it is not needed; on 3.14+, PEP 649 makes deferred evaluation the default.

### **Generics with `TypeVar`**

A `TypeVar` is a placeholder for an unknown type that the type checker can solve for. Generic functions are written the same way as generic classes.

```python
from typing import TypeVar, Sequence

T = TypeVar("T")

def first(seq: Sequence[T]) -> T:
    return seq[0]

first([1, 2, 3])              # int
first(["a", "b"])             # str
first(iter([True, False]))    # bool
```

The same `T` appears in both the input and the output, so the checker knows the return type matches the element type.

On Python 3.12+, generics can be declared inline. The old `TypeVar("T")` plus bare-name style still works, but the new syntax is shorter.

```python
# 3.12+ only
def first[T](seq: Sequence[T]) -> T:
    return seq[0]

class Box[T]:
    def __init__(self, value: T) -> None:
        self.value = value
    def get(self) -> T:
        return self.value
```

`type Box[T] = ...` is the equivalent for type aliases; `class Box[T](...): ...` is the equivalent for classes.

**Constrained** type variables must be one of a fixed set.

```python
from typing import TypeVar

AnyStr = TypeVar("AnyStr", str, bytes)    # PEP 484 example

def concat(a: AnyStr, b: AnyStr) -> AnyStr:
    return a + b

concat("foo", "bar")          # OK
concat(b"foo", b"bar")        # OK
concat("foo", b"bar")         # error -- str and bytes don't match
```

**Bounded** type variables must be a subtype of a specific type.

```python
from typing import TypeVar
from numbers import Number

N = TypeVar("N", bound=Number)

def double(x: N) -> N:
    return x + x
```

Either constrained (`AnyStr`) or bounded (`bound=Number`) can be used — not both.

Variance is a property of a generic class, not of a generic function, so it shows up when writing a generic container or interface rather than a plain `def`.

- Covariant (`T_co`) — the type variable can only come out of the container. A `Sequence[Cat]` is a subtype of `Sequence[Animal]`, since the read-only `Sequence` is covariant.
- Contravariant (`T_contra`) — the type variable can only go in. A `Handler[Cat]` can be used where a `Handler[Animal]` is expected, because the handler can handle any animal.
- Invariant (default) — neither. A `list[Cat]` is not a `list[Animal]`, because a `list[Cat]` won't accept an `Animal` for `append`.

PEP 695 lets the type checker infer variance automatically. `infer_variance=True` gives the same behavior on older versions.

```python
class Box[T](Generic[T]):       # 3.12+
    def get(self) -> T: ...
    def put(self, x: T) -> None: ...
```

In practice, most application code does not need to mark variance — it only matters when designing reusable container types or callback interfaces.

### **`Protocol` — Structural Typing**

Duck typing says: if it walks like a duck and quacks like a duck, it's a duck. Nominal typing says: if it inherits from `Duck`, it's a duck. `Protocol` is duck typing with type-checker support.

```python
from typing import Protocol

class SupportsClose(Protocol):
    def close(self) -> None: ...

def close_resource(r: SupportsClose) -> None:
    r.close()
```

Any class that has a `close(self) -> None` method satisfies `SupportsClose` — no inheritance required. This is structural subtyping.

Before `Protocol`, an `abc.ABC` with abstract methods was the usual approach, and callers had to inherit from it. With `Protocol`, any class with the right shape simply works, and the type checker confirms it at compile time.

```python
from typing import Protocol

class SupportsRead(Protocol):
    def read(self, n: int = -1) -> str: ...

def slurp(r: SupportsRead) -> str:
    return r.read()

class MyFile:
    def read(self, n: int = -1) -> str:
        return "data"

slurp(MyFile())             # "data" -- no inheritance needed
```

By default, `isinstance(obj, SomeProtocol)` raises `TypeError`. Decorating the protocol with `@runtime_checkable` allows it — but only for member existence, not signature compatibility.

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...

class File:
    def close(self) -> None:
        print("closing")

isinstance(File(), Closeable)    # True
```

The runtime check is shallow: it only checks that the names exist. A class with `def close(self): pass`, with the wrong return type, still passes `isinstance` if marked `runtime_checkable`. Rely on the runtime check only as a fast "does this object quack at all?" gate, not for full type safety.

A lot of modern library code is written against `Protocol` rather than a specific class, for decoupling — any class satisfying the protocol can be plugged in, and tests can pass simple stand-in objects.

```python
from typing import Protocol

class SupportsSend(Protocol):
    async def send(self, msg: str) -> None: ...

# Anything with an `async def send(self, msg)` method works here --
# a WebSocket connection, an in-memory test double, and so on.
async def publish(s: SupportsSend, msg: str) -> None:
    await s.send(msg)
```

`typing.io`, `typing.re`, `collections.abc`, and `asyncio` all define protocols (`SupportsRead`, `SupportsWrite`, `Iterable`, `Iterator`, `Awaitable`, `Coroutine`, and more) — any time those types appear in a signature, that is a `Protocol` in use.

### **`ParamSpec` and `Concatenate` — Typing Decorators Without Losing the Signature**

`ParamSpec` lets a decorator preserve the entire parameter list of the wrapped function, so `inspect.signature` and type checkers still see the real call shape.

**The problem**

```python
from typing import Callable, TypeVar
from functools import wraps

T = TypeVar("T")

def my_decorator(f: Callable[..., T]) -> Callable[..., T]:
    @wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper

@my_decorator
def add(a: int, b: int) -> int:
    return a + b

add(1, 2)        # works
add("a", "b")    # also works -- no static error
```

`Callable[..., T]` means "takes anything." A type checker cannot tell a caller that `add` is supposed to take two `int`s.

**The fix**

```python
from typing import Callable, TypeVar, ParamSpec
from functools import wraps

P = ParamSpec("P")
R = TypeVar("R")

def my_decorator(f: Callable[P, R]) -> Callable[P, R]:
    @wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return f(*args, **kwargs)
    return wrapper

@my_decorator
def add(a: int, b: int) -> int:
    return a + b

add(1, 2)        # OK
add("a", "b")    # type error: expected int
```

`P` captures the parameter list; `P.args` and `P.kwargs` are the syntactic markers the type checker uses to forward the call. The result type is preserved too. `P.args` and `P.kwargs` must always be used together — one alone cannot be used, and neither can be assigned to a variable.

`Concatenate[X, P]` describes a callable whose first positional parameter is `X`, followed by the parameters described by `P` — the recipe for decorators that inject or remove parameters. `Concatenate` only supports prepending, not appending, since there is no sound way to add trailing positional parameters in a statically checkable way.

```python
from typing import Callable, TypeVar
from typing_extensions import ParamSpec, Concatenate
from functools import wraps

P = ParamSpec("P")
R = TypeVar("R")
Request = TypeVar("Request")

def with_request(f: Callable[Concatenate[Request, P], R]) -> Callable[P, R]:
    """A decorator that injects a Request as the first argument."""
    @wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        request = build_request()
        return f(request, *args, **kwargs)
    return wrapper

@with_request
def handle(request, user_id: int) -> str:
    return f"{user_id} via {request.method}"

handle(user_id=42)    # request is injected; user_id is a kwarg
```

**A complete typed decorator, combining everything above**

```python
import functools
import time
from typing import Callable, TypeVar
from typing_extensions import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

def timer(unit: str = "ms") -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            t0 = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = (time.perf_counter() - t0) * (1000 if unit == "ms" else 1)
            print(f"{func.__name__} took {elapsed:.2f}{unit}")
            return result
        return wrapper
    return decorator

@timer(unit="ms")
def heavy(a: int, b: str) -> bool:
    return bool(a and b)
```

`heavy` keeps its full type signature — autocomplete, static type checkers, `inspect.signature`, and `help()` all see the original.

| Construct | Module | Use Case |
| --- | --- | --- |
| `Callable[[A, B], R]` | `typing` | Type a function |
| `Callable[..., R]` | `typing` | Any args, fixed return |
| `Union[A, B]` / `A \| B` | `typing` / builtin | Either type |
| `Optional[A]` / `A \| None` | `typing` / builtin | A or None |
| `TypeVar("T")` | `typing` | Generic function or class |
| `TypeVar("T", bound=Number)` | `typing` | Subtype-constrained |
| `TypeVar("AnyStr", str, bytes)` | `typing` | Constrained set |
| `def f[T](x: T) -> T` | PEP 695 (3.12+) | Inline generic |
| `class Proto(Protocol): ...` | `typing` | Structural type |
| `@runtime_checkable` | `typing` | `isinstance` against a Protocol |
| `ParamSpec("P")` | `typing` / `typing_extensions` | Capture a parameter list |
| `Concatenate[X, P]` | `typing` / `typing_extensions` | Inject or remove a leading parameter |

## **Error Handling Inside Functions**

A function either returns a value or it raises. Error handling ensures it raises the right exception, with the right message, in the right place, caught by the right caller.

### **Exceptions Are Just Objects**

```python
def parse_age(raw: str) -> int:
    if not raw.isdigit():
        raise ValueError(f"age must be digits, got {raw!r}")
    return int(raw)

try:
    age = parse_age("thirty")
except ValueError as e:
    print("bad input —", e)        # bad input — age must be digits, got 'thirty'
```

`raise X` triggers exception propagation: Python unwinds the call stack until it finds an `except X` (or a parent class), then runs the handler. If nothing handles it, the program crashes with a traceback.

### **Custom Exceptions — A Hierarchy Rooted at the Domain**

Built-in exceptions (`ValueError`, `TypeError`, `KeyError`, `FileNotFoundError`) suit built-in failures. Domain failures deserve their own hierarchy, and the minimal correct custom exception is one line.

```python
class AppError(Exception):
    """Base for all errors raised by this application."""

class ValidationError(AppError):
    """Input failed validation."""

class ExternalServiceError(AppError):
    """A downstream dependency failed."""

class RateLimitedError(ExternalServiceError):
    """The downstream told us to back off."""
```

Callers can catch the precise subclass (`except RateLimitedError`) or the broad root (`except AppError`), choosing the granularity themselves.

Custom exceptions should inherit from `Exception`, not `BaseException`. Inheriting from `BaseException` bypasses `except Exception:` handlers — the right choice for `KeyboardInterrupt` and `SystemExit`, not for application errors.

```python
# Good
class MyError(Exception): ...

# Almost certainly a bug
class MyError(BaseException): ...
```

When an exception has a record ID, a field name, or a downstream URL, store those as attributes — not folded into the message string.

```python
class DataProcessingError(Exception):
    def __init__(self, message: str, *, record_id: int, field: str) -> None:
        super().__init__(message)
        self.record_id = record_id
        self.field = field

raise DataProcessingError(
    "amount out of range",
    record_id=4823,
    field="amount",
)
```

Callers can route on `e.field` or log `e.record_id` without parsing a string.

When a low-level exception is caught and a domain exception is raised instead, chain them with `raise X from Y` so the original traceback is preserved.

```python
try:
    raw = requests.get(url, timeout=5).text
except requests.RequestException as e:
    raise ExternalServiceError(f"failed to fetch {url}") from e
```

The traceback then shows both errors, with an explicit "the above exception was the direct cause of the following." `raise X from None` deliberately suppresses the original, which is rare.

### **Where Validation Belongs — Fail Fast vs Defensive**

The right answer is: validate at the boundary, trust inside.

Inside a module, a function should assume its inputs are valid. If the caller hands over garbage, raise immediately rather than silently coercing or working around a programmer error.

```python
def total_sales(orders: list[Order]) -> Money:
    if orders is None:                  # fail fast
        raise ValueError("orders must not be None")
    return sum(o.amount for o in orders)
```

This keeps the function's contract clear: it promises a `Money` for a non-empty `list[Order]`, and raises if that contract is broken.

At the edge of the system — an HTTP handler, a CLI entry point, a message-queue consumer, a deserializer — the opposite rule applies: anything might show up, so validate aggressively there, and once validated, the rest of the code can stop worrying.

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class SignupRequest(BaseModel):
    email: str = Field(..., pattern=r"^[\w.]+@[\w.]+$")
    age: int = Field(..., ge=0, le=150)

@app.post("/signup")
def signup(body: SignupRequest):
    # body is already validated, normalized, and type-checked
    return create_user(body.email, body.age)
```

Pydantic does the validation; the function receives a known-good input. The same pattern applies to CLI args (typer), config (Pydantic Settings), and message-queue payloads.

Python style favors EAFP — easier to ask forgiveness than permission: try the operation, catch the specific exception, handle it.

```python
# EAFP
try:
    value = d[key]
except KeyError:
    value = default

# LBYL -- less Pythonic
if key in d:
    value = d[key]
else:
    value = default
```

EAFP is preferred because it is faster in the common case (no double lookup), it is race-safe in concurrent code, and it correctly handles "the value is `None` but the key is present." LBYL is still fine when the check is cheap and the operation is expensive.

### **The Three Golden Rules of Exception Handling**

1. Catch only what can actually be handled. A bare `except:` or `except Exception:` inside a low-level module turns real bugs into silent wrong answers — catch `ValueError`, catch `requests.RequestException`, catch a custom `AppError`, but only catch what there is a plan for.
2. Do not use exceptions for routine control flow. "User not found" is a normal outcome — return `None` or a result type. Reserve exceptions for the exceptional: network down, disk full, programmer error.
3. Let the context manager own cleanup. Any resource — files, connections, locks — belongs in a `with` block so cleanup runs even on exception. For custom resources, implement `__enter__`/`__exit__` or use `@contextlib.contextmanager`.

```python
# Good
with db.connection() as conn:
    conn.execute(...)

# Bad
conn = db.connection()
try:
    conn.execute(...)
finally:
    conn.close()
```

`logger.exception(...)`, called inside an `except` block, captures the full traceback automatically. Outside an `except` block, `exc_info=True` does the same.

```python
import logging

log = logging.getLogger(__name__)

try:
    result = call_external_api()
except ExternalServiceError as e:
    log.exception("external call failed")     # logs the traceback
    raise
```

A traceback with no context is half a traceback — always include the entity being worked on, such as the user ID, order ID, or request URL.

| Situation | Raise | Return |
| --- | --- | --- |
| Programmer passed garbage (`None` to a function that needs a list) | yes | |
| Input from outside the system (HTTP body, CLI arg, file content) | after validation | the validation result, or raise an HTTP 400 |
| Lookup that may legitimately find nothing (user not found, key missing) | | yes — return `None` or a default |
| Network/IO failure the caller cannot anticipate | yes | |
| Routine branching logic | | always return |
| Unexpected internal state (invariant violation) | yes — fail fast | |

## **Functions in Real Codebases**

The habits and techniques that make the difference between "I can read this code" and "I can read any code" — the ones that show up when opening an unfamiliar repository for the first time.

### **Recursion — And When It Bites**

A recursive function calls itself, and the recursive form is often the clearest way to express an algorithm. The catch: CPython has a recursion limit (default around 1000), and there is no tail-call optimization.

```python
def factorial(n: int) -> int:
    if n <= 1:
        return 1
    return n * factorial(n - 1)

factorial(5)         # 120
factorial(2000)      # RecursionError: maximum recursion depth exceeded
```

```python
import sys
sys.getrecursionlimit()                  # usually 1000
sys.setrecursionlimit(10_000)            # possible, but be careful
```

Increasing the limit is risky — Python stack frames can be large, and a too-high limit can crash the interpreter with a C-level stack overflow. Use the smallest value that works.

For any function doing a small amount of work per call, rewriting it as a `while` loop with an explicit stack usually works, giving `O(n)` time, `O(n)` memory, and no recursion limit.

```python
# Recursive
def walk_tree(node):
    yield node
    for child in node.children:
        yield from walk_tree(child)

# Iterative
def walk_tree(node):
    stack = [node]
    while stack:
        current = stack.pop()
        yield current
        stack.extend(current.children)
```

Recursion is the right tool for tree and graph traversals (where the recursion is the structure), divide-and-conquer algorithms (merge sort, quicksort) that split cleanly, recursive-descent parsers matching a recursive grammar, and anything mapping directly onto a recursive data structure. It is not the right tool for linear data with a known upper bound, anything needing `sys.setrecursionlimit` to work on real inputs, or performance-critical inner loops, where iteration is faster.

`functools.lru_cache` makes many recursive functions practical. `fib(50)` is 49 calls deep with naive recursion and explodes the call stack; with `lru_cache`, each value is computed once and the actual call depth stays shallow.

```python
import functools

@functools.lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

fib(500)         # instant; no recursion issue
```

### **Pure Functions vs Side Effects**

A function is pure if its return value depends only on its arguments and it has no observable side effects — no I/O, no mutation of inputs, no global state. A function is impure if it crosses the boundary between the program and the world — printing, reading a file, hitting a network, mutating a global, writing to a database.

```python
# Pure
def apply_discount(price_cents: int, percent: float) -> int:
    return int(round(price_cents * (1 - percent / 100)))

# Impure
def apply_discount_and_log(price_cents: int, percent: float) -> int:
    final = int(round(price_cents * (1 - percent / 100)))
    logger.info("discount applied", price=price_cents, percent=percent, final=final)
    return final
```

The pure version is one assertion away from being fully tested. The impure version needs a logger fixture, a way to assert on log output, and a way to disable logging for non-test runs — the same logic, but far more test code.

The "functional core, imperative shell" pattern is the standard way to organize real programs: the core is a set of pure functions holding all the business logic, and the shell is a thin layer doing I/O and calling into the core.

```python
# Functional core -- all pure
def compute_total(items: list[Item], tax_rate: float) -> Money:
    subtotal = sum(i.price for i in items)
    tax = subtotal * tax_rate
    return Money(subtotal + tax)

# Imperative shell -- the only place with side effects
def checkout(cart: list[Item], user: User) -> None:
    total = compute_total(cart, user.tax_rate)
    db.save_order(user, cart, total)
    email.send_receipt(user, total)
```

The shell is hard to test but tiny, with no decisions inside it. The core has all the decisions and is trivially testable. This is the standard layout for backend services, CLIs, ETL jobs, and notebooks. If a function is pure, calls can be rearranged, parallelized, memoized, or replaced without breaking anything; impure functions carry hidden dependencies at every call site.

### **Function Composition Patterns**

Composition takes the output of one function and feeds it to the next — the `map`/`filter`/`reduce` chain already covered is composition. A `pipe` helper turns `f(g(h(x)))` into `pipe(x, h, g, f)`.

```python
from typing import Callable, TypeVar

A = TypeVar("A")
T = TypeVar("T")

def pipe(value: A, *fns: Callable[[T], T]) -> T:
    for f in fns:
        value = f(value)
    return value

result = pipe(
    "  Aarav KUMAR  ",
    str.strip,
    str.lower,
    lambda s: s.replace(" ", "."),
)
# 'aarav.kumar'
```

The result is just a `for` loop under the hood, but the call site reads left-to-right, which most people find easier than nested calls. `compose` builds a new function right-to-left instead of applying functions to a value immediately.

```python
def compose(*fns: Callable[[T], T]) -> Callable[[T], T]:
    def composed(value: T) -> T:
        for f in reversed(fns):
            value = f(value)
        return value
    return composed

clean = compose(str.strip, str.lower, lambda s: s.replace(" ", "."))
clean("  Aarav KUMAR  ")       # 'aarav.kumar'
```

The OOP instinct is to add behavior via a base class or a mixin; the functional instinct is to compose small functions. The functional version is more flexible, easier to test since each function is small and pure, and easier to reorder.

### **Async Functions — How They Interact With Everything Else**

`async def` defines a coroutine function. Calling it returns a coroutine object; the body does not run until it is awaited or scheduled with `asyncio.run`, `asyncio.create_task`, or `asyncio.gather`.

```python
import asyncio

async def fetch_one() -> int:
    await asyncio.sleep(1)
    return 42

async def main() -> None:
    a = fetch_one()          # coroutine object, body hasn't run
    b = fetch_one()          # another coroutine, also unstarted
    results = await asyncio.gather(a, b)
    print(results)           # [42, 42], both finished in about 1s total
```

A coroutine is the object returned by calling an `async def`, awaited from another coroutine. A task is a coroutine wrapped by `asyncio.create_task`, running in the background, awaitable and cancellable. A future is a low-level awaitable representing an eventual result — most code uses tasks, not futures.

```python
# One-shot: run a coroutine and block until done
asyncio.run(main())

# Concurrent: schedule multiple coroutines, wait for all
results = await asyncio.gather(coro1(), coro2(), coro3())

# Background: schedule a coroutine, do other work, await later
task = asyncio.create_task(coro())
# ... do other things ...
result = await task
```

`async for` consumes an async iterator, such as an async generator.

```python
async def aio_ticker(interval: float, n: int):
    for i in range(n):
        await asyncio.sleep(interval)
        yield f"tick {i}"

async def main():
    async for tick in aio_ticker(0.5, 3):
        print(tick)
```

`async with` is the async version of `with`, used for locks, sessions, and transactions.

```python
async with db.transaction() as tx:
    await tx.execute(...)
```

A sync decorator wrapping an `async def` silently breaks the coroutine, since the wrapper returns a coroutine object instead of awaiting it. The fix is the three-layer async-aware factory with `inspect.iscoroutinefunction` branching.

```python
import functools
import inspect
import time
import asyncio

def timer(func):
    if inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            t0 = time.perf_counter()
            result = await func(*args, **kwargs)
            print(f"{func.__name__} took {(time.perf_counter() - t0) * 1000:.2f}ms")
            return result
        return async_wrapper
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {(time.perf_counter() - t0) * 1000:.2f}ms")
        return result
    return sync_wrapper
```

`inspect.iscoroutinefunction` runs once at decoration time, so the per-call cost is zero. Almost every modern Python library is async-first or async-friendly.

```python
import httpx

async def fetch_many(urls: list[str]) -> list[str]:
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
    return [r.text for r in responses]
```

The same pattern shows up in `asyncpg`, SQLAlchemy 2.0 async, `motor` for MongoDB, LangChain, FastAPI route handlers, and `aiofiles`.

### **Dataclasses and `__call__` — Objects That Behave Like Functions**

Anything callable with `()` is callable: functions, methods, classes (calling a class instantiates it), and any object with a `__call__` method.

```python
import collections.abc

callable(len)                                 # True
callable(dict)                                # True
callable([].append)                           # True
callable(42)                                  # False
isinstance(len, collections.abc.Callable)      # True
```

Adding `__call__` to a class turns its instances into callables.

```python
class Greeter:
    def __init__(self, greeting: str) -> None:
        self.greeting = greeting

    def __call__(self, name: str) -> str:
        return f"{self.greeting}, {name}"

hello = Greeter("Hello")
hello("Aarav")              # 'Hello, Aarav'
```

The instance carries state — the greeting — and behaves like a function. This is the same shape as a closure with state, but more discoverable and easier to extend. Combining `@dataclass` with `__call__` produces a stateful callable that prints well, compares structurally, and can be hashed.

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Scale:
    factor: float

    def __call__(self, x: float) -> float:
        return x * self.factor

s = Scale(2.5)
s(10)         # 25.0
```

This is the standard recipe for a function with parameters set once and then passed around — it composes with other callables (`map(Scale(2.0), data)`) and shows up in real SDKs as configuration objects.

| Use `__call__` | Use a Closure |
| --- | --- |
| The callable has multiple fields of state | The state is one or two values |
| A `repr()`, equality, or hashing for the configured callable is wanted | The callable is throwaway |
| More methods need to be attached to the configured callable | Only `f(x) -> y` is needed |
| Subclassing is wanted | One-off use |

The dataclass plus `__call__` form is the most production-grade — it is what scikit-learn estimators look like (`clf = StandardScaler(); clf.fit(X); clf.transform(X)`) and what configuration objects look like in modern SDKs. LangChain's runnables are callables — a chat model instance, a prompt template, and a chain are all callable, and composing them with `|` works because every piece implements `__call__` or an equivalent async variant.

```python
chain = prompt | llm | parser
result = chain.invoke({"input": "hi"})    # chain(...) is a callable
```

### **Reading Unfamiliar Codebases — `__wrapped__` and the Decorator Chain**

When a function is decorated with `@functools.wraps`, Python sets a `__wrapped__` attribute on the wrapper that points to the original — following the chain recovers the undecorated function.

```python
import functools

@functools.wraps(func)
def wrapper(*args, **kwargs): ...

wrapper.__wrapped__ is func        # True
```

For multiple decorators:

```python
@bold
@italic
@debug
def greet(name): ...
```

`greet.__wrapped__` is the `italic`-wrapped function, `greet.__wrapped__.__wrapped__` is the `debug`-wrapped function, and `greet.__wrapped__.__wrapped__.__wrapped__` is the original.

`inspect.unwrap(func)` follows the `__wrapped__` chain until it reaches a function without one, returning the original, and it also detects cycles.

```python
import inspect

original = inspect.unwrap(greet)        # the actual `def greet`
```

`inspect.signature(greet)` already follows `__wrapped__` automatically, so `help(greet)` shows the right signature even after wrapping.

When a decorated function is called: the call site invokes `decorated_func(*args, **kwargs)`; the outermost wrapper's code runs first (logging, auth, timing, or whatever it does); it calls the next layer down; this continues until the original is reached; the original returns, and each wrapper in turn can post-process, transform, or suppress the return value.

```python
import inspect

# What does this function actually look like to the outside?
print(decorated_func)
print(decorated_func.__name__)
print(inspect.signature(decorated_func))
print(decorated_func.__doc__)

# What is the original underneath?
print(inspect.unwrap(decorated_func))

# What decorators are stacked on it?
func = decorated_func
while hasattr(func, "__wrapped__"):
    print("layer —", func)
    func = func.__wrapped__
print("original —", func)
```

The last loop is the exact step-by-step that runs at call time. Reading it is the difference between "this function is mysterious" and "this function does A, then B, then C, then the body."

If a decorator did not use `functools.wraps`, the `__wrapped__` chain is missing. The remaining, last-resort options are reading the source with `inspect.getsource(func)`, or inspecting the closure with `func.__closure__[0].cell_contents` if the decorator stored the original there. The first rule of writing decorators is to always use `@functools.wraps(func)`, so every consumer can introspect, document, and rewrap the function without spelunking.

## **Common Mistakes**

- Giving a parameter a default of `None` without annotating it as `Optional[X]` or `X | None` — type checkers treat this mismatch as a bug, even though the code runs fine at import time.
- Inheriting a custom exception from `BaseException` instead of `Exception`, which silently makes it invisible to `except Exception:` handlers throughout the codebase.
- Using a bare `except:` or a blanket `except Exception:` inside a low-level module, which turns real bugs into silent wrong answers instead of surfacing them where they can be diagnosed.
- Applying a synchronous decorator to an `async def` function without checking `inspect.iscoroutinefunction`, which returns an un-awaited coroutine object instead of the real result.
- Raising and re-raising exceptions without `raise X from Y`, which discards the original traceback and makes the true root cause of a failure much harder to trace.
- Reaching for `sys.setrecursionlimit` to push past a `RecursionError` instead of converting the function to an iterative form, risking a C-level stack overflow rather than a clean Python exception.
- Writing a decorator without `@functools.wraps`, which breaks the `__wrapped__` chain and leaves every future reader of that code without a way to recover the original function's signature and metadata.

## **Production Patterns**

| Library / Tool | Key Feature | Best Use Case |
| --- | --- | --- |
| `Protocol` (`typing`) | Structural typing without inheritance | Decoupling interfaces from concrete implementations, easier test doubles |
| `ParamSpec` / `Concatenate` | Preserves a wrapped function's exact signature | Decorator libraries such as `tenacity`, `fastapi.Depends` |
| Pydantic `BaseModel` | Validates and normalizes input at the system boundary | HTTP request bodies, CLI config, message-queue payloads |
| `functools.lru_cache` | Memoizes recursive calls | Turning exponential recursive algorithms into practical ones |
| `httpx.AsyncClient` | Async-first HTTP client | Concurrent outbound API calls |
| LangChain runnables (`|` composition) | Every piece implements `__call__` or an async equivalent | Composing prompts, models, and parsers into pipelines |

## **Modern Python Patterns**

| Older Style | Modern Style |
| --- | --- |
| `Union[int, str]`, `Optional[dict]` | `int \| str`, `dict \| None` (3.10+) |
| `TypeVar("T")` declared separately, then used in a generic function | `def first[T](seq: Sequence[T]) -> T:` inline generic syntax (3.12+) |
| `Callable[..., T]` in a decorator, losing the wrapped function's real argument types | `Callable[P, R]` with `ParamSpec`, preserving the exact signature |
| `abc.ABC` with abstract methods, requiring inheritance | `Protocol`, satisfied by any class with the right shape |
| `from __future__ import annotations` required for forward references | PEP 649 makes deferred evaluation the default on 3.14+ |

## **Quick Reference**

| Pattern | Syntax | Purpose |
| --- | --- | --- |
| Type a function | `Callable[[int, int], int]` | Describe a function's parameter and return types |
| Optional value | `X \| None` | Mark a value that may be `None` |
| Generic function | `def first[T](seq: Sequence[T]) -> T:` | Return type tied to input type |
| Structural interface | `class P(Protocol): def method(self) -> None: ...` | Duck typing with type-checker support |
| Runtime protocol check | `@runtime_checkable` | Allow `isinstance` against a `Protocol` |
| Preserve decorator signature | `ParamSpec("P")`, `Callable[P, R]` | Keep a wrapped function's real signature |
| Inject a leading parameter | `Concatenate[X, P]` | Type a decorator that adds a first argument |
| Domain exception hierarchy | `class AppError(Exception): ...` | Let callers catch broad or precise error types |
| Preserve a traceback | `raise DomainError(...) from original_error` | Chain a low-level error into a domain error |
| Validate at the edge | Pydantic `BaseModel` on an HTTP/CLI boundary | Keep the rest of the code trusting its inputs |
| Ask forgiveness | `try: ... except KeyError: ...` | Preferred over checking membership first |
| Recursion to iteration | `while stack: node = stack.pop(); stack.extend(...)` | Avoid `RecursionError` on real inputs |
| Functional core | Pure function with no I/O | Easiest code to test and refactor |
| Pipe values through functions | `pipe(value, f, g, h)` | Left-to-right function composition |
| Await a coroutine | `await asyncio.gather(coro1(), coro2())` | Run coroutines concurrently |
| Async-safe decorator | `if inspect.iscoroutinefunction(func): ...` | Support both sync and async functions |
| Callable object | `def __call__(self, x): ...` | State plus a function-shaped interface |
| Recover the original function | `inspect.unwrap(decorated_func)` | Follow the `__wrapped__` chain |