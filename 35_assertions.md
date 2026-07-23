# **Python Assertions**

The `assert` statement is a debugging aid, not a validation tool. It evaluates an expression, and if the result is falsy, it raises an `AssertionError`. The idea is simple: place `assert`s into code that *should* always be true, and Python will stop the program the moment one of those assumptions breaks.

This file covers what `assert` does, the exact syntax, how the optional message works, when to use it, when to avoid it, and how it behaves in real production and testing code.

## **What is an Assertion?**

An **assertion** is a sanity check written into the code itself. It says: "I, the programmer, am *certain* this condition is true at this point. If it is not, something is so broken that the program cannot continue safely."

The `assert` statement is the Python syntax for writing that sanity check. It is meant to catch **bugs in your own code**, not bad input from a user, a file, a network call, or a database.

## **Basic Syntax**

```python
assert <expression>
assert <expression>, <message>
```

Two forms:

- `assert <expression>` — if `<expression>` is falsy, raise `AssertionError`.
- `assert <expression>, <message>` — same, but the exception carries `<message>` as its description.

**Example 1 — no message:**

```python
def set_age(age):
    assert age >= 0
    print(f"Age set to {age}")

set_age(25)
set_age(-1)
```

```
Age set to 25
Traceback (most recent call last):
  File "test.py", line 6, in <module>
    set_age(-1)
  File "test.py", line 2, in set_age
    assert age >= 0
AssertionError
```

**Example 2 — with a helpful message:**

```python
def set_age(age):
    assert age >= 0, f"age cannot be negative, got {age}"
    print(f"Age set to {age}")

set_age(-1)
```

```
Traceback (most recent call last):
  File "test.py", line 6, in <module>
    set_age(-1)
  File "test.py", line 2, in set_age
    assert age >= 0, f"age cannot be negative, got {age}"
AssertionError: age cannot be negative, got -1
```

Notes:

- Without a message, the traceback just says `AssertionError`, which tells the programmer that *something* failed but not what.
- With a message, the value of `<message>` is shown after the colon, exactly like any other exception.
- Always prefer the message form. It costs nothing to write and saves debugging time later.

## **Core Mechanics**

### **What counts as "falsy" for `assert`?**

The `assert` statement calls `bool(<expression>)`. Anything that is falsy fails the assertion. Everything else passes.

Falsy values in Python: `False`, `0`, `0.0`, `None`, empty string `""`, empty list `[]`, empty dict `{}`, empty tuple `()`, empty set `set()`.

```python
def check(value):
    assert value, f"value {value!r} is falsy"
    print("passed:", value)

check(1)
check("hello")
check(0)
check("")
check(None)
check([])
```

```
passed: 1
passed: hello
Traceback (most recent call last):
  File "test.py", line 2, in <module>
    check(0)
  File "test.py", line 2, in check
    assert value, f"value {value!r} is falsy"
AssertionError: value 0 is falsy
```

(After the traceback, `check("")`, `check(None)`, `check([])` would also fail, but the program already terminated on the first failure.)

### **A common mistake: asserting a tuple**

Writing `assert (condition, message)` is a classic bug. A non-empty tuple is always truthy, so the assertion never fails no matter what the condition is.

```python
# Wrong — this tuple is always truthy, so the assert never fires
assert (2 + 2 == 5, "math is broken")
print("this line always runs, even though 2 + 2 != 5")

# Right — no parentheses around the whole thing
assert 2 + 2 == 5, "math is broken"
```

```
this line always runs, even though 2 + 2 != 5
Traceback (most recent call last):
  File "test.py", line 6, in <module>
    assert 2 + 2 == 5, "math is broken"
AssertionError: math is broken
```

Modern Python (3.9 and later) actually issues a `SyntaxWarning` for `assert (x, "message")` precisely because this mistake is so common.

### **Three equivalent ways to write an assert**

```python
# Form 1: simple condition
assert x > 0

# Form 2: simple condition with message
assert x > 0, "x must be positive"

# Form 3: equivalent expanded form (what Python actually does)
if __debug__:
    if not (x > 0):
        raise AssertionError("x must be positive")
```

`__debug__` is a built-in constant that is `True` unless Python was started with the `-O` optimization flag. That is the key to the next topic: how to *disable* all assertions in production.

### **Disabling assertions: `python -O`**

Running Python with `-O` (capital O, for "optimize") sets `__debug__` to `False` and *removes* every `assert` statement before the code runs. This makes the program slightly faster, but it is dangerous: any `assert` you wrote becomes a no-op, as if it were never there.

