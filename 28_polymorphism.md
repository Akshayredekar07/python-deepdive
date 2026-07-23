# **Polymorphism and Operator Overloading**

## **What is Polymorphism**

The word *polymorphism* means "many forms". In Python OOP, polymorphism is the ability of the same operator, method, or function to behave differently based on the type of objects it is acting on.

A real-life example: the word **Friendship**. A boy starts love with the word *Friendship*, a girl ends love with the same word *Friendship*. The word is the same, but the meaning is different. The same word, different purpose — that is polymorphism.

Another real-life example: a mother calls her son and says "Please bring Red Label." She might be asking for weight (kgs) or for bottles. Same request, different interpretations depending on context.

In Python, polymorphism shows up in three main places:

- **Operator overloading** — the same operator (`+`, `*`, `<`, `>`, etc.) does different things for different types.
- **Method overloading** — the same method name handles different argument patterns.
- **Method overriding** — a child class provides its own version of a parent method (covered in the inheritance file).

## **Python vs Java — Feature Comparison**

Before diving into operator overloading, here is a quick comparison of what Python and Java support out of the box.

| Feature | Java | Python |
|---|---|---|
| Operator Overloading | Not Possible | Possible |
| Method Overloading | Possible | Not Possible |
| Constructor Overloading | Possible | Not Possible |
| Method Overriding | Possible | Possible |
| Constructor Overriding | Not Possible | Possible |

This table is the reason Python developers think differently about polymorphism. Python does not do method or constructor overloading in the Java sense. Instead, it uses **default arguments**, **`*args`**, and **`**kwargs`** to simulate the same flexibility. Where Python shines is **operator overloading** — Java simply does not allow it for custom classes.

## **Operator Overloading**

Python provides built-in support for overloading operators. Java does not. The way Python does it is via special methods (also called **magic methods** or **dunder methods**) that begin and end with double underscores. For every operator, there is a corresponding magic method. If you want to support that operator on your custom objects, you override the magic method in your class.

A few common ones:

- `+` is overloaded via `__add__(self, other)`
- `-` via `__sub__(self, other)`
- `*` via `__mul__(self, other)`
- `<` via `__lt__(self, other)`
- `>` via `__gt__(self, other)`
- `<=` via `__le__(self, other)`
- `>=` via `__ge__(self, other)`
- `==` via `__eq__(self, other)`
- `print(obj)` uses `__str__(self)`
- `len(obj)` uses `__len__(self)`

### **Overloading `<` and `>` Operators**

If you want `<` and `>` to work on your custom objects, you only need to override one of `__lt__` or `__gt__`. Python will derive the other one from it (it will simply reverse the result).

```python
class Student:
    def __init__(self, name, marks) -> None:
        self.name = name
        self.marks = marks

    def __lt__(self, other):
        result = self.marks < other.marks
        return result


s1 = Student("Durga", 78)
s2 = Student("Ravi", 87)
# Base on marks
print(s1 < s2)   # 78 < 87
print(s2 < s1)   # 87 < 78
print(s2 > s1)   # 87 > 78
```

```
True
False
True
```

Notice the rule: **to provide support for `<` and `>`, override either `__lt__` or `__gt__`**. Overriding just `__lt__` makes both `<` and `>` work because `>` is the reverse of `<`.

A common real-world need is to compare by marks, and if marks are equal, fall back to comparing by name:

```python
class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def __lt__(self, other):
        if self.marks == other.marks:
            result = self.name < other.name
        else:
            result = self.marks < other.marks
        return result

s1 = Student('Durga', 100)
s2 = Student('Apple', 200)
s3 = Student('Ravi', 100)

print(s1 < s2)   # True — 100 < 200
print(s1 < s3)   # True — same marks, "Durga" < "Ravi"
```

```
True
True
```

**More Examples — `__lt__` / `__gt__` in Real Development**

job scheduling with a min-heap. `heapq` compares items with `<`, so overloading `__lt__` lets you push custom objects straight into a heap ordered by priority.

```python
import heapq

class Job:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __repr__(self):
        return f"Job({self.name}, p={self.priority})"

jobs = [Job("backup", 3), Job("deploy", 1), Job("cleanup", 5)]
heapq.heapify(jobs)
while jobs:
    print(heapq.heappop(jobs))
```

```
Job(deploy, p=1)
Job(backup, p=3)
Job(cleanup, p=5)
```

FastAPI: sorting API response objects by latency so the fastest endpoint check shows first in a health-check report.

```python
class EndpointHealth:
    def __init__(self, path, latency_ms):
        self.path = path
        self.latency_ms = latency_ms

    def __lt__(self, other):
        return self.latency_ms < other.latency_ms

    def __repr__(self):
        return f"{self.path} -> {self.latency_ms}ms"

checks = [
    EndpointHealth("/users", 220),
    EndpointHealth("/orders", 45),
    EndpointHealth("/health", 5),
]
print(sorted(checks))
```

