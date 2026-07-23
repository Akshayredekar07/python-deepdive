# **OOP Part 1: Foundations**

## **Classes and Objects**

In Python, everything is an object. To create objects, you need a model or a blueprint, which is a **class**. A class can contain:

- **Variables** (also called attributes or properties) — the data an object holds.
- **Methods** (also called functions inside a class) — the actions an object can perform.

```python
class Student:
    ''' This is a student class with required data '''
    def __init__(self, name, rollno, marks):
        self.name = name
        self.rollno = rollno
        self.marks = marks

    def talk(self):
        print("Hello My Name is:", self.name)
        print("My Rollno is:", self.rollno)
        print("My Marks are:", self.marks)
```

The triple-quoted string just below the class header is a **docstring**. It is optional, but writing one is a good habit. You can read it back with `print(Student.__doc__)` or `help(Student)`.

The physical existence of a class is an **object**. You can create any number of objects for one class. The variable that holds the object is called a **reference variable**, because it lets you reach the object's data and methods.

```python
s1 = Student("Durga", 101, 80)
s1.talk()
```

```
Hello My Name is: Durga
My Rollno is: 101
My Marks are: 80
```

`Student("Durga", 101, 80)` creates the object. `s1` is the reference variable. `s1.talk()` calls the method on that object.

### **Examples**

```python
# Example 1: A Point in 2D
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(3, 4)
print(p.x, p.y)
```

```
3 4
```

```python
# Example 2: A Book with a method
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def summary(self):
        return f"'{self.title}' by {self.author}, {self.pages} pages"

b = Book("Dune", "Frank Herbert", 412)
print(b.summary())
```

```
'Dune' by Frank Herbert, 412 pages
```

```python
# Example 3: A Rectangle that computes its area
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

r = Rectangle(5, 3)
print("area =", r.area())
```

```
area = 15
```

```python
# Example 4: Class with docstring and help()
class Animal:
    """A simple animal class for demo purposes."""
    def __init__(self, species, sound):
        self.species = species
        self.sound = sound

a = Animal("dog", "woof")
print(Animal.__doc__)
help(Animal)
```

```
A simple animal class for demo purposes.
Help on class Animal in module __main__:

class Animal(builtins.object)
 |  A simple animal class for demo purposes.
 |  ...
```

```python
# Example 5: Multiple objects, same class
class Lamp:
    def __init__(self, color):
        self.color = color

    def glow(self):
        return f"The {self.color} lamp is glowing"

l1 = Lamp("red")
l2 = Lamp("blue")
l3 = Lamp("green")
print(l1.glow())
print(l2.glow())
print(l3.glow())
```

```
The red lamp is glowing
The blue lamp is glowing
The green lamp is glowing
```

## **The `self` Variable**

`self` is the default name Python uses for the parameter that points to the **current object** — the one on which a method is being called. It works like `this` in Java or C++.

Two rules to follow:

- `self` should be the first parameter of the constructor: `def __init__(self):`.
- `self` should be the first parameter of every instance method: `def talk(self):`.

The name `self` is a convention, not a keyword. You could call it `this` or `me`, but every Python developer and linter expects `self`, so do not rename it.

### **Examples**

```python
# Example 1: self is the current object
class Demo:
    def __init__(self, value):
        self.value = value

    def show(self):
        print("value =", self.value)
        print("id of self =", id(self))

d = Demo(42)
d.show()
print("id of d =", id(d))
# Both ids match — self inside the method IS d outside.
```

```
value = 42
id of self = 140234567891200
id of d = 140234567891200
```

```python
# Example 2: Methods that return self (for chaining)
class Builder:
    def __init__(self):
        self.text = ""

    def add(self, chunk):
        self.text += chunk
        return self

    def upper(self):
        self.text = self.text.upper()
        return self

b = Builder()
result = b.add("hello ").add("world").upper()
print(result.text)
```

```
HELLO WORLD
```

```python
# Example 3: self vs other objects of the same class
class Counter:
    def __init__(self, start=0):
        self.count = start

    def increment(self):
        self.count += 1

a = Counter(10)
b = Counter(100)
a.increment()
a.increment()
b.increment()
print("a =", a.count)
print("b =", b.count)
# self in a.increment() is a, self in b.increment() is b.
```

```
a = 12
b = 101
```

```python
# Example 4: Renaming self (not recommended, but allowed)
class Weird:
    def __init__(banana, x):  # banana works like self
        banana.x = x
    def show(banana):
        print(banana.x)

w = Weird(7)
w.show()
# Don't do this in real code. Convention is self.
```

```
7
```

```python
# Example 5: self is not passed automatically when calling on the class
class Helper:
    def greet(self, name):
        return f"Hi {name}, I'm {self}"

h = Helper()
print(h.greet("Virat"))   # works
# print(Helper.greet("Virat"))  # TypeError: missing 1 required positional argument: 'self'
```

```
Hi Virat, I'm <__main__.Helper object at 0x...>
```

## **Constructors (`__init__`)**

A **constructor** is a special method whose name is always `__init__`. It is run automatically by Python the moment you create an object. The main job of the constructor is to **declare and initialize the instance variables** for that object.

The simplest constructor:

```python
class Test:
    def __init__(self):
        print("constructor executed!")

t1 = Test()
t2 = Test()
```

```
constructor executed!
constructor executed!
```

Each `Test()` call creates a new object, and each one runs the constructor. So the print runs once per object, automatically.

### **Constructor That Takes Arguments**

A constructor almost always takes arguments so the caller can pass in the data for that specific object. The arguments get assigned to instance variables through `self`:

```python
class Student:
    def __init__(self, name, rollnum, marks):
        self.name = name
        self.rollnum = rollnum
        self.marks = marks

s1 = Student("virat", 18, 100)
print(s1.name, s1.rollnum, s1.marks)
```

```
virat 18 100
```

`s1` is now a `Student` object with its own `name`, `rollnum`, and `marks`. A second `Student("rohit", 45, 95)` would create a completely separate object with its own values.

### **The Ten Rules About Constructors**

These are the points to keep in your head for constructors in Python:

1. A constructor is a special method.
2. The constructor is always named `__init__`.
3. You never have to call the constructor yourself. Python runs it the moment you write `ClassName(...)`.
4. For each object, the constructor runs exactly once.
5. The main job of the constructor is to declare and initialize instance variables.
6. A constructor always takes at least one argument, and that argument is `self`.
7. Within a Python class, the constructor is **optional**. If you do not write one, Python's virtual machine (PVM) provides a default one.
8. You *can* call the constructor explicitly. When you do, it behaves like a normal method on the existing object — no new object is created.
9. Python does **not** support constructor overloading the way Java does. If you write more than one `__init__` in the same class, only the last one survives.
10. The constructor and a normal method are not the same thing, even if the names look similar. A method named `Test` (no underscores) is just a regular method, not a constructor.

### **Rule 7 in Action: The Default Constructor**

```python
class Test:
    def m1(self):
        print("This is valid")

t = Test()
```

`m1` is a regular method, but no `__init__` is defined. Python quietly provides a default `__init__(self)` so `Test()` works.

### **Rule 8 in Action: Calling the Constructor Explicitly**

```python
class Test:
    def __init__(self):
        print(f"Constructor execution! with id {id(self)}")

t = Test()
t.__init__()
t.__init__()
```

```
Constructor execution! with id 3028624611920
Constructor execution! with id 3028624611920
Constructor execution! with id 3028624611920
```

