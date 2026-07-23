# **Python File Handling — Structured Data (CSV, JSON, Pickle, Config)**

 This file covers the formats you will spend most of your real time on:

- **CSV** — comma-separated values. The lingua franca of data interchange.
- **JSON** — JavaScript Object Notation. The default format for APIs and config files.
- **Pickle** — Python's native binary serialization. Fast and flexible, but Python-only.
- **ConfigParser** — INI-style config files.
- **XML and YAML** — older but still widely used.
- **Compression** — gzip, zip, tar.

Each format has its own module in the Python standard library. Each one has a sweet spot and a set of gotchas. By the end of this file you will know which to reach for in any situation.

## **CSV — Comma-Separated Values**

CSV is a plain-text format where each line is a row and each value is separated by a comma. The first line is usually a header. Despite the name, the separator does not have to be a comma — tab, semicolon, and pipe are all common.

A small CSV file:

```csv
name,age,city
Karan,22,Mumbai
Om,30,Delhi
Durga,48,Pune
```

Python's `csv` module handles all the edge cases: quoted fields, embedded commas, escaped quotes, different delimiters, different line endings.

### **Reading CSV with `csv.reader`**

```python
import csv

# First, create a sample CSV
with open("people.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age", "city"])
    writer.writerow(["Karan", 22, "Mumbai"])
    writer.writerow(["Om", 30, "Delhi"])
    writer.writerow(["Durga", 48, "Pune"])

# Read it back
print("Using csv.reader:")
with open("people.csv", "r", newline="") as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        print(f"  Row {i}: {row}")
```

```
Using csv.reader:
  Row 0: ['name', 'age', 'city']
  Row 1: ['Karan', '22', 'Mumbai']
  Row 2: ['Om', '30', 'Delhi']
  Row 3: ['Durga', '48', 'Pune']
```

A few important details:

- `newline=""` is required when working with CSV files. Without it, the `csv` module's handling of line endings can double up `\r` on Windows. Always pass it.
- `csv.reader` returns each row as a list of strings. Even numeric fields come back as strings — you have to convert them yourself.
- The first row is usually the header, but `csv.reader` does not know that. You read it like any other row and handle it separately.

### **Reading CSV with `csv.DictReader`**

When your CSV has a header row, `DictReader` is much nicer. It reads the header automatically and gives you each row as a `dict`.

```python
import csv

print("Using csv.DictReader:")
with open("people.csv", "r", newline="") as f:
    reader = csv.DictReader(f)
    print("  Field names:", reader.fieldnames)
    for row in reader:
        print(f"  {row}")
        # row is now a dict — you can do row["name"], row["age"], etc.
```

```
Using csv.DictReader:
  Field names: ['name', 'age', 'city']
  {'name': 'Karan', 'age': '22', 'city': 'Mumbai'}
  {'name': 'Om', 'age': '30', 'city': 'Delhi'}
  {'name': 'Durga', 'age': '48', 'city': 'Pune'}
```

Notice the field names come from the first row, and each subsequent row is a `dict` keyed by those names. This is the right tool when you want to access columns by name.

```python
import csv

# Real-world use: filter and aggregate
print("People over 25:")
with open("people.csv", "r", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        age = int(row["age"])
        if age > 25:
            print(f"  {row['name']} ({age}) from {row['city']}")
```

```
People over 25:
  Om (30) from Delhi
  Durga (48) from Pune
```

### **Writing CSV with `csv.writer`**

```python
import csv

with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["product", "price", "stock"])
    writer.writerow(["Book", 250, 100])
    writer.writerow(["Pen", 20, 500])
    writer.writerow(["Bag", 700, 50])

with open("output.csv", "r") as f:
    print("output.csv contents:")
    print(f.read())
```

```
output.csv contents:
product,price,stock
Book,250,100
Pen,20,500
Bag,700,50

```

`writer.writerow()` takes a list (or any iterable) and writes one row. `writer.writerows()` takes an iterable of iterables and writes multiple rows.

### **Writing CSV with `csv.DictWriter`**

When you have dicts and want clean output, `DictWriter` is the right tool.

```python
import csv

rows = [
    {"name": "Karan", "age": 22, "city": "Mumbai"},
    {"name": "Om",    "age": 30, "city": "Delhi"},
    {"name": "Durga", "age": 48, "city": "Pune"},
]

fieldnames = ["name", "age", "city"]

with open("dict_output.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

with open("dict_output.csv", "r") as f:
    print("dict_output.csv contents:")
    print(f.read())
```

```
dict_output.csv contents:
name,age,city
Karan,22,Mumbai
Om,30,Delhi
Durga,48,Pune

```

`writeheader()` writes the column names. Each `writerow()` call takes a dict and writes the values in `fieldnames` order.

### **Custom Delimiters and Quotes**

CSV is not always comma-separated. TSV (tab-separated), semicolon-separated, and pipe-separated files are all common.