```
[/health -> 5ms, /orders -> 45ms, /users -> 220ms]
```

comparing cloud instance options by hourly cost so you can pick the cheapest instance type that meets a minimum vCPU requirement.

```python
class CloudInstance:
    def __init__(self, instance_type, vcpus, cost_per_hour):
        self.instance_type = instance_type
        self.vcpus = vcpus
        self.cost_per_hour = cost_per_hour

    def __lt__(self, other):
        return self.cost_per_hour < other.cost_per_hour

    def __repr__(self):
        return f"{self.instance_type} (${self.cost_per_hour}/hr)"

instances = [
    CloudInstance("m5.large", 2, 0.096),
    CloudInstance("t3.micro", 2, 0.0104),
    CloudInstance("c5.xlarge", 4, 0.17),
]
cheapest = min(instances)
print(cheapest)
print(sorted(instances))
```

```
t3.micro ($0.0104/hr)
[t3.micro ($0.0104/hr), m5.large ($0.096/hr), c5.xlarge ($0.17/hr)]
```

### **Overloading `<=` and `>=` Operators**

To make `<=` and `>=` work, override either `__le__` or `__ge__`.

```python
class Student:
    def __init__(self, name, marks) -> None:
        self.name = name
        self.marks = marks

    def __le__(self, other):
        result = self.marks < other.marks
        return result


s1 = Student("Durga", 100)
s2 = Student("Ravi", 200)
s3 = Student("Shiva", 100)

print(s1 <= s2)    # 100 < 200 -> True
print(s1 <= s3)    # 100 < 100 -> False
print(s1 >= s3)    # reverse of above -> False
print(s1 >= s2)    # reverse of s1<=s2 -> False
print(s1 <= s3)
```

```
True
False
False
False
False
```

**More Examples — `__le__` / `__ge__` in Real Development**

comparing two schema/migration versions to decide whether a migration has already been applied.

```python
class MigrationVersion:
    def __init__(self, version):
        self.version = version   # e.g. 12

    def __le__(self, other):
        return self.version <= other.version

    def __repr__(self):
        return f"v{self.version}"

current_db_version = MigrationVersion(12)
required_version = MigrationVersion(15)

if current_db_version <= required_version:
    print(f"Need to run migrations up to {required_version}")
```

```
Need to run migrations up to v15
```

checking whether a packet's size is within (or exceeds) the network's MTU (Maximum Transmission Unit) before sending.

```python
class Packet:
    def __init__(self, size_bytes):
        self.size_bytes = size_bytes

    def __le__(self, other):
        return self.size_bytes <= other.size_bytes

    def __repr__(self):
        return f"Packet({self.size_bytes}B)"

MTU = Packet(1500)
outgoing = Packet(1400)

print(outgoing <= MTU)   # fits without fragmentation
print(Packet(2000) <= MTU)
```

```
True
False
```

checking if current resource utilization is at or above an auto-scaling threshold.

```python
class ResourceUsage:
    def __init__(self, cpu_percent):
        self.cpu_percent = cpu_percent

    def __ge__(self, other):
        return self.cpu_percent >= other.cpu_percent

    def __repr__(self):
        return f"{self.cpu_percent}% CPU"

current = ResourceUsage(82)
scale_out_threshold = ResourceUsage(80)

if current >= scale_out_threshold:
    print("Trigger auto-scaling: add another instance")
```

```
Trigger auto-scaling: add another instance
```

### **Overriding Just `__gt__`**

You can override `__gt__` directly. Then `<` is automatically derived as the reverse.

```python
class Student:
    def __init__(self, name, mark):
        self.name = name
        self.mark = mark

    def __gt__(self, other):
        res = self.mark > other.mark
        return res

s1 = Student('Ak', 99)
s2 = Student('Sej', 98)
print(s1 > s2)
print(s1 < s2)
```

```
True
False
```

**More Examples — `__gt__` in Real Development**

OS: comparing process priority so a scheduler can pick which process runs next (lower `nice` value usually means higher priority, but here we model higher-number-wins for simplicity).

```python
class Process:
    def __init__(self, pid, priority):
        self.pid = pid
        self.priority = priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __repr__(self):
        return f"PID {self.pid} (priority {self.priority})"

p1 = Process(101, 5)
p2 = Process(102, 9)
next_to_run = p1 if p1 > p2 else p2
print(next_to_run)
```

```
PID 102 (priority 9)
```

comparing two `TreeNode` values while building or balancing a binary search tree.

```python
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __gt__(self, other):
        return self.value > other.value

def insert(root, node):
    if node > root:
        if root.right is None:
            root.right = node
        else:
            insert(root.right, node)
    else:
        if root.left is None:
            root.left = node
        else:
            insert(root.left, node)

root = TreeNode(50)
insert(root, TreeNode(70))
insert(root, TreeNode(30))
print(root.right.value, root.left.value)
```

```
70 30
```

### **Overloading `*` Operator**

