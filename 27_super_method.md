# **Python `super()`**

## **What Is `super()`**

`super()` is a built-in function that returns a temporary object representing the parent class. The most common use is to call a parent class's constructor or method from inside a child class, without having to hardcode the parent's name.

```python
super().__init__(...)   # call the parent's __init__
super().method(...)     # call any parent method
super().attribute       # access a parent class variable
```

The big advantage of `super()` over hardcoding the parent name is that it respects the **method resolution order (MRO)**. In single inheritance it almost always refers to the immediate parent. In multiple inheritance, it walks the chain in the correct order, so your code keeps working if the inheritance graph changes.

### **Examples**

```python
# Example 1: A simple child uses super() to call the parent
class A:
    def hello(self):
        return "from A"

class B(A):
    def hello(self):
        return super().hello() + " -> from B"

print(B().hello())
```

```
from A -> from B
```

```python
# Example 2: super() in __init__ chains setup
class A:
    def __init__(self):
        self.a = "set by A"

class B(A):
    def __init__(self):
        super().__init__()
        self.b = "set by B"

x = B()
print(x.a, x.b)
```

```
set by A set by B
```

```python
# Example 3: Without super() — parent fields missing
class A:
    def __init__(self):
        self.a = 1

class B(A):
    def __init__(self):
        # forgot super().__init__()
        self.b = 2

x = B()
print(x.b)        # OK
# print(x.a)      # AttributeError if uncommented
```

```
2
```

```python
# Example 4: super() works without arguments inside a method
class A:
    def greet(self): return "Hi"

class B(A):
    def greet(self):
        return super().greet() + " there"

print(B().greet())
```

```
Hi there
```

```python
# Example 5: super() inside a class body needs explicit form
class A:
    pass

# x = super()       # RuntimeError: super(): no arguments
x = super(A, A)     # this is the explicit form
print(x)            # a super proxy, no useful output but no error
```

```
<super: <class 'A'>, <A object>>
```

## **Why `super()` Exists — The Problem It Solves**

Without `super()`, you would have to call the parent by name:

```python
class Child(Parent):
    def __init__(self, x, y):
        Parent.__init__(self, x)        # hardcoded parent
        self.y = y
```

That works, but it has three problems:

- If you rename the parent class, you have to update every place it is referenced.
- In multiple inheritance, hardcoded calls miss the MRO and can skip parents.
- It is harder to read because the relationship between classes is hidden in the names.

`super()` fixes all three:

```python
class Child(Parent):
    def __init__(self, x, y):
        super().__init__(x)            # always uses the correct next class
        self.y = y
```

### **Examples**

```python
# Example 1: Hardcoded call breaks if parent is renamed
class A:
    def hello(self): return "A"
class B(A):
    def hello(self):
        A.hello(self)            # hardcoded
        return "B"

print(B().hello())
# If you rename A to AA, every B method that says A.hello(self) breaks.
```

```
A
B
```

```python
# Example 2: super() does not depend on the parent's name
class A:
    def hello(self): return "A"
class B(A):
    def hello(self):
        super().hello()
        return "B"

print(B().hello())
```

```
A
B
```

```python
# Example 3: Diamond — super() visits A only once
class A:
    def m(self): print("A")
class B(A):
    def m(self):
        print("B")
        super().m()
class C(A):
    def m(self):
        print("C")
        super().m()
class D(B, C):
    def m(self):
        print("D")
        super().m()

D().m()
```

```
D
B
C
A
```

```python
# Example 4: Hardcoded call in the same diamond — A runs twice
class A:
    def m(self): print("A")
class B(A):
    def m(self):
        print("B")
        A.m(self)                # hardcoded
class C(A):
    def m(self):
        print("C")
        A.m(self)                # hardcoded
class D(B, C):
    def m(self):
        print("D")

D().m()
```

```
D
B
A
C
A
```

```python
# Example 5: Using class name in MRO
class D(B, C):
    def m(self):
        print("D")
        B.m(self)        # jumps to B
        C.m(self)        # jumps to C
        A.m(self)        # jumps to A

# That is the price of hardcoding — you have to know the chain.
```

## **`super()` in the Constructor — The Most Common Use**

This is the pattern you will use most. The child calls the parent's `__init__` to set up the fields the parent is responsible for, then sets up its own.

