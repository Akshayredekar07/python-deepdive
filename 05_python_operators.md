# **Python Operators**

## **Introduction**

An operator is a symbol that tells Python to perform a specific operation on one or more values (called operands). Understanding operators deeply matters because every meaningful Python expression — from a Pydantic validator to a FastAPI permission check — is built from them.

Python provides the following categories of operators:

- Arithmetic Operators
- Relational (Comparison) Operators
- Equality Operators
- Logical Operators
- Bitwise Operators
- Assignment Operators (including the Walrus Operator `:=`)
- Ternary (Conditional) Operator
- Identity Operators
- Membership Operators

---

## **Arithmetic Operators**

Arithmetic operators perform standard mathematical operations.

| Operator | Description         | Example    | Result  |
|----------|---------------------|------------|---------|
| `+`      | Addition            | `10 + 2`   | `12`    |
| `-`      | Subtraction         | `10 - 2`   | `8`     |
| `*`      | Multiplication      | `10 * 2`   | `20`    |
| `/`      | Division (float)    | `10 / 2`   | `5.0`   |
| `//`     | Floor Division      | `10 // 3`  | `3`     |
| `%`      | Modulo (remainder)  | `10 % 3`   | `1`     |
| `**`     | Exponentiation      | `10 ** 2`  | `100`   |

```python
a = 10
b = 2

print("a + b  —", a + b)   # 12
print("a - b  —", a - b)   # 8
print("a * b  —", a * b)   # 20
print("a / b  —", a / b)   # 5.0   — always float
print("a // b —", a // b)  # 5
print("a % b  —", a % b)   # 0
print("a ** b —", a ** b)  # 100
```

**Important notes:**

- `/` always returns a `float`, even when both operands are integers (`10 / 2` → `5.0`, not `5`).
- `//` performs floor division — it rounds down to the nearest integer. If either operand is a float, the result is a float (`7.0 // 2` → `3.0`).
- `%` (modulo) returns the remainder after division, commonly used to check if a number is even or odd.
- `**` is right-associative: `2 ** 3 ** 2` is evaluated as `2 ** (3 ** 2)` = `2 ** 9` = `512`.

### **String Operations with `+` and `*`**

The `+` and `*` operators are overloaded to work on strings as well.

- `+` performs string concatenation — both operands must be strings.
- `*` performs string repetition — one operand must be an integer.

```python
print("durga" + "soft")   # 'durgasoft'
print("durga" * 3)         # 'durgadurgadurga'

# These raise TypeError:
# "durga" + 10
# "durga" * 2.5
```

### **Production Example — Pagination Offset Calculation**

Modulo and floor division appear constantly in real backend code for pagination logic.

```python
def get_page_range(page: int, page_size: int = 10) -> dict:
    offset = (page - 1) * page_size   # start row
    limit = page_size
    total_pages_hint = f"Page {page} starts at row {offset}"
    return {"offset": offset, "limit": limit, "hint": total_pages_hint}

print(get_page_range(3))
# {'offset': 20, 'limit': 10, 'hint': 'Page 3 starts at row 20'}
```

### **Production Example — Bitwise Power Check (Fast Even/Odd)**

```python
# Checking even/odd with % is idiomatic; in performance-critical paths
# bitwise AND against 1 is marginally faster
employee_ids = [1001, 1002, 1003, 1004, 1005]

for eid in employee_ids:
    label = "even" if eid % 2 == 0 else "odd"
    print(f"Employee {eid} — {label}")
```

---

## **Relational (Comparison) Operators**

Relational operators compare two values and return a boolean (`True` or `False`).

| Operator | Description              |
|----------|--------------------------|
| `>`      | Greater than             |
| `>=`     | Greater than or equal to |
| `<`      | Less than                |
| `<=`     | Less than or equal to    |

```python
a = 10
b = 20

print("a > b  —", a > b)   # False
print("a >= b —", a >= b)  # False
print("a < b  —", a < b)   # True
print("a <= b —", a <= b)  # True
```

### **String Comparison**

Strings are compared lexicographically using the Unicode value of each character.

```python
a = "durga"
b = "durga"

print("a > b  —", a > b)   # False
print("a >= b —", a >= b)  # True
print("a < b  —", a < b)   # False
print("a <= b —", a <= b)  # True
```

