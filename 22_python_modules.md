# **Python Modules and Imports**

## **What Is a Module**

A module is simply a file that contains Python code — variables, functions, classes, runnable statements — saved with a `.py` extension. Every single `.py` file you write is automatically a module, whether you meant it to be one or not. Once code lives inside a module, that code can be reused in other files instead of being copy-pasted.

Modules exist to solve a simple problem: as programs grow, keeping everything in one file becomes messy and hard to maintain. Splitting related code into separate files makes the codebase easier to read, test, and reuse.

### **Creating a Simple Module**

Save the following as `mathutils.py`:

```python
# mathutils.py
x = 888

def add(a, b):
    print("The Sum:", a + b)

def product(a, b):
    print("The Product:", a * b)
```

This file is now a module called `mathutils`. It contains one variable (`x`) and two functions (`add`, `product`). Nothing special had to be done to turn it into a module — just writing Python in a `.py` file is enough.

### **Using the Module from Another File**

Save the following as `test.py` in the same folder as `mathutils.py`:

```python
# test.py
import mathutils

print(mathutils.x)
mathutils.add(10, 20)
mathutils.product(10, 20)
```

Running `test.py`:

```
888
The Sum: 30
The Product: 200
```

Walking through this:

1. `import mathutils` loads the file `mathutils.py` and creates a module object named `mathutils` in the current program.
2. `mathutils.x` reaches into that module's namespace to read the variable `x`.
3. `mathutils.add(10, 20)` calls the `add` function defined inside the module.

When a module is imported for the first time, Python compiles it into bytecode and caches that compiled version on disk inside a `__pycache__` folder next to the module, as a `.pyc` file. This is purely a performance optimization. On the next import, if the source has not changed, Python skips recompiling and loads the cached `.pyc` directly.

## **Ways to Import a Module**

### **Basic Import**

```python
import modulename
```

After this, members are accessed through dot notation: `modulename.member`.

### **Import With an Alias**

A module can be imported under a shorter or more convenient name using `as`:

```python
import mathutils as mu

print(mu.x)
mu.add(10, 20)
mu.product(10, 20)
```

This is extremely common in real projects — for example `import numpy as np` or `import pandas as pd`. Once aliased, the original module name (`mathutils`) is not available in that file; only `mu` is.

### **Importing Specific Members**

Instead of pulling in the whole module, individual members can be imported directly into the current namespace:

```python
from mathutils import x, add

print(x)
add(10, 20)
```

Members that were not explicitly imported are not available:

```python
from mathutils import x, add
product(10, 20)
```

```
NameError: name 'product' is not defined
```

Walking through it: `from mathutils import x, add` copies just `x` and `add` into the current file's namespace, so they can be used without the `mathutils.` prefix. `product` was never brought in, so calling it directly fails.

### **Importing Everything With `*`**

```python
from mathutils import *

print(x)
add(10, 20)
product(10, 20)
```

This brings every public name from the module into the current namespace. It is convenient for quick scripts, but in larger codebases it is generally avoided because:

- It makes it unclear where a name came from.
- It can silently overwrite existing names in the current file.
- It is hard for tools like linters to reason about.

### **Renaming Members on Import**

Individual members — not just modules — can be renamed at import time:

```python
from mathutils import x as y, add as total

print(y)
total(10, 20)
```

Once a member is aliased this way, the original name is no longer available:

```python
from mathutils import x as y
print(x)
```

```
NameError: name 'x' is not defined
```

Only `y` is bound. This is useful when a member name clashes with a name already in the importing file.

### **Summary of Import Styles**

| Style | Example | Notes |
|---|---|---|
| Basic import | `import module` | Access members as `module.name` |
| Multiple imports | `import module1, module2` | One line, multiple modules |
| Aliased import | `import module as m` | Access as `m.name` |
| Multiple aliased | `import module1 as m1, module2 as m2` | Mix aliased and plain in one line |
| Import specific member | `from module import member` | Use `member` directly |
| Import multiple members | `from module import member1, member2` | Comma separated |
| Aliased member | `from module import member as x` | Renames on import |
| Import everything | `from module import *` | Avoid in larger projects |

## **How Python Finds Modules**

When `import modulename` runs, Python searches for `modulename` in a list of locations stored in `sys.path`. This list typically includes, in order:

1. The directory of the script being run (the empty string `''` entry).
2. Directories listed in the `PYTHONPATH` environment variable, if it is set.
3. The standard library directories bundled with Python.
4. The `site-packages` directory where pip-installed third-party packages live.

You can see the full list:

```python
import sys
print(sys.path)
```

Sample output:

```
['', '/home/you/my_project', '/usr/lib/python311.zip', '/usr/lib/python3.11',
 '/usr/lib/python3.11/lib-dynload',
 '/home/you/.local/lib/python3.11/site-packages',
 '/usr/lib/python3.11/site-packages']
```

The empty string at the start means "the current working directory when Python started". This is why a file in the same folder as your script is importable without any extra setup.

### **Adding to `sys.path` Programmatically**

A common quick fix is to append a folder to `sys.path` at runtime:

```python
import sys
sys.path.append("/home/you/my_project")
import my_helpers
```

This is fine for scripts and notebooks but should not replace proper packaging for a project that other people will install.

### **Setting `PYTHONPATH`**

`PYTHONPATH` is a colon-separated (Linux/macOS) or semicolon-separated (Windows) list of extra directories that Python prepends to `sys.path` at startup.

On Linux/macOS:

```
export PYTHONPATH=/home/you/my_project:/home/you/shared
python my_script.py
```

On Windows (PowerShell):

