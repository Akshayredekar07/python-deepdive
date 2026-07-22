# **Inner Classes and Nested Methods**

## **What is an Inner Class**

An **inner class** (also called a **nested class**) is a class that is declared inside another class. In Python, there is no special keyword for this — you simply write a `class` statement inside another `class` body.

The general rule for when to use an inner class:

> **Without the existence of one type of object, if there is no chance of existing another type of object, then we should go for inner classes.**

In other words, if class B only makes sense in the context of class A, then B should be an inner class of A.

### **Real-World Examples**

**Example 1: University and Department**

Without a university object, there is no chance of a department object existing. The Department should be a part of the University and cannot exist on its own.

```python
class University:    # Outer class
    class Department:    # Inner class
        pass
```

**Example 2: Car and Engine**

Without a car object, there is no chance of an engine object existing. The Engine should be associated with the Car.

```python
class Car:
    class Engine:
        pass
```

**Example 3: Head and Brain**

Without a head object, there is no chance of a brain object existing. The Brain should be inside the Head.

```python
class Head:
    class Brain:
        pass
```

### **More Real-World Examples — Software Engineering Domains**

**Example 4: FastAPI — Request and its Query Params (API Design)**

A `Pagination` object never makes sense outside the request it belongs to. This is the same pattern used in real API code, where a request/schema class groups its own sub-structures.

```python
class ProductListRequest:
    class Pagination:
        def __init__(self, page: int = 1, size: int = 10):
            self.page = page
            self.size = size
```

**Example 5: DSA — LinkedList and Node**

A `Node` has no meaning outside a `LinkedList`. This is the standard way senior engineers structure linked-list implementations so the `Node` type doesn't leak into the global namespace.

```python
class LinkedList:
    class Node:
        pass
```

**Example 6: Networking — TCPServer and Connection**

A `Connection` cannot exist without a `TCPServer` accepting it. Bundling them communicates that `Connection` is server-owned.

```python
class TCPServer:
    class Connection:
        pass
```

**Example 7: Operating Systems — Process and Thread**

A `Thread` only exists within the context of a `Process` that owns it.

```python
class Process:
    class Thread:
        pass
```

**Example 8: DBMS — Database and Table**

A `Table` has no independent existence outside the `Database` it belongs to.

```python
class Database:
    class Table:
        pass
```

**Example 9: Cloud — VPC and Subnet**

A `Subnet` cannot exist without a `VPC` (Virtual Private Cloud) to belong to — this mirrors how AWS/GCP model these resources.

```python
class VPC:
    class Subnet:
        pass
```

### **Without Inner Classes vs With Inner Classes**

Without inner classes, you would model these as separate top-level classes:

```python
class Head:
    pass

class Mouth:
    pass

class Eye:
    pass
```

This works, but it loses the semantic relationship. The reader of the code does not know that `Mouth` and `Eye` are conceptually parts of a `Head`.

With inner classes, the relationship is explicit:

```python
class Head:
    class Eye:
        pass
    class Brain:
        pass
    class Mouth:
        pass
```

Now the structure of the code mirrors the structure of the domain. The `Head` class contains its parts, and they cannot reasonably be used without it.

### **Advantages of Inner Classes**

- **Modularity** of the application — related classes are grouped together.
- **Security** — the inner class is naturally scoped to the outer class.
- **Readability** — the relationship is obvious from the code.
- **Namespacing** — the inner class name is qualified by the outer class, so `Head.Brain` cannot accidentally collide with a `Brain` class defined elsewhere.

## **Defining an Inner Class**

```python
class OuterClass:
    def __init__(self) -> None:
        print("Outerclass object creation")

    class InnerClass:
        def __init__(self) -> None:
            print("Innerclass object creation")

        def m1(self):
            print("Inner class method")
```

Notice the rule from earlier: **without an existing outer class object, there is no chance of an existing inner class object**. The inner class object is always associated with the outer class object.

### **More Examples of Defining an Inner Class**

**Example — FastAPI-style Settings with a nested Config class**

This mirrors the real Pydantic `Config` pattern used in almost every FastAPI project.

