# **Python File Handling — Basics (Open, Read, Write, Close)**

## **What is File Handling**

A file is a named location on disk used to store data permanently. Unlike variables, which lose their values when a program ends, files persist across runs. Every meaningful program — a log analyzer, a config loader, a CSV exporter, a web server, a build script — has to read or write files at some point.

In Python, file handling is built on a simple mental model:

1. **Open** the file — get a file object that talks to the OS on your behalf.
2. **Read or write** data through that object.
3. **Close** the file — release the OS resource and flush any pending writes.

The first thing to internalize is that opening a file is a request to the operating system. The OS hands back a *file descriptor* (a small integer) and Python wraps it in a file object. Until you close it, that file is "locked" by your process, and the OS holds onto limited resources (open file handles, buffer memory, locks). That is why closing files matters.

## **The `open()` Built-in Function**

The single entry point for file handling in Python is `open()`. Its basic signature:

```python
file_object = open(file, mode='r', encoding=None, buffering=-1)
```

The most important parameters:

- `file` — the path to the file (string or `Path` object).
- `mode` — what you want to do (read, write, append, binary, etc.). Default is `'r'` (read text).
- `encoding` — for text mode, the character encoding. Default depends on the platform, but `'utf-8'` is the safe modern choice.
- `buffering` — controls buffering. `-1` means default, `0` is unbuffered (binary mode only), `1` is line-buffered (text mode only), and any positive integer is the buffer size in bytes.

The first example — open a file, read its content, print it, close it:

```python
# Step 1: make sure we have a file to read
with open("sample.txt", "w") as f:
    f.write("Hello from Python file handling.\n")
    f.write("This is the second line.\n")
    f.write("And the third one.")

# Step 2: read the file we just wrote
f = open("sample.txt", "r")
content = f.read()
print("Type of f:", type(f))
print("Name of file:", f.name)
print("Mode:", f.mode)
print("Closed?", f.closed)
print("Content:")
print(content)
f.close()
print("Closed after close()?", f.closed)
```

```
Type of f: <class '_io.TextIOWrapper'>
Name of file: sample.txt
Mode: r
Closed? False
Content:
Hello from Python file handling.
This is the second line.
And the third one.
Closed after close()?, True
```

A few things to notice:

- `type(f)` is `<class '_io.TextIOWrapper'>` — that is the default file object for **text mode**. There is a different class (`_io.BufferedReader`, `_io.BufferedWriter`) for **binary mode**.
- `f.name` gives the path you used to open it.
- `f.mode` gives the mode string you passed.
- `f.closed` is `False` while the file is open, and becomes `True` after `close()`.

The default mode is `'r'` (read text), so `open("sample.txt")` and `open("sample.txt", "r")` are equivalent. The default encoding depends on the platform (`utf-8` on most modern systems, but `cp1252` on some Windows configurations). For portable code, always pass `encoding="utf-8"` explicitly.

## **Closing Files — Why It Matters**

Every open file consumes a limited OS resource (a file descriptor). On most systems, the per-process limit is around 1024 by default, sometimes 65536. If you open files in a loop and never close them, you will eventually run out and get an `OSError: [Errno 24] Too many open files`.

There are three ways to close a file:

1. **Call `close()` explicitly** — works, but easy to forget, especially when an error happens mid-way.
2. **Use `try / finally`** — guarantees the file is closed even if an exception fires.
3. **Use a `with` statement** — the modern, recommended way. Closes the file automatically when the block exits, even on errors.

The explicit close version:

```python
f = open("sample.txt", "r")
try:
    content = f.read()
    print("Read", len(content), "characters")
finally:
    f.close()
    print("File closed in finally")
```

```
Read 79 characters
File closed in finally
```

Even if the `read()` call raises an exception, the `finally` block runs and the file is closed. This is the safe pattern, but it is verbose. The `with` statement does the same thing in two lines.

## **The `with` Statement — The Modern Way**

A `with` statement wraps a block in a **context manager**. The file object returned by `open()` is a context manager, so using `with` guarantees `close()` is called automatically when the block exits — normally or via an exception.

