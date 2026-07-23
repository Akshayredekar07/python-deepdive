# **Python Decorators**

## **Functions Are Objects First**

Decorators only make sense once one fact is fully absorbed: in Python, a function is just another object, like an int, a string, or a list. It can be printed, assigned to a variable, passed around, stored in a data structure, and returned from another function. Decorators are built entirely out of these ordinary object behaviors; there is no special magic beyond them.

**A function has an identity, just like any other object:**

```python
def f1():
    print("Durga")

print(f1)
print(id(f1))
```

```
<function f1 at 0x000002365EB240E0>
2432540229856
```

Note:

- `f1` by itself, without `()`, refers to the function object. `f1()` calls it.
- `id(f1)` shows the function's memory address, exactly like `id()` would for any other object.

**A function can be assigned another name (function aliasing):**

```python
def wish(name):
    p = print
    p("good morning ", name)

greeting = wish
wish("durga")
greeting("durga")
del wish
greeting("sunny")
```

```
good morning  durga
good morning  durga
good morning  sunny
```

Note:

- `p = print` assigns the built-in `print` function to a new name, `p`. This is the same mechanism as `greeting = wish`.
- `greeting = wish` does not copy the function; both names point at the same function object.
- `del wish` only removes the name `wish` from the current scope. The function object itself keeps existing, because `greeting` still refers to it, so `greeting("sunny")` still works after `wish` is gone.

**Functions can be nested, and an outer function can return an inner one:**

```python
def outer():
    print("Outer function started")
    def inner():
        print("Inner function executed")
    print("Outer function about to return inner")
    return inner

newf = outer()   # newf now refers to inner
print(newf)
```

```
Outer function started
Outer function about to return inner
<function outer.<locals>.inner at 0x000002365EB24160>
```

```python
newf()
newf()
newf()
newf()
```

```
Inner function executed
Inner function executed
Inner function executed
Inner function executed
```

Note:

- Calling `outer()` runs the body of `outer` once, prints its two messages, and returns the `inner` function object itself, not the result of calling it.
- `newf` now refers to `inner`. Calling `newf()` any number of times calls `inner`, completely independently of `outer`.
- `inner.<locals>` in the repr shows that `inner` was defined inside `outer`'s local scope.

**Functions can be passed as arguments to other functions:**

```python
def f1(func):
    print(f"f1 function got {func} function as argument")
    func()

def fx():
    print('fx function')

def fy():
    print('fy function')

f1(fx)
f1(fy)
```

```
f1 function got <function fx at 0x00000265ED1ED440> function as argument
fx function
f1 function got <function fy at 0x00000265ED1EC860> function as argument
fy function
```

Note:

- `fx` and `fy` are passed into `f1` without calling them, so `f1` receives the function *objects* themselves and decides when to call them with `func()`.
- A function can also return multiple values, packed as a tuple, for example `return 10, 20, 30` returns `(10, 20, 30)`. That is covered fully in the return-types note; it is mentioned here only as one more example of a function producing an ordinary object that can be passed around.

**Summary of what makes decorators possible:**

- In Python, everything is treated as an object, including functions.
- Every function can be considered an object, with its own identity and address.
- A different name can be assigned to an existing function; this is function aliasing.
- A function can be defined inside another function; this is a nested function.
- A function can return another function.
- A function can be passed as an argument to another function.

## **What Is a Decorator**

A decorator is a function which can take a function as an argument, extend its functionality, and return the modified function with that extended functionality.

- The main objective of a decorator is to extend the functionality of an existing function without modifying that function's own code.
- A decorator wraps the original function inside a new function, and that new function is what actually gets called from then on.
- The `@` symbol placed above a function definition is simply shorthand for passing that function into a decorator function.

More precisely, a decorator:

- Is a function.
- Always takes a function as its argument, often called the input function.
- Creates a new function with extended functionality.
- May use the original input function somewhere inside that new function.
- Returns the extended function as its output.
- Extends the original function's behavior from the outside, without ever touching the original function's own code.

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

