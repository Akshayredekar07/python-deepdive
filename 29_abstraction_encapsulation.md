# **Encapsulation, Abstract Classes and Interfaces**

## **Encapsulation**

Encapsulation is one of the four pillars of OOP (along with inheritance, polymorphism, and abstraction). It is the practice of **bundling data and the methods that operate on that data into a single unit (a class)**, and **restricting direct access to some of the object's components** from outside the class.

In Python, encapsulation is implemented through three visibility levels:

- **Public** — accessible from anywhere.
- **Protected** — a soft convention saying "do not use this from outside".
- **Private** — name-mangled to avoid accidental collision in subclasses.

These three modifiers are explained in detail further down in this file. The bigger umbrella topic — abstract classes and interfaces — is also part of the encapsulation story, because both are tools for defining what should be visible (and what must be implemented) versus what should be hidden.

## **Abstract Method**

An **abstract method** is a method that has a **declaration but no implementation/body**. It is an incomplete method. The implementation is left for child classes to provide.

In Python, abstract methods are declared using the `@abstractmethod` decorator, which lives in the `abc` module.

```python
from abc import abstractmethod
class Vehicle:
    @abstractmethod
    def getNoOfWheels(self):
        pass
```

The body of `getNoOfWheels` is just `pass` — that is the placeholder. The real implementation is the responsibility of any subclass.

### **Q&A on Abstract Methods**

**Q1. What is an abstract method?**

A method that has a declaration but no body. It is incomplete and must be implemented by a subclass.

**Q2. Who is responsible for providing the implementation of an abstract method?**

The child class is responsible for providing the implementation.

**Q3. How do you declare an abstract method?**

By using the `@abstractmethod` decorator.

**Q4. Where is `@abstractmethod` defined?**

It is in the `abc` module. You import it as `from abc import abstractmethod` or `from abc import *`.

**Q5. Can we create the object of an abstract class?**

No. An abstract class with at least one abstract method cannot be instantiated.

**Q6. Can we declare an abstract method in a normal class?**

No. Abstract methods can only live in a class that inherits from `ABC` (or has `metaclass=ABCMeta`).

### **Quick Demo of an Abstract Method**

```python
from abc import abstractmethod
class Vehicle:
    @abstractmethod
    def getNoOfWheels(self):
        pass

class Bus(Vehicle):
    def getNoOfWheels(self):
        return 6

class Auto(Vehicle):
    pass
```

`Bus` provides an implementation, so it can be instantiated. `Auto` does not — it is still abstract and cannot be instantiated.

### **More Abstract Method Examples — Real Software Engineering Contexts**

Each block below is standalone, so you can copy and run any single one on its own.

**FastAPI — repository layer method that every concrete repository must provide**

```python
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int):
        pass
```

**DSA — a stack contract that every stack implementation must satisfy**

```python
from abc import ABC, abstractmethod

class Stack(ABC):
    @abstractmethod
    def push(self, item):
        pass
```

**Networking — a socket handler contract for sending data**

```python
from abc import ABC, abstractmethod

class Connection(ABC):
    @abstractmethod
    def send(self, data: bytes):
        pass
```

**OS — a process scheduler contract**

```python
from abc import ABC, abstractmethod

class Scheduler(ABC):
    @abstractmethod
    def schedule(self, process_id: int):
        pass
```

**DBMS — a query builder contract**

```python
from abc import ABC, abstractmethod

class QueryBuilder(ABC):
    @abstractmethod
    def build(self) -> str:
        pass
```

**Cloud — a deployment contract for infrastructure providers**

```python
from abc import ABC, abstractmethod

class DeploymentTarget(ABC):
    @abstractmethod
    def deploy(self, artifact_path: str):
        pass
```

## **Abstract Class**

An **abstract class** is a class whose implementation is **partially complete or not complete at all**. In Python, every abstract class must be a child of the `ABC` class from the `abc` module. `ABC` stands for **Abstract Base Class**.

