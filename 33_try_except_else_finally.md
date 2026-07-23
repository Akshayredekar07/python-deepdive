# **try / except / else / finally**

This file is the working part of Python exception handling. The previous file established the *what* and the *why*; this one shows the *how* — the exact rules of how `try`, `except`, `else`, and `finally` interact, what runs in which order, and which combinations are even legal Python.

By the end of this file you should be able to look at any `try/except/else/finally` block and predict, statement by statement, what will run.

---

## **What is a "Risky Code" Block?**

Customized exception handling follows one simple rule:

- Code that **might raise** an exception → goes inside a `try` block (this is called "risky code").
- Code that **handles** the exception → goes inside an `except` block (this is the "handling code" or "alternative code").

```python
try:
 # Risky code — anything that might raise goes here
except SomeException:
 # Handling code — the alternative path
```

That is the whole shape. Everything else in this file is decoration on that skeleton.

### **Example — Without try/except (abnormal termination)**

```python
print("stmt-1")
print(10 / 0)
print("stmt-3")
```

```
stmt-1
ZeroDivisionError: division by zero
```

The PVM prints `stmt-1`, then crashes on `10 / 0`. `stmt-3` never runs. This is **abnormal (non-graceful) termination** — the program died in the middle.

### **Example — With try/except (graceful termination)**

```python
print("stmt-1")
try:
 print(10 / 0)
except ZeroDivisionError:
 print(10 / 2)
print("stmt-3")
```

```
stmt-1
5.0
stmt-3
```

This is **graceful termination** — the program ran into a problem, but it absorbed the problem, chose an alternative (`10 / 2` instead of `10 / 0`), and continued all the way to `stmt-3`. The user never saw a traceback.

---

## **Control Flow in try / except**

The cleanest way to think about `try/except` is as a small state machine with four possible cases. The cases differ based on (a) whether an exception was raised in the `try` block, and (b) whether a matching `except` block was found.

```
try:
 stmt-1
 stmt-2
 stmt-3
except XXX:
 stmt-4
stmt-5
```

### **Case 1 — No exception**

```
Execution: stmt-1, stmt-2, stmt-3, stmt-5
Termination: Normal
```

The `try` block runs to completion, the `except` block is skipped, and execution continues to `stmt-5`.

### **Case 2 — Exception at stmt-2, matching except block**

```
Execution: stmt-1, stmt-4, stmt-5
Termination: Normal
```

`stmt-2` raises. The PVM looks for a matching `except` block, finds it, runs it as `stmt-4`, then continues to `stmt-5`.

### **Case 3 — Exception at stmt-2, no matching except block**

```
Execution: stmt-1
Termination: Abnormal
```

`stmt-2` raises. The PVM finds *no* matching `except` block, so it propagates the exception upward. `stmt-4` and `stmt-5` are both skipped.

### **Case 4 — Exception at stmt-4 or stmt-5**

```
Termination: Always Abnormal
```

Once you leave the `try` block, you are back in "normal" Python. An exception in the handler or after the handler is not caught by the handler itself.

### **Conclusions**

- Inside the `try` block, **once an exception fires, the rest of the `try` block does not run**, even if a matching `except` block catches it. The PVM jumps directly from the failing line to the matching handler.
- Only put *risky* code inside the `try` block. Keep the block as small as possible. A 100-line `try` is a debugging nightmare.
- Exceptions can also be raised inside the `except` block. They are *not* caught by the same `try/except` and will propagate up.
- Any exception raised outside the `try` block (e.g. in `stmt-4` or `stmt-5`) will result in abnormal termination.

---

## **Printing Exception Information**

When the PVM catches an exception, it builds an exception *object* containing everything you might want to know: the message, the type, and the traceback. The `except ... as msg` syntax lets you grab that object so you can log it, re-raise it, or just print it nicely.

```python
try:
 print(10 / 0)
except ZeroDivisionError as msg:
 print("Exception raised and its description is:", msg)
```

```
Exception raised and its description is: division by zero
```

The variable `msg` *is* the exception object. Calling `print(msg)` calls `str(msg)`, which returns the human-readable description.

### **Three useful ways to inspect the exception**