Notice the `id(self)` is the same every time. Each call ran the constructor on the *same* object `t`. No new object was created. Compare to a regular method call: it has to be triggered with `()` and runs the same way.

### **Rule 9 in Action: Python Does Not Overload Constructors**

```python
class Test:
    def __init__(self):
        print("No-arg constructor!")

    def __init__(self, x):
        print("One-arg constructor!")
```

Trying `Test()` now raises:

```
TypeError: Test.__init__() missing 1 required positional argument: 'x'
```

Python does not look at the previous `__init__`. It keeps the *last* one and ignores the others. This is one of the biggest differences from Java. If you want different "ways" to construct an object in Python, the standard answer is **default arguments** or **classmethod factory methods**, both covered in the methods section below.

### **Rule 10 in Action: A Method Named `Test` Is Not a Constructor**

```python
class Test:
    def Test(self):
        print("Special method!")

t = Test()
```

Creating `t` runs the default `__init__`, not the method `Test`. You have to call the method yourself:

```python
t.Test()
```

```
Special method!
```

### **Method vs Constructor — Side by Side**

| Method | Constructor |
|---|---|
| Name can be anything | Name is always `__init__` |
| Does not run on its own; you must call it | Runs automatically when you create an object |
| Can be called any number of times on the same object | Runs only once per object |
| Holds business logic (what the object does) | Holds instance-variable setup (what the object is) |

### **Real-World Example: A Movie Class**

```python
class Movie:
    def __init__(self, title, actor, actress):
        self.title = title
        self.actor = actor
        self.actress = actress

    def movie_info(self):
        print("\nMovie name:", self.title)
        print("Actor name:", self.actor)
        print("Actress name:", self.actress)
```

This pattern (constructor for setup, regular method for behavior) is what you will see in almost every real Python class — a Django model, a Pydantic schema, a SQLAlchemy ORM class, a request handler in FastAPI. The constructor collects the data; the methods use it.

### **Examples**

```python
# Example 1: Constructor with default values
class User:
    def __init__(self, name, role="viewer", active=True):
        self.name = name
        self.role = role
        self.active = active

u1 = User("Karan")
u2 = User("Drishya", "admin")
u3 = User("Om", "editor", False)
print(u1.name, u1.role, u1.active)
print(u2.name, u2.role, u2.active)
print(u3.name, u3.role, u3.active)
```

```
Karan viewer True
Drishya admin True
Om editor False
```

```python
# Example 2: Constructor with *args (variable positional)
class Team:
    def __init__(self, name, *members):
        self.name = name
        self.members = list(members)

t = Team("Backend", "Karan", "Om", "Harsha")
print(t.name, t.members)
```

```
Backend ['Karan', 'Om', 'Harsha']
```

```python
# Example 3: Constructor with **kwargs (variable keyword)
class Config:
    def __init__(self, **options):
        self.options = options

c = Config(host="localhost", port=5432, debug=True)
print(c.options)
print(c.options["host"])
```

```
{'host': 'localhost', 'port': 5432, 'debug': True}
localhost
```

```python
# Example 4: Chained constructor calls with defaults
class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

p1 = Point()
p2 = Point(5)
p3 = Point(5, 9)
print(p1, p2, p3)
```

```
Point(0, 0) Point(5, 0) Point(5, 9)
```

```python
# Example 5: Constructor that does setup work
class DatabaseConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connected = True
        print(f"Connected to {self.host}:{self.port}")

db = DatabaseConnection("localhost", 5432)
db.connected
```

```
Connected to localhost:5432
True
```

```python
# Example 6: Reusing a constructor with explicit call
class Box:
    def __init__(self, length=1, width=1, height=1):
        self.length = length
        self.width = width
        self.height = height
    def volume(self):
        return self.length * self.width * self.height

b = Box(2, 3, 4)
print("first volume =", b.volume())
b.__init__(10, 10, 10)   # reset the same object
print("second volume =", b.volume())
```

```
first volume = 24
second volume = 1000
```

```python
# Example 7: Multiple __init__ — only the last one wins
class Bad:
    def __init__(self):
        self.a = 1
    def __init__(self, x):
        self.a = x

# Bad()        # TypeError: missing 1 required positional argument: 'x'
b = Bad(5)
print(b.a)
```

```
5
```

```python
# Example 8: Factory via classmethod instead of constructor overloading
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    def __repr__(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"

    @classmethod
    def from_string(cls, text):
        y, m, d = text.split("-")
        return cls(int(y), int(m), int(d))

d1 = Date(2025, 4, 12)
d2 = Date.from_string("2025-04-12")
print(d1, d2)
```

```
2025-04-12 2025-04-12
```

## **Types of Variables**

Inside a Python class, three kinds of variables are allowed:

1. **Instance variables** (object-level) — value changes from object to object.
2. **Static variables** (class-level) — value is shared across all objects.
3. **Local variables** (method-level) — value lives only while the method runs.

### **Instance Variables (Object-Level)**

If the value of a variable is different for every object, that variable is an instance variable. Each object gets its **own separate copy**. The usual place to define one is inside the constructor using `self`, but there are three valid places.

#### **Where to Declare Instance Variables**

1. **Inside the constructor** by using `self`. Runs every time an object is created.
2. **Inside an instance method** by using `self`. Only added when the method is called.
3. **Outside the class** by using an object reference. Added on demand from outside the class.

```python
class Test:
    def __init__(self):
        self.a = 10
        self.b = 20

    def m1(self):
        self.c = 30

t = Test()
print(t.__dict__)
t.m1()
print(t.__dict__)
t.d = 40
t.f = 50
print(t.__dict__)
```

```
{'a': 10, 'b': 20}
{'a': 10, 'b': 20, 'c': 30}
{'a': 10, 'b': 20, 'c': 30, 'd': 40, 'f': 50}
```

`__dict__` is a quick way to inspect what instance variables an object currently has. It returns a regular Python dictionary.

#### **How to Access Instance Variables**

- **Inside the class**: use `self`.
- **Outside the class**: use the object reference.

```python
class Test:
    def __init__(self):
        self.a = 10
        self.b = 20

    def m1(self):
        print(self.a)
        print(self.b)

t = Test()
t.m1()
print(t.a, t.b)
```

```
10
20
10 20
```

#### **How to Delete Instance Variables**

- **Inside the class**: `del self.variableName`.
- **Outside the class**: `del objectReference.variableName`.

```python
class Test:
    def __init__(self):
        self.a = 10
        self.b = 20
        self.c = 30
        self.d = 40

    def m1(self):
        del self.d

t = Test()
print(t.__dict__)
t.m1()
print(t.__dict__)
del t.c
print(t.__dict__)
del t.c, t.a
print(t.__dict__)
```

```
{'a': 10, 'b': 20, 'c': 30, 'd': 40}
{'a': 10, 'b': 20, 'c': 30}
{'a': 10, 'b': 20}
{}
```

Deleting an instance variable on one object does **not** affect other objects. Each one keeps its own copy.

```python
class Test:
    def __init__(self):
        self.a = 10
        self.b = 20
        self.c = 30
        self.d = 40

t1 = Test()
t1.m1 = lambda: None
del t1.a
print(t1.__dict__)
t2 = Test()
print(t2.__dict__)
```

```
{'b': 20, 'c': 30, 'd': 40}
{'a': 10, 'b': 20, 'c': 30, 'd': 40}
```

`del t1.a` only removes `a` from `t1`. `t2` still has its own `a`.

#### **Instance Variables Are Per-Object**