The `*` operator is overloaded through `__mul__`. Here is a classic payroll example: an `Employee` has a per-day salary, a `TimeSheet` records how many days were worked, and `employee * timesheet` returns the total salary.

```python
class Employee:
    def __init__(self, name, salaryperday):
        self.name = name
        self.salaryperday = salaryperday

    def __mul__(self, other):
        money = self.salaryperday * other.workingDay
        return money

    def __str__(self):
        return 'name {}, salaryperday {} '.format(self.name, self.salaryperday)


class TimeSheet:
    def __init__(self, name, workingDay):
        self.name = name
        self.workingDay = workingDay

e = Employee('Akshay', 1000000)
t = TimeSheet('Akshay', 20)
print(e * t)
print(e)
```

```
20000000
name Akshay, salaryperday 1000000 
```

A very common question: **how does the operator know which class's `__mul__` to call?** The rule is simple — the magic method of the **left operand's class** is called first. So `e * t` calls `Employee.__mul__`, with `self = e` and `other = t`. Inside `__mul__`, we read `other.workingDay`, which is why the `TimeSheet` object is passed as `other`.

What if you write `t * e` instead? Then `self = t` and `other = e`, but `TimeSheet` does not define `__mul__`, so Python raises:

```
TypeError: unsupported operand type(s) for *: 'TimeSheet' and 'Employee'
```

To support `t * e`, you would need to define `__mul__` inside `TimeSheet` and read `other.salaryperday` there. This is a useful trick: **you can define the same magic method in both classes** to support the operator in both directions.

```python
class TimeSheet:
    def __init__(self, name, workingDay):
        self.name = name
        self.workingDay = workingDay

    def __mul__(self, other):
        # self = t, other = e
        return self.workingDay * other.salaryperday
```

Now both `e * t` and `t * e` work.

**More Examples — `__mul__` in Real Development**

computing a cloud bill by multiplying a resource's hourly rate by the number of hours it ran — the same pattern as the `Employee * TimeSheet` example, just for infra billing.

```python
class CloudResource:
    def __init__(self, name, rate_per_hour):
        self.name = name
        self.rate_per_hour = rate_per_hour

    def __mul__(self, other):
        return self.rate_per_hour * other.hours_running

    def __str__(self):
        return f"{self.name} @ ${self.rate_per_hour}/hr"


class UsageWindow:
    def __init__(self, hours_running):
        self.hours_running = hours_running

vm = CloudResource("ec2-web-01", 0.096)
usage = UsageWindow(730)   # roughly a month
print(f"Bill: ${vm * usage:.2f}")
```

```
Bill: $70.08
```

computing total data transferred by multiplying bandwidth (Mbps) by duration (seconds).

```python
class Bandwidth:
    def __init__(self, mbps):
        self.mbps = mbps

    def __mul__(self, other):
        return self.mbps * other.seconds  # megabits transferred

    def __str__(self):
        return f"{self.mbps} Mbps"


class Duration:
    def __init__(self, seconds):
        self.seconds = seconds

link = Bandwidth(100)
window = Duration(60)
print(f"Total transferred: {link * window} megabits")
```

```
Total transferred: 6000 megabits
```

scaling a `Matrix`-like row-vector by a scalar, a common building block in numerical/DSA problems before reaching for NumPy.

```python
class Vector:
    def __init__(self, values):
        self.values = values

    def __mul__(self, scalar):
        return Vector([v * scalar for v in self.values])

    def __repr__(self):
        return f"Vector({self.values})"

v = Vector([1, 2, 3])
print(v * 3)
```

```
Vector([3, 6, 9])
```

### **Overloading `+` Operator**

The `+` operator is overloaded through `__add__`. The classic example: two `Book` objects — adding them gives the total number of pages.

```python
class Book:
    def __init__(self, page) -> None:
        self.page = page

    def __add__(self, other):
        total_pages = self.page + other.page
        return total_pages

b1 = Book(100)
b2 = Book(200)
b3 = Book(600)
b4 = Book(100)

print(b1 + b2)
# print(b1 + b2 + b3)   # TypeError: unsupported operand type(s) for +: 'int' and 'Book'
```

```
300
```

The `print(b1 + b2 + b3)` line fails because `b1 + b2` returns an integer (300), and Python does not know how to add an integer to a `Book`. The fix is to return a `Book` from `__add__` instead:

```python
class Book:
    def __init__(self, page) -> None:
        self.page = page

    def __add__(self, other):
        total_pages = self.page + other.page
        newBook = Book(total_pages)
        return newBook

    def __str__(self) -> str:
        return str(self.page)

b1 = Book(100)
b2 = Book(200)
b3 = Book(600)
b4 = Book(100)

print(b1 + b2 + b3)
```

```
900
```

The general pattern for chained `+` is: **the result of `__add__` should be the same type as the operands**. Then `b1 + b2 + b3` works, because each step returns a `Book`, and the next `+` calls `__add__` again.

You can confirm this is happening by adding print statements in each magic method:

