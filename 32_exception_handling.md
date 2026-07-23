# **Exception Handling**

Every Python program you write can fail in two fundamentally different ways — at *parse time* or at *run time*. The first kind stops the program before it ever starts; the second kind crashes the program while it is running. Exception handling is the entire discipline of catching and reacting to that second kind of failure gracefully, so that one bad input or one missing file does not bring down the whole program.

This file covers the mental model you need before you write a single `try`/`except` block: what counts as a "runtime error", how the Python Virtual Machine (PVM) reacts to an unhandled exception, and the full hierarchy of built-in exception classes.

---

## **What is an Exception?**

An **exception** is an unwanted, unexpected event that disturbs the normal flow of a program. It is *not* a syntax mistake — it is a situation that the language cannot figure out in advance: the user typed `"ten"` when you asked for an integer, the file you wanted to read does not exist, a network socket closed mid-read, or you divided by zero.

Because exceptions happen *while the program is running*, you (the programmer) cannot prevent them by writing the code differently. The only thing you can do is *anticipate* them and decide what the program should do instead of crashing.

### **Syntax Errors vs Runtime Errors**

In any programming language, there are two kinds of errors. The distinction matters because exception handling can only fix one of them.

| Error type | When it is caught | Who has to fix it | Can `try/except` help? |
|---|---|---|---|
| **Syntax error** | Before execution starts, by the interpreter | The programmer | No |
| **Runtime error (exception)** | During execution, by the PVM | The program itself (with `try/except`) | Yes |

**Example 1 — Syntax error (missing colon):**

```python
x = 10
if x == 10
 print("Hello")
```

```
SyntaxError: invalid syntax
```

The interpreter refuses to even start executing the file. You must fix the source code; there is no Python construct that will let the program "recover" from this.

**Example 2 — Syntax error (old `print` statement):**

```python
print "Hello"
```

```
SyntaxError: Missing parentheses in call to 'print'
```

Same story — Python 3 requires `print(...)`. The error is structural, so `try/except` cannot catch it. (Note: the `SyntaxError` *class* itself can be raised at runtime, for example by `eval()` — but the syntax errors in your `.py` files will always crash the interpreter before any `try` block can run.)

**Example 3 — Runtime errors (exceptions):**

```python
print(10 / 0)
```

```
ZeroDivisionError: division by zero
```

```python
print(10 / "ten")
```

```
TypeError: unsupported operand type(s) for /: 'int' and 'str'
```

```python
x = int(input("Enter Number: "))
```

If the user types `ten`, the program crashes:

```
ValueError: invalid literal for int() with base 10: 'ten'
```

All three of these are exceptions. They happen *while the program is running*, and they are exactly the class of errors that the `try/except` machinery was designed to handle.

**Note:** The exception handling concept is applicable for *runtime* errors, not for syntax errors. Don't try to wrap a SyntaxError in `try/except` and expect it to "fix" your code — it won't, because the interpreter never gets far enough to run your `try` block.

### **What Does "Handling" Actually Mean?**

The whole point of exception handling is **graceful termination** of the program. Graceful termination means three things:

1. **Resources are not blocked.** Open files get closed, database connections get released, locks get released.
2. **Important tasks are not skipped.** A failure in step 4 of a 7-step workflow should not leave steps 5, 6, 7 silently undone.
3. **The user gets a useful message** instead of a raw traceback dumped to the console.

It is important to understand what "handling" does *not* mean. Exception handling is **not** "repairing" the exception. You do not magically make the bad input become good input. Instead, you provide an *alternative path* — a fallback that lets the program continue in a sensible direction.

A classic illustration is a program that needs to read a file from a remote server in London. If the network call fails at runtime, the worst thing the program can do is print a traceback and die. A much better behavior is to fall back to a local copy of the file and continue. The remote file is still missing — we did not "fix" that — but the program is still running.

```python
# Conceptual illustration — not meant to be run
def load_config():
 try:
 # Primary path: try the remote config first
 return read_remote_file("london-server", "config.json")
 except (ConnectionError, TimeoutError, FileNotFoundError):
 # Fallback path: silently switch to the local copy
 return read_local_file("config.json")
```

The point is: exception handling is about *what the program does next*, not about *what caused the problem*.

### **Common Interview-Style Q&A**

**Q1. What is an exception?**
An exception is an unwanted and unexpected event that occurs at runtime and disturbs the normal flow of a program. In Python, every exception is represented by a class instance, and the interpreter raises it to signal that something went wrong.

**Q2. What is the purpose of exception handling?**
The purpose of exception handling is to ensure *graceful termination* — the program finishes its important work, releases its resources, and gives the user a meaningful message, even when something goes wrong at runtime. It also isolates the *error-handling code* from the *normal logic code*, which makes both easier to read.

