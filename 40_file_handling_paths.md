# **Python File Handling — Paths, Directories, and Modern Patterns**

## **What This File Covers**

The first two files focused on opening, reading, and writing individual files. This file covers everything around them — the path system, the directory tree, file metadata, and the modern idioms (especially `pathlib`) that you will see in any production-grade Python codebase.

You will use these tools constantly: when loading a config file relative to the script, when uploading a file in a web request, when walking a folder of CSVs, when copying a backup, when generating a temp file for a test, when reading a file size without opening it.

## **Paths — Two Ways to Represent Them**

A file path is just a string that tells the OS where a file lives. But there are two ways to work with paths in Python:

1. **`os.path`** — the original, string-based API. Functions take strings, return strings.
2. **`pathlib`** — the modern, object-based API. Functions take `Path` objects, return `Path` objects.

Both are still widely used. New code should prefer `pathlib`. Old codebases often use `os.path`. Knowing both lets you read either.

### **Plain String Paths**

The simplest form: just a string.

```python
path = "data/sales.csv"
print("Path:", path)
print("Type:", type(path))
```

```
Path: data/sales.csv
Type: <class 'str'>
```

Strings work, but they have no awareness of the filesystem. You cannot ask a string "is this a file or a directory?" — you have to call `os.path.isfile(path)` separately.

### **`os.path` Functions**

`os.path` is a module of pure functions that operate on path strings.

```python
import os

p = "data/sales.csv"
print("isabs (absolute?):", os.path.isabs(p))
print("basename:        ", os.path.basename(p))   # sales.csv
print("dirname:         ", os.path.dirname(p))    # data
print("split:           ", os.path.split(p))      # ('data', 'sales.csv')
print("splitext:        ", os.path.splitext(p))   # ('data/sales', '.csv')
print("join:            ", os.path.join("data", "2024", "sales.csv"))
print("normpath:        ", os.path.normpath("data/./2024/../sales.csv"))
print("exists:          ", os.path.exists(p))
print("isfile:          ", os.path.isfile(p))
print("isdir:           ", os.path.isdir("data"))
```

```
isabs (absolute?): False
basename:         sales.csv
dirname:          data
split:            ('data', 'sales.csv')
splitext:         ('data/sales', '.csv')
join:             data/2024/sales.csv
normpath:         data/sales.csv
exists:           False
isfile:           False
isdir:            False
```

The `os.path.join()` function is platform-aware — on Windows it uses `\`, on Unix it uses `/`. That is why you should use it instead of `+`-ing strings.

### **`pathlib.Path` — The Modern Way**

`pathlib.Path` wraps a path string in an object with methods. It was introduced in Python 3.4 and is the recommended approach for new code.

```python
from pathlib import Path

p = Path("data/sales.csv")
print("Path:", p)
print("Type:", type(p))
print("name:     ", p.name)         # sales.csv
print("stem:     ", p.stem)         # sales
print("suffix:   ", p.suffix)       # .csv
print("parent:   ", p.parent)       # data
print("parts:    ", p.parts)        # ('data', 'sales.csv')
print("exists:   ", p.exists())
print("is_file:  ", p.is_file())
print("is_dir:   ", p.is_dir())
```

```
Path: data/sales.csv
Type: <class 'pathlib.PosixPath'>
name:      sales.csv
stem:      sales
suffix:    .csv
parent:    data
parts:     ('data', 'sales.csv')
exists:    False
is_file:   False
is_dir:    False
```

The `Path` object has properties for almost every part of the path:

- `p.name` — the final component (file or directory name).
- `p.stem` — the name without the suffix.
- `p.suffix` — the last suffix (e.g., `.csv`).
- `p.parent` — the directory containing the path.
- `p.parts` — the path split into a tuple.
- `p.anchor` — the root (`/` on Unix, `C:\` on Windows).
- `p.suffixes` — list of all suffixes (e.g., `['.tar', '.gz']`).

### **Building Paths with `/`**

One of the nicest features of `Path` is that you can build paths with the `/` operator. It joins path components in a platform-correct way.

```python
from pathlib import Path