```python
class Test:
    def __init__(self):
        self.a = 10
        self.b = 20

t1 = Test()
t1.a = 888
t1.b = 999
t2 = Test()
print('t1:', t1.a, t1.b)
print('t2:', t2.a, t2.b)
```

```
t1: 888 999
t2: 10 20
```

This is the single most important property of instance variables — they belong to one object, not to the class. Same logic applies in any framework that wraps Python objects: an attribute you set on a Django model instance does not appear on a different one.

### **Examples**

```python
# Example 1: Declaring instance variables in 3 places
class Bag:
    def __init__(self):
        self.color = "red"     # place 1: in the constructor

    def add_item(self, item):
        self.last_item = item  # place 2: in an instance method

b = Bag()
b.brand = "Nike"             # place 3: outside the class
b.add_item("pen")
print(b.__dict__)
```

```
{'color': 'red', 'last_item': 'pen', 'brand': 'Nike'}
```

```python
# Example 2: Each object gets its own copy
class Car:
    def __init__(self, model, speed):
        self.model = model
        self.speed = speed

c1 = Car("Tesla", 200)
c2 = Car("BMW", 240)
c1.speed = 150
print(c1.model, c1.speed)
print(c2.model, c2.speed)
```

```
Tesla 150
BMW 240
```

```python
# Example 3: Access from inside and outside
class Profile:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        return f"I am {self.name}, {self.age} years old"

p = Profile("Karan", 22)
print(p.introduce())   # inside, using self
print(p.name, p.age)   # outside, using object reference
```

```
I am Karan, 22 years old
Karan 22
```

```python
# Example 4: Delete instance variables
class Box:
    def __init__(self, a, b, c, d):
        self.a, self.b, self.c, self.d = a, b, c, d

b = Box(1, 2, 3, 4)
del b.c
print(b.__dict__)
del b.a, b.b
print(b.__dict__)
```

```
{'a': 1, 'b': 2, 'd': 4}
{'d': 4}
```

```python
# Example 5: Deleting on one object does not affect another
class Settings:
    def __init__(self):
        self.theme = "dark"
        self.lang = "en"

s1 = Settings()
s2 = Settings()
del s1.theme
print(s1.__dict__)
print(s2.__dict__)
```

```
{'lang': 'en'}
{'theme': 'dark', 'lang': 'en'}
```

```python
# Example 6: Real-world — a User profile
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.login_count = 0     # starts at 0

    def login(self):
        self.login_count += 1

u1 = User("karan", "k@x.com")
u2 = User("om", "o@x.com")
u1.login()
u1.login()
u2.login()
print(u1.username, u1.login_count)
print(u2.username, u2.login_count)
```

```
karan 2
om 1
```

### **Static Variables (Class-Level)**

If a value does not change from object to object, it should be a static variable. The class itself holds **one copy**, and every object reads from that same copy.

Most static variables are declared inside the class body but **outside any method**.

```python
class Test:
    a = 10
    def __init__(self):
        self.b = 20
```

#### **Where to Declare Static Variables**

- Within the class directly, outside any method.
- Inside the constructor, using the class name.
- Inside an instance method, using the class name.
- Inside a class method, using either the class name or `cls`.
- Inside a static method, using the class name.
- Outside the class, using the class name.

```python
class Test:
    a = 10
    def __init__(self):
        Test.b = 20
        Test.c = 34

    def m1(self):
        Test.d = 44

    @classmethod
    def m2(cls):
        Test.k = 67
        cls.p = 91

    @staticmethod
    def m3():
        Test.s = 77

t = Test()
t.m1()
Test.m2()
Test.m3()
Test.f = 60
print(Test.__dict__)
```

`Test.__dict__` shows the class-level namespace. Your own variables appear alongside the default dunder attributes (`__module__`, `__init__`, `__dict__`, `__weakref__`, `__doc__`).

#### **How to Access Static Variables**

Static variables are visible from anywhere:

- Inside a constructor: `self.a` or `Test.a`.
- Inside an instance method: `self.a` or `Test.a`.
- Inside a class method: `cls.a` or `Test.a`.
- Inside a static method: `Test.a` (no `self` or `cls` here).
- Outside the class: `Test.a` or `object.a`.

```python
class MyClass:
    static_variable = "I am static"

    def instance_method(self):
        print("Accessing via self:", self.static_variable)

    @classmethod
    def class_method(cls):
        print("Accessing via cls:", cls.static_variable)

    @staticmethod
    def static_method():
        print("Accessing via class name:", MyClass.static_variable)

obj = MyClass()
obj.instance_method()
MyClass.class_method()
MyClass.static_method()
print("Access via object reference:", obj.static_variable)
```

```
Accessing via self: I am static
Accessing via cls: I am static
Accessing via class name: I am static
Access via object reference: I am static
```

#### **How to Update Static Variables — and the Big Gotcha**

Static variables can only be updated through the **class name** or `cls` (inside a class method). If you try to update them with `self` or an object reference, you do **not** change the class-level value — you create a brand-new instance variable that shadows the static one for that one object.

```python
class Test:
    a = 10
    @classmethod
    def m1(cls):
        cls.a = 20

    @staticmethod
    def m2():
        Test.a = 30

t = Test()
Test.m1()
Test.m2()
print(Test.a)
```

```
30
```

The rule, summarized:

- You can **declare** a static variable with class name, cls, self, or an object reference.
- You can only **update** a static variable with class name or cls.
- You can only **delete** a static variable with class name or cls.

The shadowing trap in detail:

```python
class Test:
    a = 10
    def m1(self):
        self.a = 888

t1 = Test()
t1.m1()
print(Test.a)   # class-level static variable
print(t1.a)     # instance variable on t1
```

```
10
888
```

`t1.a = 888` did not change `Test.a`; it created `t1.a` and the instance variable wins when you read `t1.a`. The class variable is still `10`.

The same trap in another form:

```python
class Test:
    a = 10
    def m1(self):
        print(self.a)
        self.a = 888
        print(self.a)

    def m2(self):
        print(Test.a)

t = Test()
t.m1()
t.m2()
```

```
10
888
10
```

Inside `m1`, the first `print` reads the class variable through `self.a` (because no instance variable exists yet). After the assignment, `self.a` is the new instance variable. `m2` reads the still-untouched class variable through `Test.a`.

#### **How to Delete Static Variables**

```python
class Test:
    a = 10
    @classmethod
    def m1(cls):
        del cls.a

print(Test.__dict__)
Test.m1()
print(Test.__dict__)
```

A bigger example that puts every place together:

```python
class Test:
    a = 10
    def __init__(self):
        Test.b = 20
        del Test.a

    def m1(self):
        Test.c = 30
        del Test.b

    @classmethod
    def m2(cls):
        cls.d = 40

    @staticmethod
    def m3():
        Test.e = 50
        del Test.d

t = Test()
t.m1()
Test.m2()
Test.m3()
Test.f = 60
del Test.e
print(Test.__dict__)
```

If you try to delete a static variable through an object reference, you get an `AttributeError` because the object only has instance variables.

#### **Instance vs Static — The Whole Picture**

```python
class Test:
    x = 10
    def __init__(self):
        self.y = 20

t1 = Test()
t2 = Test()
print('t1:', t1.x, t1.y)
print('t2:', t2.x, t2.y)
Test.x = 888
t1.y = 999
print('t1:', t1.x, t1.y)
print('t2:', t2.x, t2.y)
```

```
t1: 10 20
t2: 10 20
t1: 888 999
t2: 888 20
```

What this shows:

- `x` is the class variable. Both `t1.x` and `t2.x` start at `10`.
- Setting `Test.x = 888` updates the class variable, so both `t1.x` and `t2.x` now read `888`.
- Setting `t1.y = 999` only affects `t1`. `t2.y` stays `20`.

### **Examples**

```python
# Example 1: Simple static variable shared by everyone
class Player:
    max_speed = 10   # class level

    def __init__(self, name):
        self.name = name

p1 = Player("Karan")
p2 = Player("Om")
print(p1.max_speed, p2.max_speed)
Player.max_speed = 12
print(p1.max_speed, p2.max_speed)
```

```
10 10
12 12
```

```python
# Example 2: Access static via 4 ways
class C:
    s = 100

    def __init__(self):
        print("ctor via self:", self.s, "via class:", C.s)

    def m(self):
        print("m via self:", self.s, "via class:", C.s)

    @classmethod
    def cm(cls):
        print("cm via cls:", cls.s, "via class:", C.s)

    @staticmethod
    def sm():
        print("sm via class:", C.s)

c = C()
c.m()
C.cm()
C.sm()
print("outside via obj:", c.s, "via class:", C.s)
```

```
ctor via self: 100 via class: 100
m via self: 100 via class: 100
cm via cls: 100 via class: 100
sm via class: 100
outside via obj: 100 via class: 100
```

```python
# Example 3: Update via class name — everyone sees the change
class Counter:
    total = 0
    def __init__(self):
        Counter.total += 1

a = Counter()
b = Counter()
c = Counter()
print(Counter.total)
```

```
3
```

```python
# Example 4: The shadow trap when using self
class Trap:
    value = 10
    def set_bad(self, v):
        self.value = v    # creates an instance variable, does not change the class

t = Trap()
t.set_bad(99)
print("Trap.value =", Trap.value)   # still 10
print("t.value    =", t.value)      # 99
```

```
Trap.value = 10
t.value    = 99
```

```python
# Example 5: Update via class method using cls
class Settings:
    debug = False
    @classmethod
    def enable_debug(cls):
        cls.debug = True

print(Settings.debug)
Settings.enable_debug()
print(Settings.debug)
```

```
False
True
```

```python
# Example 6: Static variable used as a constant
class Math:
    PI = 3.14159
    E = 2.71828

print(Math.PI)
print(Math.E)
```

```
3.14159
2.71828
```

```python
# Example 7: Real-world — app-wide config
class AppConfig:
    APP_NAME = "MyApp"
    VERSION = "1.0.0"
    MAX_USERS = 100

print(AppConfig.APP_NAME, AppConfig.VERSION, AppConfig.MAX_USERS)
```

```
MyApp 1.0.0 100
```

### **Local Variables (Method-Level)**

A variable declared inside a method is a local variable. It is created when the method starts, destroyed when the method returns, and **cannot be accessed from outside the method**.

```python
class Test:
    def m1(self):
        a = 1000
        print(a)

    def m2(self):
        b = 2000
        print(b)

t = Test()
t.m1()
t.m2()
```

```
1000
2000
```

The next example shows the scope rule:

```python
class Test:
    def m1(self):
        a = 1000
        print(a)

    def m2(self):
        b = 2000
        print(a)   # a was local to m1, not visible here
        print(b)

t = Test()
t.m1()
t.m2()
```

```
1000
NameError: name 'a' is not defined
```

Local variables in Python are subject to the same scoping rules as anywhere else — they live and die inside their function. Using `self.a = ...` would have made it an instance variable instead, visible across the whole class.

### **Examples**

```python
# Example 1: Local variable does not leak out
def helper():
    secret = 42
    return secret

print(helper())
# print(secret)   # NameError if uncommented
```

```
42
```

```python
# Example 2: Two methods, two independent locals
class Calc:
    def add(self, x, y):
        result = x + y      # local
        return result
    def mul(self, x, y):
        result = x * y      # local, same name, different method
        return result

c = Calc()
print(c.add(3, 4))
print(c.mul(3, 4))
```

```
7
12
```

```python
# Example 3: Loop variable inside a method is also local
class Sum:
    def total(self, numbers):
        s = 0           # local
        for n in numbers:
            s += n
        return s

print(Sum().total([1, 2, 3, 4, 5]))
```

```
15
```

```python
# Example 4: Local vs instance variable name collision
class Demo:
    def m(self, x):
        temp = x            # local
        self.temp = x * 2   # instance variable (different name? no — same!)
        return temp

d = Demo()
print(d.m(5))
print(d.__dict__)
```

```
5
{'temp': 10}
```

```python
# Example 5: Trying to use a local in another method (NameError)
class Scope:
    def set(self, v):
        flag = v
    def get(self):
        return flag    # flag was local to set, not visible here

s = Scope()
s.set(1)
# s.get()   # NameError: name 'flag' is not defined
```

```
[will raise NameError if uncommented]
```

### **Real-World Example: A Bank Customer**

This combines all three variable types. The bank name is the same for every customer (static), the customer name and balance are unique per customer (instance), and the deposit/withdraw methods do temporary arithmetic (local).

```python
import sys

class Customer:
    bankname = "Durga Bank"

    def __init__(self, name, balance=0.0):
        self.name = name
        self.balance = balance

    def deposit(self, amt):
        self.balance += amt
        print(f"Balance after deposit: {self.balance}")

    def withdraw(self, amt):
        if amt > self.balance:
            print("Insufficient balance. Please try again!")
            sys.exit()
        self.balance -= amt
        print(f"Balance after withdrawal: {self.balance}")

    def checkbalance(self):
        print(f"Your current balance is {self.balance}")

print(f"Welcome to {Customer.bankname}")
name = input("Enter your name: ")
c = Customer(name)

while True:
    print('d - Deposit\nw - Withdraw\np - CheckBalance\ne - Exit')
    option = input("Choose an option: ").strip().lower()

    if option == 'p':
        c.checkbalance()
    elif option == 'd':
        amount = float(input("Enter amount to deposit: "))
        c.deposit(amount)
    elif option == 'w':
        amount = float(input("Enter amount to withdraw: "))
        c.withdraw(amount)
    elif option == 'e':
        print("Thanks for Banking!")
        sys.exit()
    else:
        print("Invalid option. Please try again.")
```

What to notice in this example:

- `bankname` is a static variable — every customer sees the same name, and changing `Customer.bankname` would update it for everyone.
- `self.name` and `self.balance` are instance variables — each `Customer` has its own.
- Inside `deposit`, `amt` and the temporary `self.balance + amt` are local to that call.
- The class can be used as the single source of truth for shared settings (`bankname`) and the right place to put utility methods that touch one customer at a time.

## **Types of Methods**

Python has three kinds of methods inside a class:

1. **Instance methods** — operate on a specific object. First parameter is `self`.
2. **Class methods** — operate on the class itself. First parameter is `cls`. Decorated with `@classmethod`.
3. **Static methods** — independent utility functions. No `self`, no `cls`. Decorated with `@staticmethod`.

### **Instance Methods**

If the method uses at least one instance variable (with or without using static variables), it is an instance method.

```python
class Student:
    def __init__(self, x, y):
        self.name = x
        self.branch = y

    def student_info(self):
        print("Student name:", self.name)
        print("Student branch:", self.branch)

s1 = Student("Durga", 23)
s1.student_info()
```

```
Student name: Durga
Student branch: 23
```

- First parameter: `self`, the current object.
- No decorator.
- Called using the object reference.

### **Examples**

