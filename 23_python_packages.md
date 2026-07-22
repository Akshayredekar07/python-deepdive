# **Python Packages**

## **What Is a Package**

A package is a way of grouping related modules together into a single unit, so that a large project does not end up as one giant folder of unrelated `.py` files. In simple terms, a package is a folder or directory that contains Python modules, plus some way of telling Python that the folder should be treated as a package rather than just an ordinary folder.

In the traditional (and still most common) form, any folder that contains an `__init__.py` file is treated by Python as a package. This is called a regular package. A package can also contain other packages inside it, which are called sub-packages, allowing a project to be organized as a tree of related modules instead of a single flat namespace.

The whole idea — taking related code, grouping it into a folder, and giving that folder its own name — is sometimes described as an encapsulation mechanism. It hides the internal file layout of a feature behind one clean name that the rest of the program imports from.

### **Why Packages Are Useful**

- **Resolves naming conflicts.** Two different packages can each have a module called `utils.py` without clashing, because they are accessed as `package_a.utils` and `package_b.utils`.
- **Uniquely identifies components.** A function's full dotted path, such as `myapp.reports.pdf.generate`, tells you exactly where that function lives without any ambiguity.
- **Improves modularity.** Packages structure code into smaller, reusable, focused pieces, so a feature can be developed, tested, and reused independently of the rest of the application.
- **Enables distribution.** Once code is inside a package, it can be packaged with `pyproject.toml` and shared via `pip` or published to PyPI.
- **Supports versioning and dependencies.** A package is the natural unit that carries its own version number, its own dependencies, and its own entry points.

## **Package Structure Example**

A minimal package looks like this on disk:

```
mathpack/
    __init__.py
    arithmetic.py
    geometry.py
```

`arithmetic.py`:

```python
# mathpack/arithmetic.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
```

`geometry.py`:

```python
# mathpack/geometry.py
import math

def area_circle(radius):
    return math.pi * radius * radius

def area_rectangle(length, width):
    return length * width
```

`__init__.py` can be left completely empty. Its presence alone is what makes Python treat the `mathpack` folder as a package.

Using the package from another file in the same project:

```python
# main.py
from mathpack import arithmetic
from mathpack.geometry import area_circle

print(arithmetic.add(10, 5))
print(area_circle(2))
```

Running `main.py`:

```
15
12.566370614359172
```

Walking through this:

- `from mathpack import arithmetic` imports the `arithmetic` module that lives inside the `mathpack` package. The module is then accessed as `arithmetic.add(...)`.
- `from mathpack.geometry import area_circle` reaches one level deeper, directly into the `geometry` module, and imports just the `area_circle` function so it can be called without any prefix.
- Even though the package was not "installed", importing works because `mathpack/` lives in the same directory as `main.py`, and the current directory is the first entry on `sys.path`.

## **The Role of `__init__.py`**

`__init__.py` runs automatically the first time its package (or anything inside it) is imported. It can be empty, or it can be used for several common purposes:

- Running package-level setup code, such as configuring logging defaults or reading a config file.
- Re-exporting selected functions from sub-modules, so users can write `from mathpack import add` instead of `from mathpack.arithmetic import add`.
- Defining `__all__` to control exactly what gets imported when someone writes `from mathpack import *`.
- Declaring the package's public version string (`__version__`).

### **Re-exporting Inside `__init__.py`**

`mathpack/__init__.py`:

```python
# mathpack/__init__.py
"""mathpack: small arithmetic and geometry helpers."""

__version__ = "0.1.0"

from .arithmetic import add, subtract
from .geometry import area_circle, area_rectangle

__all__ = [
    "__version__",
    "add", "subtract",
    "area_circle", "area_rectangle",
]
```

With this `__init__.py` in place, callers can do:

```python
from mathpack import add, area_circle

print(add(2, 3))
print(area_circle(2))
```

`__all__` is a list of strings naming the public members of the package. It only affects `from mathpack import *`; explicit imports like `from mathpack import add` still work regardless of what is or is not listed in `__all__`.

### **Why Re-export?**

Without re-exports, every user of your package has to know which sub-module each function lives in. With re-exports in `__init__.py`, the top-level import path stays stable even if you later move a function from `arithmetic.py` to a different sub-module. Internal refactors stay internal.

### **What Happens at Import Time**

When something does `import mathpack` for the first time, Python:

1. Searches `sys.path` for a folder named `mathpack`.
2. Runs the file `mathpack/__init__.py` top to bottom.
3. Binds whatever the `__init__.py` file left in the module's namespace under the name `mathpack`.

If `__init__.py` is empty, `import mathpack` succeeds but gives you a module with almost nothing in it. You would then access sub-modules as `mathpack.arithmetic` or import them separately.

## **Sub-Packages**

A package can contain other packages nested inside it, forming a tree structure that mirrors how a larger application's features are organized.

```
ecommerce/
    __init__.py
    orders/
        __init__.py
        create.py
        cancel.py
    payments/
        __init__.py
        gateway.py
        refunds.py
```

Importing from a nested sub-package uses the full dotted path:

```python
from ecommerce.orders import create
from ecommerce.payments.gateway import charge_card

create.new_order(user_id=101, item="Laptop")
charge_card(amount=55000, currency="INR")
```

Each folder in the chain — `ecommerce`, `ecommerce/orders`, and `ecommerce/payments` — needs its own `__init__.py` to be treated as a regular package. If any level in that chain is missing `__init__.py`, Python 3.3 and later will still often import it as an implicit namespace package, but that folder will then behave slightly differently (see the namespace package section below). For ordinary application code, adding `__init__.py` everywhere is the more predictable choice.

## **Absolute vs Relative Imports**

Inside a package, modules can import from each other in two ways.

### **Absolute Imports**

The full dotted path from a top-level package, regardless of where the importing file lives:

```python
# ecommerce/orders/create.py
from ecommerce.payments.gateway import charge_card
from ecommerce.orders import cancel
```

Absolute imports are explicit and easy to read. They work no matter where the importing file is in the package tree.

### **Relative Imports**

A relative import uses dots that mean "this package" (`.`) or "the parent package" (`..`):

```python
# ecommerce/orders/create.py
from . import cancel                  # sibling module in the same package
from ..payments.gateway import charge_card   # module in the parent package
```

The leading single dot is "the current package" (`ecommerce.orders`). The double dot is "the parent package" (`ecommerce`).

Relative imports only work inside a package — they fail in a script that is run directly. They are useful when:

- The package might be renamed or moved. Only the external import paths change; the internal relative imports stay the same.
- You want to make the package clearly self-contained.

### **Which to Prefer**

In modern Python codebases, absolute imports are the default choice because they are easier to read and to search. Relative imports are fine for tightly coupled sub-modules, especially inside the same sub-package.

## **Namespace Packages**

Since Python 3.3 (PEP 420), a folder without an `__init__.py` file can still be imported as a package. This is called an implicit namespace package. Unlike a regular package, a namespace package is not tied to a single physical directory; it can be assembled from multiple directories on `sys.path` that all share the same package name.

```
partA/
    myns/
        modulea.py

partB/
    myns/
        moduleb.py
```

Here, neither `myns` folder contains an `__init__.py`. If both `partA` and `partB` are on `sys.path`, then `myns` becomes a single namespace package that combines contents from both locations:

```python
import sys
sys.path.append("partA")
sys.path.append("partB")

import myns.modulea
import myns.moduleb
```

Namespace packages are mainly useful for splitting a large project's code across multiple separately installed distributions that all contribute to the same top-level name. For example, large frameworks sometimes ship optional plugin packages that all install under the same top-level name.

For a normal, self-contained application or library, a regular package with explicit `__init__.py` files is simpler to reason about and is the more common choice.

### **Regular Package vs Namespace Package**

| Aspect | Regular package | Namespace package |
|---|---|---|
| Marker | `__init__.py` present | No `__init__.py` |
| First available in | Python 1.5 | Python 3.3 (PEP 420) |
| Location | Single physical directory | Can span multiple directories or even multiple distributions |
| Setup code at import | Runs in `__init__.py` | Nothing runs; the package is just a virtual namespace |
| Typical use | Most applications and libraries | Plugins, framework extensions, very large codebases |

## **How Python Locates Packages**

When `import package.module` runs, Python searches every directory listed in `sys.path` for a folder named `package`. `sys.path` is built from, in order:

1. The directory containing the script being run (or the current directory in interactive mode).
2. The `PYTHONPATH` environment variable, if it is set.
3. The standard library directories bundled with Python.
4. The `site-packages` directories where pip-installed third-party packages live.

