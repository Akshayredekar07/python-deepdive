# **Python Decorators**

## **What Is a Decorator**

A decorator is a function which can take a function as an argument, extend its functionality, and return the modified function with that extended functionality.

- The main objective of a decorator is to extend the functionality of an existing function without modifying that function's own code.
- A decorator wraps the original function inside a new function, and that new function is what actually gets called from then on.
- The `@` symbol placed above a function definition is simply shorthand for passing that function into a decorator function.

Consider a plain greeting function.

```python
def wish(name):
    print("Hello", name, "Good Morning")
```

This function always prints the same style of message, regardless of who is passed in.

```python
wish("Durga")    # Hello Durga Good Morning
wish("Ravi")     # Hello Ravi Good Morning
wish("Harsha")   # Hello Harsha Good Morning
```

Suppose the message needs to change only for `"Harsha"`, without touching the `wish()` function itself. A decorator makes this possible.

```python
def decor(func):
    def inner(name):
        if name == "Harsha":
            print("Hello Harsha Bad Morning")
        else:
            func(name)
    return inner

@decor
def wish(name):
    print("Hello", name, "Good Morning")

wish("Durga")
wish("Ravi")
wish("Harsha")
```

Output:

```
Hello Durga Good Morning
Hello Ravi Good Morning
Hello Harsha Bad Morning
```

Whenever `wish()` is called, the `decor` function's `inner` runs in its place, since `@decor` already replaced `wish` with `inner` at definition time. The original `wish()` function was never edited — the new behavior was added entirely from the outside.

## **Writing a Basic Decorator**

Mechanically, `@decor` above `def wish(name):` means exactly this line, applied immediately after `wish` is defined:

```python
wish = decor(wish)
```

- `decor` receives the original `wish` function as its argument, `func`.
- Inside `decor`, a new function `inner` is defined, which contains the extra logic and calls `func` when that extra logic does not need to intervene.
- `decor` returns `inner`, and that returned function becomes the new `wish`.

This is exactly the closure mechanism: `inner` remembers `func` from the enclosing scope of `decor`, even after `decor` has finished running.

## **Calling a Function With and Without the Decorator**

Skipping the `@decor` line makes it possible to call the same function both in its original, undecorated form and in its decorated form, side by side.

```python
def decor(func):
    def inner(name):
        if name == "Harsha":
            print("Hello Harsha Bad Morning")
        else:
            func(name)
    return inner

def wish(name):
    print("Hello", name, "Good Morning")

decorfunction = decor(wish)

wish("Durga")            # decorator not applied
wish("Harsha")            # decorator not applied

decorfunction("Durga")    # decorator applied
decorfunction("Harsha")   # decorator applied
```

Output:

```
Hello Durga Good Morning
Hello Harsha Good Morning
Hello Durga Good Morning
Hello Harsha Bad Morning
```

`wish` was never reassigned here, so calling `wish(...)` directly still runs the plain, undecorated version. `decorfunction`, on the other hand, points at `inner`, the wrapped version — this is the same distinction as choosing whether or not to write `@decor` above the function definition.

## **Handling Any Function Signature — `*args` and `**kwargs`**

The examples above only work for functions that take exactly one argument, `name`. A decorator meant to be reused across many different functions needs to accept and forward any number of positional and keyword arguments.

```python
def smart_division(func):
    def inner(a, b):
        print("We are dividing", a, "with", b)
        if b == 0:
            print("OOPS... cannot divide")
            return
        else:
            return func(a, b)
    return inner

@smart_division
def division(a, b):
    return a / b

print(division(20, 2))
print(division(20, 0))
```

Output:

```
We are dividing 20 with 2
10.0
We are dividing 20 with 0
OOPS... cannot divide
None
```

Without the decorator, `division(20, 0)` would raise `ZeroDivisionError` and stop the program. With `smart_division` wrapping it, the zero-division case is intercepted and handled before the original function ever runs.

`inner(a, b)` above still only matches functions that take two positional arguments. Generalizing it with `*args, **kwargs` makes the same decorator usable on any function, regardless of its parameters.

```python
def logged(func):
    def inner(*args, **kwargs):
        print("calling", func.__name__, "with", args, kwargs)
        result = func(*args, **kwargs)
        print(func.__name__, "returned", result)
        return result
    return inner

@logged
def add(a, b):
    return a + b

@logged
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}"

add(3, 4)
greet("Om", greeting="Hi")
```

`*args` collects any positional arguments into a tuple, and `**kwargs` collects any keyword arguments into a dict; `func(*args, **kwargs)` then unpacks them back out when calling the original function, so `inner` never needs to know the original function's exact signature.