```python
# Example 1: Simple instance method
class Greeter:
    def __init__(self, name):
        self.name = name
    def hello(self):
        return f"Hello, {self.name}!"

g = Greeter("Karan")
print(g.hello())
```

```
Hello, Karan!
```

```python
# Example 2: Method that uses multiple instance variables
class Wallet:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
    def add(self, amount):
        self.balance += amount
    def spend(self, amount):
        if amount > self.balance:
            return "Not enough money"
        self.balance -= amount
        return f"{self.owner} now has {self.balance}"

w = Wallet("Om", 100)
w.add(50)
print(w.spend(30))
print(w.spend(200))
```

```
Om now has 120
Not enough money
```

```python
# Example 3: Method that calls another method using self
class Counter:
    def __init__(self):
        self.value = 0
    def increment(self):
        self.value += 1
    def increment_twice(self):
        self.increment()
        self.increment()

c = Counter()
c.increment_twice()
print(c.value)
```

```
2
```

```python
# Example 4: Method that returns a value derived from instance data
class Rectangle:
    def __init__(self, w, h):
        self.w = w
        self.h = h
    def area(self):
        return self.w * self.h
    def perimeter(self):
        return 2 * (self.w + self.h)

r = Rectangle(4, 5)
print(r.area(), r.perimeter())
```

```
20 18
```

```python
# Example 5: Real-world — a Cart total
class Cart:
    def __init__(self):
        self.items = []
    def add(self, name, price):
        self.items.append((name, price))
    def total(self):
        return sum(price for _, price in self.items)

cart = Cart()
cart.add("Book", 250)
cart.add("Pen", 20)
cart.add("Bag", 700)
print("Total =", cart.total())
```

```
Total = 970
```

### **Class Methods**

If the method uses only static (class-level) variables and not any instance variables, it should be a class method. Class methods are decorated with `@classmethod`, and their first parameter is `cls`, which refers to the class object.

```python
class Test:
    @classmethod
    def m1(cls):
        print(id(cls))

    @classmethod
    def m2(cls):
        print(id(cls))

print(id(Test))
Test.m1()
Test.m2()
```

```
2897417868688
2897417868688
2897417868688
```

`cls` is `Test` itself. The variable name `cls` is a convention; any name works, but `cls` is what everyone uses.

A more useful class method example:

```python
class Student:
    college_name = "SpaceX"
    director = "Elon Musk"

    def __init__(self, x, y):
        self.name = x
        self.branch = y

    @classmethod
    def college_info(cls):
        print("College Name:", cls.college_name)
        print("Director Name:", cls.director)

s = Student("Durga", "CS")
s.college_info()
```

```
College Name: SpaceX
Director Name: Elon Musk
```

Notice `college_info` uses `cls.college_name`, not `Student.college_name`. That makes it a real class method — if you ever subclass `Student`, the same method will pick up the subclass's `college_name`.

A pattern that shows up constantly in real Python: an object counter.

```python
class Test:
    count = 0

    def __init__(self):
        Test.count += 1

    @classmethod
    def getNoOfObjects(cls):
        print("Total no of objects created:", cls.count)

t1 = Test()
t2 = Test()
t3 = Test()
Test.getNoOfObjects()
```

```
Total no of objects created: 3
```

This is the same pattern used by SQLAlchemy, Django ORM, pytest plugins, and many other frameworks to track their internal state.

### **Examples**

```python
# Example 1: Class method as alternative constructor
class Date:
    def __init__(self, year, month, day):
        self.year, self.month, self.day = year, month, day
    def __repr__(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"

    @classmethod
    def from_string(cls, text):
        y, m, d = text.split("-")
        return cls(int(y), int(m), int(d))

d = Date.from_string("2025-04-12")
print(d)
```

```
2025-04-12
```

```python
# Example 2: Class method that uses cls (subclass-friendly)
class Animal:
    species = "unknown"
    @classmethod
    def describe(cls):
        return f"I am a {cls.species}"

class Dog(Animal):
    species = "dog"

class Cat(Animal):
    species = "cat"

print(Dog.describe())
print(Cat.describe())
# cls resolves to Dog or Cat at call time
```

```
I am a dog
I am a cat
```

```python
# Example 3: Object counter with class method
class Sensor:
    count = 0
    def __init__(self, name):
        self.name = name
        Sensor.count += 1
    @classmethod
    def how_many(cls):
        return cls.count

s1 = Sensor("temp")
s2 = Sensor("humidity")
s3 = Sensor("pressure")
print(Sensor.how_many())
```

```
3
```

```python
# Example 4: Class method as a settings reader
class App:
    name = "MyApp"
    version = "1.0"
    @classmethod
    def banner(cls):
        return f"{cls.name} v{cls.version}"

print(App.banner())
```

```
MyApp v1.0
```

```python
# Example 5: Using cls to build a new object
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    @classmethod
    def origin(cls):
        return cls(0, 0)
    def __repr__(self):
        return f"({self.x}, {self.y})"

print(Point.origin())
print(Point(3, 4))
```

```
(0, 0)
(3, 4)
```

```python
# Example 6: Real-world — CSV row to dict constructor
class Row:
    def __init__(self, name, age, city):
        self.name = name
        self.age = age
        self.city = city
    def __repr__(self):
        return f"Row({self.name}, {self.age}, {self.city})"

    @classmethod
    def from_csv(cls, line):
        name, age, city = line.split(",")
        return cls(name, int(age), city)

print(Row.from_csv("Karan,22,Mumbai"))
```

```
Row(Karan, 22, Mumbai)
```

### **Static Methods**

If the method uses neither instance variables nor class variables — just local variables — it is a general utility. Declare it as a static method with `@staticmethod`.

```python
class Student:
    college_name = "SpaceX"
    director = "Elon Musk"

    def __init__(self, x, y):
        self.name = x
        self.branch = y

    def student_info(self):
        print("Student name:", self.name)
        print("Student branch:", self.branch)

    @classmethod
    def college_info(cls):
        print("College Name:", cls.college_name)
        print("Director Name:", cls.director)

    @staticmethod
    def get_avg(x, y, z):
        return (x + y + z) / 3

s = Student("Durga", "CS")
print(s.get_avg(45, 67, 23))
```

```
45.0
```

- No `self`, no `cls`.
- `@staticmethod` decorator (recommended for clarity, but technically optional).
- Called by class name or object reference.

A common backend use: a small helper that just does a calculation.

```python
class Calculations:
    @staticmethod
    def add(x, y):
        print("The sum:", x + y)

    @staticmethod
    def product(x, y):
        print("Product of nums:", x * y)

    @staticmethod
    def avg(x, y):
        print("The avg of numbers:", (x + y) / 2)

Calculations.add(43, 51)
Calculations.product(45, 76)
```

```
The sum: 94
Product of nums: 3420
```

### **Examples**

```python
# Example 1: Pure math helper
class Math:
    @staticmethod
    def square(n):
        return n * n
    @staticmethod
    def is_even(n):
        return n % 2 == 0

print(Math.square(7))
print(Math.is_even(10))
```

```
49
True
```

```python
# Example 2: A small validation helper
class Validator:
    @staticmethod
    def is_email(s):
        return "@" in s and "." in s
    @staticmethod
    def is_strong_password(s):
        return len(s) >= 8 and any(c.isdigit() for c in s)

print(Validator.is_email("k@x.com"))
print(Validator.is_strong_password("abc"))
```

```
True
False
```