```
$env:PYTHONPATH = "C:\my_project;C:\shared"
python my_script.py
```

### **The `sys.modules` Cache**

Python keeps a dictionary of every module that has been loaded in the current program. The second import of the same name in the same program does not re-run the file — Python just hands back the same object from this cache.

```python
import sys
import math

print("math" in sys.modules)   # True
print(sys.modules["math"])     # <module 'math' (built-in)>
```

If a module cannot be found in any of these locations, Python raises `ModuleNotFoundError`. This is why a module saved in an unrelated folder cannot simply be imported without either moving it, adding its folder to `sys.path`, or installing it as a package.

## **Reloading a Module**

By default, Python loads a module only once per program run, no matter how many times `import` is written for it.

`counter.py`:

```python
# counter.py
print("This is from counter module")
```

`test.py`:

```python
# test.py
import counter
import counter
import counter
print("This is test module")
```

Output:

```
This is from counter module
This is test module
```

The module body runs only the first time. Subsequent `import counter` statements just reuse the already-loaded module from the internal cache (`sys.modules`). If the source file is changed after the first import, those changes are not automatically picked up.

### **Forcing a Reload with `importlib.reload()`**

The old `imp` module is deprecated since Python 3.4. The current, recommended way to force a reload is `importlib.reload()`:

```python
import importlib
import counter

importlib.reload(counter)
```

Calling `reload()` recompiles the module and re-executes its top-level code, replacing the objects inside the module's namespace with new ones. Important caveats:

- It does not update variables elsewhere in the program that already hold references to the old objects.
- It does not automatically reload the module's own dependencies; those must be reloaded separately.
- In practice it is mainly useful during interactive development — in a REPL or a Jupyter notebook.
- In Jupyter, the magic command `%autoreload 2` does this automatically on every cell run.

## **Inspecting a Module**

### **`dir()`**

`dir()` without arguments lists the names defined in the current namespace. `dir(module)` lists the names defined inside a given module.

```python
# test.py
x = 10
y = 20

def greet():
    print("Hello")

print(dir())
```

Output (order may vary slightly by Python version):

```
['__annotations__', '__builtins__', '__cached__', '__doc__', '__file__',
 '__loader__', '__name__', '__package__', '__spec__', 'greet', 'x', 'y']
```

```python
import mathutils
print(dir(mathutils))
```

Output:

```
['__builtins__', '__cached__', '__doc__', '__file__', '__loader__',
 '__name__', '__package__', '__spec__', 'add', 'product', 'x']
```

Python automatically adds a set of special attributes to every module (`__name__`, `__file__`, `__doc__`, and so on). These did not have to be written manually.

To see only the names defined by the user, filter out the dunders:

```python
import mathutils

public = [name for name in dir(mathutils) if not name.startswith("__")]
print(public)   # ['add', 'product', 'x']
```

### **`help()`**

`help()` prints the documentation for a module, function, or object, pulled from docstrings and signatures:

```python
import math
help(math)
```

This opens an interactive help viewer in the terminal. Press `q` to exit. You can also pass a specific name:

```python
help(math.sqrt)
```

### **Other Inspection Tools**

| Function | What it does |
|---|---|
| `type(obj)` | Returns the type of `obj`. |
| `getattr(obj, 'name')` | Returns `obj.name` as a value, useful for dynamic access. |
| `hasattr(obj, 'name')` | Returns `True` if `obj.name` exists. |
| `vars(obj)` | Returns the `__dict__` of `obj` as a dictionary. |
| `inspect.getsource(fn)` | Returns the source code of a function (from the `inspect` module). |
| `inspect.signature(fn)` | Returns the parameter signature of a function. |

## **The `__name__` Variable**

Every module has a built-in variable called `__name__`. Its value depends on how the file is being used:

- If the file is run directly with `python filename.py`, `__name__` is the string `"__main__"`.
- If the file is imported as a module from somewhere else, `__name__` is the module's actual name.

`greeter.py`:

```python
# greeter.py
def run():
    if __name__ == "__main__":
        print("The code executed as a program")
    else:
        print("The code executed as a module from some other program")

run()
```

`test.py`:

```python
# test.py
import greeter
greeter.run()
```

Running `greeter.py` directly:

```
$ python greeter.py
The code executed as a program
```

Running `test.py`, which imports `greeter`:

```
$ python test.py
The code executed as a module from some other program
The code executed as a module from some other program
```

The first line comes from the `import greeter` triggering `greeter.run()`. The second line is from the explicit `greeter.run()` call in `test.py`.

### **The `if __name__ == "__main__"` Pattern**

A very common pattern is to put the "only run when executed directly" code inside a guard. This keeps reusable code free of side effects when the file is imported.

```python
def main():
    print("Running the main logic")

if __name__ == "__main__":
    main()
```

When this file is imported elsewhere, `main()` does not run automatically. It only runs when the file itself is executed directly, for example with `python filename.py`.

Best practice: keep the block under `if __name__ == "__main__"` as small as possible. Move the actual logic into a `main()` function so it can be imported and tested cleanly.

### **The `__all__` Variable**

`__all__` is a list of strings defined at the top of a module that controls what `from module import *` brings in. Without `__all__`, `import *` brings in every name that does not start with an underscore. With `__all__`, only the listed names are exposed.

`mymodule.py`:

```python
# mymodule.py
__all__ = ["public_function", "PublicClass"]

def public_function():
    return "I am public"

def _helper():
    return "I am internal, not exported"

class PublicClass:
    pass

class _InternalClass:
    pass
```

In another file:

```python
from mymodule import *
print(public_function())   # I am public
print(PublicClass)         # <class 'mymodule.PublicClass'>
print(_helper())           # NameError: name '_helper' is not defined
```

`_helper` is still reachable as `mymodule._helper()`, but it is not pulled in by `import *`. `__all__` is the module author's way of declaring a public API and hiding helpers.

An empty `__all__ = []` is valid and means "export nothing with `import *`".

## **Packages: Grouping Modules Together**

A package is a folder that groups related modules together, so a large project can be organized into a tree instead of one flat pile of files.

```
mypackage/
    __init__.py
    stats.py
    strings.py
```

The presence of an `__init__.py` file historically marked a folder as a "regular" package. Since Python 3.3 (PEP 420), a folder without `__init__.py` can still be imported as an implicit "namespace package", but for ordinary application code, a regular package with `__init__.py` is still the common and predictable choice.

`__init__.py` can be:

- Empty — just a marker so the folder is treated as a regular package.
- Used to run package-level setup code the first time the package is imported.
- Used to re-export names so users can do `from package import thing` instead of `from package.submodule import thing`.
- Used to define `__all__` to control what `from package import *` exposes.

### **Importing from a Package**

```python
from mypackage import stats
from mypackage.stats import mean

import mypackage.strings
```

All three forms work. The second form is the most common in real code.

### **Relative Imports**

Inside a package, one module can import a sibling module using a relative import. A single dot (`.`) means "this package", and two dots (`..`) mean "the parent package".

```python
# inside mypackage/strings.py
from . import stats
from .stats import mean
```

Relative imports only work inside packages, not in a standalone script run directly. They make it easier to move or rename a package without rewriting absolute import paths everywhere inside it.

### **Regular Package vs Namespace Package**

| Type | How it is recognized | When to use it |
|---|---|---|
| Regular package | A directory with an `__init__.py` file | Most application code. Explicit, predictable, faster to import. |
| Namespace package | A directory without `__init__.py` (PEP 420) | When a single logical package is spread across multiple directories or distributions. |

For everyday work, write `__init__.py` in every package directory.

## **Running a Module as a Script**

Python can execute a module directly using the `-m` flag, which runs the module by its dotted name after searching `sys.path`, rather than by file path:

```
python -m http.server 8000
python -m venv myenv
python -m pip install requests
python -m unittest discover
```

Running a module this way still sets `__name__` to `"__main__"` for that module, so its `if __name__ == "__main__":` block runs.

Why use `python -m` instead of `python script.py`:

- The module is located through `sys.path`, so it benefits from the same import rules as a normal import. This is how `python -m pip` finds the pip that matches the current Python interpreter.
- It is the standard way to run tools that come with packages — for example `python -m http.server` or `python -m pytest`.

### **The `__main__.py` File**

If a package contains a file called `__main__.py`, then `python -m package_name` runs that file. This is how you turn a package into a runnable CLI tool.

```
mypackage/
    __init__.py
    __main__.py
    stats.py
```

`mypackage/__main__.py`:

```python
# mypackage/__main__.py
from . import stats

def main():
    print(stats.mean([1, 2, 3, 4, 5]))

main()
```

Running it:

```
$ python -m mypackage
3.0
```

`__main__.py` typically does not need its own `if __name__ == "__main__":` guard — when run via `python -m`, the file is the entry point and its top-level code runs directly.

## **The `math` Module**

`math` is a standard library module for common mathematical operations, useful for anything from basic arithmetic helpers to statistics and ML preprocessing work.

### **Common Functions**

```python
from math import sqrt, ceil, floor, fabs, log

print(sqrt(4))        # 2.0
print(sqrt(2))        # 1.4142135623730951
print(ceil(10.1))     # 11
print(floor(10.1))    # 10
print(fabs(-10.6))    # 10.6
print(log(100, 10))   # 2.0
```

What each one does:

- `sqrt(x)` — square root, returned as a float.
- `ceil(x)` — smallest integer greater than or equal to `x`.
- `floor(x)` — largest integer less than or equal to `x`.
- `fabs(x)` — absolute value, always returned as a float. The built-in `abs()` preserves the input type, but `fabs()` always returns a float.
- `log(x, base)` — logarithm of `x` in the given base.

### **Trigonometric Functions**

```python
from math import sin, cos, tan, radians, degrees

angle = radians(90)
print(sin(angle))             # 1.0
print(cos(angle))             # 6.123233995736766e-17 (essentially 0)
print(tan(radians(45)))       # 0.9999999999999999
print(degrees(3.141592653589793))   # 180.0
```

The trigonometric functions expect radians, not degrees. Use `radians()` and `degrees()` to convert.

### **Power, Constants, and a Note on Float Math**

```python
from math import pow, pi, e, isclose

print(pow(2, 10))      # 1024.0
print(pi)              # 3.141592653589793
print(e)               # 2.718281828459045

# floats are not exact; use isclose instead of ==
print(0.1 + 0.2 == 0.3)            # False
print(isclose(0.1 + 0.2, 0.3))     # True
```

## **The `random` Module**

`random` generates pseudo-random numbers and makes random selections. It is useful for simulations, shuffling data, sampling, and testing.

### **`random()`**

Returns a random float in the half-open range $[0.0, 1.0)$. The value $1.0$ is never returned.

```python
from random import random

for i in range(5):
    print(random())
```

Sample output:

```
0.5488135039273248
0.7151893663724195
0.6027633760716439
0.5448831829968969
0.4236547993389047
```

### **`randint(a, b)`**

Returns a random integer between `a` and `b`, with both ends included.

```python
from random import randint

for i in range(5):
    print(randint(1, 6))
```

Sample output:

```
3
6
1
4
2
```

This is the function to use to simulate a six-sided die.

### **`uniform(a, b)`**

Returns a random float between `a` and `b`. The endpoint order does not matter.

```python
from random import uniform

for i in range(5):
    print(uniform(1.0, 10.0))
```

### **`randrange(start, stop, step)`**

Returns a random number chosen from the range produced by `start`, `stop`, `step`, without including `stop`.

```python
from random import randrange

for i in range(5):
    print(randrange(1, 11, 2))
    # picks from 1, 3, 5, 7, 9
```

### **`choice(sequence)`**

Selects one random element from a non-empty sequence. Calling `choice` on an empty sequence raises `IndexError`.

```python
from random import choice

names = ["Tanvi", "Rohit", "Karan", "Om", "Harsha", "Meera"]
print(choice(names))
```

### **`choices()` — With Replacement**

Picks `k` elements from a sequence, with replacement (the same element can appear more than once). Weights are optional.

```python
from random import choices

names = ["Drishya", "Tanvi", "Rohit", "Karan"]
print(choices(names, k=3))
```

Sample output:

```
['Rohit', 'Drishya', 'Rohit']
```

Notice 'Rohit' appears twice — that is replacement.

Weighted example:

```python
from random import choices

print(choices(["win", "lose", "draw"], weights=[2, 1, 1], k=6))
```

Sample output:

```
['win', 'win', 'lose', 'win', 'draw', 'win']
```

The relative weights control the probability of each outcome.

### **`shuffle()` and `sample()`**

Two more `random` functions used often when preparing data:

```python
from random import shuffle, sample

marks = [45, 67, 89, 32, 78, 90]

shuffle(marks)
print(marks)        # list reordered in place, no return value

top_three = sample(marks, 3)
print(top_three)    # new list of 3 distinct elements
```

`shuffle()` modifies the list directly and returns `None`. `sample()` does not modify the original sequence — it returns a new list of unique, randomly chosen elements. This is useful when a random subset is needed without duplicates, such as a train/test split on a small custom dataset.

### **`seed()` for Reproducibility**

`random` numbers are produced by a deterministic algorithm. Setting a seed makes the sequence reproducible — essential for tests, debugging, and shared experiments.

```python
import random

random.seed(42)
print(random.randint(1, 100))   # 82

random.seed(42)
print(random.randint(1, 100))   # 82 again
```

Run the script on two different machines and you will get the same numbers.

### **Quick Reference: `random` Functions**

| Function | Returns |
|---|---|
| `random()` | Float in $[0.0, 1.0)$ |
| `randint(a, b)` | Integer in $[a, b]$ inclusive |
| `uniform(a, b)` | Float in $[a, b]$ |
| `randrange(start, stop, step)` | One value from the range |
| `choice(seq)` | One random element |
| `choices(seq, k=n, weights=...)` | `n` elements, with replacement |
| `sample(seq, k=n)` | `n` unique elements |
| `shuffle(list)` | Shuffles in place, returns `None` |
| `seed(n)` | Set the RNG seed for reproducibility |

## **Other Useful Standard Library Modules**

### **`os` — Operating System Interface**

```python
import os

print(os.getcwd())                  # current working directory
print(os.listdir("."))              # files in current folder
os.mkdir("new_folder")              # create a folder
os.rename("a.txt", "b.txt")         # rename a file
os.remove("b.txt")                  # delete a file
print(os.path.join("a", "b", "c"))  # 'a/b/c' (or 'a\\b\\c' on Windows)
```

### **`sys` — System-Specific Functions**

```python
import sys

print(sys.version)         # Python version string
print(sys.platform)       # 'linux', 'win32', 'darwin', etc.
print(sys.argv)            # command-line arguments as a list
sys.exit("Goodbye")        # exit the program with a message
```

### **`datetime` — Dates and Times**

```python
from datetime import datetime, date, timedelta

now = datetime.now()
print(now)                            # 2025-04-12 14:35:21.123456

today = date.today()
print(today.isoformat())              # 2025-04-12

tomorrow = today + timedelta(days=1)
print(tomorrow)                       # 2025-04-13
```

### **`json` — Reading and Writing JSON**

```python
import json

data = {"name": "Drishya", "age": 21, "scores": [88, 92, 79]}

text = json.dumps(data)               # Python object -> JSON string
print(text)
# {"name": "Drishya", "age": 21, "scores": [88, 92, 79]}

loaded = json.loads(text)             # JSON string -> Python object
print(loaded["name"])                 # Drishya

with open("data.json", "w") as f:
    json.dump(data, f, indent=2)      # save to file

with open("data.json") as f:
    restored = json.load(f)           # read from file
print(restored)
```

### **`collections` — Specialised Containers**

```python
from collections import Counter, defaultdict, namedtuple

c = Counter("abracadabra")
print(c)                        # Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
print(c.most_common(2))         # [('a', 5), ('b', 2)]

d = defaultdict(int)
for letter in "banana":
    d[letter] += 1
print(dict(d))                  # {'b': 1, 'a': 3, 'n': 2}

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y)                 # 3 4
```

### **`itertools` — Iterator Building Blocks**

```python
import itertools

counter = itertools.count(start=1, step=2)
print(next(counter), next(counter), next(counter))   # 1 3 5

cycler = itertools.cycle(["A", "B", "C"])
print(next(cycler), next(cycler), next(cycler))       # A B C

print(list(itertools.combinations([1, 2, 3], 2)))
# [(1, 2), (1, 3), (2, 3)]

print(list(itertools.permutations([1, 2, 3], 2)))
# [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
```

### **`statistics` — Basic Statistics**