```python
class Settings:
    def __init__(self, env: str) -> None:
        print(f"Settings loaded for env={env}")
        self.env = env

    class Config:
        def __init__(self) -> None:
            print("Config object created")

        def describe(self):
            print("case_sensitive=True, env_file='.env'")
```

**Example — DSA: LinkedList with a Node inner class**

```python
class LinkedList:
    def __init__(self) -> None:
        print("LinkedList created")
        self.head = None

    class Node:
        def __init__(self, data) -> None:
            print(f"Node created with data={data}")
            self.data = data
            self.next = None
```

**Example — DBMS: Connection with a nested Cursor class**

```python
class Connection:
    def __init__(self, dsn: str) -> None:
        print(f"Connection opened to {dsn}")
        self.dsn = dsn

    class Cursor:
        def __init__(self) -> None:
            print("Cursor created")

        def execute(self, query: str):
            print(f"Executing: {query}")
```

## **Creating Inner Class Objects**

There are several equivalent ways to create an inner class object.

### **Way 1 — Through an outer class object**

```python
o = OuterClass()
i = o.InnerClass()
i.m1()
```

```
Outerclass object creation
Innerclass object creation
Inner class method
```

Using `o`, you can call any OuterClass method. Using `o.InnerClass()`, you get the inner class and can call its methods.

### **Way 2 — One-liner through a temporary outer object**

```python
IObj = OuterClass().InnerClass()
IObj.m1()
```

```
Outerclass object creation
Innerclass object creation
Inner class method
```

### **Way 3 — Fully chained call**

```python
OuterClass().InnerClass().m1()
```

```
Outerclass object creation
Innerclass object creation
Inner class method
```

The outer class is created, used to reach the inner class, the inner class is created, and `m1()` is called — all in one line. The intermediate objects are discarded as soon as the line finishes.

### **The Same Three Ways, Applied to Real Dev Scenarios**

**DSA — creating a Node through a LinkedList (Way 1 style)**

```python
ll = LinkedList()
n = ll.Node(10)
print(n.data)
```

```
LinkedList created
Node created with data=10
10
```

**DBMS — creating a Cursor through a Connection (Way 2 style)**

```python
cur = Connection("postgres://localhost/mydb").Cursor()
cur.execute("SELECT * FROM users")
```

```
Connection opened to postgres://localhost/mydb
Cursor created
Executing: SELECT * FROM users
```

**FastAPI-style — creating and reading Config in one line (Way 3 style)**

```python
Settings("production").Config().describe()
```

```
Settings loaded for env=production
Config object created
case_sensitive=True, env_file='.env'
```

## **Multiple Inner Classes in the Same Outer Class**

A single outer class can have many inner classes. Each is independent of the others.

```python
class OuterClass:
    def __init__(self) -> None:
        print("Outerclass object creation")

    class InnerClass:
        def __init__(self) -> None:
            print("Innerclass object creation")

        def m1(self):
            print("Inner class method")

    class InnerClass1:
        def __init__(self) -> None:
            print("Innerclass1 object creation")

        def m2(self):
            print("Inner class 1 method")


O = OuterClass()
I = O.InnerClass()
J = O.InnerClass1()
I.m1()
J.m2()
```

```
Outerclass object creation
Innerclass object creation
Innerclass1 object creation
Inner class method
Inner class 1 method
```

The order of `print` statements shows that the outer object is created first, then each inner object is created on demand, then their methods are called.

### **More Examples — Multiple Inner Classes in Real Systems**

**DSA — a Stack class exposing both a Node and an EmptyStackError inner class**

```python
class Stack:
    def __init__(self) -> None:
        print("Stack created")
        self.items = []

    class Node:
        def __init__(self, value) -> None:
            print(f"Node created: {value}")
            self.value = value

    class EmptyStackError:
        def __init__(self) -> None:
            print("EmptyStackError object created")

        def message(self):
            print("Cannot pop from an empty stack")


s = Stack()
n = s.Node(42)
e = s.EmptyStackError()
e.message()
```

```
Stack created
Node created: 42
EmptyStackError object created
Cannot pop from an empty stack
```

**FastAPI-style — an Endpoint class with separate Request and Response inner classes**

