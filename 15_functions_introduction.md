# **Python Functions**

## **WHAT IS A FUNCTION, AND WHY DO WE USE IT**

A function is a named, reusable block of code that performs a specific task. You write the logic once, give it a name, and then call that name whenever you need that task done — instead of retyping the same lines everywhere.

```python
def calculate_area(length, width):
    return length * width

room1 = calculate_area(10, 12)
room2 = calculate_area(8, 9)
room3 = calculate_area(15, 20)
```

Without a function, you would repeat `length * width` in three different places, and if the formula ever needed to change, you would have to find and fix every copy.

**Why functions matter — the actual reasons we use them:**

- **Reusability.** Write the logic once, call it as many times as needed.
- **Readability.** `calculate_area(10, 12)` tells a reader what is happening far better than a raw expression buried in the middle of a script.
- **Maintainability.** If the formula for area changes, there is exactly one place to fix it.
- **Decomposition.** Large problems become manageable when broken into small, named steps — a big program becomes a set of small functions calling each other.
- **Testability.** A function with clear inputs and outputs can be tested in isolation, separately from the rest of the program.
- **Abstraction.** The caller of a function only needs to know what it does, not how it does it internally. `len(my_list)` is used constantly without anyone thinking about how it is implemented.

Every concept in the rest of this document — parameters, return values, scope, closures, decorators — exists to make this basic idea (name a block of code, reuse it) more powerful and more precise.

---

## **STAGE 1 — CORE MECHANICS**

### **1.1 `def`, Parameters, Return Values, and `None` Returns**

**The basic shape**

```python
def add(a, b):
    return a + b

result = add(2, 3)
print(result)        # 5
print(type(add))     # <class 'function'>
```

- `def` introduces a function. The name (`add`) is bound to a function object in the current scope.
- Parameters (`a`, `b`) are local names bound to the arguments passed at call time.
- `return` sends a value back to the caller. Without it, the function returns `None`.

**Multiple return values**

Python functions can return any object, including a tuple — this is the idiomatic way to return "multiple values":

```python
def min_max(values):
    return min(values), max(values)

lo, hi = min_max([3, 1, 4, 1, 5, 9, 2, 6])
print(lo, hi)   # 1 9
```

**`None` returns — three common cases**

```python
def f1():
    return          # explicit return with no value

def f2():
    pass             # return statement omitted entirely

def f3():
    x = 1 + 1        # expression statement, value discarded, no return at all

print(f1() is None)  # True
print(f2() is None)  # True
print(f3() is None)  # True
```

**Common mistake — printing vs returning.** `print(f())` prints `None` for a `None`-returning function, which often surprises beginners. Distinguish the return value from what the function prints:

```python
def greet(name):
    print(f"Hello, {name}!")   # side effect: prints to stdout
                                # implicit return value: None

x = greet("Ada")
print("x =", x)
# Hello, Ada!
# x = None
```

**Functions with no `return` at all — the "void function" pattern**

```python
def record(order_id, amount):
    print(f"recorded {order_id}")   # imagine a database write here

result = record(1, 99.0)
print(result is None)   # True
```

This is a procedure-style function, used for its side effect rather than its return value.

**Early return for guard clauses**

You can `return` from anywhere in a function body. This is the idiomatic way to handle guard clauses — bailing out early when preconditions fail:

```python
def withdraw(balance, amount):
    if amount <= 0:
        return "amount must be positive"
    if amount > balance:
        return "insufficient funds"
    balance -= amount
    return balance

print(withdraw(100, 20))   # 80
print(withdraw(100, 200))  # insufficient funds
```

Early returns are generally preferred over deeply nested `if/else`, since they keep the "happy path" at the top indentation level.

**A function is an object, and `def` is executable**

`def` runs at the moment Python reaches that line — it is not "declared" ahead of time the way it is in some other languages.

```python
if True:
    def shout(s):
        return s.upper()
else:
    def shout(s):
        return s.lower()

print(shout("hi"))   # HI
```

A `def` inside an `if` only creates the function object on the branch that actually runs. This same "evaluated once, when reached" behavior is exactly what causes the mutable default trap in section 1.3.

---

### **1.2 Positional vs Keyword Arguments**

```python
def describe(name, age, city):
    return f"{name} is {age}, lives in {city}"

print(describe("Ada", 36, "London"))                      # positional, matched by order
print(describe(age=36, city="London", name="Ada"))        # keyword, matched by name
print(describe("Ada", age=36, city="London"))              # mixed: positional first, then keyword
```