```python
# 1) Just the message
try:
 print(10 / 0)
except ZeroDivisionError as msg:
 print(msg)
```

```
division by zero
```

```python
# 2) Get the class name explicitly
try:
 print(10 / 0)
except ZeroDivisionError as msg:
 print("Exception class:", msg.__class__.__name__)
```

```
Exception class: ZeroDivisionError
```

```python
# 3) Catch the broader parent and still recover the original class
try:
 x = int(input("10.4")) # user typed something non-numeric
except Exception as msg:
 print("Caught class:", msg.__class__.__name__)
 print("Message: ", msg)
```

```
Caught class: ValueError
Message: invalid literal for int() with base 10: '10.4'
```

That third example is a small but very useful pattern: by catching the parent (`Exception`) and reading `__class__.__name__`, you can log "what kind of error" without writing ten separate `except` clauses. In production code this is how you build dashboards that count errors by type.

---

## **Try with Multiple Except Blocks**

Different exception types deserve different responses. The most common way to express that is **one `except` block per type**, listed top-to-bottom.

```python
try:
 # Risky code
except ZeroDivisionError:
 # Alternative arithmetic
except FileNotFoundError:
 # Use a local file
```

When multiple `except` blocks are present, the PVM walks them top-to-bottom and runs the **first** one whose class matches the raised exception. Subsequent blocks are not checked.

### **Example — Division calculator with two specific handlers**

```python
try:
 x = int(input("Enter First Number: "))
 y = int(input("Enter Second Number: "))
 print(x / y)
except ZeroDivisionError:
 print("Can't Divide with Zero")
except ValueError:
 print("Please provide int value only")
```

Three run-throughs:

```
Enter First Number: 10
Enter Second Number: 2
5.0
```

```
Enter First Number: 10
Enter Second Number: 0
Can't Divide with Zero
```

```
Enter First Number: 10
Enter Second Number: ten
Please provide int value only
```

### **Order of `except` Blocks Matters**

Python checks `except` blocks **from top to bottom**, and the first match wins. This means you must order them from **most specific to most general**, otherwise the parent class will swallow the child class before the child's handler ever gets a chance.

```python
try:
 x = int(input("Enter First Number: "))
 y = int(input("Enter Second Number: "))
 print(x / y)
except ArithmeticError: # parent — catches ZeroDivisionError too
 print("ArithmeticError")
except ZeroDivisionError: # dead code — never reached
 print("ZeroDivisionError")
```

```
Enter First Number: 10
Enter Second Number: 0
ArithmeticError
```

The `ZeroDivisionError` line never executes, because `ArithmeticError` matches first. The rule to remember: **narrow handlers above, broad handlers below.**

---

## **Single Except Block for Multiple Exceptions**

If you want the same handling code to run for several different exception types, you can group them in a single `except` clause using a tuple. Internally Python treats it as a tuple of exception classes.

```python
except (Exception1, Exception2, ...):
 # shared handling code
except (Exception1, Exception2, ...) as msg:
 # same, but msg captures the exception object
```

### **Example — one handler for two error types**

```python
try:
 x = int(input("Enter First Number: "))
 y = int(input("Enter Second Number: "))
 print(x / y)
except (ZeroDivisionError, ValueError) as msg:
 print("Please provide valid numbers only. Problem:", msg)
```

```
Enter First Number: 10
Enter Second Number: 0
Please provide valid numbers only. Problem: division by zero
```

```
Enter First Number: 10
Enter Second Number: ten
Please provide valid numbers only. Problem: invalid literal for int() with base 10: 'ten'
```

This is a very common, very readable pattern when the response is the same for multiple errors.

### **Real-world pattern — list lookup with two distinct errors**

```python
numbers = [1, 2, 3]

try:
 index = int(input("Enter an index: "))
 print("Value at index:", numbers[index])
except ValueError as e:
 print("Invalid input! Description:", e)
except IndexError as e:
 print("Index out of range! Description:", e)
except Exception as e:
 print("Some other exception. Class:", e.__class__.__name__, "Msg:", e)
```

If the user types `9` (a valid integer, but out of range):