```python
class UserEndpoint:
    def __init__(self) -> None:
        print("UserEndpoint registered")

    class Request:
        def __init__(self, user_id: int) -> None:
            print(f"Request received for user_id={user_id}")
            self.user_id = user_id

    class Response:
        def __init__(self, status: int) -> None:
            print(f"Response object created with status={status}")
            self.status = status

        def send(self):
            print(f"Sending response with status {self.status}")


ep = UserEndpoint()
req = ep.Request(101)
res = ep.Response(200)
res.send()
```

```
UserEndpoint registered
Request received for user_id=101
Response object created with status=200
Sending response with status 200
```

**Cloud — an EC2Instance class with Volume and SecurityGroup inner classes**

```python
class EC2Instance:
    def __init__(self, instance_id: str) -> None:
        print(f"EC2Instance {instance_id} launched")
        self.instance_id = instance_id

    class Volume:
        def __init__(self, size_gb: int) -> None:
            print(f"Volume attached: {size_gb}GB")

    class SecurityGroup:
        def __init__(self, name: str) -> None:
            print(f"SecurityGroup attached: {name}")


i = EC2Instance("i-0abcd1234")
v = i.Volume(50)
sg = i.SecurityGroup("web-sg")
```

```
EC2Instance i-0abcd1234 launched
Volume attached: 50GB
SecurityGroup attached: web-sg
```

## **Nesting of Inner Classes**

It is possible to nest inner classes — define an inner class inside another inner class. This is useful when the relationship chain is naturally hierarchical.

```python
class Outer:
    def __init__(self) -> None:
        print("Outerclass object creation")

    class InnerClass:
        def __init__(self) -> None:
            print("Innerclass object creation")

        class InnerInnerClass:
            def __init__(self) -> None:
                print("InnerInnerclass object creation")

            def m1(self):
                print("Nested Inner class method")


Outer().InnerClass().InnerInnerClass().m1()
```

```
Outerclass object creation
Innerclass object creation
InnerInnerclass object creation
Nested Inner class method
```

The chained call walks the full hierarchy: `Outer` → `InnerClass` → `InnerInnerClass` → `m1()`.

### **More Examples — Multi-Level Nesting in Real Systems**

**DBMS — Database → Table → Column**

A `Column` only makes sense inside a `Table`, which only makes sense inside a `Database`. This three-level chain mirrors how a schema is actually structured.

```python
class Database:
    def __init__(self, name) -> None:
        print(f"Database '{name}' connected")

    class Table:
        def __init__(self) -> None:
            print("Table object created")

        class Column:
            def __init__(self) -> None:
                print("Column object created")

            def describe(self):
                print("Nested column inside table inside database")


Database("shop_db").Table().Column().describe()
```

```
Database 'shop_db' connected
Table object created
Column object created
Nested column inside table inside database
```

**Cloud — VPC → Subnet → Instance**

```python
class VPC:
    def __init__(self) -> None:
        print("VPC object created")

    class Subnet:
        def __init__(self) -> None:
            print("Subnet object created")

        class Instance:
            def __init__(self) -> None:
                print("Instance object created")

            def start(self):
                print("Instance started inside subnet inside VPC")


VPC().Subnet().Instance().start()
```

```
VPC object created
Subnet object created
Instance object created
Instance started inside subnet inside VPC
```

**Operating Systems — System → Process → Thread**

```python
class System:
    def __init__(self) -> None:
        print("System object created")

    class Process:
        def __init__(self) -> None:
            print("Process object created")

        class Thread:
            def __init__(self) -> None:
                print("Thread object created")

            def run(self):
                print("Thread running inside process inside system")


System().Process().Thread().run()
```

```
System object created
Process object created
Thread object created
Thread running inside process inside system
```

## **Real-World Example — Human, Head, Brain**

This is the canonical example of nested inner classes, because a Brain only makes sense inside a Head, and a Head only makes sense inside a Human.

### **Manual Construction**

```python
class Human:
    class Head:
        def talk(self):
            print("Talking...!")

        class Brain:
            def think(self):
                print("Thinking...!")


human = Human()
head = human.Head()
head.talk()

brain = head.Brain()
brain.think()
```

```
Talking...!
Thinking...!
```

The chain is: Human → Head (via the human object) → Brain (via the head object).

### **One-Line Chained Calls**

```python
brain = Human().Head().Brain()
brain.think()
```

```
Thinking...!
```