**The order rule.** Positional arguments must come before keyword arguments. The following is a `SyntaxError`:

```python
# describe(name="Ada", 36, "London")
# SyntaxError: positional argument follows keyword argument
```

**Calling with the wrong number of arguments**

```python
def f(a, b, c):
    return a, b, c

# f(1, 2)          -> TypeError: missing 1 required positional argument: 'c'
# f(1, 2, 3, 4)    -> TypeError: f() takes 3 positional arguments but 4 were given
f(1, b=2, c=3)     # valid
f(1, 2, c=3)       # valid
f(a=1, b=2, c=3)   # valid
```

**A function with many parameters**

```python
def create_user(name, email, age, role, active=True, newsletter=False):
    return {
        "name": name, "email": email, "age": age,
        "role": role, "active": active, "newsletter": newsletter,
    }

print(create_user("Ada", "ada@x.io", 36, "admin"))                       # all positional, easy to mix up
print(create_user("Ada", "ada@x.io", 36, role="admin", newsletter=True)) # mixed, easier to read
```

**Rule of thumb.** Use keyword arguments when the function has more than roughly two parameters (especially boolean flags), when the argument is conceptually a name or a label (`kind="primary"`, `timeout=30`), or when you want to skip later optional parameters. Use positional arguments when the order is obvious from context (`add(a, b)`, `point(x, y)`).

---

### **1.3 Default Arguments and the Mutable Default Trap**

Default values are evaluated once, when the `def` line runs — not on every call. This single fact explains both the basic behavior and the most famous pitfall in Python.

**Basic defaults**

```python
def greet(name, greeting="Hello", punctuation="!"):
    return f"{greeting}, {name}{punctuation}"

print(greet("Ada"))                       # Hello, Ada!
print(greet("Ada", "Hi"))                 # Hi, Ada!
print(greet("Ada", punctuation="."))      # Hello, Ada.
print(greet("Ada", "Hey", "?"))           # Hey, Ada?
```

**The mutable default trap**

```python
def add_to_list(item, target=[]):
    target.append(item)
    return target

print(add_to_list(1))   # [1]
print(add_to_list(2))   # [1, 2]   -- bug, expected [2]
print(add_to_list(3))   # [1, 2, 3]
```

What is happening:

1. When Python first sees the `def`, it evaluates `[]` and creates one specific list object.
2. That list object is stored on the function itself, in `f.__defaults__`.
3. Every call that omits `target` reuses that same list. `append` mutates it in place, so the changes persist across calls.

**The fix — use `None` as a sentinel**

```python
def add_to_list(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target

print(add_to_list(1))   # [1]
print(add_to_list(2))   # [2]   -- correct
print(add_to_list(3))   # [3]
```

`None` is immutable, so it cannot be mutated through the parameter. The function body creates a fresh list on every call.

**Seeing the trap directly**

You can inspect the default that Python stored on the function object:

```python
def f(items=[]):
    items.append("x")
    return items

print(f.__defaults__)     # ([],)             -- one list, defined once
f()
print(f.__defaults__)     # (['x'],)          -- same list, mutated
f()
print(f.__defaults__)     # (['x', 'x'],)     -- still the same list
```

**When a mutable default is not a bug**

Occasionally a shared, mutable default is exactly what you want — for example a memoization cache or a module-level registry:

```python
def register(name, _registry=[]):
    _registry.append(name)
    return _registry

print(register("ada"))   # ['ada']
print(register("alan"))  # ['ada', 'alan']    -- both calls intentionally share the same list
```

The convention is to prefix the parameter with an underscore to signal "intentionally shared, do not pass this in." Most linters (pylint, ruff) will still warn, so use this sparingly and document why.

**A real-world caching example**

```python
def fib(n, cache={}):
    if n in cache:
        return cache[n]
    if n < 2:
        result = n
    else:
        result = fib(n - 1) + fib(n - 2)
    cache[n] = result
    return result

print(fib(10))   # 55
```

A cleaner version still uses the sentinel pattern so the cache is created explicitly:

```python
def fib(n, cache=None):
    if cache is None:
        cache = {}
    # ... rest of the function
```

**Late-binding closures — a preview**

The same "evaluated once" rule shows up again in closures (Stage 4):

```python
funcs = [lambda i=i: i for i in range(3)]
print([f() for f in funcs])   # [0, 1, 2]   -- correct, because of the i=i default

funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])   # [2, 2, 2]   -- classic late-binding bug
```

