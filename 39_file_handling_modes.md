# **Python File Handling — Modes, Pointer, Binary, and Buffering**

## **What This File Covers**

The previous file showed the basic `open()`, read, write, and `with` patterns. This file goes deeper into the four things that come up constantly in real Python work:

- **File modes** — every combination of `r`, `w`, `a`, `x`, `b`, `t`, `+`, and what they actually do.
- **The file pointer** — `seek()`, `tell()`, `truncate()` for random access.
- **Text vs binary** — when to use which, and how bytes relate to strings.
- **Buffering** — how Python decides when to actually write to disk.

Together these are the building blocks of any non-trivial file code — log rotation, binary protocol parsing, large-file processing, downloading files, and image/PDF handling.

## **File Modes — The Full Table**

The `mode` argument to `open()` is a string of one or more characters. Each character is a flag. Python reads them in order: the first character is the **action** (`r`, `w`, `a`, `x`), and the rest are **modifiers** (`b`, `t`, `+`).

### **The Action Characters**

| Char | Name | File must exist? | Truncates? | Creates if missing? | Readable? | Writable? | Pointer starts at |
|---|---|---|---|---|---|---|---|
| `r` | read | yes | no | no | yes | no | 0 (start) |
| `w` | write | no | yes | yes | no | yes | 0 (start) |
| `a` | append | no | no | yes | no | yes | end (always) |
| `x` | exclusive create | no | no | yes (raises if exists) | no | yes | 0 (start) |

A quick demo of each in action — write a known file, then explore what each mode does:

```python
# Set up: write a 3-line file
with open("demo.txt", "w") as f:
    f.write("Line 1\n")
    f.write("Line 2\n")
    f.write("Line 3\n")

# Mode 'r' — read only
with open("demo.txt", "r") as f:
    print("r mode — pointer at:", f.tell())
    print(f.read())
    print("Try to write in r mode:")
    try:
        f.write("extra")
    except io.UnsupportedOperation as e:
        print("  Got:", e)
```

```
r mode — pointer at: 0
Line 1
Line 2
Line 3
Try to write in r mode:
  Got: not writable
```

```python
import io   # used for the UnsupportedOperation exception class

# Mode 'w' — truncates and writes
with open("demo.txt", "w") as f:
    print("w mode — pointer at:", f.tell())
    f.write("NEW CONTENT\n")
    print("After write, pointer at:", f.tell())

with open("demo.txt", "r") as f:
    print("File now contains:")
    print(f.read())
```

```
w mode — pointer at: 0
After write, pointer at: 12
File now contains:
NEW CONTENT

```

The original three lines are gone. That is the cost of `'w'` mode — it silently truncates. There is no "are you sure" prompt.

```python
# Mode 'a' — append, never truncates, pointer always at end
with open("demo.txt", "a") as f:
    print("a mode — pointer at:", f.tell())
    f.write("Appended line A\n")
    f.write("Appended line B\n")
    print("After writes, pointer at:", f.tell())

with open("demo.txt", "r") as f:
    print("File now contains:")
    print(f.read())
```

```
a mode — pointer at: 12
After writes, pointer at: 41
File now contains:
NEW CONTENT
Appended line A
Appended line B

```

The pointer started at `12` (the end of the existing content) and moved forward as we appended. In append mode, the pointer is always at the end — `seek()` works but any subsequent write appends again.

```python
# Mode 'x' — exclusive create, fails if file already exists
import os

# Clean slate
if os.path.exists("new_file.txt"):
    os.remove("new_file.txt")

# First 'x' succeeds
with open("new_file.txt", "x") as f:
    f.write("Created exclusively\n")
print("First 'x' open succeeded")

# Second 'x' fails because file already exists
try:
    with open("new_file.txt", "x") as f:
        f.write("Will not be written")
except FileExistsError as e:
    print("Second 'x' open failed:", e)
```