```python
class Person:
    def __init__(self, name, age, height, weight):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight

    def display(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Height: {self.height}")
        print(f"Weight: {self.weight}")

class Student(Person):
    def __init__(self, name, age, height, weight, rollno, marks):
        super().__init__(name, age, height, weight)
        self.rollno = rollno
        self.marks = marks

    def display(self):
        super().display()
        print(f"Roll No: {self.rollno}")
        print(f"Marks: {self.marks}")

s = Student("Akshay", 23, 5.5, 50, 101, 80)
s.display()
```

```
Name: Akshay
Age: 23
Height: 5.5
Weight: 50
Roll No: 101
Marks: 80
```

Two important things to notice:

- `super().__init__(name, age, height, weight)` runs the parent's setup on the same `self` (the child object). That is what puts `name`, `age`, `height`, `weight` on the Student instance.
- `super().display()` inside the child's `display` reuses the parent's version and adds the student's fields. This is the standard way to extend rather than replace.

### **Without `super().__init__`, the child has no parent fields**

```python
class P:
    def __init__(self):
        self.parent_field = "I am from P"

class C(P):
    def __init__(self):
        # forgot to call super().__init__()
        self.child_field = "I am from C"

c = C()
print(c.child_field)
# print(c.parent_field)   # AttributeError
```

If you forget `super().__init__()`, the parent's fields do not exist on the child object. This is one of the most common bugs in inheritance-based code.

### **Examples**

```python
# Example 1: Standard pattern — extend parent constructor
class Animal:
    def __init__(self, species):
        self.species = species

class Dog(Animal):
    def __init__(self, name):
        super().__init__("Dog")
        self.name = name

d = Dog("Bruno")
print(d.species, d.name)
```

```
Dog Bruno
```

```python
# Example 2: Add new fields on top of parent fields
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class Admin(User):
    def __init__(self, name, email, level):
        super().__init__(name, email)
        self.level = level

a = Admin("Om", "o@x.com", 3)
print(a.name, a.email, a.level)
```

```
Om o@x.com 3
```

```python
# Example 3: super() before any other code
class Base:
    def __init__(self):
        print("Base init")
class Child(Base):
    def __init__(self):
        super().__init__()
        print("Child init")

Child()
```

```
Base init
Child init
```

```python
# Example 4: Pass arguments up
class A:
    def __init__(self, x):
        self.x = x

class B(A):
    def __init__(self, x, y):
        super().__init__(x)
        self.y = y

b = B(1, 2)
print(b.x, b.y)
```

```
1 2
```

```python
# Example 5: Three-level chain
class A:
    def __init__(self):
        self.a = "A"
class B(A):
    def __init__(self):
        super().__init__()
        self.b = "B"
class C(B):
    def __init__(self):
        super().__init__()
        self.c = "C"

c = C()
print(c.a, c.b, c.c)
```

```
A B C
```

```python
# Example 6: Forgetting super loses parent fields
class A:
    def __init__(self):
        self.x = 1

class B(A):
    def __init__(self):
        # forgot super().__init__()
        self.y = 2

b = B()
print("y =", b.y)
# print("x =", b.x)    # AttributeError
```

```
y = 2
```

## **`super()` with Methods — Calling the Parent Version**

`super()` is not just for constructors. Any parent method can be called this way.

```python
class P:
    a = 10

    def __init__(self):
        print("Parent constructor")

    def m1(self):
        print("Parent instance method")

    @classmethod
    def m2(cls):
        print("Parent class method")

    @staticmethod
    def m3():
        print("Parent static method")

class C(P):
    def __init__(self):
        print("Child constructor")

    def method(self):
        print("Parent static value =", super().a)
        super().m1()
        super().m2()
        super().m3()
        super().__init__()

c = C()
c.method()
```

```
Child constructor
10
Parent instance method
Parent class method
Parent static method
Parent constructor
```

### **What `super()` Can and Cannot Reach**

`super()` only gives you access to the **parent class's namespace**, not to the current instance's instance variables.