This connects directly to the loop-variable-leak issue in section 2.6 below.

---

### **1.4 `*args` and `**kwargs`**

**`*args` — extra positional arguments as a tuple**

```python
def total(*args):
    return sum(args)

print(total(1, 2, 3))         # 6
print(total())                 # 0
print(total(10, 20, 30, 40))  # 100
```

`args` is just a tuple inside the function. The name `args` is a convention — the `*` is what matters, not the name.

**`**kwargs` — extra keyword arguments as a dict**

```python
def configure(**kwargs):
    for key, value in kwargs.items():
        print(f"  {key} = {value!r}")

configure(timeout=30, retries=3, debug=True)
#   timeout = 30
#   retries = 3
#   debug = True
```

**Combining them with regular parameters**

The fixed order is: positional, then `*args`, then keyword-only, then `**kwargs`.

```python
def make_profile(name, *tags, active=True, **extras):
    return {
        "name": name,
        "tags": tags,
        "active": active,
        "extras": extras,
    }

print(make_profile("Ada", "py", "ml", "rust", active=False, team="platform", level=3))
# {'name': 'Ada', 'tags': ('py', 'ml', 'rust'), 'active': False, 'extras': {'team': 'platform', 'level': 3}}
```

**A logger that accepts anything**

```python
def log(level, *messages, **fields):
    parts = [f"[{level}]", *messages]
    if fields:
        parts.append(" | " + " ".join(f"{k}={v}" for k, v in fields.items()))
    print(" ".join(parts))

log("INFO", "user signed in", user="ada", ip="10.0.0.1")
# [INFO] user signed in | user=ada ip=10.0.0.1
```

**Unpacking at the call site — the reverse direction**

`*` and `**` at the call site unpack an iterable or mapping into separate arguments:

```python
def add(a, b, c):
    return a + b + c

nums = [1, 2, 3]
print(add(*nums))          # 6, equivalent to add(1, 2, 3)

opts = {"b": 2, "c": 3}
print(add(1, **opts))      # 6, equivalent to add(1, b=2, c=3)
```

This is the foundation of how forwarding functions and decorators work.

**A forwarding wrapper**

```python
def debug_call(func, *args, **kwargs):
    print(f"calling {func.__name__}({args}, {kwargs})")
    result = func(*args, **kwargs)
    print(f"  -> {result!r}")
    return result

debug_call(pow, 2, 8)
# calling pow((2, 8), {})
#   -> 256
```

**Common mistake — parameter ordering.** The following are syntax errors:

```python
# def f(**kwargs, *args):       SyntaxError
# def f(*args, **kwargs, x):    SyntaxError
# def f(name=1, *args):         SyntaxError
```

The valid order is:

```python
def f(positional_only, /, positional_or_keyword, *args, keyword_only, **kwargs):
    pass
```

---

### **1.5 Positional-Only (`/`) and Keyword-Only (`*`) Parameter Markers**

PEP 570 (Python 3.8+) introduced two markers in the parameter list:

- `/` — everything to the left is positional-only.
- `*` — everything to the right is keyword-only.
- Parameters between `/` and `*` are positional-or-keyword, the default behavior.

**Keyword-only with `*`**

```python
def order(item, quantity, *, discount=0.0, gift_wrap=False):
    return {
        "item": item, "quantity": quantity,
        "discount": discount, "gift_wrap": gift_wrap,
    }

print(order("book", 2))
print(order("book", 2, discount=0.1))
print(order("book", 2, gift_wrap=True))

# order("book", 2, 0.1)      -- TypeError, discount is keyword-only
# order(item="book", 2)      -- SyntaxError, positional after keyword
```

`discount` and `gift_wrap` must be passed by name. This eliminates a class of bugs where a caller writes `order("book", 2, 0.1)` thinking `0.1` is a price.

**Positional-only with `/`**

```python
def divide(a, b, /):
    return a / b

print(divide(10, 2))     # 5.0

# divide(a=10, b=2)       -- TypeError, a is positional-only
```

Useful for functions whose parameter names are not part of the public API contract, for performance-sensitive C-backed functions, and to prevent callers from depending on internal parameter names.

**Combining all three sections**

