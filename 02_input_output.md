# **Python Input, Command Line Arguments, and Output**

## **Reading Dynamic Input from the Keyboard**

In Python 3, the `input()` function reads a value typed by the user at runtime. It always returns the entered value as a `str`, regardless of what the user types — even if they enter a number or a boolean.

```python
type(input("Enter value: "))
# Enter value: 10     → <class 'str'>
# Enter value: 10.5   → <class 'str'>
# Enter value: True   → <class 'str'>
```

To use the entered value in arithmetic or comparisons, you must explicitly convert it to the desired type.

---

### **Way 1 — Using Intermediate Variables**

Read the input into a string variable first, then convert it separately. This approach is the most readable for beginners.

```python
x = input("Enter First Number: ")
y = input("Enter Second Number: ")

i = int(x)
j = int(y)

print("The Sum:", i + j)
# The Sum: 300
```

---

### **Way 2 — Direct Type Casting Inside `input()`**

Wrap the `input()` call directly inside a type conversion function. This is more concise and the most common pattern in practice.

```python
x = int(input("Enter First Number: "))
y = int(input("Enter Second Number: "))

print("The Sum:", x + y)
# The Sum: 300
```

---

### **Way 3 — One-Liner Approach**

Combine reading, converting, and printing in a single expression. Use this only when brevity matters more than readability.

```python
print("The Sum:", int(input("Enter First Number: ")) + int(input("Enter Second Number: ")))
# The Sum: 300
```

---

### **Example — Reading an Employee Record**

This program reads multiple fields of different types for a single employee and confirms the data back to the user.

```python
eno   = int(input("Enter Employee No: "))
ename = input("Enter Employee Name: ")
esal  = float(input("Enter Employee Salary: "))
eaddr = input("Enter Employee Address: ")

# bool(non-empty-string) is always True; this is a known limitation
married = bool(input("Employee Married? [True|False]: "))

print("Please Confirm Information")
print("Employee No:", eno)
print("Employee Name:", ename)
print("Employee Salary:", esal)
print("Employee Address:", eaddr)
print("Employee Married?:", married)
```

**Note:** Using `bool(input(...))` does not correctly parse the string `"False"` — `bool("False")` evaluates to `True` because the string is non-empty. For real boolean input parsing, use a comparison: `input("Married? ").strip().lower() == "true"`.

---

## **Reading Multiple Values in a Single Line**

Python allows reading several values at once using `split()` combined with a list comprehension. The `split()` method divides the input string by whitespace (default) or any separator you provide.

```python
a, b = [int(x) for x in input("Enter 2 numbers: ").split()]
print("Product is:", a * b)
# Enter 2 numbers: 10 20
# Product is: 200
```

### **Custom Separator**

Pass any delimiter string to `split()` to use it instead of whitespace.

```python
a, b, c = [float(x) for x in input("Enter 3 float numbers: ").split(',')]
print("The Sum is:", a + b + c)
# Enter 3 float numbers: 10.5,20.6,20.1
# The Sum is: 51.2
```

---

## **Using `eval()` for Expression Input**

The `eval()` function takes a string and evaluates it as a Python expression, returning the resulting value.

```python
x = eval("10 + 20 + 30")
print(x)  # 60
```

You can pass `input()` directly to `eval()` so the user can enter a live expression:

```python
x = eval(input("Enter Expression: "))
# Enter Expression: 10 + 2 * 3 / 4
print(x)  # 11.5
```

`eval()` can also parse structured types like lists, tuples, and sets if the user types them in the correct literal syntax:

```python
l = eval(input("Enter List: "))
print("Type of l:", type(l))
print("Contents of l:", l)
# Enter List: [1, 2, 3]
# Type of l: <class 'list'>
# Contents of l: [1, 2, 3]
```

**Safety note:** `eval()` executes arbitrary Python code. Always validate or sanitize input before using `eval()` in any production or networked application. Use `ast.literal_eval()` instead when you only need to parse Python literals safely.

```python
import ast

expression = input("Enter a mathematical expression (e.g., 10 + 20 * 3): ")

try:
    result = eval(expression)
    print("Result:", result)
except Exception as e:
    print("Invalid expression:", e)
# Result: 70
```

