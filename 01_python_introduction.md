# **Python Fundamentals — 2026 Edition**

## **What is Python?**

Python is a general-purpose, high-level programming language developed by **Guido van Rossum** in 1989 at the National Research Institute, Netherlands. It was officially released on **February 20, 1991**, and is widely recommended as the first language for beginners due to its clean, readable syntax.

- Named after the British TV comedy show *Monty Python's Flying Circus*, not the snake.
- Combines ideas from C, C++, Perl, and Modula-3.
- Current stable version: **Python 3.14** (released October 7, 2025).

**Why Python is simpler than other languages:**

Java requires a class definition, a `main` method, and `System.out.println` just to print something. C needs header includes and a `main` function with the right signature. Python does the same in one line:

```python
print("Hello, World!")
```

---

## **Python Versions Timeline**

| Version | Release Date | Notes |
|---|---|---|
| Python 1.0 | January 1994 | First public release |
| Python 2.0 | October 2000 | Unicode support added |
| Python 3.0 | December 2008 | Not backward-compatible with Python 2 |
| Python 3.13 | October 2024 | Improved REPL, experimental GIL-free mode |
| **Python 3.14** | **October 7, 2025** | **Current stable release** |


## **Applications of Python**

- Desktop and Web Applications
- Database Applications
- Network Programming
- Game Development
- Data Analysis, Machine Learning, and Artificial Intelligence
- IoT Applications

---

## **Features of Python**

- **Simple and Easy to Learn** — Readable syntax with fewer keywords; reads close to plain English.
- **Freeware and Open Source** — No license required; the source code is publicly available and customizable (e.g., Jython was built by modifying CPython).
- **High-Level Language** — You focus on program logic; Python handles memory allocation and machine-level details.
- **Platform Independent** — Python source code compiles to bytecode that runs on Windows, Linux, or macOS without modification.
- **Dynamically Typed** — Variable types are assigned automatically at runtime; no need to declare types explicitly.
- **Supports Multiple Paradigms** — Supports both procedural and object-oriented programming styles.
- **Interpreted** — No explicit compilation step; the interpreter runs code line by line and reports errors as they are encountered.
- **Extensible** — Performance-critical parts can be written in C or C++ and called from Python (e.g., NumPy internals).
- **Embeddable** — Python code can be embedded inside other programs written in C or C++.
- **Extensive Standard Library** — Ships with built-in modules for file I/O, networking, JSON, CSV, cryptography, and much more.

---

## **Limitations of Python**

- Slower than compiled languages like C or Java because it is interpreted.
- Very limited use in mobile application development; no mainstream Python-based framework for native Android or iOS apps.

---

## **Flavors of Python**

| Flavor | Purpose |
|---|---|
| CPython | Standard implementation, written in C; what you get from python.org |
| Jython / JPython | Runs on the JVM; used for Java integration |
| IronPython | Runs on .NET platform |
| PyPy | Uses JIT compilation for significantly faster execution |
| RubyPython | For Ruby platform integration |
| AnacondaPython | Distribution pre-loaded with data science libraries |

---

## **Identifiers**

An identifier is a name you give to a variable, function, class, or module in your program.

```python
salary = 75000
employee_name = "Rohit"
```

### **Rules for Writing Identifiers**

- Allowed characters are letters (a–z, A–Z), digits (0–9), and underscore (`_`). No other symbols are permitted.
- An identifier must not start with a digit, though digits are allowed after the first character.
- Identifiers are case-sensitive — `total`, `Total`, and `TOTAL` are three different names.
- Reserved words like `def`, `if`, and `class` cannot be used as identifiers.
- There is no length limit, but overly long names are discouraged for readability.

```python
# Valid
total = 10
total123 = 20
_rate = 3.5
java2share = "notes"

# Invalid
123total = 10    # starts with a digit — SyntaxError
ca$h = 500       # $ not allowed — SyntaxError
def = 10         # reserved word — SyntaxError
```

**Valid vs Invalid — quick reference:**

| Identifier | Valid? |
|---|---|
| `123total` | No — starts with digit |
| `total123` | Yes |
| `java2share` | Yes |
| `ca$h` | No — `$` not allowed |
| `_abc_abc_` | Yes |
| `def` | No — reserved word |
| `if` | No — reserved word |

### **Underscore Conventions**