### **Chaining Relational Operators**

Python allows chaining comparison operators, which reads naturally like a mathematical range expression.

```python
x = 25
print(10 < x < 50)         # True — x is between 10 and 50
print(10 < 20 < 30 < 40)   # True
print(10 < 20 < 15)        # False — 20 < 15 fails
```

Chaining is more readable and avoids redundant `and` expressions. It is idiomatic Python.

**Note:** Relational operators cannot compare incompatible types — `10 > "durga"` raises a `TypeError`.

### **Production Example — Age Gate Validation**

```python
def is_eligible_for_loan(age: int, credit_score: int) -> bool:
    return 21 <= age <= 65 and credit_score >= 700

print(is_eligible_for_loan(30, 750))   # True
print(is_eligible_for_loan(17, 800))   # False
print(is_eligible_for_loan(70, 750))   # False
```

---

## **Equality Operators**

| Operator | Description                        |
|----------|------------------------------------|
| `==`     | Returns `True` if values are equal |
| `!=`     | Returns `True` if values differ    |

Unlike relational operators, equality operators can compare across incompatible types without raising an error — they simply return `False`.

```python
print(10 == 20)            # False
print(10 != 20)            # True
print(10 == True)          # False — True equals 1, not 10
print(False == False)      # True
print("durga" == "durga")  # True
print(10 == "durga")       # False — no TypeError here
```

### **Chaining Equality Operators**

```python
print(10 == 10 == 10 == 10)  # True — all comparisons pass
print(10 == 20 == 30)        # False — first comparison fails
```

---

## **Logical Operators**

Logical operators combine boolean expressions. They also work on non-boolean values using Python's concept of truthiness.

| Operator | Boolean Behaviour                                |
|----------|--------------------------------------------------|
| `and`    | Returns `True` only if both operands are `True`. |
| `or`     | Returns `True` if at least one operand is `True`.|
| `not`    | Inverts the boolean value.                       |

```python
print(True and False)   # False
print(True or False)    # True
print(not False)        # True
```

### **Short-Circuit Evaluation with Non-Boolean Types**

Python does not evaluate the second operand if the first operand already determines the result. This is called short-circuit evaluation and is important for writing safe guard clauses.

**`and` rules:**
- If the first operand is falsy (0, `False`, `""`, `None`, `[]`), it returns the first operand immediately.
- Otherwise, it returns the second operand.

**`or` rules:**
- If the first operand is truthy, it returns the first operand immediately.
- Otherwise, it returns the second operand.

```python
print(10 and 20)        # 20  — first is truthy, return second
print(0 and 20)         # 0   — first is falsy, return first
print(10 or 20)         # 10  — first is truthy, return first
print(0 or 20)          # 20  — first is falsy, return second
print(not 10)           # False
print(not 0)            # True

# With strings
print("durga" and "durgasoft")  # 'durgasoft'
print("" and "durga")           # ''
print("durga" or "")            # 'durga'
print(not "")                   # True
print(not "durga")              # False
```

### **Production Example — Default Config with `or`**

The `or` short-circuit pattern is a classic Python idiom for providing fallback defaults.

```python
import os

# If the env variable is not set, fall back to a default
db_host = os.environ.get("DB_HOST") or "localhost"
db_port = os.environ.get("DB_PORT") or "5432"
log_level = os.environ.get("LOG_LEVEL") or "INFO"

print(f"Connecting to {db_host}:{db_port} — Log level: {log_level}")
```

**Caution:** From Python 3.8+, prefer `or` defaults only for string/truthy fallbacks. For values that can legitimately be `0` or `False`, use `if value is None` or the `??`-style pattern via Pydantic validators instead.

### **Production Example — Guard Clause with `and`**

```python
def process_order(order: dict) -> str:
    # Short-circuit: skip expensive DB call if order is empty
    is_valid = order and order.get("items") and order.get("user_id")
    if not is_valid:
        return "Invalid order — missing required fields"
    return f"Processing order for user {order['user_id']}"

print(process_order({"user_id": 42, "items": ["GPU", "SSD"]}))
# Processing order for user 42

print(process_order({}))
# Invalid order — missing required fields
```

---

## **Bitwise Operators**

