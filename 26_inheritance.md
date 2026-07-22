# **Python Inheritance**

## **What Is Inheritance**

Inheritance is a way to build a new class on top of an existing one. The new class automatically gets all the variables, methods, and constructors of the existing class, and can add or override things on top of it.

The class being inherited from is called the **parent**, **super**, or **base** class. The class doing the inheriting is called the **child**, **sub**, or **derived** class.

```python
class Parent:
    def greet(self):
        print("Hello from Parent")

class Child(Parent):     # Child inherits from Parent
    def child_only(self):
        print("Hello from Child")

c = Child()
c.greet()        # inherited
c.child_only()   # defined here
```

```
Hello from Parent
Hello from Child
```

The `Child(Parent)` syntax is what makes it inheritance. The class name in the parentheses is the parent.

### **Try it in Jupyter — Small Examples**

```python
# Example 1: A parent that knows one trick
class Animal:
    def speak(self):
        return "Some sound"

class Dog(Animal):
    pass        # Dog inherits speak() unchanged

d = Dog()
print(d.speak())
```

```
Some sound
```

```python
# Example 2: A child adds its own behaviour on top
class Animal:
    def speak(self):
        return "Some sound"

class Cat(Animal):
    def purr(self):
        return "purr purr"

c = Cat()
print(c.speak())    # inherited
print(c.purr())      # new
```

```
Some sound
purr purr
```

```python
# Example 3: A chain of grandparents
class A:
    def a(self):
        return "from A"
class B(A):
    def b(self):
        return "from B"
class C(B):
    def c(self):
        return "from C"

x = C()
print(x.a(), x.b(), x.c())
```

```
from A from B from C
```

```python
# Example 4: isinstance() and issubclass()
class Vehicle: pass
class Car(Vehicle): pass
class Bike(Vehicle): pass

c = Car()
print(isinstance(c, Car))     # True
print(isinstance(c, Vehicle)) # True (parent counts)
print(issubclass(Car, Vehicle))  # True
print(issubclass(Bike, Car))    # False (siblings)
```

```
True
True
True
False
```

```python
# Example 5: __bases__ to see the parent classes
class Parent: pass
class Child(Parent): pass

print(Child.__bases__)        # tuple of direct parents
print(Parent.__bases__)       # object by default
```

```
(<class '__main__.Parent'>,)
(<class 'object'>,)
```

```python
# Example 6: A real-world mini shape
class User:
    def __init__(self, name):
        self.name = name
    def describe(self):
        return f"User: {self.name}"

class Admin(User):
    def describe(self):
        return f"Admin: {self.name} (full access)"

print(User("Om").describe())
print(Admin("Karan").describe())
```

```
User: Om
Admin: Karan (full access)
```

## **Why Use Inheritance — The Real Reason**

The point of inheritance is **code reuse** and **maintainability**. Imagine a loan processing system with three loan types — Home, Car, Personal. They all need most of the same operations (calculate EMI, validate documents, generate statement, send notification, etc.).

Without inheritance, every loan class would have to copy 250 methods, and any bug fix would need to happen 750 times across the codebase.

```
Without Inheritance (the bad way)
    class HomeLoan:        250 methods
    class CarLoan:         250 methods
    class PersonalLoan:    250 methods
    Total:                 750 methods
    Effort:                75 hours
```

With inheritance, the common 200 methods live in a base `Loan` class. Each loan type only adds its own 50 specific methods, and the total drops to 350.

```
With Inheritance (the right way)
    class Loan:                    200 common methods
    class HomeLoan(Loan):           50 home-loan-specific methods
    class CarLoan(Loan):            50 car-loan-specific methods
    class PersonalLoan(Loan):       50 personal-loan-specific methods
    Total:                         350 methods
    Effort:                        35 hours
```

A bug fix in the base `Loan` class now propagates to every child automatically. That is the maintainability win.

This is exactly how the real world uses inheritance. `SQLAlchemy.declarative_base` provides common ORM behaviour. `FastAPI`'s `BaseModel` (via Pydantic) provides common validation. `Django`'s `models.Model` provides common database fields. `unittest.TestCase` provides common test scaffolding. In every case, the base class holds shared behaviour, and subclasses add specifics.

### **Try it in Jupyter — Small Examples**