```python
# Example 3: String utility namespace
class Str:
    @staticmethod
    def is_palindrome(s):
        return s == s[::-1]
    @staticmethod
    def reverse_words(s):
        return " ".join(s.split()[::-1])

print(Str.is_palindrome("level"))
print(Str.reverse_words("hello world python"))
```

```
True
python world hello
```

```python
# Example 4: Grouping related functions under a class
class Temperature:
    @staticmethod
    def c_to_f(c):
        return c * 9 / 5 + 32
    @staticmethod
    def f_to_c(f):
        return (f - 32) * 5 / 9

print(Temperature.c_to_f(100))
print(Temperature.f_to_c(32))
```

```
212.0
0.0
```

```python
# Example 5: Real-world — simple ID generator
class IdGen:
    @staticmethod
    def make_id(prefix):
        import random
        return f"{prefix}-{random.randint(1000, 9999)}"

print(IdGen.make_id("ORD"))
print(IdGen.make_id("USR"))
```

```
ORD-4731
USR-2018
```

```python
# Example 6: Calling a static method from inside an instance method
class Order:
    TAX_RATE = 0.18   # static
    def __init__(self, amount):
        self.amount = amount
    def final_price(self):
        tax = Order._compute_tax(self.amount)   # calling a static from an instance method
        return self.amount + tax
    @staticmethod
    def _compute_tax(amount):
        return amount * Order.TAX_RATE

o = Order(1000)
print(o.final_price())
```

```
1180.0
```

### **Decision Matrix — Which Method Should I Write?**

Look at the variables the method needs. The right method is determined by the **variables it touches**, not the decorators.

| Variables used | Method type | Decorator | First arg |
|---|---|---|---|
| Only instance variables | Instance method | (none) | `self` |
| Instance + static + local | Instance method | (none) | `self` |
| Instance + local | Instance method | (none) | `self` |
| Only static + local | Class method | `@classmethod` | `cls` |
| Only static | Class method | `@classmethod` | `cls` |
| Only local | Static method | `@staticmethod` | (none) |

The shorthand version:

- "If I need `self`, it is an instance method."
- "If I need `cls` only, it is a class method."
- "If I need neither, it is a static method."

### **A Class Without a Decorator — What Happens?**

If you write a method without `@staticmethod` and without `@classmethod`, it is an instance method by default. Python will pass the object as the first argument. Calling it by the class name works only because Python will not pass an object in that case.

```python
class MyClass:
    def ambiguous_method():
        print("This could be static or instance")

MyClass.ambiguous_method()    # works like a static call
obj = MyClass()
# obj.ambiguous_method()      # TypeError: takes 0 positional arguments but 1 was given
```

A static method is what you actually want here:

```python
class MyClass:
    @staticmethod
    def static_method():
        print("This is a static method")

MyClass.static_method()
obj = MyClass()
obj.static_method()
```

```
This is a static method
This is a static method
```

This pattern is rare. Most of the time you will write `@staticmethod` explicitly, and your linter or IDE will remind you if you forget.

### **Real-World Example: File Utilities as a Class**

Static methods are a clean way to group related functions under one namespace.

```python
class FileUtils:
    @staticmethod
    def read_file(file_path):
        with open(file_path, 'r') as f:
            return f.read()

    @staticmethod
    def write_file(file_path, content):
        with open(file_path, 'w') as f:
            f.write(content)

FileUtils.write_file("example.txt", "Hello, world!")
print(FileUtils.read_file("example.txt"))
```

```
Hello, world!
```

This is one of the patterns used by `pathlib.Path`, the `os` module, and many utility libraries — a class is the natural namespace for related functions, even when it never needs an instance.

## **Getters and Setters**

A **getter** returns the value of an instance variable. A **setter** sets the value. They are useful when:

- You do not have the data at the time of object creation (so a constructor is awkward).
- You want to validate the value before storing it.
- You want read-only access to a field from outside the class.

The basic version:

```python
class Student:
    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_marks(self, marks):
        self.marks = marks

    def get_marks(self):
        return self.marks

n = int(input("Enter the number of students: "))
students = []
for i in range(n):
    s = Student()
    name = input("Enter Student name: ")
    s.set_name(name)
    marks = float(input("Enter your marks: "))
    s.set_marks(marks)
    students.append(s)

for s in students:
    print("Hi", s.get_name(), ", your marks are", s.get_marks())
```

```
Hi karan, your marks are 56.0
Hi Varun, your marks are 78.0
```

A common pattern with validation inside the setter:

```python
class Student:
    def set_marks(self, marks):
        if not 0 <= marks <= 100:
            raise ValueError("marks must be between 0 and 100")
        self.marks = marks

    def get_marks(self):
        return self.marks
```

### **The Pythonic Way: `@property`**

Python's `@property` decorator turns a method into an attribute that is accessed like a regular variable, but it still runs a method under the hood. The benefit is that the calling code stays clean, while you keep the validation, computed values, and read-only control.

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self):
        return 3.14 * self._radius ** 2

circle = Circle(5)
print(circle.radius)    # 5 — getter
circle.radius = 10      # setter with validation
print(circle.area)      # 314.0 — computed from current radius
```

```
5
314.0
```

Things to notice:

- `circle.radius` looks like attribute access, but it calls `radius()` behind the scenes.
- `circle.radius = 10` looks like assignment, but it actually calls the setter, so negative values are rejected.
- `circle.area` is read-only — there is no `area.setter`, so trying `circle.area = ...` raises `AttributeError`.

### **When to Use Getters vs Setters vs Constructor**

- **Constructor**: when you know the data at object creation time, and it is required.
- **Setter**: when the data may not be available at creation time, or when you need validation.
- **Getter**: when other code needs to read the value, or when the value is computed from other state.
- **`@property`**: when you want a method to look like an attribute from the outside (read-only or validated).

### **Examples**

```python
# Example 1: Simple setter with validation
class Person:
    def __init__(self, name):
        self.name = name
    def set_age(self, age):
        if age < 0:
            raise ValueError("age cannot be negative")
        self.age = age
    def get_age(self):
        return self.age

p = Person("Karan")
p.set_age(22)
print(p.get_age())
# p.set_age(-1)   # ValueError if uncommented
```

```
22
```

```python
# Example 2: @property with read-only computed value
class Square:
    def __init__(self, side):
        self.side = side
    @property
    def area(self):
        return self.side * self.side
    @property
    def perimeter(self):
        return 4 * self.side

s = Square(5)
print(s.area, s.perimeter)
```

```
25 20
```

```python
# Example 3: @property with setter that validates
class Email:
    def __init__(self, value):
        self._value = value
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, new):
        if "@" not in new:
            raise ValueError("not a valid email")
        self._value = new

e = Email("k@x.com")
e.value = "new@x.com"
print(e.value)
# e.value = "no-at-sign"   # ValueError if uncommented
```

```
new@x.com
```

```python
# Example 4: A temperature class with bounds
class Temperature:
    def __init__(self, celsius):
        self._c = celsius
    @property
    def celsius(self):
        return self._c
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._c = value
    @property
    def fahrenheit(self):
        return self._c * 9 / 5 + 32

t = Temperature(25)
print(t.celsius, t.fahrenheit)
t.celsius = 30
print(t.celsius, t.fahrenheit)
```

```
25 77.0
30 86.0
```

```python
# Example 5: Deleter with @property
class Account:
    def __init__(self, balance):
        self._balance = balance
    @property
    def balance(self):
        return self._balance
    @balance.setter
    def balance(self, v):
        if v < 0:
            raise ValueError("balance cannot be negative")
        self._balance = v
    @balance.deleter
    def balance(self):
        print("balance reset")
        del self._balance