```python
from abc import ABC
class Vehicle(ABC):
    @abstractmethod
    def getNoOfWheels(self):
        pass

class Bus(Vehicle):
    def getNoOfWheels(self):
        return 6

class Auto(Vehicle):
    def getNoOfWheels(self):
        return 3

b = Bus()
print(b.getNoOfWheels())
a = Auto()
print(a.getNoOfWheels())
```

```
6
3
```

The hierarchy here:

- `Vehicle` is abstract (it has an abstract method).
- `Bus` and `Auto` are concrete — they implement `getNoOfWheels`.
- `b` and `a` are valid objects of `Bus` and `Auto`.

### **The Relationship Between ABC and `object`**

In Python, every class is — directly or indirectly — a child of `object`. So `class Vehicle(ABC):` is really saying "make `Vehicle` a child of `ABC`, which is itself a child of `object`".

```python
print(Vehicle.__bases__)
```

```
(<class 'abc.ABC'>,)
```

The class `ABC` is provided by Python specifically to mark a class as "this one is allowed to have abstract methods".

### **The Four Cases — When Can We Instantiate?**

This is one of the most useful tables in this file:

| Case | Class design | Can we instantiate? |
|---|---|---|
| 1 | Class does NOT inherit from `ABC` | Yes — it is a concrete class. |
| 2 | Class inherits from `ABC` but has ZERO abstract methods | Yes — instantiation is allowed. |
| 3 | Class inherits from `ABC` and has at least one abstract method, but it is the class itself (not a subclass) | No — `Can't instantiate abstract class ... with abstract method ...`. |
| 4 | Class is a child of an abstract class and provides implementations for all abstract methods | Yes — it has become a concrete class. |

Let us verify each case.

**Case 1 — No ABC, no abstract methods**

```python
from abc import *
class Test:   # concrete class
    pass

t = Test()
print("ok")
```

```
ok
```

**Case 2 — Inherits ABC, but zero abstract methods**

```python
from abc import *
class Test:   # still concrete because it doesn't have ABC parent
    @abstractmethod
    def m1(self):
        pass

t = Test()
```

Wait — this raises a `TypeError` because `Test` does not inherit from `ABC`. The `@abstractmethod` decorator only makes sense inside a class whose metaclass is `ABCMeta`. If the class is not a child of `ABC`, the `@abstractmethod` decoration is silently ignored, but instantiation still requires that the method be implemented. Let me re-demonstrate the actual behavior:

```python
from abc import *
class Test(ABC):     # inherits ABC
    @abstractmethod
    def m1(self):
        print("🚀")

    def m2(self):
        pass

# t = Test()  # TypeError: Can't instantiate abstract class Test with abstract method m1

class Child(Test):    # implements m1
    def m1(self):
        print("Abstract method implemented")

c = Child()
c.m1()
c.m2()
```

```
Abstract method implemented
```

### **Practical Abstract Class with Two Abstract Methods**

```python
from abc import abstractmethod, ABC

class Test(ABC):
    @abstractmethod
    def m1(self):
        pass

    @abstractmethod
    def m2(self):
        pass

    def m3(self):
        print('Hello m3')
        return None

class Child(Test):
    def m1(self):
        print('Hello m1')
        return None

    def m2(self):
        print('Hello m2')
        return None

c = Child()
c.m1()
c.m2()
c.m3()
```

```
Hello m1
Hello m2
Hello m3
```

The child class **must** implement both `m1` and `m2` to be instantiable. The concrete method `m3` is inherited as-is.

### **More Abstract Class Examples — Real Software Engineering Contexts**

Each block is standalone and copy-pasteable on its own.

**FastAPI — a base repository with one abstract method and one shared concrete method**

```python
from abc import ABC, abstractmethod

class BaseRepository(ABC):
    @abstractmethod
    def get_by_id(self, entity_id: int):
        pass

    def log_access(self, entity_id: int):
        print(f"Accessing entity {entity_id}")

class InMemoryUserRepository(BaseRepository):
    def __init__(self):
        self.users = {1: "Akshay", 2: "Neha"}

    def get_by_id(self, entity_id: int):
        self.log_access(entity_id)
        return self.users.get(entity_id)

repo = InMemoryUserRepository()
print(repo.get_by_id(1))
```

```
Accessing entity 1
Akshay
```