Bitwise operators work directly on the binary representation of integers. They are only applicable to `int` and `bool` types — using them on `float` raises a `TypeError`.

| Operator | Name              | Description                                            |
|----------|-------------------|--------------------------------------------------------|
| `&`      | AND               | Result bit is 1 only if both bits are 1.               |
| `\|`     | OR                | Result bit is 1 if at least one bit is 1.              |
| `^`      | XOR               | Result bit is 1 if the bits are different.             |
| `~`      | Complement        | Inverts all bits. `~n` equals `-(n + 1)`.             |
| `<<`     | Left Shift        | Shifts bits left; equivalent to multiplying by `2^n`.  |
| `>>`     | Right Shift       | Shifts bits right; equivalent to dividing by `2^n`.    |

```python
print(4 & 5)    # 4   — 0100 & 0101 = 0100
print(4 | 5)    # 5   — 0100 | 0101 = 0101
print(4 ^ 5)    # 1   — 0100 ^ 0101 = 0001
print(~5)       # -6  — bitwise complement, result is -(5+1)

print(10 << 2)  # 40  — 10 * (2^2) = 10 * 4 = 40
print(10 >> 2)  # 2   — 10 // (2^2) = 10 // 4 = 2
```

**Why `~5` is `-6`:** Python stores integers in two's complement form. Inverting all bits of `5` (binary `...0000 0101`) gives `...1111 1010`, which represents `-6` in two's complement.

### **Bitwise Operators with Boolean Types**

Since `True == 1` and `False == 0`, bitwise operators work on booleans as well.

```python
print(True & False)   # False
print(True | False)   # True
print(True ^ False)   # True
print(~True)          # -2  — -(1+1)
print(True << 2)      # 4   — 1 * 4
print(True >> 2)      # 0
```

### **Production Example — Permission Flags (Role-Based Access Control)**

Bitwise operators are the standard technique for compact, fast permission systems in production APIs. Each bit represents one permission.

```python
# Permission flags — each is a power of 2 (single bit set)
READ    = 0b0001   # 1
WRITE   = 0b0010   # 2
DELETE  = 0b0100   # 4
ADMIN   = 0b1000   # 8

# Assign permissions to a user by ORing flags together
arjun_perms = READ | WRITE          # 0011 = 3
tanvi_perms = READ | WRITE | DELETE  # 0111 = 7
harsha_perms = READ | ADMIN          # 1001 = 9

def can(user_perms: int, flag: int) -> bool:
    return bool(user_perms & flag)   # bitwise AND to check if bit is set

print(can(arjun_perms, READ))    # True
print(can(arjun_perms, DELETE))  # False
print(can(tanvi_perms, DELETE))  # True
print(can(harsha_perms, ADMIN))  # True

# Revoke WRITE from Arjun using XOR (toggles the bit)
arjun_perms ^= WRITE
print(can(arjun_perms, WRITE))   # False
```

This exact pattern is used inside Django's permission system and many JWT scope implementations.

### **Production Example — Fast Even/Odd and Power-of-Two Check**

```python
def is_even(n: int) -> bool:
    return not (n & 1)   # last bit is 0 for even numbers

def is_power_of_two(n: int) -> bool:
    # A power of 2 has exactly one bit set; n & (n-1) clears it
    return n > 0 and (n & (n - 1)) == 0

print(is_even(1024))          # True
print(is_power_of_two(64))    # True
print(is_power_of_two(100))   # False
```

---

## **Assignment Operators**

Assignment operators assign a value to a variable. Compound assignment operators combine a computation with the assignment in one step.

```python
x = 10        # basic assignment
x += 20       # x = x + 20 → 30
print(x)      # 30

x = 10
x &= 5        # x = x & 5 → 0
print(x)      # 0
```

### **Compound Assignment Operators Reference**

| Operator | Equivalent To  | Example       |
|----------|----------------|---------------|
| `+=`     | `x = x + n`   | `x += 5`      |
| `-=`     | `x = x - n`   | `x -= 3`      |
| `*=`     | `x = x * n`   | `x *= 2`      |
| `/=`     | `x = x / n`   | `x /= 4`      |
| `%=`     | `x = x % n`   | `x %= 7`      |
| `//=`    | `x = x // n`  | `x //= 3`     |
| `**=`    | `x = x ** n`  | `x **= 2`     |
| `&=`     | `x = x & n`   | `x &= 0xFF`   |
| `\|=`   | `x = x \| n`  | `x \|= 0x01`  |
| `^=`     | `x = x ^ n`   | `x ^= 0b101`  |
| `>>=`    | `x = x >> n`  | `x >>= 1`     |
| `<<=`    | `x = x << n`  | `x <<= 2`     |