Whenever `wish()` is called, the `decor` function's `inner` runs in its place, since `@decor` already replaced `wish` with `inner` at definition time. The original `wish()` function was never edited; the new behavior was added entirely from the outside.

**A decorator does not have to call the original function at all:**

```python
def decor(func):
    def inner():
        print("Send person to beauty parlour")
        print("Showing a person with full decoration")
    return inner

@decor
def display():
    print("Showing a person as it")

display()
```

```
Send person to beauty parlour
Showing a person with full decoration
```

Note:

- `func` (the original `display`) is never called inside `inner` here, so "Showing a person as it" never prints. This is legal: a decorator can replace a function's behavior entirely instead of extending it, though the far more common pattern is to call `func(...)` somewhere inside the wrapper, so the original behavior still runs alongside the new behavior.

**Special-casing certain inputs is a common, simple use of a decorator:**

```python
def beautified(fun):
    def inner(name):
        names = ['CM', 'PM', 'prajakta']
        if name in names:
            print(f"Very very good morning! {name}")
        else:
            fun(name)
    return inner

@beautified
def wish(name):
    print('Good morning:', name)

wish('Durga')
wish('prajakta')
```

```
Good morning: Durga
Very very good morning! prajakta
```

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

wish("Durga")             # decorator not applied
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

`wish` was never reassigned here, so calling `wish(...)` directly still runs the plain, undecorated version. `decorfunction`, on the other hand, points at `inner`, the wrapped version. This is the same distinction as choosing whether or not to write `@decor` above the function definition.

**The same manual-assignment pattern, in a more production-flavored example:**

```python
import time

def logger(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling '{func.__name__}' with arguments: {args}, {kwargs}")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"[LOG] '{func.__name__}' execution time: {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def process_order(order_id, customer_name):
    print(f"Processing order {order_id} for customer {customer_name}...")

logged_process_order = logger(process_order)

process_order(101, "jaybabu")             # original, no logging
logged_process_order(102, "sandhya")      # decorated, with logging
```

```
Processing order 101 for customer jaybabu...
[LOG] Calling 'process_order' with arguments: (102, 'sandhya'), {}
Processing order 102 for customer sandhya...
[LOG] 'process_order' execution time: 0.0000 seconds
```

Note:

- `process_order` and `logged_process_order` are two separate names pointing at two different function objects: the plain function and the wrapped one. Both can be called, and each behaves according to whether it was passed through `logger` or not.

## **Refresher: `*args` and `**kwargs`**

Before generalizing a decorator to any function signature, it helps to see plainly what `*args` and `**kwargs` do on their own, outside of any decorator.

```python
def example_function(a, b, *args, **kwargs):
    print(f"a: {a}, b: {b}")
    print(f"args: {args}")
    print(f"kwargs: {kwargs}")

example_function(1, 2, 3, 4, name="Rahul", city="Mumbai")
```

```
a: 1, b: 2
args: (3, 4)
kwargs: {'name': 'Rahul', 'city': 'Mumbai'}
```

Note:

- `a` and `b` capture the first two positional arguments by name.
- `*args` collects any further positional arguments into a tuple.
- `**kwargs` collects any keyword arguments into a dict.
- This exact idea is what lets a decorator's inner function accept and forward arguments for a function it knows nothing about in advance.

## **Handling Any Function Signature — `*args` and `**kwargs`**

The examples so far only work for functions that take exactly one argument, `name`. A decorator meant to be reused across many different functions needs to accept and forward any number of positional and keyword arguments.

**A decorator tied to a fixed, two-argument signature:**

```python
def decorator_fun(func_param):
    def inside(x, y):
        print(40 * '*')
        print(f"Sum of {x} and {y} is:")
        func_param(x, y)
        print(40 * '*')
    return inside

@decorator_fun
def add(a, b):
    print(a + b)

add(10, 20)
```

```
****************************************
Sum of 10 and 20 is:
30
****************************************
```

Note:

- `inside(x, y)` only works because `add` also happens to take exactly two positional arguments. Decorating any function with a different number of arguments, such as `add(a, b, c)`, would raise a `TypeError` about the wrong number of positional arguments.