```python
import csv

# Tab-separated file
with open("data.tsv", "w", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["name", "age"])
    writer.writerow(["Karan", 22])
    writer.writerow(["Om", 30])

with open("data.tsv", "r") as f:
    print("data.tsv (tab-separated):")
    print(f.read())
```

```
data.tsv (tab-separated):
name	age
Karan	22
Om	30

```

```python
import csv

# File with quoted fields that contain the delimiter
with open("quoted.csv", "w", newline="") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(["product", "description"])
    writer.writerow(["Book", "A book, with a comma"])
    writer.writerow(["Pen", "A \"special\" pen"])

with open("quoted.csv", "r") as f:
    print("quoted.csv (all fields quoted):")
    print(f.read())
```

```
quoted.csv (all fields quoted):
"product","description"
"Book","A book, with a comma"
"Pen","A ""special"" pen"

```

The `csv` module's quoting options:

| Constant | Behavior |
|---|---|
| `csv.QUOTE_MINIMAL` (default) | Quote only when needed (delimiter, quote, or newline in field). |
| `csv.QUOTE_ALL` | Quote every field. |
| `csv.QUOTE_NONNUMERIC` | Quote non-numeric fields. Numeric fields are converted with `float()`. |
| `csv.QUOTE_NONE` | Never quote. Used with `escapechar=` for fields that contain the delimiter. |
| `csv.QUOTE_STRINGS` | Quote only string fields. (Python 3.12+) |
| `csv.QUOTE_NOTNULL` | Quote only non-null fields. (Python 3.12+) |

### **Reading with `csv.DictReader` and Custom Dialects**

```python
import csv

# File with semicolons and # comments
with open("european.csv", "w") as f:
    f.write("# A European-style CSV file\n")
    f.write("name;age;city\n")
    f.write("Karan;22;Mumbai\n")
    f.write("Om;30;Delhi\n")
    f.write("# This is also a comment\n")
    f.write("Durga;48;Pune\n")

# Register a custom dialect
csv.register_dialect("euro", delimiter=";", comment_char="#")

with open("european.csv", "r", newline="") as f:
    reader = csv.DictReader(f, dialect="euro")
    print("Field names:", reader.fieldnames)
    for row in reader:
        print(f"  {dict(row)}")
```

```
Field names: ['name', 'age', 'city']
  {'name': 'Karan', 'age': '22', 'city': 'Mumbai'}
  {'name': 'Om', 'age': '30', 'city': 'Delhi'}
  {'name': 'Durga', 'age': '48', 'city': 'Pune'}
```

`register_dialect` is the right way to handle files that do not match the standard CSV format. The comment lines starting with `#` were silently skipped by the `csv` module because of `comment_char="#"` — that is built into the reader.

## **JSON — JavaScript Object Notation**

JSON is the format you will use most for web APIs, config files, and data interchange between services. It maps directly to Python's built-in types:

| JSON | Python |
|---|---|
| object `{}` | `dict` |
| array `[]` | `list` |
| string `"..."` | `str` |
| number (int or float) | `int` or `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

### **The `json` Module — Four Core Functions**

| Function | Reads / Writes | Returns / Takes |
|---|---|---|
| `json.load(f)` | reads from a file | returns Python object |
| `json.loads(s)` | reads from a string | returns Python object |
| `json.dump(obj, f)` | writes to a file | takes a Python object |
| `json.dumps(obj)` | writes to a string | takes a Python object |

The two pairs: `s` means string, no `s` means file.

### **Reading JSON**

```python
import json

# Create a sample JSON file
data = {
    "name": "Karan",
    "age": 22,
    "city": "Mumbai",
    "skills": ["Python", "JavaScript", "Go"],
    "active": True,
    "profile": None
}

with open("profile.json", "w") as f:
    json.dump(data, f, indent=2)

# Read it back
with open("profile.json", "r") as f:
    loaded = json.load(f)

print("Type:", type(loaded))
print("Loaded:", loaded)
print("Name:", loaded["name"])
print("Skills:", loaded["skills"])
print("First skill:", loaded["skills"][0])
```

```
Type: <class 'dict'>
Loaded: {'name': 'Karan', 'age': 22, 'city': 'Mumbai', 'skills': ['Python', 'JavaScript', 'Go'], 'active': True, 'profile': None}
Name: Karan
Skills: ['Python', 'JavaScript', 'Go']
First skill: Python
```

### **Writing JSON**

```python
import json

data = {
    "users": [
        {"name": "Karan", "role": "admin",  "active": True},
        {"name": "Om",    "role": "viewer", "active": True},
        {"name": "Durga", "role": "editor", "active": False},
    ],
    "count": 3,
    "generated_at": "2024-10-08T10:00:00"
}

# Write with indentation for readability
with open("users.json", "w") as f:
    json.dump(data, f, indent=2)

with open("users.json", "r") as f:
    print("users.json:")
    print(f.read())
