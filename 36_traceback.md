# **Python Tracebacks**

A traceback is the report Python prints when an exception is unhandled, or when it is logged with `exc_info=True`. It looks intimidating at first, but every line in it is structured information. Once the structure is learned, any traceback can be read in a few seconds, and the bug can be found quickly instead of by guessing.

This file walks through the anatomy of a traceback, how to read one, the difference between chained tracebacks, and how to work with tracebacks programmatically using the `traceback` module and `logging`.

## **What is a Traceback?**

A **traceback** is a stack of frames, ordered from the most recently entered frame at the top to the program's entry point at the bottom. Each frame tells you:

- The file the code was in.
- The line number.
- The function name (or `<module>` for top-level code).
- The actual source line that was running.

The very last line of a traceback is the **exception line**, the type of exception and the message that came with it. Everything above it is the *path* the program took to get there.

## **Anatomy of a Traceback**

Run this program:

```python
def inner(x):
    return 10 / x

def middle(x):
    return inner(x) * 2

def outer(x):
    return middle(x) + 1

print(outer(0))
```

Output:

```
Traceback (most recent call last):
  File "demo.py", line 10, in <module>
    print(outer(0))
  File "demo.py", line 8, in outer
    return middle(x) + 1
  File "demo.py", line 5, in middle
    return inner(x) * 2
  File "demo.py", line 2, in inner
    return 10 / x
ZeroDivisionError: division by zero
```

Anatomy, top to bottom:

- **`Traceback (most recent call last):`** — the header. It is always the first line, and it always reads exactly this way.
- **Frame lines** — the path of function calls. Each frame has two parts:
  - `File "demo.py", line 10, in <module>` — the file, the line number, and the function (or `<module>`).
  - `    print(outer(0))` — the actual source line. On Python 3.11 and later, this line is often followed by a row of `^` carets pointing at the exact sub-expression that failed, thanks to PEP 657.
- **The exception line** — the very last line. It is the *type* of the exception, a colon, and the *message*:
  - `ZeroDivisionError: division by zero`

The reading order is: **read the exception line first, then read the frames top-to-bottom to understand how the program got there.** The top frame is where the exception was raised; the bottom frame is where the program started.

## **Why the Order Matters**

The frames are listed in **reverse call order**, most recent at the top, original call at the bottom. The frame nearest the exception line is always at the top. That is the line that *raised* the exception. The deeper frames are the *callers*.

In the example above:

- `inner` raised `ZeroDivisionError` on line 2 (top frame).
- `inner` was called by `middle` on line 5 (next frame).
- `middle` was called by `outer` on line 8 (next frame).
- `outer` was called by top-level code on line 10 (bottom frame).

When a bug is fixed, it is almost always fixed in the **top frame** (where the error was raised), not in the bottom one. The bottom frame is just the entry point.

## **Common Traceback Patterns**

### **Pattern 1 — single-frame traceback**

The simplest case: an error happens at the top level of a script.

```python
print(10 / 0)
```

```
Traceback (most recent call last):
  File "demo.py", line 1, in <module>
    print(10 / 0)
ZeroDivisionError: division by zero
```

Note:

- Only one frame (`<module>`), because nothing else was on the call stack.

### **Pattern 2 — multi-frame traceback (the common case)**

Function `a` calls function `b` calls function `c`, and `c` raises. The traceback lists all three frames, deepest (where the error happened) at the top.

```python
def c():
    return int("ten")

def b():
    return c()

def a():
    return b()

a()
```

```
Traceback (most recent call last):
  File "demo.py", line 9, in <module>
    a()
  File "demo.py", line 6, in a
    return b()
  File "demo.py", line 3, in b
    return c()
  File "demo.py", line 2, in c
    return int("ten")
ValueError: invalid literal for int() with base 10: 'ten'
```

Note:

- Four frames, top-down: `<module> -> a -> b -> c`.
- The actual `int("ten")` that raised is in the top frame, line 2 of `c`.

### **Pattern 3 — exception inside an `except` block (chained traceback)**