```
Some other exception. Class: IndexError Msg: list index out of range
```

Wait — the `IndexError` handler should have caught that. Let's re-run the *correct* version:

```python
numbers = [1, 2, 3]

try:
 index = int(input("Enter an index: "))
 print("Value at index:", numbers[index])
except ValueError as e:
 print("Invalid input! Description:", e)
except IndexError as e:
 print("Index out of range! Description:", e)
```

```
Enter an index: 9
Index out of range! Description: list index out of range
```

The takeaway: when you have specific handlers, write them in order. Do not let a catch-all `Exception` at the end hide problems you already know how to handle.

---

## **Default Except Block**

A bare `except:` with no class name will catch *any* exception (anything that is a subclass of `BaseException`, including `SystemExit` and `KeyboardInterrupt`). It is the most aggressive catch possible.

```python
try:
 # risky code
except:
 # runs for literally any exception
```

### **Example — default except as the last resort**

```python
try:
 x = int(input("Enter First Number: "))
 y = int(input("Enter Second Number: "))
 print(x / y)
except ZeroDivisionError:
 print("ZeroDivisionError: Can't divide with zero")
except:
 print("Default Except: Please provide valid input only")
```

```
Enter First Number: 10
Enter Second Number: 0
ZeroDivisionError: Can't divide with zero
```

```
Enter First Number: 10
Enter Second Number: ten
Default Except: Please provide valid input only
```

The `ZeroDivisionError` handler runs first because it is listed first; the bare `except` only handles whatever the specific handlers did not.

### **The hard rule — bare `except` must be last**

```python
try:
 print(10 / 0)
except: # ← bare except first
 print("Default Except")
except ZeroDivisionError: # ← SyntaxError: default 'except:' must be last
 print("ZeroDivisionError")
```

```
SyntaxError: default 'except:' must be last
```

Python enforces this at parse time. A bare `except` matches *everything*, so if it were not the last block, no `except` block after it would ever run — making those blocks dead code. The parser saves you from that footgun.

### **All legal `except` shapes**

| Form | Catches |
|---|---|
| `except ZeroDivisionError:` | Only `ZeroDivisionError` (and any subclass) |
| `except ZeroDivisionError as msg:` | Same, plus `msg` holds the exception object |
| `except (ZeroDivisionError, ValueError):` | Any of the listed types |
| `except (ZeroDivisionError, ValueError) as msg:` | Same, plus `msg` holds the exception |
| `except:` | Anything (must be last) |

---

## **The `finally` Block**

The `finally` block is for **cleanup code** — work that absolutely must run no matter what. The classic example is closing a file, but the pattern applies to any resource: database connections, network sockets, locks, temporary files.

Why is `finally` needed at all? Because cleanup cannot reliably go in either of the other two places:

- **Cleanup in `try`?** There is no guarantee every line of the `try` block will run. If an exception fires on line 3 of a 5-line `try`, lines 4 and 5 are skipped — including your cleanup.
- **Cleanup in `except`?** The `except` block does not run at all if no exception is raised. You would have to duplicate the cleanup in the `try` block, which defeats the purpose.

`finally` solves both problems. It runs whether the `try` block raised or not, whether the `except` block caught the exception or not.

```python
try:
 # Risky code
except:
 # Handling code
finally:
 # Cleanup code — always runs
```

### **Case 1 — No exception**

```python
try:
 print("try")
except:
 print("except")
finally:
 print("finally")
```

```
try
finally
```

`except` is skipped (nothing went wrong); `finally` still runs.

### **Case 2 — Exception raised and handled**

```python
try:
 print("try")
 print(10 / 0) # raises ZeroDivisionError
except ZeroDivisionError:
 print("except")
finally:
 print("finally")
```

```
try
except
finally
```

The `try` block raised, the matching `except` block caught it, then `finally` ran.

### **Case 3 — Exception raised but not handled**

```python
try:
 print("try")
 print(10 / 0) # raises ZeroDivisionError
except NameError: # wrong type — does not match
 print("except")
finally:
 print("finally")
```

```
try
finally
---------------------------------------------------------------------------
ZeroDivisionError Traceback (most recent call last)
 ...
ZeroDivisionError: division by zero
```