---

## **Walrus Operator `:=` (Assignment Expression)**

Introduced in **Python 3.8** via PEP 572, the walrus operator `:=` allows you to assign a value to a variable inside an expression. This eliminates redundant calls and tightens loop conditions.

**Syntax:**
```python
variable := expression
```

The walrus operator both evaluates the expression and binds the result to `variable` at the same time.

### **Classic Use — Avoiding Double Calls in a Loop**

```python
import re

log_lines = [
    "ERROR: connection timeout on host db-prod-01",
    "INFO: health check passed",
    "ERROR: disk usage exceeded 90% on /var/data",
    "DEBUG: cache miss for key user:1042",
]

# Without walrus — re.search is called twice per line
for line in log_lines:
    if re.search(r"ERROR", line):
        print("Alert:", re.search(r"ERROR", line).group())

# With walrus — called once, result reused
for line in log_lines:
    if match := re.search(r"ERROR", line):
        print("Alert —", line)
```

### **Walrus in List Comprehension**

```python
from datetime import datetime

def parse_date(s: str) -> datetime | None:
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        return None

raw = ["2024-03-15", "bad-date", "2025-01-01", "nope", "2026-06-10"]

# Without walrus — parse_date() called twice per item
valid = [parse_date(d) for d in raw if parse_date(d)]

# With walrus — called once, falsy results filtered out
valid = [dt for d in raw if (dt := parse_date(d))]
print(valid)
```

### **Production Example — FastAPI / Pydantic Guard Chain**

This early-return pattern is idiomatic in API handler functions where each step depends on the previous one succeeding.

```python
from typing import Optional

def validate_user(data: dict) -> Optional[dict]:
    return data if data.get("email") else None

def check_permissions(user: dict) -> Optional[dict]:
    return {"can_write": True} if user.get("role") == "admin" else None

def save_to_db(user: dict, data: dict) -> Optional[dict]:
    return {"id": 1, **data}  # simulate DB insert

def handle_submission(raw_data: dict) -> dict:
    if not (user := validate_user(raw_data)):
        return {"status": 400, "body": "Invalid user"}
    if not (perms := check_permissions(user)) or not perms["can_write"]:
        return {"status": 403, "body": "Forbidden"}
    if not (record := save_to_db(user, raw_data)):
        return {"status": 500, "body": "DB failure"}
    return {"status": 201, "body": record}

result = handle_submission({"email": "arjun@durgasoft.in", "role": "admin"})
print(result)  # {'status': 201, 'body': {...}}
```

**When not to use walrus:** Avoid it for trivial one-liners where a regular assignment is clearer. Do not stack more than two or three walrus expressions in the same expression — it hurts readability.

---

## **Ternary (Conditional) Operator**

Python's ternary operator expresses a conditional assignment in a single line.

**Syntax:**
```python
x = value_if_true if condition else value_if_false
```

```python
a, b = 10, 20

x = 30 if a < b else 40
print(x)   # 30
```

### **Minimum and Maximum of Two Numbers**

```python
a = int(input("Enter First Number: "))
b = int(input("Enter Second Number: "))

min_val = a if a < b else b
max_val = a if a > b else b

print("Minimum —", min_val)
print("Maximum —", max_val)
```

### **Nested Ternary — Minimum of Three Numbers**

```python
a = int(input("Enter First Number: "))
b = int(input("Enter Second Number: "))
c = int(input("Enter Third Number: "))

min_val = a if (a < b and a < c) else b if b < c else c
print("Minimum —", min_val)
```

### **Number Comparison**

```python
a = int(input("Enter First Number: "))
b = int(input("Enter Second Number: "))

print(
    "Both numbers are equal" if a == b else
    "First Number is Less than Second Number" if a < b else
    "First Number is Greater than Second Number"
)
```