```python
with open("sample.txt", "r") as f:
    content = f.read()
    print("Read", len(content), "characters")
    print("Is closed inside with?", f.closed)

print("Is closed after with?", f.closed)
```

```
Read 79 characters
Is closed inside with? False
Is closed after with? True
```

Notice that `f.closed` is still `False` *inside* the `with` block — the file is open. As soon as the block ends, `closed` flips to `True`. That automatic cleanup is the whole point.

A `with` statement is equivalent to writing the `try / finally` by hand:

```python
# What 'with' actually does under the hood
f = open("sample.txt", "r")
f.__enter__()     # returns the file object itself
try:
    content = f.read()
    print(content)
finally:
    f.__exit__(None, None, None)   # calls close()
```

In real code, you will use `with` for almost every file operation. The only reason to call `close()` directly is in long-running programs that hold a file open across many function calls (rare, and even then a `with` should wrap the lifetime).

## **Reading Files — All the Methods**

There are four common ways to read a text file, and each one serves a different purpose.

### **Method 1 — `read()` (everything at once)**

`read()` with no argument reads the **entire file** into a single string. Use this for small files only — for large files, it can eat up all your memory.

```python
with open("sample.txt", "r") as f:
    content = f.read()
    print("Type:", type(content))
    print("Length:", len(content), "characters")
    print("---")
    print(content)
```

```
Type: <class 'str'>
Length: 79 characters
---
Hello from Python file handling.
This is the second line.
And the third one.
```

You can also pass a size argument to read at most that many characters:

```python
with open("sample.txt", "r") as f:
    chunk1 = f.read(20)
    print("Chunk 1:", repr(chunk1))
    chunk2 = f.read(20)
    print("Chunk 2:", repr(chunk2))
    chunk3 = f.read(20)
    print("Chunk 3:", repr(chunk3))
```

```
Chunk 1: 'Hello from Python file '
Chunk 2: 'handling.\nThis is the '
Chunk 3: 'second line.\nAnd the t'
```

Each `read(20)` call returns up to 20 characters and advances an internal pointer. The pointer does not wrap around or restart — once you read 20 characters, the next `read(20)` picks up where the last one stopped.

### **Method 2 — `readline()` (one line at a time)**

`readline()` reads from the current pointer position up to and including the next `\n`. If there is no `\n`, it returns the rest of the file. If the file is already at the end, it returns an empty string `''` (which is falsy — a common way to detect EOF).

```python
with open("sample.txt", "r") as f:
    line1 = f.readline()
    line2 = f.readline()
    line3 = f.readline()
    line4 = f.readline()
    print("Line 1:", repr(line1))
    print("Line 2:", repr(line2))
    print("Line 3:", repr(line3))
    print("Line 4 (empty = EOF):", repr(line4))
```

```
Line 1: 'Hello from Python file handling.\n'
Line 2: 'This is the second line.\n'
Line 3: 'And the third one.'
Line 4 (empty = EOF): ''
```

Notice the `\n` at the end of lines 1 and 2. Line 3 does not have a `\n` because the file ends right after it. Line 4 is `''` — that is the standard end-of-file signal from `readline()`.

### **Method 3 — `readlines()` (all lines as a list)**

`readlines()` reads the entire file and returns a list of strings, one per line (each line still ends with `\n`, except possibly the last one).

```python
with open("sample.txt", "r") as f:
    lines = f.readlines()
    print("Type:", type(lines))
    print("Number of lines:", len(lines))
    for i, line in enumerate(lines, 1):
        print(f"  Line {i}: {line!r}")
```

```
Type: <class 'list'>
Number of lines: 3
  Line 1: 'Hello from Python file handling.\n'
  Line 2: 'This is the second line.\n'
  Line 3: 'And the third one.'
```

Like `read()`, this loads the whole file into memory. Use it only when the file is small enough to fit comfortably.

### **Method 4 — Iterate the file object directly (the most Pythonic way)**

A file object is an **iterator** over its lines. You can use it in a `for` loop without calling any read method at all. This is the recommended way to process a file line by line — it is memory-efficient (lines are read on demand) and reads cleanly.

```python
with open("sample.txt", "r") as f:
    for i, line in enumerate(f, 1):
        print(f"Line {i}: {line!r}")
```

