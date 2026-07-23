# **Python Return Types**

A Python function is a small machine: you hand it inputs (arguments), it does some work, and it hands you back an output (a return value). The return value is the *only* way the function talks back to its caller. Everything printed inside the function disappears the moment the function ends. This file covers what a function can return, when it returns `None`, how to return multiple values, the early-return pattern, and how to annotate return types.

## **What is a Return Value?**

The `return` statement ends the function and hands a value back to the caller. The value can be any Python object: a number, a string, a list, a dict, a custom object, a function, even `None`.

**Example 1 — basic return:**

```python
def square(x):
    return x * x

result = square(7)
print("result =", result)
print("type   =", type(result).__name__)
```

```
result = 49
type   = int
```

Note:

- `square(7)` evaluates to `49`. The variable `result` holds that value.
- A function that uses `return` behaves very differently from one that only uses `print`. See "Return vs Print" below.

## **The Six Things a Function Can Return**

| Return value | Example | What the caller gets |
|---|---|---|
| A single value | `return 42` | The number `42` |
| An expression | `return 2 * x + 1` | Whatever the expression evaluates to |
| Multiple values (as a tuple) | `return 1, 2, 3` | A tuple `(1, 2, 3)` |
| A collection (list, dict, set) | `return [1, 2, 3]` | The list itself |
| `None` (explicit) | `return None` | `None` |
| Nothing (no `return` statement) | (none) | Implicit `None` |

## **Return a Single Value**

```python
def full_name(first, last):
    return f"{first} {last}"

def age_in_days(years):
    return years * 365

print(full_name("Durga", "Prasad"))
print("age in days:", age_in_days(2))
```

```
Durga Prasad
age in days: 730
```

Note:

- Both functions return a single value. The caller can store it, print it, or pass it to another function.

## **Return Multiple Values (Tuple Packing)**

Python functions can return multiple values. The syntax `return a, b, c` packs them into a tuple, which the caller typically *unpacks* into multiple variables.

**Example 1 — packing and unpacking:**

```python
def min_max(numbers):
    return min(numbers), max(numbers)

low, high = min_max([3, 1, 4, 1, 5, 9, 2, 6])
print("low =", low, "high =", high)
print("type =", type(min_max([1, 2, 3])).__name__)
```

```
low = 1 high = 9
type = tuple
```

Note:

- `return min(numbers), max(numbers)` is shorthand for `return (min(numbers), max(numbers))`, a tuple literal.
- The caller writes `low, high = min_max(...)`, which is tuple unpacking.
- Internally the return value is a single tuple. "Multiple values" is just convenient syntax around one object.

**Example 2 — return more than two values:**

```python
def stats(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

lo, hi, avg = stats([10, 20, 30, 40])
print(f"low={lo}, high={hi}, average={avg}")
```

```
low=10, high=40, average=25.0
```

Note:

- This works for any number of return values. Three is common, four is fine, ten starts to be a code smell that usually means a dict or a small object would communicate better.

**Example 3 — return a dict instead of many values:**

```python
def stats_dict(numbers):
    return {
        "min": min(numbers),
        "max": max(numbers),
        "avg": sum(numbers) / len(numbers),
    }

result = stats_dict([10, 20, 30, 40])
print(result)
print("avg only:", result["avg"])
```

```
{'min': 10, 'max': 40, 'avg': 25.0}
avg only: 25.0
```

Note:

- With more than two or three return values, a dict is usually clearer. Each value is named, so the caller does not have to remember the order.

**Example 4 — return a `NamedTuple` (named fields, still a tuple)**

The standard library itself often returns lightweight named tuples instead of plain ones, for example `os.stat()` and `urllib.parse.urlparse()`. This gives named fields without the overhead of a full class.