```python
import sys
for path in sys.path:
    print(path)
```

This is why a package that is not on `sys.path`, and has not been installed with `pip`, cannot simply be imported from an unrelated project folder without extra steps, such as adding its parent folder to `sys.path` manually or installing it properly.

## **Packages vs Modules vs Libraries vs Frameworks**

| Term | Definition | Import form | Example |
|---|---|---|---|
| Module | A single `.py` file. | `import module` | `mathutils.py` |
| Package | A directory with `__init__.py` plus modules and sub-packages. | `import package.module` | `mathpack/` |
| Library | A reusable collection of modules and/or packages, usually distributed via `pip`. | `import library` | `requests`, `numpy` |
| Framework | A library that calls your code (inversion of control). | `import framework` | `django`, `flask` |

A package is just the unit of organization used to build libraries and frameworks.

## **`__init__.py` Patterns Used in Real Codebases**

### **Expose the Version**

```python
# mypackage/__init__.py
__version__ = "1.4.2"
```

Users can do `import mypackage; print(mypackage.__version__)` to check what is installed. Many tools (including setuptools and `pip show`) read this value.

### **Lazy Imports for Speed**

If importing a sub-module is slow because it loads large data files or heavy C extensions, you can defer the import until the user actually calls the function:

```python
# mypackage/__init__.py
__version__ = "0.1.0"

def heavy_function(*args, **kwargs):
    from mypackage._heavy import heavy_function as _impl
    return _impl(*args, **kwargs)
```

The first time `heavy_function` is called, the real implementation is imported. The rest of the package stays light at import time.

### **Configure Logging Once**

```python
# mypackage/__init__.py
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
```

Adding a `NullHandler` is the standard advice for libraries: it prevents "No handlers could be found" warnings without forcing a particular logging configuration on the user.

### **Re-export Everything Public**

```python
# mypackage/__init__.py
from .core import Engine, run
from .helpers import format_result, format_error
from .errors import PackageError, ConfigError

__all__ = [
    "Engine", "run",
    "format_result", "format_error",
    "PackageError", "ConfigError",
    "__version__",
]
```

This pattern — small re-export `__init__.py` plus actual implementation in sub-modules — is the most common shape for a published library.

## **Project Layouts: Flat vs `src/`**

There are two common ways to lay out a project that will be packaged.

### **Flat Layout**

```
myproject/
    pyproject.toml
    README.md
    mypackage/
        __init__.py
        module_a.py
        module_b.py
    tests/
        test_module_a.py
```

The package directory sits directly at the project root, next to `pyproject.toml` and `README.md`.

### **`src/` Layout**

```
myproject/
    pyproject.toml
    README.md
    src/
        mypackage/
            __init__.py
            module_a.py
            module_b.py
    tests/
        test_module_a.py
```

The package directory is moved one level deeper, inside a `src/` folder.

### **Why the `src/` Layout Is Recommended for Libraries**

The `src/` layout solves a real bug that catches people with the flat layout. Because Python puts the current working directory at the top of `sys.path`, running tests from the project root with the flat layout makes Python find the local source files first — not the installed version. That means:

- Code that depends on `pip install -e .` actually being done will silently pass tests against a half-installed state.
- Configuration mistakes in `pyproject.toml` (wrong package name, missed `package_dir`) may not show up at all, because tests use the in-tree source anyway.

With the `src/` layout, the local source is in `src/`, which is not on `sys.path` by default. Tests can only import the package if it has actually been installed (for example with `pip install -e .`). This forces you to catch packaging bugs early.

### **When to Use Which**

| Layout | Best for |
|---|---|
| Flat | Small scripts, weekend projects, learning exercises, single-file utilities. |
| `src/` | Anything that will be packaged, distributed, shared, or installed by other people. |

The Packaging Authority and the official Python Packaging User Guide both recommend `src/` for any non-trivial project.

## **Building Distributable Packages with `pyproject.toml`**

Once a package is meant to be shared, published, or reused across multiple projects, it is turned into a proper installable distribution using `pyproject.toml`, which has become the standard, tool-agnostic configuration file for Python packaging.

### **The Three Main Tables**

`pyproject.toml` has three top-level tables you should know:

- `[build-system]` — strongly recommended. Declares which build backend to use (`setuptools`, `hatchling`, `flit`, `poetry`) and which packages that backend needs to do its job.
- `[project]` — the PEP 621 metadata table. Holds the package name, version, description, dependencies, Python version, authors, and more.
- `[tool.*]` — tool-specific configuration. For example `[tool.setuptools]` configures setuptools, `[tool.pytest]` configures pytest, `[tool.black]` configures Black.

### **A Minimal `pyproject.toml`**

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "mathpack"
version = "0.1.0"
description = "A small demo package for arithmetic and geometry helpers"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"},
]
keywords = ["math", "demo", "tutorial"]
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
dependencies = []
```

`[build-system]` tells installation tools which backend to use to actually build the package. `[project]` is the PEP 621 metadata table. With this file in place, the package can be built and installed locally in editable mode, which is convenient during development because code changes are picked up without reinstalling:

```
pip install -e .
```

After that, `import mathpack` works from anywhere in the environment, not just from inside the project folder, because the package has been properly registered.

### **Adding Optional Dependencies (`extras`)**

Optional features are listed in `[project.optional-dependencies]` and installed with `pip install mathpack[feature]`:

```toml
[project.optional-dependencies]
plot = ["matplotlib>=3.5"]
server = ["fastapi>=0.100", "uvicorn>=0.23"]
dev = [
    "pytest>=7.0",
    "black>=23.0",
    "ruff>=0.1",
]
all = ["mathpack[plot,server,dev]"]
```

Install with:

```
pip install mathpack[plot]
pip install mathpack[dev]
pip install mathpack[all]
```

This pattern is how most published libraries keep the core install small while still offering batteries-included installs for specific use cases.

### **Adding Console Scripts (Entry Points)**

To install a real command on the user's `PATH` when they install your package, declare it under `[project.scripts]`:

```toml
[project.scripts]
mathpack-demo = "mathpack.cli:main"
```

The format is `command-name = "package.module:function"`. After `pip install mathpack`, the user can run `mathpack-demo` from any shell, and it will call `main()` inside `mathpack.cli`. On Windows, an equivalent `.exe` is generated in the `Scripts` folder of the active environment.

For GUI applications that should not pop a terminal window, use `[project.gui-scripts]` instead:

```toml
[project.gui-scripts]
mathpack-gui = "mathpack.gui_app:main"
```

### **Adding Project URLs and Metadata**

```toml
[project.urls]
Homepage = "https://example.com/mathpack"
"Bug Tracker" = "https://github.com/yourname/mathpack/issues"
Changelog = "https://github.com/yourname/mathpack/blob/main/CHANGELOG.md"
```

This information shows up on the PyPI page for the package.

### **Configuring Setuptools Explicitly**

With setuptools as the backend, you can declare which packages and data files to include:

```toml
[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
include = ["mathpack*"]
```

`where = ["src"]` tells setuptools to look for packages inside `src/`, which pairs with the `src/` layout. `include = ["mathpack*"]` makes the discovery pattern explicit so unrelated folders in `src/` are not accidentally packaged.

To include non-Python files (templates, JSON schemas, default config files), use `package-data`:

```toml
[tool.setuptools.package-data]
mathpack = ["templates/*.html", "data/*.json"]
```

## **Entry Points: Console Scripts and Plugins**

Entry points are how a package exposes things to the outside world at install time. There are two main flavors.

### **Console Scripts**

A console script is a command that runs after `pip install`. The mapping is `name = "module:function"`:

```toml
[project.scripts]
mathpack-demo = "mathpack.cli:main"
```

```python
# src/mathpack/cli.py
import argparse
from . import add, area_circle, __version__

def main():
    parser = argparse.ArgumentParser(prog="mathpack-demo")
    parser.add_argument("--version", action="store_true")
    args = parser.parse_args()

    if args.version:
        print(f"mathpack {__version__}")
        return

    print("add(2, 3) =", add(2, 3))
    print("area_circle(2) =", round(area_circle(2), 4))

if __name__ == "__main__":
    main()
```

After `pip install -e .`:

```
$ mathpack-demo --version
mathpack 0.1.0

$ mathpack-demo
add(2, 3) = 5
area_circle(2) = 12.5664
```

The entry point mechanism is exactly what powers `pip`, `black`, `ruff`, `pytest`, `django-admin`, and most other commands you type in a Python environment.

### **Plugin Entry Points**

A package can also advertise "hooks" that other packages can plug into. For example, a test framework might expose a `pytest11` entry point, and any third-party plugin can register itself under that name:

```toml
# in your package's pyproject.toml
[project.entry-points."mathpack.formats"]
csv  = "mathpack.formats.csv:CsvFormat"
json = "mathpack.formats.json:JsonFormat"
```

Your code can then discover all installed plugins at runtime:

```python
# src/mathpack/plugins.py
from importlib.metadata import entry_points

def list_formats():
    eps = entry_points(group="mathpack.formats")
    return {ep.name: ep.load() for ep in eps}
```

This is the mechanism frameworks like `pytest`, `flask`, `mkdocs`, and `pluggy`-based systems use to discover extensions.

## **Building a Distribution**

Once `pyproject.toml` is in place, the project can be built into distribution files. The standard tool is `build`:

```
pip install build
python -m build
```

This produces two files inside a `dist/` folder:

- `mathpack-0.1.0.tar.gz` — a source distribution (sdist). Contains the source code and can be installed on any platform.
- `mathpack-0.1.0-py3-none-any.whl` — a built distribution (wheel). Already compiled, installs faster, and is the preferred form for `pip` to download.

You can check the contents of either file with `tar tzf` or by unzipping. Wheels are zip files under the hood.

```
dist/
    mathpack-0.1.0-py3-none-any.whl
    mathpack-0.1.0.tar.gz
```

The `--sdist` and `--wheel` flags build only one of the two:

```
python -m build --wheel
python -m build --sdist
```

## **Publishing to PyPI and Test PyPI**

The standard upload tool is `twine`. It is used because it sends files over HTTPS securely and lets you review the upload before it goes live.

```
pip install twine
```

Upload to Test PyPI first (a separate server that does not affect the real index) to make sure everything looks right:

```
python -m twine upload --repository testpypi dist/*
```

Then upload to the real PyPI:

```
python -m twine upload dist/*
```

`twine` will prompt for a username and a token. The recommended way is to create an API token on the PyPI website, scope it to one project, and paste it when prompted.

A real release flow looks like:

1. Bump the version in `pyproject.toml` and `__init__.py`.
2. Update the changelog.
3. Commit and tag the release in git.
4. `python -m build` to produce sdist and wheel.
5. `twine upload dist/*` to push to PyPI.
6. `pip install --upgrade mathpack` anywhere to verify.

## **Versioning**

The convention for Python packages is [Semantic Versioning](https://semver.org/) — `MAJOR.MINOR.PATCH`:

- Increment `MAJOR` for incompatible API changes.
- Increment `MINOR` for new backward-compatible features.
- Increment `PATCH` for backward-compatible bug fixes.

Pre-release and build metadata are written as `1.2.0a1`, `1.2.0b2`, `1.2.0rc1`, or `1.2.0.post1`.

The version is stored in two places that must stay in sync:

- `pyproject.toml` under `[project] version`.
- A `__version__` string in the package's `__init__.py`.

A common pattern is to read the version from the installed metadata instead of duplicating it:

```python
# mypackage/__init__.py
from importlib.metadata import version

__version__ = version("mypackage")
```

This requires the package to be installed, but it eliminates the risk of the two values drifting.

## **Package Data Files**

Many packages need to ship non-Python files — HTML templates, JSON schemas, default config files, certificate bundles. There are two ways to do this.

### **For Pure-Python Projects (Recommended): `package-data`**

```toml
[tool.setuptools.package-data]
mypackage = ["templates/*.html", "data/*.json"]
```

Files matching the patterns are included inside the wheel and sdist and are accessible at runtime via `importlib.resources`:

```python
# inside mypackage
from importlib.resources import files

template = (files("mypackage") / "templates" / "home.html").read_text()
```

### **For Source Distributions Only: `MANIFEST.in`**

If you need a file only in the sdist (for example, documentation sources that are not part of the runtime), use a `MANIFEST.in` file:

```
include README.md
include LICENSE
recursive-include mypackage/data *.json
```

## **Case Study 1: Turning `mathpack` into a Real Package**

Starting from a simple folder, here is what a complete, installable, distributable project looks like.

```
mathpack-project/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── mathpack/
│       ├── __init__.py
│       ├── arithmetic.py
│       ├── geometry.py
│       └── cli.py
└── tests/
    ├── test_arithmetic.py
    └── test_geometry.py
```

`src/mathpack/__init__.py`:

```python
"""mathpack: small arithmetic and geometry helpers."""

from importlib.metadata import version

__version__ = version("mathpack")

from .arithmetic import add, subtract
from .geometry import area_circle, area_rectangle

__all__ = [
    "__version__",
    "add", "subtract",
    "area_circle", "area_rectangle",
]
```

`src/mathpack/arithmetic.py`:

```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
```

`src/mathpack/geometry.py`:

```python
import math

def area_circle(radius):
    return math.pi * radius * radius

def area_rectangle(length, width):
    return length * width
```

`src/mathpack/cli.py`:

```python
import argparse
from . import __version__, add, area_circle

def main():
    parser = argparse.ArgumentParser(prog="mathpack")
    parser.add_argument("--version", action="store_true")
    args = parser.parse_args()

    if args.version:
        print(f"mathpack {__version__}")
        return

    print("add(2, 3) =", add(2, 3))
    print("area_circle(2) =", round(area_circle(2), 4))

if __name__ == "__main__":
    main()
```

`pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "mathpack"
version = "0.1.0"
description = "Small arithmetic and geometry helpers"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [{name = "Your Name", email = "you@example.com"}]

[project.optional-dependencies]
dev = ["pytest>=7.0"]

[project.scripts]
mathpack = "mathpack.cli:main"

[tool.setuptools.packages.find]
where = ["src"]
```

`tests/test_arithmetic.py`:

```python
from mathpack import add, subtract

def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(10, 4) == 6
```

Build, install, and use:

```
$ pip install -e ".[dev]"
$ mathpack --version
mathpack 0.1.0
$ mathpack
add(2, 3) = 5
area_circle(2) = 12.5664
$ pytest
...
```

Walking through the design:

- The `src/` layout forces the test to import the installed package, so the tests would fail loudly if `pyproject.toml` pointed at the wrong directory.
- `__init__.py` re-exports the public API so users only need to know the top-level name.
- `__version__` is read from the package metadata, so there is no second source of truth.
- The `mathpack` script is declared once in `pyproject.toml` and works on every platform.

## **Case Study 2: A Plugin Architecture with Entry Points**

**Scenario:** You are building a data-conversion toolkit. The core package can read and write CSV and JSON. You want third parties to be able to add support for new formats (YAML, Parquet, Excel) without modifying your code.

```
src/converter/
    __init__.py
    core.py        # generic read/write engine
    formats/
        __init__.py
        csv_fmt.py
        json_fmt.py
    plugins.py     # entry-point discovery
```

`src/converter/core.py`:

```python
class Reader:
    def read(self, path):
        raise NotImplementedError

class Writer:
    def write(self, path, rows):
        raise NotImplementedError
```

`src/converter/formats/csv_fmt.py`:

```python
import csv
from ..core import Reader, Writer

class CsvReader(Reader):
    def read(self, path):
        with open(path, newline="") as f:
            return list(csv.DictReader(f))

class CsvWriter(Writer):
    def write(self, path, rows):
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
```

`src/converter/formats/json_fmt.py`:

```python
import json
from ..core import Reader, Writer

class JsonReader(Reader):
    def read(self, path):
        with open(path) as f:
            return json.load(f)

class JsonWriter(Writer):
    def write(self, path, rows):
        with open(path, "w") as f:
            json.dump(rows, f, indent=2)
```

`src/converter/plugins.py`:

```python
from importlib.metadata import entry_points

GROUP = "converter.formats"

def discover():
    """Find all installed format plugins and return {name: (Reader, Writer)}."""
    eps = entry_points(group=GROUP)
    found = {}
    for ep in eps:
        plugin = ep.load()
        found[ep.name] = (plugin.Reader, plugin.Writer)
    return found
```

`pyproject.toml` for the core package:

```toml
[project.entry-points."converter.formats"]
csv  = "converter.formats.csv_fmt"
json = "converter.formats.json_fmt"
```

A third-party plugin in a separate package would look like this:

```toml
# pyproject.toml of converter-yaml
[project.entry-points."converter.formats"]
yaml = "converter_yaml.format"
```

Once both packages are installed in the same environment, `discover()` returns `csv`, `json`, and `yaml` without the core package knowing anything about YAML support. This is the same pattern used by `pytest`, `mkdocs`, `sphinx`, and many other extensible tools.

## **Case Study 3: A Real E-commerce Package Layout**

A larger application typically has more layers than just `core/`. Here is a realistic layout for an e-commerce service:

```
shop_project/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── shop/
│       ├── __init__.py
│       ├── config.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes.py
│       ├── catalog/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   └── repository.py
│       ├── orders/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   └── service.py
│       └── payments/
│           ├── __init__.py
│           ├── gateway.py
│           └── refunds.py
└── tests/
    ├── test_catalog.py
    ├── test_orders.py
    └── test_payments.py
```

`src/shop/__init__.py`:

```python
"""shop: e-commerce service package."""

__version__ = "1.0.0"

from .config import Settings, load_settings
from .orders.service import place_order, cancel_order
from .payments.gateway import charge_card
from .catalog.repository import list_products

__all__ = [
    "__version__",
    "Settings", "load_settings",
    "place_order", "cancel_order",
    "charge_card",
    "list_products",
]
```

A module in `orders/` that needs something from `payments/`:

```python
# src/shop/orders/service.py
from shop.payments.gateway import charge_card
from shop.catalog.repository import get_product

def place_order(user_id, product_id, quantity):
    product = get_product(product_id)
    amount = product.price * quantity
    return charge_card(amount=amount, currency="INR")
```

This shows several things at once:

- Sub-packages are first-class namespaces (`shop.payments.gateway`).
- The top-level `__init__.py` re-exports the most-used names, so most call sites stay short.
- Tests live in a separate top-level `tests/` directory, not inside `src/shop/`, so they are never included in the distribution.

## **Common Gotchas**

- **Forgetting `__init__.py` in a nested sub-package** can cause confusing import errors in older tooling or in mixed setups, even though modern Python may still import it as a namespace package. Being explicit avoids the ambiguity.
- **Mixing the flat layout and the `src/` layout** in the same project tends to cause `pip install -e .` to accidentally pick up the wrong version of the code. Stick to one layout per project.
- **A package folder that shares its name with a standard library or popular third-party package** (for example naming a personal package `email`, `json`, or `numpy`) will shadow the real one for any code that runs from that folder, leading to strange errors that have nothing to do with the personal package itself.
- **Circular imports between sub-modules** of the same package — for example `orders.py` importing from `payments.py` while `payments.py` imports from `orders.py` — raise `ImportError`. Move the shared logic into a third module that both import from.
- **Heavy work in `__init__.py`** at import time makes the package slow to import and can break code that does `import mypackage; mypackage.something()`. Move startup work into functions and use lazy imports if needed.
- **`__pycache__` and `.pyc` files inside the source tree** should not be shipped. With the `src/` layout and a proper `pyproject.toml`, the build backend will not include them. If you see compiled files in your wheel, check your `include` patterns.
- **Two versions of the same package installed at once** (one in the system Python, one in a venv) cause `ModuleNotFoundError` for code that runs outside the venv, or version-mismatch errors for code that runs inside it. Use virtual environments and check `pip show package` to see which version is actually loaded.
- **Forgetting to bump the version** in both `pyproject.toml` and `__init__.py` (or the metadata) before publishing a new release means the new file uploads but users still see the old version because their package manager is happy with what they already have.

## **Best Practices for Packaging**

- **Use the `src/` layout** for any non-trivial project, even if you are not publishing yet. It catches packaging bugs early.
- **Pin the build backend version** in `[build-system] requires`, e.g. `["setuptools>=68"]`. The build environment is reproducible that way.
- **Keep `__init__.py` small and side-effect free.** No top-level `print`, no database connections, no file reads. Re-export public names; do the heavy work inside functions.
- **Set `__version__` from the package metadata** so there is only one source of truth.
- **Use entry points** to expose CLI commands. Avoid asking users to remember `python -m yourpackage`.
- **Declare optional dependencies** under `[project.optional-dependencies]` and let users opt in with `pip install yourpackage[feature]`.
- **Put tests outside the package** directory. Tests should run against the installed package, not the in-tree source.
- **Provide a `README.md`** and reference it from `pyproject.toml` with `readme = "README.md"`. PyPI renders it on the project page.
- **Choose a license** and include the `LICENSE` file at the project root. Most ecosystems expect an SPDX identifier in `pyproject.toml` too.
- **Use semantic versioning** (`MAJOR.MINOR.PATCH`) and document the policy in `README.md`.
- **Test the build before publishing.** `python -m build` should succeed, `twine check dist/*` should report no errors, and the produced wheel should install in a fresh virtual environment.

## **Quick Reference Summary**

### **Package Concepts**

| Concept | Syntax / File | Purpose |
|---|---|---|
| Mark a folder as a package | `__init__.py` inside the folder | Makes the folder importable as a package |
| Import a module from a package | `from package import module` | Access as `module.name` |
| Import a member directly | `from package.module import name` | Use `name` without any prefix |
| Re-export in `__init__.py` | `from .module import name` | Shortens import paths for users of the package |
| Control `import *` | `__all__ = ["a", "b"]` | Defines the public surface of the package |
| Sub-package | Nested folder, each with its own `__init__.py` | Organizes a large package into smaller groups |
| Namespace package | Folder with no `__init__.py` | Combines contributions from multiple locations |
| Relative import | `from . import sibling` | Import within the same package |
| Absolute import | `from package.module import name` | Full dotted path from a top-level package |

### **`pyproject.toml` Tables**

| Table | Purpose |
|---|---|
| `[build-system]` | Which backend builds the package (`setuptools`, `hatchling`, `flit`, `poetry`) and what it needs. |
| `[project]` | Name, version, description, dependencies, Python version, authors, license, classifiers. |
| `[project.optional-dependencies]` | Named groups of extra dependencies installed with `[feature]`. |
| `[project.scripts]` | Console commands installed on `PATH` at install time. |
| `[project.gui-scripts]` | Same, but no terminal window pops up on Windows. |
| `[project.urls]` | Homepage, bug tracker, changelog, etc. Shown on the PyPI page. |
| `[project.entry-points."group"]` | Plugin hooks for third-party packages. |
| `[tool.setuptools.packages.find]` | Where setuptools looks for packages to include. |
| `[tool.setuptools.package-data]` | Non-Python files to include in the wheel. |

### **Common Commands**

| Task | Command |
|---|---|
| Install package in editable mode | `pip install -e .` |
| Install with an extra | `pip install -e ".[dev]"` |
| Build sdist and wheel | `python -m build` |
| Build only the wheel | `python -m build --wheel` |
| Validate distributions | `python -m twine check dist/*` |
| Upload to Test PyPI | `python -m twine upload --repository testpypi dist/*` |
| Upload to PyPI | `python -m twine upload dist/*` |
| Check what is installed | `pip show package-name` |
| Show a package's files | `pip show -f package-name` |

### **Layout vs Use Case**

| Layout | Source location | Best for |
|---|---|---|
| Flat | `mypackage/` at project root | Small scripts, learning, single-file utilities |
| `src/` | `src/mypackage/` | Anything packaged, distributed, shared, or installed by others |

## **Practice and Next Steps**

- Turn the `mathpack` example above into an actual folder on disk, add a second sub-package called `stats`, and practice importing across both from a separate `main.py` file.
- Write an `__init__.py` that re-exports selected functions and defines `__all__`, then compare `from mathpack import *` before and after adding `__all__`.
- Convert a flat-layout project you already have into a `src/` layout and confirm `pip install -e ".[dev]"` still works.
- Add a `cli.py` to a package and expose it through `[project.scripts]`. Install in editable mode and run the command from a totally different folder.
- Add an entry-point group to a package (for example `myapp.formats`) and write a tiny throwaway plugin in a separate project that registers a format under that group. Confirm `entry_points()` sees it.
- Use `python -m build` to produce a wheel, then `pip install ./dist/yourpackage-0.1.0-py3-none-any.whl` in a fresh virtual environment and confirm `import yourpackage` works.
- Upload your built package to Test PyPI, then install it from Test PyPI in another environment with `pip install --index-url https://test.pypi.org/simple/ yourpackage`.
- Try renaming your package to something that shadows a standard library name (for example `email` or `json`), watch the failure, and rename it back.
- In a single project, deliberately put top-level `print()` calls in `__init__.py`, then `import` the package from another script. Notice the side effects at import time, and refactor the `print` calls into a function that is only called inside `if __name__ == "__main__":`.

After these, the natural next topics are: virtual environments in depth, lock files (`pip-tools`, `uv`, `poetry`), automated publishing with GitHub Actions, and signing releases with Sigstore or PGP.