Nested ternaries work, but keep them shallow — two levels maximum. Deeper nesting becomes difficult to read and should be replaced with `if-elif-else` blocks.

### **Production Example — HTTP Status Label**

```python
def status_label(code: int) -> str:
    return "success" if 200 <= code < 300 else "redirect" if 300 <= code < 400 else "error"

print(status_label(200))   # success
print(status_label(301))   # redirect
print(status_label(500))   # error
```

### **Production Example — Ternary in f-strings and Pydantic**

```python
from dataclasses import dataclass

@dataclass
class Employee:
    name: str
    salary: float
    department: str

    def summary(self) -> str:
        tier = "senior" if self.salary >= 100_000 else "junior"
        return f"{self.name} — {tier} {self.department} engineer"

rohit = Employee("Rohit", 120_000, "ML")
drishya = Employee("Drishya", 75_000, "backend")

print(rohit.summary())    # Rohit — senior ML engineer
print(drishya.summary())  # Drishya — junior backend engineer
```

---

## **Special Operators**

### **Identity Operators**

Identity operators check whether two variables point to the exact same object in memory — not whether they are equal in value.

| Operator  | Description                                               |
|-----------|-----------------------------------------------------------|
| `is`      | Returns `True` if both variables reference the same object. |
| `is not`  | Returns `True` if both variables reference different objects. |

```python
a = 10
b = 10
print(a is b)    # True — Python caches small integers

x = True
y = True
print(x is y)    # True

a = "durga"
b = "durga"
print(a is b)    # True — string interning
print(id(a), id(b))

list1 = ["one", "two", "three"]
list2 = ["one", "two", "three"]
print(id(list1), id(list2))    # different addresses
print(list1 is list2)          # False — different objects
print(list1 is not list2)      # True
print(list1 == list2)          # True — same content
```

**Rule:** Use `is` to compare against singletons like `None`, `True`, or `False`. Use `==` for value comparison.

```python
# Correct idiom in production code
def get_user(user_id: int):
    result = None  # simulate DB miss
    if result is None:
        return {"error": "User not found"}
    return result
```

### **Membership Operators**

Membership operators check whether a value exists inside a collection (string, list, tuple, set, dict).

| Operator   | Description                                            |
|------------|--------------------------------------------------------|
| `in`       | Returns `True` if the value is found in the collection. |
| `not in`   | Returns `True` if the value is not found.               |

```python
sentence = "hello, learning Python is very easy!"
print('h' in sentence)        # True
print('d' in sentence)        # False
print('Python' in sentence)   # True
print('d' not in sentence)    # True

engineers = ["Karan", "Om", "Harsha", "Tanvi"]
print("Karan" in engineers)    # True
print("Durga" in engineers)    # False
print("Durga" not in engineers) # True
```

### **Production Example — Membership in API Role Checks**

```python
ALLOWED_ROLES = {"admin", "moderator", "ml_engineer"}

def authorize(user_role: str, endpoint: str) -> bool:
    if user_role not in ALLOWED_ROLES:
        print(f"Unauthorized — role '{user_role}' is not permitted")
        return False
    print(f"Access granted to '{endpoint}' for role '{user_role}'")
    return True

authorize("admin", "/api/v1/models/deploy")    # Access granted
authorize("viewer", "/api/v1/models/deploy")   # Unauthorized
```

**Performance note:** Use a `set` instead of a `list` for membership checks when the collection is large. `in` on a `set` is O(1); on a `list` it is O(n).

```python
# Slow — O(n) scan
ROLES_LIST = ["admin", "moderator", "ml_engineer"]
"admin" in ROLES_LIST   # scans left to right

# Fast — O(1) hash lookup
ROLES_SET = {"admin", "moderator", "ml_engineer"}
"admin" in ROLES_SET    # direct hash lookup
```

---

## **Operator Precedence**

When multiple operators appear in a single expression, Python evaluates them in a defined order. Higher in the table means evaluated first.