```python
class Book:
    def __init__(self, page) -> None:
        print("New object crated...")
        self.page = page

    def __add__(self, other):
        print("Add method execution...")
        total_pages = self.page + other.page
        newBook = Book(total_pages)
        return newBook

    def __str__(self) -> str:
        print("str method execution...")
        return str(self.page)

b1 = Book(100)
b2 = Book(200)
b3 = Book(600)
b4 = Book(100)
b = b1 + b2 + b3 + b4
print(b)
```

```
New object crated...
New object crated...
New object crated...
New object crated...
Add method execution...
New object crated...
Add method execution...
New object crated...
Add method execution...
New object crated...
str method execution...
1000
```

This output shows exactly the order of operations:

1. Four `Book` objects are constructed.
2. Each `+` calls `__add__` on the left operand, which constructs a new `Book` and returns it.
3. The new `Book` becomes the left operand of the next `+`.
4. `print(b)` calls `__str__` exactly once, on the final result.

**More Examples — `__add__` in Real Development**

FastAPI: merging two Pydantic-style response/filter objects — a common pattern when combining query parameters from different sources (path params + query params) into one filter before hitting the database.

```python
class QueryFilter:
    def __init__(self, filters: dict):
        self.filters = filters

    def __add__(self, other):
        merged = {**self.filters, **other.filters}
        return QueryFilter(merged)

    def __repr__(self):
        return f"QueryFilter({self.filters})"

base_filter = QueryFilter({"is_active": True})
user_filter = QueryFilter({"role": "admin"})
final_filter = base_filter + user_filter
print(final_filter)
```

```
QueryFilter({'is_active': True, 'role': 'admin'})
```

combining two `WHERE` clause builders into a single condition, useful when building a query dynamically across multiple service layers.

```python
class WhereClause:
    def __init__(self, conditions):
        self.conditions = conditions   # list of SQL condition strings

    def __add__(self, other):
        return WhereClause(self.conditions + other.conditions)

    def __str__(self):
        return " AND ".join(self.conditions)

c1 = WhereClause(["age > 18"])
c2 = WhereClause(["country = 'IN'"])
combined = c1 + c2
print(f"SELECT * FROM users WHERE {combined}")
```

```
SELECT * FROM users WHERE age > 18 AND country = 'IN'
```

combining two route segments into a single network path, similar to how routers build up a full path from hop-by-hop segments.

```python
class RouteSegment:
    def __init__(self, hops):
        self.hops = hops

    def __add__(self, other):
        return RouteSegment(self.hops + other.hops)

    def __str__(self):
        return " -> ".join(self.hops)

segment1 = RouteSegment(["Client", "Router-A"])
segment2 = RouteSegment(["Router-B", "Server"])
full_route = segment1 + segment2
print(full_route)
```

```
Client -> Router-A -> Router-B -> Server
```

### **Mixing `+` and `*`**

`__add__` and `__mul__` work together when both are defined. The same `Book` example with chaining:

```python
class Book:
    def __init__(self, pg):
        self.pg = pg

    def __add__(self, other):
        return Book(self.pg + other.pg)

    def __str__(self):
        return '  Total no of Pg {} '.format(self.pg)

    def __mul__(self, other):
        return Book(self.pg * other.pg)

b1 = Book(1)
b2 = Book(2)
b3 = Book(3)
b4 = Book(4)
print(b1 + b2 + b3 + b4)        # 1+2+3+4 = 10
print(b1 + b2 * b3 + b4)        # 1 + 2*3 + 4 = 11 (Python's standard precedence: * before +)
```

```
  Total no of Pg 10 
  Total no of Pg 11 
```

The result of `b1 + b2 * b3 + b4` is `11` because Python evaluates `*` before `+`, exactly the same way it would with plain numbers: `1 + (2*3) + 4`.

**More Examples — Mixing `+` and `*` in Real Development**

a common billing formula — `total = base_fee + (usage * rate)` — works naturally once both operators are overloaded, and Python's normal precedence (`*` before `+`) applies exactly as expected.

```python
class Cost:
    def __init__(self, amount):
        self.amount = amount

    def __add__(self, other):
        return Cost(self.amount + other.amount)

    def __mul__(self, other):
        return Cost(self.amount * other)

    def __str__(self):
        return f"${self.amount:.2f}"

base_fee = Cost(5.00)
rate_per_hour = Cost(0.10)
hours_used = 120

total_bill = base_fee + rate_per_hour * hours_used
print(total_bill)   # 5 + (0.10 * 120) = 17.00
```

```
$17.00
```

## **`__str__` and `__repr__`**

These two methods control how an object is converted to a string. They look similar but serve different purposes.

- `__str__` — returns a **human-readable** string. Called by `print(obj)` and `str(obj)`. Goal: a nice string for end users.
- `__repr__` — returns an **unambiguous** string. Called by `repr(obj)` and by the REPL when you type the object's name. Goal: a string that, ideally, can be fed back to `eval()` to recreate the object.

### **`__str__` in Action**