```python
# Example 1: A small base class with shared setup
class Animal:
    def __init__(self, name):
        self.name = name
    def describe(self):
        return f"{self.name} ({self.__class__.__name__})"

class Dog(Animal): pass
class Cat(Animal): pass

print(Dog("Bruno").describe())
print(Cat("Whiskers").describe())
# describe() is written once in the base, used by both
```

```
Bruno (Dog)
Whiskers (Cat)
```

```python
# Example 2: Add a method only on one child
class Animal:
    def __init__(self, name):
        self.name = name
class Dog(Animal):
    def bark(self):
        return "Woof"
class Cat(Animal):
    def meow(self):
        return "Meow"

print(Dog("Bruno").bark())
print(Cat("Whiskers").meow())
```

```
Woof
Meow
```

```python
# Example 3: Show the savings — one bug fix flows down
class Payment:
    def validate(self, amount):
        if amount <= 0:
            raise ValueError("amount must be > 0")
        return True

class CardPayment(Payment): pass
class UpiPayment(Payment): pass

# Fixing validate() in Payment fixes it for both children automatically.
CardPayment().validate(100)
UpiPayment().validate(50)
```

```
True
True
```

```python
# Example 4: Count shared vs specific methods
class Vehicle:
    def start(self): return "started"
    def stop(self):  return "stopped"
    def honk(self):  return "beep"

class Car(Vehicle):
    def open_trunk(self): return "trunk open"

print("Vehicle has:", [m for m in dir(Vehicle) if not m.startswith("_")])
print("Car has:    ", [m for m in dir(Car)     if not m.startswith("_")])
print("Car's own methods:", [m for m in vars(Car) if not m.startswith("_")])
```

```
Vehicle has: ['honk', 'start', 'stop']
Car has:     ['honk', 'open_trunk', 'start', 'stop']
Car's own methods: ['open_trunk']
```

## **IS-A vs HAS-A — A Quick Note**

Inheritance covers the **IS-A** side of class relationships. A `CarLoan` IS-A `Loan`, an `Employee` IS-A `Person`, a `Square` IS-A `Rectangle`.

The opposite side is **HAS-A** — when one class *contains or uses* another as part of its data. A `Car` HAS-A `Engine`, an `Employee` HAS-A `Car`, a `Library` HAS-A list of `Book`s. That side is covered in its own file (`python_hasa_composition.md`).

The decision rule:

- If you want to **extend** existing functionality with more functionality → use **IS-A (inheritance)**.
- If you want to **use** existing functionality as-is → use **HAS-A (composition)**.

Both can be combined in the same class. The example below shows an `Employee` that IS-A `Person` and HAS-A `Car` at the same time:

```python
class Car:
    def __init__(self, name, model, color):
        self.name = name
        self.model = model
        self.color = color

    def getInfo(self):
        print(f"Car name: {self.name}, model: {self.model}, color: {self.color}")


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def eat_drink(self):
        print("Eating vadapav and drinking lassi!")


class Employee(Person):                # IS-A: Employee is a Person
    company = "DurgaSoft"

    def __init__(self, name, age, eid, esal, car):   # HAS-A: Employee has a Car
        super().__init__(name, age)
        self.eid = eid
        self.esal = esal
        self.car = car

    def empWork(self):
        print("Python programming based on the requirements")

    def empInfo(self):
        print(f"Employee name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Company: {self.company}")
        print(f"ID: {self.eid}")
        print(f"Salary: {self.esal}")
        print("Employee car information:")
        self.car.getInfo()


car = Car("Range Rover", "4.7V", "Gray")
emp = Employee("Durga", 41, 2344, 700000, car)
emp.eat_drink()    # inherited from Person
emp.empWork()      # defined in Employee
emp.empInfo()      # uses both Person fields and the Car
```

```
Eating vadapav and drinking lassi!
Python programming based on the requirements
Employee name: Durga
Age: 41
Company: DurgaSoft
ID: 2344
Salary: 700000
Employee car information:
Car name: Range Rover, model: 4.7V, color: Gray
```

The IS-A part of this example is what this file focuses on. The HAS-A part is the topic of the composition file.

## **Types of Inheritance in Python**

There are six patterns. The first five are valid in Python. The sixth is not allowed.

### **Single Inheritance**

One parent, one child. The simplest form.

```python
class P:
    def m1(self):
        print("Parent method")

class C(P):
    def m2(self):
        print("Child method")

c = C()
c.m1()
c.m2()
```

```
Parent method
Child method
```