| Priority | Operator(s)                          | Description                         |
|----------|--------------------------------------|-------------------------------------|
| 1        | `()`                                 | Parentheses                         |
| 2        | `**`                                 | Exponentiation                      |
| 3        | `~`, unary `-`                       | Bitwise complement, unary minus     |
| 4        | `*`, `/`, `%`, `//`                  | Multiplication, division, modulo    |
| 5        | `+`, `-`                             | Addition, subtraction               |
| 6        | `<<`, `>>`                           | Bitwise shifts                      |
| 7        | `&`                                  | Bitwise AND                         |
| 8        | `^`                                  | Bitwise XOR                         |
| 9        | `\|`                                 | Bitwise OR                          |
| 10       | `>`, `>=`, `<`, `<=`, `==`, `!=`     | Comparison operators                |
| 11       | `=`, `+=`, `-=`, ...                 | Assignment operators                |
| 12       | `is`, `is not`                       | Identity operators                  |
| 13       | `in`, `not in`                       | Membership operators                |
| 14       | `not`                                | Logical NOT                         |
| 15       | `and`                                | Logical AND                         |
| 16       | `or`                                 | Logical OR                          |

```python
print(3 + 10 * 2)        # 23  — * before +
print((3 + 10) * 2)      # 26  — parentheses first

a, b, c, d = 30, 20, 10, 5

print((a + b) * c / d)       # 100.0
print(a + (b * c) / d)       # 70.0

result = 3 / 2 * 4 + 3 + (10 / 5) ** 3 - 2
# Step by step:
# = 1.5 * 4 + 3 + 2.0**3 - 2
# = 6.0 + 3 + 8.0 - 2
# = 15.0
print(result)   # 15.0
```

**Practical tip:** When in doubt, use parentheses. They never hurt performance and always improve readability, which matters more in production code.

---

## **The `math` Module**

The `math` module is part of Python's standard library. It provides mathematical functions and constants beyond what the basic arithmetic operators offer.

```python
import math

print(math.sqrt(16))   # 4.0
print(math.pi)         # 3.141592653589793
print(math.e)          # 2.718281828459045
print(math.inf)        # inf
print(math.nan)        # nan
```

### **Using an Alias**

```python
import math as m

print(m.sqrt(25))   # 5.0
print(m.pi)         # 3.141592653589793
```

### **Importing Specific Members**

```python
from math import sqrt, pi, ceil, floor

print(sqrt(49))    # 7.0
print(ceil(4.2))   # 5
print(floor(4.9))  # 4
```

Once a function is imported this way, you cannot access it via `math.sqrt()` — the module name is not in scope.

### **Key Functions Reference**

| Function          | Description                                              | Example                | Result    |
|-------------------|----------------------------------------------------------|------------------------|-----------|
| `ceil(x)`         | Smallest integer ≥ x                                     | `ceil(4.1)`            | `5`       |
| `floor(x)`        | Largest integer ≤ x                                      | `floor(4.9)`           | `4`       |
| `pow(x, y)`       | x raised to power y (returns float)                      | `pow(2, 10)`           | `1024.0`  |
| `factorial(x)`    | x! (x must be a non-negative integer)                    | `factorial(5)`         | `120`     |
| `trunc(x)`        | Truncates decimal part, returns integer                  | `trunc(4.99)`          | `4`       |
| `gcd(x, y)`       | Greatest common divisor                                  | `gcd(12, 8)`           | `4`       |
| `sqrt(x)`         | Square root                                              | `sqrt(144)`            | `12.0`    |
| `sin(x)`          | Sine of x in radians                                     | `sin(math.pi / 2)`     | `1.0`     |
| `cos(x)`          | Cosine of x in radians                                   | `cos(0)`               | `1.0`     |
| `tan(x)`          | Tangent of x in radians                                  | `tan(math.pi / 4)`     | `~1.0`    |
| `log(x, base)`    | Logarithm of x to a given base (default: natural log)    | `log(100, 10)`         | `2.0`     |
| `isnan(x)`        | Returns `True` if x is NaN                               | `isnan(float('nan'))`  | `True`    |
| `isinf(x)`        | Returns `True` if x is infinite                          | `isinf(math.inf)`      | `True`    |

### **Key Constants Reference**

| Constant   | Value                   | Use Case                       |
|------------|-------------------------|--------------------------------|
| `math.pi`  | `3.141592653589793`     | Circle geometry                |
| `math.e`   | `2.718281828459045`     | Natural logarithm, exponential |
| `math.inf` | Positive infinity       | Sentinel value in algorithms   |
| `math.nan` | Not a number            | Missing/undefined numeric data |
| `math.tau` | `6.283185...` (2π)      | Full-circle radian operations  |