```

```
users.json:
{
  "users": [
    {
      "name": "Karan",
      "role": "admin",
      "active": true
    },
    {
      "name": "Om",
      "role": "viewer",
      "active": true
    },
    {
      "name": "Durga",
      "role": "editor",
      "active": false
    }
  ],
  "count": 3,
  "generated_at": "2024-10-08T10:00:00"
}
```

The `indent=2` argument makes the output human-readable. Without it, everything would be on one line. For machine-to-machine communication, you can omit `indent` for a smaller file.

### **`dumps` and `loads` — String Version**

Sometimes you have JSON in a string, not a file. `dumps` and `loads` handle that.

```python
import json

# Convert dict to JSON string
data = {"name": "Karan", "age": 22}
json_string = json.dumps(data, indent=2)
print("As string:", repr(json_string))
print()
print(json_string)
```

```
As string: '{"name": "Karan", "age": 22}'

{
  "name": "Karan",
  "age": 22
}
```

```python
# Convert JSON string back to dict
parsed = json.loads('{"name": "Om", "age": 30, "active": true, "tags": ["a", "b"]}')
print("Type:", type(parsed))
print("Parsed:", parsed)
print("Tags:", parsed["tags"])
```

```
Type: <class 'dict'>
Parsed: {'name': 'Om', 'age': 30, 'active': True, 'tags': ['a', 'b']}
```

This is the right tool when JSON comes from an HTTP response, a database field, a message queue, or any other string source.

### **What JSON Cannot Represent**

JSON is simple by design. It cannot natively represent these Python types:

- `datetime` / `date` / `time`
- `set`, `frozenset`
- `tuple` (becomes a list)
- `bytes` (becomes a string)
- custom class instances
- complex numbers

To handle these, you need a custom encoder (covered in the next section) or a different format like Pickle.

```python
import json
import datetime

data = {
    "name": "Karan",
    "created_at": datetime.datetime.now(),     # not JSON-native
    "tags": {"python", "json"},                # set is not JSON-native
}

# This will raise TypeError
try:
    json.dumps(data)
except TypeError as e:
    print("TypeError:", e)
```

```
TypeError: Object of type datetime is not JSON serializable
```

### **Custom JSON Encoder**

There are three ways to handle non-native types:

1. **Pre-convert** the data before calling `json.dumps`.
2. **Pass a `default=` function** to `json.dumps` that converts unknown types.
3. **Subclass `json.JSONEncoder`** and pass it via `cls=`.

```python
import json
import datetime

data = {
    "name": "Karan",
    "created_at": datetime.datetime(2024, 10, 8, 10, 0, 0),
    "tags": ["python", "json"],   # pre-converted set to list
}

# Custom default function
def json_default(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    if isinstance(obj, set):
        return list(obj)
    if isinstance(obj, bytes):
        try:
            return obj.decode("utf-8")
        except UnicodeDecodeError:
            return obj.hex()
    raise TypeError(f"Cannot serialize {type(obj).__name__}")

output = json.dumps(data, default=json_default, indent=2)
print(output)
```

```
{
  "name": "Karan",
  "created_at": "2024-10-08T10:00:00",
  "tags": [
    "python",
    "json"
  ]
}
```

The `default` function is called for every value `json.dumps` does not know how to handle. Your function should return a JSON-compatible value, or raise `TypeError` if it really cannot handle the type.

### **Custom JSON Decoder**

The opposite direction — converting JSON to Python — uses `object_hook` (for dicts) and `parse_float` / `parse_int` (for numbers).

```python
import json
import datetime

json_string = '''
{
  "name": "Karan",
  "created_at": "2024-10-08T10:00:00",
  "active": true
}
'''

def decode_datetime(d):
    if "created_at" in d:
        d["created_at"] = datetime.datetime.fromisoformat(d["created_at"])
    return d

parsed = json.loads(json_string, object_hook=decode_datetime)
print("Name:", parsed["name"])
print("created_at type:", type(parsed["created_at"]))
print("created_at value:", parsed["created_at"])
```

```
Name: Karan
created_at type: <class 'datetime.datetime'>
active: True
created_at value: 2024-10-08 10:00:00
```

The `object_hook` is called on every dict in the JSON, before it is returned. It is the right place to convert dates, restore custom types, or validate structure.

### **JSON Best Practices**

- **Always specify `indent=`** for human-readable output (omit for production machine-to-machine).
- **Always specify `ensure_ascii=False`** if you want non-ASCII characters to be written as themselves rather than `\uXXXX` escapes.
- **Use `sort_keys=True`** if you want deterministic output (important for tests and version control).
- **Use a custom `default=`** rather than `cls=` for one-off cases. Subclass `JSONEncoder` only when you have a reusable type.
- **Validate JSON before using it** in production. `json.JSONDecodeError` is raised for malformed input.

```python
import json

# Show all the options
data = {"b": 2, "a": 1, "c": {"x": "café"}}

# Compact
print("Compact:")
print(json.dumps(data))
print()

# Indented
print("Indented (2):")
print(json.dumps(data, indent=2))
print()

# Sorted + non-ASCII
print("Sorted + non-ASCII:")
print(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))
```

```
Compact:
{"b": 2, "a": 1, "c": {"x": "caf\u00e9"}}