```python
import statistics as stats

data = [88, 92, 79, 95, 84, 90, 88]
print(stats.mean(data))     # 88.0
print(stats.median(data))   # 88
print(stats.mode(data))     # 88
print(stats.stdev(data))    # 5.477225575051661
```

## **Installing and Using Third-Party Modules**

Modules that are not part of the standard library are installed using `pip`, Python's package installer, and then imported the same way as any built-in module:

```
pip install requests
```

```python
import requests

response = requests.get("https://api.github.com")
print(response.status_code)   # 200
```

For real projects, third-party modules are usually installed inside a virtual environment rather than system-wide, so that different projects can depend on different, isolated sets of package versions without conflicting with each other:

```
python -m venv .venv
source .venv/bin/activate     # on Windows: .venv\Scripts\activate
pip install requests pandas
```

## **Case Study 1: A Reusable Pricing Module**

**Scenario:** You are building a small e-commerce system. Three scripts all need to compute the final price of a cart, applying tax and discount rules. Instead of duplicating the logic, put it in a module.

`pricing.py`:

```python
# pricing.py
DEFAULT_TAX_RATE = 0.18          # 18% GST
DEFAULT_DISCOUNT = 0.10          # 10% festival discount

def apply_discount(subtotal, rate=DEFAULT_DISCOUNT):
    """Return subtotal after applying a discount rate in [0, 1]."""
    if not 0 <= rate <= 1:
        raise ValueError("discount rate must be between 0 and 1")
    return subtotal * (1 - rate)

def add_tax(amount, rate=DEFAULT_TAX_RATE):
    """Return amount plus tax."""
    if rate < 0:
        raise ValueError("tax rate cannot be negative")
    return amount * (1 + rate)

def total_price(subtotal, discount=DEFAULT_DISCOUNT, tax=DEFAULT_TAX_RATE):
    """Compute the final price in one call."""
    after_discount = apply_discount(subtotal, discount)
    return add_tax(after_discount, tax)

def format_inr(amount):
    """Format a number as Indian Rupee currency string."""
    return f"Rs. {amount:,.2f}"
```

`checkout.py`:

```python
# checkout.py
from pricing import total_price, format_inr, DEFAULT_TAX_RATE

cart = [
    ("Notebook", 120.00, 3),
    ("Pen", 20.00, 5),
]

subtotal = sum(price * qty for _, price, qty in cart)
print("Subtotal:        ", format_inr(subtotal))
print("Tax rate:        ", f"{DEFAULT_TAX_RATE * 100:.0f}%")
print("Final total:     ", format_inr(total_price(subtotal)))

# Custom rules per call
vip_total = total_price(subtotal, discount=0.20, tax=0.12)
print("VIP total:       ", format_inr(vip_total))
```

Running `checkout.py`:

```
Subtotal:         Rs. 460.00
Tax rate:         18%
Final total:      Rs. 488.72
VIP total:        Rs. 412.16
```

Walking through the design:

- `pricing.py` has no top-level print or input calls, so importing it has no side effects.
- Constants like `DEFAULT_TAX_RATE` are module-level so users can read them but they remain the single source of truth.
- Each function is small, single-purpose, and reusable.
- The script uses `from pricing import total_price, format_inr` — explicit and easy to read.

## **Case Study 2: A Logger Utility Module**

**Scenario:** Your project has many scripts that all need to print timestamped status messages. Instead of copy-pasting `print(f"[{datetime.now()}] ...")` everywhere, build a small logger module.

`logger.py`:

```python
# logger.py
from datetime import datetime

_LEVELS = {"DEBUG": 10, "INFO": 20, "WARN": 30, "ERROR": 40}
_current_level = _LEVELS["INFO"]

def set_level(name):
    """Set the minimum level that will be printed."""
    global _current_level
    if name not in _LEVELS:
        raise ValueError(f"unknown level: {name}")
    _current_level = _LEVELS[name]

def _emit(level, message):
    if _LEVELS[level] < _current_level:
        return
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{stamp} [{level}] {message}")

def debug(msg):   _emit("DEBUG", msg)
def info(msg):    _emit("INFO",  msg)
def warn(msg):    _emit("WARN",  msg)
def error(msg):   _emit("ERROR", msg)
```

`app.py`:

```python
# app.py
from logger import info, warn, error, set_level

set_level("INFO")

info("application starting")
warn("disk space below 10%")
error("could not connect to database")
info("retrying in 5 seconds")
```

Running `app.py`:

```
2025-04-12 14:35:21 [INFO] application starting
2025-04-12 14:35:21 [WARN] disk space below 10%
2025-04-12 14:35:21 [ERROR] could not connect to database
2025-04-12 14:35:21 [INFO] retrying in 5 seconds
```

In a larger project, you would replace `print` with Python's built-in `logging` module, but the structure here — a module that owns configuration (`set_level`) and exposes simple functions — is exactly the same.

## **Case Study 3: A Configuration Module**

**Scenario:** Scripts need to read settings (database URL, feature flags, API keys) without hardcoding them. A small config module reads from environment variables with safe defaults.

`config.py`:

```python
# config.py
import os

def _get_bool(name, default):
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")

# Database
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = int(os.environ.get("DB_PORT", "5432"))
DB_NAME = os.environ.get("DB_NAME", "appdb")

# Feature flags
FEATURE_NEW_UI    = _get_bool("FEATURE_NEW_UI", False)
FEATURE_BETA_API  = _get_bool("FEATURE_BETA_API", True)

# Derived
def database_url():
    return f"postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}"

def summary():
    return {
        "db": database_url(),
        "new_ui": FEATURE_NEW_UI,
        "beta_api": FEATURE_BETA_API,
    }
```