### **`ast.literal_eval` — The Safe Alternative**

`ast.literal_eval` parses only Python literals (strings, numbers, lists, dicts, tuples, sets, booleans, `None`). It raises `ValueError` on anything else. Use this instead of `eval()` whenever you are parsing user-supplied data.

```python
import ast

raw = input("Enter a list of scores: ")
scores = ast.literal_eval(raw)
print(type(scores), scores)
# Enter a list of scores: [95, 88, 72, 100]
# <class 'list'> [95, 88, 72, 100]

# Attempting to inject code raises ValueError instead of executing it
ast.literal_eval("__import__('os').system('rm -rf /')")
# ValueError: malformed node or string
```

---

## **Command Line Arguments**

Command line arguments are values passed to a Python script at the time it is executed from the terminal. They are accessible via `argv`, a list provided by the `sys` module.

Key facts about `argv`:

- `argv` is a `list`, not an array.
- `argv[0]` always holds the name of the script itself — it is not one of the user-supplied arguments.
- `argv[1]`, `argv[2]`, and so on hold the actual arguments supplied by the user.
- All command line arguments arrive as strings and must be cast to other types as needed.

---

### **Checking the Type of `argv`**

```python
# run as a .py file, not in a notebook
from sys import argv

print(type(argv))
# <class 'list'>
```

---

### **Accessing Script Name and Arguments**

```python
from sys import argv

print("Script Name:", argv[0])
print("Command Line Arguments:", argv[1:])
```

```
$ py session01.py 10 20 30
Script Name: session01.py
Command Line Arguments: ['10', '20', '30']
```

---

### **Iterating Over All Arguments**

```python
from sys import argv

print("The Number of Command Line Arguments:", len(argv))
print("The List of Command Line Arguments:", argv)
print("Command Line Arguments one by one:")

for x in argv:
    print(x)
```

```
$ py session01.py 10 20 30 40 05 60 70 80
The Number of Command Line Arguments: 9
The List of Command Line Arguments: ['session01.py', '10', '20', '30', '40', '05', '60', '70', '80']
```

---

### **Summing Numeric Arguments**

Because `argv` values are strings, you must cast them to `int` or `float` before arithmetic. Attempting to add them as strings concatenates them instead.

```python
from sys import argv

total = 0
for x in argv[1:]:
    total = total + int(x)

print("Sum is:", total)
# $ py session01.py 10 20 30 40 05 60 70 80
# Sum is: 315
```

---

### **Note 1 — Handling Arguments That Contain Spaces**

Spaces are the default separator between command line arguments. To pass a value that contains a space, wrap it in double quotes (not single quotes).

| Command | Output |
|---|---|
| `py test.py Arjun thakur` | `Arjun` (split into two separate arguments) |
| `py test.py 'Arjun thakur'` | `'Arjun` (single quotes are not treated as grouping) |
| `py test.py "Arjun thakur"` | `Arjun thakur` (correctly passed as one argument) |

---

### **Note 2 — All Arguments Are Strings**

Every value in `argv` is a `str`. Use `int()`, `float()`, or other conversion functions before performing arithmetic.

```python
from sys import argv

print(argv[1] + argv[2])             # string concatenation: '1020'
print(int(argv[1]) + int(argv[2]))   # integer addition: 30
# $ py test.py 10 20
```

---

### **Note 3 — IndexError on Out-of-Range Access**

Accessing an `argv` index that was not provided at the command line raises an `IndexError`. Always guard against this in scripts that require a minimum number of arguments.

```python
from sys import argv
print(argv[100])
# IndexError: list index out of range
```

---

## **Production CLI Patterns**

Raw `sys.argv` is only appropriate for the simplest scripts. Real-world tools use `argparse`, `click`, or `typer` — each offering progressively less boilerplate and more safety.

---

### **`argparse` — Standard Library, No Dependencies**

`argparse` is built into Python and handles types, defaults, choices, and `--help` automatically. It is the minimum baseline for any script that other people will use.