**DSA — an abstract sorting algorithm with a shared helper and one abstract step**

```python
from abc import ABC, abstractmethod

class SortAlgorithm(ABC):
    @abstractmethod
    def sort(self, arr: list) -> list:
        pass

    def is_sorted(self, arr: list) -> bool:
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

class BubbleSort(SortAlgorithm):
    def sort(self, arr: list) -> list:
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

data = [5, 2, 9, 1]
sorter = BubbleSort()
result = sorter.sort(data)
print(result)
print(sorter.is_sorted(result))
```

```
[1, 2, 5, 9]
True
```

**Networking — an abstract protocol handler with a shared logging method**

```python
from abc import ABC, abstractmethod

class ProtocolHandler(ABC):
    @abstractmethod
    def handle_packet(self, packet: bytes):
        pass

    def log_packet_size(self, packet: bytes):
        print(f"Packet size: {len(packet)} bytes")

class HttpHandler(ProtocolHandler):
    def handle_packet(self, packet: bytes):
        self.log_packet_size(packet)
        print("Parsing as HTTP request")

handler = HttpHandler()
handler.handle_packet(b"GET / HTTP/1.1")
```

```
Packet size: 14 bytes
Parsing as HTTP request
```

**OS — an abstract process manager with a shared utility method**

```python
from abc import ABC, abstractmethod

class ProcessManager(ABC):
    @abstractmethod
    def create_process(self, name: str):
        pass

    def list_running(self, processes: list):
        for p in processes:
            print(f"Running: {p}")

class LinuxProcessManager(ProcessManager):
    def create_process(self, name: str):
        print(f"Forking process: {name}")
        return name

manager = LinuxProcessManager()
pid = manager.create_process("worker")
manager.list_running([pid])
```

```
Forking process: worker
Running: worker
```

**Cloud — an abstract cloud resource with a shared tagging method**

```python
from abc import ABC, abstractmethod

class CloudResource(ABC):
    @abstractmethod
    def provision(self):
        pass

    def apply_tags(self, tags: dict):
        print(f"Applying tags: {tags}")

class VirtualMachine(CloudResource):
    def provision(self):
        print("Provisioning virtual machine...")

vm = VirtualMachine()
vm.provision()
vm.apply_tags({"env": "staging"})
```

```
Provisioning virtual machine...
Applying tags: {'env': 'staging'}
```

## **Interfaces in Python**

In general, **if an abstract class contains only abstract methods, it is considered an interface**. A 100% pure abstract class (no concrete methods, no instance variables) is the Pythonic equivalent of a Java interface.

Any requirement specification — a set of method names that must be implemented — is considered an interface.

```python
from abc import *
class CollegeAutomationSystem(ABC):
    @abstractmethod
    def getStudentsMarks(self):
        pass

    @abstractmethod
    def updateStudentMarks(self):
        pass

class DurgaSoft(CollegeAutomationSystem):
    def getStudentsMarks(self):
        print("getStudentMarks Executing")

    def updateStudentMarks(self):
        print("updateStudentMarks Executing")

d = DurgaSoft()
d.getStudentsMarks()
d.updateStudentMarks()
```

```
getStudentMarks Executing
updateStudentMarks Executing
```

### **Interface vs Abstract Class vs Concrete Class**

| Type | What it is | Can it be instantiated? | What it contains | When to use |
|---|---|---|---|---|
| **Interface** | A pure abstract class | No (incomplete) | Only abstract methods, only constants | You only know the *requirements*, not the implementation. |
| **Abstract class** | A partially implemented class | No (incomplete) | Abstract methods + concrete methods + state | You have *some* implementation, but parts are left to children. |
| **Concrete class** | A fully implemented class | Yes | All methods implemented | You have the *complete* implementation, ready to use. |

The decision rule:

- If you do not know **anything** about the implementation, just the requirement specification → use an **interface**.
- If you have **partial** implementation → use an **abstract class**.
- If you have **complete** implementation, ready to provide service → use a **concrete class**.

### **Real-World Example — Database Connectivity**

A classic interface use case: different database backends, same operations.

