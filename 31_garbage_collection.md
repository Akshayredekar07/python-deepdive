# **Garbage Collection and Destructors**

## **The Problem the Garbage Collector Solves**

A real-life story explains the motivation behind garbage collection:

Imagine a person who takes extremely good care of something they want to keep — but as soon as they need to return it, they completely neglect it. They never give it back.

In C++, the programmer is responsible for both **creating** objects and **destroying** them. This leads to a common class of bugs:

- The programmer forgets to destroy an object → **memory leak**.
- The programmer destroys the same object twice → **double free / crash**.

Languages like Python, Java, and C# solve this by introducing a **Garbage Collector (GC)**. The programmer creates objects, and the runtime automatically destroys them when they are no longer needed.

The basic rule in Python:

**If an object has no reference variable pointing to it, then the object is eligible for the Garbage Collector.**

The programmer's job is **not** to destroy objects — the GC does that. The programmer's job is **only** to make an object eligible for GC when it is no longer required.

### **What This Looks Like in Real Systems**

**Example — DBMS: a leaked connection vs a properly released one**

```python
# The "manual, error-prone" version — like C++, this is what GC saves you from
class RawConnection:
    def __init__(self, dsn):
        print(f"Connection opened: {dsn}")
        self.dsn = dsn

    def close(self):
        print(f"Connection manually closed: {self.dsn}")

conn = RawConnection("postgres://localhost/orders")
# forgot to call conn.close() here -> in C++ this would leak the socket/memory
# in Python, once `conn` has no more references, GC reclaims it automatically
conn = None
print("conn reassigned; Python will reclaim the old object automatically")
```

```
Connection opened: postgres://localhost/orders
conn reassigned; Python will reclaim the old object automatically
```

**Example — Cloud: a client object nobody explicitly destroys**

```python
class S3ClientWrapper:
    def __init__(self, bucket):
        print(f"S3 client created for bucket: {bucket}")
        self.bucket = bucket

def upload_report():
    client = S3ClientWrapper("reports-bucket")
    print(f"Uploading to {client.bucket}")
    # no explicit destroy call needed — once the function returns,
    # `client` goes out of scope and becomes eligible for GC

upload_report()
print("upload_report() finished — client object is now eligible for GC")
```

```
S3 client created for bucket: reports-bucket
Uploading to reports-bucket
upload_report() finished — client object is now eligible for GC
```

## **Enabling and Disabling the Garbage Collector**

The GC is enabled by default. You can check, disable, and re-enable it via the `gc` module.

```python
import gc
print(gc.isenabled())
```

```
True
```

To disable it:

```python
gc.disable()
print(gc.isenabled())
```

```
False
```

To re-enable it:

```python
gc.enable()
print(gc.isenabled())
```

```
True
```

In real code, you almost never touch these settings. The default behaviour is exactly what you want.

### **Real-World Reasons to Touch GC Settings**

**Example — DSA/data processing: disabling GC during a tight bulk-loading loop**