```python
# train.py — ML training script with argparse
import argparse

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a classification model")

    parser.add_argument("--model",    type=str,   required=True,  help="Model name: resnet50 | vgg16 | efficientnet")
    parser.add_argument("--epochs",   type=int,   default=10,     help="Number of training epochs")
    parser.add_argument("--lr",       type=float, default=1e-3,   help="Learning rate")
    parser.add_argument("--batch",    type=int,   default=32,     help="Batch size")
    parser.add_argument("--device",   type=str,   default="cuda", choices=["cuda", "cpu"])
    parser.add_argument("--verbose",  action="store_true",        help="Enable verbose logging")

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(f"Training {args.model} for {args.epochs} epochs | lr={args.lr} | device={args.device}")
    if args.verbose:
        print(f"Batch size: {args.batch}")

if __name__ == "__main__":
    main()
```

```
$ python train.py --model resnet50 --epochs 20 --lr 0.0005 --verbose
Training resnet50 for 20 epochs | lr=0.0005 | device=cuda
Batch size: 32

$ python train.py --help
usage: train.py [-h] --model MODEL [--epochs EPOCHS] [--lr LR] ...
```

---

### **`click` — Decorator-Based, Production Favourite**

`click` wraps each command as a decorated function. It is widely used in ML tooling, FastAPI CLIs, and data pipeline scripts. It handles type coercion before validation, which catches bad input earlier than `argparse`.

```python
# ingest.py — data pipeline entry point with click
import click

@click.command()
@click.option("--source",   required=True,  type=click.Path(exists=True), help="Path to input CSV")
@click.option("--dest",     required=True,  type=str,                     help="S3 bucket or local output path")
@click.option("--workers",  default=4,      type=int,                     help="Number of parallel workers")
@click.option("--dry-run",  is_flag=True,                                 help="Validate without writing output")
def ingest(source: str, dest: str, workers: int, dry_run: bool) -> None:
    """Ingest CSV data from SOURCE and write processed output to DEST."""
    click.echo(f"Reading: {source}")
    click.echo(f"Workers: {workers} | Dry run: {dry_run}")
    if not dry_run:
        click.echo(f"Writing to: {dest}")

if __name__ == "__main__":
    ingest()
```

```
$ python ingest.py --source data/raw.csv --dest s3://meera-bucket/processed/ --workers 8
Reading: data/raw.csv
Workers: 8 | Dry run: False
Writing to: s3://meera-bucket/processed/

$ python ingest.py --source missing.csv --dest /tmp/out
Error: Invalid value for '--source': Path 'missing.csv' does not exist.
```

**click subcommands** — useful for tools with multiple verbs like `db migrate`, `db seed`:

```python
import click

@click.group()
def db() -> None:
    """Database management commands."""
    pass

@db.command()
@click.option("--env", default="dev", type=click.Choice(["dev", "staging", "prod"]))
def migrate(env: str) -> None:
    click.echo(f"Running migrations on {env}")

@db.command()
def seed() -> None:
    click.echo("Seeding database with fixture data")

if __name__ == "__main__":
    db()
```

```
$ python manage.py db migrate --env staging
Running migrations on staging
```

---

### **`typer` — Type-Hint-Driven, Zero Boilerplate**

`typer` reads Python type annotations directly to build the CLI. There are no decorators for individual options — the function signature is the spec. This is the most modern approach as of 2026 and pairs naturally with Pydantic.

```python
# evaluate.py — model evaluation CLI with typer
from pathlib import Path
import typer

app = typer.Typer()

@app.command()
def evaluate(
    checkpoint: Path  = typer.Argument(...,          help="Path to model checkpoint (.pt file)"),
    dataset:    str   = typer.Option("val",          help="Dataset split: train | val | test"),
    batch_size: int   = typer.Option(64,             help="Batch size for evaluation"),
    threshold:  float = typer.Option(0.5,            help="Confidence threshold for predictions"),
    save_report: bool = typer.Option(False, "--save",help="Save evaluation report to disk"),
) -> None:
    """Evaluate a trained model checkpoint on a dataset split."""
    typer.echo(f"Loading checkpoint: {checkpoint}")
    typer.echo(f"Split: {dataset} | Batch: {batch_size} | Threshold: {threshold}")
    if save_report:
        typer.echo("Saving report to eval_report.json")

if __name__ == "__main__":
    app()
```