```python
# Save as script.py
# Run with:      python script.py
# Then run with: python -O script.py

def divide(a, b):
    assert b != 0, "divisor must be non-zero"
    return a / b

print(divide(10, 0))
```

**Run 1 — `python script.py`:**

```
Traceback (most recent call last):
  File "script.py", line 7, in <module>
    print(divide(10, 0))
  File "script.py", line 3, in divide
    assert b != 0, "divisor must be non-zero"
AssertionError: divisor must be non-zero
```

**Run 2 — `python -O script.py`:**

```
Traceback (most recent call last):
  File "script.py", line 3, in divide
    return a / b
ZeroDivisionError: division by zero
```

Notes:

- The same code, run the same way, produces a different error depending on the flag.
- With `-O`, the `assert` was stripped, so the program went straight to `10 / 0`, and the *user* got a raw `ZeroDivisionError` instead of the clear, programmer-written `AssertionError`.
- This is exactly why `assert` must never be the only line standing between your program and bad input.

## **When to Use Assertions**

Use `assert` for conditions that should be **logically impossible** to violate if your code is correct. These are internal checks about the *state of the program*, not checks about *external input*.

| Good use of `assert` | Why it fits |
|---|---|
| Internal invariants (e.g. `assert balance >= 0` inside your own account class) | If the invariant breaks, the class itself has a bug. |
| Type-like sanity checks (e.g. `assert isinstance(x, int)`) | A clear "this should be an int" note for other programmers. |
| Post-conditions (e.g. after sorting, `assert result == sorted(result)`) | A self-check that your own logic actually worked. |
| Documenting assumptions in code | `assert len(items) > 0` reads as "we expect items to be non-empty here". |
| Verifying function preconditions during development | Catches misuse of your own helper functions early, before shipping. |
| Checking configuration consistency at startup | If two settings that must agree do not, the app should refuse to boot in a controlled way, before `-O` is stripped in a debug run. |
| Catching your own bugs early | This is the entire purpose of `assert`. |

## **When NOT to Use Assertions**

| Bad use of `assert` | Why it is wrong |
|---|---|
| Validating user input (forms, CLI arguments, API request bodies) | `assert` can be disabled with `-O`. A bad user should never be able to silently break your program. Use `if`/`raise` instead. |
| Validating data from a file, network response, or database row | Same reason — external data is not under the programmer's control and can be malformed. |
| Enforcing business rules (e.g. "an order cannot ship with zero items") | Business rules must always be enforced, in every run mode, so they need `raise`, not `assert`. |
| Checking permissions or authentication | A stripped `assert` would mean a permission check silently vanishes. This is a security risk. |
| As a substitute for `raise` in library code that others will call | Callers of your library cannot rely on an `assert` staying active; use explicit exceptions instead. |
| Any check where the *program* should react and recover from the failure | Production code should handle the failure gracefully, not crash with an unhandled `AssertionError`. |

**The rule:** if the condition is something a user, a file, a network call, or an attacker could cause, use `if` + `raise`. If the condition is something only a bug in your own code could cause, use `assert`.

## **Examples**

### **Example 1 — `assert` for internal invariants**

```python
class Wallet:
    def __init__(self, balance):
        assert balance >= 0, f"initial balance cannot be negative, got {balance}"
        self.balance = balance

    def withdraw(self, amount):
        assert amount > 0, "withdrawal must be positive"
        self.balance -= amount
        assert self.balance >= 0, f"BUG: balance went negative ({self.balance})"

w = Wallet(100)
w.withdraw(30)
print("balance:", w.balance)
w.withdraw(80)
```

```
balance: 70
Traceback (most recent call last):
  File "test.py", line 15, in <module>
    w.withdraw(80)
  File "test.py", line 10, in withdraw
    assert self.balance >= 0, f"BUG: balance went negative ({self.balance})"
AssertionError: BUG: balance went negative (-10)
```

Notes:

- The first two `assert`s validate arguments and the invariant, catching programmer errors at the source.
- The third `assert` documents the *post-condition*: after a withdrawal, balance should still be non-negative. The instant it broke, the `AssertionError` pointed straight at the bug.

### **Example 2 — `assert` for type-like sanity checks**

```python
def greet(name):
    assert isinstance(name, str), f"expected str, got {type(name).__name__}"
    print(f"Hello, {name}!")

greet("Karan")
greet(42)
```