The `except` block did *not* match. But `finally` ran *before* the unhandled exception propagated up and crashed the program. This is one of `finally`'s superpowers — it runs even when the program is about to die.

### **The one exception to "always" — `os._exit(0)`**

The only situation in which `finally` will **not** run is when the program is terminated using `os._exit(0)`. That call kills the process immediately, before Python's cleanup machinery gets a chance to run.

```python
import os

try:
 print("try")
 os._exit(0) # hard exit — finally does NOT run
except:
 print("except")
finally:
 print("finally") # never reached
```

```
try
```

`os._exit(0)` is the nuclear option. It is rarely used in normal application code; you will mostly see it in scripts that need to exit without running any atexit hooks (e.g. some build tools or test harnesses). For normal cleanup, `finally` is your safety net.

---

## **The `else` Block**

The `else` block runs **only if the `try` block did not raise an exception**. It is the place to put code that depends on the success of the `try` block, so that the "happy path" stays out of the `try` block itself.

```python
try:
 print('try')
except:
 print('except')
else:
 print('else')
finally:
 print('finally')
```

```
try
else
finally
```

### **Why bother with `else`?**

The recommended pattern in modern Python is:

- **`try`** — the smallest possible amount of risky code.
- **`except`** — only the exception-handling logic.
- **`else`** — the success-path code that uses the result of the `try` block.
- **`finally`** — the cleanup.

This split makes the code dramatically easier to read: success and failure are visually separated, and the `try` block is tight.

### **Example — file reading with proper structure**

```python
f = None
try:
 f = open('abc.txt', 'r') # risky
except FileNotFoundError:
 print('Specified file not found')
else:
 print(f.read()) # success path — only runs if open() succeeded
finally:
 if f is not None:
 f.close()
 print("Cleanup attempted")
```

If `abc.txt` exists:

```
Hey brother stay updated!!
Cleanup attempted
```

If it doesn't:

```
Specified file not found
Cleanup attempted
```

Note: in modern code, the `with open(...) as f:` statement is preferred over this manual `try/except/else/finally`. The `with` statement guarantees the file gets closed. Exception handling still matters for the *other* things that can go wrong (file does not exist, permission denied, etc.).

### **Combined example — `try/except/else/finally` end-to-end**

```python
def divide_numbers(a, b):
 try:
 result = a / b
 except ZeroDivisionError as e:
 print(f"Error: {e}")
 except TypeError as e:
 print(f"Error: {e}")
 else:
 # Runs only if no exception fired in try
 print(f"Division successful! The result is {result}")
 finally:
 # Runs no matter what
 print("Execution completed.")

print("Case 1: Valid Division")
divide_numbers(10, 2)

print("\nCase 2: Division by Zero")
divide_numbers(10, 0)

print("\nCase 3: Invalid Input Types")
divide_numbers(10, "two")
```

```
Case 1: Valid Division
Division successful! The result is 5.0
Execution completed.

Case 2: Division by Zero
Error: division by zero
Execution completed.

Case 3: Invalid Input Types
Error: unsupported operand type(s) for /: 'int' and 'str'
Execution completed.
```

This is the canonical "complete" exception handling pattern. Note carefully: in Case 1 the `else` block ran (success); in Cases 2 and 3 it did not. In *all* three cases, `finally` ran.

---

## **`return` and `finally` Interact**

A surprising number of bugs in real codebases come from misunderstanding how `return` interacts with `finally`. The rule is simple and absolute:

**`finally` overrides any `return` in the `try` or `except` block.**

### **Case A — `return` in try, nothing in finally**

```python
def f1():
 try:
 return 10
 except:
 print('except')
 finally:
 print('Finally')

print(f1())
```

```
Finally
10
```

The function returns `10`, but `finally` runs *before* the return value is actually delivered to the caller. Both messages print.

### **Case B — `return` in finally beats `return` in try**

```python
def f1():
 try:
 return 10
 except:
 print('except')
 finally:
 return 20 # ← this wins

print(f1())
```

```
20
```