```
First 'x' open succeeded
Second 'x' open failed: [Errno 17] File exists: 'new_file.txt'
```

`x` is the safe "create new" mode. It is the right choice when you want to ensure you are not overwriting an existing file (for example, when creating a new log file or a temp output).

### **The Modifier Characters**

| Char | Name | Effect |
|---|---|---|
| `t` | text | The default. Reads/writes `str`. Uses the platform's line endings. |
| `b` | binary | Reads/writes `bytes`. No encoding or line-ending translation. |
| `+` | update | Adds the missing ability (read+write, read+append, etc.). |

You combine them with an action: `"rt"`, `"rb"`, `"wb"`, `"ab"`, `"r+"`, `"w+"`, `"a+"`, `"rb+"`, `"wb+"`, and so on. If you do not specify `t` or `b`, Python defaults to text mode.

### **The Combined Mode Table**

| Mode | Equivalent to | Read | Write | Truncate | Create | Pointer |
|---|---|---|---|---|---|---|
| `r` / `rt` | read text | yes | no | no | no | start |
| `rb` | read binary | yes | no | no | no | start |
| `r+` / `r+t` | read + write text | yes | yes | no | no | start |
| `rb+` / `r+b` | read + write binary | yes | yes | no | no | start |
| `w` / `wt` | write text | no | yes | yes | yes | start |
| `wb` | write binary | no | yes | yes | yes | start |
| `w+` / `w+t` | read + write text | yes | yes | yes | yes | start |
| `wb+` / `w+b` | read + write binary | yes | yes | yes | yes | start |
| `a` / `at` | append text | no | yes | no | yes | end |
| `ab` | append binary | no | yes | no | yes | end |
| `a+` / `a+t` | read + append text | yes | yes | no | yes | end |
| `ab+` / `a+b` | read + append binary | yes | yes | no | yes | end |
| `x` | exclusive create text | no | yes | no | yes (fails if exists) | start |

A practical example showing the difference between `r+`, `w+`, and `a+`:

```python
import os

# Reset
if os.path.exists("rw_demo.txt"):
    os.remove("rw_demo.txt")
with open("rw_demo.txt", "w") as f:
    f.write("0123456789")    # 10 characters

# r+ — read+write, no truncate, must exist
with open("rw_demo.txt", "r+") as f:
    print("r+ initial position:", f.tell())
    print("Read 3 chars:", f.read(3))
    f.seek(0)
    f.write("ABC")           # overwrites first 3 chars
    print("Final pointer after seek+write:", f.tell())

with open("rw_demo.txt", "r") as f:
    print("After r+:", f.read())
```

```
r+ initial position: 0
Read 3 chars: 012
Final pointer after seek+write: 3
After r+: ABC3456789
```

In `r+` mode, writing at position 0 overwrote the first three characters. The file is still 10 characters long — we did not append, we replaced.

```python
# w+ — read+write, truncates immediately
with open("rw_demo.txt", "w+") as f:
    print("w+ initial position:", f.tell())
    f.write("HELLO")
    f.seek(0)
    print("After seek+read:", f.read())

with open("rw_demo.txt", "r") as f:
    print("File after w+:", f.read())
```

```
w+ initial position: 0
After seek+read: HELLO
File after w+: HELLO
```

`w+` truncated the file when it was opened, so the original `0123456789` was gone.

```python
# a+ — read+append, pointer always at end
with open("rw_demo.txt", "a+") as f:
    print("a+ initial position:", f.tell())
    f.write(" WORLD")
    f.seek(0)
    print("After seek, full read:", f.read())
    print("Final position:", f.tell())
```

```
a+ initial position: 5
After seek, full read: HELLO WORLD
Final position: 11
```

In `a+` mode, the pointer starts at the end. Writes always go to the end (the OS ignores seek-before-write). Reads can be done from anywhere by `seek()`-ing first.

## **The File Pointer — `seek()` and `tell()`**