a = Account(100)
print(a.balance)
a.balance = 200
print(a.balance)
del a.balance
# print(a.balance)   # AttributeError if uncommented
```

```
100
200
balance reset
```

```python
# Example 6: Real-world — read-only product ID
class Product:
    def __init__(self, name, price):
        self._id = id(self)        # pretend unique id
        self.name = name
        self.price = price
    @property
    def id(self):
        return self._id           # read-only

p = Product("Book", 250)
print(p.id, p.name, p.price)
# p.id = 999   # AttributeError: cannot set attribute
```

```
140234567891200 Book 250
```

## **Access Modifiers**

Python does not enforce access control the way Java or C++ does. There is no `private` keyword that actually hides a variable. What Python has are **conventions**, and the most common three are public, protected, and private.

### **Public**

No prefix. Accessible everywhere.

```python
class MyClass:
    def __init__(self):
        self.public_var = "I am public"

obj = MyClass()
print(obj.public_var)
```

```
I am public
```

### **Protected — Single Underscore Prefix**

A single underscore is a soft signal: "this is for internal use; please do not touch it from outside the class." Python does not enforce it. The attribute is still accessible, but linters and human reviewers will flag it.

```python
class MyClass:
    def __init__(self):
        self._protected_var = "I am protected"

obj = MyClass()
print(obj._protected_var)
```

```
I am protected
```

### **Private — Double Underscore Prefix (Name Mangling)**

A double underscore prefix triggers **name mangling**. The interpreter rewrites the name so it is harder to collide with a subclass. The attribute is still reachable, but you have to know the mangled name.

```python
class MyClass:
    def __init__(self):
        self.__private_var = "I am private"

obj = MyClass()
# print(obj.__private_var)        # AttributeError
print(obj._MyClass__private_var)  # works, but do not do this
```

```
I am private
```

The mangled name is `_ClassName__attribute`. So inside `MyClass`, `__private_var` actually lives as `_MyClass__private_var` on the object.

The point of name mangling is not to hide secrets. It is to prevent a child class from accidentally overriding a parent's "private" attribute. Look at this:

```python
class Parent:
    def __init__(self):
        self.__my_var = "Parent's var"

class Child(Parent):
    def __init__(self):
        super().__init__()
        self.__my_var = "Child's var"

p = Parent()
c = Child()
print(p._Parent__my_var)
print(c._Child__my_var)
```

```
Parent's var
Child's var
```

Each `__my_var` is mangled to its own class. The Parent's value does not overwrite the Child's. If the developer had used `_my_var` (single underscore) or `my_var` (no underscore) instead, the two would share one attribute and silently clobber each other.

### **What "Private" Really Means in Python**

There is no way to make an attribute truly inaccessible in Python. The single underscore is a convention for "do not use this from outside". The double underscore is a mechanism to avoid name collisions in subclasses. Neither is a security boundary — anyone who knows the mangled name can read or write the value.

For real protection, you should use the `private` attributes **plus** the `@property` decorator so that reads and writes go through controlled methods. That is the standard pattern:

```python
class Account:
    def __init__(self, balance):
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self.__balance += amount

a = Account(100)
print(a.balance)
a.deposit(50)
print(a.balance)
# a.balance = 1000   # AttributeError: can't set attribute
# a.__balance        # AttributeError
```

```
100
150
```

This is the closest Python gets to "read-only from outside". The attribute is hidden, the getter is exposed, and the only way to change the value is through a method that enforces rules.

### **Examples**

```python
# Example 1: Public attribute (no prefix)
class A:
    def __init__(self):
        self.x = 1
a = A()
print(a.x)
a.x = 2
print(a.x)
```

```
1
2
```

```python
# Example 2: Protected — single underscore is just a convention
class B:
    def __init__(self):
        self._x = 10
b = B()
print(b._x)            # still works
b._x = 99
print(b._x)
```

```
10
99
```

```python
# Example 3: Private — name mangling in action
class C:
    def __init__(self):
        self.__x = 100
c = C()
# print(c.__x)                # AttributeError
print(c._C__x)                 # the real name on the object
```

```
100
```

```python
# Example 4: Mangled names are different in parent and child
class Base:
    def __init__(self):
        self.__token = "BASE"
class Sub(Base):
    def __init__(self):
        super().__init__()
        self.__token = "SUB"

b = Base()
s = Sub()
print(b._Base__token)
print(s._Sub__token)
```

```
BASE
SUB
```

```python
# Example 5: Real-world — a bank account with a private balance
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self.__balance += amount

    def withdraw(self, amount):
        if amount > self.__balance:
            raise ValueError("insufficient funds")
        self.__balance -= amount

acc = BankAccount("Karan", 1000)
print(acc.owner, acc.balance)
acc.deposit(500)
print(acc.balance)
# acc.balance = 99999    # AttributeError
# acc.__balance          # AttributeError
```

```
Karan 1000
1500
```

```python
# Example 6: Methods can also be private
class Counter:
    def __init__(self):
        self._value = 0
    def increment(self):
        self.__tick()
        self._value += 1
    def __tick(self):
        pass   # internal step

c = Counter()
c.increment()
print(c._value)
# c.__tick()    # AttributeError
```

```
1
```

## **Passing Members of One Class to Another**

A class can reach the attributes and methods of another class. The common shape is: pass an object of one class as an argument to a method (or function) of another class, then use dot syntax on it.

```python
class Employee:
    def __init__(self, eno, ename, esal):
        self.eno = eno
        self.ename = ename
        self.esal = esal

    def display(self):
        print(f"Employee Number {self.eno}, Name {self.ename}, and Salary {self.esal}")

class Manager:
    def update_salary(emp):
        print("Previous salary:", emp.esal)
        emp.esal += 10000
        emp.display()

e = Employee(872425, "durga", 70000)
Manager.update_salary(e)
```

```
Previous salary: 70000
Employee Number 872425, Name durga, and Salary 80000
```

`Manager.update_salary` did not need an `Employee` to exist. It just took any object that has `esal` and `display()`. This is duck typing in action — "if it walks like a duck and quacks like a duck, treat it like a duck."

A bigger example showing the same trick across more than one class:

```python
class Employee:
    def __init__(self, eno):
        self.eno = eno

class Customer:
    def __init__(self, custid):
        self.custid = custid

class Demo:
    def m1(x):
        print("Type of x:", type(x))
        print("Employee number is", x.eno)

    def m2(y):
        print("Type of y:", type(y))
        print("Customer id is", y.custid)

e = Employee('e-101')
c = Customer('c-101')
Demo.m1(e)
Demo.m2(c)
```

```
Type of x: <class '__main__.Employee'>
Employee number is e-101
Type of y: <class '__main__.Customer'>
Customer id is c-101
```

And here is a clean way to build a small "router" that dispatches to the right method based on the class:

```python
class Test:
    def m1(x):
        print("m1 of test")

class Demo:
    def m1(x):
        print("m1 of demo")

class Sample:
    def m1(x, y):
        x.m1()
        y.m1()

t = Test()
d = Demo()
Sample.m1(t, d)
Sample.m1(d, t)
Sample.m1(t, t)
```

```
m1 of test
m1 of demo
m1 of demo
m1 of test
m1 of test
m1 of test
```

This is the same shape as dependency injection in larger frameworks. A class receives the collaborator it needs and uses it; the collaborator does not need to know about the class that uses it.

### **Reference Variables — How Many Point to the Same Object**

This is a small but important detail. When you assign one variable to another, both point to the same object. There is no copy unless you explicitly make one.

```python
class Test:
    pass