```python
from abc import ABC, abstractmethod

class DBInterface(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

class Oracle(DBInterface):
    def connect(self):
        print('Connecting to Oracle Database...')

    def disconnect(self):
        print('Disconnecting to Oracle Database...')

class Sybase(DBInterface):
    def connect(self):
        print('Connecting to Sybase Database...')

    def disconnect(self):
        print('Disconnecting to Sybase Database...')

dbname = input('Enter Database Name:')
if dbname == 'Oracle':
    x = Oracle()
elif dbname == 'Sybase':
    x = Sybase()
else:
    raise ValueError(f"Unsupported database name: {dbname}")

x.connect()
x.disconnect()
```

```
Connecting to Oracle Database...
Disconnecting to Oracle Database...
```

The client code (`x.connect(); x.disconnect()`) does not know or care which database it is talking to. That is the point of an interface.

### **Real-World Example — Printer**

A configuration-driven version that picks a printer class at runtime based on a config file:

```python
from abc import ABC, abstractmethod

class Printer(ABC):
    @abstractmethod
    def printit(self, text):
        pass

    @abstractmethod
    def disconnect(self):
        pass

class EPSON(Printer):
    def printit(self, text):
        print('Printing from EPSON Printer...')
        print(text)

    def disconnect(self):
        print('Printing completed on EPSON Printer...')

class HP(Printer):
    def printit(self, text):
        print('Printing from HP Printer...')
        print(text)

    def disconnect(self):
        print('Printing completed on HP Printer...')

try:
    with open('config.txt', 'r') as f:
        pname = f.readline().strip()
    classname = globals()[pname]
    x = classname()
    x.printit('This data has to print...')
    x.disconnect()
except FileNotFoundError:
    print("The file 'config.txt' does not exist.")
except KeyError:
    print(f"Unsupported printer name: {pname}")
```

```
Printing from HP Printer...
This data has to print...
Printing completed on HP Printer...
```

`globals()[pname]` converts a string like `"HP"` into the actual class object `HP`, then instantiates it. This is the same pattern used in plugin systems and dependency-injection containers.

### **Layered Implementation Pattern**

A common shape: a base interface, a partial implementation, and a final concrete class.

```python
from abc import ABC, abstractmethod

class CollegeAutomation(ABC):
    @abstractmethod
    def m1(self):
        pass

    @abstractmethod
    def m2(self):
        pass

    @abstractmethod
    def m3(self):
        pass

class AbsCls(CollegeAutomation):
    def m1(self):
        print('m1 method implementation')

    def m2(self):
        print('m2 method implementation')

class ConcreteCls(AbsCls):
    def m3(self):
        print('m3 method implementation')

c = ConcreteCls()
c.m1()
c.m2()
c.m3()
```

```
m1 method implementation
m2 method implementation
m3 method implementation
```

This is exactly how frameworks like Django, FastAPI, and SQLAlchemy are organized. The framework provides an abstract base, you implement one or two methods, and the framework fills in the rest.

### **More Interface Examples — Real Software Engineering Contexts**

Each block is standalone and copy-pasteable on its own.

**FastAPI — a notification interface with two channel implementations**

```python
from abc import ABC, abstractmethod

class NotificationService(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str):
        pass

class EmailNotification(NotificationService):
    def send(self, recipient: str, message: str):
        print(f"Sending email to {recipient}: {message}")

class SmsNotification(NotificationService):
    def send(self, recipient: str, message: str):
        print(f"Sending SMS to {recipient}: {message}")

channel = "email"
service = EmailNotification() if channel == "email" else SmsNotification()
service.send("akshay@example.com", "Your order shipped")
```

```
Sending email to akshay@example.com: Your order shipped
```

**DSA — a cache interface with two eviction strategies**

```python
from abc import ABC, abstractmethod

class Cache(ABC):
    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def put(self, key, value):
        pass

class LRUCache(Cache):
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.store = {}

    def get(self, key):
        return self.store.get(key, -1)

    def put(self, key, value):
        if len(self.store) >= self.capacity:
            oldest_key = next(iter(self.store))
            del self.store[oldest_key]
        self.store[key] = value

cache = LRUCache(2)
cache.put("a", 1)
cache.put("b", 2)
print(cache.get("a"))
```