`main.py`:

```python
# main.py
from config import database_url, summary, FEATURE_NEW_UI

print("Connecting to:", database_url())
print("Summary:", summary())

if FEATURE_NEW_UI:
    print("Loading the new UI...")
else:
    print("Loading the classic UI...")
```

Running with no env vars set:

```
Connecting to: postgresql://localhost:5432/appdb
Summary: {'db': 'postgresql://localhost:5432/appdb', 'new_ui': False, 'beta_api': True}
Loading the classic UI...
```

Running with overrides:

```
$ FEATURE_NEW_UI=1 python main.py
Connecting to: postgresql://localhost:5432/appdb
Summary: {'db': 'postgresql://localhost:5432/appdb', 'new_ui': True, 'beta_api': True}
Loading the new UI...
```

This pattern — one module that owns all environment-driven configuration — is standard in real web services and CLI tools.

## **Case Study 4: A Validation Module for User Input**

**Scenario:** A web form handler receives strings from user input. You need a small set of validator functions that can be reused across multiple endpoints. Put them in a module.

`validators.py`:

```python
# validators.py
import re

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_RE = re.compile(r"^\+?\d{10,15}$")

class ValidationError(ValueError):
    pass

def require_text(value, field, max_length=200):
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field} is required")
    if len(value) > max_length:
        raise ValidationError(f"{field} must be at most {max_length} chars")
    return value.strip()

def is_email(value):
    return bool(EMAIL_RE.match(value or ""))

def is_phone(value):
    return bool(PHONE_RE.match(value or ""))

def require_email(value, field="email"):
    if not is_email(value):
        raise ValidationError(f"{field} is not a valid email")
    return value

def require_age(value, field="age", minimum=0, maximum=120):
    try:
        age = int(value)
    except (TypeError, ValueError):
        raise ValidationError(f"{field} must be an integer")
    if not minimum <= age <= maximum:
        raise ValidationError(f"{field} must be between {minimum} and {maximum}")
    return age
```

`signup.py`:

```python
# signup.py
from validators import (
    require_text, require_email, require_age, ValidationError
)

def signup(payload):
    name  = require_text(payload.get("name"), "name")
    email = require_email(payload.get("email"))
    age   = require_age(payload.get("age"))
    return {"name": name, "email": email, "age": age}

if __name__ == "__main__":
    test_payloads = [
        {"name": "Drishya", "email": "d@x.com", "age": "21"},
        {"name": "   ",      "email": "bad",     "age": "999"},
        {"name": "Om",       "email": "o@x.com", "age": "abc"},
    ]
    for p in test_payloads:
        try:
            print("OK:", signup(p))
        except ValidationError as e:
            print("REJECTED:", e)
```

Running `signup.py`:

```
OK: {'name': 'Drishya', 'email': 'd@x.com', 'age': 21}
REJECTED: name is required
REJECTED: age must be between 0 and 120
```

Putting validators in a module means every form handler, every test, and every CLI subcommand can reuse the same logic. Notice the file also defines a custom `ValidationError` class — that becomes a useful type to catch across the whole app.

## **Case Study 5: An HTTP Client Wrapper Module**

**Scenario:** Your service calls several external REST APIs. You want one place to handle timeouts, retries, and JSON parsing so individual scripts stay simple.

`http_client.py`:

```python
# http_client.py
import time
import requests

DEFAULT_TIMEOUT = 10
MAX_RETRIES = 3
RETRYABLE_STATUS = {500, 502, 503, 504}

class HTTPError(Exception):
    def __init__(self, status, body, url):
        super().__init__(f"{status} on {url}: {body[:120]}")
        self.status = status
        self.body = body
        self.url = url

def get_json(url, params=None, timeout=DEFAULT_TIMEOUT, retries=MAX_RETRIES):
    """GET a URL and return parsed JSON, with retries on transient errors."""
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, params=params, timeout=timeout)
        except requests.RequestException as e:
            last_error = e
            time.sleep(0.5 * attempt)
            continue

        if response.status_code == 200:
            return response.json()

        if response.status_code in RETRYABLE_STATUS:
            last_error = HTTPError(response.status_code, response.text, url)
            time.sleep(0.5 * attempt)
            continue

        raise HTTPError(response.status_code, response.text, url)

    raise RuntimeError(f"giving up after {retries} attempts: {last_error}")
```

`weather.py`:

```python
# weather.py
from http_client import get_json, HTTPError

def fetch_weather(city):
    url = "https://wttr.in/" + city
    params = {"format": "j1"}
    data = get_json(url, params=params)
    return data

if __name__ == "__main__":
    try:
        result = fetch_weather("Mumbai")
        print("Got data, top-level keys:", list(result.keys()))
    except HTTPError as e:
        print("API error:", e)
    except RuntimeError as e:
        print("Network problem:", e)
```

What this design gives you:

- Every call site gets the same retry policy, timeout, and error type without repeating the logic.
- The custom `HTTPError` carries the status code, body, and URL — useful for logging and metrics.
- Swapping the HTTP library (say, from `requests` to `httpx`) only changes one file.

## **Case Study 6: A Real Project Package Layout**

**Scenario:** You are turning a small project into something you can install and reuse. Here is a typical, production-ready layout.

```
myproject/
├── pyproject.toml
├── README.md
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── __main__.py
│       ├── config.py
│       ├── pricing.py
│       └── utils/
│           ├── __init__.py
│           ├── logger.py
│           └── validators.py
└── tests/
    ├── test_pricing.py
    └── test_validators.py
```