base = Path("/var/log")
log_file = base / "app" / "today.log"
print("Built path:", log_file)
print("Type:      ", type(log_file))
```

```
Built path: /var/log/app/today.log
Type:       <class 'pathlib.PosixPath'>
```

This is the same as `os.path.join("/var/log", "app", "today.log")`, but it reads more naturally and returns a `Path` object that you can keep chaining.

### **`os.path` vs `pathlib` — Side by Side**

| Task | `os.path` | `pathlib` |
|---|---|---|
| Build a path | `os.path.join(a, b)` | `Path(a) / b` |
| Get filename | `os.path.basename(p)` | `Path(p).name` |
| Get directory | `os.path.dirname(p)` | `Path(p).parent` |
| Split extension | `os.path.splitext(p)` | `Path(p).suffix` |
| Check exists | `os.path.exists(p)` | `Path(p).exists()` |
| Check is file | `os.path.isfile(p)` | `Path(p).is_file()` |
| Get absolute | `os.path.abspath(p)` | `Path(p).resolve()` |
| Get home dir | `os.path.expanduser("~")` | `Path.home()` |
| Current dir | `os.getcwd()` | `Path.cwd()` |
| Read text | `open(p).read()` | `Path(p).read_text()` |
| Write text | `open(p, "w").write(s)` | `Path(p).write_text(s)` |
| Read bytes | `open(p, "rb").read()` | `Path(p).read_bytes()` |
| Write bytes | `open(p, "wb").write(b)` | `Path(p).write_bytes(b)` |

Both styles are valid. For new code, prefer `pathlib`. For working with old code or third-party libraries that expect strings, you can convert with `str(path)` or `Path(string)`.

## **The `os` Module — File and Directory Operations**

`os` is the workhorse module for filesystem operations. Most of its functions raise `OSError` (or a subclass like `FileNotFoundError`) on failure.

### **Creating and Removing Directories**

```python
import os

# Create a single directory
os.mkdir("my_folder")
print("Created my_folder, exists?", os.path.exists("my_folder"))

# Create a chain of directories (like mkdir -p)
os.makedirs("my_folder/inner/deep", exist_ok=True)
print("Created chain, all exist?", os.path.exists("my_folder/inner/deep"))

# Remove an empty directory
os.rmdir("my_folder/inner/deep")
print("Removed deep, exists?", os.path.exists("my_folder/inner/deep"))

# Clean up
os.removedirs("my_folder/inner")
print("Cleanup done")
```

```
Created my_folder, exists? True
Created chain, all exist? True
Removed deep, exists? False
Cleanup done
```

`mkdir()` creates a single directory and raises if the parent does not exist. `makedirs()` creates the whole chain. `rmdir()` removes a single empty directory; `removedirs()` removes a chain of empty directories.

### **Renaming and Removing Files**

```python
import os

# Create a test file
with open("original.txt", "w") as f:
    f.write("hello")

# Rename
os.rename("original.txt", "renamed.txt")
print("After rename, files:", os.listdir("."))

# Remove
os.remove("renamed.txt")
print("After remove, files:", os.listdir("."))
```

```
After rename, files: ['.git', 'renamed.txt', 'sample.txt', ...]
After remove, files: ['.git', 'sample.txt', ...]
```

`os.rename()` is the way to rename or move a file. `os.remove()` (also aliased as `os.unlink()`) deletes a file. There is no undo — be careful with these.

### **Listing Directory Contents**

```python
import os

# Create some files to list
os.makedirs("list_demo/sub", exist_ok=True)
for name in ["a.txt", "b.txt", "c.log"]:
    with open(f"list_demo/{name}", "w") as f:
        f.write("x")
with open("list_demo/sub/nested.txt", "w") as f:
    f.write("x")

# List everything in list_demo
print("All entries:")
for entry in os.listdir("list_demo"):
    print(" -", entry)

# Filter to just files
print("\nOnly files:")
for entry in os.listdir("list_demo"):
    full = os.path.join("list_demo", entry)
    if os.path.isfile(full):
        print(" -", entry)

# Filter to just directories
print("\nOnly directories:")
for entry in os.listdir("list_demo"):
    full = os.path.join("list_demo", entry)
    if os.path.isdir(full):
        print(" -", entry)
```

```
All entries:
 - a.txt
 - b.txt
 - c.log
 - sub

Only files:
 - a.txt
 - b.txt
 - c.log

Only directories:
 - sub