```
1
```

**Networking — a socket client interface for TCP and UDP**

```python
from abc import ABC, abstractmethod

class SocketClient(ABC):
    @abstractmethod
    def connect(self, host: str, port: int):
        pass

    @abstractmethod
    def close(self):
        pass

class TcpClient(SocketClient):
    def connect(self, host: str, port: int):
        print(f"Opening TCP connection to {host}:{port}")

    def close(self):
        print("Closing TCP connection")

class UdpClient(SocketClient):
    def connect(self, host: str, port: int):
        print(f"Sending UDP datagram target set to {host}:{port}")

    def close(self):
        print("Releasing UDP socket")

client = TcpClient()
client.connect("127.0.0.1", 8080)
client.close()
```

```
Opening TCP connection to 127.0.0.1:8080
Closing TCP connection
```

**DBMS — a connection interface for two SQL backends**

```python
from abc import ABC, abstractmethod

class SQLConnection(ABC):
    @abstractmethod
    def execute(self, query: str):
        pass

class PostgresConnection(SQLConnection):
    def execute(self, query: str):
        print(f"Running on Postgres: {query}")

class MySQLConnection(SQLConnection):
    def execute(self, query: str):
        print(f"Running on MySQL: {query}")

db_type = "postgres"
conn = PostgresConnection() if db_type == "postgres" else MySQLConnection()
conn.execute("SELECT * FROM students")
```

```
Running on Postgres: SELECT * FROM students
```

**Cloud — a storage interface for three providers**

```python
from abc import ABC, abstractmethod

class CloudStorage(ABC):
    @abstractmethod
    def upload(self, file_name: str):
        pass

    @abstractmethod
    def download(self, file_name: str):
        pass

class S3Storage(CloudStorage):
    def upload(self, file_name: str):
        print(f"Uploading {file_name} to S3")

    def download(self, file_name: str):
        print(f"Downloading {file_name} from S3")

class GCSStorage(CloudStorage):
    def upload(self, file_name: str):
        print(f"Uploading {file_name} to Google Cloud Storage")

    def download(self, file_name: str):
        print(f"Downloading {file_name} from Google Cloud Storage")

provider_name = "S3Storage"
provider = globals()[provider_name]()
provider.upload("report.csv")
```

```
Uploading report.csv to S3
```

## **Public, Protected and Private Attributes**

Python does not enforce access control the way Java or C++ does. There is no `private` keyword that actually hides a variable. What Python has are **conventions** — three styles, each with a different "please don't touch this" level.

### **Public Attributes**

Public attributes have no prefix. They are accessible from anywhere — inside the class, from a subclass, from outside the class.

```python
class Example:
    def __init__(self):
        self.public_attr = "I am public"

example = Example()
print(example.public_attr)   # Accessing public attribute
```

```
I am public
```

Public attributes are the default and should be used for anything that is part of the class's normal interface.

### **More Public Attribute Examples — Real Software Engineering Contexts**

**FastAPI — a public request model field**

```python
class CreateOrderRequest:
    def __init__(self, item_name: str, quantity: int):
        self.item_name = item_name
        self.quantity = quantity

req = CreateOrderRequest("Keyboard", 2)
print(req.item_name)
print(req.quantity)
```

```
Keyboard
2
```

**DSA — a public node value in a linked list**

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

n = Node(10)
print(n.value)
```

```
10
```

**Networking — a public host and port on a request object**

```python
class HttpRequest:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

req = HttpRequest("api.example.com", 443)
print(req.host, req.port)
```

```
api.example.com 443
```

**OS — a public process name**

```python
class Process:
    def __init__(self, name: str, pid: int):
        self.name = name
        self.pid = pid

p = Process("worker", 4521)
print(p.name, p.pid)
```

```
worker 4521
```

### **Protected Attributes**

Protected attributes have a **single underscore** prefix (`_protected_attr`). They are not meant to be accessed outside the class and its subclasses. The single underscore is a **theoretical convention, not enforced** by Python — the attribute is still accessible from anywhere, but linters and human reviewers will flag it.

```python
class Base:
    def __init__(self):
        self._protected_attr = "I am protected"