| Pattern | Meaning |
|---|---|
| `_name` | Private by convention |
| `__name` | Strongly private; triggers name-mangling inside classes |
| `__name__` | Special/magic name defined by Python (e.g., `__init__`, `__add__`) |

---

## **Reserved Words**

Reserved words (keywords) are predefined names with a fixed meaning in Python. They represent built-in operations and control structures and cannot be used as identifiers — doing so raises a `SyntaxError`.

- Python 3.14 has **35 keywords** in total.
- All keywords are lowercase, except `True`, `False`, and `None` which are capitalized.
- `a = true` raises a `NameError`; the correct form is `a = True`.

```python
import keyword
print(keyword.kwlist)
```

| Category | Keywords |
|---|---|
| Boolean and null | `True`, `False`, `None` |
| Logical operators | `and`, `or`, `not`, `is` |
| Conditionals | `if`, `elif`, `else` |
| Loops | `while`, `for`, `break`, `continue`, `in`, `yield` |
| Functions / Classes | `def`, `class`, `return`, `lambda`, `pass` |
| Exception handling | `try`, `except`, `finally`, `raise`, `assert` |
| Imports | `import`, `from`, `as` |
| Scope and cleanup | `global`, `nonlocal`, `del`, `with` |

---

## **Data Types in Python**

A data type defines what kind of value a variable holds and what operations are valid on it. Python is **dynamically typed** — you never declare the type; the interpreter assigns it automatically based on the value.

```python
x = 42         # int
x = 3.14       # float — same variable, type changes
x = "Tanvi"    # str
```

**Built-in functions to inspect a variable:**

- `type(x)` — returns the type of `x`.
- `id(x)` — returns the memory address of the object.

```python
a = 100
print(type(a))   # <class 'int'>
print(id(a))     # memory address
```

**Inbuilt data types in Python:**

`int`, `float`, `complex`, `bool`, `str`, `bytes`, `bytearray`, `range`, `list`, `tuple`, `set`, `frozenset`, `dict`, `None`

---

### **int**

The `int` type represents whole numbers. Python integers have no fixed size limit — they grow as large as memory allows.

Python allows integer literals in four number systems:

| System | Prefix | Example | Decimal Value |
|---|---|---|---|
| Decimal (base 10) | None | `255` | 255 |
| Binary (base 2) | `0b` or `0B` | `0b11111111` | 255 |
| Octal (base 8) | `0o` or `0O` | `0o377` | 255 |
| Hexadecimal (base 16) | `0x` or `0X` | `0xFF` | 255 |

```python
a = 255         # decimal
b = 0b11111111  # binary  -> 255
c = 0o377       # octal   -> 255
d = 0xFF        # hex     -> 255

print(a, b, c, d)  # 255 255 255 255
```

**Base conversion functions:**

```python
print(bin(15))      # '0b1111'
print(bin(0o11))    # '0b1001'
print(oct(10))      # '0o12'
print(oct(0b1111))  # '0o17'
print(hex(100))     # '0x64'
print(hex(0o12345)) # '0x14e5'
```

**Real-world use — file permission flags:**

```python
READ    = 0b100   # 4
WRITE   = 0b010   # 2
EXECUTE = 0b001   # 1
permissions = READ | WRITE
print(permissions)  # 6
```

---

### **float**

The `float` type represents numbers with a decimal point. Internally uses 64-bit double precision (IEEE 754), giving around 15–17 significant digits.

```python
price = 1499.99
tax_rate = 0.18
total = price + (price * tax_rate)
print(total)  # 1769.9882
```

**Exponential (scientific) notation** is supported using `e` or `E`:

```python
avogadro = 6.022e23     # 6.022 × 10^23
electron_mass = 9.109e-31
```

**Restriction:** Floats can only be written in decimal form. Binary, octal, and hex prefixes on floats are all `SyntaxError`:

```python
f = 0b11.01    # SyntaxError
f = 0o12.5     # SyntaxError
f = 0xFF.5     # SyntaxError
```

---

### **complex**

A complex number has a real part and an imaginary part, written as `a + bj` where `j` is the imaginary unit.

```python
z1 = 3 + 5j
z2 = 10 + 5.5j
z3 = 0.5 + 0.1j

result = z1 + z2
print(result)     # (13+10.5j)
print(z1.real)    # 3.0
print(z1.imag)    # 5.0
```