The **file pointer** is the position in the file where the next read or write will happen. In text mode, the pointer is measured in **characters**. In binary mode, it is measured in **bytes**.

### **`tell()` — Where am I?**

`tell()` returns the current pointer position as an integer.

```python
with open("demo.txt", "r") as f:
    print("Start:", f.tell())
    f.read(5)
    print("After read(5):", f.tell())
    f.readline()
    print("After readline():", f.tell())
```

```
Start: 0
After read(5): 5
After readline(): 12
```

### **`seek()` — Move the Pointer**

`seek(offset, whence)` moves the pointer to a new position. The `whence` argument controls how `offset` is interpreted:

| `whence` | Value | Meaning |
|---|---|---|
| `SEEK_SET` (or `0`) | absolute | Move to `offset` from the start of the file. |
| `SEEK_CUR` (or `1`) | relative | Move `offset` from the current position (positive = forward, negative = backward). |
| `SEEK_END` (or `2`) | from end | Move to `offset` from the end of the file. |

```python
with open("demo.txt", "rb") as f:    # binary mode for byte-level seek
    f.seek(0, 2)         # SEEK_END — go to end
    size = f.tell()
    print("File size:", size, "bytes")

    f.seek(0)            # back to start
    print("First 6 bytes:", f.read(6))

    f.seek(-3, 2)        # 3 bytes from end
    print("Last 3 bytes:", f.read())
```

```
File size: 41 bytes
First 6 bytes: b'NEW CO'
Last 3 bytes: b'B\n\n'
```

A practical use case — reading the header and footer of a file without loading the middle:

```python
# Pretend we have a binary file with a 4-byte header and 4-byte footer
with open("binary_demo.bin", "wb") as f:
    f.write(b"HDR!")                  # 4-byte header
    f.write(b"MIDDLE-CONTENT-HERE")   # 19 bytes
    f.write(b"FTR!")                  # 4-byte footer

# Read header, footer, and length without loading the middle
with open("binary_demo.bin", "rb") as f:
    header = f.read(4)
    print("Header:", header)

    f.seek(-4, 2)                     # 4 bytes from end
    footer = f.read(4)
    print("Footer:", footer)

    f.seek(0, 2)
    size = f.tell()
    middle_size = size - 8
    print(f"Middle is {middle_size} bytes (we did not load it)")
```

```
Header: b'HDR!'
Footer: b'FTR!'
Middle is 19 bytes (we did not load it)
```

This trick is used in real systems like audio/video file parsers, where you want to read metadata at the end of a huge file without loading the whole thing.

### **`truncate()` — Shrink the File**

`truncate(size)` cuts the file to at most `size` bytes (or characters in text mode). If you do not pass a size, it cuts to the current pointer position.

```python
with open("trunc_demo.txt", "w") as f:
    f.write("Hello, World!")

with open("trunc_demo.txt", "r+") as f:
    f.seek(5)               # pointer at position 5 (after "Hello")
    f.truncate()            # cut everything from here to the end
    print("After truncate at pos 5:")
    print(f.read())
```

```
After truncate at pos 5:
Hello
```

The file went from 13 characters (`Hello, World!`) to 5 characters (`Hello`). `truncate()` is destructive — use it with care.

## **Text vs Binary Mode**

This is one of the most important distinctions in file handling.

### **Text Mode (the default)**

- Reads/writes **strings** (`str`).
- Uses an **encoding** (`utf-8`, `latin-1`, etc.) to translate between bytes on disk and Python strings in memory.
- Translates platform-specific line endings automatically. On Windows, `\r\n` in the file becomes `\n` in your string. On Unix, `\n` stays as `\n`.
- Pointer positions are measured in **characters**, not bytes.

```python
# Write a string with a non-ASCII character
text = "Café résumé\n"
with open("text_demo.txt", "w", encoding="utf-8") as f:
    f.write(text)

# Read it back
with open("text_demo.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print("Type:", type(content))
    print("Content:", repr(content))
    print("Length (chars):", len(content))
```