```
$ python evaluate.py checkpoints/best.pt --dataset test --threshold 0.6 --save
Loading checkpoint: checkpoints/best.pt
Split: test | Batch: 64 | Threshold: 0.6
Saving report to eval_report.json
```

---

### **Comparison Table**

| Feature | `sys.argv` | `argparse` | `click` | `typer` |
|---|---|---|---|---|
| Built-in (no install) | Yes | Yes | No | No |
| Auto `--help` | No | Yes | Yes | Yes |
| Type coercion | Manual | Yes | Yes | Via type hints |
| Subcommands | Manual | Yes | Yes | Yes |
| Decorator syntax | No | No | Yes | No |
| Type-hint driven | No | No | No | Yes |
| Best for | One-off scripts | Standard tools | Production CLIs | Modern codebases |

---

## **Input Validation in Production — Pydantic v2**

In real applications, user input never comes from `input()` alone — it arrives as JSON from an API, form fields, config files, or CLI flags. The standard for validating all of this in Python is **Pydantic v2**, which is Rust-backed and 5–50x faster than v1.

The core idea: define a model class with type annotations; Pydantic coerces and validates every field on instantiation, raising `ValidationError` with structured detail on failure.

---

### **Basic Model Validation**

```python
from pydantic import BaseModel, Field, EmailStr
from pydantic import ValidationError

class EmployeeIn(BaseModel):
    emp_id:  int
    name:    str
    salary:  float = Field(gt=0, description="Must be positive")
    email:   EmailStr
    dept:    str    = Field(default="General", max_length=50)
    active:  bool   = True

try:
    emp = EmployeeIn(
        emp_id=101,
        name="Vikram",
        salary=95000.0,
        email="vikram@company.in",
        dept="Data Science",
    )
    print(emp)
    # emp_id=101 name='Vikram' salary=95000.0 email='vikram@company.in' dept='Data Science' active=True

except ValidationError as e:
    print(e.json(indent=2))
```

When validation fails, the error payload is structured and machine-readable:

```python
try:
    EmployeeIn(emp_id="abc", name="Rohit", salary=-500, email="not-an-email")
except ValidationError as e:
    for err in e.errors():
        print(err["loc"], "->", err["msg"])
# ('emp_id',) -> Input should be a valid integer
# ('salary',) -> Input should be greater than 0
# ('email',)  -> value is not a valid email address
```

---

### **`@field_validator` — Custom Field Rules**

Use `@field_validator` when a field needs logic beyond type and range checks.

```python
from pydantic import BaseModel, field_validator

class MLConfig(BaseModel):
    model_name: str
    learning_rate: float
    epochs: int
    device: str

    @field_validator("learning_rate")
    @classmethod
    def lr_must_be_small(cls, v: float) -> float:
        if not (1e-6 <= v <= 1.0):
            raise ValueError(f"learning_rate must be in [1e-6, 1.0], got {v}")
        return v

    @field_validator("device")
    @classmethod
    def device_must_be_valid(cls, v: str) -> str:
        allowed = {"cuda", "cpu", "mps"}
        if v not in allowed:
            raise ValueError(f"device must be one of {allowed}")
        return v

config = MLConfig(model_name="resnet50", learning_rate=3e-4, epochs=30, device="cuda")
print(config.model_dump())
# {'model_name': 'resnet50', 'learning_rate': 0.0003, 'epochs': 30, 'device': 'cuda'}
```

---

### **Parsing Input from JSON or a Dict (API boundary)**

In FastAPI and similar frameworks, request bodies are parsed directly into Pydantic models. You can replicate this manually using `model_validate`:

```python
from pydantic import BaseModel
from typing import Optional

class InferenceRequest(BaseModel):
    text:       str
    max_tokens: int            = 512
    temperature: float         = 0.7
    model:      str            = "HuggingFaceTB/SmolLM2-1.7B-Instruct"
    stream:     bool           = False
    user_id:    Optional[str]  = None

# Simulating a JSON payload arriving from an HTTP request
payload = {
    "text": "Summarise the transformer architecture in three sentences.",
    "max_tokens": 256,
    "temperature": 0.3,
    "user_id": "u_tanvi_42",
}

req = InferenceRequest.model_validate(payload)
print(req.model_dump())
# {'text': 'Summarise the transformer architecture...', 'max_tokens': 256,
#  'temperature': 0.3, 'model': 'HuggingFaceTB/SmolLM2-1.7B-Instruct',
#  'stream': False, 'user_id': 'u_tanvi_42'}
```