```
Diagram:
    P
    |
    C
```

This is the shape you will use most of the time in real code. A `User` class, a `Product` class, a `RequestHandler` class — most of your classes have one parent.

### **Try it in Jupyter — Small Examples**

```python
# Example 1: Single — most common shape
class Animal:
    def eat(self):
        return "eating"

class Dog(Animal):
    def bark(self):
        return "woof"

d = Dog()
print(d.eat(), d.bark())
```

```
eating woof
```

```python
# Example 2: A small FastAPI-style handler base
class BaseHandler:
    def handle(self, request):
        return f"handled {request}"

class PingHandler(BaseHandler):
    pass

print(PingHandler().handle("ping"))
```

```
handled ping
```

```python
# Example 3: Child overrides one method
class Animal:
    def speak(self):
        return "..."

class Cat(Animal):
    def speak(self):
        return "meow"

print(Animal().speak(), Cat().speak())
```

```
... meow
```

```python
# Example 4: Add a new attribute in the child
class User:
    def __init__(self, name):
        self.name = name

class AdminUser(User):
    def __init__(self, name, level):
        super().__init__(name)
        self.level = level

a = AdminUser("Om", 3)
print(a.name, a.level)
```

```
Om 3
```

```python
# Example 5: Check the inheritance chain
class A: pass
class B(A): pass
print(B.__mro__)
```

```
(<class '__main__.B'>, <class '__main__.A'>, <class 'object'>)
```

### **Multilevel Inheritance**

A chain: `C` inherits from `B`, which inherits from `A`. The child at the bottom has access to everything above it.

```python
class P:
    def m1(self):
        print("Parent method")

class C(P):
    def m2(self):
        print("Child method")

class CC(C):
    def m3(self):
        print("Sub child method")

c = CC()
c.m1()
c.m2()
c.m3()
```

```
Parent method
Child method
Sub child method
```

```
Diagram:
    P
    |
    C
    |
    CC
```

A real example: an `Animal` → `Mammal` → `Dog` hierarchy.

```python
class Animal:
    def __init__(self, species):
        self.species = species
    def breathe(self):
        return f"{self.species} is breathing"

class Mammal(Animal):
    def give_birth(self):
        return f"{self.species} gives birth to live young"

class Dog(Mammal):
    def __init__(self, breed):
        super().__init__("Dog")
        self.breed = breed
    def bark(self):
        return f"{self.breed} is barking"

d = Dog("Labrador")
print(d.breathe())      # from Animal
print(d.give_birth())   # from Mammal
print(d.bark())         # from Dog
```

```
Dog is breathing
Dog gives birth to live young
Labrador is barking
```

### **Try it in Jupyter — Small Examples**

```python
# Example 1: Three levels, each adds one thing
class A:
    def a(self): return "A"

class B(A):
    def b(self): return "B"

class C(B):
    def c(self): return "C"

x = C()
print(x.a(), x.b(), x.c())
```

```
A B C
```

```python
# Example 2: Real-world — Animal / Mammal / Dog
class Animal:
    def __init__(self, name):
        self.name = name
class Mammal(Animal):
    def warm_blooded(self): return True
class Dog(Mammal):
    def speak(self): return "Woof"

d = Dog("Bruno")
print(d.name, d.warm_blooded(), d.speak())
```

```
Bruno True Woof
```

```python
# Example 3: Override at every level
class A:
    def hello(self): return "A.hello"
class B(A):
    def hello(self): return "B.hello"
class C(B):
    def hello(self): return "C.hello"

print(C().hello())   # C wins
```

```
C.hello
```

```python
# Example 4: Use super() to chain
class A:
    def hello(self): return "A"
class B(A):
    def hello(self):
        return super().hello() + " -> B"
class C(B):
    def hello(self):
        return super().hello() + " -> C"

print(C().hello())
```

```
A -> B -> C
```

```python
# Example 5: ML-ish — BaseModel / Classifier / RandomForest-like
class BaseModel:
    def fit(self, X, y): print("BaseModel.fit")
    def predict(self, X): return [0]

class TreeModel(BaseModel):
    def fit(self, X, y):
        super().fit(X, y)
        print("TreeModel.fit")

class RandomForestModel(TreeModel):
    def fit(self, X, y):
        super().fit(X, y)
        print("RandomForestModel.fit")

RandomForestModel().fit(None, None)
```