- The real part can be in decimal, binary, octal, or hex form.
- The imaginary part must always be a decimal value — binary or octal imaginary parts are a `SyntaxError`.

```python
a = 0xFF + 3j    # valid — hex real, decimal imaginary
b = 3 + 0b10j    # SyntaxError — binary imaginary not allowed
```

Complex numbers are commonly used in signal processing, electrical engineering, and scientific computing.

---

### **bool**

The `bool` type has exactly two values: `True` and `False`. Internally, `True == 1` and `False == 0`, so booleans work in arithmetic.

```python
is_active = True
has_access = False

score = 85
passed = score >= 50
print(passed)          # True

print(True + True)     # 2
print(True - False)    # 1
```

Boolean values are the result of comparisons and logical operations, and they control all conditional logic (`if`, `while`) in programs.

---

### **str**

The `str` type represents a sequence of characters. Strings are immutable — individual characters cannot be changed after creation. There is no separate `char` type; a single character is just a string of length 1.

Strings can be defined with single, double, or triple quotes. Triple quotes allow multi-line strings and embedded quotes without escaping:

```python
name = 'Tanvi'
city = "Pune"
bio = """Software engineer.
Loves Python and coffee."""

s1 = '''This is a "quoted" word'''
s2 = """This is a 'quoted' word"""
```

**Indexing** — positive indices count from left (starting at 0), negative from right (starting at -1):

```python
s = "software"
print(s[0])    # 's'
print(s[-1])   # 'e'
print(s[40])   # IndexError: string index out of range
```

**Slicing** — `[start:end]` where start is inclusive and end is exclusive:

```python
s = "software"
print(s[1:5])  # 'oftw'
print(s[:4])   # 'soft'
print(s[4:])   # 'ware'
print(s[:])    # 'software'
```

**Other string operations:**

```python
tag = "py"
print(tag * 3)   # 'pypypy'
print(len(s))    # 8
```

**Escape characters:**

| Escape | Meaning |
|---|---|
| `\n` | New line |
| `\t` | Horizontal tab |
| `\r` | Carriage return |
| `\b` | Backspace |
| `\f` | Form feed |
| `\v` | Vertical tab |
| `\'` | Single quote |
| `\"` | Double quote |
| `\\` | Backslash |

```python
msg = "Status:\tActive\nUser:\tKaran"
print(msg)
# Status:    Active
# User:      Karan

path = "C:\\Users\\Karan\\Documents"
print(path)  # C:\Users\Karan\Documents
```

---

### **bytes**

The `bytes` type is an immutable sequence of integers in the range 0–255. It is used for binary data like images, network packets, and raw file I/O.

```python
data = [72, 101, 108, 108, 111]
b = bytes(data)
print(b)        # b'Hello'
print(b[0])     # 72
```

---

### **bytearray**

`bytearray` is identical to `bytes` but mutable — individual elements can be modified after creation.

```python
buf = bytearray([10, 20, 30, 40])
buf[0] = 99
print(list(buf))  # [99, 20, 30, 40]
```

Every value must stay in the range 0–255, otherwise a `ValueError` is raised:

```python
bytearray([10, 256])  # ValueError: byte must be in range(0, 256)
```

---

### **range**

The `range` type represents an immutable sequence of integers. It does not store all values in memory — it computes each value on demand, making it memory-efficient even for large sequences.

Three forms:

- `range(n)` — generates 0 to n–1.
- `range(start, stop)` — generates start to stop–1.
- `range(start, stop, step)` — generates values with a step between each.

```python
r1 = range(5)          # 0, 1, 2, 3, 4
r2 = range(1, 6)       # 1, 2, 3, 4, 5
r3 = range(0, 10, 2)   # 0, 2, 4, 6, 8

for i in r3:
    print(i)

print(list(range(5)))  # [0, 1, 2, 3, 4]
```

Range is immutable — you cannot assign to an index:

```python
r = range(10)
print(r[0])    # 10  — indexing is allowed
print(r[15])   # IndexError: range object index out of range
r[0] = 100     # TypeError: 'range' object does not support item assignment
```

---

### **list**

A `list` is an ordered, mutable, heterogeneous collection. It preserves insertion order, allows duplicate values, and can grow or shrink dynamically.