```python
class P:
    a = 10
    def __init__(self):
        self.b = 20

class C(P):
    a = 999

    def __init__(self):
        super().__init__()
        self.b = 30

    def m1(self):
        print("self.a   =", self.a)        # instance/child lookup: 999
        print("self.b   =", self.b)        # instance variable: 30
        print("super().a =", super().a)    # parent class variable: 10
        # print("super().b =", super().b)  # AttributeError

c = C()
c.m1()
```

```
self.a   = 999
self.b   = 30
super().a = 10
```

Rule of thumb:

- For **class variables** (static variables), use `super().var` or `self.var` — both work.
- For **instance variables**, always use `self.var`. `super().var` does not work because the parent's `self` is not the child's.

### **Examples**

```python
# Example 1: Reuse a parent method and add more
class Logger:
    def log(self, msg):
        return f"[LOG] {msg}"

class TimestampedLogger(Logger):
    def log(self, msg):
        from datetime import datetime
        return f"{super().log(msg)} at {datetime.now().isoformat()}"

print(TimestampedLogger().log("ready"))
```

```
[LOG] ready at 2025-04-12T10:30:00.000000
```

```python
# Example 2: Override but call parent for the default
class Shape:
    def describe(self): return "shape"

class Circle(Shape):
    def describe(self):
        return f"{super().describe()} -> circle"

print(Circle().describe())
```

```
shape -> circle
```

```python
# Example 3: super() to read a parent class variable
class P:
    name = "Parent"

class C(P):
    name = "Child"
    def show(self):
        print("self.name   =", self.name)
        print("super().name =", super().name)

C().show()
```

```
self.name   = Child
super().name = Parent
```

```python
# Example 4: Extend a method to do extra work
class Validator:
    def validate(self, value):
        return value is not None

class NonEmptyValidator(Validator):
    def validate(self, value):
        if not super().validate(value):
            return False
        return len(str(value)) > 0

print(NonEmptyValidator().validate("hi"))
print(NonEmptyValidator().validate(""))
print(NonEmptyValidator().validate(None))
```

```
True
False
False
```

```python
# Example 5: super() with __str__
class User:
    def __str__(self):
        return f"User"

class Admin(User):
    def __str__(self):
        return f"Admin(extends {super().__str__()})"

print(Admin())
```

```
Admin(extends User)
```

```python
# Example 6: super().attr is read-only through super
class P:
    a = 10

class C(P):
    def show(self):
        print(super().a)
        # super().a = 99    # AttributeError: 'super' object has no attribute 'a' setter

C().show()
```

```
10
```

## **`super()` from Inside Different Method Types**

The rules below are the part people get wrong most often. Memorize them and you will never be confused.

### **From a Constructor or Instance Method — `super()` Can Call Anything**

From a constructor or an instance method, `super()` can reach:

- The parent class's constructor
- The parent class's instance methods
- The parent class's class methods
- The parent class's static methods
- The parent class's static variables

```python
class P:
    def __init__(self):
        print("Parent constructor")
    def m1(self):
        print("Parent instance method")
    @classmethod
    def m2(cls):
        print("Parent class method")
    @staticmethod
    def m3():
        print("Parent static method")

class C(P):
    def __init__(self):
        super().__init__()
        super().m1()
        super().m2()
        super().m3()

c = C()
```

```
Parent constructor
Parent instance method
Parent class method
Parent static method
```

### **From a Class Method — `super()` Can Reach Only Class and Static Methods**

From a class method, `super()` can reach:

- The parent class's class methods
- The parent class's static methods

It **cannot** reach the parent constructor or instance method, because there is no `self` to bind to from a class method.

```python
class P:
    def __init__(self):
        print("Parent constructor")
    def m1(self):
        print("Parent instance method")
    @classmethod
    def m2(cls):
        print("Parent class method")
    @staticmethod
    def m3():
        print("Parent static method")

class C(P):
    @classmethod
    def method(cls):
        # super().__init__()    # AttributeError: 'super' object has no __init__
        # super().m1()          # RuntimeError
        super().m2()              # works
        super().m3()              # works

C.method()
```

```
Parent class method
Parent static method
```

### **Workaround — Calling Parent Instance Methods from a Class Method**

You can still do it, but you have to construct the call manually with `super(SubClass, cls)` and pass the class as if it were an instance:

```python
class A:
    def __init__(self):
        print("Parent constructor")
    def m1(self):
        print("Parent instance method")

class B(A):
    @classmethod
    def m2(cls):
        super(B, cls).__init__(cls)    # pass cls as the first arg
        super(B, cls).m1(cls)

B.m2()
```

```
Parent constructor
Parent instance method
```

This works, but it is ugly. In real code, if you need to call an instance method from a class method, the cleaner answer is usually to make the caller an instance method too.

### **From a Static Method — `super()` Cannot Be Used Directly**

A static method has no `cls` and no `self`, so the default `super()` call has nothing to bind to.

```python
class P:
    @staticmethod
    def m3():
        print("Parent static method")

class C(P):
    @staticmethod
    def m1():
        # super().m3()    # RuntimeError: super(): no arguments
        pass
```

You can still reach parent static methods by being explicit:

```python
class A:
    @staticmethod
    def m1():
        print("Parent static method")

class B(A):
    @staticmethod
    def m2():
        super(B, B).m1()    # pass the class itself twice

B.m2()
```

```
Parent static method
```

Again, in real code, you almost never need to call a static method via `super()` from another static method. The cleanest fix is usually to make the caller an instance or class method.

### **Summary of the Rules**

| From this method type | `super()` can call | `super()` cannot call |
|---|---|---|
| Instance method / constructor | constructor, instance, class, static methods; class variables | instance variables (use `self`) |
| Class method | class, static methods | constructor, instance methods (no `self`) |
| Static method | (nothing by default) | (everything, without manual `super(Sub, Sub).x()` workaround) |

### **Examples**

```python
# Example 1: From constructor — call all four kinds
class P:
    def __init__(self): print("P ctor")
    def m1(self): print("P inst")
    @classmethod
    def m2(cls): print("P cls")
    @staticmethod
    def m3(): print("P static")

class C(P):
    def __init__(self):
        super().__init__()
        super().m1()
        super().m2()
        super().m3()

C()
```

```
P ctor
P inst
P cls
P static
```

```python
# Example 2: From instance method — same powers
class P:
    def m1(self): print("P inst")
    @classmethod
    def m2(cls): print("P cls")
    @staticmethod
    def m3(): print("P static")

class C(P):
    def call_all(self):
        super().m1()
        super().m2()
        super().m3()

C().call_all()
```

```
P inst
P cls
P static
```

```python
# Example 3: From class method — only class and static
class P:
    def m1(self): print("P inst")
    @classmethod
    def m2(cls): print("P cls")
    @staticmethod
    def m3(): print("P static")

class C(P):
    @classmethod
    def call_some(cls):
        super().m2()
        super().m3()
        # super().m1()    # RuntimeError

C.call_some()
```

```
P cls
P static
```

```python
# Example 4: From class method — calling parent instance method via explicit form
class A:
    def __init__(self): print("A init")
    def m1(self): print("A m1")

class B(A):
    @classmethod
    def call(cls):
        super(B, cls).__init__(cls)    # A.__init__ via super
        super(B, cls).m1(cls)          # A.m1 via super

B.call()
```

```
A init
A m1
```

```python
# Example 5: From static method — needs explicit form too
class A:
    @staticmethod
    def m1(): print("A static")

class B(A):
    @staticmethod
    def call():
        super(B, B).m1()      # explicit form

B.call()
```

```
A static
```

```python
# Example 6: Try uncommenting the wrong combinations to see the error
class P:
    def __init__(self): print("P ctor")
    def m1(self): print("P inst")

class C(P):
    @staticmethod
    def bad():
        # super().__init__()    # RuntimeError
        # super().m1()          # RuntimeError
        pass

C.bad()
print("done")
```

```
done
```

## **Calling a Specific Parent's Method — Skipping the MRO**

Sometimes you want to call a method from a particular ancestor, not just the next one in line. There are two ways.

### **Way 1 — By Name**

```python
class A:
    def m1(self):
        print("A class Method")

class B(A):
    def m1(self):
        print("B class Method")

class C(B):
    def m1(self):
        print("C class Method")

class D(C):
    def m1(self):
        print("D class Method")

class E(D):
    def m1(self):
        B.m1(self)        # skip A, skip C, skip D, call B's m1
        A.m1(self)        # call A's m1 directly

e = E()
e.m1()
```

```
B class Method
A class Method
```