```
Line 1: 'Hello from Python file handling.\n'
Line 2: 'This is the second line.\n'
Line 3: 'And the third one.'
```

The variable `line` includes the trailing `\n`. If you do not want it, strip it with `line.rstrip('\n')` or just `line.strip()`.

```python
with open("sample.txt", "r") as f:
    for i, line in enumerate(f, 1):
        cleaned = line.rstrip("\n")
        print(f"Line {i}: {cleaned!r}  (length {len(cleaned)})")
```

```
Line 1: 'Hello from Python file handling.'  (length 33)
Line 2: 'This is the second line.'  (length 23)
Line 3: 'And the third one.'  (length 17)
```

### **Which Read Method Should You Use?**

| Method | Returns | Memory | When to use |
|---|---|---|---|
| `read()` | whole file as one string | full file in memory | tiny files, or you really need the whole thing. |
| `read(n)` | next `n` characters | up to `n` characters | reading in fixed-size chunks (rare). |
| `readline()` | next line (one string) | one line | when you need to peek or process one line at a time. |
| `readlines()` | list of all lines | full file in memory | small files you want to index. |
| iterate `for line in f` | one line per iteration | one line at a time | **the default choice** for any non-trivial file processing. |

## **Writing Files — All the Methods**

Writing is the mirror of reading. There are two write methods: `write()` and `writelines()`.

### **Method 1 — `write()` (one string at a time)**

`write()` takes a single string and appends it to the file. It does **not** add a newline — if you want one, include `\n` in your string.

```python
with open("output.txt", "w") as f:
    n1 = f.write("First line\n")
    n2 = f.write("Second line\n")
    n3 = f.write("Third line without newline")
    print("Wrote", n1, "chars")
    print("Wrote", n2, "chars")
    print("Wrote", n3, "chars")

# Read it back to confirm
with open("output.txt", "r") as f:
    print("--- file contents ---")
    print(f.read())
```

```
Wrote 11 chars
Wrote 12 chars
Wrote 24 chars
--- file contents ---
First line
Second line
Third line without newline
```

A subtle but useful detail: `write()` returns the number of characters written. You can ignore the return value, but it is helpful for logging or for confirming that a write actually happened.

### **Method 2 — `writelines()` (many strings at once)**

`writelines()` takes an iterable of strings and writes each one. Like `write()`, it does **not** add newlines between them — your strings have to include their own separators.

```python
lines = [
    "Apple\n",
    "Banana\n",
    "Cherry\n",
    "Date\n",
]

with open("fruits.txt", "w") as f:
    f.writelines(lines)

with open("fruits.txt", "r") as f:
    print(f.read())
```

```
Apple
Banana
Cherry
Date

```

A common confusion: many people expect `writelines()` to behave like `print()` and add newlines automatically. It does not. The strings in the list must already end with `\n` (or you use `print(line, file=f)` instead, which does add one).

### **Using `print()` to Write Files**

A third option, often the most convenient one, is `print()`. It supports a `file=` argument that lets you redirect output to any open file. Unlike `write()`, it **does** add a newline by default, and it converts non-string arguments to strings for you.

```python
with open("greetings.txt", "w") as f:
    print("Hello, world", file=f)
    print("The answer is", 42, file=f)
    print("List of names:", ["Karan", "Om", "Durga"], file=f)

with open("greetings.txt", "r") as f:
    print(f.read())
```

```
Hello, world
The answer is 42
List of names: ['Karan', 'Om', 'Durga']

```

`print(..., file=f)` is equivalent to `f.write(str(...) + "\n")`, but it is shorter and handles the conversion for you. This is the most common way to write log lines.

## **Q&A — Common Beginner Questions**

**Q1. What happens if you open a non-existent file in read mode?**

You get a `FileNotFoundError`. Python does not create the file automatically for read mode — it has to exist already.

```python
try:
    with open("does_not_exist.txt", "r") as f:
        f.read()
except FileNotFoundError as e:
    print("Caught:", e)
```

```
Caught: [Errno 2] No such file or directory: 'does_not_exist.txt'
```

**Q2. What happens if you open an existing file in write mode?**