When an exception is raised *while another is being handled*, Python chains them automatically. The new exception's traceback shows up with a "During handling of the above exception, another exception occurred" separator.

```python
try:
    int("ten")
except ValueError:
    print(undefined_variable)
```

```
Traceback (most recent call last):
  File "demo.py", line 2, in <module>
    int("ten")
ValueError: invalid literal for int() with base 10: 'ten'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "demo.py", line 4, in <module>
    print(undefined_variable)
NameError: name 'undefined_variable' is not defined
```

Note:

- The first traceback is the original `ValueError`. The interpreter caught it and started running the `except` block.
- Inside the `except` block, a new exception (`NameError`) was raised.
- Python chains them automatically so both can be seen: the original problem and the new problem caused while handling it. This is usually a sign of a bug inside the `except` block itself.

### **Pattern 4 — `raise from` traceback (explicit chaining)**

When code writes `raise NewException(...) from OldException`, the traceback is explicit: it shows both exceptions and a `The above exception was the direct cause of the following exception:` line.

```python
def load_config(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError as e:
        raise RuntimeError(f"Could not load config from {path}") from e

load_config("missing.json")
```

```
Traceback (most recent call last):
  File "demo.py", line 3, in load_config
    with open(path) as f:
FileNotFoundError: [Errno 2] No such file or directory: 'missing.json'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "demo.py", line 8, in <module>
    load_config("missing.json")
  File "demo.py", line 6, in load_config
    raise RuntimeError(f"Could not load config from {path}") from e
RuntimeError: Could not load config from missing.json
```

Note:

- The first (lower-numbered lines) traceback is the *cause*: the real `FileNotFoundError`, which ends up stored in `e.__cause__` of the `RuntimeError`.
- The second traceback is the *new* exception the caller actually sees: `RuntimeError`.
- The `from e` clause is what makes this an explicit `__cause__`, as opposed to the implicit `__context__` seen in Pattern 3. This is the standard way to re-raise a low-level error as a higher-level, application-specific one, which is common in real backend code (turning a `FileNotFoundError` or a database driver error into a domain error like `ConfigError` or `RepositoryError`).

### **Pattern 5 — `from None` (suppressed cause)**

Writing `raise NewException(...) from None` hides the original cause from the printed traceback. This is appropriate when the original error contains internal details, such as database connection strings or file paths, that should not be shown to an end user or an API caller.

```python
def get_user(user_id):
    try:
        return db_query(user_id)
    except DatabaseError:
        raise UserNotFoundError(user_id) from None

get_user(42)
```

```
Traceback (most recent call last):
  File "demo.py", line 7, in <module>
    get_user(42)
  File "demo.py", line 5, in get_user
    raise UserNotFoundError(user_id) from None
UserNotFoundError: user 42 not found
```

Note:

- The `DatabaseError` that triggered the `UserNotFoundError` is gone from the printed traceback. Only `UserNotFoundError` is shown.
- `__cause__` is explicitly set to `None`. The implicit `__context__` may still be set internally, but it is not printed because `from None` was used.
- This pattern is common at the boundary of a system, for example an API layer that does not want to leak internal exception details to a client, while still logging the full original traceback internally before suppressing it in the response.

## **Reading a Traceback Step by Step**

Given this program:

```python
def apply_discount(price, percent):
    return price * (1 - percent / 100)

def checkout(cart, percent):
    for item in cart:
        discounted = apply_discount(item["price"], percent)
        item["final"] = discounted
    return cart

print(checkout([{"price": {"amount": 100, "currency": "USD"}}], 150))
```

Output:

```
Traceback (most recent call last):
  File "shop.py", line 10, in <module>
    print(checkout([{"price": {"amount": 100, "currency": "USD"}}], 150))
  File "shop.py", line 6, in checkout
    discounted = apply_discount(item["price"], percent)
  File "shop.py", line 2, in apply_discount
    return price * (1 - percent / 100)
TypeError: unsupported operand type(s) for *: 'dict' and 'float'
```

Step-by-step reading:

1. **The last line:** `TypeError: unsupported operand type(s) for *: 'dict' and 'float'`. Somewhere, Python tried to multiply a `dict` by a `float`, which is not allowed.
2. **The top frame:** `shop.py, line 2, in apply_discount`, the `return price * (1 - percent / 100)` line. The multiplication itself happens here.
3. **The next frame:** `shop.py, line 6, in checkout`, the caller. It passed `item["price"]` as the first argument. The cart entry stored `"price"` as a nested dict (`{"amount": 100, "currency": "USD"}`) instead of a plain number, which is why `apply_discount` received a `dict` instead of an `int` or `float`.
4. **The data flow:** the bug is not in `apply_discount` itself; it is upstream, wherever the cart item was built with the wrong shape for `"price"`.

This is the general workflow for any traceback: read the exception line, then the top frame, then walk down the call stack to understand the data flow that led there.

## **The `traceback` Module**

Python ships with a `traceback` module that works with tracebacks as objects instead of only as printed text. The most useful functions are:

| Function | What it returns |
|---|---|
| `traceback.print_exc()` | Print the current exception's traceback to `sys.stderr` (or any file passed to it) |
| `traceback.format_exc()` | Return the traceback as a string |
| `traceback.format_exception(exc)` | Format a specific exception as a list of strings |
| `traceback.extract_tb(tb)` | Walk a traceback object and return a list of frame summaries |
| `traceback.print_exception(exc)` | Print a specific exception, including one caught earlier and stored |

### **Example — log the traceback instead of crashing**

```python
import logging
import traceback

logging.basicConfig(level=logging.INFO)

def risky():
    return 1 / 0

try:
    risky()
except Exception:
    logging.error("Something went wrong:\n%s", traceback.format_exc())
    print("Program continues normally after logging")
```

```
ERROR:root:Something went wrong:
Traceback (most recent call last):
  File "demo.py", line 10, in <module>
    risky()
  File "demo.py", line 7, in risky
    return 1 / 0
ZeroDivisionError: division by zero
Program continues normally after logging
```

Note:

- `traceback.format_exc()` returns the traceback as a string. The program caught the exception, logged it, and continued running instead of crashing.

### **Example — programmatically inspect frames**

```python
import traceback

def c():
    return 1 / 0

def b():
    return c()

def a():
    return b()

try:
    a()
except Exception as e:
    frames = traceback.extract_tb(e.__traceback__)
    print(f"Exception: {type(e).__name__}: {e}")
    print(f"Frames from deepest to shallowest ({len(frames)} total):")
    for frame in frames:
        print(f"  {frame.filename}:{frame.lineno} in {frame.name}() -> {frame.line}")
```

```
Exception: ZeroDivisionError: division by zero
Frames from deepest to shallowest (4 total):
  demo.py:14 in <module>() -> a()
  demo.py:11 in a() -> return b()
  demo.py:8 in b() -> return c()
  demo.py:4 in c() -> return 1 / 0
```

Note:

- `traceback.extract_tb` returns a list of `FrameSummary` objects. Each one has `.filename`, `.lineno`, `.name`, and `.line`.
- `frames` is a plain list, so `len(frames)` works directly. This is how loggers, profilers, and error-tracking tools (such as Sentry-style services) programmatically walk the call stack to build structured error reports.

### **Example — `sys.exc_info()`, the low-level way**

```python
import sys
import traceback

try:
    int("ten")
except Exception:
    exc_type, exc_value, exc_tb = sys.exc_info()
    print("Type:    ", exc_type.__name__)
    print("Message: ", exc_value)
    print("Traceback object:", type(exc_tb).__name__)
    print("Number of frames:", len(traceback.extract_tb(exc_tb)))
```

```
Type:     ValueError
Message:  invalid literal for int() with base 10: 'ten'
Traceback object: traceback
Number of frames: 1
```

Note:

- `sys.exc_info()` returns the currently handled exception's type, value, and traceback object. It returns `(None, None, None)` outside an `except` block, so it is only useful inside one.
- A raw traceback object does not support `len()` directly. To count frames, pass it through `traceback.extract_tb(...)` first, which returns a plain list.
- The third element, `exc_tb`, is the same traceback object attached to the exception itself as `e.__traceback__`.

## **Tracebacks in Logging**

The `logging` module has first-class support for tracebacks. The common pattern is to call `logging.exception(...)` (or pass `exc_info=True` to `logger.error(...)`).

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def divide(a, b):
    return a / b

def process(values):
    for v in values:
        try:
            print(f"  {v} / 2 = {divide(v, 2)}")
        except ZeroDivisionError:
            logging.exception(f"Failed to process {v!r}")

print("Starting...")
process([10, 0, 20])
print("Done.")
```

```
Starting...
  10 / 2 = 5.0
2026-07-23 07:46:26,123 [ERROR] Failed to process 0
Traceback (most recent call last):
  File "demo.py", line 15, in process
    print(f"  {v} / 2 = {divide(v, 2)}")
  File "demo.py", line 9, in divide
    return a / b
ZeroDivisionError: division by zero
  20 / 2 = 10.0
Done.
```

Note:

- `logging.exception(...)` logs the message and the current traceback together, at `ERROR` level.
- The program continued after the failure; `20 / 2` was still processed. This is the standard production pattern: log the failure with its full traceback, then keep going instead of crashing the whole process for one bad item.

### **Real-world pattern — a web request handler that logs but never leaks internals**

```python
import logging
import traceback

logging.basicConfig(level=logging.INFO)

class NotFoundError(Exception):
    pass

def fetch_record(record_id, database):
    if record_id not in database:
        raise NotFoundError(f"record {record_id} not found")
    return database[record_id]

def handle_request(record_id, database):
    """
    Simulates a request handler in a web framework.
    Internal exceptions are logged in full, but the caller only
    ever receives a safe, generic response.
    """
    try:
        record = fetch_record(record_id, database)
        return {"status": 200, "data": record}
    except NotFoundError:
        logging.warning("Record %s was requested but does not exist", record_id)
        return {"status": 404, "error": "record not found"}
    except Exception:
        logging.error("Unexpected error handling request:\n%s", traceback.format_exc())
        return {"status": 500, "error": "internal server error"}

db = {1: {"name": "Priya"}, 2: {"name": "Aman"}}

print(handle_request(1, db))
print(handle_request(99, db))
```

```
{'status': 200, 'data': {'name': 'Priya'}}
2026-07-23 07:46:26,456 WARNING:root:Record 99 was requested but does not exist
{'status': 404, 'error': 'record not found'}
```

Note:

- Expected failures, such as a missing record, are logged at `WARNING` and turned into a normal 404 response.
- Truly unexpected exceptions are logged at `ERROR` with the full traceback captured through `traceback.format_exc()`, while the caller still only receives a generic `500` message. This separation, log everything internally, expose almost nothing externally, is the core traceback-handling pattern used in production web services.

## **Caveats and Edge Cases**

### **A traceback object only exists while its exception is live**

Outside an `except` block, `sys.exc_info()` returns `(None, None, None)`. A traceback object exists while the exception is propagating or while something still holds a reference to it (through `e.__traceback__`, for example).

```python
try:
    1 / 0
except ZeroDivisionError as e:
    tb = e.__traceback__
    print("Got traceback:", type(tb).__name__)

# Outside the except block, sys.exc_info() is all None
import sys
print("After handling:", sys.exc_info())
```

```
Got traceback: traceback
After handling: (None, None, None)
```

Note:

- Inside the `except` block, the traceback is accessible via `e.__traceback__`. Outside it, `sys.exc_info()` is reset to all `None`.

### **`__traceback__` attribute on exception objects**

Every exception object carries its own traceback in `__traceback__`. A reference to the exception can be kept and inspected later, even after the `except` block has finished.

```python
import traceback

saved = None

try:
    int("ten")
except ValueError as e:
    saved = e
    print("Caught:", e)