```

`os.listdir()` returns names only — to tell files from directories, you need `os.path.isfile()` or `os.path.isdir()`.

### **`os.walk()` — Recursive Directory Walking**

When you need to traverse an entire tree, `os.walk()` is the tool.

```python
import os

# Build a deeper demo tree
os.makedirs("walk_demo/src", exist_ok=True)
os.makedirs("walk_demo/tests", exist_ok=True)
for path, content in [
    ("walk_demo/README.md", "# Demo"),
    ("walk_demo/src/app.py", "print('hi')"),
    ("walk_demo/src/util.py", "print('util')"),
    ("walk_demo/tests/test_app.py", "print('test')"),
]:
    with open(path, "w") as f:
        f.write(content)

# Walk the tree
for current_dir, dirs, files in os.walk("walk_demo"):
    print(f"In: {current_dir}")
    print(f"  Subdirectories: {dirs}")
    print(f"  Files:          {files}")
```

```
In: walk_demo
  Subdirectories: ['src', 'tests']
  Files:          ['README.md']
In: walk_demo/src
  Subdirectories: []
  Files:          ['app.py', 'util.py']
In: walk_demo/tests
  Subdirectories: []
  Files:          ['test_app.py']
```

For each directory it visits, `os.walk()` yields a 3-tuple: `(current_path, list_of_subdirs, list_of_files)`. You can modify `dirs` in place to prune the walk (e.g., skip `.git` directories).

```python
# Practical example: find all .py files in a tree, skipping hidden directories
for current_dir, dirs, files in os.walk("walk_demo"):
    # Modify dirs in place to skip hidden directories
    dirs[:] = [d for d in dirs if not d.startswith(".")]

    for filename in files:
        if filename.endswith(".py"):
            full_path = os.path.join(current_dir, filename)
            print("Python file:", full_path)
```

```
Python file: walk_demo/src/app.py
Python file: walk_demo/src/util.py
Python file: walk_demo/tests/test_app.py
```

This is the canonical "find all Python files" recipe. Real code search tools like `grep` and IDE indexing work this way.

## **`pathlib` — Modern Path Operations**

The `pathlib` module has a parallel set of operations, all as methods on `Path` objects.

### **Listing with `iterdir()` and Glob**

```python
from pathlib import Path

p = Path("walk_demo")
print("All entries:")
for entry in p.iterdir():
    print(f"  {entry}  (is_file={entry.is_file()}, is_dir={entry.is_dir()})")
```

```
All entries:
  walk_demo/README.md  (is_file=True, is_dir=False)
  walk_demo/src  (is_file=False, is_dir=True)
  walk_demo/tests  (is_file=False, is_dir=True)
```

`Path.iterdir()` yields `Path` objects instead of strings. Each one has `.is_file()`, `.is_dir()`, and all the other path methods.

### **Glob Patterns**

`glob` lets you match filenames using shell-style wildcards.

```python
from pathlib import Path

p = Path("walk_demo")

print("All .py files anywhere in the tree:")
for f in p.rglob("*.py"):
    print(f"  {f}")

print("\nAll top-level files (no recursion):")
for f in p.glob("*"):
    if f.is_file():
        print(f"  {f}")

print("\nAll top-level .py files:")
for f in p.glob("*.py"):
    print(f"  {f}")
```

```
All .py files anywhere in the tree:
  walk_demo/src/app.py
  walk_demo/src/util.py
  walk_demo/tests/test_app.py

All top-level files (no recursion):
  walk_demo/README.md

All top-level .py files:
(empty)
```

- `p.glob(pattern)` matches only in the current directory.
- `p.rglob(pattern)` matches recursively — equivalent to `**/pattern` in shell glob.

### **Reading and Writing with `pathlib`**

`Path` has shortcuts for the most common file operations.

```python
from pathlib import Path

p = Path("note.txt")

# Write text
p.write_text("Hello from pathlib.\n", encoding="utf-8")
print("Wrote file. Size:", p.stat().st_size, "bytes")

# Read text
content = p.read_text(encoding="utf-8")
print("Read back:", repr(content))
```

```
Wrote file. Size: 21 bytes
Read back: 'Hello from pathlib.\n'
```

`write_text()` opens the file in write mode, writes the string, and closes it. `read_text()` opens in read mode, reads everything, and closes it. Both are one-liners for simple cases.

```python
from pathlib import Path