class Derived(Base):
    def access_protected(self):
        return self._protected_attr   # Accessing protected attribute

derived = Derived()
print(derived.access_protected())
```

```
I am protected
```

### **More Protected Attribute Examples — Real Software Engineering Contexts**

**FastAPI — a protected config value used by subclasses of a settings base**

```python
class BaseSettings:
    def __init__(self):
        self._db_url = "postgresql://localhost:5432/app"

class DevSettings(BaseSettings):
    def show_db_url(self):
        return self._db_url

settings = DevSettings()
print(settings.show_db_url())
```

```
postgresql://localhost:5432/app
```

**DSA — a protected internal list backing a queue**

```python
class Queue:
    def __init__(self):
        self._items = []

class PriorityQueue(Queue):
    def add(self, item):
        self._items.append(item)
        self._items.sort()

pq = PriorityQueue()
pq.add(5)
pq.add(1)
print(pq._items)
```

```
[1, 5]
```

**Networking — a protected retry count used by subclasses**

```python
class BaseClient:
    def __init__(self):
        self._retry_count = 3

class ResilientClient(BaseClient):
    def show_retries(self):
        return self._retry_count

client = ResilientClient()
print(client.show_retries())
```

```
3
```

**OS — a protected scheduler queue used by subclasses**

```python
class BaseScheduler:
    def __init__(self):
        self._ready_queue = []

class RoundRobinScheduler(BaseScheduler):
    def add_process(self, pid: int):
        self._ready_queue.append(pid)

scheduler = RoundRobinScheduler()
scheduler.add_process(101)
print(scheduler._ready_queue)
```

```
[101]
```

### **Private Attributes**

Private attributes have a **double underscore** prefix (`__private_attr`). They are only meant to be accessible within the class itself. Python enforces this through a mechanism called **name mangling** — the interpreter rewrites the name to `_ClassName__attribute`. The attribute is still reachable if you know the mangled name, but it is hidden from normal attribute access.

```python
class Example:
    def __init__(self):
        self.__private_attr = "I am private"

    def get_private_attr(self):
        return self.__private_attr

example = Example()
print(example.get_private_attr())   # correct way to access private attribute
# print(example.__private_attr)     # AttributeError
```

```
I am private
```

### **More Private Attribute Examples — Real Software Engineering Contexts**

**FastAPI — a private token hidden behind a getter method**

```python
class AuthSession:
    def __init__(self, token: str):
        self.__token = token

    def get_token(self):
        return self.__token

session = AuthSession("abc123")
print(session.get_token())
```

```
abc123
```

**DSA — a private internal array in a custom Stack**

```python
class Stack:
    def __init__(self):
        self.__items = []

    def push(self, item):
        self.__items.append(item)

    def peek(self):
        return self.__items[-1]

s = Stack()
s.push(10)
s.push(20)
print(s.peek())
```

```
20
```

**Networking — a private checksum on a packet**

```python
class Packet:
    def __init__(self, data: bytes):
        self.data = data
        self.__checksum = sum(data) % 256

    def get_checksum(self):
        return self.__checksum

pkt = Packet(b"hello")
print(pkt.get_checksum())
```

```
50
```

**DBMS — private credentials on a connection pool**

```python
class ConnectionPool:
    def __init__(self, username: str, password: str):
        self.__username = username
        self.__password = password

    def connect(self):
        print(f"Connecting as {self.__username}")

pool = ConnectionPool("admin", "secret")
pool.connect()
```

```
Connecting as admin
```

### **A Class With All Three Visibility Levels**

```python
class Test:
    def __init__(self) -> None:
        self.x = 10          # public variable

    def m1(self):
        print("Public method m1")

    def m2(self):
        print(self.x)
        self.m1()

t = Test()
print(t.x)
t.m1()
```

```
10
Public method m1
```

`x` and `m1` are public — accessible from anywhere.

### **Private Members — The Naming Convention in Detail**

```python
class Test:
    def __init__(self) -> None:
        self.__x = 10        # private member

    def __m1(self):
        print("Private m1 method")

    def m2(self):
        print(self.__x)
        self.__m1()

