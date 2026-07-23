# **Custom Exceptions and the `raise` Keyword**

Built-in exceptions cover a lot of ground — `ValueError`, `KeyError`, `TypeError`, `FileNotFoundError`. But real applications have errors that no built-in describes well: "insufficient funds in wallet", "age outside the eligible range for this scheme", "user tried to apply a discount code that has already expired", "API returned a payload that doesn't match the expected schema". For these situations you define and raise your own exception classes.

This file covers the `raise` keyword, how to write a custom exception class, the PEP 8 conventions for naming and inheritance, exception chaining with `raise from`, and the patterns you will see in real codebases.

---

## **Types of Exceptions**

Python exceptions fall into two broad categories:

| Category | Also called | Who defines them | How they get raised |
|---|---|---|---|
| **Predefined exceptions** | Built-in exceptions, inbuilt exceptions | The Python language | The PVM raises them automatically when a specific runtime condition is met |
| **User-defined exceptions** | Customized exceptions, programmatic exceptions | You, the programmer | You raise them explicitly with the `raise` keyword |

### **Predefined Exceptions — Examples**

```python
# 1) ZeroDivisionError — division by zero
print(10 / 0)
```

```
ZeroDivisionError: division by zero
```

```python
# 2) ValueError — wrong value, right type
x = int("ten")
```

```
ValueError: invalid literal for int() with base 10: 'ten'
```

The PVM does the work — you did not write `raise ZeroDivisionError(...)` anywhere. The PVM detected the runtime condition and created the exception object on its own.

### **User-Defined Exceptions — When You Need Them**

You define a custom exception when **no built-in exception describes the problem semantically**. The built-in `ValueError` can carry the message "balance cannot be negative", but it cannot distinguish "negative balance" from "user typed a non-numeric string" — both are `ValueError`. If your application needs to *react* to one differently from the other, you need your own class.

Common real-world examples:

- `InsufficientFundsError`
- `InvalidInputError` / `InvalidAgeError`
- `TooYoungException` / `TooOldException`
- `OrderAlreadyShippedError`
- `PaymentDeclinedError`
- `DatabaseConnectionError`, `RetryableError`, `PermanentError` (a small hierarchy)

**Note:** the `raise` keyword is **best suited for customized exceptions**. For predefined exceptions, you almost never write `raise ValueError(...)` yourself — the PVM raises them for you. You *can* re-raise a built-in (e.g. `raise ValueError("custom message")`), and that is sometimes useful, but the everyday use of `raise` is with your own classes.

---

## **Defining a Custom Exception Class**

The minimum legal custom exception is two lines:

```python
class MyError(Exception):
 pass
```

That is enough to make `MyError` a distinct exception type that callers can catch specifically:

```python
try:
 raise MyError("something went wrong")
except MyError as e:
 print("Caught:", e)
```

```
Caught: something went wrong
```

The base class `Exception.__init__` accepts a single string message and stores it in `self.args[0]`, which is what `str(e)` returns. You do not need to write your own `__init__` for that.

### **When you need more than a message**

Define `__init__` when your exception needs to carry *structured* information, not just a string. The pattern is:

1. Call `super().__init__(message)` first — this preserves the standard message behavior, so the exception still prints nicely in tracebacks.
2. Store extra attributes on `self`.

```python
class InsufficientFundsError(Exception):
 """Raised when a wallet does not have enough balance for a transaction."""

 def __init__(self, balance, amount):
 self.balance = balance
 self.amount = amount
 self.deficit = amount - balance
 super().__init__(
 f"Need {amount}, but wallet only has {balance} "
 f"(short by {self.deficit})"
 )
```

Now the exception carries both a human-readable message and structured data that handlers can use programmatically:

```python
try:
 raise InsufficientFundsError(balance=100, amount=350)
except InsufficientFundsError as e:
 print("Message:", e)
 print("Balance:", e.balance)
 print("Amount: ", e.amount)
 print("Deficit:", e.deficit)
```

```
Message: Need 350, but wallet only has 100 (short by 250)
Balance: 100
Amount: 350
Deficit: 250
```

### **The minimum-viable class from the source content**

The original notes use this very simple pattern — a custom exception that just stores a single string:

```python
class TooYoungException(Exception):
 def __init__(self, arg):
 self.msg = arg
```

This works, but a few things are worth knowing:

- The base `Exception.__init__` would have done the same thing (it stores the message automatically). Writing `self.msg = arg` is essentially duplicate work — but it makes the message accessible as a named attribute (`e.msg` instead of `e.args[0]`), which some people prefer.
- For production code, the more common modern style is to just call `super().__init__(arg)` and access the message via `str(e)`.
- The custom `__init__` above stores the message in `self.msg` but does *not* call `super().__init__`, so `str(e)` will return the default `Exception` repr, not the message. That is usually a bug — the traceback will be less helpful.

```python
class TooYoungException(Exception):
 def __init__(self, arg):
 super().__init__(arg) # also let the base class store the message
 self.msg = arg # and keep our own named attribute
```

With this version, both `str(e)` and `e.msg` return the message, and the traceback displays it correctly.

---

## **The `raise` Keyword**

`raise` is how you tell the PVM: "stop the normal flow of this function and start looking for an exception handler". It works in three forms.

### **Form 1 — Raise a new exception**

```python
raise SomeExceptionClass("message")
```

This creates an instance of `SomeExceptionClass` and throws it. The PVM starts looking for a matching `except` block. If none is found, the program dies with a traceback.

**Real-world example — marriage eligibility:**

```python
class TooYoungException(Exception):
 def __init__(self, arg):
 super().__init__(arg)
 self.msg = arg

class TooOldException(Exception):
 def __init__(self, arg):
 super().__init__(arg)
 self.msg = arg

age = int(input("Enter Age: "))
if age > 60:
 raise TooYoungException("Plz wait some more time, you will get best match soon!!!")
elif age < 18:
 raise TooOldException("Your age already crossed marriage age...no chance of getting married")
else:
 print("You will get match details soon by email!!!")
```

Three run-throughs:

| Input | Output |
|---|---|
| Age = 90 | `__main__.TooYoungException: Plz wait some more time, you will get best match soon!!!` |
| Age = 12 | `__main__.TooOldException: Your age already crossed marriage age...no chance of getting married` |
| Age = 27 | `You will get match details soon by email!!!` |

Note how the exception *name* tells the user what kind of problem happened (`TooYoungException` vs `TooOldException`) — exactly the kind of clarity that built-in exceptions cannot give you for domain-specific problems.

### **Form 2 — Re-raise the current exception**

Inside an `except` block, a bare `raise` (no argument) re-raises the *same* exception object, preserving the original traceback. This is the right way to do "log it, then let the caller deal with it":

```python
try:
 data = open('config.json').read()
except FileNotFoundError as e:
 print("Logging: config file missing at startup")
 raise # re-raise — same exception, same traceback
```

The exception propagates up to the next handler, but the *current* handler had a chance to log, clean up, or add context first.

### **Form 3 — Raise a new exception chained from a caught one (`raise ... from`)**

This is the modern, recommended form for "I caught a low-level error, but the caller should see a higher-level one". The `from` clause preserves the original cause in the traceback.

```python
try:
 raw = db.query("SELECT * FROM users")
except DatabaseConnectionError as err:
 raise RetryableError("Database temporarily unavailable") from err
```

When this propagates, the traceback shows both the `RetryableError` (the high-level, domain-specific problem) *and* the original `DatabaseConnectionError` (the low-level technical cause). The two are linked via the `__cause__` attribute, which you can read programmatically:

```python
try:
 try:
 raise ConnectionError("network down")
 except ConnectionError as e:
 raise RuntimeError("Service unavailable") from e
except RuntimeError as e:
 print("Top-level:", e)
 print("Caused by:", e.__cause__)
```

```
Top-level: Service unavailable
Caused by: network down
```

If you want to *suppress* the original cause (which is rare and usually a bad idea), you can write `raise NewException(...) from None`.

### **Implicit chaining — when you don't write `from`**

If you raise a new exception *inside* an `except` block *without* using `from`, Python still records the relationship, but as `__context__` instead of `__cause__`. The traceback shows a "During handling of the above exception, another exception occurred" line. The two are subtly different: `__cause__` is for *explicit* chaining, `__context__` is for *implicit* chaining.

```python
def parse_age(raw):
 try:
 return int(raw)
 except ValueError:
 raise TypeError(f"age must be numeric, got {raw!r}") # implicit chain

try:
 parse_age("twelve")
except TypeError as e:
 print("Outer:", e)
 print("Context:", type(e.__context__).__name__, "->", e.__context__)
```