## **`functools.wraps` and Preserving Function Identity**

Decorating a function quietly replaces its identity — tools that inspect a function, such as `help()`, debuggers, and automatic API documentation generators, start seeing the wrapper instead of the real function.

```python
def logged(func):
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner

@logged
def add(a, b):
    """Add two numbers together."""
    return a + b

print(add.__name__)   # inner   -- should be 'add'
print(add.__doc__)    # None    -- should be 'Add two numbers together.'
```

`functools.wraps` fixes this by copying `__name__`, `__doc__`, `__module__`, and other metadata from the original function onto the wrapper.

```python
import functools

def logged(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner

@logged
def add(a, b):
    """Add two numbers together."""
    return a + b

print(add.__name__)   # add
print(add.__doc__)    # Add two numbers together.
```

`functools.wraps(func)` also sets `inner.__wrapped__ = func`, a direct reference back to the original function, which is how `inspect.signature(add)` can still report the correct, original parameter list even after decoration.

- Every decorator written from now on should use `functools.wraps` on its inner function, with no exceptions.
- Skipping it costs nothing in a small script, but in a codebase with many decorated functions, every one of them reports as the same generic wrapper name in stack traces, profilers, and generated API docs.

## **Decorator Factories — Decorators That Take Arguments**

A decorator like `@logged` above takes no configuration of its own. Many real decorators need configuration — `@retry(max_attempts=3)`, `@app.get("/students")`, `@lru_cache(maxsize=128)` — which requires one additional layer of nesting.

```python
import functools
import time

def retry(max_attempts=3, delay=1.0, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    print(f"attempt {attempt}/{max_attempts} failed —", repr(e))
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_exception
        return inner
    return decorator

@retry(max_attempts=4, delay=0.5, exceptions=(ConnectionError,))
def fetch_report(report_name):
    import random
    if random.random() < 0.7:
        raise ConnectionError(f"could not reach server for {report_name}")
    return f"downloaded {report_name}"
```

Three layers are at work here:

1. `retry(max_attempts=4, delay=0.5, exceptions=(ConnectionError,))` runs first, immediately, and returns `decorator`.
2. `decorator` is then applied to `fetch_report`, exactly like a normal decorator, and returns `inner`.
3. `inner` is what actually runs each time `fetch_report(...)` is called.

Written without the `@` sugar:

```python
fetch_report = retry(max_attempts=4, delay=0.5, exceptions=(ConnectionError,))(fetch_report)
```

## **Class-Based Decorators**

A decorator does not have to be a function. Any callable — including a class whose instances define `__call__` — can serve as a decorator.

```python
import functools

class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        print(func_name := self.func.__name__, "has been called", self.calls, "time(s)")
        return self.func(*args, **kwargs)

@CountCalls
def process_order(order_id):
    return f"processed {order_id}"

process_order(1)
process_order(2)
print(process_order.calls)   # 2
```

`@CountCalls` runs `process_order = CountCalls(process_order)`. `process_order` is now an instance of `CountCalls` rather than a plain function, but since the class defines `__call__`, calling `process_order(...)` still works exactly like calling a function — while also giving a natural place, `self`, to hold state such as `self.calls`.

A class-based decorator can also take its own configuration in `__init__`, with `__call__` playing the role of the `decorator` layer from a function-based factory.

```python
class RequiresRole:
    def __init__(self, role):
        self.role = role

    def __call__(self, func):
        @functools.wraps(func)
        def inner(user, *args, **kwargs):
            if user.get("role") != self.role:
                raise PermissionError(f"requires role — {self.role}")
            return func(user, *args, **kwargs)
        return inner

@RequiresRole("admin")
def delete_report(user, report_id):
    return f"deleted report {report_id}"

admin = {"name": "Tanvi", "role": "admin"}
analyst = {"name": "Karan", "role": "analyst"}

print(delete_report(admin, "report_2025.pdf"))
# delete_report(analyst, "report_2025.pdf")   # PermissionError: requires role — admin
```

A class-based decorator reads more naturally when it needs to track meaningful internal state (`self.calls`, `self.cache`), or when the decorated result should expose extra attributes or methods back to the caller.

## **Decorator Chaining — Stacking Multiple Decorators**

More than one decorator can be applied to the same function, and together they form decorator chaining.

```python
def decor1(func):
    def inner():
        x = func()
        return x * x
    return inner

def decor2(func):
    def inner():
        x = func()
        return 2 * x
    return inner

@decor2
@decor1
def num():
    return 10

print(num())
```