---

### **`pydantic-settings` — Config from `.env` Files**

Environment-based config is the standard in 12-factor apps. `pydantic-settings` reads `.env` files and environment variables into a typed model automatically.

```python
# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name:      str   = "RagService"
    debug:         bool  = False
    db_url:        str
    redis_url:     str   = "redis://localhost:6379"
    api_key:       str
    max_workers:   int   = 4

# .env file would contain:
# DB_URL=postgresql://user:pass@localhost/ragdb
# API_KEY=sk-abc123
# DEBUG=true

settings = AppSettings()
print(settings.app_name, settings.debug, settings.max_workers)
# RagService True 4
```

This pattern replaces brittle `os.getenv("KEY")` calls scattered across the codebase.

---

## **Output Statements — `print()`**

The `print()` function sends text or object representations to standard output. It supports many calling forms.

---

### **Form 1 — No Arguments**

Calling `print()` with no arguments writes a single newline character, producing a blank line in the output.

```python
print()
```

---

### **Form 2 — Printing a String Literal**

```python
print("Hello World")
print("Hello \n World")   # newline inside the string
print("Hello\tWorld")     # tab character
print(10 * "Hello")       # HelloHelloHello... (10 times)
print("Hello" + "World")  # HelloWorld
print("Hello", "World")   # Hello World (comma adds a space)
```

- Using `+` between two strings concatenates them without any space.
- Using `,` between arguments in `print()` adds a space between them automatically.
- Adding a string and a non-string type with `+` raises a `TypeError`; use `,` or f-strings instead.

---

### **Form 3 — Multiple Arguments and the `sep` Parameter**

By default, `print()` places a single space between each argument. Use the `sep` keyword to change the separator.

```python
a, b, c = 10, 20, 30

print("The Values are:", a, b, c)   # The Values are: 10 20 30
print(a, b, c, sep=',')             # 10,20,30
print(a, b, c, sep=':')             # 10:20:30
```

---

### **Form 4 — The `end` Parameter**

By default, `print()` appends a newline (`\n`) after each call. Use `end` to replace that character with anything else.

```python
print("Hello", end=' ')
print("Durga", end=' ')
print("Soft")
# Hello Durga Soft
```

---

### **Form 5 — Printing Objects**

Any Python object can be passed directly to `print()`. The object's `__str__` representation is displayed.

```python
l = [10, 20, 30, 40]
t = (10, 20, 30, 40)

print(l)   # [10, 20, 30, 40]
print(t)   # (10, 20, 30, 40)
```

---

### **Form 6 — Mixing Strings and Variables**

```python
name = "Tanvi"
age  = 26
role = "ML Engineer"
city = "Pune"

print("Hello", name, "Your Age is", age)
# Hello Tanvi Your Age is 26

print("You are working as", role, "in", city)
# You are working as ML Engineer in Pune
```

---

### **Form 7 — `%`-Style Formatted Strings (Legacy)**

The `%` operator inserts variables into a string using format specifiers. This style predates f-strings and is still common in legacy codebases and in the `logging` module.

| Specifier | Type |
|---|---|
| `%i` or `%d` | Integer |
| `%f` | Float |
| `%s` | String (or any object) |

```python
a, b, c = 10, 20, 30

print("a value is %i" % a)
# a value is 10

print("b value is %d and c value is %d" % (b, c))
# b value is 20 and c value is 30

name = "Harsha"
scores = [88, 92, 79]
print("Hello %s ... Your Scores are %s" % (name, scores))
# Hello Harsha ... Your Scores are [88, 92, 79]
```

---

### **Form 8 — `str.format()` with Placeholders**

The `format()` method replaces `{}` placeholders in a string. Placeholders can be positional (indexed) or named.