**A decorator that intercepts a specific failure case, still tied to two arguments:**

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

**Generalizing with `*args, **kwargs` so the same decorator works on any function:**

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

Decorating a function quietly replaces its identity. Tools that inspect a function, such as `help()`, debuggers, and automatic API documentation generators, start seeing the wrapper instead of the real function.

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

A decorator like `@logged` above takes no configuration of its own. Many real decorators need configuration, such as `@retry(max_attempts=3)`, `@app.get("/students")`, or `@lru_cache(maxsize=128)`, which requires one additional layer of nesting.

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

A decorator does not have to be a function. Any callable, including a class whose instances define `__call__`, can serve as a decorator.

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

`@CountCalls` runs `process_order = CountCalls(process_order)`. `process_order` is now an instance of `CountCalls` rather than a plain function, but since the class defines `__call__`, calling `process_order(...)` still works exactly like calling a function, while also giving a natural place, `self`, to hold state such as `self.calls`.

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

## **Real-World Style Examples**

These are hand-written decorators in the same spirit as `RequiresRole` above: small, self-contained, and typical of the kind of checks that show up in real backend code before reaching for a framework's built-in decorators.

**Example — an authentication check:**

```python
def authenticate(func):
    def wrapper(user, *args, **kwargs):
        if not user.get("is_authenticated", False):
            print("[ERROR] User is not authenticated. Access denied.")
            return None
        print(f"[INFO] User '{user['name']}' is authenticated. Proceeding...")
        return func(user, *args, **kwargs)
    return wrapper

def fetch_user_data(user, data_type):
    print(f"Fetching {data_type} for user {user['name']}...")

secure_fetch_user_data = authenticate(fetch_user_data)

authenticated_user = {"name": "Rohit", "is_authenticated": True}
unauthenticated_user = {"name": "Priya", "is_authenticated": False}

secure_fetch_user_data(authenticated_user, "order history")
secure_fetch_user_data(unauthenticated_user, "order history")
```

```
[INFO] User 'Rohit' is authenticated. Proceeding...
Fetching order history for user Rohit...
[ERROR] User is not authenticated. Access denied.
```

Note:

- The plain `fetch_user_data(user, data_type)` function has no idea an authentication check exists; the check was added entirely from the outside, by wrapping it.
- `secure_fetch_user_data` is the safe version to expose to callers; the original `fetch_user_data` still exists and still has no protection, so it matters which name the rest of the codebase actually calls.

**Example — enforcing a business rule (a loan limit check):**

```python
def validate_loan(func):
    def wrapper(customer, loan_amount, *args, **kwargs):
        if loan_amount > customer.get("max_loan_limit", 0):
            print(f"[ERROR] Loan amount of {loan_amount} exceeds the limit for {customer['name']}.")
            return None
        print(f"[INFO] Loan of {loan_amount} for {customer['name']} is within the permissible limit.")
        return func(customer, loan_amount, *args, **kwargs)
    return wrapper

def process_loan(customer, loan_amount):
    print(f"Processing loan of {loan_amount} for customer {customer['name']}...")

validated_process_loan = validate_loan(process_loan)

customer_rahul = {"name": "Rahul", "max_loan_limit": 500000}
customer_ananya = {"name": "Ananya", "max_loan_limit": 300000}

validated_process_loan(customer_rahul, 600000)
validated_process_loan(customer_ananya, 250000)
```

```
[ERROR] Loan amount of 600000 exceeds the limit for Rahul.
[INFO] Loan of 250000 for Ananya is within the permissible limit.
Processing loan of 250000 for customer Ananya...
```

Note:

- This is the same shape as `authenticate`: check a precondition first, print or return early if it fails, otherwise call the original function and let it do its job.
- Both `authenticate` and `validate_loan` are, structurally, exactly the "extend without modifying" idea from the very first definition of a decorator in this file, just applied to authentication and to a business rule instead of a greeting message.

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

**Swapping the stacking order changes the result:**

```python
def double_it(func):
    def inner():
        return 2 * func()
    return inner

def square_it(func):
    def inner():
        x = func()
        return x * x
    return inner

@square_it
@double_it
def num():
    return 10

print(num())
```

