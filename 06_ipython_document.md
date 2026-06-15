# IPython Practical Workflow Guide
> Scope: Daily engineering use — file ops, scripting, inspection, debugging, and automation from inside IPython.
> Context: Windows (`D:\Python\01_language_basics\pysh\`), IPython 9.x

---

## 0. Common Mistakes — What NOT To Do

These are real errors made during actual use. Read this first.

### Mistake 1 — Running terminal commands inside IPython

```python
# WRONG — typed inside IPython prompt
ipython --no-banner
ipython -i hello.py
```

```
NameError: name 'ipython' is not defined
SyntaxError: invalid syntax
```

`ipython` is a terminal binary. You can't call it from inside itself.

```powershell
# CORRECT — run these in PowerShell BEFORE launching IPython
ipython --no-banner
ipython -i hello.py
```

Once you see `In [1]:` you are inside IPython. Terminal commands go in PowerShell. IPython commands go in IPython.

---

### Mistake 2 — Pasting `%%writefile` as a single line

```python
# WRONG — pasted all on one line
%%writefile hello.py def greet(name): return f"Hello, {name}!" print(greet("Akshay"))
```

`%%writefile` is a **cell magic**. It must be the first line of input, and every subsequent line of content must be entered one by one on separate lines.

```python
# CORRECT — each line entered separately, Enter twice at the end
%%writefile hello.py
def greet(name):
    return f"Hello, {name}!"

print(greet("Akshay"))

```

Press **Enter on an empty line** to close and save. You will see `Writing hello.py`.

---

### Mistake 3 — Not pressing Enter twice to close the block

After the last line of a `%%writefile` block (or any multiline block), you must press Enter on a **blank line** to signal end of input. If you just press Enter after the last code line, IPython waits for more input and the file never gets written.

```
%%writefile hello.py
def greet(name):
    return f"Hello, {name}!"
                              ← press Enter here on blank line to close
Writing hello.py              ← only appears after blank Enter
```

---

### Mistake 4 — Using `!cd` to navigate

```python
# WRONG — cd in a subprocess dies immediately
!cd D:\Python\01_language_basics\pysh
```

The directory change happens in a temporary subprocess and is lost instantly. IPython's `%pwd` still shows the old path.

```python
# CORRECT — use the %cd magic which persists in the session
%cd D:\Python\01_language_basics\pysh
```

---

## 1. Launching IPython in Your Working Directory

Open PowerShell, navigate first, then launch:

```powershell
cd D:\Python\01_language_basics\pysh
ipython
```

Useful launch flags (PowerShell only, before entering IPython):

```powershell
ipython --no-banner          # skip the startup text
ipython -i hello.py          # run hello.py then drop into shell with its namespace loaded
ipython --profile=myprofile  # launch with a specific profile
```

Once inside, confirm location:

```python
%pwd
%ls
```

---

## 2. Navigation — Moving Around the Filesystem

| Command | What it does |
|---|---|
| `%pwd` | Print current directory |
| `%cd path` | Change directory (persists in session) |
| `%ls` | List files |
| `%mkdir dirname` | Create directory |
| `%rm filename` | Remove file |
| `%cp src dst` | Copy file |
| `%mv src dst` | Move/rename file |
| `%pushd path` | Push current dir to stack, cd into path |
| `%popd` | Pop back to previous dir |
| `%dhist` | Show directory visit history |

```python
%cd D:\Python\01_language_basics\pysh
%mkdir experiments
%cd experiments
%pwd
%cd ..
```

> ⚠️ **Watch out:** `%ls` on Windows can behave inconsistently. Fall back to `!dir` or `!dir /b` for reliable file listing.

---

## 3. Creating Files — `%%writefile`

Everything after `%%writefile filename` on the next lines becomes the file content. Press Enter on a blank line at the end to save.

**Python file:**

```python
%%writefile hello.py
def greet(name):
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(greet("Akshay"))

```

Output: `Writing hello.py`

**Append to existing file (`-a` flag):**

```python
%%writefile -a hello.py
def farewell(name):
    return f"Goodbye, {name}!"

```

Output: `Appending to hello.py`

**JSON config file:**

```python
%%writefile config.json
{
  "model": "nemotron",
  "temperature": 0.3,
  "max_tokens": 2048
}

```

**Text file:**

```python
%%writefile notes.txt
Session notes — 14 Jun 2026
- Tested greet() function
- Config written

```

---

## 4. Reading Files

### `%load` — load file content into input buffer

```python
%load hello.py
```

This pastes the file's content into the current input cell. Press Enter to execute. After execution, all top-level names from the file are in your session namespace.

> ⚠️ **Watch out:** Re-running `%load` on a file you already modified in the session reloads the original file and overwrites your in-session edits.

### Print file contents to screen

```python
!type hello.py      # Windows
!cat hello.py       # Linux / Mac
```

### Read into a Python variable

```python
from pathlib import Path
text = Path("notes.txt").read_text()
print(text)
```

---

## 5. Running Files — `%run`

```python
%run hello.py
```

After `%run`, all top-level names from the script are available in your session:

```python
%run hello.py
greet("Ravi")       # function is now in session namespace
```

Flags:

```python
%run -t hello.py    # print wall-clock time after execution
%run -n hello.py    # execute but do NOT import names into session
%run -i hello.py    # run in current namespace (shares your session variables)
```

Run with arguments:

```python
%run myscript.py --input data.csv --epochs 10
```

---

## 6. Shell Commands With `!`

Anything after `!` runs as a system command in a temporary subprocess.

```python
!pip install rich
!python --version
!dir                         # Windows
!dir /b                      # bare filenames only
!echo "test" > output.txt    # write via shell redirect
```

**Capture shell output into a Python variable:**

```python
files = !dir /b
print(files)
# ['config.json', 'experiments', 'hello.py', 'notes.txt']

py_files = [f for f in files if f.endswith(".py")]
```

**Inject Python variables into shell commands:**

```python
target = "hello.py"
!python {target}     # {varname} expands the Python variable
```

---

## 7. Namespace Inspection

```python
%who            # list all variable names
%whos           # names + type + value summary
%who str        # only string variables
%who function   # only functions
```

Inspect any object:

```python
greet?          # docstring + signature
greet??         # full source code
Path?           # works on any class or object
```

---

## 8. History

```python
%history            # all inputs this session
%history -n         # with line numbers
%history 1-10       # lines 1 through 10
%history -g greet   # search history for keyword
```

Save history to file:

```python
%history -f session_log.py
```

Re-run or recall a past line:

```python
%rerun 5        # re-execute line 5
%recall 5       # paste line 5 into input buffer (editable before running)
```

---

## 9. Timing and Profiling

```python
%time sum(range(1_000_000))              # single run timing
%timeit sum(range(1_000_000))            # averaged over many runs
%timeit -n 100 -r 5 sum(range(1_000_000))
```

Cell-level timing:

```python
%%timeit
total = 0
for i in range(1_000_000):
    total += i

```

Profile a call (cProfile output):

```python
%prun sum(range(1_000_000))
```

---

## 10. Debugging

```python
1 / 0
# ZeroDivisionError

%debug      # drop into pdb at the point of failure
```

Auto-launch debugger on every exception:

```python
%pdb on
```

Key pdb commands inside `%debug`:

| Command | Action |
|---|---|
| `p varname` | print variable |
| `n` | next line |
| `s` | step into function |
| `c` | continue |
| `q` | quit debugger |
| `l` | list surrounding code |
| `u` / `d` | move up/down stack frames |

---

## 11. Environment Variables

```python
%env                        # show all env vars
%env PATH                   # get one var
%env MY_API_KEY=abc123      # set for this session
```

For `.env` files (LangChain / LLM work):

```python
from dotenv import load_dotenv
import os

load_dotenv(".env")
os.getenv("OPENROUTER_API_KEY")
```

---

## 12. Aliases

```python
%alias show_py dir *.py /b       # Windows: list .py files
%alias run_main python main.py
%alias_magic t timeit             # %t as shorthand for %timeit
```

Persist aliases across sessions — add to:
`C:\Users\Admin\.ipython\profile_default\startup\00_aliases.ipy`

---

## 13. Saving Work

Save specific lines to a file:

```python
%save greet_module.py 8-10 20    # saves lines 8, 9, 10 and 20
```

Save entire session:

```python
%history -f full_session.py
```

---

## 14. Multiline Code

IPython auto-indents after `:` — just keep typing:

```python
for i in range(3):
    print(i)
                    # press Enter on blank line to run
```

Paste from clipboard (strips `>>>` prompts automatically):

```python
%paste      # pulls from clipboard and executes
%cpaste     # interactive paste mode; type -- on blank line to finish
```

---

## 15. Reset and Cleanup

```python
%reset -f               # clear all variables, no prompt
%reset_selective greet  # delete only 'greet'
%xdel big_array         # delete + trigger garbage collection immediately
```

---

## 16. Full Workflow Example

```python
# 1 — confirm location
%pwd
%ls

# 2 — create a Python module
%%writefile data_loader.py
import json
from pathlib import Path

def load_config(path="config.json"):
    return json.loads(Path(path).read_text())

def summarize(cfg):
    for k, v in cfg.items():
        print(f"  {k}: {v}")


# 3 — create a config file
%%writefile config.json
{
  "model": "nemotron",
  "temperature": 0.3,
  "max_tokens": 2048
}


# 4 — run and test
%run data_loader.py
cfg = load_config()
summarize(cfg)

# 5 — inspect namespace
%whos

# 6 — benchmark
%timeit load_config()

# 7 — save session
%history -f session_14jun.py

# 8 — shell check
files = !dir /b
print([f for f in files if f.endswith(".py")])
```

---

## 17. Quick Reference

| Task | Command |
|---|---|
| Create a file | `%%writefile filename` |
| Append to a file | `%%writefile -a filename` |
| Load file into buffer | `%load filename` |
| Run a script | `%run filename.py` |
| Run shell command | `!command` |
| Capture shell output | `result = !command` |
| Show variables | `%whos` |
| Time expression | `%timeit expr` |
| Profile function | `%prun func()` |
| Debug last error | `%debug` |
| Navigate directory | `%cd path` |
| Show history | `%history` |
| Save history to file | `%history -f output.py` |
| Save specific lines | `%save file.py 1-10` |
| Inspect object | `obj?` or `obj??` |
| Set env var | `%env KEY=value` |
| Reset namespace | `%reset -f` |
| Paste from clipboard | `%paste` |

---

## 18. IPython Profile — Persist Config Across Sessions

```powershell
# Run in PowerShell (outside IPython)
ipython profile create
# Creates: C:\Users\Admin\.ipython\profile_default\
```

Startup file — auto-runs on every IPython launch:
`C:\Users\Admin\.ipython\profile_default\startup\00_startup.py`

```python
import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

get_ipython().run_line_magic('alias', 'pyfiles dir *.py /b')
get_ipython().run_line_magic('pdb', 'on')

print("[startup] ready")
```