```python
class Student:
    def __init__(self, name, marks) -> None:
        self.name = name
        self.marks = marks

    def __str__(self) -> str:
        return self.name   # override __str__ default implementation

s1 = Student("Durga", 100)
s2 = Student("Ravi", 200)

print(s1)
print(s2)
```

```
Durga
Ravi
```

By default, `print(s1)` would have shown something like `<__main__.Student object at 0x7f...>`. By overriding `__str__`, we control what gets printed.

A more useful version returns a formatted string:

```python
class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def __str__(self):
        return 'Student with Name: {}, Marks: {}'.format(self.name, self.marks)

s1 = Student('Durga', 100)
s2 = Student('Ravi', 200)

print(s1)
print(s2)
```

```
Student with Name: Durga, Marks: 100
Student with Name: Ravi, Marks: 200
```

The rule:

- `+` operator → `__add__`
- `print` function → `__str__`

**More Examples — `__str__` in Real Development**

FastAPI: a request/response model with a clean `__str__` so logs are readable instead of showing a raw object address.

```python
class APIResponse:
    def __init__(self, status_code, path, duration_ms):
        self.status_code = status_code
        self.path = path
        self.duration_ms = duration_ms

    def __str__(self):
        return f"[{self.status_code}] {self.path} ({self.duration_ms}ms)"

resp = APIResponse(200, "/api/v1/users", 42)
print(f"Request completed: {resp}")
```

```
Request completed: [200] /api/v1/users (42ms)
```

a database row/record object whose `__str__` prints a friendly summary, useful when printing query results while debugging.

```python
class UserRow:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

    def __str__(self):
        return f"User#{self.user_id}: {self.name} <{self.email}>"

row = UserRow(101, "Akshay Redekar", "akshay@example.com")
print(row)
```

```
User#101: Akshay Redekar <akshay@example.com>
```

printing an IP packet in a log-friendly format instead of the default object representation.

```python
class IPPacket:
    def __init__(self, src, dst, protocol):
        self.src = src
        self.dst = dst
        self.protocol = protocol

    def __str__(self):
        return f"{self.protocol} packet: {self.src} -> {self.dst}"

packet = IPPacket("192.168.1.10", "10.0.0.5", "TCP")
print(packet)
```

```
TCP packet: 192.168.1.10 -> 10.0.0.5
```

### **The Difference Between `str()` and `repr()`**

A practical demonstration using a `datetime` object:

```python
import datetime
today = datetime.datetime.now()

s = str(today)
print(s)
# today1 = eval(s)    # would raise an error

s = repr(today)
print(s)

today2 = eval(s)
print(today2)
print(type(today2))
```

```
2024-10-08 21:34:42.616405
datetime.datetime(2024, 10, 8, 21, 34, 42, 616405)
2024-10-08 21:34:42.616405
<class 'datetime.datetime'>
```

What is happening:

- `str(today)` gives a nicely formatted date string. Useful for display.
- `repr(today)` gives a string that looks like the constructor call itself: `datetime.datetime(2024, 10, 8, 21, 34, 42, 616405)`. Crucially, you can pass this string to `eval()` to recreate the original object.

The rule, in plain English:

- `str()` produces a string for **humans to read**.
- `repr()` produces a string for **developers to debug**, often round-trippable through `eval()`.

**More Examples — `__str__` vs `__repr__` in Real Development**

a `DBConnection` object where `__str__` gives a safe, human-friendly summary (no password), while `__repr__` gives an unambiguous, developer-facing view for debugging in logs.

```python
class DBConnection:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def __str__(self):
        return f"Connected to {self.host}:{self.port} as {self.user}"

    def __repr__(self):
        return f"DBConnection(host={self.host!r}, port={self.port}, user={self.user!r})"

conn = DBConnection("db.internal", 5432, "app_user", "s3cret")
print(conn)          # calls __str__
print(repr(conn))    # calls __repr__, password intentionally excluded
```

```
Connected to db.internal:5432 as app_user
DBConnection(host='db.internal', port=5432, user='app_user')
```

a `CloudResource` object where `__repr__` is round-trippable (mirrors constructor args), which is exactly what you want when logging objects for later debugging or replay.

```python
class CloudResource:
    def __init__(self, resource_id, region):
        self.resource_id = resource_id
        self.region = region

    def __str__(self):
        return f"{self.resource_id} (in {self.region})"

    def __repr__(self):
        return f"CloudResource(resource_id={self.resource_id!r}, region={self.region!r})"

r = CloudResource("i-0abc123", "ap-south-1")
print(r)
print([r])   # lists use __repr__ for their elements
```

```
i-0abc123 (in ap-south-1)
[CloudResource(resource_id='i-0abc123', region='ap-south-1')]
```

## **Method Overloading in Python**

Method overloading — same method name, different parameter lists — is **not possible** in Python in the way it is in Java or C++.

The reason is Python's **dynamic typing**. Java and C++ need overloaded methods because they require you to specify the data type of every parameter. A method called `add(int a, int b)` is a different signature from `add(float a, float b)`. Python does not require you to declare types, so the same method body can already handle many different kinds of input.