```
BaseModel.fit
TreeModel.fit
RandomForestModel.fit
```

### **Hierarchical Inheritance**

One parent, multiple children. Each child gets the parent's behaviour and adds its own.

```python
class Animal:
    def __init__(self, species):
        self.species = species
    def breathe(self):
        return f"{self.species} is breathing"

class Mammal(Animal):
    def give_birth(self):
        return f"{self.species} gives birth to live young"

class Bird(Animal):
    def lay_eggs(self):
        return f"{self.species} lays eggs"

class Dog(Mammal):
    def __init__(self, breed):
        super().__init__("Dog")
        self.breed = breed
    def bark(self):
        return f"{self.breed} is barking"

class Eagle(Bird):
    def __init__(self):
        super().__init__("Eagle")
    def hunt(self):
        return "Eagle is hunting from the sky"

dog = Dog("Labrador")
eagle = Eagle()

print(dog.breathe())      # from Animal
print(dog.give_birth())   # from Mammal
print(dog.bark())         # from Dog

print(eagle.breathe())    # from Animal
print(eagle.lay_eggs())   # from Bird
print(eagle.hunt())       # from Eagle
```

```
Dog is breathing
Dog gives birth to live young
Labrador is barking
Eagle is breathing
Eagle lays eggs
Eagle is hunting from the sky
```

```
Diagram:
    Animal
    /    \
Mammal   Bird
   |       |
  Dog    Eagle
```

This pattern shows up in real frameworks: `unittest.TestCase` has multiple specialised subclasses; `tkinter.Frame` and `tkinter.Toplevel` both inherit from a common widget base; SQLAlchemy's declarative base has many model classes hanging off it.

### **Try it in Jupyter — Small Examples**

```python
# Example 1: Shape family
class Shape:
    def name(self): return "shape"

class Circle(Shape):
    def name(self): return "circle"

class Square(Shape):
    def name(self): return "square"

print(Circle().name(), Square().name())
```

```
circle square
```

```python
# Example 2: Notification system with three channels
class Notification:
    def send(self, msg): return f"send '{msg}'"

class EmailNotification(Notification):
    def send(self, msg):
        return f"email: {super().send(msg)}"

class SmsNotification(Notification):
    def send(self, msg):
        return f"sms:   {super().send(msg)}"

print(EmailNotification().send("hi"))
print(SmsNotification().send("hi"))
```

```
email: send 'hi'
sms:   send 'hi'
```

```python
# Example 3: Three children, two methods
class Vehicle:
    def fuel(self): return "unknown"

class Car(Vehicle):
    def fuel(self): return "petrol"
class Truck(Vehicle):
    def fuel(self): return "diesel"
class Bike(Vehicle):
    def fuel(self): return "none (manual)"

for v in [Car(), Truck(), Bike()]:
    print(v.fuel())
```

```
petrol
diesel
none (manual)
```

```python
# Example 4: Children that share parent but not each other
class Employee:
    def role(self): return "employee"
class Developer(Employee):
    def role(self): return "developer"
class Manager(Employee):
    def role(self): return "manager"

print(Developer().role(), Manager().role())
```

```
developer manager
```

```python
# Example 5: MRO with siblings
class Parent: pass
class Child1(Parent): pass
class Child2(Parent): pass

print(Child1.__bases__)
print(Child2.__bases__)
print(Child1.__mro__)
```

```
(<class '__main__.Parent'>,)
(<class '__main__.Parent'>,)
(<class '__main__.Child1'>, <class '__main__.Parent'>, <class 'object'>)
```

### **Multiple Inheritance**

One child, multiple parents. The child gets the combined behaviour of all its parents.

```python
class P1:
    def m1(self):
        print("Parent1 method")

class P2:
    def m2(self):
        print("Parent2 method")

class C(P1, P2):
    def m3(self):
        print("Child method")

c = C()
c.m1()
c.m2()
c.m3()
```

```
Parent1 method
Parent2 method
Child method
```

A more realistic example: a `Ball` is both something that moves and something that has mass.

```python
class Motion:
    def __init__(self, velocity):
        self.velocity = velocity
    def move(self):
        return f"Moving at {self.velocity} m/s"

class Mass:
    def __init__(self, mass):
        self.mass = mass
    def describe_mass(self):
        return f"Has a mass of {self.mass} kg"

class Ball(Motion, Mass):
    def __init__(self, velocity, mass):
        Motion.__init__(self, velocity)
        Mass.__init__(self, mass)
    def describe(self):
        return f"Ball: {self.move()} and {self.describe_mass()}"

ball = Ball(5, 0.5)
print(ball.describe())
```