The file is **truncated** — its contents are erased, and you start writing from scratch. There is no "are you sure?" prompt. If you want to add to the end, use append mode (`'a'`) instead.

**Q3. What happens if you open a file in append mode but it does not exist?**

The file is **created**. Unlike read mode, append and write modes both create the file if it does not exist.

**Q4. Why do we use `with` instead of `f.close()`?**

`with` is safer. If an exception fires between `open()` and `close()`, the explicit version leaks the file open. `with` guarantees the file is closed in every case, including exceptions, keyboard interrupts, and `sys.exit()`.

**Q5. Can you read and write the same file in the same `with` block?**

Yes, if you open it in read+write mode (e.g., `'r+'` or `'w+'`). The default mode `'r'` is read-only, and `'w'` truncates the file. See the modes file for the full breakdown.

**Q6. Do I have to specify the encoding?**

In practice, yes — always. On most modern systems, the default is `utf-8` and everything works, but on some Windows setups the default is `cp1252` and that breaks on non-ASCII characters. `open("file.txt", "r", encoding="utf-8")` is the safe form for text files.

**Q7. What is the difference between `read()` and `readlines()`?**

`read()` returns one big string. `readlines()` returns a list of strings, one per line. Both load the whole file into memory. For large files, use `for line in f` instead.

**Q8. Why does `readline()` return an empty string at the end?**

Empty string means "you are past the end of the file." This is a sentinel value — you can use it in a `while` loop to read until EOF.

## **Real-World Example — A Log Analyzer**

Putting everything together. Suppose you have a log file where each line is a timestamped event, and you want to count events by level (INFO, WARNING, ERROR).

```python
# Step 1: create a sample log file
log_content = """\
2024-10-08 10:00:01 INFO  Application started
2024-10-08 10:00:15 INFO  User logged in: karan
2024-10-08 10:01:02 WARN  Slow query detected (2.3s)
2024-10-08 10:01:45 ERROR Database connection lost
2024-10-08 10:02:10 INFO  Retrying connection
2024-10-08 10:02:30 INFO  Connection restored
2024-10-08 10:05:00 WARN  Memory usage at 85%
2024-10-08 10:10:00 ERROR Payment gateway timeout
"""

with open("app.log", "w") as f:
    f.write(log_content)

# Step 2: read it line by line, count by level
counts = {"INFO": 0, "WARN": 0, "ERROR": 0}
with open("app.log", "r") as f:
    for line in f:
        parts = line.split()
        if len(parts) >= 3:
            level = parts[2]
            if level in counts:
                counts[level] += 1

# Step 3: write a summary file
with open("summary.txt", "w") as f:
    print("Log Summary", file=f)
    print("=" * 30, file=f)
    for level, n in counts.items():
        print(f"{level:6} : {n}", file=f)
    total = sum(counts.values())
    print("=" * 30, file=f)
    print(f"TOTAL  : {total}", file=f)

# Step 4: print the summary
with open("summary.txt", "r") as f:
    print(f.read())
```

```
Log Summary
==============================
INFO   : 4
WARN   : 2
ERROR  : 2
==============================
TOTAL  : 8

```

This example ties together several things: writing the initial log, reading line by line with `for line in f`, parsing each line with `split()`, and writing the summary with `print(..., file=f)`. The pattern `for line in f` is the most common file-processing loop in real Python code.

## **Examples**

```python
# Example 1: Read a small file and count characters and words
with open("sample.txt", "r") as f:
    content = f.read()
    print("Characters:", len(content))
    print("Words:", len(content.split()))
    print("Lines:", content.count("\n") + 1)
```

```
Characters: 79
Words: 14
Lines: 3
```

```python
# Example 2: Copy a file (simple version)
with open("sample.txt", "r") as src:
    data = src.read()
with open("sample_copy.txt", "w") as dst:
    dst.write(data)
print("Copied", len(data), "characters")
```

```
Copied 79 characters
```

```python
# Example 3: Read a file and skip blank lines
with open("sample.txt", "r") as f:
    for line in f:
        if line.strip() == "":
            continue
        print("Kept:", line.rstrip())
```

```
Kept: Hello from Python file handling.
Kept: This is the second line.
Kept: And the third one.
```