Decorators stack from the bottom up, but run from the top down at call time:

- `@decor2` above `@decor1` means `num = decor2(decor1(num))`.
- `decor1` wraps the original `num` first, so it runs closest to the real function.
- `decor2` wraps the result of that, so it runs last, on the outside.
- `num()` therefore computes `decor1(num)` first, producing $10 \times 10 = \boxed{100}$, and then `decor2` doubles that result: $2 \times 100 = \boxed{200}$.

**Reading order in a realistic example**

```python
def bold(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return inner

def italic(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return inner

@bold
@italic
def message(text):
    return text

print(message("hello"))   # <b><i>hello</i></b>
```

`italic` wraps the original `message` first, and `bold` wraps the result of that — so at call time, `bold`'s wrapper runs first, calls into `italic`'s wrapper, which finally calls the original function. This is the same nesting shape as middleware chains: the outermost decorator is the first thing to start and the last thing to finish.

Order also changes what a decorator actually measures. `@retry` above `@timer` times each retry attempt individually; `@timer` above `@retry` times the entire retry loop, including every failed attempt, as one block. Both are valid, but they answer different questions, so picking the wrong order silently produces the wrong numbers rather than an error.

## **Async-Safe Decorators**

A decorator written the ordinary way breaks the moment it is applied to an `async def` function, because calling a coroutine function does not run it — it returns a coroutine object that still needs to be awaited.

```python
def logged(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        print("calling", func.__name__)
        return func(*args, **kwargs)   # does not actually run an async function
    return inner

@logged
async def fetch(url):
    import asyncio
    await asyncio.sleep(0.1)
    return f"data from {url}"

# result = fetch("https://api.example.com")
# print(result)   # <coroutine object fetch at 0x...>  -- never actually ran
```

The fix is an `async def` wrapper that awaits the original coroutine.

```python
def logged(func):
    @functools.wraps(func)
    async def inner(*args, **kwargs):
        print("calling", func.__name__)
        result = await func(*args, **kwargs)
        print(func.__name__, "finished")
        return result
    return inner

@logged
async def fetch(url):
    import asyncio
    await asyncio.sleep(0.1)
    return f"data from {url}"

import asyncio
result = asyncio.run(fetch("https://api.example.com"))
print(result)
```

A decorator meant to work on both sync and async functions detects which kind it received and branches accordingly, using `inspect.iscoroutinefunction`.

```python
import inspect
import time

def timer(func):
    if inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_inner(*args, **kwargs):
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            print(func.__name__, "took", f"{time.perf_counter() - start:.4f}s")
            return result
        return async_inner
    else:
        @functools.wraps(func)
        def sync_inner(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            print(func.__name__, "took", f"{time.perf_counter() - start:.4f}s")
            return result
        return sync_inner
```

This exact branching pattern is how libraries such as `tenacity` (retries) support decorating both `def` and `async def` functions with a single decorator.

## **Common Mistakes**

- Writing `inner(name)` with a fixed parameter list instead of `inner(*args, **kwargs)` ties the decorator to one specific function signature; the fix is to always accept and forward `*args, **kwargs` unless the decorator is intentionally single-purpose.
- Forgetting to `return inner` (or `return decorator`) at the end of a wrapping function silently returns `None`, so the decorated name becomes unusable; every layer of a decorator must explicitly return the function or class below it.
- Forgetting `functools.wraps(func)` on the inner function leaves `__name__` and `__doc__` pointing at the wrapper instead of the original — harmless in a script, but confusing in stack traces and broken in tools like FastAPI that read a function's real signature to build documentation.
- Applying `@decor` and then also calling `decorfunction = decor(wish)` on the same name causes double wrapping, so the extra behavior runs twice; a function should be decorated exactly once, either with `@decor` or with a manual reassignment, not both.
- Stacking decorators in the wrong order — for example, `@timer` below `@retry` instead of above it — silently changes what is being measured or protected, rather than raising an error, so the intended order needs to be worked out deliberately, not guessed.
- Applying a synchronous-only decorator to an `async def` function returns an un-awaited coroutine object instead of the real result, and the bug is often only noticed much later, when something tries to use that "result" and fails somewhere unrelated.
- Building a decorator factory like `retry(max_attempts=3)` but forgetting the extra layer of nesting — writing `def retry(max_attempts, func):` instead of `def retry(max_attempts): def decorator(func): ...` — breaks the `@retry(max_attempts=3)` call syntax entirely.

## **Production Patterns**

Decorator factories are the same three-layer shape seen throughout this file, no matter which library defines them.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/students/{student_id}")
def get_student(student_id: int):
    return {"student_id": student_id, "name": "Arjun"}