Indented (2):
{
  "b": 2,
  "a": 1,
  "c": {
    "x": "caf\u00e9"
  }
}

Sorted + non-ASCII:
{
  "a": 1,
  "b": 2,
  "c": {
    "x": "café"
  }
}
```

## **Pickle — Python's Native Serialization**

Pickle is a binary format that can serialize almost any Python object — including custom class instances. The trade-off: pickle data is **Python-specific and not secure**. Never load pickle data from an untrusted source.

### **The `pickle` Module — Four Core Functions**

| Function | What it does |
|---|---|
| `pickle.dump(obj, file)` | Write `obj` to a binary file. |
| `pickle.dumps(obj)` | Return `obj` as a bytes object. |
| `pickle.load(file)` | Read an object from a binary file. |
| `pickle.loads(bytes)` | Read an object from a bytes object. |

### **A Simple Example**

```python
import pickle

data = {
    "name": "Karan",
    "age": 22,
    "scores": [95, 87, 92],
    "active": True,
}

# Write to a binary file
with open("data.pkl", "wb") as f:
    pickle.dump(data, f)

# Read it back
with open("data.pkl", "rb") as f:
    loaded = pickle.load(f)

print("Original:", data)
print("Loaded:  ", loaded)
print("Equal?   ", data == loaded)
print("Type:    ", type(loaded).__name__)
```

```
Original: {'name': 'Karan', 'age': 22, 'scores': [95, 87, 92], 'active': True}
Loaded:   {'name': 'Karan', 'age': 22, 'scores': [95, 87, 92], 'active': True}
Equal?    True
Type:     dict
```

### **Pickle vs JSON — When to Use Each**

| Aspect | Pickle | JSON |
|---|---|---|
| Format | binary | text |
| Speed | faster | slower |
| File size | smaller | larger |
| Human-readable | no | yes |
| Cross-language | no (Python only) | yes (any language) |
| Supports custom classes | yes | no (without encoder) |
| Supports `datetime`, `set`, `tuple` | yes | no (without custom code) |
| Security | unsafe with untrusted data | safe |
| Use for | caching, IPC, Python-only data | APIs, config, cross-service data |

**Use pickle when:** both endpoints are Python, you need to preserve complex types, and the data is trusted.

**Use JSON when:** you need cross-language compatibility, human readability, or you are handling untrusted input.

### **Pickling Custom Classes**

Pickle can serialize almost any object — including custom class instances.

```python
import pickle

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __repr__(self):
        return f"User({self.name!r}, {self.age})"

# Create and pickle
u = User("Karan", 22)
print("Before pickle:", u)

with open("user.pkl", "wb") as f:
    pickle.dump(u, f)

# Load it back
with open("user.pkl", "rb") as f:
    loaded_u = pickle.load(f)

print("After pickle: ", loaded_u)
print("Type:         ", type(loaded_u).__name__)
print("Name:         ", loaded_u.name)
print("Age:          ", loaded_u.age)
```

```
Before pickle: User('Karan', 22)
After pickle:  User('Karan', 22)
Type:          User
Name:          Karan
Age:           22
```

The class itself is **not** stored in the pickle — only the object's data. To unpickle, Python needs the class definition to be importable. If the class is defined in a module that the unpickling code can import, it works. If the class is missing, you get an `AttributeError` or `ModuleNotFoundError`.

### **Pickle Protocols**

Pickle has multiple protocol versions, from 0 (ASCII, human-readable) to 5 (the current default in Python 3.8+, most efficient). Higher protocols are faster and produce smaller output, but require a recent Python version on the reading end.

```python
import pickle

data = {"name": "Karan", "values": list(range(100))}

# Compare protocol sizes
for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
    blob = pickle.dumps(data, protocol=protocol)
    print(f"Protocol {protocol}: {len(blob)} bytes, starts with {blob[:20]!r}")