```
Outer: age must be numeric, got 'twelve'
Context: ValueError -> invalid literal for int() with base 10: 'twelve'
```

**Best practice:** when you are *replacing* one exception with another, use `raise X from Y` explicitly. It signals intent and makes the cause-vs-context distinction clear in the traceback.

---

## **Custom Exception Best Practices (PEP 8 + Modern Conventions)**

### **Rule 1 — Inherit from `Exception`, not `BaseException`**

PEP 8 is explicit: *derive exceptions from `Exception` rather than `BaseException`*. Direct inheritance from `BaseException` is reserved for cases where catching the exception is almost always the wrong thing to do (e.g. `SystemExit`, `KeyboardInterrupt`).

```python
# Good
class MyError(Exception):
 pass

# Bad — will catch Ctrl+C and sys.exit() if anyone ever does `except MyError`
class MyError(BaseException):
 pass
```

### **Rule 2 — End the class name with `Error` if it is an error**

PEP 8: *use the suffix "Error" on your exception names (if the exception actually is an error).* Non-error exceptions used for non-local flow control or signaling need no suffix.

```python
# Errors end with "Error"
class InsufficientFundsError(Exception): ...
class InvalidAgeError(Exception): ...
class DatabaseConnectionError(Exception): ...

# Non-error signals don't need the suffix
class StopTraining(Exception): ... # used to break out of a training loop, not really an "error"
class RetrySignal(Exception): ...
```

### **Rule 3 — Build a base class for your project's exceptions**

When you build a library or a sizable application, define one `BaseAppError` that inherits from `Exception`, then derive every other custom exception from *that*. This lets the top-level error boundary catch your whole domain at once, while internal code can still handle specific subtypes precisely.

```python
# exceptions.py — a dedicated module for your project's exceptions

class BankingError(Exception):
 """Base class for all banking-related exceptions."""

class InsufficientFundsError(BankingError):
 """Raised when a wallet has less money than the transaction needs."""

class InvalidAccountError(BankingError):
 """Raised when an account number does not exist in the system."""

class DailyLimitExceededError(BankingError):
 """Raised when a withdrawal would push the user over the daily limit."""
```

Now the top-level error boundary can do:

```python
try:
 banking_app.run_daily_batch()
except BankingError as e:
 log.error("Banking operation failed", exc_info=e)
 notify_ops_team(e)
```

while the *internal* code can still respond with surgical precision:

```python
try:
 wallet.withdraw(amount)
except InsufficientFundsError as e:
 wallet.suggest_topup(amount - e.balance) # specific handling
except DailyLimitExceededError:
 wallet.notify_user_about_limit() # specific handling
```

### **Rule 4 — Call `super().__init__` with the message**

This is the small habit that makes tracebacks usable. It guarantees that `str(e)` and the traceback display show the message you passed in.

```python
class DataProcessingError(Exception):
 def __init__(self, message, record_id=None, field=None):
 super().__init__(message) # ← don't skip this
 self.record_id = record_id
 self.field = field
```

If you forget `super().__init__(message)`, the traceback will not include the message, and `str(e)` will return the default `Exception` repr.

### **Rule 5 — Prefer built-in exceptions when one fits**

If a built-in exception describes the problem, use it. Custom exceptions add value when they communicate *domain-specific intent*.

```python
# Built-in is fine here
if age < 0:
 raise ValueError("age cannot be negative")

# Custom is better here — communicates the domain concept
if age < 18 or age > 60:
 raise InvalidAgeError(age, "must be between 18 and 60")
```

### **Rule 6 — Catch the specific class, not the base class, internally**

A common anti-pattern is having the application catch its own base exception too broadly, just to suppress failures. Catch at the right boundary instead — the top-level error boundary catches the base class; internal logic catches the specific subclass.

```python
# Bad — base class used to suppress errors internally
try:
 retry_api_call()
except BankingError:
 pass # swallow the problem

# Good — specific handling internally
try:
 retry_api_call()
except RetryableError:
 schedule_retry()
except PermanentError:
 alert_oncall()
```

### **Rule 7 — Always inherit from `Exception` (or a subclass) — never from `BaseException` for application code**

Already covered in Rule 1, but worth repeating: `BaseException` is for system-level events. Custom application exceptions that inherit from `BaseException` are a code smell.

---