```python
name   = "Drishya"
salary = 85000
dept   = "Data Science"

print("Hello {0}, your salary is {1} and your department is {2}".format(name, salary, dept))
# Hello Drishya, your salary is 85000 and your department is Data Science

print("Hello {n}, your salary is {s} and your department is {d}".format(n=name, s=salary, d=dept))
# Hello Drishya, your salary is 85000 and your department is Data Science
```

---

## **Modern Output — f-strings (Python 3.6+, Preferred)**

f-strings are the standard for string formatting in all modern Python code. They are evaluated at parse time, fully support arbitrary expressions, and are faster than both `%` formatting and `.format()`.

### **Basic f-string**

```python
name  = "Karan"
score = 94.5
rank  = 1

print(f"Name: {name} | Score: {score:.2f} | Rank: {rank}")
# Name: Karan | Score: 94.50 | Rank: 1
```

### **Expressions and Calls Inside f-strings**

Any valid Python expression can go inside `{}`:

```python
import math

radius = 7.0
print(f"Area: {math.pi * radius ** 2:.4f}")
# Area: 153.9380

items = ["GPU", "RAM", "SSD"]
print(f"Cart has {len(items)} items: {', '.join(items)}")
# Cart has 3 items: GPU, RAM, SSD
```

### **`=` Specifier for Debug Printing (Python 3.8+)**

The `=` suffix inside an f-string prints both the expression and its value. This is useful for quick debugging without a debugger.

```python
batch_size = 32
lr         = 3e-4
model_name = "SmolLM2"

print(f"{batch_size=} | {lr=} | {model_name=}")
# batch_size=32 | lr=0.0003 | model_name='SmolLM2'
```

### **Multi-line f-strings**

```python
emp_id   = 201
emp_name = "Meera"
emp_dept = "MLOps"
emp_sal  = 120000

report = (
    f"Employee Report\n"
    f"  ID   : {emp_id}\n"
    f"  Name : {emp_name}\n"
    f"  Dept : {emp_dept}\n"
    f"  Salary: ₹{emp_sal:,}"
)
print(report)
# Employee Report
#   ID   : 201
#   Name : Meera
#   Dept : MLOps
#   Salary: ₹1,20,000
```

### **f-string Format Specifiers Reference**

| Specifier | Meaning | Example | Output |
|---|---|---|---|
| `:.2f` | Float, 2 decimal places | `f"{3.14159:.2f}"` | `3.14` |
| `:,` | Thousands separator | `f"{1000000:,}"` | `1,000,000` |
| `:>10` | Right-align in 10 chars | `f"{'hi':>10}"` | `        hi` |
| `:<10` | Left-align in 10 chars | `f"{'hi':<10}"` | `hi        ` |
| `:^10` | Center in 10 chars | `f"{'hi':^10}"` | `    hi    ` |
| `:05d` | Zero-pad integer | `f"{42:05d}"` | `00042` |
| `:e` | Scientific notation | `f"{0.000123:e}"` | `1.230000e-04` |
| `:%` | Percentage | `f"{0.947:.1%}"` | `94.7%` |
| `=` suffix | Debug: name=value | `f"{lr=}"` | `lr=0.0003` |
| `!r` | `repr()` of value | `f"{'hi'!r}"` | `'hi'` |

---

## **Production Output — Replace `print()` with Logging**

`print()` is fine for scripts and notebooks. In any code that runs in staging or production — APIs, training jobs, data pipelines, background workers — use the `logging` module instead. `print()` has no log level, no timestamp, no routing to files, and cannot be silenced without code changes.

### **Why `print()` Fails in Production**

- It writes to stdout with no metadata — no timestamp, no severity, no module name.
- There is no way to suppress debug prints without deleting or commenting them out.
- Output cannot be routed to a file, a log aggregator (CloudWatch, Datadog, ELK), or a monitoring system.
- It cannot be filtered by severity level at deploy time.

### **Standard Library `logging` — Correct Baseline**

```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log"),
    ],
)

logger = logging.getLogger(__name__)

logger.debug("Checkpoint path resolved")   # suppressed at INFO level
logger.info("Training started: epochs=30, lr=3e-4")
logger.warning("GPU memory at 90% capacity")
logger.error("Validation loss diverged at epoch 12")
```