# Later, possibly in a different function
print("Still have it:", saved)
print("Type:        ", type(saved).__name__)
print("Message:     ", saved)
print("Number of frames:", len(traceback.extract_tb(saved.__traceback__)))
```

```
Caught: invalid literal for int() with base 10: 'ten'
Still have it: invalid literal for int() with base 10: 'ten'
Type:         ValueError
Message:      invalid literal for int() with base 10: 'ten'
Number of frames: 1
```

Note:

- The exception object `saved` stays alive as long as something holds a reference to it, and its traceback stays attached to it.
- Holding on to many exception objects (for example, appending every failure to a list in a long-running batch job) also keeps their tracebacks, and everything the tracebacks reference, alive in memory. For long batch jobs it is usually better to store `traceback.format_exc()` (a plain string) rather than the exception object itself.

### **Fine-grained error locations (PEP 657) and how to turn them off**

Since Python 3.11, tracebacks include column-level information: a row of `^` carets under the frame's source line, pointing at the exact sub-expression that failed. This is especially useful on long lines with several operations.

```python
def compute(a, b, c):
    return a + b / c

compute(1, 2, 0)
```

```
Traceback (most recent call last):
  File "demo.py", line 4, in <module>
    compute(1, 2, 0)
  File "demo.py", line 2, in compute
    return a + b / c
               ~~^~~
ZeroDivisionError: division by zero
```

Note:

- The `~~^~~` markers point specifically at `b / c`, not the whole line, even though the line also contains `a +`. This matters a great deal once expressions get longer, such as chained attribute access or several arithmetic operations on one line.
- This feature stores extra position data in compiled code objects, which uses a small amount of extra memory and disk space. It can be disabled with the `-X no_debug_ranges` command-line option, or by setting the `PYTHONNODEBUGRANGES` environment variable, if that overhead matters in a memory-constrained environment.

## **Examples**

### **Example 1 — read a multi-frame traceback**

```python
def c(): return 1 / 0
def b(): return c()
def a(): return b()
a()
```

```
Traceback (most recent call last):
  File "demo.py", line 4, in <module>
    a()
  File "demo.py", line 3, in a
    return b()
  File "demo.py", line 2, in b
    return c()
  File "demo.py", line 1, in c
    return 1 / 0
ZeroDivisionError: division by zero
```

Note:

- Top frame (`c`, line 1): the actual `1 / 0`.
- Below it: `b -> a -> <module>`, the chain of callers.

### **Example 2 — traceback from a list index out of range**

```python
def get_name(people, idx):
    return people[idx]["name"]

people = [{"name": "Durga"}, {"name": "Karan"}]
print(get_name(people, 5))
```

```
Traceback (most recent call last):
  File "demo.py", line 5, in <module>
    print(get_name(people, 5))
  File "demo.py", line 2, in get_name
    return people[idx]["name"]
IndexError: list index out of range
```

Note:

- The exception is `IndexError`. The fix is to check that `idx` is within range before indexing, or to use `.get`-style safe access where it makes sense.

### **Example 3 — `NameError` from a typo**

```python
def calc():
    total = 10
    return toatl + 5

calc()
```

```
Traceback (most recent call last):
  File "demo.py", line 4, in <module>
    calc()
  File "demo.py", line 3, in calc
    return toatl + 5
NameError: name 'toatl' is not defined. Did you mean: 'total'?
```

Note:

- Since Python 3.10, tracebacks sometimes suggest the correct spelling for a `NameError` or `AttributeError`. The error itself is still a `NameError`; the suggestion is just a hint.

### **Example 4 — `KeyError` from a missing dict key**

```python
config = {"host": "localhost", "port": 8080}
print(config["hosst"])
```

```
Traceback (most recent call last):
  File "demo.py", line 2, in <module>
    print(config["hosst"])
KeyError: 'hosst'
```

Note:

- The message shows the actual key that was missing, including typos like `'hosst'`. Compare it against the dict's real keys to spot the mistake. Using `config.get("host")` with a sensible default is often safer than direct indexing for keys that might be absent.

### **Example 5 — traceback preserved across re-raise**

```python
def level_3():
    return 1 / 0