```python
from typing import NamedTuple

class Stats(NamedTuple):
    minimum: float
    maximum: float
    average: float

def stats_named(numbers):
    return Stats(min(numbers), max(numbers), sum(numbers) / len(numbers))

result = stats_named([10, 20, 30, 40])
print(result)
print("average:", result.average)
low, high, avg = result  # still unpacks like a regular tuple
print(low, high, avg)
```

```
Stats(minimum=10, maximum=40, average=25.0)
average: 25.0
10 40 25.0
```

Note:

- `NamedTuple` gives the readability of named fields (`result.average`) while still behaving like a normal tuple for unpacking and indexing. It is a good middle ground between a plain tuple and a full dict or dataclass, and is cheaper to create than a dataclass for simple, immutable groups of values.

## **Return None**

`None` is Python's "no value" sentinel. A function returns `None` in two cases:

1. **Explicit:** the function says `return None`, or just `return` with nothing after it.
2. **Implicit:** the function has no `return` statement at all, or execution falls off the end of the function body.

**Example 1 — explicit `return None`:**

```python
def greet(name):
    if not name:
        return None
    print(f"Hello, {name}!")

result = greet("")
print("returned:", result)
```

```
returned: None
```

**Example 2 — implicit `None` (no `return`):**

```python
def greet(name):
    print(f"Hello, {name}!")

result = greet("Karan")
print("returned:", result)
```

```
Hello, Karan!
returned: None
```

Note:

- A function that only calls `print(...)` and has no `return` still returns a value. That value is `None`.
- This is the single most common surprise for beginners: "I called the function, why is `result` `None`?" The function never stated what to return.

**Example 3 — printing is not returning:**

```python
def square_wrong(x):
    print(x * x)        # just prints; caller gets None

def square_right(x):
    return x * x        # returns; caller can use the value

a = square_wrong(5)
b = square_right(5)
print("a =", a)
print("b =", b)
```

```
25
a = None
b = 25
```

Note:

- `square_wrong(5)` printed `25` to the console, but the caller received `None`.
- `square_right(5)` printed nothing on its own, but the caller received `25` and could use it in further code.

## **Return vs Print**

| `print` inside a function | `return` from a function |
|---|---|
| Writes to standard output | Hands a value to the caller |
| Disappears after the function returns | Can be stored, passed, used in expressions |
| For humans watching the program run | For other code to use |
| Side effect | Output |
| `print(x)` does not give the caller `x` | `return x` gives the caller `x` |

The rule: a function should `return` if its caller needs the value, and `print` only for human-facing messages. Many functions do both: print a status message, then return the actual result.

## **Early Return Pattern (Guard Clauses)**

A guard clause is an `if` at the top of a function that checks a precondition and returns early if it fails. The rest of the function then runs only on the happy path, without nested `if`s.

**Example 1 — without guard clauses (deeply nested):**

```python
def process(data):
    if data is not None:
        if isinstance(data, list):
            if len(data) > 0:
                total = sum(data)
                return total / len(data)
            else:
                return 0
        else:
            raise TypeError("data must be a list")
    else:
        return 0
```

**Example 2 — with guard clauses (flat, readable):**

```python
def process(data):
    if data is None:
        return 0
    if not isinstance(data, list):
        raise TypeError("data must be a list")
    if len(data) == 0:
        return 0
    return sum(data) / len(data)

print(process(None))
print(process([10, 20, 30]))
try:
    process("not a list")
except TypeError as e:
    print("raised:", e)
```

```
0
20.0
raised: data must be a list
```

Note:

- Each guard clause is one line. The happy path, `return sum(data) / len(data)`, is at the bottom and fully visible.
- This is the common modern Python style: validate inputs at the top, do the real work at the bottom.

**Example 3 — guard clauses in a real validation function**

```python
def register_user(username, password, age):
    if not username:
        return False, "username is required"
    if len(password) < 8:
        return False, "password must be at least 8 characters"
    if age < 13:
        return False, "must be at least 13 years old"
    return True, "ok"

for args in [("", "secret123", 20), ("karan", "abc", 20), ("karan", "secret123", 10), ("karan", "secret123", 20)]:
    ok, message = register_user(*args)
    print(f"register_user{args} -> ok={ok}, message={message!r}")
```