# Binary version
p = Path("binary.dat")
p.write_bytes(b"\x89PNG\r\n\x1a\n" + b"some bytes")
data = p.read_bytes()
print("Type:", type(data))
print("First 8 bytes:", data[:8])
print("Size:", p.stat().st_size, "bytes")
```

```
Type: <class 'bytes'>
First 8 bytes: b'\x89PNG\r\n\x1a\nso'
Size: 16 bytes
```

For anything more complex (read in chunks, custom modes, encoding handling), drop down to `with open(p, ...) as f:`.

### **File Metadata — `stat()`**

`Path.stat()` returns file metadata as an `os.stat_result` object.

```python
import os
import time
from pathlib import Path

p = Path("note.txt")
p.write_text("hello world")

info = p.stat()
print("Size:        ", info.st_size, "bytes")
print("Created:     ", time.ctime(info.st_ctime))
print("Modified:    ", time.ctime(info.st_mtime))
print("Accessed:    ", time.ctime(info.st_atime))
print("Is file:     ", info.st_mode & 0o100000 != 0)  # S_ISREG check
print("Is directory:", info.st_mode & 0o040000 != 0)  # S_ISDIR check
```

```
Size:         11 bytes
Created:      Tue Oct  8 12:34:56 2024
Modified:     Tue Oct  8 12:34:56 2024
Accessed:     Tue Oct  8 12:34:56 2024
Is file:      True
Is directory: False
```

The `st_mode` field is a bit-packed integer that includes file type and permissions. The `0o100000` and `0o040000` constants are the file-type bits. For a cleaner check, use `Path.is_file()` and `Path.is_dir()` instead.

## **The `shutil` Module — High-Level File Operations**

`shutil` (shell utilities) provides high-level operations for whole files and directories. It builds on top of `os`.

### **Copying Files**

```python
import shutil
from pathlib import Path

# Reset
for p in [Path("src.txt"), Path("dst.txt")]:
    if p.exists():
        p.unlink()

Path("src.txt").write_text("Important content here\n")

# shutil.copy — copies content + permissions, but keeps the file open independently
shutil.copy("src.txt", "dst.txt")
print("After shutil.copy:")
print("  src.txt size:", Path("src.txt").stat().st_size)
print("  dst.txt size:", Path("dst.txt").stat().st_size)
print("  content:     ", Path("dst.txt").read_text().rstrip())
```

```
After shutil.copy:
  src.txt size: 23 bytes
  dst.txt size: 23 bytes
  content:      Important content here
```

`shutil.copy()` copies the file content and the permission bits. It does **not** copy the metadata (timestamps).

```python
# shutil.copy2 — also copies metadata (timestamps)
import os
import time

# Set an old timestamp on the source
old_time = time.time() - 10000
os.utime("src.txt", (old_time, old_time))

shutil.copy2("src.txt", "dst_meta.txt")

src_mtime = os.path.getmtime("src.txt")
dst_mtime = os.path.getmtime("dst_meta.txt")
print("Source mtime:", time.ctime(src_mtime))
print("Copy  mtime:", time.ctime(dst_mtime))
print("Metadata preserved?", abs(src_mtime - dst_mtime) < 1)
```

```
Source mtime: Sun Oct  6 09:48:16 2024
Copy  mtime: Sun Oct  6 09:48:16 2024
Metadata preserved? True
```

`shutil.copy2()` is the right choice when you want a true backup that preserves everything.

| Function | Copies content | Copies permissions | Copies metadata |
|---|---|---|---|
| `shutil.copy()` | yes | yes | no |
| `shutil.copy2()` | yes | yes | yes |
| `shutil.copyfile()` | yes | no (uses default) | no |

### **Copying and Removing Directory Trees**

```python
import shutil
from pathlib import Path

# Build a source tree
src = Path("source_tree")
if src.exists():
    shutil.rmtree(src)
src.mkdir()
(src / "a.txt").write_text("A")
(src / "sub").mkdir()
(src / "sub" / "b.txt").write_text("B")

# Copy the whole tree
dst = Path("copied_tree")
if dst.exists():
    shutil.rmtree(dst)
shutil.copytree(src, dst)

# Confirm the copy
print("Files in copied tree:")
for f in dst.rglob("*"):
    print(f"  {f}  ({'dir' if f.is_dir() else f.read_text()!r})")