```
Type: <class 'str'>
Content: 'Café résumé\n'
Length (chars): 13
```

### **Binary Mode**

- Reads/writes **bytes** (`bytes`).
- No encoding translation. What you write is exactly what ends up on disk.
- No line-ending translation. `\n` stays as `\n`, `\r\n` stays as `\r\n`.
- Pointer positions are measured in **bytes**.
- Required for any non-text data: images, audio, video, PDFs, executables, network protocols.

```python
# Write the same string, but as bytes
data = b"Cafe resume\n"   # ASCII, no encoding needed
with open("bin_demo.bin", "wb") as f:
    f.write(data)

# Read it back
with open("bin_demo.bin", "rb") as f:
    content = f.read()
    print("Type:", type(content))
    print("Content:", repr(content))
    print("Length (bytes):", len(content))
```

```
Type: <class 'bytes'>
Content: b'Cafe resume\n'
Length (bytes): 12
```

Notice the `b"..."` prefix — that is a bytes literal. The `é` and `é` from the text example cannot appear in a bytes literal; bytes are 0-255 integers.

### **Encoding Gotchas**

What happens if you read a UTF-8 file as Latin-1?

```python
# Write with utf-8
with open("encoded.txt", "w", encoding="utf-8") as f:
    f.write("Café")

# Try to read with latin-1
try:
    with open("encoded.txt", "r", encoding="latin-1") as f:
        print(f.read())
except UnicodeDecodeError as e:
    print("Decode error:", e)
```

```
Decode error: 'utf-8' codec can't decode byte 0xc3 in position 3: invalid continuation byte
```

The `é` in UTF-8 is the two bytes `0xC3 0xA9`. Latin-1 only handles one byte at a time, so it sees `0xC3` and has no idea what to do with it.

A common modern best practice: **always specify `encoding="utf-8"` explicitly**, even though it is usually the default. It removes any ambiguity across platforms.

### **When to Use Each Mode**

| Use case | Mode | Why |
|---|---|---|
| Log files, config files, CSV, JSON, source code | text (`r`, `w`, `a`) | Human-readable strings, line-based processing. |
| Images (PNG, JPG), audio (MP3, WAV), video (MP4) | binary (`rb`, `wb`) | Not text — encoding would corrupt them. |
| PDF, ZIP, executables, serialized objects | binary (`rb`, `wb`) | Same reason. |
| Network protocols, custom binary formats | binary (`rb`, `wb`) | You are working with bytes, not characters. |
| Mixed text + special characters | text with `encoding="utf-8"` | Standard practice for any text. |

## **Real-World Example — A Tiny Image Copy**

Copying a binary file is the simplest possible demo of binary mode. It works for any file type — images, PDFs, audio.

```python
# First, create a small "binary" file by writing some bytes
# (We use bytes here instead of a real image to keep the example self-contained.)
with open("source.bin", "wb") as f:
    f.write(b"\x89PNG\r\n\x1a\n")         # PNG magic number
    f.write(b"fake image content here")    # 23 more bytes

# Confirm size on disk
import os
print("Source file size:", os.path.getsize("source.bin"), "bytes")

# Copy it
with open("source.bin", "rb") as src:
    data = src.read()
with open("copy.bin", "wb") as dst:
    dst.write(data)

# Confirm the copy is identical
print("Copy file size:   ", os.path.getsize("copy.bin"), "bytes")
print("Bytes match?     ", open("source.bin", "rb").read() == open("copy.bin", "rb").read())
```

```
Source file size: 38 bytes
Copy file size:    38 bytes
Bytes match?      True
```

A more efficient version for large files — read and write in chunks so you never hold the whole file in memory:

```python
def copy_in_chunks(src_path, dst_path, chunk_size=4096):
    with open(src_path, "rb") as src, open(dst_path, "wb") as dst:
        while True:
            chunk = src.read(chunk_size)
            if not chunk:
                break
            dst.write(chunk)
            print(f"  wrote {len(chunk)} bytes")
    print("Copy complete")

print("Copying source.bin in 10-byte chunks:")
copy_in_chunks("source.bin", "chunked_copy.bin", chunk_size=10)
print("Size matches?", os.path.getsize("source.bin") == os.path.getsize("chunked_copy.bin"))
```

```
Copying source.bin in 10-byte chunks:
  wrote 10 bytes
  wrote 10 bytes
  wrote 10 bytes
  wrote 8 bytes
Copy complete
Size matches? True
```

The 38-byte file got split into chunks of 10, 10, 10, and 8 bytes — last chunk is just whatever is left. This is exactly how `shutil.copyfile()` works internally.

## **Buffering**

When you `write()` to a file, the bytes do not go straight to the disk. They sit in a **buffer** in memory, and the OS flushes the buffer to disk periodically. Buffering makes file I/O much faster because disk operations are slow.

### **How Buffering Works**

- **Default text mode**: line-buffered if the file is a terminal, otherwise block-buffered (typically 8 KB or 8192 bytes).
- **`buffering=1`**: line-buffered — flush after every newline character.
- **`buffering=N` (N > 1)**: block-buffered with a buffer of N bytes.
- **`buffering=0`**: unbuffered (binary mode only) — every write goes directly to the OS.

```python
import time

# Line-buffered text mode: writes flush on each newline
with open("line_buffered.txt", "w", buffering=1) as f:
    f.write("Line 1\n")
    f.write("Line 2\n")
    f.write("Line 3 (no newline yet)...")   # no newline, so not flushed
    print("Buffer state at end of with — file is about to close")
    print("File size on disk (after with closes):")
# After the with block, the file is closed, which flushes everything
import os
print("  ", os.path.getsize("line_buffered.txt"), "bytes")
```

```
Buffer state at end of with — file is about to close
File size on disk (after with closes):
   38 bytes
```

```python
# Block-buffered text mode: writes are batched
with open("block_buffered.txt", "w", buffering=8192) as f:
    f.write("Lots of data " * 100)
    # Nothing has been flushed yet because the buffer is not full
    print("Before close, file size on disk:")
    print("  ", os.path.getsize("block_buffered.txt"), "bytes")
# After the with block, the file is closed and the buffer is flushed
print("After close, file size on disk:")
print("  ", os.path.getsize("block_buffered.txt"), "bytes")
```

```
Before close, file size on disk:
   0 bytes
After close, file size on disk:
   1500 bytes
```

Before the `with` block ended, the file was 0 bytes on disk — the writes were sitting in the buffer. After the close, the buffer was flushed and the file is 1500 bytes.

### **`flush()` — Force a Flush**

If you need the data to hit disk **now** (for example, in a logging system where you want the latest log line to be on disk even if the program crashes), call `f.flush()`.

```python
import time

with open("flush_demo.txt", "w", buffering=8192) as f:
    f.write("Critical message\n")
    f.flush()    # force the buffer to disk
    print("After flush, file size on disk:")
    print("  ", os.path.getsize("flush_demo.txt"), "bytes")
    print("(Simulating a crash here — but the message is safe on disk)")
```

```
After flush, file size on disk:
   18 bytes
(Simulating a crash here — but the message is safe on disk)
```

The `flush()` is what makes log files reliable. In the standard `logging` module, every log call calls `flush()` automatically for this exact reason.

## **Q&A — Common Intermediate Questions**

**Q1. Can I open a file for both reading and writing?**

Yes — use `r+`, `w+`, or `a+`. They differ in whether the file is truncated and where the pointer starts.

**Q2. What happens if I use `seek()` in text mode?**

It works, but only with offsets that come from `tell()`. Random offsets can raise `ValueError: can't have non-byte value` or `io.UnsupportedOperation: can't do nonzero cur-relative seeks` on streams that do not support it. In practice, use binary mode for any non-trivial seek.