```
register_user('', 'secret123', 20) -> ok=False, message='username is required'
register_user('karan', 'abc', 20) -> ok=False, message='password must be at least 8 characters'
register_user('karan', 'secret123', 10) -> ok=False, message='must be at least 13 years old'
register_user('karan', 'secret123', 20) -> ok=True, message='ok'
```

Note:

- Returning a `(success, message)` tuple is a very common pattern for form and request validation, especially in code that does not want to raise exceptions for expected, recoverable failures.
- Each guard clause returns as soon as it finds a problem, so only one failure is reported at a time, in the order the checks were written.

## **Returning Functions (Closures and Decorators)**

A function can return another function. This is the basis of closures and decorators.

**Example 1 — returning a function:**

```python
def make_multiplier(n):
    def multiplier(x):
        return x * n
    return multiplier

times3 = make_multiplier(3)
times10 = make_multiplier(10)

print(times3(7))
print(times10(7))
print(type(times3).__name__)
```

```
21
70
function
```

Note:

- `make_multiplier(3)` returns a function, specifically the inner `multiplier` function.
- The returned function "remembers" the value of `n` from when it was created. That is a *closure*.

**Example 2 — decorator that returns a wrapped function:**

```python
import functools

def uppercase_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper()
    return wrapper

@uppercase_decorator
def greet(name):
    return f"hello, {name}"

print(greet("karan"))
print(greet.__name__)
```

```
HELLO, KARAN
greet
```

Note:

- A decorator is a function that takes a function and returns a (usually modified) function.
- The `@uppercase_decorator` syntax is shorthand for `greet = uppercase_decorator(greet)`.
- `functools.wraps(func)` copies over `__name__`, `__doc__`, and other metadata from the original function to `wrapper`. Without it, `greet.__name__` would print `"wrapper"` instead of `"greet"`, which makes debugging and introspection confusing in real codebases.

## **Returning Collections**

Functions commonly return lists, dicts, or sets. The collection itself is what is returned; the caller can iterate it, index it, or modify it.

**Example 1 — return a list:**

```python
def evens_up_to(n):
    return [i for i in range(n) if i % 2 == 0]

print(evens_up_to(10))
```

```
[0, 2, 4, 6, 8]
```

**Example 2 — return a dict:**

```python
def word_lengths(words):
    return {w: len(w) for w in words}

print(word_lengths(["Durga", "Karan", "Om"]))
```

```
{'Durga': 5, 'Karan': 5, 'Om': 2}
```

**Example 3 — return a generator (lazy collection):**

```python
def evens_up_to_gen(n):
    for i in range(n):
        if i % 2 == 0:
            yield i

g = evens_up_to_gen(10)
print("type:", type(g).__name__)
print("list:", list(g))
```

```
type: generator
list: [0, 2, 4, 6, 8]
```

Note:

- `yield` turns a function into a *generator function*. Calling it returns a generator object immediately, without running any of the function body yet.
- Values are produced on demand, one at a time, as the caller iterates. For large datasets this saves memory, since the whole collection never has to exist in memory at once.

**Example 4 — measuring the memory difference between a list and a generator**

```python
import sys

def squares_list(n):
    return [i * i for i in range(n)]

def squares_gen(n):
    return (i * i for i in range(n))

n = 1_000_000
lst = squares_list(n)
gen = squares_gen(n)

print("list size in bytes:     ", sys.getsizeof(lst))
print("generator size in bytes:", sys.getsizeof(gen))
```

```
list size in bytes:      8448728
generator size in bytes: 200
```

Note:

- The list holds all one million values in memory at once. The generator holds only the small amount of state needed to produce the next value.
- This is why data-processing code that reads large files or database result sets often returns a generator instead of a fully built list.