```python
def fmt(
    text,                   # positional-or-keyword
    /,
    width,                  # positional-or-keyword
    *,
    align="left",           # keyword-only
    fill=" ",               # keyword-only
):
    return f"{text:{fill}{align[0]}{width}}"

print(fmt("hi", 10, align="right"))               # '        hi'
print(fmt("hi", 10, align="center", fill="*"))    # '****hi****'
print(fmt("hi", width=10, align="right"))         # '        hi'

# fmt(text="hi", 10)      -- SyntaxError, text is positional-only
# fmt("hi", 10, "right")  -- TypeError, align is keyword-only
```

**A real stdlib example**

```python
help(dict.update)   # note the (self, /, ...) -- self is positional-only
```

Many CPython builtins use `/` for `self` in methods, which is why you cannot write `dict.update(self=d)`.

**Reference table**

| Position in signature | Behavior |
| --- | --- |
| Before `/` | Positional-only, cannot pass by name |
| Between `/` and `*` | Positional-or-keyword, the default |
| After `*` (unnamed) | Keyword-only |
| `*args` | Captures extra positional arguments into a tuple |
| `**kwargs` | Captures extra keyword arguments into a dict |

A canonical example combining all five:

```python
def f(a, b, /, c, d, *args, e, f, **kwargs):
    pass
```

---

### **1.6 Docstrings and Type Hints**

**Docstrings**

A docstring is a string literal appearing as the first statement in a function body. It becomes the function's `__doc__`.

```python
def celsius_to_fahrenheit(c):
    """Convert a temperature from Celsius to Fahrenheit.

    Parameters
    ----------
    c : float
        Temperature in degrees Celsius.

    Returns
    -------
    float
        Temperature in degrees Fahrenheit.
    """
    return c * 9 / 5 + 32

print(celsius_to_fahrenheit(100))  # 212.0
```

Three conventions seen in real code: Google style (`Args:`, `Returns:`, `Raises:`), NumPy/SciPy style (`Parameters` / `Returns` sections with dashes), and reStructuredText/Sphinx style (`:param x:` directives). Pick one per project and stay consistent — tools like Sphinx and `mkdocstrings` render any of them, and `help()` displays whichever style you used.

Single-line docstrings (`"""Return x squared."""`) suit small, obvious functions. Multi-line docstrings — a summary line, a blank line, then detail — suit anything more involved (PEP 257).

**Type hints**

Type hints were standardized in PEP 484 (Python 3.5+). They are not enforced at runtime — they are metadata that tools like `mypy`, `pyright`, `ruff`, and IDEs read.

```python
def add(a: int, b: int) -> int:
    return a + b

print(add.__annotations__)
# {'a': int, 'b': int, 'return': int}
```

`__annotations__` is just a dict, populated at function-definition time. Python does not check that the actual arguments match the declared types.

**Common built-in type hints**

```python
from typing import Optional, Sequence, Union, Callable

def lookup(
    key: str,
    mapping: dict[str, int],
    default: Optional[int] = None,    # Optional[int] means Union[int, None]
) -> list[tuple[str, int]]:
    ...
```

Since Python 3.10, the `|` union syntax is preferred in new code:

```python
def parse(value: str | int) -> float | None:
    if isinstance(value, str):
        return float(value)
    if isinstance(value, int):
        return float(value)
    return None
```

**A note on `Optional` vs `= None`**

```python
def f(x: int = 0): ...              # "if missing, default to 0"
def g(x: Optional[int] = None): ... # "x can be an int or None; if missing, default to None"
def h(x: int = None): ...           # style mistake -- type says int, default is None; mypy flags this
```

A parameter with a default of `None` whose annotation is not `Optional[X]` (or `X | None`) is almost always a bug that a static type checker will catch.

**A fully hinted function, with a `Raises:` section**

```python
from typing import Sequence

def calculate_discount(
    prices: Sequence[float],
    discount_percent: float,
    apply_tax: bool = False,
) -> list[float]:
    """
    Calculate final prices after applying a discount and optional tax.

    Args:
        prices: A sequence of original prices.
        discount_percent: The discount to apply, from 0.0 to 1.0.
        apply_tax: Whether to add 8 percent tax after the discount.

    Returns:
        A list of final calculated prices.

    Raises:
        ValueError: If discount_percent is not between 0 and 1.
    """
    if not 0.0 <= discount_percent <= 1.0:
        raise ValueError("Discount must be between 0.0 and 1.0")
    tax_rate = 1.08 if apply_tax else 1.0
    return [p * (1 - discount_percent) * tax_rate for p in prices]
```

A `Raises:` section documents which exceptions callers should expect and handle — useful both for humans and for tools that generate API docs.