t1 = Test()
t2 = t1
t3 = t2
t4 = t1
print(type(t4))
```

```
<class '__main__.Test'>
```

`is` is the right check for "are these the same object?":

```python
print(t1 is t2)   # True
print(t1 is t3)   # True
```

Knowing that several variables can point at one object is what makes shared mutable state in Python both powerful and easy to misuse. The golden rule: never let two variables that look different both edit the same object unless that is what you meant.

### **Examples**

```python
# Example 1: One class calls another's method
class Logger:
    def log(self, msg):
        print(f"[LOG] {msg}")

class Service:
    def __init__(self, logger):
        self.logger = logger
    def do_work(self):
        self.logger.log("working...")
        return "done"

lg = Logger()
svc = Service(lg)
print(svc.do_work())
```

```
[LOG] working...
done
```

```python
# Example 2: Multiple classes share the same collaborator
class Printer:
    def print(self, text):
        print(text)

class Report:
    def __init__(self, title, body, printer):
        self.title = title
        self.body = body
        self.printer = printer
    def render(self):
        self.printer.print(self.title)
        self.printer.print(self.body)

p = Printer()
r = Report("Sales 2025", "Revenue up 20%", p)
r.render()
```

```
Sales 2025
Revenue up 20%
```

```python
# Example 3: Swapping collaborators at runtime
class FileSink:
    def write(self, text):
        with open("out.txt", "a") as f:
            f.write(text + "\n")

class StdoutSink:
    def write(self, text):
        print(text)

class App:
    def __init__(self, sink):
        self.sink = sink
    def emit(self, msg):
        self.sink.write(msg)

# A = App(FileSink())     # writes to file
A = App(StdoutSink())      # prints to console
A.emit("hello")
A.emit("world")
```

```
hello
world
```

```python
# Example 4: Method on one class receives an object of another
class Box:
    def __init__(self, w, h):
        self.w, self.h = w, h

class Geometry:
    @staticmethod
    def area(b):
        return b.w * b.h

b = Box(3, 4)
print(Geometry.area(b))
```

```
12
```

```python
# Example 5: Two objects passed into a third class
class Car:
    def __init__(self, model):
        self.model = model
class Bike:
    def __init__(self, model):
        self.model = model
class Garage:
    def __init__(self, vehicle1, vehicle2):
        self.v1 = vehicle1
        self.v2 = vehicle2
    def list_all(self):
        return [self.v1.model, self.v2.model]

g = Garage(Car("Tesla"), Bike("Yamaha"))
print(g.list_all())
```

```
['Tesla', 'Yamaha']
```

```python
# Example 6: Aliased references — same object, two names
class Bag:
    def __init__(self, items):
        self.items = items

a = Bag([1, 2, 3])
b = a
b.items.append(4)
print(a.items)
print(a is b)
```

```
[1, 2, 3, 4]
True
```

```python
# Example 7: Real-world — a small event bus
class EventBus:
    def __init__(self):
        self.listeners = []
    def subscribe(self, fn):
        self.listeners.append(fn)
    def publish(self, event):
        for fn in self.listeners:
            fn(event)

def log_event(event):
    print(f"got event: {event}")

bus = EventBus()
bus.subscribe(log_event)
bus.publish("user_login")
bus.publish("user_logout")
```

```
got event: user_login
got event: user_logout
```

## **Quick Reference Summary**

### **Constructor Rules**

| Rule | Notes |
|---|---|
| Name is always `__init__` | Do not rename. |
| Runs automatically on object creation | You do not call it. |
| Runs once per object | Each new object triggers it. |
| Main job: declare and initialize instance variables | Use `self` to set them. |
| Always takes at least `self` | More arguments are common. |
| Optional — Python provides a default if missing | The default does nothing. |
| Can be called explicitly | `t.__init__()` re-runs it on the same object. |
| No overloading — only the last `__init__` survives | Use default args or factory methods instead. |

### **Variable Types**

| Type | Where defined | How many copies | Access from inside | Access from outside | How to update |
|---|---|---|---|---|---|
| Instance | Constructor / instance method / outside via `obj` | One per object | `self.x` | `obj.x` | `obj.x = ...` or `self.x = ...` |
| Static | Class body / constructor / methods / outside (always with class name or `cls`) | One per class | `self.x`, `cls.x`, or `ClassName.x` | `ClassName.x` or `obj.x` (read only) | Only `ClassName.x = ...` or `cls.x = ...` |
| Local | Inside a method | One per call | Local name | Not accessible | Reassign within the method |

### **Method Types**

| Method | Decorator | First arg | Reads/writes | When to use |
|---|---|---|---|---|
| Instance | (none) | `self` | Instance + class state | Method acts on a specific object |
| Class | `@classmethod` | `cls` | Class state only | Factory, alternate constructor, count, settings |
| Static | `@staticmethod` | (none) | Only locals | Pure utility function grouped under the class |

### **Method Selection — Decision Rules**

| Variables used | Pick this |
|---|---|
| Instance variable (with or without static, with or without local) | Instance method |
| Only static + local | Class method |
| Only local | Static method |

### **Getters, Setters, and Properties**

| Pattern | When to use |
|---|---|
| Constructor only | All data is known at creation and is required. |
| Plain getter/setter methods | Data is not known at creation, or simple validation is needed. |
| `@property` + setter | You want attribute-style access but still need validation or read-only control. |
| `@property` only (no setter) | Read-only, computed value. |

### **Access Modifiers**

| Style | Prefix | Effect | When to use |
|---|---|---|---|
| Public | (none) | Always accessible | Normal attributes and methods. |
| Protected | `_` | Convention "do not use from outside" | Internal helpers, methods subclasses may override. |
| Private | `__` | Name-mangled to `_ClassName__attr` | Attributes that should not clash with subclass attributes. |
| Read-only | `__attr` + `@property` (no setter) | Read from outside, write only inside | Balance fields, IDs, anything users should not reassign. |

### **Common Patterns**

| Pattern | Shape |
|---|---|
| Constructor + instance method | Object owns data and behaviour. |
| Class method as factory | `ClassName.from_something(...)` returns an instance. |
| Static method as utility | Pure function logically grouped with a class. |
| `@property` for computed value | Method that looks like an attribute. |
| Pass object to other class | A class uses another class's members via duck typing. |

## **Practice and Next Steps**

Work through these to lock in everything above:

- Write a `Car` class with `make`, `model`, and `year` instance variables. Add an `info()` instance method that prints them.
- Add a class variable `wheels = 4` and prove that changing `Car.wheels` updates it for every instance.
- Add a class method `from_string(s)` that takes a string like `"Toyota,Camry,2022"` and returns a `Car`.
- Add a static method `is_older(car, year)` that returns `True` if the car is older than `year`.
- Use `@property` for a `car_age` computed attribute that returns the current year minus the car's year.
- Write a `BankAccount` class with a `__balance` private attribute, a `deposit` method, a `withdraw` method, and a read-only `balance` property.
- Create two classes `Manager` and `Developer` that both have a `name` and a `salary`. Write a `pay_raise` function (or method) that takes either of them and increases the salary by 10%. Confirm duck typing works.
- Inside a class, write a method that creates a new instance variable on `self` only when the method is called. Print `obj.__dict__` before and after to see the new key appear.
- Try writing two `__init__` methods in the same class. Confirm only the last one survives. Then refactor to use a default argument instead.
- Create a counter that tracks how many objects of a class exist, using a class variable and a class method.