def level_2():
    try:
        level_3()
    except Exception:
        raise    # bare raise: same exception, same traceback

def level_1():
    level_2()

level_1()
```

```
Traceback (most recent call last):
  File "demo.py", line 12, in <module>
    level_1()
  File "demo.py", line 9, in level_1
    level_2()
  File "demo.py", line 4, in level_2
    level_3()
  File "demo.py", line 2, in level_3
    return 1 / 0
ZeroDivisionError: division by zero
```

Note:

- Even though `level_2` caught and re-raised, the traceback still shows `level_3` as the origin. A bare `raise` (with no arguments) preserves the original traceback exactly. Writing `raise e` instead of a bare `raise` inside an `except Exception as e:` block would reset part of the traceback and is usually a mistake.

### **Example 6 — `traceback.format_exc()` to convert to a string**

```python
import traceback

try:
    {"a": 1}["b"]
except KeyError:
    tb_text = traceback.format_exc()
    print("Type:    str")
    print("Length: ", len(tb_text), "characters")
    print("---")
    print(tb_text, end="")
```

```
Type:    str
Length:  123 characters
---
Traceback (most recent call last):
  File "demo.py", line 5, in <module>
    {"a": 1}["b"]
KeyError: 'b'
```

Note:

- `format_exc()` returns the traceback as a multi-line string, which can be stored, sent over the network, written to a file, or attached to a bug report.

### **Example 7 — using `sys.exception()` in Python 3.11+**

```python
import sys

try:
    int("ten")
except Exception:
    # Python 3.11+: sys.exception() returns the live exception directly
    exc = sys.exception()
    print("Live exception:", type(exc).__name__, "->", exc)
```

```
Live exception: ValueError -> invalid literal for int() with base 10: 'ten'
```

Note:

- `sys.exception()` is the modern way to get the current exception inside an `except` block. It is equivalent to `sys.exc_info()[1]`, but with cleaner, more direct semantics.

### **Example 8 — retrying a flaky network call and only logging the final failure**

```python
import time
import logging
import traceback
import random

logging.basicConfig(level=logging.INFO)

class ServiceUnavailable(Exception):
    pass

def call_external_service(attempt):
    # Simulates a network call that fails on the first two tries
    if attempt < 3:
        raise ServiceUnavailable(f"service timed out on attempt {attempt}")
    return {"result": "ok"}