```python
Human().Head().Brain().think()
```

```
Thinking...!
```

Both are equivalent ways to chain the construction and the method call in a single expression.

### **Automatic Construction via the Outer Constructor**

A more realistic shape is to have the outer constructor create the inner objects automatically. Then the outer class is responsible for ensuring its inner objects exist.

```python
class Human:
    def __init__(self, name):
        print("Human object is created")
        self.name = name
        self.head = self.Head()

    def info(self):
        print(f"Hello myself {self.name}")
        print("I am full busy with")
        self.head.talk()
        self.head.brain.think()

    class Head:
        def __init__(self) -> None:
            print("Head object is created")
            self.brain = self.Brain()

        def talk(self):
            print("Talking...!")

        class Brain:
            def __init__(self) -> None:
                print("Brain object is created")

            def think(self):
                print("Thinking...!")

human = Human("Durga")
human.info()
```

```
Human object is created
Head object is created
Brain object is created
Hello myself Durga
I am full busy with
Talking...!
Thinking...!
```

The order of output is exactly the order of construction:

1. The Human is created, which triggers its constructor.
2. The constructor creates a `Head`, which triggers Head's constructor.
3. The Head's constructor creates a `Brain`, which triggers Brain's constructor.
4. By the time `info()` is called, the entire chain exists.
5. `info()` calls `talk()` on the head and `think()` on the brain.

This pattern — outer creates middle creates inner, all automatically — is what you will see in many real codebases where one logical object contains smaller, dependent ones.

A slightly different version that demonstrates calling through a temporary object instead of `self`:

```python
class Human:
    def __init__(self, name):
        print("Human object is created")
        self.name = name
        self.head = self.Head()

    def info(self):
        print(f"Hello myself {self.name}")
        print("I am full busy with")
        self.head.talk()
        # Human("").Head().Brain().think()
        # self.head.brain.think()    # this also works

    class Head:
        def __init__(self) -> None:
            print("Head object is created")
            self.brain = self.Brain()

        def talk(self):
            print("Talking...!")

        class Brain:
            def __init__(self) -> None:
                print("Brain object is created")

            def think(self):
                print("Thinking...!")

human = Human("Durga")
human.info()
```

```
Human object is created
Head object is created
Brain object is created
Hello myself Durga
I am full busy with
Talking...!
```

When `info()` is called, the brain was already created during the head's construction. The line that calls `think()` has been commented out — the user can uncomment either of the two commented lines to see the brain's `think()` in action.

## **Another Real-World Example — Person with Date of Birth**

A common pattern is to use an inner class to model a sub-concept that only exists within the outer class.

```python
class Person:
    def __init__(self, name, dd, mm, yyyy):
        print("Person object created")
        self.name = name
        self.dob = self.Dob(dd, mm, yyyy)

    def info(self):
        print("Name ", self.name)
        self.dob.dispaly()

    class Dob:
        def __init__(self, dd, mm, yyyy):
            print("Dob is created")
            self.dd = dd
            self.mm = mm
            self.yyyy = yyyy

        def dispaly(self):
            print("DOB : {}/{}/{}".format(self.dd, self.mm, self.yyyy))

p = Person("Durga", 7, 9, 2001)
p.info()
```

```
Person object created
Dob is created
Name  Durga
DOB : 7/9/2001
```

`Dob` is an inner class of `Person`. It does not make sense without a `Person` to belong to, so it lives inside the outer class. The outer class's constructor builds the `Dob` automatically, and `info()` delegates the printing of the date to `dob.dispaly()`.

## **More Real-World Examples — Applying the Pattern to Software Engineering Tasks**

### **Example — FastAPI-style Settings with auto-built Config (backend/API development)**

This is exactly the shape you see in a real FastAPI project: a `Settings` class that builds a nested `Config` on construction, without the caller having to think about it.

```python
class Settings:
    def __init__(self, app_name: str):
        print("Settings object created")
        self.app_name = app_name
        self.config = self.Config()

    def show(self):
        print(f"App: {self.app_name}")
        self.config.display()

    class Config:
        def __init__(self) -> None:
            print("Config object created")
            self.debug = True
            self.env_file = ".env"

        def display(self):
            print(f"debug={self.debug}, env_file={self.env_file}")


settings = Settings("OrdersAPI")
settings.show()
```