## **Type Hints for Return Types**

Python 3.5+ supports type hints. They do not change runtime behavior, but they tell readers, and tools like `mypy`, `pyright`, and IDEs, what the function is supposed to return.

**Example 1 — basic type hints:**

```python
def square(x: int) -> int:
    return x * x

print(square(5))
```

```
25
```

Note:

- `x: int` says the parameter should be an `int`.
- `-> int` says the function returns an `int`.

**Example 2 — `-> None` for a function that does not return a value:**

```python
def log(message: str) -> None:
    print(f"[LOG] {message}")

log("server started")
print("returned:", log("still running"))
```

```
[LOG] server started
[LOG] still running
returned: None
```

Note:

- `-> None` is the standard way to say "this function does its work as a side effect, and does not produce a value the caller should use".

**Example 3 — multiple return types with `Union` or the `|` syntax:**

```python
from typing import Union

def find_user(user_id: int) -> Union[dict, None]:
    users = {1: {"name": "Durga"}, 2: {"name": "Karan"}}
    return users.get(user_id)    # dict if found, None if not

print(find_user(1))
print(find_user(99))
```

```
{'name': 'Durga'}
None
```

Note:

- `Union[dict, None]` says the function returns either a `dict` or `None`.
- Since Python 3.10, `dict | None` can be written directly instead of `Union[dict, None]`.

**Example 4 — `Optional[T]` is shorthand for `Union[T, None]`:**

```python
from typing import Optional

def find_user(user_id: int) -> Optional[dict]:
    users = {1: {"name": "Durga"}}
    return users.get(user_id)

print(find_user(1))
print(find_user(99))
```

```
{'name': 'Durga'}
None
```

Note:

- `Optional[dict]` means exactly `Union[dict, None]`. The `Optional` form is generally preferred when the `None` case is the expected, common outcome, such as a lookup that might not find anything.

**Example 5 — collection return types:**

```python
def squares(n: int) -> list[int]:
    return [i * i for i in range(n)]

def word_lengths(words: list[str]) -> dict[str, int]:
    return {w: len(w) for w in words}

def split_name(full: str) -> tuple[str, str]:
    first, last = full.split(" ", 1)
    return first, last

print(squares(5))
print(word_lengths(["Durga", "Om"]))
print(split_name("Karan Singh"))
```

```
[0, 1, 4, 9, 16]
{'Durga': 5, 'Om': 2}
('Karan', 'Singh')
```

Note:

- Since Python 3.9 (PEP 585), the built-in types can be used directly as generics: `list[int]`, `dict[str, int]`, `tuple[str, str]`.
- The older forms `typing.List`, `typing.Dict`, and `typing.Tuple` still work but have been deprecated since Python 3.9 in favor of the built-ins above. They are still needed only when supporting Python versions older than 3.9.

## **Mutating vs Returning (a Common Gotcha)**

A function can either return a new value or mutate an existing object in place. Mixing the two is a frequent source of bugs.

**Example 1 — mutate and return the same object (usually a bad idea):**

```python
def add_item_wrong(items, new_item):
    items.append(new_item)        # mutates the caller's list
    return items

cart = ["apple", "banana"]
result = add_item_wrong(cart, "cherry")
print("cart:  ", cart)
print("result:", result)
print("same object?", cart is result)
```

```
cart:   ['apple', 'banana', 'cherry']
result: ['apple', 'banana', 'cherry']
same object? True
```

Note:

- `add_item_wrong` mutates `cart` and returns it. The caller now has two names pointing at the same list, which can be surprising if the caller expected `cart` to stay unchanged.

**Example 2 — return a new list (the right way):**

```python
def add_item_right(items, new_item):
    return items + [new_item]      # creates a new list

cart = ["apple", "banana"]
result = add_item_right(cart, "cherry")
print("cart:  ", cart)
print("result:", result)
print("same object?", cart is result)
```