**Q3. What is the *meaning* of exception handling?**
It does *not* mean repairing the exception (you cannot "fix" the fact that the user typed `"ten"`). It means providing an alternative way for the program to continue. You define a fallback path, and the program uses that path instead of crashing.

---

## **Default Exception Handling in Python**

Every exception in Python is an object. For every exception type, there is a corresponding class. When something goes wrong, the Python Virtual Machine (PVM) creates an instance of the appropriate exception class and starts looking for handling code.

If no handling code is found, the PVM does three things:

1. It prints a **traceback** showing exactly where the exception happened.
2. It prints the **exception type and message** (e.g. `ZeroDivisionError: division by zero`).
3. It **terminates the program abnormally** — every line of code that was supposed to run *after* the exception is skipped.

**Example — default behavior, no handling:**

```python
print("Hello")
print(10 / 0)
print("Hi")
```

```
Hello
Traceback (most recent call last):
 File "test.py", line 2, in <module>
 print(10 / 0)
ZeroDivisionError: division by zero
```

Notice three things:

- `Hello` *was* printed — the PVM only stopped when it hit `10 / 0`.
- `Hi` was *not* printed — the moment the exception fired, the PVM stopped executing this script.
- The error message shows you the line number and the offending expression, so you know exactly where to look.

This is what the PVM does for you "for free". The problem is that "for free" still ends with your program dead. Customized exception handling — using `try/except` — gives you a way to take back control.

---

## **Exception Hierarchy in Python**

Every exception class in Python either directly or indirectly inherits from `BaseException`. This forms a tree, and understanding the tree is essential because of one important rule: **an `except` clause that catches a parent class will also catch every child class**.

```
BaseException
├── BaseExceptionGroup
├── GeneratorExit
├── KeyboardInterrupt
├── SystemExit
└── Exception
 ├── StopIteration
 ├── StopAsyncIteration
 ├── ArithmeticError
 │ ├── FloatingPointError
 │ ├── OverflowError
 │ └── ZeroDivisionError
 ├── AssertionError
 ├── AttributeError
 ├── BufferError
 ├── EOFError
 ├── ExceptionGroup
 ├── ImportError
 │ └── ModuleNotFoundError
 ├── LookupError
 │ ├── IndexError
 │ └── KeyError
 ├── MemoryError
 ├── NameError
 │ └── UnboundLocalError
 ├── OSError
 │ ├── BlockingIOError
 │ ├── ChildProcessError
 │ ├── ConnectionError
 │ │ ├── BrokenPipeError
 │ │ ├── ConnectionAbortedError
 │ │ ├── ConnectionRefusedError
 │ │ └── ConnectionResetError
 │ ├── FileExistsError
 │ ├── FileNotFoundError
 │ ├── InterruptedError
 │ ├── IsADirectoryError
 │ ├── NotADirectoryError
 │ ├── PermissionError
 │ ├── ProcessLookupError
 │ └── TimeoutError
 ├── ReferenceError
 ├── RuntimeError
 │ ├── NotImplementedError
 │ ├── PythonFinalizationError
 │ └── RecursionError
 ├── SyntaxError
 │ ├── IndentationError
 │ │ └── TabError
 ├── SystemError
 ├── TypeError
 ├── ValueError
 │ ├── UnicodeError
 │ │ ├── UnicodeDecodeError
 │ │ ├── UnicodeEncodeError
 │ │ └── UnicodeTranslateError
 └── Warning
 ├── BytesWarning
 ├── DeprecationWarning
 ├── EncodingWarning
 ├── FutureWarning
 ├── ImportWarning
 ├── PendingDeprecationWarning
 ├── ResourceWarning
 ├── RuntimeWarning
 ├── SyntaxWarning
 ├── UnicodeWarning
 └── UserWarning
```

### **The Important Split: `BaseException` vs `Exception`**

`BaseException` is the absolute root. Four of its direct children are *system* events that you almost never want to catch:

| Class | When it is raised | Why you should not catch it broadly |
|---|---|---|
| `SystemExit` | `sys.exit()` is called | Catching it would prevent the program from ever exiting. |
| `KeyboardInterrupt` | The user hits `Ctrl+C` | Catching it would make your program impossible to interrupt. |
| `GeneratorExit` | A generator's `close()` is called | Internal protocol — leave it alone. |
| `Exception` | All "regular" runtime errors | This is the one you actually catch. |

**`Exception` is the parent of every "normal" runtime error** — `ZeroDivisionError`, `KeyError`, `ValueError`, `TypeError`, `FileNotFoundError`, and so on. PEP 8 (the official Python style guide) is explicit about this: when you write `except` clauses, catch `Exception` (or a subclass), not `BaseException`. Catching `BaseException` will swallow `Ctrl+C` and `sys.exit()`, and your program becomes unkillable.