The function *technically* returns `10` from the `try` block, but because `finally` runs before the value leaves the function, and `finally` has its own `return 20`, the caller sees `20`. **A `return` in `finally` swallows any earlier return value.**

This is almost always a bug. Do not put `return` in `finally` unless you specifically want to override earlier returns.

### **Case C — exception caught, finally still runs, function returns the captured value**

```python
def f2():
 try:
 print('Namaste')
 return 10
 except:
 print('except')
 finally:
 print('finally')

f2()
```

```
Namaste
finally
10
```

(Note: `f2()` is called but the return value is discarded because we did not `print(f2())` — but `10` is the value the function hands back.)

### **Case D — `return` in both except and finally**

```python
def f3():
 try:
 return 1
 except:
 return 2
 finally:
 return 3

print(f3())
```

```
3
```

`finally` wins. Always.

### **Case E — `return` in try is None when except fires**

```python
def f1():
 try:
 print(10 / 0)
 return 10
 except:
 print('except')
 finally:
 print('finally')

print(f1())
```

```
except
finally
None
```

The `try` block raised before reaching `return 10`, so there is no value to return from `try`. The `except` block runs (printing `except`) and does not have a `return`, so the function falls off the end. Then `finally` runs (printing `finally`). The implicit return is `None`, which is what the caller sees.

**Key takeaway:** `finally` is for *cleanup* (closing files, releasing locks, logging), not for *value production*. Putting `return` in `finally` is a code smell that hides the real return path from anyone reading the function.

---

## **Control Flow in try / except / finally**

Adding `finally` to the earlier state machine gives you a more complete picture. The structure is:

```
try:
 stmt-1
 stmt-2
 stmt-3
except:
 stmt-4
finally:
 stmt-5
stmt-6
```

| Case | What happens | Execution order | Termination |
|---|---|---|---|
| 1 | No exception | 1, 2, 3, 5, 6 | Normal |
| 2 | Exception at stmt-2, except matches | 1, 4, 5, 6 | Normal |
| 3 | Exception at stmt-2, except does not match | 1, 5 | Abnormal (stmt-6 skipped) |
| 4 | Exception at stmt-4 | 1, 5 | Abnormal (stmt-6 skipped) |
| 5 | Exception at stmt-5 or stmt-6 | — | Abnormal |

The big addition over plain `try/except` is this: **if the `try` block was entered at all, the `finally` block always runs** — even when the program is about to die of an unhandled exception. That is precisely why `finally` is the right place to close files and release locks.

---

## **Nested try / except / finally**

You can put a `try/except/finally` block inside *any* of the `try`, `except`, or `finally` blocks of an outer `try/except/finally`. The general rule:

- **General risky code** → outer `try`
- **High-risk / specific risky code** → inner `try`
- If the inner `try` raises and the inner `except` matches → handled locally.
- If the inner `try` raises and the inner `except` does *not* match → falls out to the outer `except`.

### **Example — clean nesting**

```python
try:
 print("outer try block")
 try:
 print("Inner try block")
 print(10 / 0)
 except ZeroDivisionError:
 print("Inner except block")
 finally:
 print("Inner finally block")
except:
 print("outer except block")
finally:
 print("outer finally block")
print("Last statement")
```

```
outer try block
Inner try block
Inner except block
Inner finally block
outer finally block
Last statement
```

Notice the order: inner `except` runs first (it caught the local error), then inner `finally`, then outer `finally`, then the rest of the program. The outer `except` did not run because the inner one already handled the exception.

### **Control Flow in Nested try / except / finally**

```
try:
 stmt-1, stmt-2, stmt-3
 try:
 stmt-4, stmt-5, stmt-6
 except X:
 stmt-7
 finally:
 stmt-8, stmt-9
except Y:
 stmt-10
finally:
 stmt-11
stmt-12
```