```
cart:   ['apple', 'banana']
result: ['apple', 'banana', 'cherry']
same object? False
```

Note:

- `add_item_right` returns a new list, leaving the original untouched. The caller decides what to do with the new list.

The general rule: a function should either mutate or return, not both. If it returns a new object, it should not also mutate the inputs. If it mutates inputs in place, it should return `None` to signal "there is no new value to use; look at the object you already had."

## **Another Common Gotcha: Forgetting to `return` in Recursion**

A very common bug in recursive functions is calling the recursive step without returning its result, which silently discards the computed value.

```python
def factorial_wrong(n):
    if n <= 1:
        return 1
    factorial_wrong(n - 1) * n   # BUG: result is computed and thrown away

def factorial_right(n):
    if n <= 1:
        return 1
    return factorial_right(n - 1) * n   # result is returned up the call chain

print("wrong:", factorial_wrong(5))
print("right:", factorial_right(5))
```

```
wrong: None
right: 120
```

Note:

- `factorial_wrong` computes `factorial_wrong(n - 1) * n` correctly at every step, but without a `return`, that value is discarded and the function falls off the end, returning `None`.
- This bug is easy to miss because the recursive calls do happen and do compute the right numbers internally; only the final value never makes it back to the original caller.

## **Examples**

### **Example 1 — return a primitive**

```python
def celsius_to_fahrenheit(c):
    return c * 9 / 5 + 32

print(celsius_to_fahrenheit(100))
```

```
212.0
```

### **Example 2 — return a string**

```python
def shout(msg):
    return msg.upper() + "!"

print(shout("hello"))
```

```
HELLO!
```

### **Example 3 — return a tuple (multiple values)**

```python
def divmod_safe(a, b):
    if b == 0:
        return None
    return a // b, a % b

print(divmod_safe(17, 5))
print(divmod_safe(17, 0))
```

```
(3, 2)
None
```

Note:

- Returning `None` for the error case is one option. Raising an exception, such as `ZeroDivisionError` or a custom `ValueError`, is usually preferred for genuinely exceptional conditions, since a caller that forgets to check for `None` will get a confusing `TypeError` later instead of a clear error at the source.

### **Example 4 — return a list**

```python
def first_n_evens(n):
    return [i for i in range(n * 2) if i % 2 == 0][:n]

print(first_n_evens(5))
```

```
[0, 2, 4, 6, 8]
```

### **Example 5 — return a dict**

```python
def parse_header(line):
    key, value = line.split(":", 1)
    return {key.strip(): value.strip()}

print(parse_header("  Host : example.com  "))
```

```
{'Host': 'example.com'}
```

### **Example 6 — return `None` explicitly vs implicitly**

```python
def explicit_none():
    return None

def implicit_none():
    pass    # falls off the end of the function

print("explicit:", explicit_none())
print("implicit:", implicit_none())
```

```
explicit: None
implicit: None
```

### **Example 7 — early return for guard clauses**

```python
def get_grade(score):
    if score < 0 or score > 100:
        return None
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"

print(get_grade(85))
print(get_grade(150))
print(get_grade(40))
```

```
B
None
F
```

Note:

- Each guard clause is short. The "no grade" case is handled at the top, before the actual grading logic runs.

### **Example 8 — return a generator**

```python
def fib_gen(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fib_gen(7):
    print(num, end=" ")
print()
```

```
0 1 1 2 3 5 8
```

### **Example 9 — return a function (closure)**

```python
def make_adder(n):
    def adder(x):
        return x + n
    return adder

add5 = make_adder(5)
add10 = make_adder(10)
print(add5(100))
print(add10(100))
```

```
105
110
```

### **Example 10 — type hints for collections**

```python
def group_by_length(words: list[str]) -> dict[int, list[str]]:
    result: dict[int, list[str]] = {}
    for w in words:
        result.setdefault(len(w), []).append(w)
    return result

print(group_by_length(["Durga", "Karan", "Om", "Ram", "Sita"]))
```