```
Settings object created
Config object created
App: OrdersAPI
debug=True, env_file=.env
```

### **Example — DSA: LinkedList that auto-creates its head Node (data structures)**

```python
class LinkedList:
    def __init__(self, first_value):
        print("LinkedList object created")
        self.head = self.Node(first_value)

    def show_head(self):
        print(f"Head value: {self.head.data}")

    class Node:
        def __init__(self, data) -> None:
            print(f"Node object created with data={data}")
            self.data = data
            self.next = None


ll = LinkedList(5)
ll.show_head()
```

```
LinkedList object created
Node object created with data=5
Head value: 5
```

### **Example — DBMS: ConnectionPool that auto-creates a Connection (database engineering)**

```python
class ConnectionPool:
    def __init__(self, dsn: str):
        print("ConnectionPool object created")
        self.dsn = dsn
        self.connection = self.Connection(dsn)

    def run_query(self, query: str):
        self.connection.execute(query)

    class Connection:
        def __init__(self, dsn) -> None:
            print(f"Connection object created for {dsn}")
            self.dsn = dsn

        def execute(self, query: str):
            print(f"[{self.dsn}] running: {query}")


pool = ConnectionPool("mysql://localhost/orders")
pool.run_query("SELECT COUNT(*) FROM orders")
```

```
ConnectionPool object created
Connection object created for mysql://localhost/orders
[mysql://localhost/orders] running: SELECT COUNT(*) FROM orders
```

### **Example — Cloud: CloudResourceManager that auto-creates a Bucket (cloud/DevOps)**

```python
class CloudResourceManager:
    def __init__(self, project: str):
        print("CloudResourceManager object created")
        self.project = project
        self.bucket = self.Bucket()

    def summary(self):
        print(f"Project: {self.project}")
        self.bucket.info()

    class Bucket:
        def __init__(self) -> None:
            print("Bucket object created")
            self.region = "us-east-1"

        def info(self):
            print(f"Bucket region: {self.region}")


mgr = CloudResourceManager("my-cloud-project")
mgr.summary()
```

```
CloudResourceManager object created
Bucket object created
Project: my-cloud-project
Bucket region: us-east-1
```

### **Example — Networking: HTTPClient that auto-creates a RetryPolicy (networking)**

```python
class HTTPClient:
    def __init__(self, base_url: str):
        print("HTTPClient object created")
        self.base_url = base_url
        self.retry_policy = self.RetryPolicy()

    def get(self, path: str):
        print(f"GET {self.base_url}{path}")
        self.retry_policy.describe()

    class RetryPolicy:
        def __init__(self) -> None:
            print("RetryPolicy object created")
            self.max_retries = 3

        def describe(self):
            print(f"Will retry up to {self.max_retries} times on failure")


client = HTTPClient("https://api.example.com")
client.get("/users")
```

```
HTTPClient object created
RetryPolicy object created
GET https://api.example.com/users
Will retry up to 3 times on failure
```

## **Nested Methods**

A **nested method** is a method defined inside another method. Python allows this — unlike some other languages where methods can only exist at the class level.

### **The Problem — Repeated Code in One Method**

When the same block of code repeats inside a single method, defining a nested method can clean it up.

```python
class Test:
    def m1():
        a = 10
        b = 20
        print("Sum ", a + b)
        print("Diff ", a - b)
        print("Prod ", a * b)
        print("Div ", a / b)
        print()

        a = 100
        b = 200
        print("Sum ", a + b)
        print("Diff ", a - b)
        print("Prod ", a * b)
        print("Div ", a / b)
        print()

        a = 1000
        b = 2000
        print("Sum ", a + b)
        print("Diff ", a - b)
        print("Prod ", a * b)
        print("Div ", a / b)
        print()


Test.m1()
```

```
Sum  30
Diff  -10
Prod  200
Div  0.5

Sum  300
Diff  -100
Prod  20000
Div  0.5

Sum  3000
Diff  -1000
Prod  2000000
Div  0.5
```

Three repetitions of the same block. This is the situation where a nested method helps.

### **Refactored with a Nested Method**