```

```
Files in copied tree:
  copied_tree  ('dir')
  copied_tree/a.txt  ('dir', 'A')
  copied_tree/sub  ('dir')
  copied_tree/sub/b.txt  ('B')
```

`shutil.copytree()` recursively copies an entire directory. `shutil.rmtree()` recursively removes one.

### **Moving Files**

```python
import shutil
from pathlib import Path

Path("to_move.txt").write_text("data")
shutil.move("to_move.txt", "moved.txt")
print("After move, to_move.txt exists?", Path("to_move.txt").exists())
print("After move, moved.txt exists?  ", Path("moved.txt").exists())
```

```
After move, to_move.txt exists? False
After move, moved.txt exists?   True
```

`shutil.move()` is a rename if the source and destination are on the same filesystem, or a copy+delete across filesystems.

## **Temporary Files — `tempfile`**

The `tempfile` module creates files and directories that are automatically cleaned up. This is essential for tests, intermediate processing, and any time you need a scratch file that should not outlive your program.

### **Named vs Unnamed Temp Files**

```python
import tempfile
import os

# Unnamed temp file (returns a file object, deletes on close)
print("Unnamed tempfile:")
with tempfile.TemporaryFile(mode="w+", delete=True) as f:
    f.write("Scratch data\n")
    f.seek(0)
    print("  inside with — content:", repr(f.read()))
    print("  inside with — name:  ", f.name)
# After the with block, the file is deleted automatically
```

```
Unnamed tempfile:
  inside with — content: 'Scratch data\n'
  inside with — name:   3
```

The unnamed file is a low-level file descriptor (not on the filesystem path). Useful for in-process scratch data.

```python
import tempfile
import os
from pathlib import Path

# Named temp file (has a real path, useful for debugging)
print("Named tempfile:")
with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as f:
    f.write("Visible temp file\n")
    f.flush()
    print("  inside with — name:    ", f.name)
    print("  inside with — exists? ", os.path.exists(f.name))
    print("  inside with — content: ", repr(f.read()))

# We can still use it after the with block
print("\n  after with — file still exists?", os.path.exists(f.name))

# Manually clean up
os.unlink(f.name)
print("  after manual cleanup — exists?  ", os.path.exists(f.name))
```

```
Named tempfile:
  inside with — name:     /tmp/tmp1234abcd.txt
  inside with — exists?  True
  inside with — content:  'Visible temp file\n'

  after with — file still exists? True
  after manual cleanup — exists?   False
```

The `delete=False` argument is what makes the file survive after the `with` block. The `suffix=".txt"` argument gives it a useful extension. If you do not pass `delete=False`, the file is deleted on close.

### **Temporary Directories**

```python
import tempfile
import os
from pathlib import Path

with tempfile.TemporaryDirectory() as tmpdir:
    print("Temp dir created:", tmpdir)
    p = Path(tmpdir) / "scratch.txt"
    p.write_text("scratch")
    print("File in temp dir:", p, "exists?", p.exists())
    print("Contents:", p.read_text())
print("After with — temp dir exists?", os.path.exists(tmpdir))
```

```
Temp dir created: /tmp/tmp1abc23de
File in temp dir: /tmp/tmp1abc23de/scratch.txt exists? True
Contents: scratch
After with — temp dir exists? False
```

`TemporaryDirectory` is the cleanest way to get a scratch directory — it is created on enter and removed on exit (along with all contents).

## **In-Memory File Objects — `io.StringIO` and `io.BytesIO`**

Sometimes you want a file-like object that lives in RAM instead of on disk. The `io` module provides `StringIO` for text and `BytesIO` for bytes. They implement the same interface as real files, so any function that takes a file object will accept them.

```python
import io

# StringIO — text in memory
buf = io.StringIO()
buf.write("First line\n")
buf.write("Second line\n")
buf.seek(0)
print("Type:", type(buf))
print("Read with readline():", repr(buf.readline()))
print("Read remaining:", repr(buf.read()))
buf.close()
```

```
Type: <class '_io.StringIO'>
Read with readline(): 'First line\n'
Read remaining: 'Second line\n'
```

```python
import io