```
Ball: Moving at 5 m/s and Has a mass of 0.5 kg
```

When two parents have a method with the same name, the **leftmost parent wins** in the inheritance list. So `class C(P1, P2):` will call `P1.m1()` before `P2.m1()`.

```python
class P1:
    def m1(self):
        print("Parent1 method")

class P2:
    def m1(self):
        print("Parent2 method")

class C(P1, P2):
    def m2(self):
        print("Child method")

c = C()
c.m1()
c.m2()
```

```
Parent1 method
Child method
```

### **Try it in Jupyter — Small Examples**

```python
# Example 1: Two capabilities, one class
class Flyable:
    def fly(self): return "flying"

class Swimmable:
    def swim(self): return "swimming"

class Duck(Flyable, Swimmable):
    pass

d = Duck()
print(d.fly(), d.swim())
```

```
flying swimming
```

```python
# Example 2: Order matters when names clash
class A:
    def m(self): return "A"
class B:
    def m(self): return "B"

class C1(A, B): pass
class C2(B, A): pass

print(C1().m())
print(C2().m())
```

```
A
B
```

```python
# Example 3: Multiple inheritance for mixins
class JsonMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

class LogMixin:
    def log(self, msg):
        print(f"[{self.__class__.__name__}] {msg}")

class User(JsonMixin, LogMixin):
    def __init__(self, name):
        self.name = name

u = User("Karan")
print(u.to_json())
u.log("created")
```

```
{"name": "Karan"}
[User] created
```

```python
# Example 4: Diamond — A is shared by B and C
class A:
    def m(self): return "A"
class B(A):
    def m(self): return "B"
class C(A):
    def m(self): return "C"
class D(B, C):
    pass

print(D().m())    # B wins because it's first
print(D.__mro__)
```

```
B
(<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
```

```python
# Example 5: Multiple inheritance with __init__
class A:
    def __init__(self): print("A init")
class B:
    def __init__(self): print("B init")
class C(A, B):
    def __init__(self):
        super().__init__()    # walks MRO, calls A.__init__ only
        print("C init")

C()
```

```
A init
C init
```

### **Hybrid Inheritance**

A combination of two or more of the patterns above. It is common in real systems. For example, a project might have a mix of multilevel and hierarchical chains.

```
Diagram example:
      A
     / \
    B   C
   /     \
  D       E
   \     /
     F
    / \
   G   H
```

This is the most common shape in real codebases. It is also where things get tricky with method resolution, so it is worth keeping hierarchies shallow.

### **Try it in Jupyter — Small Examples**

```python
# Example 1: Diamond — common real-world shape
class A:
    def m(self): return "A"
class B(A): pass
class C(A): pass
class D(B, C): pass

print(D().m())   # A
print(D.__mro__)
```

```
A
(<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
```

```python
# Example 2: Realistic — service layer + mixin
class BaseService:
    def name(self): return "BaseService"

class CacheMixin:
    def cache(self): return "cached"

class UserService(BaseService, CacheMixin):
    pass

class OrderService(BaseService, CacheMixin):
    pass

u = UserService()
o = OrderService()
print(u.name(), u.cache())
print(o.name(), o.cache())
```

```
BaseService cached
BaseService cached
```

```python
# Example 3: Multi-level + hierarchical mix
class A: pass
class B(A): pass
class C(A): pass
class D(B): pass
class E(B): pass

print(D.__mro__)
print(E.__mro__)
```

```
(<class '__main__.D'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>)
(<class '__main__.E'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>)
```

### **Cyclic Inheritance — Not Allowed**

A class cannot inherit from itself, directly or indirectly. Python raises an error at class creation time.

```python
# Direct cycle — not allowed
class A(A):
    pass

# Indirect cycle — not allowed
class A(B):
    pass
class B(A):
    pass
```

Both raise `TypeError: inconsistent method resolution order` or `NameError` depending on the exact shape. The rule is simple: a class cannot be its own ancestor.

### **Try it in Jupyter — Small Examples**

```python
# Example 1: Direct cycle
# class A(A):
#     pass
# TypeError: invalid __mro__
```