```python
class Test:
    def m1(self):
        def cal(a, b):
            print("Sum ", a + b)
            print("Diff ", a - b)
            print("Prod ", a * b)
            print("Div ", a / b)
            print()
        cal(10, 20)
        cal(14, 76)
        cal(93, 66)

t = Test()
t.m1()
```

```
Sum  30
Diff  -10
Prod  200
Div  0.5

Sum  90
Diff  -62
Prod  1064
Div  0.18421052631578946

Sum  159
Diff  27
Prod  6138
Div  1.4090909090909092
```

The `cal` function is defined once inside `m1`, then called three times with different inputs. The repetition is gone, the logic is centralized, and `m1` reads cleanly.

### **The General Rule**

- If a piece of logic is used **repeatedly within one method**, use a **nested method**.
- If a piece of logic is used **repeatedly across methods of the same class**, use a **regular method** of the class.

### **A Real-World Example — Price Calculation**

A nested method is a natural way to express "first apply discount, then apply tax" without duplicating the math:

```python
def calculate_final_price(price, discount):
    def apply_discount(p):
        return p - (p * discount / 100)

    def apply_tax(p):
        tax_rate = 5   # 5% tax
        return p + (p * tax_rate / 100)

    discounted_price = apply_discount(price)
    final_price = apply_tax(discounted_price)
    return final_price


# Usage
original_price = 1000
discount = 10
final_price = calculate_final_price(original_price, discount)
print(f"The final price after discount and tax is: {final_price}")
```

```
The final price after discount and tax is: 945.0
```

The nested methods `apply_discount` and `apply_tax` are private to `calculate_final_price`. They cannot be called from outside, and they capture the `discount` value from the enclosing scope via closure. This is a clean way to express a multi-step transformation.

## **More Real-World Nested Method Examples — Across Software Engineering Domains**

### **Example — DSA: Binary Search with a nested comparison helper**

The nested `mid_check` avoids repeating the same comparison logic across multiple recursive calls.

```python
def binary_search(arr, target):
    def mid_check(low, high):
        if low > high:
            return -1
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            return mid_check(mid + 1, high)
        else:
            return mid_check(low, mid - 1)

    return mid_check(0, len(arr) - 1)


numbers = [2, 4, 6, 8, 10, 12, 14]
print(binary_search(numbers, 10))
print(binary_search(numbers, 5))
```

```
4
-1
```

### **Example — Networking: Retry-with-backoff using a nested attempt function**

A common real pattern: retry an HTTP/socket call with exponential backoff, without duplicating the "try, catch, wait" block for every attempt.

```python
import time

def fetch_with_retry(url, max_attempts=3):
    def attempt(n):
        print(f"Attempt {n}: connecting to {url}")
        if n < max_attempts:
            print("  -> failed, backing off")
            return attempt(n + 1)
        print("  -> success")
        return "200 OK"

    return attempt(1)


result = fetch_with_retry("https://api.example.com/data")
print(result)
```

```
Attempt 1: connecting to https://api.example.com/data
  -> failed, backing off
Attempt 2: connecting to https://api.example.com/data
  -> failed, backing off
Attempt 3: connecting to https://api.example.com/data
  -> success
200 OK
```

### **Example — DBMS: Building a dynamic WHERE clause with a nested helper**

Query-builder code often repeats the "condition + AND" pattern; a nested method keeps it in one place.

```python
def build_query(table, filters):
    def add_condition(column, value):
        return f"{column} = '{value}'"

    conditions = [add_condition(col, val) for col, val in filters.items()]
    where_clause = " AND ".join(conditions)
    return f"SELECT * FROM {table} WHERE {where_clause}"


query = build_query("users", {"status": "active", "role": "admin"})
print(query)
```

```
SELECT * FROM users WHERE status = 'active' AND role = 'admin'
```

### **Example — OS/File Processing: Reading multiple log files with a nested line-parser**

```python
def process_logs(file_names):
    def parse_line(line):
        return line.strip().upper()

    for name in file_names:
        print(f"Processing {name}")
        sample_lines = [f"{name} line1", f"{name} line2"]
        for line in sample_lines:
            print("  ", parse_line(line))


process_logs(["app.log", "error.log"])
```