```python
cart = ["laptop", "mouse", 1499.99, True]
print(cart[0])      # 'laptop'
print(cart[-1])     # True
print(cart[1:3])    # ['mouse', 1499.99]

cart[2] = 1299.99
cart.append("keyboard")
cart.remove("mouse")
print(cart)         # ['laptop', 1299.99, True, 'keyboard']

tags = ["python", "ml"]
print(tags * 2)     # ['python', 'ml', 'python', 'ml']
```

**Key features:**

- Insertion order is preserved.
- Heterogeneous objects are allowed (mix of types in one list).
- Duplicates are allowed.
- Growable — elements can be added or removed at any time.

---

### **tuple**

A `tuple` is an ordered, immutable collection. It works like a list for indexing and slicing, but no element can be added, removed, or changed after creation.

```python
coordinates = (28.6139, 77.2090)   # Delhi lat/lon
rgb_red = (255, 0, 0)

print(coordinates[0])      # 28.6139
coordinates[0] = 0         # TypeError: 'tuple' object does not support item assignment
```

- Tuples are the read-only version of lists.
- Use tuples for fixed data like coordinates, color codes, or config values that should not change.

---

### **set**

A `set` is an unordered collection of unique elements. It does not preserve insertion order, does not allow duplicates, and does not support index-based access.

```python
visitors = {"Rohit", "Tanvi", "Om", "Rohit", "Tanvi"}
print(visitors)   # {'Om', 'Tanvi', 'Rohit'} — duplicates removed

visitors.add("Harsha")
visitors.remove("Om")
print(visitors)   # {'Tanvi', 'Rohit', 'Harsha'}

print(visitors[0])  # TypeError: 'set' object is not subscriptable
```

Sets support mathematical operations like union (`|`), intersection (`&`), and difference (`-`):

```python
backend = {"Python", "Django", "PostgreSQL"}
frontend = {"React", "TypeScript", "Python"}
print(backend & frontend)   # {'Python'}
```

**Key features:**

- Insertion order is not preserved.
- Duplicate values are automatically removed.
- Heterogeneous objects are allowed.
- Mutable and growable.

---

### **frozenset**

`frozenset` is exactly like `set` but immutable. Once created, elements cannot be added or removed.

```python
s = {10, 20, 30, 40}
fs = frozenset(s)
print(type(fs))   # <class 'frozenset'>
print(fs)         # frozenset({40, 10, 20, 30})

fs.add(70)        # AttributeError: 'frozenset' object has no attribute 'add'
fs.remove(10)     # AttributeError
```

Because it is immutable, a `frozenset` can be used as a dictionary key or as an element inside another set — a regular `set` cannot.

---

### **dict**

A `dict` stores data as key-value pairs. Keys must be unique; duplicate keys silently overwrite the previous value. Values can be anything and can repeat.

```python
employee = {
    "name": "Karan",
    "role": "ML Engineer",
    "salary": 120000
}

print(employee["name"])    # 'Karan'
employee["salary"] = 135000
employee["team"] = "AI Research"
print(employee)
```

Duplicate key — last assignment wins:

```python
config = {"host": "localhost", "host": "192.168.1.1"}
print(config)   # {'host': '192.168.1.1'}
```

Starting with an empty dict and adding pairs:

```python
cache = {}
cache["session_id"] = "abc123"
cache["user"] = "Rohit"
print(cache)   # {'session_id': 'abc123', 'user': 'Rohit'}
```

**Key points:**

- Duplicate keys are not allowed; duplicate values are fine.
- Dicts are mutable — keys can be added, modified, or deleted.
- From Python 3.7 onwards, insertion order is preserved.

---

### **None**

`None` represents the absence of a value. It is its own type (`NoneType`) and is similar to `null` in Java. It is used when a variable has no meaningful value yet, or when a function does not explicitly return anything.

```python
def get_user(user_id):
    if user_id == 0:
        return None
    return {"name": "Karan", "id": user_id}

result = get_user(0)
print(result)          # None
print(type(result))    # <class 'NoneType'>
```

---

## **Data Types Summary**