`src/myproject/__init__.py`:

```python
# src/myproject/__init__.py
"""myproject: small e-commerce pricing toolkit."""

__version__ = "0.1.0"

from .pricing import total_price, apply_discount, add_tax, format_inr
from .config import database_url, summary

__all__ = [
    "__version__",
    "total_price", "apply_discount", "add_tax", "format_inr",
    "database_url", "summary",
]
```

`src/myproject/__main__.py`:

```python
# src/myproject/__main__.py
from . import __version__
from .pricing import format_inr, total_price

def main():
    print(f"myproject {__version__}")
    subtotal = 460.0
    print("Final total:", format_inr(total_price(subtotal)))

if __name__ == "__main__":
    main()
```

Installing it (from the project root, with a virtual environment active):

```
pip install -e .
```

Running it as a script:

```
$ python -m myproject
myproject 0.1.0
Final total: Rs. 488.72
```

Walking through the design:

- `src/` layout keeps project source code separate from the project root, which avoids accidentally importing a half-installed version.
- `__init__.py` re-exports the public API at the top level, so users can do `from myproject import total_price` instead of `from myproject.pricing import total_price`.
- `__all__` makes the public API explicit.
- `__main__.py` turns the package into a runnable CLI tool via `python -m myproject`.
- The inner `utils/` subpackage shows that packages can contain other packages — relative imports like `from .utils import logger` work from anywhere inside `myproject/`.

## **Common Gotchas in Production**

### **Shadowing a Standard Library Name**

Naming a personal file the same as a standard library module, for example `random.py` or `math.py`, will shadow the real module and break any code that tries to import the real one, because Python finds the local file first.

```
project/
    math.py          # your file — shadows the real math module
    script.py        # `import math` now imports your file, not the real one
```

If you ever import something and the behaviour is "wrong but not quite broken", check whether a local file with the same name exists in the project folder.

### **Wildcard Imports Overwriting Names**

```python
from math import *
pi = "I am a pie recipe"

print(pi)        # "I am a pie recipe"  -- your local pi won
```

The wildcard import brings in `pi = 3.14...` from the `math` module, but only as a binding step. If you rebind `pi` after the import, your local value wins. The reverse is also true: if you bind `pi` first, then `from math import *` will silently overwrite it. This is the kind of bug that is hard to spot, which is why explicit imports are preferred.

### **Circular Imports**

When module A imports module B and module B imports module A, you can get an `ImportError` at startup. The fix is usually to move the shared code into a third module that both A and B depend on.

`models.py` and `views.py` both need a `User` class. If `models.py` does `from views import render_user` at the top, and `views.py` does `from models import User` at the top, the import order decides which one fails. Instead:

- Put `User` in `models.py` (no top-level import of `views`).
- Put `render_user` in `views.py` and import `User` lazily inside the function:

```python
# views.py
def render_user(user):
    from models import format_phone   # local import: safe
    return format_phone(user.phone)
```

Local imports inside functions are a clean way out of circular dependencies.

### **Using `eval` on Untrusted Input**

`eval()` parses and runs any Python expression, including code that reads files, makes network calls, or deletes things. Never pass user input to `eval`. The safe replacement for parsing literal data structures is `ast.literal_eval`:

```python
import ast

data = ast.literal_eval("[1, 2, 3]")      # OK: real list
print(data)                                # [1, 2, 3]

bad = ast.literal_eval("__import__('os').system('rm -rf /')")
# ValueError: malformed node or string
```

`ast.literal_eval` only accepts literal Python structures — numbers, strings, lists, dicts, tuples, booleans, and `None`. Anything else raises `ValueError`.

### **Mutable Default Arguments**

This is a classic module-level function trap. Default argument values are evaluated once at function definition time, not on every call. So if you write:

```python
def add_item(item, bucket=[]):
    bucket.append(item)
    return bucket
```

The same `bucket` list is shared across every call that uses the default:

```python
print(add_item("a"))   # ['a']
print(add_item("b"))   # ['a', 'b']
print(add_item("c"))   # ['a', 'b', 'c']
```

The fix is to use `None` as the default and create a new container inside the function:

```python
def add_item(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

This bug is a property of how Python evaluates default arguments — it has nothing to do with modules directly, but it shows up the moment you start defining functions in your own modules.

### **Top-Level Side Effects**

If a module prints, opens a file, or connects to a database at import time, every script that imports it pays that cost — including scripts that just want one helper function. Keep the top level of a module limited to definitions (functions, classes, constants). Move any work that produces output or talks to the outside world into functions, and call them from `if __name__ == "__main__":` or from the importing script.

## **Best Practices for Modules**

- **Name modules with lowercase letters and underscores.** `my_helpers.py`, not `MyHelpers.py`.
- **Keep one clear responsibility per module.** A file called `math_helpers.py` should only contain math helpers.
- **Put `if __name__ == "__main__":` at the bottom** of any file that is both a script and an importable module, and call a `main()` function from inside it.
- **Define `__all__` in modules** that users might `import *` from. It documents your public API.
- **Prefer `import module` over `from module import *`.** Wildcards hide where names came from and make debugging harder.
- **Avoid side effects at import time.** Top-level code should mostly define functions, classes, and constants.
- **Group imports at the top of the file** in this order: standard library, then third-party, then your own. Separate the groups with a blank line.

```python
# standard library
import os
import sys

# third-party
import requests