## **Choosing What to Catch: A Decision Matrix**

When you write a `try/except`, you have to decide *what to catch*. Here is a decision matrix that captures the trade-offs:

| Goal | What to catch | Example |
|---|---|---|
| React to one specific problem | That specific class | `except FileNotFoundError:` |
| React the same way to several related problems | Tuple of classes | `except (ValueError, TypeError):` |
| Cover an entire family (e.g. all math errors) | The parent class | `except ArithmeticError:` |
| Cover all "normal" runtime errors at the top level | `Exception` | `except Exception:` in a top-level error boundary |
| Catch literally everything (DON'T) | `BaseException` or bare `except` | Almost always wrong |
| Catch, log, re-raise to the caller | Catch specific, then `raise` | `except KeyError: log; raise` |
| Convert a low-level error to a domain error | Catch low-level, `raise DomainError from err` | `except ConnectionError: raise RetryableError from err` |

---

## **A Complete Real-World Example: Banking Wallet**

The previous sections scattered the custom-exception pattern across small examples. Here is one 30-ish-line program that ties everything together: a tiny banking wallet with custom exceptions, structured attributes, layered handling, and `finally`-based cleanup.

```python
class BankingError(Exception):
 """Base class for all banking-related errors."""
 def __init__(self, message):
 super().__init__(message)
 self.msg = message

class InsufficientFundsError(BankingError):
 def __init__(self, balance, amount):
 self.balance = balance
 self.amount = amount
 super().__init__(
 f"Need {amount}, but wallet only has {balance}"
 )

class DailyLimitExceededError(BankingError):
 def __init__(self, limit, attempted):
 self.limit = limit
 self.attempted = attempted
 super().__init__(
 f"Daily limit is {limit}, attempted withdrawal {attempted}"
 )

class InvalidAccountError(BankingError):
 pass


class Wallet:
 DAILY_LIMIT = 5000

 def __init__(self, owner, balance, account_no):
 self.owner = owner
 self.balance = balance
 self.account_no = account_no
 self.withdrawn_today = 0
 if not account_no.startswith("BK-"):
 raise InvalidAccountError(f"Bad account number format: {account_no}")

 def withdraw(self, amount):
 # Step 1: validate the amount
 if amount <= 0:
 raise ValueError("withdrawal amount must be positive")

 # Step 2: check daily limit
 if self.withdrawn_today + amount > self.DAILY_LIMIT:
 raise DailyLimitExceededError(self.DAILY_LIMIT, amount)

 # Step 3: check funds
 if amount > self.balance:
 raise InsufficientFundsError(self.balance, amount)

 # All checks passed
 self.balance -= amount
 self.withdrawn_today += amount
 print(f"[{self.owner}] Withdrew {amount}. New balance: {self.balance}")
 return amount

 def __repr__(self):
 return f"Wallet(owner={self.owner!r}, balance={self.balance}, account={self.account_no!r})"


# ---------- Use the wallet ----------

wallets = [
 Wallet("Durga", 1000, "BK-001"),
 Wallet("Karan", 8000, "BK-002"),
]

transactions = [
 ("Durga", 200), # ok
 ("Durga", 900), # insufficient funds
 ("Karan", 4500), # ok
 ("Karan", 1000), # would exceed daily limit
 ("Karan", 2000), # ok
]

for owner, amount in transactions:
 wallet = next(w for w in wallets if w.owner == owner)
 try:
 wallet.withdraw(amount)
 except InsufficientFundsError as e:
 print(f" -> REJECTED for {owner}: {e} (short by {e.amount - e.balance})")
 except DailyLimitExceededError as e:
 print(f" -> REJECTED for {owner}: {e} (limit was {e.limit})")
 except ValueError as e:
 print(f" -> REJECTED for {owner}: bad input — {e}")
 except BankingError as e:
 # Catch-all for any other banking problem we have not handled specifically
 print(f" -> UNHANDLED banking error for {owner}: {e}")

print("\nFinal state:")
for w in wallets:
 print(" ", w)
```

Output:

```
[Durga] Withdrew 200. New balance: 800
 -> REJECTED for Durga: Need 900, but wallet only has 800 (short by 100)
[Karan] Withdrew 4500. New balance: 3500
 -> REJECTED for Karan: Daily limit is 5000, attempted withdrawal 1000
[Karan] Withdrew 2000. New balance: 1500

Final state:
 Wallet(owner='Durga', balance=800, account='BK-001')
 Wallet(owner='Karan', balance=1500, account='BK-002')
```

Notice the layered handling:

- Three *specific* exception types are caught first, each with a custom message built from the structured attributes on the exception object.
- A *base-class* catch (`BankingError`) sits at the bottom as a safety net for any new banking error we add in the future.
- The `ValueError` for negative amounts is caught separately because it is not a `BankingError` — it is a generic input validation problem that we want to handle differently.
- Each rejection prints a useful, specific message instead of a raw traceback.

This is the structure you want in real code: a hierarchy of exceptions, specific handlers at the call site, a base-class catch as a safety net, and structured attributes that handlers can use.

---

## **Examples**

### **Example 1 — The minimum-viable custom exception**

```python
class MyError(Exception):
 pass

try:
 raise MyError("custom message")
except MyError as e:
 print("Caught:", e)
 print("Type: ", type(e).__name__)
```

```
Caught: custom message
Type: MyError
```

### **Example 2 — Exception with structured data**

```python
class APIError(Exception):
 def __init__(self, status_code, message):
 self.status_code = status_code
 super().__init__(f"[{status_code}] {message}")

try:
 raise APIError(404, "user not found")
except APIError as e:
 print("Status:", e.status_code)
 print("Full: ", e)
```

```
Status: 404
Full: [404] user not found
```

### **Example 3 — `raise from` preserves the original cause**

```python
def load_config(path):
 try:
 with open(path) as f:
 return f.read()
 except FileNotFoundError as e:
 raise RuntimeError(f"Could not load config from {path}") from e

try:
 load_config("does_not_exist.json")
except RuntimeError as e:
 print("Top error: ", e)
 print("Caused by: ", type(e.__cause__).__name__, "->", e.__cause__)
```

```
Top error: Could not load config from does_not_exist.json
Caused by: FileNotFoundError -> [Errno 2] No such file or directory: 'does_not_exist.json'
```

### **Example 4 — Bare `raise` re-raises with the original traceback**

```python
import logging

logging.basicConfig(level=logging.INFO)

def read_number():
 try:
 return int(input("Enter an integer: "))
 except ValueError:
 logging.exception("read_number failed") # logs the full traceback
 raise # re-raise — caller still sees the error

try:
 n = read_number()
except ValueError as e:
 print("Caller caught:", e)
```

If the user types `ten`:

```
Enter an integer: ten
ERROR:root:read_number failed
Traceback (most recent call last):
 ...
ValueError: invalid literal for int() with base 10: 'ten'
Caller caught: invalid literal for int() with base 10: 'ten'
```

The exception was logged *and* propagated — the caller still had to handle it.

### **Example 5 — Hierarchical base class for a project**

```python
class ECommerceError(Exception):
 """Base for the entire e-commerce domain."""

class ProductError(ECommerceError):
 """Base for product-related errors."""

class OutOfStockError(ProductError):
 pass

class PricingError(ECommerceError):
 pass

class InvalidCouponError(PricingError):
 pass

class ExpiredCouponError(PricingError):
 pass

# Top-level boundary catches the whole domain
def checkout(cart, coupon):
 try:
 for item in cart:
 if item["qty"] > item["stock"]:
 raise OutOfStockError(
 f"{item['name']}: only {item['stock']} in stock"
 )
 if coupon == "EXPIRED10":
 raise ExpiredCouponError("Coupon EXPIRED10 expired last week")
 if coupon == "NOPE":
 raise InvalidCouponError(f"Unknown coupon code: {coupon}")
 except OutOfStockError as e:
 print(" Out of stock:", e)
 except PricingError as e:
 print(" Pricing problem:", e)
 except ECommerceError as e:
 # Any new e-commerce error type lands here
 print(" Other e-commerce error:", e)

checkout(
 cart=[
 {"name": "Notebook", "qty": 1, "stock": 50},
 {"name": "Pen", "qty": 5, "stock": 3}, # 5 > 3 -> OutOfStockError
 ],
 coupon=None
)
```

```
 Out of stock: Pen: only 3 in stock
```

The top-level catch is the base class `ECommerceError`, but the *specific* `OutOfStockError` is caught first because it is listed first.

### **Example 6 — `raise` inside a loop with per-iteration handler**

```python
def process(records):
 successes, failures = 0, 0
 for i, record in enumerate(records):
 try:
 if record < 0:
 raise ValueError(f"negative value: {record}")
 print(f" record {i}: ok ({record})")
 successes += 1
 except ValueError as e:
 print(f" record {i}: SKIPPED — {e}")
 failures += 1
 return successes, failures

s, f = process([10, -5, 20, -1, 30])
print(f"\nDone. Successes: {s}, Failures: {f}")
```

```
 record 0: ok (10)
 record 1: SKIPPED — negative value: -5
 record 2: ok (20)
 record 3: SKIPPED — negative value: -1
 record 4: ok (30)

Done. Successes: 3, Failures: 2
```

One bad record did not stop the rest of the batch.

### **Example 7 — `from None` to suppress the original cause**

```python
def get_user(user_id):
 try:
 return db_query(user_id) # raises some low-level error
 except DatabaseError as e:
 # We deliberately hide the low-level error from the API consumer
 raise UserNotFoundError(user_id) from None

try:
 get_user(42)
except UserNotFoundError as e:
 print("Caught:", e)
 print("Has explicit cause?", e.__cause__)
```

```
Caught: User 42 not found
Has explicit cause? None
```

Use `from None` sparingly. It is appropriate when the underlying error contains sensitive information (e.g. raw SQL, internal IPs) that should not leak to the API consumer.

### **Example 8 — Catching a built-in vs a custom exception, side by side**

```python
class TooYoungException(Exception):
 def __init__(self, arg):
 super().__init__(arg)
 self.msg = arg

class TooOldException(Exception):
 def __init__(self, arg):
 super().__init__(arg)
 self.msg = arg

age = 12
try:
 if age > 60:
 raise TooYoungException("Plz wait some more time")
 if age < 18:
 raise TooOldException("Already crossed marriage age")
except TooYoungException as e:
 print("Too young:", e)
except TooOldException as e:
 print("Too old:", e)
```

```
Too old: Already crossed marriage age
```

Two custom exceptions, each handled with a different message — the value of naming a domain concept precisely.

### **Example 9 — Confirming inheritance with `issubclass`**

```python
class BankError(Exception): pass
class InsufficientFundsError(BankError): pass
class InvalidAccountError(BankError): pass

print(issubclass(InsufficientFundsError, BankError)) # True
print(issubclass(BankError, Exception)) # True
print(issubclass(Exception, BaseException)) # True
print(issubclass(InsufficientFundsError, ValueError)) # False — independent hierarchy
```

```
True
True
True
False
```

A custom exception inherits from `Exception` through the chain `InsufficientFundsError → BankError → Exception → BaseException`. It is *not* related to `ValueError` — they are siblings in the hierarchy, not parent/child.

### **Example 10 — Combining custom exceptions with `try/except/else/finally`**

```python
class OrderError(Exception): pass
class OutOfStockError(OrderError): pass

class Order:
 def __init__(self, items, stock):
 self.items = items
 self.stock = stock

 def place(self):
 try:
 for item, qty in self.items.items():
 if self.stock.get(item, 0) < qty:
 raise OutOfStockError(
 f"only {self.stock.get(item, 0)} {item} in stock, need {qty}"
 )
 except OutOfStockError as e:
 print("Order failed:", e)
 else:
 print("Order placed successfully")
 for item, qty in self.items.items():
 self.stock[item] -= qty
 finally:
 print("Order attempt complete\n")

stock = {"Pen": 10, "Notebook": 5}
Order({"Pen": 3, "Notebook": 2}, stock).place()
Order({"Pen": 99}, stock).place()
```

```
Order placed successfully
Order attempt complete

Order failed: only 7 Pen in stock, need 99
Order attempt complete
```

The `else` block runs only on success; the `finally` block runs in both cases.

---

## **Quick Reference Summary**

### **Built-in vs Custom Exceptions**

| Aspect | Built-in | Custom |
|---|---|---|
| Defined by | Python | You |
| Raised by | The PVM (automatically) | The `raise` keyword (you) |
| When to use | The runtime problem matches a built-in concept | The runtime problem is domain-specific |
| Examples | `ZeroDivisionError`, `ValueError` | `InsufficientFundsError`, `OutOfStockError` |

### **How to Write a Custom Exception**

| Pattern | Code | When to use |
|---|---|---|
| Minimum viable | `class E(Exception): pass` | Just a distinct type, no extra data |
| With a message | `class E(Exception): pass` + `raise E("msg")` | The default — message via `str(e)` |
| With structured data | Override `__init__`, call `super().__init__(message)` | Need attributes like `balance`, `record_id` |
| Hierarchical base | `class AppError(Exception): pass` + `class SpecificError(AppError): pass` | Library / large application code |

### **The Three Forms of `raise`**

| Form | What it does | Typical use |
|---|---|---|
| `raise NewError("msg")` | Raise a new exception | "This shouldn't have happened" |
| `raise` (bare) | Re-raise the current exception | "I caught it to log it, but the caller still has to handle it" |
| `raise NewError("msg") from old_error` | Raise a new exception, link the old one as the cause | "Translate a low-level error into a domain-level one, but keep the original traceback" |
| `raise NewError("msg") from None` | Raise a new exception, suppress the original cause | "Hide the low-level details from the API consumer" |

### **PEP 8 Naming Rules for Custom Exceptions**

| Rule | Do | Don't |
|---|---|---|
| Inherit from `Exception`, not `BaseException` | `class MyError(Exception)` | `class MyError(BaseException)` |
| End error class names with `Error` | `OutOfStockError`, `InvalidAgeError` | `OutOfStock`, `InvalidAge` |
| Non-error exceptions can omit the suffix | `class StopTraining(Exception)` | `class StopTrainingError(Exception)` |
| Build a base class for your project | `class AppError(Exception): pass` | Lots of unrelated top-level exceptions |

### **Catching Strategy**

| Goal | What to catch | Why |
|---|---|---|
| React to a specific problem | That specific class | Surgical response, no over-catching |
| React the same way to a few related problems | Tuple of classes | Avoids code duplication |
| Cover an entire family | The parent class | Convenient when a single response is fine for the whole family |
| Top-level error boundary | `Exception` (or your project's base error class) | Catches everything "regular", lets `Ctrl+C` and `sys.exit()` through |
| Literally everything | `BaseException` / bare `except` | Almost always wrong — catches `Ctrl+C` and `sys.exit()` |

### **Exception Chaining at a Glance**

| Syntax | `__cause__` set? | `__context__` set? | When to use |
|---|---|---|---|
| `raise NewError from old` | to `old` | Implicit | Explicit translation: "this low-level error caused this high-level error" |
| `raise NewError` (inside `except`) | | to the current exception | Implicit — Python records the relationship automatically |
| `raise NewError from None` | to `None` | Implicit | Suppress the original cause deliberately (e.g. for security) |
| `raise` (bare) | unchanged | unchanged | Re-raise the same exception with the original traceback |

---

## **Practice and Next Steps**

1. **Build a base class for a domain.** Pick a domain (banking, library, university, e-commerce — your choice). Define one `DomainError(Exception)` base, then three specific subclasses with structured attributes. Use them in a small 10-line program.
2. **Rewrite a `ValueError` as a custom error.** Take any piece of code that currently raises `ValueError` and replace it with a custom exception that better describes the domain problem. Show the difference in the traceback.
3. **Use `raise from`.** Write a function that catches a built-in (e.g. `KeyError`, `FileNotFoundError`) and re-raises a custom exception. Inspect the `__cause__` attribute to confirm the original cause is preserved.
4. **Test the `from None` pattern.** Modify the function from exercise 3 to use `from None`. Verify the traceback no longer shows the original cause.
5. **Build a layered handler.** Write a function that catches three specific exceptions in order, then a base-class catch, then a final bare `except`. Test which one fires for each kind of input and verify that bare `except` really is dead code (or only fires for things you did not anticipate).
6. **Read PEP 8's exception section.** Skim the [Style Guide for Python Code](https://peps.python.org/pep-0008/#programming-recommendations) — specifically the *Programming Recommendations* section on exceptions. Note the four rules (inherit from `Exception`, suffix `Error`, exception chaining, name specific exceptions).
7. **Refactor a real script.** Take any small program you have and replace any `print("error:", e)` with a proper custom exception that carries structured data. Add a `try/except` at the top level that catches your base exception class and logs it nicely.
8. **Skim the standard library.** Look at the exceptions in `requests`, `django`, or another library you use. Notice their naming conventions and inheritance hierarchies. This is the best way to internalize the pattern — read what experienced developers wrote.