```python
# Example 2: Indirect cycle
# class A(B): pass
# class B(A): pass
# NameError: name 'B' is not defined
```

```python
# Example 3: Self-reference check
class A: pass
# class A(A): pass   # would fail
# class B(A): pass
# class A(B): pass   # would also fail
```

```python
# Example 4: What happens if you try (using try/except)
try:
    class X(X):
        pass
except Exception as e:
    print(type(e).__name__, "->", e)
```

```
TypeError -> __mro__ entries must be unique
```

```python
# Example 5: Cyclic via two classes
try:
    exec("class A(B): pass\nclass B(A): pass")
except Exception as e:
    print(type(e).__name__, "->", e)
```

```
NameError -> name 'B' is not defined
```

## **Method Overriding**

When a child class defines a method with the same name as one in the parent, the child's version takes over. The parent version is **overridden**.

```python
class Animal:
    def speak(self):
        print("Some sound")

class Dog(Animal):
    def speak(self):         # overrides Animal.speak
        print("Woof!")

class Cat(Animal):
    def speak(self):         # overrides Animal.speak
        print("Meow!")

Dog().speak()
Cat().speak()
Animal().speak()
```

```
Woof!
Meow!
Some sound
```

This is how polymorphism works in Python — the same method name behaves differently depending on the actual type of the object at runtime. This is the foundation of frameworks like Pydantic, SQLAlchemy, and Django ORM, where you override `__str__`, `save`, `clean`, or `validate` to customize behaviour.

### **Overriding vs Overloading**

A quick note because the words are easy to mix up:

- **Overriding** — child class replaces a parent method with its own. Supported fully in Python.
- **Overloading** — same method name, different parameter list. Python does **not** support this the way Java does. Use default arguments or `*args` instead. (Covered in the polymorphism / operator overloading file.)

### **Try it in Jupyter — Small Examples**

```python
# Example 1: Override and call the parent too
class A:
    def hello(self): return "A.hello"
class B(A):
    def hello(self):
        return super().hello() + " then B.hello"

print(B().hello())
```

```
A.hello then B.hello
```

```python
# Example 2: Override to specialize
class Shape:
    def area(self): return 0
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
# Example 3: Polymorphism in a loop
class Animal:
    def speak(self): return "..."
class Dog(Animal):
    def speak(self): return "Woof"
class Cat(Animal):
    def speak(self): return "Meow"

for a in [Dog(), Cat(), Animal()]:
    print(a.speak())
```

```
Woof
Meow
...
```

```python
# Example 4: Override a built-in dunder
class MyList(list):
    def __repr__(self):
        return f"MyList({super().__repr__()})"

print(MyList([1, 2, 3]))
```

```
MyList([1, 2, 3])
```

```python
# Example 5: Override __str__ for user-friendly printing
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __str__(self):
        return f"{self.name} ({self.age})"

print(User("Karan", 22))
print(str(User("Om", 30)))
```

```
Karan (22)
Om (30)
```

## **Constructor Behaviour in Inheritance**

When you create a child object:

- If the child defines `__init__`, the child's runs (and the parent's does not, unless you call it via `super()`).
- If the child does not define `__init__`, the parent's `__init__` runs.
- Only one object is created — the child object. The parent constructor is called on that same object.

```python
class P:
    def __init__(self):
        print(id(self))

class C(P):
    pass

c = C()
print(id(c))
```

Both `id` values match. The "parent object" is the same as the child object.

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Student(Person):
    def __init__(self, name, age, rollno, marks):
        super().__init__(name, age)
        self.rollno = rollno
        self.marks = marks

    def __str__(self):
        return f"Name={self.name}\nAge={self.age}\nRollno={self.rollno}\nMarks={self.marks}"

s1 = Student("Durga", 48, 101, 90)
print(s1)
```

```
Name=Durga
Age=48
Rollno=101
Marks=90
```

`super().__init__(name, age)` runs the parent's `__init__` on the current child object. That is how the parent fields get set. Without that call, `self.name` and `self.age` would not exist on the child object.

The full picture of `super()` is in the dedicated `super()` file. For inheritance basics, the key is just: **call `super().__init__(...)` as the first line of the child constructor** whenever the parent has its own `__init__` that sets fields you need.

### **Try it in Jupyter — Small Examples**

```python
# Example 1: Child without __init__ — parent's runs
class A:
    def __init__(self):
        print("A init")
class B(A):
    pass