**Practical consequence — polymorphism in `except`:**

```python
try:
 x = int(input("Enter a number: "))
 result = 100 / x
except ArithmeticError as e:
 # This catches ZeroDivisionError, OverflowError, FloatingPointError, ...
 print("Arithmetic problem:", e)
```

```
Enter a number: 0
Arithmetic problem: division by zero
```

Because `ZeroDivisionError` is a subclass of `ArithmeticError`, one `except ArithmeticError` line covers all three of its children. This is powerful — but it is also why you should write `except` clauses in order from **most specific to most general**. The full mechanics of *why order matters* are covered in `python_try_except_else_finally.md`.

**Example — confirming the hierarchy at runtime:**

```python
print(issubclass(ZeroDivisionError, ArithmeticError))
print(issubclass(ArithmeticError, Exception))
print(issubclass(Exception, BaseException))
print(issubclass(KeyboardInterrupt, BaseException))
print(issubclass(KeyboardInterrupt, Exception))
```

```
True
True
True
True
False
```

That last line is the proof. `KeyboardInterrupt` is a `BaseException`, but it is *not* an `Exception`. If you write `except Exception:`, the user can still hit `Ctrl+C` to kill your program. If you write `except BaseException:`, they cannot.

---

## **Predefined vs User-Defined Exceptions**

There are two broad categories of exceptions:

| Category | Who defines them | Who raises them | Example |
|---|---|---|---|
| **Predefined (built-in) exceptions** | The Python language itself | The PVM, automatically | `ZeroDivisionError`, `KeyError`, `ValueError` |
| **User-defined (custom) exceptions** | You, the programmer | You, via the `raise` keyword | `InsufficientFundsError`, `TooYoungException` |

Predefined exceptions are covered in detail across this file and `python_try_except_else_finally.md`. User-defined exceptions — including the `raise` keyword, exception chaining with `raise from`, and PEP 8 conventions like the `Error` suffix — are covered in `python_custom_exceptions.md`.

---

## **Examples**

### **Example 1 — Syntax error cannot be caught**

```python
try:
 eval("x = 10 if True") # eval parses at runtime, so SyntaxError becomes a runtime exception here
except SyntaxError as e:
 print("Caught a syntax problem in eval():", e)
```

```
Caught a syntax problem in eval(): invalid syntax (<string>, line 1)
```

Note: the `SyntaxError` was *raised* at runtime (because `eval` parses its input string when called), so `try/except` *did* catch it. But if you put a literal `SyntaxError` directly in a `.py` file, the file will not run at all — there is nothing to catch.

### **Example 2 — Three runtime errors, all unhandled**

```python
print("step 1: setup complete")
print(10 / 0) # ZeroDivisionError
print("step 3: this never runs")
```

```
step 1: setup complete
Traceback (most recent call last):
 File "test.py", line 2, in <module>
 print(10 / 0)
ZeroDivisionError: division by zero
```

### **Example 3 — Walking the hierarchy with `issubclass`**

```python
for pair in [
 (ZeroDivisionError, ArithmeticError),
 (FileNotFoundError, OSError),
 (KeyError, LookupError),
 (ValueError, Exception),
 (IndentationError, SyntaxError),
 (UnicodeDecodeError, UnicodeError),
]:
 print(f"{pair[0].__name__} is subclass of {pair[1].__name__}? {issubclass(*pair)}")
```

```
ZeroDivisionError is subclass of ArithmeticError? True
FileNotFoundError is subclass of OSError? True
KeyError is subclass of LookupError? True
ValueError is subclass of Exception? True
IndentationError is subclass of SyntaxError? True
UnicodeDecodeError is subclass of UnicodeError? True
```

### **Example 4 — Confirming `Exception` does not cover system events**

```python
import sys

print("Exception is BaseException?", issubclass(Exception, BaseException))
print("SystemExit is Exception? ", issubclass(SystemExit, Exception))
print("KeyboardInterrupt is Exception?", issubclass(KeyboardInterrupt, Exception))
print("KeyboardInterrupt is BaseException?", issubclass(KeyboardInterrupt, BaseException))
```

```
Exception is BaseException? True
SystemExit is Exception? False
KeyboardInterrupt is Exception? False
KeyboardInterrupt is BaseException? True
```

### **Example 5 — Default termination kills the rest of the program**

```python
def process_order(items):
 print(f"Received {len(items)} items")
 total = sum(items) / 0 # ZeroDivisionError
 print("Total:", total) # never runs

print("start of program")
process_order([10, 20, 30])
print("end of program") # never runs
```