```
2026-06-15 10:42:01 | INFO     | __main__ | Training started: epochs=30, lr=3e-4
2026-06-15 10:42:01 | WARNING  | __main__ | GPU memory at 90% capacity
2026-06-15 10:42:01 | ERROR    | __main__ | Validation loss diverged at epoch 12
```

**Important:** Do not use f-strings inside `logging` calls. The `%`-style formatting in `logging` is lazy — the string is only built if the message will actually be emitted. f-strings are always evaluated, which wastes time when the log level would suppress the message.

```python
name = "Siddharth"
# Wrong — f-string always evaluated even if DEBUG is suppressed
logger.debug(f"Processing record for {name}")

# Correct — string only built if DEBUG is enabled
logger.debug("Processing record for %s", name)
```

---

### **`loguru` — Drop-In Replacement, Zero Config**

`loguru` replaces the standard `logging` module with a single `logger` object that is pre-configured with sensible defaults. It is widely used in fast-moving ML and API projects.

```python
from loguru import logger
import sys

# Remove default handler, add one with custom format
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
    level="INFO",
)
logger.add("logs/pipeline.log", rotation="100 MB", retention="7 days", serialize=True)

logger.info("Pipeline started | dataset=imagenet | split=train")
logger.warning("Missing annotations for 142 samples")
logger.error("DataLoader worker crashed | worker_id=3")
```

`serialize=True` writes JSON to the file — every field is queryable in log aggregators without any regex parsing.

---

### **`rich` — Formatted Terminal Output for CLIs and Notebooks**

`rich` renders tables, progress bars, syntax-highlighted code, and styled text in the terminal. It is the standard choice for CLI tools and interactive scripts where plain text output is not enough.

```python
from rich.console import Console
from rich.table import Table

console = Console()

table = Table(title="Model Evaluation Summary", show_lines=True)
table.add_column("Model",     style="cyan",   no_wrap=True)
table.add_column("Accuracy",  style="green")
table.add_column("F1 Score",  style="magenta")
table.add_column("Latency",   style="yellow")

table.add_row("ResNet50",          "94.2%", "0.941", "18ms")
table.add_row("EfficientNetV2-S",  "95.8%", "0.957", "22ms")
table.add_row("SmolLM2-1.7B",      "91.3%", "0.910", "45ms")

console.print(table)
```

```python
from rich.progress import track
import time

for step in track(range(100), description="Training epoch 1..."):
    time.sleep(0.02)
```

---

## **Common Mistakes and Gotchas**

| Mistake | Why it's wrong | Correct approach |
|---|---|---|
| `bool(input(...))` for yes/no | Any non-empty string is `True` — `"False"` is `True` | `input().strip().lower() == "true"` |
| `eval(input(...))` in a web app | Executes arbitrary code — severe security risk | `ast.literal_eval()` for literals only |
| `int(argv[2])` without guard | Crashes with `IndexError` if argument is missing | Check `len(argv)` or use `argparse` |
| `print()` in production code | No timestamp, level, or routing; cannot be filtered | Use `logging` or `loguru` |
| `logger.debug(f"value={x}")` | f-string always evaluated even when DEBUG is off | `logger.debug("value=%s", x)` |
| Hard-coding config in `input()` | Not scriptable; not testable; breaks automation | Use `argparse`, `click`, or `pydantic-settings` |
| `argv[1] + argv[2]` for numbers | String concatenation, not arithmetic | Cast with `int()` or `float()` first |

---

## **Quick Reference — Which Tool to Use**

| Scenario | Tool |
|---|---|
| Simple one-off interactive script | `input()` with `int()` / `float()` casting |
| Script with 2–3 flags, no deps allowed | `argparse` |
| CLI tool for a team or package | `click` |
| Modern type-hint-first project | `typer` |
| Validating JSON / API request body | `pydantic` `BaseModel` |
| Reading `.env` config at startup | `pydantic-settings` `BaseSettings` |
| Debug print during development | `print(f"{var=}")` |
| Any code running in production | `logging` or `loguru` |
| Rich terminal tables and progress bars | `rich` |