## **CLOSURES**

## **4.1 What a Closure Actually Is**

A closure is a function that remembers the variables from the scope it was created in, even after that outer scope has finished running.

**Basic example — the multiplier factory**

```python
def make_multiplier(factor):
    def multiplier(value):
        return value * factor
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15
```

Walk through what happens here, step by step:

1. `make_multiplier(2)` runs. Inside it, `factor` is set to `2`.
2. `make_multiplier` defines `multiplier`, a small inner function that uses `factor`.
3. `make_multiplier` returns `multiplier` and then finishes running completely.
4. Normally, once a function finishes, its local variables disappear. But `multiplier` still needs `factor`, so Python keeps `factor` alive and attached to `multiplier`.
5. `double` now refers to that `multiplier` function, permanently carrying `factor = 2` with it.
6. Calling `double(5)` runs `5 * factor`, which is `5 * 2 = \boxed{10}`.
7. `triple` was built the same way but with `factor = 3`, so `triple(5)` gives `5 * 3 = \boxed{15}`.

This is the core idea of a closure: the inner function carries a reference to the variables it needs from its enclosing scope, packaged along with the function itself.

**The three conditions for a closure to exist**

1. There must be a nested function (a function defined inside another function).
2. The nested function must reference a variable from the enclosing function.
3. The enclosing function must return the nested function (rather than just calling it).

**Seeing the closure directly — `__closure__` and cell objects**

```python
def make_multiplier(factor):
    def multiplier(value):
        return value * factor
    return multiplier

double = make_multiplier(2)

print(double.__closure__)                     # (<cell at 0x...: int object at 0x...>,)
print(double.__closure__[0].cell_contents)     # 2
print(double.__code__.co_freevars)              # ('factor',)
```

Python does not copy `factor` by value into `multiplier`. Instead it creates a **cell** — a small box holding a reference to the variable — and both the enclosing function and the inner function point at the same cell. This is also why `nonlocal` can change the enclosing variable from inside the inner function: they share the same cell, not separate copies.

**A closure over multiple variables**

```python
def make_range_checker(low, high):
    def in_range(value):
        return low <= value <= high
    return in_range

is_valid_age = make_range_checker(0, 120)
is_valid_pct = make_range_checker(0, 100)

print(is_valid_age(45))    # True
print(is_valid_pct(150))   # False
print(is_valid_age.__code__.co_freevars)   # ('high', 'low')
```

Here the inner function `in_range` remembers two variables from its enclosing scope, `low` and `high`, not just one.

**Why closures matter in practice.** They let you generate specialized functions without writing a class, keep private state that cannot be reached or changed from outside (unlike a global variable), and are the exact mechanism that makes decorators (Stage 5) work — a decorator is nothing more than a closure that wraps another function.

## **4.2 Common Closure Bug — Late Binding in Loops**

This is the single most common closure bug in real code. It shows up constantly once you start writing factories, callback registries, or UI event handlers inside a loop.

**The bug**

```python
def make_handlers():
    handlers = []
    for i in range(3):
        def handler():
            return f"handler for {i}"
        handlers.append(handler)
    return handlers

for h in make_handlers():
    print(h())
# handler for 2
# handler for 2
# handler for 2
```

All three closures share the same cell for `i`. Closures capture variables **by reference**, not by value — the inner function looks up `i` fresh every time it runs, and by the time any of the three handlers is actually called, the loop has already finished and `i` is `2`.

**Why this surprises people.** It looks like each iteration should "freeze" its own `i`, the way arguments are frozen when a function is called. But `i` here is not an argument — it is a free variable, resolved at call time by walking up to the enclosing scope, and there is only one `i` cell, reused by every iteration of the loop.

**Fix 1 — default argument, evaluated immediately at definition time**

```python
def make_handlers():
    handlers = []
    for i in range(3):
        def handler(i=i):
            return f"handler for {i}"
        handlers.append(handler)
    return handlers

for h in make_handlers():
    print(h())
# handler for 0
# handler for 1
# handler for 2
```

A default argument value is evaluated once, when the `def` line runs — which happens fresh on every loop iteration — so each `handler` gets its own snapshot of `i` baked into its signature.

**Fix 2 — an extra enclosing function per iteration**

```python
def make_handlers():
    handlers = []
    for i in range(3):
        def make_handler(i):
            def handler():
                return f"handler for {i}"
            return handler
        handlers.append(make_handler(i))
    return handlers
```

`make_handler(i)` is called once per iteration with the current value of `i` as an argument, creating a brand new scope and a brand new cell each time.

**Fix 3 — `functools.partial`**

```python
from functools import partial

def handler(i):
    return f"handler for {i}"

handlers = [partial(handler, i) for i in range(3)]
print([h() for h in handlers])   # ['handler for 0', 'handler for 1', 'handler for 2']
```

`partial` binds the current value of `i` into a new callable immediately, sidestepping the closure entirely.

**Same bug, with lambdas in a list comprehension**

```python
squares = [lambda: i * i for i in range(5)]
print([f() for f in squares])            # [16, 16, 16, 16, 16] (all see the final i)

squares = [lambda i=i: i * i for i in range(5)]
print([f() for f in squares])            # [0, 1, 4, 9, 16] (fixed)
```

**Where this bites in real code.** Registering Flask/FastAPI routes dynamically in a loop, building a dict of validators in a loop, wiring up GUI button callbacks in a loop, and building a list of partially-configured retry callbacks for different API endpoints are all places this bug shows up in production code — usually discovered only when every "different" callback mysteriously does the same thing.