Two other reasons overloading is not needed:

- **Duck typing** — Python cares about what an object can do, not what type it is. If an object has the right method or attribute, you can use it.
- **Default arguments** — instead of overloading, you can give a parameter a default value, and the same method handles both cases.

```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")
```

### **A Class With a Single Method That Handles All Types**

This is how Python "simulates" overloading — by checking the type at runtime:

```python
class Test:
    def m1(self, x):
        # print("Type of x", type(x))
        print(f"{x.__class__.__name__}-argument method")

t = Test()
t.m1(10)
t.m1("Durga")
t.m1(True)
t.m1(None)
t.m1(7.54)
t.m1([1, 2, 3, 4])
t.m1(())
t.m1({1: 3})
t.m1({2, 3, 4})
```

```
int-argument method
str-argument method
bool-argument method
NoneType-argument method
float-argument method
list-argument method
tuple-argument method
dict-argument method
set-argument method
```

One method, many types. The output reflects the actual type of the argument at runtime.

**More Examples — One Method Handling Many Types in Real Development**

FastAPI: a single path-parameter handler that behaves differently depending on whether the identifier looks like a numeric ID or a slug, without needing separate overloaded functions.

```python
def get_user_identifier(value):
    if isinstance(value, int):
        return f"Looking up user by numeric ID: {value}"
    elif isinstance(value, str):
        return f"Looking up user by slug/username: {value}"
    else:
        raise TypeError("Unsupported identifier type")

print(get_user_identifier(42))
print(get_user_identifier("akshay-redekar"))
```

```
Looking up user by numeric ID: 42
Looking up user by slug/username: akshay-redekar
```

a generic `search` function that works whether you pass a `list`, a `set`, or a `dict` — one function, many container types, thanks to duck typing.

```python
def search(container, target):
    if isinstance(container, dict):
        return target in container.keys()
    return target in container

print(search([1, 2, 3], 2))
print(search({1, 2, 3}, 5))
print(search({"a": 1, "b": 2}, "a"))
```

```
True
False
True
```

a `send()` method that accepts either `str` or `bytes` and normalizes internally, similar to how socket libraries handle mixed input.

```python
class Socket:
    def send(self, data):
        if isinstance(data, str):
            payload = data.encode("utf-8")
        elif isinstance(data, bytes):
            payload = data
        else:
            raise TypeError("data must be str or bytes")
        print(f"Sending {len(payload)} bytes: {payload}")

s = Socket()
s.send("hello")
s.send(b"hello")
```

```
Sending 5 bytes: b'hello'
Sending 5 bytes: b'hello'
```

### **What Happens if You Try to Define Multiple `m1`s**

In Python, defining a method with the same name in a class simply **overwrites** the previous one. The latest definition wins.

```python
class Test:
    def m1(self, x):
        print("one arg method")
    def m1(self, x, y):
        print("two arg method")
    def m1(self, x, y, z):
        print("three arg method")

t = Test()
# t.m1(10)    # TypeError: Test.m1() missing 2 required positional arguments: 'y' and 'z'
t.m1(32, "durga", [1, 2, 3, 4])
```

```
three arg method
```

Only the last `m1` survives. Earlier ones are silently replaced. This is the proof that Python does not support overloading.

### **How to Handle Variable Number of Arguments**

The standard Pythonic ways to simulate overloading are:

1. **Default arguments** — give parameters a default of `None`, then check inside the method.
2. **`*args` and `**kwargs`** — accept any number of arguments.

**Approach 1: Default arguments with `None`**

```python
class Test:
    def m1(self, a=None, b=None, c=None):
        if a is not None and b is not None and c is not None:
            print("3-args method")
        elif a is not None and b is not None:
            print("2-args method")
        elif a is not None:
            print("1-args method")

t = Test()
t.m1(10)
t.m1(10, 20)
t.m1(10, 20, 30)
```

```
1-args method
2-args method
3-args method
```

**Approach 2: `*args`**

```python
class Test:
    def sum(self, *a):
        res = 0
        for x in a:
            res += x
        print("Sum is:", res)

t = Test()
t.sum()
t.sum(10, 20)
t.sum(10, 20, 30)
t.sum(10, 20, 30, 40)
```

```
Sum is: 0
Sum is: 30
Sum is: 60
Sum is: 100
```

This pattern is what you will see in real codebases — a single method that adapts to any number of arguments.

**More Examples — `*args` / `**kwargs` in Real Development**

building a dynamic `WHERE` clause from an arbitrary number of keyword filters — exactly how many ORMs implement `.filter(**kwargs)`.

```python
class QueryBuilder:
    def filter(self, **kwargs):
        conditions = [f"{key} = '{value}'" for key, value in kwargs.items()]
        return " AND ".join(conditions)

qb = QueryBuilder()
print(qb.filter(country="IN"))
print(qb.filter(country="IN", role="admin"))
print(qb.filter(country="IN", role="admin", is_active="true"))
```