t = Test()
try:
    print(t.__x)
    t.__m1()
except AttributeError as e:
    print(f"Error accessing private member: {e}")
```

```
Error accessing private member: 'Test' object has no attribute '__x'
```

For every private member, **name mangling** happens at runtime:

- `__x` becomes `_Test__x`
- `__m1` becomes `_Test__m1`

You can still reach them by the mangled name:

```python
class Test:
    def __init__(self) -> None:
        self.__y = 20

    def __m1(self):
        print('Private method')

    def __m2(self):
        print(self.__y)
        self.m1()

t = Test()
print(t._Test__y)
t._Test__m1()
```

```
20
Private method
```

This proves that "private" in Python is not security — it is just a name-mangling mechanism to avoid accidental collisions.

### **Protected Members — A Simple Demonstration**

```python
class P:
    def __init__(self) -> None:
        self._x = 10    # protected member

    def m1(self):
        print(self._x)

class C(P):
    def m2(self):
        print(self._x)

c = C()
print(c._x)            # still works — convention only
```

```
10
```

Remember: **a single underscore is a theoretical convention, not an implementation-level access modifier** in Python. Java has a hard rule; Python does not.

## **Data Hiding**

Data hiding is the practice of keeping an object's internal data private so that no external code can directly read or modify it. The principle is simple: **our internal data should not directly leave our system**.

Real-world analogies:

- To check your email, you need a username and password — not direct access to the email database.
- An ICICI bank customer needs a customer ID and password — not direct access to the bank's internal ledger.

Data hiding is the *intent*. The Pythonic way to implement it is by combining **private attributes** (`__attr`) with **controlled access methods** (often via `@property`).

```python
class Account:
    def __init__(self, initialBalance) -> None:
        self.__balance = initialBalance

    def getBalance(self):
        # validation
        name = input("Enter your name:")
        pasw = input("Enter your pass:")
        if name == "durga" and pasw == "python":
            return self.__balance
        else:
            return "You have not access to this account."

a = Account(1000)
print(a.getBalance())
```

```
You have not access to this account.
```

The actual `__balance` is hidden. Reading it requires going through `getBalance()`, which enforces a check before returning the value. This is the data-hiding pattern at work.

### **Why Data Hiding Matters**

- **Security** — sensitive data is never directly exposed.
- **Validation** — any access goes through a method that can enforce rules.
- **Maintainability** — if the internal storage changes (e.g., a balance field becomes a list of transactions), only the methods need to change, not the external code that calls them.

### **More Data Hiding Examples — Real Software Engineering Contexts**

Each block is standalone and copy-pasteable on its own.

**FastAPI — hiding a password hash behind a property, exposing only safe fields**

```python
class User:
    def __init__(self, username: str, password_hash: str):
        self.username = username
        self.__password_hash = password_hash

    @property
    def password_hash(self):
        return "***hidden***"

user = User("akshay", "9f8e7d6c5b4a")
print(user.username)
print(user.password_hash)
```

```
akshay
***hidden***
```

**DSA — hiding the internal list of a Stack so callers cannot mutate it directly**

```python
class Stack:
    def __init__(self):
        self.__items = []

    def push(self, item):
        self.__items.append(item)

    def pop(self):
        return self.__items.pop() if self.__items else None

    def size(self):
        return len(self.__items)

s = Stack()
s.push(1)
s.push(2)
print(s.size())
print(s.pop())
```

```
2
2
```

**Networking — hiding a session token, exposing only an is_valid check**

```python
class Session:
    def __init__(self, token: str):
        self.__token = token

    def is_valid(self):
        return len(self.__token) > 0

session = Session("xyz-789")
print(session.is_valid())
```

```
True
```

**OS — hiding a raw file descriptor behind a read method**

```python
class FileHandle:
    def __init__(self, fd: int):
        self.__fd = fd

    def read(self):
        return f"Reading from fd {self.__fd}"