```
Processing app.log
   APP.LOG LINE1
   APP.LOG LINE2
Processing error.log
   ERROR.LOG LINE1
   ERROR.LOG LINE2
```

### **Example — Cloud/DevOps: Validating resource tags with a nested validator**

```python
def deploy_resource(name, tags):
    def validate_tag(key, value):
        if not value:
            return f"{key}: MISSING VALUE"
        return f"{key}: {value} (ok)"

    print(f"Deploying {name}")
    for key, value in tags.items():
        print("  ", validate_tag(key, value))


deploy_resource("web-server-1", {"env": "prod", "owner": "", "team": "platform"})
```

```
Deploying web-server-1
   env: prod (ok)
   owner: MISSING VALUE
   team: platform (ok)
```

### **Try it in Jupyter — Small Examples**

```python
# Example 1: Inner class with one method
class Computer:
    class CPU:
        def process(self):
            return "processing..."

c = Computer.CPU()
print(c.process())
```

```
processing...
```

```python
# Example 2: Inner class accessed via outer object
class School:
    class Student:
        def greet(self):
            return "Hi!"

s = School()
print(s.Student().greet())
```

```
Hi!
```

```python
# Example 3: Nested method used multiple times
class Helper:
    def run(self):
        def square(x):
            return x * x
        print(square(2))
        print(square(3))
        print(square(5))

Helper().run()
```

```
4
9
25
```

```python
# Example 4: Inner class with two levels of nesting
class A:
    class B:
        class C:
            def hello(self):
                return "deep hello"

print(A.B.C().hello())
```

```
deep hello
```

```python
# Example 5: Inner class automatically created
class Document:
    def __init__(self, title):
        self.title = title
        self.meta = self.Metadata()

    class Metadata:
        def __init__(self):
            self.created = "2025-01-01"
        def show(self):
            return f"created at {self.created}"

d = Document("Notes")
print(d.meta.show())
```

```
created at 2025-01-01
```

```python
# Example 6: A nested method that uses the enclosing scope
def make_multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5))
print(triple(5))
```

```
10
15
```

This is a closure — the inner function `multiply` remembers `factor` from the outer function `make_multiplier`. The same pattern shows up in decorators, callbacks, and factory functions.

### **More Jupyter-Style Examples — Dev-Flavored**

```python
# Example 7: DSA — Stack implemented with an inner Node class
class Stack:
    def __init__(self):
        self.top = None

    class Node:
        def __init__(self, value, next_node=None):
            self.value = value
            self.next = next_node

    def push(self, value):
        self.top = self.Node(value, self.top)

    def pop(self):
        value = self.top.value
        self.top = self.top.next
        return value

s = Stack()
s.push(1)
s.push(2)
s.push(3)
print(s.pop())
print(s.pop())
```

```
3
2
```

```python
# Example 8: FastAPI-style — a route handler class with an inner Validator
class CreateUserRoute:
    class Validator:
        def is_valid(self, payload):
            return "email" in payload and "name" in payload

    def handle(self, payload):
        validator = self.Validator()
        if validator.is_valid(payload):
            return f"User {payload['name']} created"
        return "400 Bad Request"

route = CreateUserRoute()
print(route.handle({"name": "Asha", "email": "asha@example.com"}))
print(route.handle({"name": "Ravi"}))
```

```
User Asha created
400 Bad Request
```

```python
# Example 9: Networking — a nested method that builds headers once and reuses them
def make_api_caller(token):
    def call(endpoint):
        headers = {"Authorization": f"Bearer {token}"}
        return f"GET {endpoint} with headers {headers}"
    return call

caller = make_api_caller("abc123")
print(caller("/orders"))
print(caller("/users"))
```

```
GET /orders with headers {'Authorization': 'Bearer abc123'}
GET /users with headers {'Authorization': 'Bearer abc123'}
```

```python
# Example 10: DBMS — Table class with an inner IndexError-style class for missing rows
class Table:
    def __init__(self, name):
        self.name = name
        self.rows = {1: "Alice", 2: "Bob"}

    class RowNotFound:
        def __init__(self, row_id):
            self.row_id = row_id

        def message(self):
            return f"Row {self.row_id} not found in table"

    def get_row(self, row_id):
        if row_id in self.rows:
            return self.rows[row_id]
        return self.RowNotFound(row_id).message()

t = Table("users")
print(t.get_row(1))
print(t.get_row(99))
```