**When to use type hints.** Yes, for function signatures in any code that lives longer than a weekend, and for parameters in public or library APIs. Optional but useful for local variables where the type is not obvious. Usually skippable for throwaway scripts or notebook scratch cells.

---

### **1.7 Recursive Functions**

A recursive function is a function that calls itself in order to solve a problem by breaking it down into smaller versions of the same problem.

```python
def factorial(n):
    if n == 0:
        result = 1
    else:
        result = n * factorial(n - 1)
    return result

print("Factorial of 4 is:", factorial(4))   # 24
print("Factorial of 5 is:", factorial(5))   # 120
```

How this unwinds:

```
factorial(3) = 3 * factorial(2)
             = 3 * 2 * factorial(1)
             = 3 * 2 * 1 * factorial(0)
             = 3 * 2 * 1 * 1
             = 6
```

Every recursive function needs two parts:

- A **base case** — the condition that stops the recursion (`n == 0` above). Without one, the function calls itself forever until Python raises `RecursionError`.
- A **recursive case** — where the function calls itself with a smaller or simpler input, moving toward the base case.

**Why use recursion.** It can reduce the length of code and improve readability for problems that are naturally defined in terms of themselves — factorials, tree traversal, directory walking. It also makes some complex problems noticeably easier to express than an equivalent loop-based version.

**A second example — summing a list recursively**

```python
def sum_list(values):
    if not values:
        return 0
    return values[0] + sum_list(values[1:])

print(sum_list([1, 2, 3, 4, 5]))   # 15
```

Recursion trades some performance and stack space for clarity — each call adds a new frame to the call stack, so very deep recursion (thousands of levels) can raise `RecursionError`. For simple counting or summing tasks, a loop is usually more efficient; recursion earns its place on problems with a naturally recursive structure.

---

## **STAGE 2 — SCOPE AND NAME RESOLUTION**

Scope answers one question: when you write `x` inside a function, which `x` are you referring to? Python answers this with the **LEGB** rule.

### **2.1 Global and Local Variables**

Python supports two main categories of variables based on where they are declared.

**Global variables** are declared outside of any function, and can be accessed from any function in that module:

```python
a = 10   # global variable

def f1():
    print(a)

def f2():
    print(a)

f1()   # 10
f2()   # 10
```

**Local variables** are declared inside a function, and are only available inside that function — they cannot be accessed from outside it:

```python
def f1():
    a = 10
    print(a)   # valid

def f2():
    print(a)   # invalid, a does not exist here

f1()
f2()
# NameError: name 'a' is not defined
```

### **2.2 The LEGB Rule**

| Letter | Name | Where names live |
| --- | --- | --- |
| L | Local | Names bound anywhere in the current function |
| E | Enclosing | Names in any enclosing (outer) function, for nested functions |
| G | Global | Names defined at the top level of a module |
| B | Built-in | Names Python predefines, such as `len`, `print`, `range` |

Python searches these scopes in order and uses the first match. If nothing matches, it raises `NameError`.

**A complete LEGB trace**

```python
x = "global x"

def outer():
    x = "enclosing x"

    def inner():
        x = "local x"
        print(x)             # local x

    inner()
    print(x)                 # enclosing x

outer()
print(x)                     # global x
```

Now remove the local, and the lookup walks up to the next scope:

```python
x = "global x"

def outer():
    x = "enclosing x"

    def inner():
        print(x)        # no local x -- Python walks L -> E -> G -> B

    inner()              # enclosing x

outer()
```

**Common mistake — Python decides scope by static analysis, not by execution order.** This trips up nearly everyone at some point. Python decides whether a name is local by scanning the whole function body ahead of time — not by tracking what has actually executed so far.

```python
x = 10

def f():
    print(x)     # Python sees "x is assigned to" later in this function...
    x = 20       # ...so x is treated as LOCAL for the ENTIRE function

f()              # UnboundLocalError: local variable 'x' referenced before assignment
```

`print(x)` runs before `x = 20`, but Python has already decided `x` is local for the whole function, so `print(x)` tries to read an unassigned local variable. You can confirm this by disassembling the function:

```python
import dis

def f():
    print(x)
    x = 20

dis.dis(f)
# shows STORE_FAST for x, not LOAD_GLOBAL -- confirming Python decided x is local
```

**Inspecting scope from inside a function**

```python
def f(a, b):
    x = "local"
    print("locals:", locals())                       # {'a': ..., 'b': ..., 'x': 'local'}
    print("globals:", list(globals().keys())[:5])     # module-level names

f(1, 2)
```