This works, but it is hardcoded — if `B` ever gets renamed, this code breaks.

### **Way 2 — `super(SubClass, self)`**

The two-argument form of `super()` lets you say "starting from this point in the MRO, give me the next class up."

```python
class A:
    def m1(self):
        print("a m1")

class B(A):
    def m1(self):
        print("b m1")

class C(B):
    def m1(self):
        print("c m1")

class D(C):
    def m1(self):
        print("d m1")

class E(D):
    def m1(self):
        B.m1(self)                          # call B.m1 directly
        super(D, self).m1()                 # call the parent of D, i.e. C.m1

ee = E()
ee.m1()
```

```
b m1
c m1
```

`super(D, self).m1()` is read as: "Treat the MRO as if we were inside D, and call the next class's `m1`." The next class after D in the chain is C, so this calls `C.m1`.

This pattern is useful when a class wants to skip exactly one level, but still respect the rest of the MRO.

### **Examples**

```python
# Example 1: Call by name to skip a level
class A:
    def m(self): return "A"
class B(A):
    def m(self): return "B"
class C(B):
    def m(self): return "C"
class D(C):
    def m(self):
        # skip C, jump to B
        return B.m(self) + " from D"

print(D().m())
```

```
B from D
```

```python
# Example 2: Use super(SubClass, self) to skip exactly one level
class A:
    def m(self): return "A"
class B(A):
    def m(self): return "B"
class C(B):
    def m(self): return "C"
class D(C):
    def m(self):
        # skip C, find next after C in MRO of D, which is B
        return super(C, self).m() + " from D"

print(D().m())
```

```
B from D
```

```python
# Example 3: Print the MRO alongside the call
class A: pass
class B(A): pass
class C(B): pass
class D(C): pass

print("MRO of D:", [cls.__name__ for cls in D.__mro__])
# super(C, self) means: "start the MRO at the class after C"
# so super(C, self).m() walks: D, then C is skipped, then B
```

```
MRO of D: ['D', 'C', 'B', 'A', 'object']
```

```python
# Example 4: Difference between super(D) and super(C)
class A:
    def m(self): return "A"
class B(A):
    def m(self): return "B"
class C(B):
    def m(self): return "C"
class D(C):
    def m(self):
        results = []
        # super(D) - normal usage, gets next = C
        # We have to call via class to actually invoke
        from types import FunctionType
        # easier: hardcode for the demo
        results.append("via super(C,self) = " + super(C, self).m())  # B
        results.append("via super(B,self) = " + super(B, self).m())  # A
        return results

print(D().m())
```

```
['via super(C,self) = B', 'via super(B,self) = A']
```

```python
# Example 5: When to use — coordinating two parents
class Logger:
    def header(self): return "[LOG]"

class Timestamper:
    def header(self): return "[10:30]"

class Service(Logger, Timestamper):
    def header(self):
        # Want Logger's header, not Timestamper's
        return Logger.header(self)

print(Service().header())
```

```
[LOG]
```

## **`super()` in Multiple Inheritance — The Real Power**

In a diamond shape, multiple parents share a common grandparent. `super()` makes sure the grandparent's code runs **once**, not three times.

```python
class A:
    def m1(self):
        print("A m1")

class B(A):
    def m1(self):
        print("B m1")
        super().m1()                  # call A's m1

class C(A):
    def m1(self):
        print("C m1")
        super().m1()                  # call A's m1

class D(B, C):
    def m1(self):
        print("D m1")
        super().m1()                  # MRO walks B → C → A, but A only runs once

d = D()
d.m1()
print(D.mro())
```

```
D m1
B m1
C m1
A m1
[<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>]
```

The MRO visits A **once** even though both B and C inherit from it. This is what `super()` is designed to handle — without it, you would have to write `A.m1(self)` manually, and you would have to know where A is in the chain.

### **Examples**

```python
# Example 1: Diamond with super() in each link
class A:
    def m(self): print("A")
class B(A):
    def m(self):
        print("B")
        super().m()
class C(A):
    def m(self):
        print("C")
        super().m()
class D(B, C):
    def m(self):
        print("D")
        super().m()

D().m()
print(D.mro())
```

```
D
B
C
A
[<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>]
```