| Case | Trigger | Execution | Termination |
|---|---|---|---|
| 1 | No exception | 1, 2, 3, 4, 5, 6, 8, 9, 11, 12 | Normal |
| 2 | Exception at stmt-2, outer except matches | 1, 10, 11, 12 | Normal |
| 3 | Exception at stmt-2, outer except does not match | 1, 11 | Abnormal |
| 4 | Exception at stmt-5, inner except matches | 1, 2, 3, 4, 7, 8, 9, 11, 12 | Normal |
| 5 | Exception at stmt-5, inner does not match, outer matches | 1, 2, 3, 4, 8, 10, 11, 12 | Normal |
| 6 | Exception at stmt-5, neither matches | 1, 2, 3, 4, 8, 11 | Abnormal |
| 7 | Exception at stmt-7, outer matches | 1, 2, 3, 4, 5, 6, 8, 10, 11, 12 | Normal |
| 8 | Exception at stmt-7, outer does not match | 1, 2, 3, 4, 5, 6, 8, 11 | Abnormal |
| 9 | Exception at stmt-8, outer matches | 1, 2, 3, 4, 5, 6, 7, 10, 11, 12 | Normal |
| 10 | Exception at stmt-8, outer does not match | 1, 2, 3, 4, 5, 6, 8, 11 | Abnormal |
| 11 | Exception at stmt-9, outer matches | 1, 2, 3, 4, 5, 6, 8, 10, 11, 12 | Normal |
| 12 | Exception at stmt-9, outer does not match | 1, 2, 3, 4, 5, 6, 8, 11 | Abnormal |
| 13 | Exception at stmt-10 | 1, 2, 3, 4, 5, 6, 8, 11 | Abnormal |
| 14 | Exception at stmt-11 or stmt-12 | — | Abnormal |

The key insight: **`finally` blocks always run if their `try` block was entered**, even if the program is about to die.

---

## **Valid and Invalid Combinations of try / except / else / finally**

The Python grammar is strict about which combinations of these four keywords are legal. Here is the full list of rules:

1. A `try` block **must** be followed by at least one `except` block *or* one `finally` block. A `try` with neither is a `SyntaxError`.
2. An `except` block **must** have a matching `try`. An `except` floating in space is a `SyntaxError`.
3. A `finally` block **must** have a matching `try`. A `finally` floating in space is a `SyntaxError`.
4. You can have **multiple `except` blocks** for a single `try`, but you can have **at most one `finally`**.
5. An `else` block **requires** at least one `except` block in the same `try`. `else` without `except` is invalid.
6. The order of the four is fixed: `try → except(s) → else → finally`. Anything else is a `SyntaxError`.
7. Nesting of `try/except/else/finally` inside any of the four outer blocks is always allowed.

### **Cheat sheet of valid / invalid patterns**

| # | Pattern | Valid? | Why |
|---|---|---|---|
| 1 | `try: pass` | | `try` needs `except` or `finally` |
| 2 | `except: pass` | | `except` needs a `try` |
| 3 | `else: pass` | | `else` needs a `try` *and* at least one `except` |
| 4 | `finally: pass` | | `finally` needs a `try` |
| 5 | `try / except` | | Minimal valid form |
| 6 | `try / finally` | | For "do something no matter what" |
| 7 | `try / except / else` | | Standard form |
| 8 | `try / else` | | `else` requires `except` |
| 9 | `try / else / finally` | | `else` requires `except` |
| 10 | `try / except / except` | | Multiple specific handlers |
| 11 | `try / except / else / else` | | Only one `else` allowed |
| 12 | `try / except / finally / finally` | | Only one `finally` allowed |
| 13 | `try / except / try / except` (nested in try) | | Nesting always allowed |
| 14 | `try / except / try / finally` (nested in except) | | Nesting always allowed |
| 15 | `try / except / try / else` (nested) | | Inner `else` needs an inner `except` |
| 16 | `try / except / try / except / finally` (nested in try) | | Full nested form |

### **The single most useful rule to remember**

If you remember nothing else: **a `try` block must be followed by at least one `except` or one `finally`.** Everything else flows from that.

---

## **Examples**

### **Example 1 — Order matters: parent before child (dead code)**

```python
# DO NOT DO THIS
try:
 x = int(input("Enter First Number: "))
 y = int(input("Enter Second Number: "))
 print(x / y)
except ArithmeticError:
 print("ArithmeticError") # matches ZeroDivisionError too
except ZeroDivisionError: # unreachable
 print("ZeroDivisionError")
```