## **4.3 Practical Uses — Factories and Hand-Rolled Memoization**

**Factories, generalized**

```python
def make_validator(predicate, error_message):
    def validate(value):
        if not predicate(value):
            raise ValueError(error_message)
        return value
    return validate

validate_positive = make_validator(lambda x: x > 0, "value must be positive")
validate_email = make_validator(lambda s: "@" in s, "value must contain @")

print(validate_positive(5))     # 5
# validate_positive(-1)         # ValueError: value must be positive
```

**A configuration-bound function — common in real APIs and pipelines**

```python
def make_api_client(base_url, api_key):
    def call(endpoint, **params):
        headers = {"Authorization": f"Bearer {api_key}"}
        url = f"{base_url}/{endpoint}"
        return {"url": url, "headers": headers, "params": params}
    return call

staging_client = make_api_client("https://staging.example.com", "key-staging-123")
prod_client = make_api_client("https://api.example.com", "key-prod-456")

print(staging_client("users", limit=10))
```

`staging_client` and `prod_client` are both closures over different `base_url`/`api_key` pairs — you get two independently configured clients without writing a class.

**Hand-rolled memoization with a closure**

Memoization caches a function's results so repeated calls with the same arguments skip recomputation. Before reaching for `functools.lru_cache` (Stage 6), it's worth building one by hand once, to see exactly what it is doing.

```python
def memoize(fn):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = fn(*args)
        return cache[args]
    return wrapper

def slow_square(n):
    import time
    time.sleep(0.5)
    return n * n

fast_square = memoize(slow_square)

print(fast_square(5))   # takes ~0.5s, computes and caches
print(fast_square(5))   # instant, returns cached result
print(fast_square(6))   # takes ~0.5s again, a new argument
```

`cache` lives in the closure created by `memoize`. Every call to `wrapper` shares the same `cache` dict through the same cell, which is exactly what lets the cache persist across calls — this is `memoize` acting as a decorator, which is the natural bridge into Stage 5.

**Memoizing a recursive function by hand**

```python
def memoize(fn):
    cache = {}
    def wrapper(n):
        if n not in cache:
            cache[n] = fn(n)
        return cache[n]
    return wrapper

@memoize
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(35))   # fast, thanks to caching (without memoize, this is painfully slow)
```

**Closures as lightweight, private state — an alternative to a class**

```python
def make_bank_account(balance=0):
    def deposit(amount):
        nonlocal balance
        balance += amount
        return balance

    def withdraw(amount):
        nonlocal balance
        if amount > balance:
            raise ValueError("insufficient funds")
        balance -= amount
        return balance

    def get_balance():
        return balance

    return {"deposit": deposit, "withdraw": withdraw, "balance": get_balance}

account = make_bank_account(100)
print(account["deposit"](50))     # 150
print(account["withdraw"](30))    # 120
print(account["balance"]())       # 120
```

Trace the balance step by step:

1. `make_bank_account(100)` sets `balance = 100` in the enclosing scope.
2. `account["deposit"](50)` adds `50` to `balance`: $100 + 50 = \boxed{150}$.
3. `account["withdraw"](30)` subtracts `30` from `balance`: $150 - 30 = \boxed{120}$.
4. `account["balance"]()` just reads the current `balance`, which is $\boxed{120}$.

There is no way to reach `balance` directly from outside — it only exists inside the closure. This is a genuine alternative to writing a small class purely to hold private mutable state.

**Per-request state in a web app — a closure with no class**

```python
def make_request_state(user_id):
    requests = 0
    def middleware():
        nonlocal requests
        requests += 1
        return f"user={user_id} call#{requests}"
    return middleware

karan_state = make_request_state("karan")
tanvi_state = make_request_state("tanvi")

print(karan_state())   # user=karan call#1
print(karan_state())   # user=karan call#2
print(tanvi_state())   # user=tanvi call#1
```

Each closure carries its own independent `requests` count — `karan_state` and `tanvi_state` never interfere with each other, even though they were built from the exact same factory function.

## **4.4 Common Closure Mistakes**

**Forgetting `nonlocal`**

```python
def make_counter():
    count = 0
    def tick():
        count = count + 1     # UnboundLocalError -- count is treated as local, read before assignment
        return count
    return tick
```

Adding `nonlocal count` fixes it. Without it, Python treats `count` inside `tick` as a brand-new local variable because it is being assigned to, and that local variable has no value yet when the addition happens.

**Holding a large object alive through a closure.** A closure keeps every variable it captures alive for as long as the closure itself is alive — including large ones you didn't mean to keep around.

```python
def make_handler(large_dataframe):        # imagine this is several GB
    def handle(row_id):
        return row_id in large_dataframe
    return handle

# handle stays alive somewhere in your app, so large_dataframe can never be
# garbage collected, even if nothing else in the program still needs it
```

If a closure only needs a small piece of a large object, extract that piece before capturing it, or restructure so the large object is passed in as an argument on each call instead of captured once and held forever.

**Storing closures in a long-lived container.** A module-level list or dict that accumulates closures over the life of a long-running process (a web server, a worker) keeps every one of those closures — and everything each of them captured — alive for as long as the process runs. This is fine for something small like the accumulator pattern above; it is a genuine memory leak if each stored closure captures something sizable, like a database connection or a large parsed document.