```
{5: ['Durga', 'Karan'], 2: ['Om'], 3: ['Ram'], 4: ['Sita']}
```

Note:

- `-> dict[int, list[str]]` says the function returns a dict whose keys are ints (word lengths) and whose values are lists of strings (the words with that length).
- Each word length gets its own group: `"Ram"` has 3 letters, so it lands in its own `3: [...]` entry rather than being merged with a different length.

### **Example 11 — return a dataclass instead of a tuple**

```python
from dataclasses import dataclass

@dataclass
class Stats:
    minimum: float
    maximum: float
    average: float

def compute_stats(numbers: list[float]) -> Stats:
    return Stats(
        minimum=min(numbers),
        maximum=max(numbers),
        average=sum(numbers) / len(numbers),
    )

result = compute_stats([10, 20, 30, 40])
print(result)
print("average:", result.average)
```

```
Stats(minimum=10, maximum=40, average=25.0)
average: 25.0
```

Note:

- A `@dataclass` is a good fit when a function returns several related values that will be passed around together elsewhere in the program, not just unpacked once at the call site.
- Compared to a `NamedTuple`, a dataclass is mutable by default (fields can be reassigned after creation) and reads slightly more like a regular class; a `NamedTuple` is immutable and behaves like a tuple for unpacking. Choose based on whether the returned value should ever change after creation.

### **Example 12 — real pattern: parsing and validating rows from a data file**

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class ParsedRow:
    name: str
    score: float

def parse_row(raw_row: str) -> Optional[ParsedRow]:
    parts = raw_row.split(",")
    if len(parts) != 2:
        return None
    name, score_text = parts[0].strip(), parts[1].strip()
    if not name or not score_text.replace(".", "", 1).isdigit():
        return None
    return ParsedRow(name=name, score=float(score_text))

raw_lines = ["Priya, 88.5", "Aman, ninety", "Om", "Sita, 91"]

for line in raw_lines:
    parsed = parse_row(line)
    if parsed is None:
        print(f"skipped invalid row: {line!r}")
    else:
        print(f"parsed: {parsed}")