```python
# Example 2: A runs only once thanks to super()
# vs. hardcoded A.m(self) which would run A twice.
class A:
    def m(self): print("A")
class B(A):
    def m(self):
        print("B")
        A.m(self)        # hardcoded
class C(A):
    def m(self):
        print("C")
        A.m(self)        # hardcoded
class D(B, C):
    def m(self):
        print("D")
        B.m(self)        # hardcoded
        C.m(self)        # hardcoded

D().m()
```

```
D
B
A
C
A
```

```python
# Example 3: Mixin chain
class JsonMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)
class LogMixin:
    def log(self, msg):
        print(f"[LOG] {msg}")
class User(JsonMixin, LogMixin):
    pass

u = User()
u.name = "Karan"
print(u.to_json())
u.log("created")
```

```
{"name": "Karan"}
[LOG] created
```

```python
# Example 4: super() with __init__ in a diamond
class A:
    def __init__(self):
        print("A init")
class B(A):
    def __init__(self):
        super().__init__()
        print("B init")
class C(A):
    def __init__(self):
        super().__init__()
        print("C init")
class D(B, C):
    def __init__(self):
        super().__init__()
        print("D init")

D()
```

```
A init
C init
B init
D init
```

```python
# Example 5: Print MRO to predict the order
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

for cls in D.__mro__:
    print(cls.__name__)
```

```
D
B
C
A
object
```

## **`super()` in Frameworks — Real Patterns You Will See**

### **Pydantic-style Validator Chain**

Pydantic's validators are typically `super()`-chained. The pattern below mirrors what `BaseModel` does internally.

```python
class BaseModel:
    def __init__(self, **data):
        self._validate(data)
        for k, v in data.items():
            setattr(self, k, v)

    def _validate(self, data):
        pass    # subclasses override

class User(BaseModel):
    def _validate(self, data):
        super()._validate(data)
        if "email" in data and "@" not in data["email"]:
            raise ValueError("invalid email")

u = User(name="Karan", email="k@x.com")
print(u.name, u.email)
```

```
Karan k@x.com
```

### **Django-style Model Save**

Django's `Model.save()` extends the base and lets subclasses add their own logic.

```python
class BaseModel:
    def save(self):
        print("BaseModel.save: writing to database")
        self.after_save()

    def after_save(self):
        pass

class User(BaseModel):
    def after_save(self):
        print("User.after_save: clearing cache")

User().save()
```

```
BaseModel.save: writing to database
User.after_save: clearing cache
```

### **unittest-style setUp/tearDown**

`unittest.TestCase` chains `setUp` and `tearDown` across the inheritance chain. The pattern looks like this:

```python
class BaseTest:
    def setUp(self):
        print("BaseTest.setUp: creating test data")

class UserTest(BaseTest):
    def setUp(self):
        super().setUp()                  # run parent setup first
        print("UserTest.setUp: creating users")

UserTest().setUp()
```

```
BaseTest.setUp: creating test data
UserTest.setUp: creating users
```

### **Logging Configuration**

```python
class BaseService:
    def __init__(self, name):
        self.name = name
        print(f"[{self.name}] BaseService ready")

class UserService(BaseService):
    def __init__(self):
        super().__init__("UserService")
        print(f"[{self.name}] user-specific setup done")

UserService()
```

```
[UserService] BaseService ready
[UserService] user-specific setup done
```

### **Examples**

```python
# Example 1: Pydantic-style chain
class BaseModel:
    def __init__(self, **data):
        self._validate(data)
        for k, v in data.items():
            setattr(self, k, v)
    def _validate(self, data):
        pass

class PositiveIntModel(BaseModel):
    def _validate(self, data):
        super()._validate(data)
        for k, v in data.items():
            if isinstance(v, int) and v < 0:
                raise ValueError(f"{k} must be non-negative")

PositiveIntModel(age=22, score=89)
print(PositiveIntModel(age=22, score=89).age)
```

```
22
```

```python
# Example 2: Django-style save chain
class Model:
    def save(self):
        print("saving to db")
        self.after_save()
    def after_save(self):
        pass

class CachedModel(Model):
    def after_save(self):
        super().after_save() if hasattr(super(), "after_save") else None
        print("clearing cache")

CachedModel().save()
```

```
saving to db
clearing cache
```