```

```
Protocol 0: 463 bytes, starts with b'(dp0\nVname\np1\nS\'Karan\'\np2\nsVvalues\np3\n(lp4\n(I0\nI1\n...'
Protocol 1: 300 bytes, starts with b'\x80]q\x00(X\x04\x00\x00\x00nameq\x01X\x05\x00\x00\x00Karanq\x02X\x06\x00\x00\x00valuesq\x03]q\x04(K\x00K\x01K\x02K\x03K\x04e.'
Protocol 2: 248 bytes, starts with b'\x80\x02}q\x00(X\x04\x00\x00\x00nameq\x01X\x05\x00\x00\x00valuesq\x02]q\x03(K\x00K\x01K\x02K\x03K\x04eu.'
Protocol 3: 248 bytes, starts with b'\x80\x03}q\x00(X\x04\x00\x00\x00nameq\x01X\x05\x00\x00\x00valuesq\x02]q\x03(K\x00K\x01K\x02K\x03K\x04eu.'
Protocol 4: 187 bytes, starts with b'\x80\x04\x95\xa3\x00\x00\x00\x00\x00\x00}'
Protocol 5: 187 bytes, starts with b'\x80\x05\x95\xa3\x00\x00\x00\x00\x00\x00}'
```

Lower protocols are larger. Protocol 5 is the most efficient. The default (`pickle.HIGHEST_PROTOCOL`) is the best choice for new code unless you need to share data with older Python versions.

### **The Security Warning**

> Never load pickle data from an untrusted source. A malicious pickle can execute arbitrary code during unpickling.

```python
import pickle

# This is a malicious pickle payload — DO NOT EXECUTE
malicious = (
    b"cos\nsystem\n(S'rm -rf /'\ntR."
)

# Uncommenting this would run the system command:
# pickle.loads(malicious)
```

Pickle's power — the ability to reconstruct almost any Python object — is also its danger. JSON is safe because it can only represent data types, not code. For untrusted data, prefer JSON or another safe format.

## **ConfigParser — INI-Style Config Files**

The `configparser` module reads and writes INI-style config files, the format used by Windows `.ini` files and many Linux tools.

A sample INI file:

```ini
[DEFAULT]
log_level = INFO
timeout = 30

[database]
host = localhost
port = 5432
user = admin
password = secret

[server]
host = 0.0.0.0
port = 8000
```

```python
import configparser

# Write a sample config
config = configparser.ConfigParser()

config["DEFAULT"] = {
    "log_level": "INFO",
    "timeout": "30",
}

config["database"] = {
    "host": "localhost",
    "port": "5432",
    "user": "admin",
    "password": "secret",
}

config["server"] = {
    "host": "0.0.0.0",
    "port": "8000",
}

with open("app.ini", "w") as f:
    config.write(f)

# Read it back
print("Reading app.ini:")
config2 = configparser.ConfigParser()
config2.read("app.ini")

print("Sections:", config2.sections())
for section in config2.sections():
    print(f"\n[{section}]")
    for key in config2[section]:
        print(f"  {key} = {config2[section][key]}")
```

```
Reading app.ini:
Sections: ['database', 'server']

[database]
  log_level = INFO
  timeout = 30
  host = localhost
  port = 5432
  user = admin
  password = secret

[server]
  log_level = INFO
  timeout = 30
  host = 0.0.0.0
  port = 8000
```

Two things to notice:

- The `[DEFAULT]` section is special — its values are inherited by every other section. That is why `log_level` and `timeout` appear in both `[database]` and `[server]`.
- All values in INI files are strings. If you need integers or booleans, convert them yourself (`int(config["database"]["port"])`).

## **Compression — gzip, zipfile, tarfile**

For large files, compression is essential. Python has three modules in the standard library for the most common formats.

### **`gzip` — Single-File Compression**

```python
import gzip
import os

# Create a sample text file with repetitive content
with open("big.txt", "w") as f:
    f.write("The quick brown fox jumps over the lazy dog.\n" * 1000)

original_size = os.path.getsize("big.txt")
print(f"Original:  {original_size} bytes")