`locals()` and `globals()` return dicts mapping name to value at the moment of the call. Modifying the dict returned by `locals()` does not affect the actual local variables — do not rely on that.

---

### **2.3 The `global` and `nonlocal` Keywords**

The `global` keyword serves two purposes: declaring a global variable inside a function, and making an existing global variable available to a function so it can be modified there.

**Reading a global vs shadowing it with a local of the same name**

```python
a = 10

def f1():
    a = 777          # this creates a NEW local variable, it does not touch the global a
    print(a)

def f2():
    print(a)          # reads the global a, unaffected by f1

f1()   # 777
f2()   # 10
```

**Using `global` to actually modify the module-level variable**

```python
a = 10

def f1():
    global a
    a = 777
    print(a)

def f2():
    print(a)

f1()   # 777
f2()   # 777, the global was genuinely changed
```

**If you try to read a variable that is only ever assigned as global inside a function, without running that function first, it does not exist yet:**

```python
def f1():
    a = 10
    print(a)

def f2():
    print(a)

f1()
f2()
# NameError: name 'a' is not defined
```

```python
def f1():
    global a
    a = 10
    print(a)

def f2():
    print(a)

f1()   # 10, this creates the global a
f2()   # 10, now it exists and can be read
```

**When a global and a local share the same name, you can still reach the global explicitly through `globals()`:**

```python
a = 10             # global variable

def f1():
    a = 777         # local variable, shadows the global inside this function
    print(a)                 # 777
    print(globals()['a'])    # 10, explicitly reaching the global dict

f1()
```

**`global` — bind to the module-level name, a second example**

```python
calls = 0

def track_call():
    global calls
    calls += 1
    print(f"call #{calls}")

track_call()   # call #1
track_call()   # call #2
print(calls)   # 2
```

Without `global`, `calls += 1` inside the function raises `UnboundLocalError`, for the same reason described in section 2.2.

**`nonlocal` — bind to an enclosing, non-global name**

`nonlocal` is the nested-function sibling of `global`. It tells Python: the name I want lives in some enclosing function's scope, not the module's global scope and not a new local.

```python
def make_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment

c = make_counter()
print(c(), c(), c())   # 1 2 3
```

`count` keeps its value between calls to `increment` because of the closure — `nonlocal` is what allows the inner function to modify, not just read, the enclosing variable.

**Common mistake — `nonlocal` requires an existing binding in an enclosing scope**

```python
def outer():
    def inner():
        nonlocal x     # SyntaxError: no binding for nonlocal 'x' found
        x = 1
    inner()

outer()
```

`nonlocal x` only works if `x` already exists in some enclosing function's scope — it is not a way to declare a brand new variable there.

**A function that remembers a value across calls**

```python
def make_accumulator(start=0):
    total = start

    def add(n):
        nonlocal total
        total += n
        return total

    return add

acc = make_accumulator()
print(acc(10))   # 10
print(acc(5))    # 15
print(acc(3))    # 18
```

This is the same pattern that makes decorators work later, in Stage 5.

**When to prefer each.** Use `global` for state that genuinely belongs to the whole module — a feature flag, a shared counter, a registry — sparingly, since global mutable state is hard to test. Use `nonlocal` when a nested function needs to update state that lives in its enclosing function — the closure pattern. Often the best alternative to both is wrapping the state in a class, or returning it as a value, which tends to be more testable.

---

### **2.4 Everything Is an Object, Including Functions**

In Python, everything is treated as an object — even a function is internally an object with an identity, a type, and attributes.

```python
def f1():
    print("Hello")

print(f1)        # <function f1 at 0x00419618>
print(id(f1))    # a unique integer identifying this object in memory
```

**Function aliasing.** Because a function is just an object, you can give it another name — this is called function aliasing.

```python
def wish(name):
    print("Good Morning:", name)

greeting = wish            # no parentheses -- this assigns the function object itself
print(id(wish))
print(id(greeting))        # same id as wish -- same object, two names

greeting("Durga")          # Good Morning: Durga
wish("Durga")               # Good Morning: Durga
```

Only one function object exists here; it can be called through either name. If the original name is deleted, the function is still reachable through the alias, since the alias holds a reference to the same object:

```python
def wish(name):
    print("Good Morning:", name)

greeting = wish
greeting("Durga")   # Good Morning: Durga
wish("Durga")        # Good Morning: Durga

del wish
# wish("Durga")      # NameError: name 'wish' is not defined
greeting("Pavan")     # Good Morning: Pavan -- still works, the object itself was never deleted
```

**Storing functions in data structures — dispatch tables**

```python
def add(a, b): return a + b
def sub(a, b): return a - b
def mul(a, b): return a * b
def div(a, b): return a / b

ops = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": div,
}

print(ops["+"](3, 4))   # 7
print(ops["*"](3, 4))   # 12
```

This pattern — keying functions by name in a dict — is the foundation of dispatch tables, HTTP routers, CLI argument parsers, and plugin systems.

**A list of strategies**

```python
import math

strategies = [
    ("linear",      lambda n: n),
    ("quadratic",   lambda n: n * n),
    ("logarithmic", lambda n: math.log2(max(n, 1))),
    ("factorial",   math.factorial),
]

for name, f in strategies:
    print(f"{name:11s} f(5) = {f(5)}")
```

**A function with attributes**

Because functions are objects, arbitrary attributes can be attached:

```python
def html_tag(name):
    """Wrap content in an HTML tag."""
    return f"<{name}>{name}</{name}>"

html_tag.purpose = "demo"
html_tag.version = 1

print(html_tag.purpose)   # demo
print(html_tag.version)   # 1
```

This pattern shows up in some testing frameworks (`pytest` uses it to mark tests) and in attribute-based dispatchers.

---

### **2.5 Nested Functions**

You can declare a function inside another function — this is called a nested function. A nested function is local to the function it is declared in, and cannot be called directly from outside it.

```python
def outer():
    print("outer function started")

    def inner():
        print("inner function execution")

    print("outer function calling inner function")
    inner()

outer()
# outer function started
# outer function calling inner function
# inner function execution

# inner()
# NameError: name 'inner' is not defined -- inner only exists inside outer's local scope
```

**A function can also return another function instead of calling it directly:**

```python
def outer():
    print("outer function started")

    def inner():
        print("inner function execution")

    print("outer function returning inner function")
    return inner

f1 = outer()
f1()
f1()
f1()
# outer function started
# outer function returning inner function
# inner function execution
# inner function execution
# inner function execution
```

Note the distinction between `f1 = outer` and `f1 = outer()`:

- `f1 = outer` — this is function aliasing (section 2.4). `f1` becomes another name for the `outer` function object itself, and `outer` has not been called yet.
- `f1 = outer()` — this calls `outer()`, which runs and returns the `inner` function object. `f1` is then a name for `inner`, not for `outer`.

This "return an inner function instead of calling it" pattern is the doorway into closures, covered in Stage 4 — the inner function remembers the environment it was created in even after `outer` has finished running.

---

### **2.6 Common Scope Mistake — the Loop Variable Leak**

In Python, `for` loop variables do not have their own scope. They leak into the enclosing function scope, and closures created inside the loop all end up sharing the same variable rather than capturing its value at each iteration.

```python
def create_multipliers():
    multipliers = []
    for i in range(3):
        multipliers.append(lambda x: x * i)
    return multipliers

mults = create_multipliers()
print(mults[0](10))  # 20, not 0
print(mults[1](10))  # 20, not 10
print(mults[2](10))  # 20
```

All three lambdas share the same enclosing `i`. By the time any of them runs, the loop has finished and `i` is `2` for all of them — this is the same late-binding behavior previewed in section 1.3.

**The fix — bind the current value as a default argument**, which is evaluated immediately when each lambda is created:

```python
def create_multipliers_fixed():
    multipliers = []
    for i in range(3):
        multipliers.append(lambda x, i=i: x * i)
    return multipliers

mults_fixed = create_multipliers_fixed()
print(mults_fixed[0](10))  # 0
print(mults_fixed[1](10))  # 10
print(mults_fixed[2](10))  # 20
```

This is a genuinely common bug whenever functions or callbacks are built inside a loop — registering handlers, building lists of tasks, wiring up UI callbacks. It will come up again with more depth in Stage 4.

---

### **2.7 Function Attributes and Introspection**

The `def` statement creates a function object with a number of built-in attributes worth knowing:

| Attribute | What it is | Example |
| --- | --- | --- |
| `__name__` | The function's name | `"greet"` |
| `__doc__` | The docstring | `"Return a greeting."` |
| `__module__` | The module it was defined in | `"__main__"` |
| `__qualname__` | Dotted name, matters inside classes | `"MyClass.method"` |
| `__defaults__` | Tuple of default-argument values | `(0,)` |
| `__kwdefaults__` | Dict of keyword-only defaults | `{"step": 1}` |
| `__code__` | The compiled code object | `code` |
| `__annotations__` | Dict of type hints | `{"x": int, "return": str}` |
| `__dict__` | Writable namespace for custom attributes | `{}` |
| `__closure__` | Closure cells, covered in Stage 4 | `None` or a tuple of cells |

**Exploring a function**

```python
def divide(a: float, b: float, *, precision: int = 2) -> float:
    """Divide a by b, rounded to `precision` decimal places."""
    return round(a / b, precision)

print(divide.__name__)                     # divide
print(divide.__annotations__)              # {'a': float, 'b': float, 'precision': int, 'return': float}
print(divide.__defaults__)                 # None, no positional defaults
print(divide.__kwdefaults__)               # {'precision': 2}
print(divide.__code__.co_argcount)          # 2, a and b are positional-or-keyword
print(divide.__code__.co_kwonlyargcount)    # 1, precision

divide.category = "math"                   # a custom attribute
print(divide.category)                      # math
```

**Where this matters in practice.** Decorators (Stage 5) read and write `__name__`, `__doc__`, and `__wrapped__`. Testing frameworks read custom attributes to mark tests. Web frameworks such as FastAPI use `__annotations__` to wire up routes from type hints. IDEs and linters use `__code__`, `__annotations__`, and signatures for autocomplete. `functools.wraps` (Stage 5) copies metadata from one function to another.

**A peek at the signature object**

```python
import inspect

def f(a: int, b: str = "x", *, c: bool = False) -> None: ...

sig = inspect.signature(f)
for name, param in sig.parameters.items():
    print(name, param.kind, param.default)
# a POSITIONAL_OR_KEYWORD <class 'inspect._empty'>
# b POSITIONAL_OR_KEYWORD x
# c KEYWORD_ONLY False
```

Parameter kinds are: `POSITIONAL_ONLY`, `POSITIONAL_OR_KEYWORD`, `VAR_POSITIONAL` (`*args`), `KEYWORD_ONLY`, `VAR_KEYWORD` (`**kwargs`).

---

## **CHEAT SHEET — STAGES 1 AND 2**

**Stage 1 essentials**

```python
def f(a, b=2, *args, c, **kwargs):
    """Docstring."""
    return a + b + sum(args) + c

f(1)                          # error, missing c
f(1, c=3)                     # ok
f(1, 2, 3, 4, c=5, d=6)       # ok, args=(3,4), kwargs={'d':6}

def add(item, target=None):    # avoid the mutable default trap
    if target is None:
        target = []
    target.append(item)
    return target

def api(x, /, y, *, z): ...    # x positional-only, z keyword-only

def total(values: list[int]) -> int: ...   # type hints

def factorial(n):               # recursion needs a base case + a recursive case
    if n == 0:
        return 1
    return n * factorial(n - 1)
```

**Stage 2 essentials**

```python
# LEGB: Local -> Enclosing -> Global -> Built-in
x = "G"
def outer():
    x = "E"
    def inner():
        x = "L"
        return x
    return inner

counter = 0
def tick():
    global counter
    counter += 1

def make_counter():
    n = 0
    def inc():
        nonlocal n
        n += 1
        return n
    return inc

f = some_function          # function aliasing
ops = {"+": add, "-": sub}  # dispatch table
triple = make_multiplier(3) # function factory
```

---

## **QUICK SELF-TEST**

1. Why do we use functions instead of just writing the same code repeatedly in a script?
2. Why does `def f(x, cart=[])` behave dangerously across multiple calls, and what is the fix?
3. What is the difference between `*args` and `**kwargs` in terms of what type each becomes inside the function?
4. Why does `count += 1` inside a function raise `UnboundLocalError` without `global` — and why does this happen even before the offending line executes?
5. What is the difference in outcome between mutating a list argument versus reassigning it inside a function?
6. What does `/` mean in a function signature? What does `*` mean?
7. Why do all the lambdas built inside a `for` loop end up using the same final value of the loop variable, and how do you fix it?
8. What are the two essential parts every recursive function must have?
9. What is the difference between `f1 = outer` and `f1 = outer()`?

If you can answer all nine confidently in your own words, Stage 1 and Stage 2 are solid, and you are ready for Stage 4 (closures) — which builds directly on sections 2.3, 2.4, and 2.6 above.