handle = FileHandle(7)
print(handle.read())
```

```
Reading from fd 7
```

**Cloud — hiding a secret access key, exposing only a masked identifier**

```python
class CloudCredentials:
    def __init__(self, access_key: str, secret_key: str):
        self.access_key = access_key
        self.__secret_key = secret_key

    def masked_secret(self):
        return "*" * (len(self.__secret_key) - 4) + self.__secret_key[-4:]

creds = CloudCredentials("AKIA123", "supersecretvalue")
print(creds.access_key)
print(creds.masked_secret())
```

```
AKIA123
************alue
```

## **Quick Reference Summary**

### **Abstract Method vs Abstract Class vs Interface**

| Concept | Definition | Key requirement | When to use |
|---|---|---|---|
| Abstract method | Method with declaration but no body | Marked with `@abstractmethod` | When the implementation is unknown and child must provide it. |
| Abstract class | A class that has at least one abstract method, or inherits from `ABC` | Must inherit from `ABC` | When the implementation is partially known. |
| Interface | A 100% pure abstract class (only abstract methods) | Must inherit from `ABC` and have no concrete methods | When only the requirements are known. |

### **Visibility Levels in Python**

| Style | Prefix | Effect | When to use |
|---|---|---|---|
| Public | (none) | Always accessible | Normal attributes and methods. |
| Protected | `_` | Convention "do not use from outside" | Internal helpers, methods subclasses may override. |
| Private | `__` | Name-mangled to `_ClassName__attr` | Attributes that should not clash with subclass attributes. |
| Read-only | `__attr` + `@property` (no setter) | Read from outside, write only inside | Balance fields, IDs, anything users should not reassign. |

### **When to Use Which — A Decision Matrix**

| Need | Use |
|---|---|
| You only have requirements, no implementation | Interface (pure abstract class). |
| You have partial implementation | Abstract class. |
| You have full implementation | Concrete class. |
| Attribute is part of normal API | Public. |
| Attribute is for internal use / subclasses | Protected. |
| Attribute must not be accessible from outside at all | Private (combined with `@property` for controlled access). |

### **Try it in Jupyter — Small Examples**

```python
# Example 1: A simple abstract class
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side * self.side

print(Square(4).area())
```

```
16
```

```python
# Example 2: Cannot instantiate abstract class
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

# a = Animal()  # TypeError if uncommented
class Dog(Animal):
    def speak(self):
        return "Woof"

print(Dog().speak())
```

```
Woof
```

```python
# Example 3: Private attribute via name mangling
class Secret:
    def __init__(self):
        self.__code = 1234

s = Secret()
print(s._Secret__code)   # the real name
# print(s.__code)        # AttributeError
```

```
1234
```

```python
# Example 4: Data hiding with @property
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

acc = BankAccount(500)
print(acc.balance)
# acc.balance = 1000   # AttributeError
# acc.__balance        # AttributeError
```

```
500
```

```python
# Example 5: Layered abstraction
from abc import ABC, abstractmethod

class Report(ABC):
    @abstractmethod
    def format(self, data):
        pass

class JsonReport(Report):
    def format(self, data):
        import json
        return json.dumps(data)

class PrettyJsonReport(JsonReport):
    def format(self, data):
        return "  " + super().format(data).replace(",", ",\n  ")

print(PrettyJsonReport().format({"a": 1, "b": 2}))
```

```
  {"a": 1,
  "b": 2}
```

## **Practice and Next Steps**

- Create an abstract class `Animal` with an abstract method `sound()`. Implement two concrete classes `Dog` and `Cat`.
- Create an interface `Payment` with abstract methods `pay()` and `refund()`. Implement `CardPayment` and `UpiPayment`.
- Build a layered structure: interface `Shape` → abstract class `Polygon` (implements one method) → concrete class `Triangle`.
- Try instantiating an abstract class. Observe the `TypeError`. Then implement the abstract method and confirm the class becomes instantiable.
- Create a class with a private attribute. Try to access it from outside, then access it via the mangled name.
- Create a class with a protected attribute. Access it from a child class to confirm it is allowed.
- Build a `BankAccount` with a private `__balance` field and a `@property` called `balance` that returns it. Try setting `balance` from outside and observe the `AttributeError`.
- Implement a small plugin system using an interface and the `globals()` trick — pick a class by name from a config string.