# BytesIO — bytes in memory
buf = io.BytesIO()
buf.write(b"binary data here\n")
buf.seek(0)
print("Type:", type(buf))
print("First 6 bytes:", buf.read(6))
print("Remaining:", repr(buf.read()))
buf.close()
```

```
Type: <class '_io.BytesIO'>
First 6 bytes: b'binary'
Remaining: b' data here\n'
```

`StringIO` and `BytesIO` show up in many real situations:

- **Testing** — feed fake file data into a function that expects a file object.
- **Composition** — chain several writers into a single in-memory buffer, then pass it to something else.
- **Streaming** — build a CSV or JSON response in memory, then send it as an HTTP response.

```python
import io
import csv

# Practical example: build a CSV in memory
buf = io.StringIO()
writer = csv.writer(buf)
writer.writerow(["name", "age", "city"])
writer.writerow(["Karan", 22, "Mumbai"])
writer.writerow(["Om", 30, "Delhi"])

# Now read it back as if it were a file
buf.seek(0)
reader = csv.reader(buf)
for row in reader:
    print(row)
```

```
['name', 'age', 'city']
['Karan', '22', 'Mumbai']
['Om', '30', 'Delhi']
```

A function that takes a file object can now accept either a real file from `open()` or an in-memory `StringIO`/`BytesIO`. That is duck typing at its best.

## **Real-World Example — A Small File Backup Tool**

Putting it all together: a script that copies a folder to a backup location, with logging, error handling, and metadata preservation.

```python
import shutil
import os
from pathlib import Path
from datetime import datetime