| Type | Mutable | Ordered | Duplicates | Example |
|---|---|---|---|---|
| `int` | No | — | — | `42` |
| `float` | No | — | — | `3.14` |
| `complex` | No | — | — | `3+5j` |
| `bool` | No | — | — | `True` |
| `str` | No | Yes | Yes | `"Tanvi"` |
| `bytes` | No | Yes | Yes | `b'hello'` |
| `bytearray` | Yes | Yes | Yes | `bytearray([1,2])` |
| `range` | No | Yes | Yes | `range(10)` |
| `list` | Yes | Yes | Yes | `[1, 2, 3]` |
| `tuple` | No | Yes | Yes | `(1, 2, 3)` |
| `set` | Yes | No | No | `{1, 2, 3}` |
| `frozenset` | No | No | No | `frozenset({1,2})` |
| `dict` | Yes | Yes (3.7+) | Keys: No | `{"a": 1}` |
| `NoneType` | No | — | — | `None` |

---

## **Immutability and Memory Optimization**

All fundamental types (`int`, `float`, `str`, `bool`) are **immutable** — once an object is created, its value cannot be changed. When you "modify" a variable, Python creates a new object and points the variable to it.

Python also reuses existing objects for the same value to save memory. This is easy to observe:

```python
a = 10
b = 10
print(a is b)        # True  — same object in memory
print(id(a), id(b))  # same address

a = a + 1
print(a is b)        # False — new object created for 11
print(id(a), id(b))  # different addresses
```

```python
s1 = "software"
s2 = "software"
print(s1 is s2)      # True — Python reuses the same string object

s1 = s1 + " engineer"
print(s1 is s2)      # False — new object created by concatenation
```

```python
b1 = True
b2 = True
print(b1 is b2)      # True — Python always reuses True and False objects
```

This reuse of objects is called **interning**. It works for small integers, boolean values, and string literals that look like valid identifiers. It saves memory when the same value appears many times across a program.

**Why immutability matters:** If two variables point to the same object and that object could be modified, changing one would silently affect the other. Immutability prevents this class of bugs entirely.

---

## **Type Casting**

Type casting means converting a value from one data type to another. Python provides five built-in functions for this: `int()`, `float()`, `complex()`, `bool()`, and `str()`.

---

### **int()**

Converts a value to an integer. When converting a float, it **truncates** (drops the decimal), it does not round. String input must be a base-10 integer literal — decimal strings like `"3.14"` and words like `"ten"` raise `ValueError`. Complex numbers cannot be converted to `int`.

```python
int(3.99)      # 3   — truncates, not rounds
int(True)      # 1
int(False)     # 0
int("42")      # 42

int("3.14")    # ValueError
int("ten")     # ValueError
int(3 + 5j)    # TypeError
```

---

### **float()**

Converts a value to a float. Accepts integers, booleans, and strings containing integer or decimal values. Non-numeric strings and complex numbers raise errors.

```python
float(10)       # 10.0
float(True)     # 1.0
float("3.14")   # 3.14
float("10")     # 10.0

float("ten")    # ValueError
float(3 + 5j)   # TypeError
```

---

### **complex()**

Has two forms:

- `complex(x)` — real part is `x`, imaginary part is `0`.
- `complex(x, y)` — real part is `x`, imaginary part is `y`.

```python
complex(10)           # (10+0j)
complex(10.5)         # (10.5+0j)
complex(True)         # (1+0j)

complex(10, -2)       # (10-2j)
complex(True, False)  # (1+0j)
```

---

### **bool()**

Converts a value to `True` or `False`. Any value that is zero, empty, or `None` is `False`; everything else is `True`.

```python
bool(0)        # False
bool(1)        # True
bool(10)       # True
bool(10.5)     # True
bool("")       # False
bool("hello")  # True
bool([])       # False
bool([1])      # True
```

---

### **str()**

Converts any value to its string representation.

```python
str(10)        # '10'
str(10.5)      # '10.5'
str(10 + 5j)   # '(10+5j)'
str(True)      # 'True'
str(None)      # 'None'
```

Real-world use — Python does not allow concatenating a string with a non-string directly, so `str()` is needed when mixing types in a message:

```python
name = "Tanvi"
score = 98
msg = "Candidate: " + name + " | Score: " + str(score)
print(msg)   # Candidate: Tanvi | Score: 98
```

---

## **Constants in Python**

Python has no built-in `const` keyword. The convention is to write constant names in all-uppercase letters to signal they should not be reassigned:

```python
MAX_RETRIES = 3
API_BASE_URL = "https://api.example.com/v1"
PI = 3.14159265
```

- This is a naming convention only — Python will not stop you from reassigning `MAX_RETRIES = 999`.
- The expectation is that you and your teammates respect the convention and treat all-uppercase names as read-only values.