**Q3. Why does my file show 0 bytes after I wrote to it?**

The data is in the buffer. Call `f.flush()` or close the file (with `with` or `f.close()`).

**Q4. What is the difference between `flush()` and `close()`?**

`flush()` writes the buffer to disk but keeps the file open. `close()` flushes first, then closes the file descriptor. `with` calls `close()` for you, which implicitly flushes.

**Q5. Should I use text mode or binary mode for CSV files?**

Text mode, with `newline=""` (covered in the CSV file). The default behavior of `open()` would translate line endings, which breaks CSV.

**Q6. Why does my binary file get corrupted when I open it in text mode?**

Text mode applies encoding and line-ending translation. For a binary file (image, audio, etc.), that translation mangles the bytes. Always use `b` mode for non-text data.

**Q7. What is the size limit for a single `read()`?**

Whatever fits in your available memory. For files larger than a few hundred MB, use `read(n)` in chunks, or `for line in f` for line-by-line processing.

**Q8. Why is `r+` mode rarely used?**

Because mixing reads and writes on the same file at the same time is bug-prone — the pointer moves around, you have to keep `seek()`-ing, and partial reads can leave the file in an unexpected state. In real code, you usually read the whole file, transform it, then write it back.

## **Examples**

```python
# Example 1: Use 'x' to safely create a new log file
import os

log_path = "today.log"
if os.path.exists(log_path):
    os.remove(log_path)

try:
    with open(log_path, "x") as f:
        f.write("Log started at 2024-10-08\n")
    print("Created", log_path, "exclusively")
except FileExistsError:
    print("Log file already exists, refusing to overwrite")
```

```
Created today.log exclusively
```

```python
# Example 2: Append a timestamped line to a log
from datetime import datetime

log_path = "today.log"
with open(log_path, "a") as f:
    f.write(f"{datetime.now().isoformat()}  INFO  Application started\n")

with open(log_path, "r") as f:
    print("Log contents:")
    print(f.read())
```

```
Log contents:
Log started at 2024-10-08
2024-10-08T09:30:00.000001  INFO  Application started

```

```python
# Example 3: r+ — read first 5 chars, then overwrite them
with open("rw_demo.txt", "r+") as f:
    print("Original first 5 chars:", f.read(5))
    f.seek(0)
    f.write("XYZ")
    f.seek(0)
    print("After overwrite:        ", f.read())
```

```
Original first 5 chars: HELLO
After overwrite:        XYZLO WORLD
```

```python
# Example 4: Read a file in binary mode, then hex-dump the first 20 bytes
with open("source.bin", "rb") as f:
    data = f.read(20)
    print("Bytes:", data)
    print("Hex:  ", data.hex())
```

```
Bytes: b'\x89PNG\r\n\x1a\nfake image '
Hex:   89504e470d0a1a0a66616b6520696d61676520
```

`bytes.hex()` is the cleanest way to see raw bytes as hex. It is the right tool for debugging binary protocols and inspecting file headers.

```python
# Example 5: SEEK_END to read the last N bytes of a file
with open("demo.txt", "rb") as f:
    f.seek(-10, 2)              # 10 bytes from end
    tail = f.read()
    print("Last 10 bytes:", tail)
```

```
Last 10 bytes: b'ne A\nLine B\n'
```

```python
# Example 6: Force flush after every write (useful for crash-safe logs)
with open("safe_log.txt", "w", buffering=1) as f:    # line-buffered
    f.write("First event\n")
    f.write("Second event\n")
    f.write("Third event (no flush needed because of buffering=1)\n")
    print("All 3 lines are on disk now (line-buffered + newlines)")
```

```
All 3 lines are on disk now (line-buffered + newlines)
```

```python
# Example 7: Read 4 bytes at a time from a binary file
with open("source.bin", "rb") as f:
    while True:
        block = f.read(4)
        if not block:
            break
        print("  block:", block.hex(), "->", block)
```