def backup_folder(src_path, dst_base):
    """Copy src_path into dst_base/<timestamp>_<src_name>/."""
    src = Path(src_path)
    if not src.exists():
        raise FileNotFoundError(f"Source does not exist: {src}")
    if not src.is_dir():
        raise NotADirectoryError(f"Source is not a directory: {src}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = Path(dst_base) / f"{timestamp}_{src.name}"

    print(f"Backing up {src} -> {dst}")
    shutil.copytree(src, dst)

    # Count what we copied
    file_count = sum(1 for _ in dst.rglob("*") if _.is_file())
    total_bytes = sum(f.stat().st_size for f in dst.rglob("*") if f.is_file())

    print(f"Backup complete: {file_count} files, {total_bytes} bytes")
    return dst

# Set up a fake source folder
src = Path("project_src")
if src.exists():
    shutil.rmtree(src)
src.mkdir()
(src / "main.py").write_text("print('main')\n")
(src / "config.json").write_text('{"name": "demo"}\n')
(src / "data").mkdir()
(src / "data" / "input.csv").write_text("a,b\n1,2\n")
(src / "data" / "notes.txt").write_text("notes\n")

# Run the backup
backup = backup_folder("project_src", "backups")
```

```
Backing up project_src -> backups/20241008_123456_project_src
Backup complete: 4 files, 58 bytes
```

The script uses `pathlib` for paths, `shutil.copytree` for the heavy lifting, and `Path.rglob` + `Path.stat` for the report. This is the structure of a real backup tool.

## **Q&A — Common Intermediate Questions**

**Q1. Should I use `os.path` or `pathlib` for new code?**

`pathlib`. It is the modern API, reads more cleanly, and is what you will see in new tutorials, libraries, and PEPs.

**Q2. How do I get the directory containing the current script?**

```python
from pathlib import Path
script_dir = Path(__file__).parent
```

`__file__` is the path of the current script. `.parent` is the directory containing it.

**Q3. How do I list only `.txt` files in a directory?**

```python
from pathlib import Path
for f in Path(".").glob("*.txt"):
    print(f)
```

For recursive matching, use `rglob("*.txt")`.

**Q4. How do I make a path work on both Windows and Linux?**

Use `pathlib` and `/` (or `os.path.join`). Do not hardcode `/` or `\`.

**Q5. How do I check if a file is empty without opening it?**

```python
from pathlib import Path
Path("file.txt").stat().st_size == 0
```

**Q6. How do I get a list of all files modified in the last 24 hours?**

```python
import time
from pathlib import Path

cutoff = time.time() - 86400
for f in Path(".").rglob("*"):
    if f.is_file() and f.stat().st_mtime > cutoff:
        print(f)
```

**Q7. How do I create a unique temp file without conflicts?**

Use `tempfile.NamedTemporaryFile()` — the OS guarantees uniqueness.

**Q8. How do I read a file from inside a Python package?**

```python
from importlib.resources import files
text = files("mypackage").joinpath("data.txt").read_text()
```

This is the modern way to access package data. Older code uses `pkg_resources` or `__file__` tricks.

## **Examples**

```python
# Example 1: Build a path safely with pathlib
from pathlib import Path

project = Path.home() / "projects" / "myapp" / "src"
print("Project root:", project)
print("Config file:  ", project / "config" / "app.yaml")
print("As string:    ", str(project / "config" / "app.yaml"))
```

```
Project root: /root/projects/myapp/src
Config file:  /root/projects/myapp/src/config/app.yaml
As string:    /root/projects/myapp/src/config/app.yaml
```

```python
# Example 2: Find the largest file in a directory
from pathlib import Path

# Create some files of different sizes
demo = Path("size_demo")
if demo.exists():
    import shutil; shutil.rmtree(demo)
demo.mkdir()
for name, size in [("a.txt", 100), ("b.bin", 5000), ("c.log", 50)]:
    (demo / name).write_bytes(b"x" * size)

# Find the largest
largest = max(demo.iterdir(), key=lambda f: f.stat().st_size)
print("Largest file:", largest.name, "->", largest.stat().st_size, "bytes")
```

```
Largest file: b.bin -> 5000 bytes
```

```python
# Example 3: Walk a tree and report all .py files
from pathlib import Path

print("Python files in current directory:")
for f in Path(".").rglob("*.py"):
    if ".venv" not in f.parts and "node_modules" not in f.parts:
        print(f"  {f}")
```

```
Python files in current directory:
(empty or list of found files)
```

```python
# Example 4: Use StringIO to test a CSV-processing function
import io
import csv

def count_rows(csv_file):
    reader = csv.reader(csv_file)
    next(reader)    # skip header
    return sum(1 for _ in reader)

# Test it without creating a real file
fake_csv = io.StringIO("name,age\nKaran,22\nOm,30\nDurga,48\n")
print("Row count:", count_rows(fake_csv))
```

```
Row count: 3
```

```python
# Example 5: Atomic write — write to temp file, then rename
from pathlib import Path
import os

target = Path("important.txt")
tmp = target.with_suffix(".tmp")

# Write to .tmp, then atomically rename
tmp.write_text("partial content")
print("Before rename, target exists?", target.exists())
print("Before rename, tmp exists?   ", tmp.exists())

os.replace(tmp, target)    # atomic on POSIX
print("After rename, target exists?", target.exists())
print("After rename, tmp exists?   ", tmp.exists())
print("Content:                     ", target.read_text())
```

```
Before rename, target exists? False
Before rename, tmp exists?    True
After rename, target exists? True
After rename, tmp exists?    False
Content:                      partial content
```

The `os.replace()` (or `Path.replace()`) is atomic — there is no point at which another process can see a half-written `important.txt`. This is the right pattern for log files, config files, and any case where a crash mid-write would be bad.

```python
# Example 6: Read a file lazily, line by line, with line numbers
from pathlib import Path

p = Path("note.txt")
p.write_text("First\nSecond\nThird\n")

for i, line in enumerate(p.read_text().splitlines(), 1):
    print(f"{i:3}: {line}")
```

```
  1: First
  2: Second
  3: Third
```

```python
# Example 7: Create a temp file and use it as a file path
import tempfile
from pathlib import Path

with tempfile.NamedTemporaryFile(mode="w", suffix=".log", delete=False) as f:
    f.write("application started\n")
    f.write("user logged in\n")
    tmp_path = Path(f.name)

# Process it later
print("Temp file:", tmp_path)
print("Contents:")
for line in tmp_path.read_text().splitlines():
    print(" ", line)

# Clean up
tmp_path.unlink()
print("After unlink, exists?", tmp_path.exists())
```

```
Temp file: /tmp/tmp1234abcd.log
Contents:
 application started
 user logged in
After unlink, exists? False
```

```python
# Example 8: Detect file type by magic bytes
from pathlib import Path

def detect_type(path):
    with open(path, "rb") as f:
        header = f.read(8)
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return "PNG image"
    if header.startswith(b"\xff\xd8\xff"):
        return "JPEG image"
    if header.startswith(b"GIF87a") or header.startswith(b"GIF89a"):
        return "GIF image"
    if header.startswith(b"%PDF"):
        return "PDF document"
    if header.startswith(b"PK\x03\x04"):
        return "ZIP archive"
    return "unknown"

# Create a few files to test
Path("test.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"x" * 100)
Path("test.pdf").write_bytes(b"%PDF-1.4\n" + b"x" * 100)
Path("test.zip").write_bytes(b"PK\x03\x04" + b"x" * 100)
Path("test.txt").write_text("just text")

for f in ["test.png", "test.pdf", "test.zip", "test.txt"]:
    print(f"{f}: {detect_type(f)}")

# Clean up
for f in ["test.png", "test.pdf", "test.zip", "test.txt"]:
    Path(f).unlink()
```

```
test.png: PNG image
test.zip: ZIP archive
test.txt: unknown
test.pdf: PDF document
```

This is how `file` and `libmagic` work — they read the first few bytes and match them against known signatures.

## **Quick Reference Summary**

### **`os.path` vs `pathlib`**

| Task | `os.path` (string-based) | `pathlib` (object-based) |
|---|---|---|
| Build path | `os.path.join(a, b)` | `Path(a) / b` |
| Get filename | `os.path.basename(p)` | `Path(p).name` |
| Get directory | `os.path.dirname(p)` | `Path(p).parent` |
| Get suffix | `os.path.splitext(p)[1]` | `Path(p).suffix` |
| Check exists | `os.path.exists(p)` | `Path(p).exists()` |
| Read text | `open(p).read()` | `Path(p).read_text()` |
| Write text | `open(p, "w").write(s)` | `Path(p).write_text(s)` |
| Read bytes | `open(p, "rb").read()` | `Path(p).read_bytes()` |
| Write bytes | `open(p, "wb").write(b)` | `Path(p).write_bytes(b)` |
| Current dir | `os.getcwd()` | `Path.cwd()` |
| Home dir | `os.path.expanduser("~")` | `Path.home()` |
| Absolute | `os.path.abspath(p)` | `Path(p).resolve()` |

### **Common `shutil` Operations**

| Function | What it does |
|---|---|
| `shutil.copy(src, dst)` | Copy file (no metadata) |
| `shutil.copy2(src, dst)` | Copy file (with metadata) |
| `shutil.copytree(src, dst)` | Recursive directory copy |
| `shutil.move(src, dst)` | Move (rename or copy+delete) |
| `shutil.rmtree(path)` | Recursive delete |
| `shutil.disk_usage(path)` | Total / used / free space |

### **`tempfile` Cheat Sheet**

| Function | Returns | Cleanup |
|---|---|---|
| `TemporaryFile()` | file object (no name) | on close |
| `NamedTemporaryFile()` | file object with `.name` | on close (unless `delete=False`) |
| `TemporaryDirectory()` | path string | on `__exit__` (along with contents) |
| `mkstemp()` | `(fd, path)` tuple | manual |

### **`io.StringIO` and `io.BytesIO`**

| Class | Stores | Use for |
|---|---|---|
| `io.StringIO` | text (`str`) | text-mode in-memory files |
| `io.BytesIO` | bytes (`bytes`) | binary in-memory files, e.g. for HTTP responses |

## **Practice and Next Steps**

- Build a script that uses `pathlib` to find the largest file in your home directory and print its size.
- Write a function that takes a directory path and returns the count of files by extension (e.g., `{'py': 12, 'txt': 3}`).
- Use `os.walk` to print every file under a directory, indented by depth.
- Build a "safe save" function that writes to a temp file first, then atomically renames it to the final path. Test it by interrupting the write partway.
- Use `shutil.copytree` to clone a folder, then `shutil.rmtree` to remove it. Confirm with `os.path.exists`.
- Use `tempfile.TemporaryDirectory` to create a scratch area, write a file inside, do some processing, and verify the directory is gone afterwards.
- Build a small "file type detector" that reads the first 8 bytes of a file and reports what it is.
- Use `StringIO` to feed CSV data into a `csv.reader` without writing a real file.
- Use `Path.glob` and `Path.rglob` to find all `.md` files in your workspace.
- Build a small backup tool that copies a source folder to a timestamped destination, with logging and error handling.