# your own
import mathutils
```

- **Use type hints and module-level docstrings** so tools like IDEs and `help()` can show useful information.
- **Keep modules small and focused.** A module that is thousands of lines is usually a sign that it should be split into a package.
- **Document the public API** at the top of the module with a short docstring, and add docstrings to every public function and class.

## **Built-in Special Module Attributes**

Every module object has a set of attributes that Python attaches automatically.

| Attribute | What it holds |
|---|---|
| `__name__` | The module's name. `"__main__"` if run directly. |
| `__file__` | The path to the module's `.py` file. May not exist for built-in modules. |
| `__doc__` | The module's docstring, or `None`. |
| `__package__` | The parent package name, or `""` for top-level modules. |
| `__loader__` | The loader object that loaded the module. |
| `__spec__` | The module spec — used by the import system. |
| `__cached__` | The path to the compiled `.pyc` file. |
| `__dict__` | The module's namespace as a regular dictionary. |

Quick demo:

```python
import math

print(math.__name__)         # math
print(math.__doc__[:60])
print(math.__file__)         # /usr/lib/python3.11/math.py
```

## **Quick Reference Summary**

### **Import Cheat Sheet**

| Want to... | Use |
|---|---|
| Import a whole module | `import math` |
| Import several modules | `import math, random` |
| Use a short name | `import numpy as np` |
| Import one name | `from math import sqrt` |
| Import several names | `from math import sqrt, pi` |
| Import with a new name | `from math import sqrt as root` |
| Import everything public | `from math import *` |
| Reload a module in a REPL | `from importlib import reload; reload(mymodule)` |

### **`dir()` and Inspection**

| Function | Purpose |
|---|---|
| `dir()` | Names in the current scope. |
| `dir(module)` | Names in a module. |
| `type(obj)` | Type of an object. |
| `help(obj)` | Built-in help viewer. |
| `getattr(obj, "name")` | Dynamic attribute access. |
| `hasattr(obj, "name")` | Test if attribute exists. |

### **`math` Highlights**

| Function | Returns |
|---|---|
| `sqrt(x)` | $\sqrt{x}$ |
| `pow(x, y)` | $x^y$ as a float |
| `ceil(x)` | Smallest integer $\ge x$ |
| `floor(x)` | Largest integer $\le x$ |
| `fabs(x)` | $\lvert x \rvert$ as a float |
| `log(x, base)` | $\log_{\text{base}}(x)$ |
| `sin(x)`, `cos(x)`, `tan(x)` | Trig (radians) |
| `radians(x)`, `degrees(x)` | Unit conversion |
| `pi`, `e` | Constants |
| `isclose(a, b)` | Safe float comparison |

### **`random` Highlights**

| Function | Returns |
|---|---|
| `random()` | Float in $[0.0, 1.0)$ |
| `randint(a, b)` | Integer in $[a, b]$ inclusive |
| `uniform(a, b)` | Float in $[a, b]$ |
| `randrange(start, stop, step)` | One value from the range |
| `choice(seq)` | One random element |
| `choices(seq, k=n)` | `n` elements, with replacement |
| `sample(seq, k=n)` | `n` unique elements |
| `shuffle(list)` | Shuffles in place, returns `None` |
| `seed(n)` | Set the RNG seed for reproducibility |

### **Module-Related Variables**

| Variable | Meaning |
|---|---|
| `__name__` | `"__main__"` if run directly, else the module's name. |
| `__file__` | Path to the source file. |
| `__doc__` | Module docstring. |
| `__all__` | List of public names for `import *`. |
| `__package__` | Parent package name. |
| `sys.modules` | Dict of all loaded modules. |
| `sys.path` | List of directories searched on import. |

### **Module vs Package vs Library vs Framework**

| Term | Definition | Example |
|---|---|---|
| Module | A single `.py` file. | `mathutils.py` |
| Package | A directory with `__init__.py` plus modules. | `mypackage/` |
| Library | A reusable collection of modules/packages. | `numpy`, `requests` |
| Framework | A library that calls your code. | `django`, `flask` |

## **Practice and Next Steps**

Small exercises to lock the concepts in:

- Create a module called `geometry.py` with functions `area_rectangle`, `area_circle`, and `area_triangle`. Import it from a separate script and call all three. Add a docstring to the module and to each function.
- Add a function called `_clean_input` to `geometry.py`. Use `__all__` so that `from geometry import *` does not expose it.
- Write a module called `passwords.py` with a function `generate(length, use_digits, use_symbols)`. Use `random.choice` inside a loop. Add an `if __name__ == "__main__":` block that prints three sample passwords.
- Print `dir(math)` and count how many names start with an underscore versus letters. Use a list comprehension to print only the public ones.
- Create a small package called `utilities` with `__init__.py`, `math_helpers.py`, and `string_helpers.py`. Import the package from a script in the parent folder and call a function from each submodule.
- Build the `pricing` module from Case Study 1, then add a `__main__.py` so you can run `python -m pricing` to print a sample total.
- In a Python REPL, import `math`, then change the value of `math.pi` with `math.pi = 3`. Restart the REPL and observe that the change did not persist. This shows that modules are normal objects whose state is per program run.
- Use `random.seed(7)` and generate five numbers with `random.random()`. Run the script twice and confirm the output is identical.
- On purpose, create a local `random.py` in your project and try to `import random` from a script in the same folder. Notice the failure, then rename your file and re-run.
- Add `import sys; print(sys.path)` to a script. Run it from a different working directory and compare the output. Notice the `''` entry at the start.
- Use `python -m http.server 8000` to start a static file server in any folder, then open `http://localhost:8000` in a browser. Use this as a sanity check that `-m` works on your machine.

After these, the natural next topics are: third-party packages with `pip` and `pyproject.toml`, virtual environments in depth, and packaging your own project so other people can `pip install` it.