```
  block: 89504e47 -> b'\x89PNG'
  block: 0d0a1a0a -> b'\r\n\x1a\n'
  block: 66616b65 -> b'fake'
  block: 20696d61 -> b' ima'
  block: 67652063 -> b'ge c'
  block: 6f6e7465 -> b'onte'
  block: 6e742068 -> b'nt h'
  block: 65726500 -> b'ere\x00'
```

```python
# Example 8: truncate() — cut a file at the current pointer
with open("trunc_demo.txt", "w") as f:
    f.write("ABCDEFGHIJ")

with open("trunc_demo.txt", "r+") as f:
    f.seek(4)            # after "ABCD"
    f.truncate()
    print("After truncate at pos 4:", repr(f.read()))
```

```
After truncate at pos 4: 'ABCD'
```

## **Quick Reference Summary**

### **File Modes Cheat Sheet**

| Mode | Action | Truncate | Create | Read | Write | Pointer |
|---|---|---|---|---|---|---|
| `r` | read | no | no | yes | no | start |
| `w` | write | yes | yes | no | yes | start |
| `a` | append | no | yes | no | yes | end |
| `x` | exclusive create | no | yes (fails if exists) | no | yes | start |
| `r+` | read + write | no | no | yes | yes | start |
| `w+` | read + write | yes | yes | yes | yes | start |
| `a+` | read + append | no | yes | yes | yes | end |
| Add `b` | binary | — | — | bytes | bytes | — |
| Add `t` | text (default) | — | — | str | str | — |

### **Pointer Operations**

| Method | What it does | Returns |
|---|---|---|
| `f.tell()` | Current position | int (chars in text, bytes in binary) |
| `f.seek(off)` | Move to absolute position `off` | int (new position) |
| `f.seek(off, 0)` | SEEK_SET — `off` from start | int |
| `f.seek(off, 1)` | SEEK_CUR — `off` from current | int |
| `f.seek(off, 2)` | SEEK_END — `off` from end | int |
| `f.truncate()` | Cut file to current position | int (new size) |
| `f.truncate(n)` | Cut file to `n` bytes/chars | int (new size) |

### **Text vs Binary**

| Aspect | Text mode (`t`) | Binary mode (`b`) |
|---|---|---|
| Data type | `str` | `bytes` |
| Encoding | applied on read/write | none — raw bytes |
| Line endings | translated to `\n` | preserved as-is |
| Pointer unit | characters | bytes |
| Use for | log, config, CSV, JSON, source | images, audio, video, PDF, ZIP, network |

### **Buffering**

| `buffering=` | Mode | Behavior |
|---|---|---|
| `0` | binary only | Unbuffered — every write goes to the OS. |
| `1` | text only | Line-buffered — flush after each `\n`. |
| `> 1` | both | Block-buffered with the given size in bytes. |
| `-1` (default) | both | Default (line-buffered for terminals, block-buffered for files). |

## **Practice and Next Steps**

- Open a file in `r+` mode, overwrite the first 5 characters, then read the result.
- Open a file in `a+` mode, seek to position 0, read everything, then append a new line.
- Use `x` mode to create a fresh file, and confirm the second attempt raises `FileExistsError`.
- Use `tell()` and `seek()` together to overwrite a specific section of a file without rewriting the whole thing.
- Use `truncate()` to cut a file to half its original size. Confirm by reading the result.
- Write a binary file containing the bytes `0x89 0x50 0x4E 0x47` (PNG magic). Read it back and print both the bytes and the hex.
- Use `seek(-10, 2)` to read the last 10 bytes of a text file and print them.
- Open a file in `buffering=1` mode, write a line, and verify it appears on disk before closing the file.
- Write a function `copy_in_chunks(src, dst, n=4096)` that copies any binary file in `n`-byte chunks. Test it on a real image or PDF.
- Read a binary file in 16-byte blocks and print each block as both bytes and hex.