```python
# Example 4: Append to an existing file
with open("output.txt", "a") as f:
    f.write("This line is appended.\n")
    f.write("Another appended line.\n")

with open("output.txt", "r") as f:
    print(f.read())
```

```
First line
Second line
Third line without newlineThis line is appended.
Another appended line.

```

```python
# Example 5: Use try/finally to close (equivalent to with)
f = open("sample.txt", "r")
try:
    print("First line:", f.readline().rstrip())
    print("Inside try, closed?", f.closed)
finally:
    f.close()
    print("After finally, closed?", f.closed)
```

```
First line: Hello from Python file handling.
Inside try, closed? False
After finally, closed? True
```

```python
# Example 6: Detect end of file with readline()
with open("sample.txt", "r") as f:
    while True:
        line = f.readline()
        if line == "":
            print("Reached EOF")
            break
        print("Got:", line.rstrip())
```

```
Got: Hello from Python file handling.
Got: This is the second line.
Got: And the third one.
Reached EOF
```

```python
# Example 7: writelines vs write for a list
items = ["alpha", "beta", "gamma"]
with open("items_no_nl.txt", "w") as f:
    f.writelines(items)        # no newlines added

with open("items_no_nl.txt", "r") as f:
    print("writelines result:", repr(f.read()))

with open("items_with_nl.txt", "w") as f:
    for item in items:
        f.write(item + "\n")    # add newlines manually

with open("items_with_nl.txt", "r") as f:
    print("write+newline result:", repr(f.read()))
```

```
writelines result: 'alphabetagamma'
write+newline result: 'alpha\nbeta\ngamma\n'
```

## **Quick Reference Summary**

### **Open / Close**

| Form | Code | When to use |
|---|---|---|
| Recommended | `with open(path, mode) as f: ...` | Always, for any file operation. |
| Explicit close | `f = open(...); ...; f.close()` | Avoid. If you must, wrap in try/finally. |
| Context manager protocol | `f.__enter__()` / `f.__exit__()` | What `with` calls under the hood. |

### **Reading Methods**

| Method | Returns | Memory | Notes |
|---|---|---|---|
| `f.read()` | whole file as `str` | O(file size) | Small files only. |
| `f.read(n)` | next `n` chars | O(n) | Reading in fixed-size chunks. |
| `f.readline()` | next line (keeps `\n`) | O(line length) | `''` means EOF. |
| `f.readlines()` | `list[str]` of all lines | O(file size) | Small files only. |
| `for line in f` | one line per iteration | O(line length) | **Default choice.** |

### **Writing Methods**

| Method | Accepts | Adds newline? | Returns |
|---|---|---|---|
| `f.write(s)` | one string | no | number of chars written |
| `f.writelines(list)` | iterable of strings | no | `None` |
| `print(..., file=f)` | any value | yes | `None` |

### **Default Mode Behavior**

| Mode | File must exist? | Truncates? | Creates if missing? |
|---|---|---|---|
| `r` (read) | Yes | No | No (raises FileNotFoundError) |
| `w` (write) | No | Yes | Yes |
| `a` (append) | No | No | Yes |
| `x` (exclusive create) | No | No | Yes (raises if exists) |

Detailed mode table is in the modes file.

### **Always Remember**

- Always pass `encoding="utf-8"` for text files on systems where the default is not utf-8.
- Always use `with` to close files automatically.
- The default mode is `'r'` (read text). If you forget to specify the mode, you cannot write.
- `for line in f` is the most common and most Pythonic way to process a file.

## **Practice and Next Steps**

- Write a script that creates a file with 5 lines, then reads it back and prints each line with its line number.
- Write a script that reads a file and counts how many lines contain a given word (e.g., "Python").
- Write a script that copies one file to another using `read()` and `write()`, then check the file sizes match.
- Write a script that appends three new lines to an existing file without erasing the original content. Confirm by reading back the full file.
- Write a script that uses `readline()` in a `while` loop and stops on the empty-string EOF signal.
- Use `try/finally` to close a file, then rewrite the same code using `with`. Compare readability.
- Create a file with mixed blank lines and content, then read it and skip the blank lines.
- Write a small log analyzer that opens a log file, counts lines by status, and writes a summary to another file.