def call_with_retries(max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        try:
            return call_with_logging(attempt)
        except ServiceUnavailable:
            if attempt == max_attempts:
                logging.error("All retries failed:\n%s", traceback.format_exc())
                raise
            logging.info("Attempt %d failed, retrying...", attempt)
            time.sleep(0)  # would normally be a real delay

def call_with_logging(attempt):
    return call_external_service(attempt)

print(call_with_retries(max_attempts=3))
```

```
2026-07-23 07:46:26,789 INFO:root:Attempt 1 failed, retrying...
2026-07-23 07:46:26,790 INFO:root:Attempt 2 failed, retrying...
{'result': 'ok'}
```

Note:

- Intermediate failures are logged briefly, without a full traceback, since they are expected and being retried.
- Only the final failure, if every retry is exhausted, gets a full `traceback.format_exc()` in the log. This keeps logs readable during normal transient failures while still preserving complete diagnostic information when a retry loop truly gives up.

## **Q&A**

**Q1. What is a traceback?**
A report Python prints when an exception is raised. It contains the call stack, from the most recent frame at the top to the entry point at the bottom, plus the exception type and message on the last line.

**Q2. Which line of the traceback is the most important?**
The last line: the exception type and message. The top frame is the second most important; it is the line of code that actually raised the exception.

**Q3. How can a traceback be printed for a caught exception?**
Use `traceback.print_exc()` or `traceback.format_exc()` inside the `except` block, or use `logging.exception("message")` to log it together with the traceback.

**Q4. What is the difference between `__cause__` and `__context__`?**
`__cause__` is set by an explicit `raise X from Y`. `__context__` is set automatically whenever a new exception is raised while another one is already being handled. Use `raise X from Y` to be explicit about chaining, and `raise X from None` to suppress showing the original cause.

**Q5. How can a traceback be walked programmatically?**
Use `traceback.extract_tb(exc.__traceback__)` to get a list of `FrameSummary` objects (filename, line number, function name, source line). Use `traceback.format_exception(exc)` to get the whole traceback as a list of strings. A raw traceback object does not support `len()` directly; convert it with `extract_tb` first.

**Q6. Why do some tracebacks show `^^^^` markers under a line?**
That is PEP 657's fine-grained error locations, available since Python 3.11. Instead of only pointing at a whole line, the interpreter points at the exact sub-expression that raised, which is useful on lines that contain several operations. It can be turned off with `-X no_debug_ranges` or the `PYTHONNODEBUGRANGES` environment variable.

**Q7. Is it safe to hold on to caught exception objects for later?**
It works, but every exception keeps its whole traceback alive, along with anything referenced from those frames. For long-running programs that collect many failures, it is usually lighter to store `traceback.format_exc()` as a string rather than keeping the exception objects themselves.

## **Quick Reference Summary**

### **Parts of a Traceback**

| Part | What it tells you |
|---|---|
| `Traceback (most recent call last):` | The header, always this exact text |
| Each frame line | File, line number, function, and source line for one call |
| `^^^^` markers (3.11+) | The exact sub-expression that failed on that line |
| The last line | The exception type and message |

### **Reading Order**

| Order | What to look for |
|---|---|
| 1st | The exception type and message (last line) |
| 2nd | The top frame, where the error was raised |
| 3rd | Walk down the call stack to understand the data flow |

### **The `traceback` Module**

| Function | Returns |
|---|---|
| `traceback.print_exc()` | Prints the current traceback to `sys.stderr` |
| `traceback.format_exc()` | Returns the current traceback as a string |
| `traceback.format_exception(exc)` | Returns a specific exception's traceback as a list of strings |
| `traceback.extract_tb(tb)` | Returns a list of frame summaries (has a normal `len()`) |
| `traceback.print_exception(exc)` | Prints a specific, previously caught exception |

### **Chaining Traces**

| Form | `__cause__` | `__context__` | Traceback shows |
|---|---|---|---|
| `raise` (bare) | unchanged | unchanged | Original traceback, unmodified |
| `raise X` inside `except` | unchanged | set to current | Two tracebacks joined by "During handling of..." |
| `raise X from Y` | set to `Y` | unchanged | Two tracebacks joined by "The above exception was the direct cause of..." |
| `raise X from None` | set to `None` | unchanged | Only the new exception's traceback |

## **Practice and Next Steps**

1. **Read five real tracebacks.** Take any five tracebacks seen recently, whether personal or from a tutorial. For each, write down the exception type, the message, the top frame, and the data flow that led there.
2. **Log a traceback.** Write a small script that catches an exception, logs it with `logging.exception(...)`, and continues. Confirm the traceback shows up in the log output.
3. **Walk a traceback programmatically.** Use `traceback.extract_tb` to print every frame's filename, line number, function name, and source line from a caught exception.
4. **Compare `__cause__` vs `__context__`.** Write two versions of similar code: one using `raise X from Y`, the other using a plain `raise X` inside an `except` block. Print `e.__cause__` and `e.__context__` for both and notice the difference.
5. **Build a tiny error reporter.** Use `traceback.format_exc()` to capture a traceback as a string, then write it to a file, simulating a "send this to a logging or monitoring service" flow.
6. **Compare traceback markers.** On Python 3.11 or later, write a function with a long line containing more than one operation (for example `total = compute_a(x) + compute_b(y)`), make one call fail, and see exactly which part the `^^^^` markers point to.
7. **Try `-X no_debug_ranges`.** Run the same failing script both normally and with `python -X no_debug_ranges script.py`, and compare how the traceback output changes.