```
400
```

Note:

- Here `double_it` runs first (closest to `num`): `double_it(num)()` gives `2 * 10 = 20`.
- `square_it` then runs on that result: `square_it(...)()` gives `20 * 20 = 400`.
- Same two operations, squaring and doubling, as the `decor1`/`decor2` example above, but applying them in the opposite order gives a completely different final number, `400` instead of `200`. This is exactly why decorator order needs to be worked out deliberately rather than guessed.

**Visualizing execution order with `Before`/`After` prints:**

```python
def decorator1(func):
    def wrapper():
        print("Decorator1: Before calling the function")
        func()
        print("Decorator1: After calling the function")
    return wrapper

def decorator2(func):
    def wrapper():
        print("Decorator2: Before calling the function")
        func()
        print("Decorator2: After calling the function")
    return wrapper

@decorator1
@decorator2
def greet():
    print("Hello!")

greet()
```

```
Decorator1: Before calling the function
Decorator2: Before calling the function
Hello!
Decorator2: After calling the function
Decorator1: After calling the function
```

The call flow for this example, step by step:

```
Start
  |
Apply @decorator2
  |
Apply @decorator1
  |
Call greet()
  |
decorator1.wrapper:
  Print "Decorator1: Before calling the function"
  |
  Call decorator2.wrapper
    |
    decorator2.wrapper:
      Print "Decorator2: Before calling the function"
      |
      Call greet()
        |
        Print "Hello!"
      (returns)
    Print "Decorator2: After calling the function"
  (returns)
Print "Decorator1: After calling the function"
  |
Done
```

Note:

- `decorator1` is the outermost wrapper, so it is the first thing to start and the last thing to finish, exactly like the `bold`/`italic` HTML example further down and like nested middleware in a web framework.

**What happens if a decorator never calls the function it wrapped:**

```python
def decorator1(func):
    def wrapper():
        print("Decorator1: Before calling the function")
        # func()
        print("Decorator1: After calling the function")
    return wrapper

def decorator2(func):
    def wrapper():
        print("Decorator2: Before calling the function")
        # func()
        print("Decorator2: After calling the function")
    return wrapper

@decorator1
@decorator2
def greet():
    print("Hello!")

greet()
```

```
Decorator1: Before calling the function
Decorator1: After calling the function
```

Note:

- With `func()` commented out in `decorator1.wrapper`, calling `greet()` never reaches `decorator2.wrapper` at all. `decorator2`'s prints and the original `"Hello!"` never happen, no matter what `decorator2` itself would have done, because the chain was already broken one layer in.
- The same idea applies even without commenting anything out. If a decorator's own logic simply never calls its `func` argument, everything wrapped inside it, including further decorators and the original function, is silently skipped:

```python
def decorator1(fun):
    def wrapper():
        print("Decorator1 execution")
    return wrapper

def decorator2(fun):
    def wrapper():
        print("Decorator2 execution")
    return wrapper

@decorator2
@decorator1
def f1():
    print("Original function execution")

f1()
```

```
Decorator2 execution
```