```
country = 'IN'
country = 'IN' AND role = 'admin'
country = 'IN' AND role = 'admin' AND is_active = 'true'
```

a cloud API client function that accepts a variable set of config overrides, the same idiom used by SDKs like boto3 for optional keyword parameters.

```python
class CloudClient:
    def launch_instance(self, instance_type, **options):
        config = {"instance_type": instance_type, **options}
        print("Launching with config:", config)

client = CloudClient()
client.launch_instance("t3.micro")
client.launch_instance("t3.micro", region="ap-south-1")
client.launch_instance("t3.micro", region="ap-south-1", tags={"env": "prod"})
```

```
Launching with config: {'instance_type': 't3.micro'}
Launching with config: {'instance_type': 't3.micro', 'region': 'ap-south-1'}
Launching with config: {'instance_type': 't3.micro', 'region': 'ap-south-1', 'tags': {'env': 'prod'}}
```

Networking/OS: a logger that accepts a variable number of positional fields, similar to how `print()`-style loggers aggregate arbitrary context.

```python
class Logger:
    def log(self, level, *fields):
        message = " | ".join(str(f) for f in fields)
        print(f"[{level}] {message}")

logger = Logger()
logger.log("INFO", "server started")
logger.log("ERROR", "connection refused", "retry 1/3")
logger.log("DEBUG", "cpu", "42%", "mem", "1.2GB")
```

```
[INFO] server started
[ERROR] connection refused | retry 1/3
[DEBUG] cpu | 42% | mem | 1.2GB
```

## **Constructor Overloading in Python**

Like method overloading, **constructor overloading is not possible** in Python. If you define multiple `__init__` methods in a class, only the last one survives. The earlier ones are silently overwritten.

```python
class Test:
    def __init__(self) -> None:
        print("One args constructor")


class Test:
    def __init__(self, x=None, y=None, z=None) -> None:
        print("No args | One args | Two args | Three args constructor")


t = Test()
t = Test(10)
t = Test(10, 20)
t = Test(10, 20, 30)
```

```
No args | One args | Two args | Three args constructor
No args | One args | Two args | Three args constructor
No args | One args | Two args | Three args constructor
No args | One args | Two args | Three args constructor
```

The same single constructor runs for all four cases, because `x`, `y`, and `z` all have default values of `None`. This is the standard Pythonic way to simulate constructor overloading.

**More Examples — Constructor "Overloading" with Defaults in Real Development**

FastAPI: an app `Config` class that works with zero args (sensible defaults for local dev) or fully overridden args for production — a very common settings pattern.

```python
class Config:
    def __init__(self, host="127.0.0.1", port=8000, debug=True):
        self.host = host
        self.port = port
        self.debug = debug

    def __str__(self):
        return f"http://{self.host}:{self.port} (debug={self.debug})"

dev_config = Config()
prod_config = Config(host="0.0.0.0", port=80, debug=False)

print(dev_config)
print(prod_config)
```

```
http://127.0.0.1:8000 (debug=True)
http://0.0.0.0:80 (debug=False)
```

a `DBConnection` class that can be constructed with just a database name (using default host/port) or with every parameter fully specified.

```python
class DBConnection:
    def __init__(self, dbname, host="localhost", port=5432, user="postgres"):
        self.dbname = dbname
        self.host = host
        self.port = port
        self.user = user

    def __str__(self):
        return f"{self.user}@{self.host}:{self.port}/{self.dbname}"

local_conn = DBConnection("myapp_dev")
remote_conn = DBConnection("myapp_prod", host="db.prod.internal", port=5433, user="app_user")

print(local_conn)
print(remote_conn)
```

```
postgres@localhost:5432/myapp_dev
app_user@db.prod.internal:5433/myapp_prod
```

### **Variable-Length Constructor with `*args`**

A more flexible version uses `*args` to accept any number of arguments:

```python
class Test:
    def __init__(self, *args) -> None:
        print("Constructor with variable number of arguments", len(args))
        for i in range(len(args)):
            print(f"argument {i+1}: {args[i]}")


t = Test(1, 2, 3, 4)
t = Test(14, 23, 31, 41, 71)
```

```
Constructor with variable number of arguments 4
argument 1: 1
argument 2: 2
argument 3: 3
argument 4: 4
Constructor with variable number of arguments 5
argument 1: 14
argument 2: 23
argument 3: 31
argument 4: 41
argument 5: 71
```

**More Examples — Variable-Length Constructor in Real Development**

a `Packet` class that accepts a variable number of header segments, since real protocol stacks (Ethernet, IP, TCP) wrap a packet in a variable number of headers.

```python
class Packet:
    def __init__(self, payload, *headers):
        self.payload = payload
        self.headers = headers

    def __str__(self):
        return f"{list(self.headers)} -> {self.payload}"

p1 = Packet("data", "TCP")
p2 = Packet("data", "Ethernet", "IP", "TCP")

print(p1)
print(p2)
```