```

```
parsed: ParsedRow(name='Priya', score=88.5)
skipped invalid row: 'Aman, ninety'
skipped invalid row: 'Om'
parsed: ParsedRow(name='Sita', score=91.0)
```

Note:

- `parse_row` returns `Optional[ParsedRow]`: either a valid, well-typed object or `None` for a row that could not be parsed.
- The caller is forced to handle both cases explicitly by checking `if parsed is None`, which is the whole point of using `Optional` in the return type: it documents, right in the signature, that failure is a normal, expected outcome the caller must deal with.

## **Q&A**

**Q1. What is the default return value of a function that has no `return`?**
`None`. A function that does not explicitly return anything, or that runs off the end of its body, returns `None` automatically.

**Q2. How can multiple values be returned from a function?**
Pack them into a tuple: `return a, b, c`. The caller typically writes `x, y, z = func()`. For more than two or three values, prefer returning a dict, a `NamedTuple`, or a `@dataclass` so the values are named instead of positional.

**Q3. What is the difference between `return` and `print`?**
`print` writes to standard output, for humans watching the program run. `return` hands a value to the caller, for code to use. Most functions should return their result; `print` is reserved for human-facing status messages and side effects.

**Q4. Should `Optional[T]` or `Union[T, None]` be used?**
They mean exactly the same thing. `Optional[T]` is preferred when the `None` case is expected and normal, such as a lookup function. `Union[T, None]`, or the `T | None` syntax on Python 3.10+, is fine everywhere else.

**Q5. Should a function mutate its inputs or return a new value?**
Pick one and stick to it. If a function returns a new value, it should not also mutate the inputs. If it mutates inputs in place, it should return `None` to signal "there is no new value; the change already happened to the object you passed in." Mixing the two is a common source of bugs.

**Q6. Why did my recursive function return `None` even though the numbers looked right while debugging?**
The recursive call's result was probably computed but never returned with an explicit `return` statement. Python does not automatically propagate the value of the last expression in a function; every path that should hand back a value needs its own `return`.

## **Quick Reference Summary**

### **Forms of `return`**

| Form | What it does |
|---|---|
| `return <expr>` | Return the value of `<expr>` |
| `return` | Return `None` |
| `return a, b, c` | Pack into a tuple, return `(a, b, c)` |
| (no return) | Return `None` (implicit) |

### **What a Function Can Return**

| Return type | Example | Caller sees |
|---|---|---|
| `int` / `float` / `str` / `bool` | `return 42` | The value |
| `None` | `return None` | `None` |
| Tuple | `return 1, 2, 3` | `(1, 2, 3)` |
| List | `return [1, 2, 3]` | The list itself |
| Dict | `return {"k": "v"}` | The dict itself |
| `NamedTuple` | `return Stats(1, 2, 3)` | An object that unpacks like a tuple, with named fields |
| Dataclass | `return Stats(...)` | An instance with named, mutable fields |
| Generator | `yield x` (function becomes a generator) | A generator object |
| Function | `return inner_func` | The inner function |
| Custom object | `return MyClass()` | An instance |

### **`return` vs `print`**

| `print(x)` | `return x` |
|---|---|
| Writes to `sys.stdout` | Hands a value to the caller |
| Disappears after the function returns | Can be stored, passed, used |
| For humans | For code |
| `result = print("hi")` gives `result is None` | `result = func_that_returns()` gives the value |

### **Type Hint Cheat Sheet**

| Hint | Means |
|---|---|
| `-> int` | Returns an int |
| `-> str` | Returns a string |
| `-> None` | Returns nothing (the function does side effects) |
| `-> list[int]` | Returns a list of ints (Python 3.9+) |
| `-> dict[str, int]` | Returns a dict of str to int |
| `-> tuple[int, str]` | Returns a 2-tuple of `(int, str)` |
| `-> Optional[dict]` | Returns a dict or `None` |
| `` -> list[str] \| None `` | Same as `Optional[list[str]]` (Python 3.10+) |
| `-> Callable[[int], int]` | Returns a function that takes an int and returns an int |

## **Practice and Next Steps**

1. **Convert `print` to `return`.** Take a function that uses `print` to "return" a value and rewrite it to actually `return` the value. Update the caller to use the returned value.
2. **Write a guard-clause version.** Take a function that uses nested `if`/`else` to validate inputs and rewrite it using guard clauses. Compare the readability.
3. **Return a dict instead of multiple values.** Take a function that returns four or more values and refactor it to return a dict, a `NamedTuple`, or a `@dataclass`. Notice how much clearer the caller becomes.
4. **Type-hint a real module.** Pick a hundred-line script and add `-> ReturnType` to every function. Use `Optional[T]` for functions that may return `None`. Run `mypy` on it and fix the issues it finds.
5. **Build a closure.** Write a function `make_power(n)` that returns a function computing `x ** n`. Verify that `square = make_power(2)` and `cube = make_power(3)` work as expected.
6. **Generator vs list.** Take a function that returns a list, change it to `yield` instead, and verify the caller can still iterate it. Compare `sys.getsizeof()` for both versions on a large input.
7. **Test the mutation gotcha.** Write a function that mutates a list. Show that the caller's list also changes. Then write a version that returns a new list and show the difference.
8. **Convert to a dataclass.** Take a function that returns three or more related values and convert it to return a `@dataclass` instead. Notice how the call site becomes self-documenting.
9. **Find the missing `return`.** Write a small recursive function on purpose without returning the recursive call's result, run it, and confirm it silently returns `None`. Then fix it and compare.