```
Hello, Karan!
Traceback (most recent call last):
  File "test.py", line 5, in <module>
    greet(42)
  File "test.py", line 2, in greet
    assert isinstance(name, str), f"expected str, got {type(name).__name__}"
AssertionError: expected str, got int
```

Note:

- This is a *programmer* check, not a user check. The function is internal helper code, so it is reasonable to assume the caller passes a string.

### **Example 3 — `assert` inside loops and iteration**

```python
def all_positive(numbers):
    for n in numbers:
        assert n > 0, f"all numbers must be positive, got {n}"
        print("ok:", n)

all_positive([1, 2, 3, 4])
all_positive([1, -1, 2])
```

```
ok: 1
ok: 2
ok: 3
ok: 4
ok: 1
Traceback (most recent call last):
  File "test.py", line 8, in <module>
    all_positive([1, -1, 2])
  File "test.py", line 3, in all_positive
    assert n > 0, f"all numbers must be positive, got {n}"
AssertionError: all numbers must be positive, got -1
```

Note:

- The first list passed all four numbers before the loop ended. The second list failed on the *first* violation, with the offending value shown in the message.

### **Example 4 — `assert` for post-conditions**

```python
def sorted_ascending(items):
    result = sorted(items)
    assert all(result[i] <= result[i + 1] for i in range(len(result) - 1)), "result is not sorted"
    return result

print(sorted_ascending([3, 1, 4, 1, 5, 9, 2, 6]))
print(sorted_ascending([1, 2, 3]))
```

```
[1, 1, 2, 3, 4, 5, 6, 9]
[1, 2, 3]
```

Note:

- The `assert` checks the *post-condition*: the function that was just written actually returned a sorted list. If `sorted()` or the custom logic around it ever had a bug, the `assert` would catch it immediately instead of letting bad data flow downstream.

### **Example 5 — `assert` for documenting assumptions**

```python
def process_order(order):
    assert "id" in order, "order must have an 'id' field"
    assert order["qty"] > 0, "order quantity must be positive"
    print(f"Processing order {order['id']} for {order['qty']} items")

process_order({"id": 101, "qty": 3})
process_order({"qty": 3})              # missing id
process_order({"id": 102, "qty": 0})   # zero qty
```

```
Processing order 101 for 3 items
Traceback (most recent call last):
  File "test.py", line 7, in <module>
    process_order({"qty": 3})
  File "test.py", line 2, in process_order
    assert "id" in order, "order must have an 'id' field"
AssertionError: order must have an 'id' field
```

Note:

- These are programmer-facing checks: the function expects a dict with a specific shape, built earlier in the same program. If a caller forgets a field, they get a clear message instead of a confusing `KeyError` several lines later.

### **Example 6 — `assert` is NOT for input validation (the right way)**

```python
# Wrong — assert can be disabled with python -O
def withdraw_wrong(balance, amount):
    assert amount > 0, "amount must be positive"
    return balance - amount

# Right — explicit raise, cannot be disabled
def withdraw_right(balance, amount):
    if amount <= 0:
        raise ValueError(f"amount must be positive, got {amount}")
    return balance - amount

print(withdraw_wrong(100, -50))   # in -O mode this "succeeds" and returns 150, a bug
print(withdraw_right(100, -50))   # always raises, no matter how Python is started
```

```
Traceback (most recent call last):
  File "test.py", line 12, in <module>
    print(withdraw_wrong(100, -50))
  File "test.py", line 3, in withdraw_wrong
    assert amount > 0, "amount must be positive"
AssertionError: amount must be positive
```

Note:

- Under normal execution both functions raise. But run the file with `python -O`, and `withdraw_wrong(100, -50)` silently returns `150`, adding money by mistake, while `withdraw_right` still raises `ValueError` every time.
- This is the single most important rule in this file: never let `assert` be the only gate between your program and money, security, or correctness-critical data.

### **Example 7 — validating a web API request (real backend pattern)**

```python
class BadRequest(Exception):
    pass

def create_user_endpoint(payload):
    # This looks like a request body coming from a client. Never trust it with assert.
    if not isinstance(payload, dict):
        raise BadRequest("request body must be a JSON object")
    if "email" not in payload or not payload["email"]:
        raise BadRequest("email is required")
    if "age" not in payload:
        raise BadRequest("age is required")

    # Internal invariant: by this point the payload is already validated,
    # so this assert is just documenting that guarantee for other developers.
    assert "email" in payload and "age" in payload, "payload should be validated by now"

    return {"status": "created", "email": payload["email"]}

print(create_user_endpoint({"email": "test@example.com", "age": 30}))
print(create_user_endpoint({"age": 30}))
```