- `decorator1` wraps `f1`, but its `wrapper` never calls `fun`, so the resulting function only ever prints `"Decorator1 execution"`. `decorator2` then wraps that result the same way, and its `wrapper` also never calls its own `fun` argument. Calling `f1()` (which is now `decorator2`'s `wrapper`) only prints `"Decorator2 execution"`. Neither `"Decorator1 execution"` nor `"Original function execution"` ever runs, even though both decorators were applied.

**Reading order in a realistic example:**

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

`italic` wraps the original `message` first, and `bold` wraps the result of that, so at call time `bold`'s wrapper runs first, calls into `italic`'s wrapper, which finally calls the original function. This is the same nesting shape as middleware chains: the outermost decorator is the first thing to start and the last thing to finish.

Order also changes what a decorator actually measures. `@retry` above `@timer` times each retry attempt individually; `@timer` above `@retry` times the entire retry loop, including every failed attempt, as one block. Both are valid, but they answer different questions, so picking the wrong order silently produces the wrong numbers rather than an error.

## **Async-Safe Decorators**

A decorator written the ordinary way breaks the moment it is applied to an `async def` function, because calling a coroutine function does not run it; it returns a coroutine object that still needs to be awaited.

```python
def logged(func):
    def inner(*args, **kwargs):
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
- Forgetting `functools.wraps(func)` on the inner function leaves `__name__` and `__doc__` pointing at the wrapper instead of the original, harmless in a script, but confusing in stack traces and broken in tools like FastAPI that read a function's real signature to build documentation.
- Applying `@decor` and then also calling `decorfunction = decor(wish)` on the same name causes double wrapping, so the extra behavior runs twice; a function should be decorated exactly once, either with `@decor` or with a manual reassignment, not both.
- Writing a wrapper that never calls its `func` argument, whether on purpose or by accident, silently skips the original function and any further decorators wrapped underneath it, without raising any error at all.
- Stacking decorators in the wrong order, for example `@timer` below `@retry` instead of above it, silently changes what is being measured or protected, rather than raising an error, so the intended order needs to be worked out deliberately, not guessed.
- Applying a synchronous-only decorator to an `async def` function returns an un-awaited coroutine object instead of the real result, and the bug is often only noticed much later, when something tries to use that "result" and fails somewhere unrelated.
- Building a decorator factory like `retry(max_attempts=3)` but forgetting the extra layer of nesting, writing `def retry(max_attempts, func):` instead of `def retry(max_attempts): def decorator(func): ...`, breaks the `@retry(max_attempts=3)` call syntax entirely.

## **Production Patterns**

Decorator factories are the same three-layer shape seen throughout this file, no matter which library defines them.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/students/{student_id}")
def get_student(student_id: int):
    return {"student_id": student_id, "name": "Arjun"}
```

`@app.get("/students/{student_id}")` takes configuration (a URL path) and returns the actual decorator that registers `get_student` as a route handler, structurally identical to `@retry(max_attempts=3)`.

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

`@app.command()` turns a plain function into a runnable CLI subcommand by reading its parameters and type hints, the same "wrap a function, read its metadata, register it somewhere" shape as a route decorator.

| Library | Key Feature | Best Use Case |
| --- | --- | --- |
| `functools` | `wraps`, `lru_cache`, `cache`, `singledispatch`, standard-library decorator building blocks | Hand-written decorators, memoization, type-based dispatch |
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

`typing.override`, added in Python 3.12, is itself a decorator worth knowing about even though it is not a custom decorator being written; it marks a method as intentionally overriding a parent class method, so a type checker can flag it if the parent method is later renamed or removed.

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
| Function aliasing | `greeting = wish` | A second name pointing at the same function object |
| Nested function | `def outer(): def inner(): ...; return inner` | A function defined, and optionally returned, inside another |
| Basic decorator | `def decor(func): ... return inner` | Wrap a function with extra behavior |
| Apply with `@` | `@decor` above `def f(): ...` | Shorthand for `f = decor(f)` |
| Apply manually | `wrapped = decor(f)` | Keep both the original and wrapped version callable |
| Any signature | `def inner(*args, **kwargs): ...` | Make a decorator reusable across functions |
| Preserve identity | `@functools.wraps(func)` on `inner` | Keep `__name__`, `__doc__`, and signature intact |
| Configurable decorator | `def retry(max_attempts): def decorator(func): ...` | Support `@retry(max_attempts=3)` |
| Class-based decorator | `class D: def __init__(self, func): ... def __call__(self, *a, **kw): ...` | Track state, expose extra attributes |
| Stacking | `@outer` `@inner` `def f(): ...` | Apply multiple decorators; bottom-up build, top-down run |
| Skip the wrapped function | A wrapper that never calls `func(...)` | Deliberately (or accidentally) replace behavior instead of extending it |
| Async-safe | `async def inner(*args, **kwargs): ... await func(...)` | Correctly wrap `async def` functions |
| Detect async | `inspect.iscoroutinefunction(func)` | Branch between sync and async wrapper logic |