```
Enter First Number: 10
Enter Second Number: 0
ArithmeticError
```

### **Example 2 — Order matters: child before parent (works as expected)**

```python
try:
 x = int(input("Enter First Number: "))
 y = int(input("Enter Second Number: "))
 print(x / y)
except ZeroDivisionError:
 print("ZeroDivisionError: handled specifically")
except ArithmeticError:
 print("ArithmeticError: other arithmetic problems only")
```

```
Enter First Number: 10
Enter Second Number: 0
ZeroDivisionError: handled specifically
```

### **Example 3 — Bare `except` must be last**

```python
try:
 print(10 / 0)
except:
 print("default")
except ZeroDivisionError: # SyntaxError when you try to run this
 print("specific")
```

```
SyntaxError: default 'except:' must be last
```

### **Example 4 — `finally` runs even when the program dies**

```python
def open_door():
 print("Door opening...")
 try:
 print("Inside try — about to crash")
 raise ValueError("oops")
 finally:
 print("Closing door in finally") # runs BEFORE the unhandled exception propagates

try:
 open_door()
except ValueError as e:
 print("Caught at top level:", e)
```

```
Door opening...
Inside try — about to crash
Closing door in finally
Caught at top level: oops
```

`finally` ran even though the exception was not caught inside `open_door`.

### **Example 5 — `else` only runs on success**

```python
def read_int():
 try:
 return int(input("Enter an integer: "))
 except ValueError:
 print("That was not an integer")
 return None
 else:
 print("Conversion succeeded")
 finally:
 print("(this is the cleanup message)")

v = read_int()
print("Got value:", v)
```

If the user types `42`:

```
Enter an integer: 42
Conversion succeeded
(this is the cleanup message)
Got value: 42
```

If the user types `forty-two`:

```
Enter an integer: forty-two
That was not an integer
(this is the cleanup message)
Got value: None
```

`else` ran only on success. `finally` ran in both cases.

### **Example 6 — `return` in `finally` swallows earlier returns**

```python
def f():
 try:
 return "from try"
 finally:
 return "from finally"

print(f())
```

```
from finally
```

### **Example 7 — Catching a broad parent and recovering the actual class**

```python
try:
 numbers = [1, 2, 3]
 index = int(input("Enter an index (0-2): "))
 print("Value:", numbers[index])
except (ValueError, IndexError) as e:
 # We don't know which one fired without asking
 print("Problem type:", e.__class__.__name__)
 print("Message: ", e)
```

Input: `9` → `Problem type: IndexError`
Input: `ten` → `Problem type: ValueError`

### **Example 8 — Iterating with a single global handler vs. per-iteration handler**

```python
def send_sms(phone_num):
 if phone_num % 10 == 4:
 raise Exception("This is a bug")
 print(f"Message is successfully sent to {phone_num}")

contact_nums = [9102341411, 9102341412, 9102341413, 9102341414]

# Version 1: per-iteration try
for i in contact_nums:
 try:
 send_sms(i)
 except Exception as e:
 print(f" Skipped {i}: {e}")
```

```
Message is successfully sent to 9102341411
Message is successfully sent to 9102341412
Message is successfully sent to 9102341413
 Skipped 9102341414: This is a bug
```

Compare with the wrong version (no inner try):

```python
for i in contact_nums:
 send_sms(i)
```

```
Message is successfully sent to 9102341411
Message is successfully sent to 9102341412
Message is successfully sent to 9102341413
---------------------------------------------------------------------------
Exception: This is a bug
```

The exception kills the entire loop. Putting the `try` *inside* the loop means a single bad number does not abort the whole batch.

### **Example 9 — Tuple `except` with formatting**

```python
try:
 x = int(input("Enter first number: "))
 y = int(input("Enter second number: "))
 print(x / y)
except (ZeroDivisionError, ValueError) as e:
 print(f"Exception Raised: {e.__class__.__name__}, Description: {e}")
```

```
Exception Raised: ValueError, Description: invalid literal for int() with base 10: 'fr'
```

### **Example 10 — Nested try for staged cleanup**