```
{'status': 'created', 'email': 'test@example.com'}
Traceback (most recent call last):
  File "test.py", line 17, in <module>
    print(create_user_endpoint({"age": 30}))
  File "test.py", line 7, in create_user_endpoint
    raise BadRequest("email is required")
BadRequest: email is required
```

Note:

- The client-facing checks use `if`/`raise` with a custom exception, so a malformed request always gets a proper error response, in every run mode.
- The trailing `assert` is purely for other developers reading the function later; it documents an assumption that should already be true and would only fail if someone edited the function incorrectly.

### **Example 8 — `assert` for verifying a recursive function**

```python
def factorial(n):
    assert n >= 0, f"factorial is undefined for negative numbers, got {n}"
    if n in (0, 1):
        return 1
    result = n * factorial(n - 1)
    assert result > 0, f"BUG: factorial produced a non-positive result ({result})"
    return result

print(factorial(5))
print(factorial(-3))
```

```
120
Traceback (most recent call last):
  File "test.py", line 9, in <module>
    print(factorial(-3))
  File "test.py", line 2, in factorial
    assert n >= 0, f"factorial is undefined for negative numbers, got {n}"
AssertionError: factorial is undefined for negative numbers, got -3
```

Note:

- The precondition `assert n >= 0` runs on every recursive call, so it also protects the base case.
- The post-condition `assert result > 0` would catch an integer overflow style bug in a language that has one; in Python it mainly documents the expected shape of the result.

### **Example 9 — `assert` for verifying data pipeline steps**

```python
def clean_scores(raw_scores):
    cleaned = [s for s in raw_scores if s is not None]
    assert len(cleaned) <= len(raw_scores), "cleaning should never add rows"
    assert all(isinstance(s, (int, float)) for s in cleaned), "all scores must be numeric after cleaning"
    return cleaned

def average(scores):
    cleaned = clean_scores(scores)
    assert len(cleaned) > 0, "cannot average an empty list of scores"
    return sum(cleaned) / len(cleaned)

print(average([80, 90, None, 70]))
print(average([None, None]))
```

```
80.0
Traceback (most recent call last):
  File "test.py", line 12, in <module>
    print(average([None, None]))
  File "test.py", line 8, in average
    assert len(cleaned) > 0, "cannot average an empty list of scores"
AssertionError: cannot average an empty list of scores
```

Note:

- Each step in the small pipeline checks its own assumption about the data it just produced. This makes it much easier to find which step introduced a bug, instead of chasing a confusing `ZeroDivisionError` from `sum(cleaned) / len(cleaned)`.

### **Example 10 — Catching `AssertionError` in tests**

```python
def apply_discount(price, percent):
    assert 0 <= percent <= 100, f"percent must be 0-100, got {percent}"
    return price * (1 - percent / 100)

tests = [
    (100, 10,  90.0),
    (100, 0,  100.0),
    (100, 100, 0.0),
    (100, 150, "should raise"),
    (100, -5,  "should raise"),
]

for price, pct, expected in tests:
    try:
        result = apply_discount(price, pct)
        status = "ok" if result == expected else "FAIL"
        print(f"  apply_discount({price}, {pct}) = {result} -> {status}")
    except AssertionError as e:
        status = "ok" if expected == "should raise" else "FAIL"
        print(f"  apply_discount({price}, {pct}) raised: {e} -> {status}")
```

```
  apply_discount(100, 10) = 90.0 -> ok
  apply_discount(100, 0) = 100.0 -> ok
  apply_discount(100, 100) = 0.0 -> ok
  apply_discount(100, 150) raised: percent must be 0-100, got 150 -> ok
  apply_discount(100, -5) raised: percent must be 0-100, got -5 -> ok
```

Note:

- Test code routinely catches `AssertionError`, or uses a framework such as `pytest` that does this automatically when its own `assert` statements fail inside test functions.
- The `assert` inside `apply_discount` is completely separate from the `assert` a test framework uses; only the framework's own assertions are part of the test-reporting machinery.

### **Example 11 — `pytest`-style assertions (how testing frameworks use `assert` differently)**

```python
# test_math_ops.py — a file that pytest would discover and run

def add(a, b):
    return a + b

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-2, -3) == -5

def test_add_mixed_numbers():
    assert add(-2, 3) == 1
```

Note:

- Inside `pytest`, a plain `assert` is the standard way to state an expectation. `pytest` rewrites these asserts internally so that a failure prints a detailed comparison, for example showing both sides of `add(2, 3) == 5` even though the message was never written by hand.
- This is a different usage pattern from application code: in tests, `assert` is not disabled by `-O` in practice because test runs are not typically launched with that flag, and the whole point of a test is to fail loudly when something is wrong.

## **Q&A**

**Q1. What is the syntax of the `assert` statement?**
`assert <expression>` or `assert <expression>, <message>`. If `<expression>` is falsy, Python raises `AssertionError`, using `<message>` as the description if one was provided.

**Q2. What exception does `assert` raise?**
`AssertionError`, which is a subclass of `Exception`. It can be caught the same way as any other exception, using `except AssertionError:`.

**Q3. Can `assert` be disabled? How?**
Yes. Running the interpreter with `python -O file.py` (or `python -OO file.py`) sets `__debug__` to `False` and removes all `assert` statements before execution. The code runs slightly faster, but every `assert` becomes a no-op.

**Q4. When should `assert` be used instead of `if`/`raise`?**
Use `assert` for *programmer-facing* checks: internal invariants, post-conditions, and assumptions about your own code. Use `if`/`raise` for *runtime checks* on data that is not fully under the programmer's control, such as user input, files, network responses, or database rows.

**Q5. Can `assert` be used in production code?**
It depends. `assert` is fine for internal sanity checks that should never realistically be reachable in production. It is not fine for any check that protects the program, the user, or money from bad data, because those checks must remain active even when `-O` is set.

**Q6. Why does `assert (x, "message")` never fail?**
Because that is a two-element tuple, and a non-empty tuple is always truthy in Python. The parentheses accidentally group the condition and the message into one object, instead of passing them as two separate arguments to `assert`. Always write `assert x, "message"` without wrapping both in parentheses.

**Q7. Does `assert` have any runtime cost?**
Yes, a small one, since Python has to evaluate the condition on every call. In most applications this cost is negligible compared to the value of catching bugs early. If an assertion is genuinely expensive to compute, for example checking that a huge list is sorted, that is a signal it may be better suited to a test suite than to a hot code path.

## **Quick Reference Summary**

### **Forms of `assert`**

| Form | Behavior |
|---|---|
| `assert <expr>` | Raise `AssertionError` if `<expr>` is falsy |
| `assert <expr>, <msg>` | Same, with `<msg>` shown in the exception description |
| `assert <expr>, <obj>` | `<obj>` is passed to `AssertionError`; it can be a string, dict, or any other object |
| `if __debug__: if not (<expr>): raise AssertionError(...)` | The expanded form Python actually runs internally |

### **When to Use vs Not Use**

| Use `assert` for | Use `if`/`raise` for |
|---|---|
| Internal invariants | User input validation |
| Post-conditions on your own functions | File, network, or database data |
| Programmer-facing sanity checks | Business rules that must always hold |
| Documenting assumptions in code | Permission and authentication checks |
| Test assertions (`pytest`, `unittest`) | Anything that must still run under `-O` |

### **Disabling**

| Command | What happens |
|---|---|
| `python file.py` | `assert` runs normally |
| `python -O file.py` | All `assert` statements are stripped; `__debug__` is `False` |
| `python -OO file.py` | Same as `-O`, plus docstrings are stripped |

## **Practice and Next Steps**

1. **Convert to `if`/`raise`.** Take any five `assert` statements from your own code and rewrite them as `if ...: raise ValueError(...)`. Compare the tracebacks side by side.
2. **Run with `-O`.** Take a small program that uses `assert` and run it both with and without `python -O`. Observe how the behavior changes.
3. **Build invariants.** Add `assert` statements to a class, for example `balance >= 0` for a wallet, `len(queue) >= 0` for a queue, or `head <= tail` for a sorted structure. Deliberately break the invariant from outside and watch the `assert` fire.
4. **Document assumptions.** Pick a twenty-line function that already exists. Write down the implicit assumptions it makes, such as "this list is non-empty" or "this dict has key 'id'". Add an `assert` for each one and notice how much clearer the function becomes.
5. **Catch `AssertionError`.** Write a small test harness, a `try`/`except AssertionError` loop, that runs a function against a list of test cases, including some that should fail the assertion.
6. **Write real `pytest` tests.** Create a file named `test_something.py` with a few functions starting with `test_`, using plain `assert` statements inside them, and run `pytest` to see how failures are reported.
7. **Read the `__debug__` docs.** Look up what `sys.flags.optimize` contains and what other constants Python exposes. Understanding how the `-O` flag works internally makes it easier to reason about what gets disabled.