B()
```

```
A init
```

```python
# Example 2: Child with __init__ — only child's runs
class A:
    def __init__(self):
        print("A init")
class B(A):
    def __init__(self):
        print("B init")

B()
```

```
B init
```

```python
# Example 3: Child calls super to extend setup
class A:
    def __init__(self):
        print("A init")
class B(A):
    def __init__(self):
        super().__init__()
        print("B init")

B()
```

```
A init
B init
```

```python
# Example 4: Only one object is created
class A:
    def __init__(self):
        print("A.init, self =", id(self))
class B(A):
    def __init__(self):
        super().__init__()
        print("B.init, self =", id(self))

b = B()
print("b outside     =", id(b))
```

```
A.init, self = 140234567891200
B.init, self = 140234567891200
b outside     = 140234567891200
```

```python
# Example 5: Forgetting super().__init__ loses parent fields
class P:
    def __init__(self):
        self.name = "from P"

class C(P):
    def __init__(self):
        # forgot super().__init__()
        self.child = "from C"

c = C()
print(c.child)
# print(c.name)    # AttributeError if uncommented
```

```
from C
```

## **Method Resolution — A Quick Note**

When a method is called on a child object, Python has to decide which version to use. It walks up the inheritance chain in a defined order, left to right, depth first.

For the vast majority of real code — single inheritance, shallow hierarchies, no name clashes — this is automatic and you never think about it. The two cases where it matters:

1. **Multiple inheritance with name clashes** — `class C(A, B):` where both `A` and `B` define `m1`. The leftmost parent wins.
2. **Diamond shapes** — grandparent A, two parents B and C, child D. Python's algorithm guarantees a consistent order, but the order can be surprising if you did not design the chain carefully.

The full MRO algorithm is interesting academically but rarely needed in day-to-day Python work. The two practical tools are:

- `print(ClassName.mro())` to inspect the order.
- `super()` to walk it without hardcoding parent class names.

Everything else, including the C3 linearization details, is covered in the references at the end of this file.

### **Try it in Jupyter — Small Examples**

```python
# Example 1: Inspect MRO
class A: pass
class B(A): pass
class C(B): pass

print(C.mro())
```

```
[<class '__main__.C'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>]
```

```python
# Example 2: Order matters in multiple inheritance
class A:
    def m(self): return "A"
class B:
    def m(self): return "B"

class C1(A, B): pass
class C2(B, A): pass

print(C1().m(), "   |   ", C2().m())
print(C1.mro())
```

```
A    |   B
[<class '__main__.C1'>, <class '__main__.A'>, <class '__main__.B'>, <class 'object'>)
```

```python
# Example 3: Diamond resolution
class A:
    def m(self): return "A"
class B(A):
    def m(self): return "B"
class C(A):
    def m(self): return "C"
class D(B, C): pass