```python
# Example 3: Test setUp chain
class BaseTest:
    def setUp(self):
        print("base setup")
class UserTest(BaseTest):
    def setUp(self):
        super().setUp()
        print("user test setup")

UserTest().setUp()
```

```
base setup
user test setup
```

```python
# Example 4: Logging configuration chain
class BaseService:
    def __init__(self, name):
        self.name = name
        print(f"[{self.name}] base ready")
class PaymentService(BaseService):
    def __init__(self):
        super().__init__("Payment")
        print(f"[{self.name}] payment-specific ready")

PaymentService()
```

```
[Payment] base ready
[Payment] payment-specific ready
```

```python
# Example 5: Cache + Log mixin
class JsonMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)
class LogMixin:
    def log(self, msg):
        print(f"[LOG] {msg}")
class Service(JsonMixin, LogMixin):
    def __init__(self, name):
        self.name = name
        self.log(f"Service {name} created")

s = Service("orders")
print(s.to_json())
```

```
[LOG] Service orders created
{"name": "orders"}
```

## **`super()` in `__init_subclass__` and `__new__` (Advanced Brief)**

These are less common in everyday Python, but worth knowing.

`__init_subclass__` is a class method on `object` that runs when a subclass is **defined**, not when an instance is created. It is how `abc.ABC`, `enum.Enum`, and `dataclasses.dataclass` wire up their subclasses.

```python
class Plugin:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        print(f"Registered new plugin: {cls.__name__}")

class JsonPlugin(Plugin):
    pass

class CsvPlugin(Plugin):
    pass
```

```
Registered new plugin: JsonPlugin
Registered new plugin: CsvPlugin
```

`__new__` is the method that actually creates the object (before `__init__`). It is also a class method, so the same rules apply: `super().__new__(cls)` is the way to let the parent's `__new__` run.

```python
class MyList(list):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        return instance

m = MyList([1, 2, 3])
print(m, type(m).__name__)
```

```
[1, 2, 3] MyList
```

For most everyday work, you do not need to touch `__new__` or `__init_subclass__`. They are there for library authors.

### **Examples**

```python
# Example 1: __init_subclass__ runs at class definition
class Plugin:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        print(f"Registered: {cls.__name__}")

class JsonPlugin(Plugin): pass
class CsvPlugin(Plugin): pass
```

```
Registered: JsonPlugin
Registered: CsvPlugin
```

```python
# Example 2: __init_subclass__ with kwargs
class Versioned:
    def __init_subclass__(cls, version, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.version = version
        print(f"{cls.__name__} version {version}")

class ApiV1(Versioned, version="1.0"): pass
class ApiV2(Versioned, version="2.0"): pass
```

```
ApiV1 version 1.0
ApiV2 version 2.0
```

```python
# Example 3: __new__ for an immutable list
class ImmutableList(list):
    def __new__(cls, *args):
        return super().__new__(cls)

    def append(self, value):
        raise RuntimeError("ImmutableList cannot be modified")

xs = ImmutableList([1, 2, 3])
print(xs)
# xs.append(4)    # RuntimeError
```

```
[1, 2, 3]
```

```python
# Example 4: __new__ returning a different class is allowed
class AlwaysStr(str):
    def __new__(cls, value):
        if not isinstance(value, str):
            value = str(value)
        return super().__new__(cls, value)

print(type(AlwaysStr(42)))   # AlwaysStr, not int
print(AlwaysStr(42))         # "42"
```

```
<class '__main__.AlwaysStr'>
42
```

```python
# Example 5: super() in __init_subclass__ to keep the chain alive
class Registry:
    registry = []
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Registry.registry.append(cls)

class A(Registry): pass
class B(Registry): pass
class C(B): pass       # nested

print(Registry.registry)
```

```
[<class '__main__.A'>, <class '__main__.B'>, <class '__main__.C'>]
```

## **Common Mistakes with `super()`**

### **1. Forgetting to call `super().__init__()` in the child**

```python
class P:
    def __init__(self):
        self.x = 10

class C(P):
    def __init__(self):
        # forgot super().__init__()
        self.y = 20

c = C()
# print(c.x)   # AttributeError
```

The child looks like it inherits from P, but `c.x` does not exist. Easy to miss until something tries to use it.