### **Example — Area of a Circle**

```python
from math import pi

radius = 16
area = pi * radius ** 2
print(f"Area of circle with radius {radius} — {area:.4f}")
# Area of circle with radius 16 — 804.2477
```

### **Production Example — Ceiling for Pagination Total Pages**

```python
from math import ceil

def total_pages(total_items: int, page_size: int = 10) -> int:
    return ceil(total_items / page_size)

print(total_pages(95))    # 10
print(total_pages(100))   # 10
print(total_pages(101))   # 11
```

### **Production Example — Cosine Similarity (Vector Search)**

Cosine similarity is used in embedding-based retrieval (RAG systems, recommendation engines). It relies on `math` functions directly for simple cases.

```python
import math

def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = math.sqrt(sum(a ** 2 for a in vec_a))
    magnitude_b = math.sqrt(sum(b ** 2 for b in vec_b))
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)

query_embedding    = [0.2, 0.8, 0.5, 0.1]
document_embedding = [0.3, 0.7, 0.4, 0.2]

score = cosine_similarity(query_embedding, document_embedding)
print(f"Similarity score — {score:.4f}")   # ~0.9877
```

---

## **Common Mistakes and Modern Patterns**

### **Mistake 1 — Using `==` to Compare Against `None`**

```python
# Wrong — fragile, can behave unexpectedly with custom __eq__
if result == None:
    pass

# Correct — always use `is` for None checks
if result is None:
    pass
```

### **Mistake 2 — Using `and`/`or` for Default Values When `0` Is Valid**

```python
count = 0

# Wrong — returns 10 even though count is a valid value
display = count or 10   # 10 ← incorrect!

# Correct — explicit None check
display = count if count is not None else 10   # 0 ← correct
```

### **Mistake 3 — Comparing Floating Point with `==`**

Floating point arithmetic is inexact. Comparing floats with `==` can silently return wrong results.

```python
# Wrong
print(0.1 + 0.2 == 0.3)   # False — due to floating point representation

# Correct — use math.isclose()
import math
print(math.isclose(0.1 + 0.2, 0.3))   # True
```

### **Modern Pattern — Union Type with `|` Operator (Python 3.10+)**

Since Python 3.10, the `|` operator is used in type annotations as a cleaner replacement for `Optional` and `Union`.

```python
# Old style (pre-3.10)
from typing import Optional, Union
def process(data: Union[str, int]) -> Optional[str]:
    return str(data) if data else None

# Modern style (Python 3.10+)
def process(data: str | int) -> str | None:
    return str(data) if data else None
```

### **Modern Pattern — Structural Pattern Matching with Operators (Python 3.10+)**

`match-case` uses structural matching, not equality operators, but understanding how values compare is still essential.

```python
def handle_event(event: dict) -> str:
    match event:
        case {"type": "login", "user": str(name)}:
            return f"User {name} logged in"
        case {"type": "error", "code": int(code)} if code >= 500:
            return f"Server error — code {code}"
        case {"type": "error", "code": int(code)}:
            return f"Client error — code {code}"
        case _:
            return "Unknown event"

print(handle_event({"type": "login", "user": "Karan"}))
# User Karan logged in

print(handle_event({"type": "error", "code": 503}))
# Server error — code 503
```

---

## **Quick Reference — Operator Summary**

| Category      | Operators                              | Works On                   |
|---------------|----------------------------------------|----------------------------|
| Arithmetic    | `+`, `-`, `*`, `/`, `//`, `%`, `**`   | int, float, str (some)     |
| Comparison    | `>`, `>=`, `<`, `<=`, `==`, `!=`      | All comparable types       |
| Logical       | `and`, `or`, `not`                     | All types (truthy/falsy)   |
| Bitwise       | `&`, `\|`, `^`, `~`, `<<`, `>>`       | int, bool only             |
| Assignment    | `=`, `+=`, `-=`, ..., `:=`            | All types                  |
| Identity      | `is`, `is not`                         | All objects                |
| Membership    | `in`, `not in`                         | Sequences and collections  |
| Ternary       | `x if cond else y`                     | All types                  |