```python
def process_file(path):
 f = None
 try:
 f = open(path, 'r')
 try:
 data = f.read()
 return data.upper()
 finally:
 print("Inner finally: read complete, file will close next")
 except FileNotFoundError:
 print("Outer except: file missing — returning empty string")
 return ""
 finally:
 if f is not None:
 f.close()
 print("Outer finally: file closed. Closed?", f.closed)

print("Result:", process_file('abc.txt'))
```

```
Inner finally: read complete, file will close next
Outer finally: file closed. Closed? True
Result: HEY BORTHER STAY UPDATED!!
```

Both `finally` blocks run in order (inner first, then outer), regardless of what happened above.

---

## **Quick Reference Summary**

### **The Four Blocks at a Glance**

| Block | Runs when | Purpose |
|---|---|---|
| `try` | Always (must be entered) | The risky code |
| `except` | An exception was raised *and* matched | Alternative / handling code |
| `else` | The `try` block did *not* raise an exception | Success-path code |
| `finally` | The `try` block was entered (always, except `os._exit`) | Cleanup code |

### **Order of `except` Blocks**

| Order | Result |
|---|---|
| Specific → General | Correct — narrow handlers run first |
| General → Specific | Wrong — narrow handlers are dead code |

### **Catch Scope Cheat Sheet**

| Form | What it catches |
|---|---|
| `except ValueError:` | Only `ValueError` and its subclasses |
| `except (ValueError, TypeError):` | Either of those two |
| `except Exception:` | All "regular" runtime errors (recommended broad catch) |
| `except BaseException:` | Almost everything, **including `Ctrl+C` — avoid** |
| `except:` | Same as `except BaseException:`, must be last |

### **`finally` and `return`**

| Where `return` is | `finally` has no `return` | `finally` has `return X` |
|---|---|---|
| `try: return A` | Returns `A` (finally runs first, then `A` is delivered) | Returns `X` (finally's value wins) |
| `except: return B` | Returns `B` (finally runs first) | Returns `X` (finally's value wins) |
| No `return` in try/except | Function returns `None` | Returns `X` |

### **Legal Combinations**

| Combination | Legal? |
|---|---|
| `try / except` | |
| `try / finally` | |
| `try / except / else` | |
| `try / except / else / finally` | |
| `try / except / except` (multiple) | |
| `try / else` | |
| `try` alone | |
| `except` alone | |
| `else` alone | |
| `finally` alone | |
| `try / except / finally / finally` | (only one `finally`) |
| `try / except / else / else` | (only one `else`) |
| `try / except ...` followed by `except ZeroDivisionError: ...` (where bare `except` is not last) | |

---

## **Practice and Next Steps**

1. **Predict the order.** Given this code, write down which lines print and in what order, then run it to verify:
 ```python
 try:
 print("A")
 raise ValueError("boom")
 print("B")
 except ValueError:
 print("C")
 else:
 print("D")
 finally:
 print("E")
 print("F")
 ```
2. **Catch and inspect.** Wrap a `1 / 0` in `try/except` and use `as msg` to print *both* `str(msg)` and `msg.__class__.__name__`. Then do the same with `int("ten")` and compare.
3. **Order matters.** Write one `try` block with three `except` clauses: `ArithmeticError`, `ZeroDivisionError`, and a bare `except`. Run `10 / 0` and observe which one fires. Then reorder them and run again.
4. **`else` vs success.** Refactor a small program (e.g. file read) so that the success path lives in the `else` block instead of the `try` block. Verify that errors are still caught.
5. **Return + finally trick.** Write a function that returns `"from try"` from the `try` block, has a `finally` that prints something but does *not* have a `return`. Then add a `return "from finally"` to the `finally` and observe the change.
6. **Nesting drill.** Write a function with a nested `try/except/finally` inside the `finally` of the outer one. Run with a value that triggers the inner `except`, then with a value that does not, and trace the output by hand before running.
7. **Valid combinations quiz.** Without running the code, decide whether each of the 16 patterns in the cheat-sheet table is valid Python. Then verify with the interpreter.
8. **Refactor a real script.** Take any small script you have (e.g. a CSV reader) and add `try/except/else/finally` to handle the file-not-found case, print a useful error, and guarantee the file gets closed.