```
Alice
Row 99 not found in table
```

```python
# Example 11: Cloud — recursive nested method to compute total storage cost
def calculate_storage_bill(buckets):
    def cost_for(size_gb, rate_per_gb=0.02):
        return round(size_gb * rate_per_gb, 2)

    total = 0
    for bucket_name, size in buckets.items():
        bucket_cost = cost_for(size)
        print(f"{bucket_name}: {size}GB -> ${bucket_cost}")
        total += bucket_cost
    return round(total, 2)

bill = calculate_storage_bill({"logs-bucket": 120, "media-bucket": 450})
print(f"Total: ${bill}")
```

```
logs-bucket: 120GB -> $2.4
media-bucket: 450GB -> $9.0
Total: $11.4
```

## **Quick Reference Summary**

### **Inner Classes**

| Concept | Description |
|---|---|
| Inner class | A class declared inside another class. |
| When to use | When the inner class only makes sense in the context of the outer class. |
| How to instantiate | `Outer().Inner()` or `outer_obj.Inner()`. |
| How to chain | `Outer().Inner1().Inner2().method()`. |
| Nesting | Allowed — an inner class can have its own inner classes. |

### **Nested Methods**

| Concept | Description |
|---|---|
| Nested method | A function defined inside another method. |
| When to use | When the same logic is repeated multiple times within a single method. |
| Scope | The nested method can only be called from within the enclosing method. |
| Captures | A nested method can read variables from the enclosing method's scope. |
| Alternative | For cross-method reuse, use a regular class method instead. |

### **Decision Matrix**

| Pattern | When to use |
|---|---|
| Inner class | A logical sub-concept that only exists in the context of the outer class. |
| Inner class with auto-construction | The outer class's `__init__` creates the inner object so callers never see the construction step. |
| Nested method | The same logic block appears several times within one method. |
| Regular class method | The same logic block appears across multiple methods of the class. |
| Helper function (top-level) | A utility that is independent of any class. |

### **Where This Shows Up in Real Codebases**

| Domain | Example inner-class relationship |
|---|---|
| FastAPI / backend APIs | `Settings.Config`, `Endpoint.Request` / `Endpoint.Response` |
| DSA | `LinkedList.Node`, `Stack.Node`, `Tree.TreeNode` |
| Networking | `TCPServer.Connection`, `HTTPClient.RetryPolicy` |
| Operating Systems | `Process.Thread`, `System.Process.Thread` |
| DBMS | `Database.Table.Column`, `Connection.Cursor` |
| Cloud / DevOps | `VPC.Subnet.Instance`, `EC2Instance.Volume` |

## **Practice and Next Steps**

- Create an `Outer` class with an `Inner` class. Instantiate the inner class in three different ways (through the outer object, one-liner through a temporary outer object, and a fully chained call).
- Create a `Library` class that has an inner class `Book`. The library's constructor should create at least one book automatically.
- Build a `Human` → `Head` → `Brain` nested inner class. Make the `Human` constructor create the head, and the `Head` constructor create the brain.
- Build a `Person` class with an inner `Dob` class. Pass date values through the outer constructor and have the inner class format and print them.
- Write a method that does the same calculation three times. Refactor it by defining a nested method and calling it three times.
- Write a function that uses two nested methods (like `apply_discount` and `apply_tax`) to compute a final price. Add another nested method (e.g., `apply_shipping`) and chain all three.
- Try nesting inner classes three levels deep. Walk the chain in a single line and call a method at the deepest level.
- Define a nested class with no `__init__` of its own. Confirm it still works because Python provides a default constructor.
- Build a `LinkedList` class with an inner `Node` class, and implement `push`/`pop` (DSA practice).
- Build a `Database` class with nested `Table` and `Column` inner classes, three levels deep (DBMS practice).
- Build an `HTTPClient` class with an inner `RetryPolicy` that the constructor creates automatically (networking practice).
- Write a `binary_search` function with a nested recursive helper, then time it against an iterative version (DSA practice).
- Write a `deploy_resource` function with a nested `validate_tag` helper, and extend it to reject resources missing an `env` tag (cloud/DevOps practice).