Disabling the cyclic GC temporarily is a known performance trick when creating millions of short-lived objects in a batch job (the cyclic collector's periodic scans add overhead).

```python
import gc

def bulk_load_records(n):
    gc.disable()
    records = []
    for i in range(n):
        records.append({"id": i, "value": i * i})
    gc.enable()
    return records

data = bulk_load_records(5)
print(f"Loaded {len(data)} records, GC re-enabled: {gc.isenabled()}")
```

```
Loaded 5 records, GC re-enabled: True
```

**Example — FastAPI-style: disabling GC around a large startup import job**

```python
import gc

class StartupImporter:
    def __init__(self):
        print("StartupImporter created")

    def run(self, rows):
        gc.disable()
        print(f"Importing {len(rows)} rows with GC paused for speed")
        gc.enable()
        print("Import finished, GC re-enabled")

importer = StartupImporter()
importer.run(["row1", "row2", "row3"])
```

```
StartupImporter created
Importing 3 rows with GC paused for speed
Import finished, GC re-enabled
```

## **Constructor vs Destructor**

Two special methods handle the lifecycle of an object:

| | `__init__(self)` | `__del__(self)` |
|---|---|---|
| Name | Constructor | Destructor |
| When it runs | Just after the object is created. | Just before the object is destroyed by GC. |
| Purpose | Perform initialization of the object. | Perform cleanup activities and resource deallocation. |

The constructor is the "welcome" — it sets things up. The destructor is the "goodbye" — it tears things down. Both are magic methods (also called **dunder methods**) because their names start and end with double underscores.

## **The Destructor in Action**

```python
import time

class Test:
    def __init__(self):
        print("Initilization activity")

    def __del__(self):
        print("Fullfilling last wish and perform cleanup activities")

t = Test()
# t = None   # t is pointing to None, hence Test() is eligible for GC
time.sleep(14)
print("End of application")
```

```
Initilization activity
Fullfilling last wish and perform cleanup activities
End of application
```

The destructor ran at the end of the program, **before** "End of application" was printed. That is the GC's contract: clean up all live objects before the Python Virtual Machine (PVM) shuts down.

### **Force Destruction with `del` or by Reassigning**

You can force the object to become eligible for GC before the program ends. Two common ways:

```python
t = Test()
t = None    # t no longer points to the Test() object
```

```python
t = Test()
del t       # t is removed entirely
# print(t)  # NameError: name 't' is not defined
```

In both cases, the object's reference count drops to zero, and `__del__` runs almost immediately (synchronously, in CPython).

### **Programmer's Responsibility**

The programmer is not responsible to destroy objects explicitly. GC is responsible for this destruction. But the programmer **is** responsible to make an object eligible for GC if it is no longer required.

### **The Destructor Pattern Applied to Real Resources**

**Example — Networking: a socket connection class**

```python
class SocketConnection:
    def __init__(self, host, port):
        print(f"Socket connected to {host}:{port}")
        self.host = host
        self.port = port

    def send(self, data):
        print(f"Sending {data!r} to {self.host}:{self.port}")

    def __del__(self):
        print(f"Socket to {self.host}:{self.port} closed")

conn = SocketConnection("192.168.1.10", 8080)
conn.send("PING")
del conn
```

```
Socket connected to 192.168.1.10:8080
Sending 'PING' to 192.168.1.10:8080
Socket to 192.168.1.10:8080 closed
```

**Example — DBMS: a database connection class**

```python
class DBConnection:
    def __init__(self, dsn):
        print(f"DB connection opened: {dsn}")
        self.dsn = dsn

    def query(self, sql):
        print(f"Running on {self.dsn}: {sql}")

    def __del__(self):
        print(f"DB connection closed: {self.dsn}")

db = DBConnection("mysql://localhost/inventory")
db.query("SELECT * FROM products")
db = None
```

```
DB connection opened: mysql://localhost/inventory
Running on mysql://localhost/inventory: SELECT * FROM products
DB connection closed: mysql://localhost/inventory
```

**Example — OS: a temporary file handler**

```python
class TempFile:
    def __init__(self, path):
        print(f"Temp file created: {path}")
        self.path = path

    def write(self, text):
        print(f"Writing to {self.path}: {text}")

    def __del__(self):
        print(f"Temp file deleted: {self.path}")

tmp = TempFile("/tmp/upload_12345.tmp")
tmp.write("chunk 1")
del tmp
```

```
Temp file created: /tmp/upload_12345.tmp
Writing to /tmp/upload_12345.tmp: chunk 1
Temp file deleted: /tmp/upload_12345.tmp
```

**Example — FastAPI-style: a per-request DB session**

```python
class RequestDBSession:
    def __init__(self, request_id):
        print(f"Session opened for request {request_id}")
        self.request_id = request_id

    def commit(self):
        print(f"Committing changes for request {self.request_id}")

    def __del__(self):
        print(f"Session for request {self.request_id} released back to pool")

def handle_request(request_id):
    session = RequestDBSession(request_id)
    session.commit()
    # once handle_request() returns, `session` goes out of scope

handle_request("req-001")
print("Request handled, session cleaned up automatically")
```

```
Session opened for request req-001
Committing changes for request req-001
Session for request req-001 released back to pool
Request handled, session cleaned up automatically
```

**Example — Cloud: a cloud storage bucket client**

```python
class BucketClient:
    def __init__(self, bucket_name):
        print(f"BucketClient connected: {bucket_name}")
        self.bucket_name = bucket_name

    def upload(self, filename):
        print(f"Uploading {filename} to {self.bucket_name}")

    def __del__(self):
        print(f"BucketClient connection for {self.bucket_name} released")

client = BucketClient("user-uploads")
client.upload("photo.png")
del client
```

```
BucketClient connected: user-uploads
Uploading photo.png to user-uploads
BucketClient connection for user-uploads released
```

## **Demonstrating `__del__` with Multiple Objects**

```python
import time

t1 = Test()
t2 = Test()
time.sleep(10)
print("complete end of application")
```

```
Initilization activity
Fullfilling last wish and perform cleanup activities
Initilization activity
Fullfilling last wish and perform cleanup activities
complete end of application
```

Each `Test()` call creates a new object. At program end, the GC destroys both, so each constructor and destructor pair runs.

### **Multiple Real-World Objects, Same Pattern**

**Example — DSA: multiple cache objects created and destroyed**

```python
class LRUCacheNode:
    def __init__(self, key):
        print(f"Cache node created: {key}")
        self.key = key

    def __del__(self):
        print(f"Cache node evicted: {self.key}")

n1 = LRUCacheNode("user:1")
n2 = LRUCacheNode("user:2")
n1 = None
n2 = None
print("both cache nodes evicted")
```

```
Cache node created: user:1
Cache node created: user:2
Cache node evicted: user:1
Cache node evicted: user:2
both cache nodes evicted
```

**Example — Networking: multiple simultaneous client connections**

```python
class ClientConnection:
    def __init__(self, client_id):
        print(f"Client {client_id} connected")
        self.client_id = client_id

    def __del__(self):
        print(f"Client {self.client_id} disconnected")

c1 = ClientConnection("A")
c2 = ClientConnection("B")
c3 = ClientConnection("C")
del c1
del c2
del c3
```

```
Client A connected
Client B connected
Client C connected
Client A disconnected
Client B disconnected
Client C disconnected
```

**Example — Cloud: multiple worker instances spun up and torn down**

```python
class WorkerInstance:
    def __init__(self, instance_id):
        print(f"Worker {instance_id} started")
        self.instance_id = instance_id

    def __del__(self):
        print(f"Worker {self.instance_id} terminated")

workers = [WorkerInstance(f"w-{i}") for i in range(3)]
workers = None
print("Autoscaler scaled down to zero workers")
```

```
Worker w-0 started
Worker w-1 started
Worker w-2 started
Worker w-0 terminated
Worker w-1 terminated
Worker w-2 terminated
Autoscaler scaled down to zero workers
```

## **Reference Counting — How the GC Knows**

Python uses **reference counting** as its primary GC strategy. An object is destroyed the moment its reference count drops to zero.

### **Multiple References to the Same Object**

```python
import time

t1 = Test()
t2 = t1
t3 = t2

del t1
time.sleep(5)
print("Object not yet destroyed after deleting t1")
```

```
Initilization activity
Object not yet destroyed after deleting t1
```

`del t1` only removed one reference. `t2` and `t3` still point to the object, so it lives on.

```python
del t2
time.sleep(7)
print("Object not yet destroyed after deleting t2")
```

```
Object not yet destroyed after deleting t2
```

Now only `t3` is left.

```python
del t3
time.sleep(7)
print("Last reference will be removed, now object is eligible for GC")
```

```
Fullfilling last wish and perform cleanup activities
Last reference will be removed, now object is eligible for GC
```

The destructor runs the moment the last reference (`t3`) is removed.

The rule, in plain English:

- If no reference variable points to the object → **eligible for GC**.
- If at least one reference variable still points to the object → **not eligible for GC**.

### **Shared References in Real Systems**

**Example — DBMS: a shared connection pool referenced by multiple services**

```python
class SharedPool:
    def __init__(self, name):
        print(f"SharedPool '{name}' created")
        self.name = name

    def __del__(self):
        print(f"SharedPool '{self.name}' destroyed")

pool = SharedPool("orders-pool")
order_service_ref = pool
payment_service_ref = pool

del pool
print("pool variable deleted, but two services still hold references")

del order_service_ref
print("order_service_ref deleted, payment_service_ref still holds it")

del payment_service_ref
print("last reference gone, pool is now destroyed")
```

```
SharedPool 'orders-pool' created
pool variable deleted, but two services still hold references
order_service_ref deleted, payment_service_ref still holds it
SharedPool 'orders-pool' destroyed
last reference gone, pool is now destroyed
```

**Example — Cloud: a shared config object used by several handlers**

```python
class CloudConfig:
    def __init__(self, region):
        print(f"CloudConfig loaded for {region}")
        self.region = region

    def __del__(self):
        print(f"CloudConfig for {self.region} unloaded")

config = CloudConfig("ap-south-1")
handler1_config = config
handler2_config = config

config = None
handler1_config = None
print("still referenced by handler2_config")

handler2_config = None
print("all references gone, config unloaded above")
```

```
CloudConfig loaded for ap-south-1
still referenced by handler2_config
CloudConfig for ap-south-1 unloaded
all references gone, config unloaded above
```

### **Counting References with `sys.getrefcount`**

You can ask Python how many references exist to a particular object. The count is always one higher than you might expect because `getrefcount` itself holds a temporary reference to the object while computing.

```python
import sys

class Test:
    pass

t1 = Test()
t2 = t1
t3 = t2
print(sys.getrefcount(t3))   # 4: t1, t2, t3, and the temporary ref inside getrefcount
```

```
4
```

```python
del t1
print(sys.getrefcount(t3))   # 3
```

```
3
```

Internally, the PVM maintains one extra reference for `self` while a method is running on the object, but that is short-lived and not counted outside of a method call.

### **Reference Counting in Practical Debugging**

**Example — DSA: verifying a node is fully detached from a tree**

```python
import sys

class TreeNode:
    def __init__(self, value):
        self.value = value

root = TreeNode(10)
left_ref = root
print(f"references to root before detaching: {sys.getrefcount(root)}")

left_ref = None
print(f"references to root after detaching one alias: {sys.getrefcount(root)}")
```

```
references to root before detaching: 3
references to root after detaching one alias: 2
```

**Example — Networking: checking if a connection object is still held anywhere**

```python
import sys

class Connection:
    def __init__(self, addr):
        self.addr = addr

conn = Connection("10.0.0.5:443")
pool_entry = conn
print(f"refcount while pooled: {sys.getrefcount(conn)}")

pool_entry = None
print(f"refcount after removing from pool: {sys.getrefcount(conn)}")
```

```
refcount while pooled: 3
refcount after removing from pool: 2
```

## **Lists Holding Multiple Objects**

```python
import time

l = [Test(), Test(), Test()]
time.sleep(4)
print("now this list no longer required...making it eligible for GC")
del l
time.sleep(5)
print("End of application")
```

```
Initilization activity
Initilization activity
Initilization activity
now this list no longer required...making it eligible for GC
Fullfilling last wish and perform cleanup activities
Fullfilling last wish and perform cleanup activities
Fullfilling last wish and perform cleanup activities
End of application
```

Three `Test` objects are created. The list holds references to all three. When the list is deleted, the references inside it are also released, so all three objects become eligible for GC and their destructors run.

### **Lists of Real Resources**

**Example — DBMS: a connection pool implemented as a list**

```python
class PooledConnection:
    def __init__(self, conn_id):
        print(f"PooledConnection {conn_id} opened")
        self.conn_id = conn_id

    def __del__(self):
        print(f"PooledConnection {self.conn_id} closed")

pool = [PooledConnection(i) for i in range(3)]
print("pool ready with 3 connections")
del pool
print("pool shut down, all connections closed")
```

```
PooledConnection 0 opened
PooledConnection 1 opened
PooledConnection 2 opened
pool ready with 3 connections
PooledConnection 0 closed
PooledConnection 1 closed
PooledConnection 2 closed
pool shut down, all connections closed
```

**Example — Networking: a list of open sockets closed together on shutdown**

```python
class OpenSocket:
    def __init__(self, port):
        print(f"Listening on port {port}")
        self.port = port

    def __del__(self):
        print(f"Stopped listening on port {self.port}")

sockets = [OpenSocket(p) for p in (8000, 8001, 8002)]
print("server running on 3 ports")
sockets = []
print("server shutdown complete")
```

```
Listening on port 8000
Listening on port 8001
Listening on port 8002
server running on 3 ports
Stopped listening on port 8000
Stopped listening on port 8001
Stopped listening on port 8002
server shutdown complete
```

**Example — Cloud: a fleet of instances torn down as a list**

```python
class Instance:
    def __init__(self, instance_id):
        print(f"Instance {instance_id} running")
        self.instance_id = instance_id

    def __del__(self):
        print(f"Instance {self.instance_id} terminated")

fleet = [Instance(f"vm-{i}") for i in range(4)]
print("fleet of 4 instances is live")
del fleet
print("fleet terminated by autoscaler")
```

```
Instance vm-0 running
Instance vm-1 running
Instance vm-2 running
Instance vm-3 running
fleet of 4 instances is live
Instance vm-0 terminated
Instance vm-1 terminated
Instance vm-2 terminated
Instance vm-3 terminated
fleet terminated by autoscaler
```

## **Q&A — Common Questions**

### **Q1. What is the difference between `t = None` and `del t`?**

- `t = None` — assigns the value `None` to the variable `t`. The variable `t` still exists, but it now points to the `None` object instead of the original one. The original object loses a reference.
- `del t` — removes the variable `t` itself. After this, `t` is no longer defined. Trying to use it raises `NameError`.

In both cases, if `t` was the only reference to an object, that object becomes eligible for GC. But the variable behaves differently afterwards.

### **Q2. What is the difference between the constructor and the destructor?**

The constructor:

- Name is always `__init__(self)`.
- Runs just after creating an object.
- Performs initialization activities.

The destructor:

- Name is always `__del__(self)`.
- Runs just before destroying an object.
- Performs cleanup activities and resource deallocation.

### **Q3. What are the differences between constructor and destructor?**

A. The job of the constructor is to create an object. **(False — objects are created by `__new__`. The constructor initializes them.)**
B. The job of the constructor is to initialize an object. **(True)**
C. The job of the destructor is to destroy an object. **(False — the GC destroys the object. The destructor performs cleanup.)**
D. The job of the destructor is to perform cleanup activities before destroying an object. **(True)**

**Answer: B and D.**

## **Lifecycle Summary**

The full lifecycle of an object in Python is:

1. **Creation** — `obj = MyClass(...)`. The `__init__` constructor runs.
2. **Usage** — the object is used through its reference variable(s).
3. **Ineligibility** — at some point, the object's reference count drops to zero (variables are reassigned, deleted, or go out of scope).
4. **Cleanup** — the GC sees the count hit zero and calls `__del__`.
5. **Memory release** — the object's memory is returned to the heap.

If the program ends before step 3, the PVM still cleans up: it tears down all remaining objects before shutting down.

## **Try it in Jupyter — Small Examples**

```python
# Example 1: Destructor runs at program end
class Greet:
    def __init__(self, name):
        self.name = name
        print(f"Hello, {name}!")
    def __del__(self):
        print(f"Goodbye, {self.name}!")

g = Greet("Karan")
print("doing work...")
```

```
Hello, Karan!
doing work...
Goodbye, Karan!
```

```python
# Example 2: Reassigning drops the reference
class Box:
    def __init__(self, label):
        self.label = label
        print(f"created {label}")
    def __del__(self):
        print(f"destroyed {self.label}")

b = Box("first")
b = Box("second")    # first is now eligible for GC
```

```
created first
created second
destroyed first
```

```python
# Example 3: List of objects all cleaned up at once
class Item:
    count = 0
    def __init__(self):
        Item.count += 1
        self.id = Item.count
        print(f"created item {self.id}")
    def __del__(self):
        print(f"destroyed item {self.id}")

items = [Item() for _ in range(3)]
print("list built")
del items
print("list deleted")
```

```
created item 1
created item 2
created item 3
list built
list deleted
destroyed item 3
destroyed item 1
destroyed item 2
```

The order of destruction is the reverse of creation in this case, but Python does not guarantee any particular order when destroying multiple objects.

```python
# Example 4: Reference count check
import sys

class A:
    pass

x = A()
print(sys.getrefcount(x))   # 2 (x and the temporary ref)
y = x
print(sys.getrefcount(x))   # 3 (x, y, and the temporary ref)
del y
print(sys.getrefcount(x))   # 2
```

```
2
3
2
```

```python
# Example 5: GC enable / disable check
import gc
print("GC enabled at start:", gc.isenabled())
gc.disable()
print("after disable:", gc.isenabled())
gc.enable()
print("after enable:", gc.isenabled())
```

```
GC enabled at start: True
after disable: False
after enable: True
```

```python
# Example 6: A destructor that does real cleanup work
class FileHandle:
    def __init__(self, path):
        self.path = path
        print(f"opened {path}")
    def write(self, text):
        print(f"writing {text!r} to {self.path}")
    def __del__(self):
        print(f"closed {self.path}")

f = FileHandle("data.txt")
f.write("hello")
del f
```

```
opened data.txt
writing 'hello' to data.txt
closed data.txt
```

In real code, you would use a context manager (`with` statement) instead of relying on `__del__`, because `__del__` is not guaranteed to run at a specific time — it only runs when the object is about to be destroyed. But the principle is the same: clean up resources when the object goes away.

### **More Jupyter-Style Examples — Dev-Flavored**

```python
# Example 7: FastAPI-style — a request-scoped resource cleaned up after handling
class RequestScope:
    def __init__(self, path):
        self.path = path
        print(f"opened request scope for {path}")
    def __del__(self):
        print(f"closed request scope for {self.path}")

def handle(path):
    scope = RequestScope(path)
    print(f"handling {path}")

handle("/api/orders")
print("request finished, scope destroyed above")
```

```
opened request scope for /api/orders
handling /api/orders
request finished, scope destroyed above
closed request scope for /api/orders
```

```python
# Example 8: DSA — a graph node with a destructor that logs eviction from memory
class GraphNode:
    def __init__(self, node_id):
        self.node_id = node_id
        print(f"node {node_id} added to graph")
    def __del__(self):
        print(f"node {self.node_id} removed from graph")

nodes = {i: GraphNode(i) for i in range(3)}
del nodes[1]
print("node 1 explicitly removed")
```

```
node 0 added to graph
node 1 added to graph
node 2 added to graph
node 1 removed from graph
node 1 explicitly removed
```

```python
# Example 9: Networking — reference counting a shared connection across two handlers
import sys

class SharedConnection:
    def __init__(self, addr):
        self.addr = addr

conn = SharedConnection("api.internal:9000")
handler_a = conn
handler_b = conn
print("refcount:", sys.getrefcount(conn))
handler_a = None
handler_b = None
conn = None
print("all handlers released the connection")
```

```
refcount: 4
all handlers released the connection
```

```python
# Example 10: OS — cleaning up a batch of temp files with a list
class TempResource:
    def __init__(self, name):
        self.name = name
        print(f"allocated temp resource {name}")
    def __del__(self):
        print(f"freed temp resource {self.name}")

resources = [TempResource(f"tmp-{i}") for i in range(3)]
print("batch job running")
resources.clear()
print("batch job finished, temp resources freed")
```

```
allocated temp resource tmp-0
allocated temp resource tmp-1
allocated temp resource tmp-2
batch job running
freed temp resource tmp-0
freed temp resource tmp-1
freed temp resource tmp-2
batch job finished, temp resources freed
```

```python
# Example 11: DBMS — a transaction object that rolls back on destruction if not committed
class Transaction:
    def __init__(self, txn_id):
        self.txn_id = txn_id
        self.committed = False
        print(f"transaction {txn_id} started")
    def commit(self):
        self.committed = True
        print(f"transaction {self.txn_id} committed")
    def __del__(self):
        if not self.committed:
            print(f"transaction {self.txn_id} rolled back")
        else:
            print(f"transaction {self.txn_id} cleaned up after commit")

t1 = Transaction("txn-1")
t1.commit()
del t1

t2 = Transaction("txn-2")
del t2   # never committed
```

```
transaction txn-1 started
transaction txn-1 committed
transaction txn-1 cleaned up after commit
transaction txn-2 started
transaction txn-2 rolled back
```

```python
# Example 12: Cloud — a lease-style object that releases a reserved resource on GC
class ReservedGPU:
    def __init__(self, gpu_id):
        self.gpu_id = gpu_id
        print(f"GPU {gpu_id} reserved")
    def __del__(self):
        print(f"GPU {self.gpu_id} released back to the pool")

def run_training_job():
    gpu = ReservedGPU("gpu-7")
    print(f"training on {gpu.gpu_id}")

run_training_job()
print("job finished, GPU released automatically above")
```

```
GPU gpu-7 reserved
training on gpu-7
job finished, GPU released automatically above
GPU gpu-7 released back to the pool
```

## **Quick Reference Summary**

### **Constructor vs Destructor**

| Aspect | `__init__` (Constructor) | `__del__` (Destructor) |
|---|---|---|
| When it runs | Right after object creation. | Right before object destruction. |
| Main purpose | Initialize instance variables. | Cleanup, resource deallocation. |
| Who calls it | Python, automatically, on `ClassName(...)`. | Garbage Collector, automatically, when ref count hits zero. |
| Optional? | Yes — Python provides a default. | Yes — Python provides a default that does nothing. |
| Runs how many times? | Once per object. | Once per object, when the object is destroyed. |

### **GC Eligibility Rules**

| Situation | Eligible for GC? |
|---|---|
| Object has at least one reference variable pointing to it. | No. |
| All reference variables have been reassigned or deleted. | Yes. |
| Object was inside a list, and the list was deleted. | Yes (the list's reference is gone). |
| Function returned, and the local variable held the only reference. | Yes. |
| Program is ending. | All remaining objects are cleaned up before shutdown. |

### **Lifecycle of an Object**

```
[ Created ]  -->  __init__ runs
     |
[ In use ]  -->  methods called, variables hold references
     |
[ Ref count drops to 0 ]
     |
[ __del__ runs ]  -->  cleanup logic
     |
[ Memory released ]
```

### **`t = None` vs `del t`**

| Operation | What happens to `t`? | What happens to the object? |
|---|---|---|
| `t = None` | `t` still exists, now points to `None`. | Loses one reference. May become eligible for GC if this was the last one. |
| `del t` | `t` is removed entirely. Using `t` later raises `NameError`. | Loses one reference. May become eligible for GC if this was the last one. |

### **Where This Shows Up in Real Codebases**

| Domain | Example object whose lifecycle matters |
|---|---|
| FastAPI / backend APIs | Per-request DB session, request-scoped cache entry |
| DSA | Cache/LRU nodes, graph nodes, tree nodes removed from a structure |
| Networking | Socket connections, client connection objects |
| Operating Systems | Temp files, file handles, process handles |
| DBMS | Database connections, connection pools, transactions |
| Cloud / DevOps | Storage clients, worker instances, reserved GPUs/resources |

## **Practice and Next Steps**

- Write a class with both `__init__` and `__del__`. Create an instance, then `del` it. Confirm the destructor runs.
- Write a class and create three objects. Reassign one variable to `None`. Confirm only that object's destructor runs.
- Use `sys.getrefcount` to count references to an object. Add and remove references, and watch the count change.
- Create a list of three objects. Delete the list. Confirm all three destructors run.
- Build a class that represents a file handle. Have `__init__` print "opened" and `__del__` print "closed". Test the lifecycle.
- Try `gc.disable()` and then create an object that becomes eligible for GC. Note that even with GC disabled, CPython's reference counting still frees the object — `gc.disable()` only disables the cyclic GC, not the reference counter.
- Test the difference between `t = None` and `del t`. Use `sys.getrefcount` to observe the effect.
- Write a class where the destructor prints "cleanup done" and the constructor prints "initialized". Time the destructor to run as late as possible.
- Build a `PooledConnection` class and a list-based connection pool (DBMS practice). Delete the pool and confirm every connection's destructor runs.
- Build a `Transaction` class whose destructor rolls back automatically if `commit()` was never called (DBMS/reliability practice).
- Build a `ReservedGPU` or `WorkerInstance` class that releases itself when a function scope ends, and trace the output (cloud/DevOps practice).
- Write a function that opens several `SocketConnection` objects, stores them in a list, and closes them all at once by deleting the list (networking practice).
- Use `sys.getrefcount` to verify that removing a node from a dictionary-based graph (like `GraphNode`) actually drops its reference count to the expected value (DSA practice).