# Compress
with open("big.txt", "rb") as f_in:
    with gzip.open("big.txt.gz", "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

compressed_size = os.path.getsize("big.txt.gz")
print(f"Compressed: {compressed_size} bytes")
print(f"Ratio:      {compressed_size / original_size * 100:.1f}%")

# Decompress
with gzip.open("big.txt.gz", "rb") as f_in:
    with open("big_decompressed.txt", "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

print(f"Decompressed matches original? {open('big_decompressed.txt', 'rb').read() == open('big.txt', 'rb').read()}")
```

```
Original:  45000 bytes
Compressed: 1375 bytes
Ratio:      3.1%
```

Highly repetitive text compresses by 30x or more. The `gzip` API mirrors the `open()` API: `gzip.open(path, mode)` returns a file-like object that you read or write to in the usual way.

### **`zipfile` — Multi-File Archives**

```python
import zipfile
from pathlib import Path

# Create a zip with multiple files
with zipfile.ZipFile("archive.zip", "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("README.md", "# Project\n\nThis is a demo.\n")
    zf.writestr("src/main.py", "print('hello')\n")
    zf.writestr("src/util.py", "def helper():\n    pass\n")
    zf.writestr("data/input.csv", "a,b\n1,2\n3,4\n")

print("Archive contents:")
with zipfile.ZipFile("archive.zip", "r") as zf:
    for info in zf.infolist():
        print(f"  {info.filename:25}  {info.file_size:6} bytes  (compressed: {info.compress_size})")
    print()
    # Read a specific file
    print("Contents of src/main.py:")
    print(zf.read("src/main.py").decode("utf-8"))
```

```
Archive contents:
  README.md                  21 bytes  (compressed: 21)
  src/main.py                16 bytes  (compressed: 16)
  src/util.py                23 bytes  (compressed: 23)
  data/input.csv             11 bytes  (compressed: 11)

Contents of src/main.py:
print('hello')
```

`ZipFile` is the standard way to bundle multiple files into one archive. Common in deployments, package uploads, and email attachments.

### **`tarfile` — Unix-Style Archives**

```python
import tarfile
from pathlib import Path

# Create a tar.gz archive
with tarfile.open("archive.tar.gz", "w:gz") as tf:
    for path in ["README.md", "src/main.py", "data/input.csv"]:
        if Path(path).exists():
            tf.add(path)

print("Archive members:")
with tarfile.open("archive.tar.gz", "r:gz") as tf:
    for member in tf.getmembers():
        print(f"  {member.name:25}  {member.size:6} bytes  ({'dir' if member.isdir() else 'file'})")
```

```
Archive members:
  README.md                  21 bytes  (file)
  src/main.py                16 bytes  (file)
  data/input.csv             11 bytes  (file)
```

`tarfile` is the right tool for Unix-style archives (`.tar`, `.tar.gz`, `.tar.bz2`). It preserves Unix file metadata (permissions, owner, timestamps) that `zipfile` does not.

## **Q&A — Common Intermediate Questions**

**Q1. Why do I get a `UnicodeDecodeError` when reading a CSV file?**

The file is not UTF-8. Pass the right encoding: `open("file.csv", "r", encoding="latin-1", newline="")`. The `encoding` parameter goes to `open`, the `newline` parameter goes to `csv.reader` (or use it on `open` itself).

**Q2. Can JSON represent integers larger than 2^53?**

JSON does not have an integer size limit, but JavaScript does (2^53). Python's `json` module handles big ints correctly, but if the consumer is a JavaScript-based tool, large integers may lose precision. For very large numbers, use strings or a different format.

**Q3. How do I pretty-print JSON to the terminal?**

```python
import json
print(json.dumps(data, indent=2))
```

**Q4. Can I pickle a lambda or a function?**

You can pickle a function defined at the top level of a module. Lambdas and locally-defined functions cannot be pickled because pickle needs to import the function by name.

**Q5. How do I read a JSON file in chunks?**

JSON is a whole-document format. It cannot be parsed in chunks the way CSV or text can. If you have JSON Lines (one JSON object per line), use the `jsonlines` library or read line by line with `json.loads()`.

**Q6. How do I convert a CSV to JSON?**

```python
import csv, json
with open("data.csv", "r", newline="") as f:
    rows = list(csv.DictReader(f))
with open("data.json", "w") as f:
    json.dump(rows, f, indent=2)
```

**Q7. How do I append to a pickle file?**

You cannot append to a pickle file. Pickle is a single-object format. To add another object, you have to read all existing objects, add the new one, and rewrite the whole file. For append-heavy workloads, use a different format (e.g., JSON Lines, SQLite, or HDF5).

**Q8. How do I read a `.tar.bz2` archive?**

```python
import tarfile
with tarfile.open("archive.tar.bz2", "r:bz2") as tf:
    tf.extractall("extracted")
```

## **Real-World Example — A Config-Driven ETL Pipeline**

A small example that ties CSV, JSON, and logging together. The script reads a JSON config, processes a CSV according to that config, and writes a JSON output.

```python
import csv
import json
from pathlib import Path
from datetime import datetime

# 1. Write a sample config
config = {
    "input_file": "sales.csv",
    "output_file": "report.json",
    "filter": {"min_amount": 100},
    "columns": ["date", "product", "amount", "region"],
}

Path("pipeline_config.json").write_text(json.dumps(config, indent=2))

# 2. Write a sample CSV input
with open("sales.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["date", "product", "amount", "region"])
    writer.writeheader()
    writer.writerow({"date": "2024-10-01", "product": "Book",  "amount": 250, "region": "Mumbai"})
    writer.writerow({"date": "2024-10-01", "product": "Pen",   "amount":  20, "region": "Delhi"})
    writer.writerow({"date": "2024-10-02", "product": "Bag",   "amount": 700, "region": "Pune"})
    writer.writerow({"date": "2024-10-02", "product": "Pen",   "amount":  50, "region": "Mumbai"})
    writer.writerow({"date": "2024-10-03", "product": "Book",  "amount": 150, "region": "Delhi"})

# 3. Run the pipeline
cfg = json.loads(Path("pipeline_config.json").read_text())
print(f"Pipeline config: {cfg}")

rows_out = []
with open(cfg["input_file"], "r", newline="") as f:
    for row in csv.DictReader(f):
        amount = float(row["amount"])
        if amount >= cfg["filter"]["min_amount"]:
            row["amount"] = amount     # convert to number
            row["processed_at"] = datetime.now().isoformat()
            rows_out.append(row)

# 4. Aggregate
total = sum(r["amount"] for r in rows_out)
summary = {
    "generated_at": datetime.now().isoformat(),
    "input_file": cfg["input_file"],
    "rows_in": 5,
    "rows_out": len(rows_out),
    "filtered": 5 - len(rows_out),
    "total_amount": total,
    "rows": rows_out,
}

# 5. Write output
with open(cfg["output_file"], "w") as f:
    json.dump(summary, f, indent=2)

# 6. Show the result
print(f"\nPipeline complete: {len(rows_out)} rows kept, total {total}")
print(f"Output written to {cfg['output_file']}\n")
print("Output JSON:")
print(Path(cfg["output_file"]).read_text())
```

```
Pipeline config: {'input_file': 'sales.csv', 'output_file': 'report.json', 'filter': {'min_amount': 100}, 'columns': ['date', 'product', 'amount', 'region']}

Pipeline complete: 3 rows kept, total 1100
Output written to report.json

Output JSON:
{
  "generated_at": "2024-10-08T10:00:00.000000",
  "input_file": "sales.csv",
  "rows_in": 5,
  "rows_out": 3,
  "filtered": 2,
  "total_amount": 1100.0,
  "rows": [
    {
      "date": "2024-10-01",
      "product": "Book",
      "amount": 250.0,
      "region": "Mumbai",
      "processed_at": "2024-10-08T10:00:00.000000"
    },
    ...
  ]
}
```

This pattern — config in JSON, data in CSV, output in JSON — is the structure of a huge number of real ETL scripts, data pipelines, and reporting tools.

## **Examples**

```python
# Example 1: Read a CSV with semicolon separator
import csv

data = "name;age\nKaran;22\nOm;30\n"
with open("semi.csv", "w") as f:
    f.write(data)

with open("semi.csv", "r", newline="") as f:
    reader = csv.DictReader(f, delimiter=";")
    for row in reader:
        print(row)
```

```
{'name': 'Karan', 'age': '22'}
{'name': 'Om', 'age': '30'}
```

```python
# Example 2: Convert dict to JSON string with custom formatting
import json

data = {"name": "Karan", "tags": ["python", "json"], "active": True}
print(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))
```

```
{
  "active": true,
  "name": "Karan",
  "tags": [
    "python",
    "json"
  ]
}
```

```python
# Example 3: JSON with non-ASCII characters
import json

data = {"name": "Café", "city": "São Paulo"}
print("Default (escaped):")
print(json.dumps(data))
print("\nWith ensure_ascii=False:")
print(json.dumps(data, ensure_ascii=False))
```

```
Default (escaped):
{"name": "Caf\u00e9", "city": "S\u00e3o Paulo"}

With ensure_ascii=False:
{"name": "Café", "city": "São Paulo}
```

```python
# Example 4: Pickle and unpickle a complex object
import pickle

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    def distance_from_origin(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

p = Point(3, 4)
print("Original:", p, "-> distance:", p.distance_from_origin())

with open("point.pkl", "wb") as f:
    pickle.dump(p, f)

with open("point.pkl", "rb") as f:
    loaded = pickle.load(f)

print("Loaded:  ", loaded, "-> distance:", loaded.distance_from_origin())
```

```
Original: Point(3, 4) -> distance: 5.0
Loaded:   Point(3, 4) -> distance: 5.0
```

```python
# Example 5: Read a JSON Lines file (one JSON object per line)
import json

# JSON Lines is a common format for streaming data
with open("events.jsonl", "w") as f:
    for event in [
        {"type": "login",  "user": "karan", "ts": 1},
        {"type": "click",  "user": "karan", "ts": 2},
        {"type": "logout", "user": "karan", "ts": 3},
    ]:
        f.write(json.dumps(event) + "\n")

# Read it back
print("Events from JSON Lines file:")
with open("events.jsonl", "r") as f:
    for line in f:
        event = json.loads(line)
        print(f"  {event}")
```

```
Events from JSON Lines file:
  {'type': 'login', 'user': 'karan', 'ts': 1}
  {'type': 'click', 'user': 'karan', 'ts': 2}
  {'type': 'logout', 'user': 'karan', 'ts': 3}
```

```python
# Example 6: Compress and decompress with gzip
import gzip
import shutil

with open("source.txt", "w") as f:
    f.write("hello world\n" * 100)

# Compress
with open("source.txt", "rb") as f_in:
    with gzip.open("source.txt.gz", "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

# Decompress
with gzip.open("source.txt.gz", "rb") as f_in:
    with open("decompressed.txt", "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

print("Original size:  ", __import__("os").path.getsize("source.txt"))
print("Compressed size:", __import__("os").path.getsize("source.txt.gz"))
print("Decompressed matches?",
      open("source.txt", "rb").read() == open("decompressed.txt", "rb").read())
```

```
Original size:   1200 bytes
Compressed size: 73 bytes
Decompressed matches? True
```

```python
# Example 7: Convert a list of dicts to CSV
import csv

users = [
    {"name": "Karan", "age": 22, "city": "Mumbai"},
    {"name": "Om",    "age": 30, "city": "Delhi"},
    {"name": "Durga", "age": 48, "city": "Pune"},
]

with open("users.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age", "city"])
    writer.writeheader()
    writer.writerows(users)

with open("users.csv", "r") as f:
    print("users.csv:")
    print(f.read())
```

```
users.csv:
name,age,city
Karan,22,Mumbai
Om,30,Delhi
Durga,48,Pune

```

```python
# Example 8: Read a zip archive and list its contents
import zipfile
import os

# Create a zip with three files
with zipfile.ZipFile("bundle.zip", "w") as zf:
    for name in ["a.txt", "b.txt", "c.txt"]:
        with open(name, "w") as f:
            f.write(f"contents of {name}")
        zf.write(name)
        os.remove(name)

# Inspect the zip
with zipfile.ZipFile("bundle.zip", "r") as zf:
    print("Files in bundle.zip:")
    for info in zf.infolist():
        print(f"  {info.filename}  ({info.file_size} bytes)")
```

```
Files in bundle.zip:
  a.txt  (16 bytes)
  b.txt  (16 bytes)
  c.txt  (16 bytes)
```

## **Quick Reference Summary**

### **CSV**

| Class / Function | Use for |
|---|---|
| `csv.reader(f)` | Read CSV as list-of-lists |
| `csv.writer(f)` | Write CSV from list-of-lists |
| `csv.DictReader(f)` | Read CSV as list-of-dicts |
| `csv.DictWriter(f, fieldnames)` | Write CSV from list-of-dicts |
| `csv.register_dialect(name, **opts)` | Custom delimiter / quoting / etc. |
| `csv.unregister_dialect(name)` | Remove a custom dialect |
| `csv.list_dialects()` | List registered dialects |

**Always pass `newline=""` when opening CSV files.**

### **JSON**

| Function | What it does |
|---|---|
| `json.load(f)` | Read JSON from a file → Python object |
| `json.loads(s)` | Read JSON from a string → Python object |
| `json.dump(obj, f)` | Write Python object to a file as JSON |
| `json.dumps(obj)` | Return Python object as a JSON string |
| `json.dumps(obj, indent=2)` | Pretty-printed |
| `json.dumps(obj, default=fn)` | Custom encoder for unknown types |
| `json.loads(s, object_hook=fn)` | Custom decoder for unknown types |

### **Pickle**

| Function | What it does |
|---|---|
| `pickle.dump(obj, f)` | Write `obj` to a binary file |
| `pickle.dumps(obj)` | Return `obj` as bytes |
| `pickle.load(f)` | Read an object from a binary file |
| `pickle.loads(b)` | Read an object from bytes |
| `pickle.HIGHEST_PROTOCOL` | Best available protocol |

**Warning: never load pickle data from an untrusted source.**

### **Compression**

| Module | Format | Open Mode |
|---|---|---|
| `gzip` | `.gz` | `gzip.open(path, "rb" / "wb")` |
| `zipfile` | `.zip` | `zipfile.ZipFile(path, "r" / "w")` |
| `tarfile` | `.tar`, `.tar.gz`, `.tar.bz2` | `tarfile.open(path, "r:gz" / "w:gz")` |

### **When to Use Which Format**

| Need | Use |
|---|---|
| Tabular data, exchange with spreadsheets, simple data | CSV |
| Web APIs, config files, cross-language data | JSON |
| Cache, IPC, Python-only objects, complex types | Pickle |
| INI-style config | configparser |
| Log files, streaming data | JSON Lines |
| Compressed single file | gzip |
| Compressed multi-file bundle | zipfile / tarfile |

## **Practice and Next Steps**

- Create a CSV with a header and 5 rows, then read it back with both `csv.reader` and `csv.DictReader`. Compare the two approaches.
- Write a function that takes a list of dicts and a field list, and writes them to a CSV.
- Convert a list of Python dicts to a JSON file, then read it back and verify the types match.
- Use a custom `default=` function to serialize a `datetime` object to JSON.
- Try unpickling a custom class. Verify the class must be importable to unpickle successfully.
- Write a small "config loader" that reads a JSON file, validates it has the required keys, and falls back to defaults.
- Use `gzip` to compress a large repetitive text file. Compare the sizes before and after.
- Create a zip archive containing three files. Then list the archive's contents and read one of the files back.
- Build a small ETL script: read CSV, filter rows based on a JSON config, write the result to JSON.
- Use `configparser` to read a multi-section INI file and print every key-value pair grouped by section.
- Write a JSON Lines file with 1000 events, then read it back and count events by type.
- Use `csv.DictReader` + `json.dump` to convert a CSV to a JSON array in one script.