```
start of program
Received 3 items
Traceback (most recent call last):
 File "test.py", line 8, in <module>
 process_order([10, 20, 30])
 File "test.py", line 3, in process_order
 total = sum(items) / 0
ZeroDivisionError: division by zero
```

### **Example 6 — The exception object is a real class instance**

```python
try:
 1 / 0
except ZeroDivisionError as err:
 print("type: ", type(err).__name__)
 print("class: ", err.__class__.__name__)
 print("message: ", str(err))
 print("args: ", err.args)
```

```
type: ZeroDivisionError
class: ZeroDivisionError
message: division by zero
args: ('division by zero',)
```

Useful when you want to log the *type* of the error (e.g. for metrics or alerts) rather than just the message.

### **Example 7 — Bare `except` is dangerous (it catches Ctrl+C too)**

```python
import time

try:
 print("Press Ctrl+C to interrupt...")
 time.sleep(5)
 print("If you see this, Ctrl+C did NOT work")
except BaseException:
 print("Caught everything including Ctrl+C — this is why 'except BaseException' is a bad idea")
```

If you run this and hit `Ctrl+C` during the 5-second sleep, the message "Caught everything..." will print instead of the program dying. This is exactly why PEP 8 says: catch `Exception`, not `BaseException`.

---

## **Quick Reference Summary**

### **Syntax Errors vs Runtime Errors**

| Aspect | Syntax error | Runtime error (exception) |
|---|---|---|
| Detected | Before execution | During execution |
| Caused by | Invalid code structure | Invalid runtime conditions |
| Caught by `try/except`? | No | Yes |
| Program runs at all? | No | Yes (until the error) |
| Example | `if x == 10` (missing `:`) | `10 / 0` |
| Fix is your job? | Always (code-level) | Either fix or `try/except` |

### **Top of the Exception Hierarchy**

| Class | Catch it? | Reason |
|---|---|---|
| `BaseException` | Almost never | Catches `SystemExit` / `KeyboardInterrupt` — program becomes unkillable. |
| `Exception` | Safe default for broad catches | Covers all "regular" runtime errors. |
| `ArithmeticError` | Specific catch for math | Parent of `ZeroDivisionError`, `OverflowError`, `FloatingPointError`. |
| `LookupError` | Specific catch for containers | Parent of `IndexError`, `KeyError`. |
| `OSError` | Specific catch for I/O | Parent of `FileNotFoundError`, `PermissionError`, etc. |

### **Most Common Built-in Exceptions**

| Exception | Raised when |
|---|---|
| `ZeroDivisionError` | You divide (or modulo) by zero. |
| `ValueError` | A function gets the right type but the wrong value (`int("ten")`). |
| `TypeError` | An operation is applied to the wrong type (`"a" + 1`). |
| `KeyError` | A `dict` lookup misses (`d["nope"]`). |
| `IndexError` | A sequence index is out of range. |
| `FileNotFoundError` | `open()` on a path that does not exist. |
| `AttributeError` | You reference an attribute the object does not have. |
| `NameError` | You reference a name that is not defined. |
| `ImportError` / `ModuleNotFoundError` | A module cannot be imported. |
| `IndentationError` | Bad indentation (this *can* slip through `eval`/`exec`). |

---

## **Practice and Next Steps**

1. **Catch the type, log the message.** Wrap a `dict` lookup in `try/except KeyError` and print *both* the exception type and the message — practice reading the `__class__.__name__` and `str(err)` of an exception object.
2. **Traceback reading drill.** Run each of the runtime errors in the table above on its own, then look at the traceback and identify: which line raised it, what class it belongs to, and which parent class you would catch to handle the whole family.
3. **The hierarchy by hand.** Pick three leaf exceptions from the tree (e.g. `KeyError`, `ZeroDivisionError`, `FileNotFoundError`) and write down their full parent chain up to `BaseException`. Then verify with `cls.__mro__`.
4. **Build a tiny calculator.** Prompt the user for two numbers, divide them, and handle `ValueError` (non-numeric input) and `ZeroDivisionError` (zero divisor) separately. Do not use a bare `except:`.
5. **Bare `except` experiment.** Write a small program with `try: input() except: print("got it")` and try to kill it with `Ctrl+C`. Compare against the same program using `except Exception:`. Observe the difference.
6. **Convert tracebacks to your own messages.** For each of the three "most common" exceptions in the table, write code that turns the raw exception into a single user-friendly sentence (e.g. `"Please enter a number, not text"` for `ValueError`).
7. **Read the official docs.** Skim the [Built-in Exceptions](https://docs.python.org/3/library/exceptions.html) page and note at least three exceptions you have never used before — you will see them again.