### **2. Trying to access instance variables via `super()`**

```python
class P:
    def __init__(self):
        self.b = 20

class C(P):
    def m1(self):
        # super().b     # AttributeError: 'super' object has no attribute 'b'
        pass
```

`super()` is not the same as `self`. It only gives you the parent's class namespace. Use `self` for instance variables.

### **3. Using `super()` from a static method without arguments**

```python
class P:
    @staticmethod
    def m3():
        print("parent")

class C(P):
    @staticmethod
    def m1():
        super().m3()    # RuntimeError: super(): no arguments
```

The fix is to use the explicit form `super(C, C).m3()` or to change the method to a class method.

### **4. Hardcoding the parent class name**

```python
class C(P):
    def __init__(self):
        P.__init__(self)   # works, but fragile
        super().__init__() # better
```

The first form does not respect the MRO. The second form does. Always prefer `super()`.

### **5. Calling `super()` outside a class method or instance method**

`super()` only works inside a method. Calling it in a top-level expression or in `__init__` of a top-level class is fine, but in a class body, it raises `RuntimeError`.

```python
class C:
    x = super()   # RuntimeError: super(): no arguments
```

This is rarely a real problem, but worth knowing.

### **Examples**

```python
# Example 1: Forgetting super().__init__
class P:
    def __init__(self):
        self.x = 1

class C(P):
    def __init__(self):
        # forgot super
        self.y = 2

c = C()
# print(c.x)   # AttributeError if uncommented
print("y is set, x is missing")
```

```
y is set, x is missing
```

```python
# Example 2: super() with instance variable
class P:
    def __init__(self):
        self.b = 20

class C(P):
    def m1(self):
        try:
            print(super().b)
        except AttributeError as e:
            print("AttributeError:", e)

C().m1()
```

```
AttributeError: 'super' object has no attribute 'b'
```

```python
# Example 3: super() in static method without args
class P:
    @staticmethod
    def m3():
        print("parent")

class C(P):
    @staticmethod
    def m1():
        try:
            super().m3()
        except RuntimeError as e:
            print("RuntimeError:", e)

C.m1()
```

```
RuntimeError: super(): no arguments
```

```python
# Example 4: Hardcoded parent (works but fragile)
class P:
    def __init__(self): print("P init")

class C(P):
    def __init__(self):
        P.__init__(self)   # hardcoded

C()
```

```
P init
```

```python
# Example 5: super() at class level (outside any method)
class C:
    # x = super()    # SyntaxError / RuntimeError depending on Python version
    pass
print("class body can't call super() without arguments")
```

```
class body can't call super() without arguments
```

## **Quick Reference Summary**

### **What `super()` Returns**

A proxy object that delegates method calls to the next class in the MRO. You use it like a normal object — calling methods on it runs them on the parent.

### **Common Forms**

| Form | When to use |
|---|---|
| `super().__init__(...)` | In a child constructor, to run the parent's setup. |
| `super().method(...)` | In a child method, to extend (not replace) a parent method. |
| `super().attr` | To read a parent class variable. |
| `super(SubClass, self).m()` | To call a specific ancestor's method, skipping the immediate parent. |
| `Parent.method(self)` | The hardcoded fallback. Avoid it when `super()` works. |

### **What `super()` Can Reach**

| From this context | Can call via `super()` | Cannot call via `super()` |
|---|---|---|
| Constructor | constructor, instance, class, static methods; class variables | instance variables (use `self`) |
| Instance method | constructor, instance, class, static methods; class variables | instance variables (use `self`) |
| Class method | class, static methods; class variables | constructor, instance methods (no `self`) |
| Static method | (only with explicit `super(Sub, Sub).x()`) | (everything by default) |

### **When to Use `super()`**

| Situation | Use `super()` |
|---|---|
| Child constructor needs parent's setup | Yes — `super().__init__(...)` |
| Child method should extend, not replace | Yes — `super().method(...)` then add more |
| Multiple inheritance with diamond shape | Yes — ensures each ancestor runs once |
| Single inheritance, no name conflict | Yes — still preferred for clarity and future-proofing |
| Need to skip one level in the MRO | Use `super(SubClass, self).method(...)` |
| Need to call a specific ancestor by name | Use `ParentClass.method(self)` as a last resort |