print(D().m())           # B
print(D.mro())
```

```
B
(<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
```

```python
# Example 4: __mro__ is a tuple you can iterate
class A: pass
class B(A): pass
for cls in B.__mro__:
    print(cls)
```

```
<class '__main__.B'>
<class '__main__.A'>
<class 'object'>
```

## **Real-World Example: A Small User Role Hierarchy**

A pattern that shows up in almost every backend service: different kinds of users with different permissions.

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    def describe(self):
        return f"{self.name} ({self.email})"

class Customer(User):
    def __init__(self, name, email, balance=0):
        super().__init__(name, email)
        self.balance = balance
    def describe(self):
        return f"Customer: {super().describe()}, balance={self.balance}"

class Admin(User):
    def __init__(self, name, email, level):
        super().__init__(name, email)
        self.level = level
    def describe(self):
        return f"Admin: {super().describe()}, level={self.level}"

c = Customer("Karan", "k@x.com", 1000)
a = Admin("Om", "o@x.com", 3)
print(c.describe())
print(a.describe())
```

```
Customer: Karan (k@x.com), balance=1000
Admin: Om (o@x.com), level=3
```

`super().describe()` inside the child lets you reuse the parent's version and add more — this is the standard way to extend behaviour without duplicating it.

## **Real-World Example: A Small ORM Shape**

This is the simplified shape of what `Django`, `SQLAlchemy`, and `Peewee` do under the hood. The base class holds the table-like behaviour; the child class holds the schema.

```python
class Model:
    _registry = {}   # aggregation: lives on the class, not the object

    def __init__(self, **fields):
        for k, v in fields.items():
            setattr(self, k, v)
        Model._registry[self.__class__.__name__] = self.__class__

    def save(self):
        print(f"Saving {self.__class__.__name__}: {self.__dict__}")

    @classmethod
    def all(cls):
        return cls._registry

class User(Model):
    pass

class Order(Model):
    pass

u = User(name="Karan", email="k@x.com")
u.save()

o = Order(id=1, total=250)
o.save()
```

```
Saving User: {'name': 'Karan', 'email': 'k@x.com'}
Saving Order: {'id': 1, 'total': 250}
```

This is composition (the base `Model` is part of every `User`/`Order`) combined with aggregation (`_registry` is shared across all instances of all subclasses). See the composition file for the full breakdown.

## **Best Practices for Inheritance**

- Prefer **composition** over inheritance when the relationship is "uses" rather than "is a kind of". This is one of the classic OO design rules. The HAS-A side is covered in `python_hasa_composition.md`.
- Keep hierarchies **shallow**. Two or three levels is usually enough. Deeper chains are hard to reason about.
- Use `super()` instead of hardcoding the parent class name. It makes subclasses behave correctly even if the chain is extended later.
- Override methods to **extend**, not to **replace without calling super**. If you write a child `display()` that does not call `super().display()`, you are silently breaking any other class in the chain that depends on the parent version.
- Document the intended extension points. A docstring on a parent method that says "Subclasses may override this to ..." is much clearer than a method that happens to be overridable.
- Use `abc.ABC` and `@abstractmethod` when you want to **force** subclasses to provide an implementation. This is the topic of the encapsulation and abstract classes file.
- Test inheritance hierarchies carefully. Bugs in the parent silently propagate to every child.

## **Quick Reference Summary**

### **Inheritance at a Glance**

| Pattern | Shape | When to use |
|---|---|---|
| Single | `A → B` | Most common. One specialised kind of one thing. |
| Multilevel | `A → B → C` | Layered abstractions (e.g. `Animal → Mammal → Dog`). |
| Hierarchical | `A → B`, `A → C` | One base behaviour, many variants. |
| Multiple | `A, B → C` | Combining orthogonal capabilities (e.g. `Motion, Mass → Ball`). |
| Hybrid | Any combination of the above | Real codebases often end up here. Keep shallow. |
| Cyclic | `A → B → A` | Not allowed. Python raises an error. |

### **IS-A vs HAS-A (in one line)**

| Need | Use |
|---|---|
| Extend behaviour (the new class is a kind of the old one) | IS-A (inheritance) — this file. |
| Just use behaviour (the new class has the old one as a part) | HAS-A (composition) — see `python_hasa_composition.md`. |

The detailed breakdown of Composition vs Aggregation lives in the composition file.

### **Method Overriding**

| What | How |
|---|---|
| Override a parent method | Define a method with the same name in the child. |
| Call the parent version too | Use `super().method(...)` inside the child. |
| Replace completely | Skip the `super()` call. Do this only intentionally. |

### **Constructor in Inheritance**

| Situation | What happens |
|---|---|
| Child has no `__init__` | Parent's `__init__` runs on the child object. |
| Child has `__init__` | Child's runs. Parent's does not run unless you call `super().__init__(...)`. |
| Want to extend parent setup | Always call `super().__init__(...)` as the first line of the child constructor. |

## **Practice and Next Steps**

- Create a `Vehicle` base class with `start()` and `stop()` methods. Inherit `Car`, `Bike`, and `Truck` from it. Each child overrides `start()` with a custom message.
- Build a `BankAccount` base class with `deposit`, `withdraw`, and `balance`. Inherit `SavingsAccount` and `CurrentAccount` with their own interest rules.
- Create a `Shape` base class with a `name`. Inherit `Circle` and `Rectangle`, each with their own `area()` method.
- Try multiple inheritance: a `FlyingCar` that inherits from both `Car` and `Aircraft`. Watch how `super()` walks the chain.
- Use `print(SubClass.mro())` on a multi-level class to see the actual method resolution order. Try it before and after reordering the parent list to see the order change.
- Refactor the Loan example at the top of this file into real classes with a base `Loan` and three children. Add a method to the base class and confirm every child gets it automatically.
- Once you are comfortable with inheritance, move on to `python_hasa_composition.md` to see how to combine IS-A and HAS-A in the same design.