```

`@app.get("/students/{student_id}")` takes configuration (a URL path) and returns the actual decorator that registers `get_student` as a route handler — structurally identical to `@retry(max_attempts=3)`.

```python
from pydantic import BaseModel, field_validator

class SignupRequest(BaseModel):
    email: str
    age: int

    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, value):
        if "@" not in value:
            raise ValueError("invalid email")
        return value
```

`@field_validator("email")` configures which field the decorator applies to, then marks the decorated method as that field's validation logic.

```python
import typer

app = typer.Typer()

@app.command()
def greet(name: str, loud: bool = False):
    message = f"Hello, {name}"
    print(message.upper() if loud else message)
```

`@app.command()` turns a plain function into a runnable CLI subcommand by reading its parameters and type hints — the same "wrap a function, read its metadata, register it somewhere" shape as a route decorator.

| Library | Key Feature | Best Use Case |
| --- | --- | --- |
| `functools` | `wraps`, `lru_cache`, `cache`, `singledispatch` — standard-library decorator building blocks | Hand-written decorators, memoization, type-based dispatch |
| `fastapi` | `@app.get`, `@app.post` register functions as HTTP route handlers | Building REST APIs |
| `pydantic` | `@field_validator`, `@model_validator` attach validation logic to model fields | Validating request or config data |
| `typer` / `click` | `@app.command`, `@click.command` turn functions into CLI subcommands | Building command-line tools |
| `tenacity` | `@retry` with backoff, jitter, and per-exception policies, sync and async both supported | Production-grade retry logic |
| `pytest` | `@pytest.fixture`, `@pytest.mark.parametrize` supply test data and setup/teardown | Testing |
| `celery` | `@shared_task` registers a function as a background/async job | Background task processing |

## **Modern Python Patterns**

Type-hinting a decorator so that a type checker still understands the wrapped function's real signature used to require importing `ParamSpec` and `TypeVar` separately.

```python
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

def timer(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(func.__name__, "took", f"{time.perf_counter() - start:.4f}s")
        return result
    return inner
```

Since Python 3.12, the same parameter and return types can be declared inline with the new generic type-parameter syntax, without importing `ParamSpec` or `TypeVar` at all.

```python
def timer[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(func.__name__, "took", f"{time.perf_counter() - start:.4f}s")
        return result
    return inner
```

`typing.override`, added in Python 3.12, is itself a decorator worth knowing about even though it is not a custom decorator being written — it marks a method as intentionally overriding a parent class method, so a type checker can flag it if the parent method is later renamed or removed.

```python
from typing import override

class ReportGenerator:
    def build(self) -> str:
        return "base report"

class PDFReportGenerator(ReportGenerator):
    @override
    def build(self) -> str:
        return "pdf report"
```

| Older Style (pre-3.10) | Modern Style (3.10+) |
| --- | --- |
| `def logger(function: C) -> C:` with `C = TypeVar('C', bound=Callable)`, losing precise argument types | `def logger[**P, R](func: Callable[P, R]) -> Callable[P, R]:` using inline generic syntax, preserving exact argument and return types |
| No standard way to flag an intentional method override | `@override` from `typing`, checked statically |
| Manually copying `__name__` and `__doc__` by hand | `@functools.wraps(func)`, copying all standard metadata in one line |

## **Quick Reference**

| Pattern | Syntax | Purpose |
| --- | --- | --- |
| Basic decorator | `def decor(func): ... return inner` | Wrap a function with extra behavior |
| Apply with `@` | `@decor` above `def f(): ...` | Shorthand for `f = decor(f)` |
| Apply manually | `wrapped = decor(f)` | Keep both the original and wrapped version callable |
| Any signature | `def inner(*args, **kwargs): ...` | Make a decorator reusable across functions |
| Preserve identity | `@functools.wraps(func)` on `inner` | Keep `__name__`, `__doc__`, and signature intact |
| Configurable decorator | `def retry(max_attempts): def decorator(func): ...` | Support `@retry(max_attempts=3)` |
| Class-based decorator | `class D: def __init__(self, func): ... def __call__(self, *a, **kw): ...` | Track state, expose extra attributes |
| Stacking | `@outer` `@inner` `def f(): ...` | Apply multiple decorators; bottom-up build, top-down run |
| Async-safe | `async def inner(*args, **kwargs): ... await func(...)` | Correctly wrap `async def` functions |
| Detect async | `inspect.iscoroutinefunction(func)` | Branch between sync and async wrapper logic |