```
['TCP'] -> data
['Ethernet', 'IP', 'TCP'] -> data
```

a `TreeNode` (or general graph node) that can be constructed with any number of children, useful for n-ary trees rather than strictly binary ones.

```python
class TreeNode:
    def __init__(self, value, *children):
        self.value = value
        self.children = list(children)

    def __str__(self):
        child_values = [c.value for c in self.children]
        return f"{self.value} -> {child_values}"

leaf1 = TreeNode("B")
leaf2 = TreeNode("C")
leaf3 = TreeNode("D")
root = TreeNode("A", leaf1, leaf2, leaf3)

print(root)
```

```
A -> ['B', 'C', 'D']
```

### **Examples**

```python
# Example 1: Overload < by marks
class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score
    def __lt__(self, other):
        return self.score < other.score

p1 = Player("A", 50)
p2 = Player("B", 80)
print(p1 < p2)    # True
print(p2 < p1)    # False
```

```
True
False
```

```python
# Example 2: Overload + to combine two Vectors
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)
```

```
Vector(4, 6)
```

```python
# Example 3: A single method that handles many input types
class Echo:
    def show(self, value):
        print(f"got a {type(value).__name__}: {value}")

Echo().show(10)
Echo().show("hello")
Echo().show([1, 2, 3])
```

```
got a int: 10
got a str: hello
got a list: [1, 2, 3]
```

```python
# Example 4: Default arguments as a form of overloading
class Greeter:
    def hello(self, name="Guest", greeting="Hello"):
        print(f"{greeting}, {name}!")

g = Greeter()
g.hello()
g.hello("Durga")
g.hello("Ravi", "Hi")
```

```
Hello, Guest!
Hello, Durga!
Hi, Ravi!
```

```python
# Example 5: __str__ vs __repr__
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return f"point at ({self.x}, {self.y})"
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

p = Point(3, 4)
print(p)           # calls __str__
print(repr(p))     # calls __repr__
print([p])         # list uses __repr__
```

```
point at (3, 4)
Point(3, 4)
[Point(3, 4)]
```

The last line is a useful trick: containers like `list` and `dict` use `__repr__` for their elements, even when you do not print them directly. That is why defining both `__str__` and `__repr__` is the standard advice.

## **Quick Reference Summary**

### **Operator Overloading**

| Operator | Magic method | Notes |
|---|---|---|
| `+` | `__add__(self, other)` | For chaining to work, return the same type. |
| `-` | `__sub__(self, other)` | |
| `*` | `__mul__(self, other)` | The left operand's class decides which `__mul__` is called. |
| `<` | `__lt__(self, other)` | `>` is automatically derived. |
| `>` | `__gt__(self, other)` | `<` is automatically derived. |
| `<=` | `__le__(self, other)` | `>=` is automatically derived. |
| `>=` | `__ge__(self, other)` | `<=` is automatically derived. |
| `==` | `__eq__(self, other)` | |
| `print(obj)` | `__str__(self)` | Human-readable. |
| `repr(obj)` | `__repr__(self)` | Unambiguous, often round-trippable. |

### **Overloading vs Overriding in Python**

| Concept | Supported in Python? | How to handle it |
|---|---|---|
| Operator overloading | Yes — via magic methods. | Override `__add__`, `__lt__`, etc. |
| Method overloading | No — last definition wins. | Use default arguments or `*args`. |
| Constructor overloading | No — last definition wins. | Use default arguments or `*args`. |
| Method overriding | Yes — fully supported. | Define a method with the same name in the child class. |
| Constructor overriding | Yes — fully supported. | Override `__init__` in the child class; call `super().__init__()` to extend. |

### **`str()` vs `repr()`**

| Method | Audience | Goal | Example |
|---|---|---|---|
| `__str__` | End users | Readable, friendly | `Student with Name: Durga, Marks: 100` |
| `__repr__` | Developers | Unambiguous, ideally round-trippable | `Point(3, 4)` |

## **Practice and Next Steps**

- Create a `Fraction` class with numerator and denominator. Overload `+`, `-`, `*`, `/` to do arithmetic on fractions.
- Create a `Vector` class and overload `+` to add two vectors element-wise. Confirm chaining works.
- Create a `Student` class and overload `<` to compare students by marks first, then by name if marks are equal.
- Create an `Employee` and `TimeSheet` setup. Overload `*` to compute the salary. Make sure both `employee * timesheet` and `timesheet * employee` work.
- Define a `Money` class. Overload `+` to add two `Money` values, and `__str__` to print in a format like `"$100"`. Test chaining `m1 + m2 + m3`.
- Add both `__str__` and `__repr__` to a class. Try `print(obj)`, `repr(obj)`, and `[obj]` to see which one fires.
- Write a class with a single method that uses `*args`. Call it with zero, one, two, and five arguments.
- Try defining two `__init__` methods in the same class. Confirm only the last one survives. Then refactor to use default arguments.