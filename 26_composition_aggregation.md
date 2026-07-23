# **HAS-A Relationship — Composition and Aggregation**

## **Using Members of One Class Inside Another Class**

There are two ways a class can use the members (attributes and methods) of another class:

1. **HAS-A relationship** — by using **Composition** or **Aggregation** (the containing class has a reference to the other class).
2. **IS-A relationship** — by using **Inheritance** (the new class extends the existing class). Covered in `python_inheritance.md`.

This file covers the HAS-A side in detail. The IS-A side is the topic of the inheritance file.

## **HAS-A Relationship — The Idea**

In a HAS-A relationship, one class **contains a reference to** an object of another class. The containing class is built on top of the contained one — it does not inherit from it, it just *uses* it.

The classic example: a `Car` HAS-A `Engine`. The car has an engine as one of its parts. The car is not a kind of engine; it just has one.

This pattern gives you two big benefits:

- **Code reusability** — the existing class's functionality is reused without copying it.
- **Loose coupling** — the containing class does not depend on the internal implementation of the contained class, just its public interface.

## **IS-A vs HAS-A**

Two different design decisions come up all the time when you have multiple classes that work together.

### **IS-A Relationship — Inheritance**

Use inheritance when the child class **is a specialized version** of the parent class. The child extends what the parent can do.

- An `Employee` IS-A `Person`.
- A `CarLoan` IS-A `Loan`.
- A `Square` IS-A `Rectangle` (debatable, but a common example).
- A `SavingsAccount` IS-A `BankAccount`.

The technical shape: `class Child(Parent)`.

### **HAS-A Relationship — Composition**

Use composition when one class **contains or uses** another class as a part of its data. The containing class is not a kind of the contained one — it just has one.

- An `Employee` HAS-A `Car` (for a company car).
- A `BankAccount` HAS-A `Customer` as its owner.
- A `Library` HAS-A list of `Book`s.
- A `Car` HAS-A `Engine`.

The technical shape: store an object of the other class as an instance variable, or call it as a local inside a method.

### **A Quick Example Combining Both**

This example shows IS-A (`Employee` extends `Person`) and HAS-A (`Employee` has a `Car`) at the same time. This is a real pattern in domain modeling.

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

The decision rule:

- If you want to **extend** existing functionality with more functionality, use IS-A (inheritance).
- If you want to **use** existing functionality as-is, use HAS-A (composition).

### **Examples**

```python
# Example 1: IS-A — child extends parent
class Shape:
    def describe(self):
        return "I am a shape"

class Circle(Shape):
    def describe(self):
        return super().describe() + " and I am a circle"

print(Circle().describe())
```

```
I am a shape and I am a circle
```

```python
# Example 2: HAS-A — class uses another class
class Engine:
    def start(self):
        return "engine running"

class Car:
    def __init__(self):
        self.engine = Engine()        # HAS-A

    def start(self):
        return f"car started ({self.engine.start()})"

print(Car().start())
```

```
car started (engine running)
```

```python
# Example 3: Both at the same time
class Address:
    def __init__(self, city, country):
        self.city = city
        self.country = country

class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address        # HAS-A

class Employee(Person):                # IS-A
    def __init__(self, name, address, eid):
        super().__init__(name, address)
        self.eid = eid

e = Employee("Karan", Address("Mumbai", "India"), 101)
print(e.name, e.address.city, e.eid)
```

```
Karan Mumbai 101
```

```python
# Example 4: Wrong design — using IS-A when HAS-A fits
class Engine:
    def hp(self): return 200

# BAD: a Car is NOT a kind of Engine
class Car(Engine):
    pass

c = Car()
print(c.hp())    # works, but semantically wrong

# GOOD: a Car HAS an Engine
class Car2:
    def __init__(self):
        self.engine = Engine()

c2 = Car2()
print(c2.engine.hp())
```

```
200
200
```

```python
# Example 5: Test the IS-A relationship with isinstance
class Animal: pass
class Dog(Animal): pass

d = Dog()
print("d is Dog    ->", isinstance(d, Dog))     # yes
print("d is Animal ->", isinstance(d, Animal))  # yes, because of IS-A
print("d is int    ->", isinstance(d, int))     # no

# HAS-A relationship would not pass this test
class Collar: pass
class Dog2:
    def __init__(self):
        self.collar = Collar()        # HAS-A only

d2 = Dog2()
print("d2 has Collar object ->", isinstance(d2.collar, Collar))   # yes
print("d2 is Collar          ->", isinstance(d2, Collar))         # no
```

```
d is Dog    -> True
d is Animal -> True
d is int    -> False
d2 has Collar object -> True
d2 is Collar          -> False
```

## **Composition vs Aggregation — The Two Flavors of HAS-A**

Both Composition and Aggregation are HAS-A relationships, but they describe how tightly the two classes are bound.

### **Composition — Strong Association**

If the contained object **cannot exist** without the container object, the relationship is **composition**. The lifetime of the contained object is tied to the container's. When the container is destroyed, the contained one goes with it.

The classic example: a `University` contains `Department`s. Without a university, departments do not exist independently.

```python
class University:
    def __init__(self, name):
        self.name = name
        self.department = self.Department()      # Department is created inside

    class Department:
        def __init__(self):
            self.name = "Computer Science"
        def __str__(self):
            return self.name

u = University("Durgasoft University")
print(u.department)
```

```
Computer Science
```

The `Department` is created inside the `University` constructor and has no meaning on its own. That is composition.

Another classic example: a `Car` has an `Engine`. Without a car, the engine does not have a host.

```python
class Engine:
    def __init__(self) -> None:
        self.power = "125kw"

    def use_engine(self):
        print("Engine Specific Functionality!")


class Car:
    def __init__(self):
        self.engine = Engine()    # HAS-A — Car contains an Engine

    def use_car(self):
        print("Car required engine functionality!")
        self.engine.use_engine()
        print("The power of engine: ", self.engine.power)

c = Car()
c.use_car()
```

```
Car required engine functionality!
Engine Specific Functionality!
The power of engine:  125kw
```

What is happening:

- The `Car` constructor creates an `Engine` and stores it on `self.engine`.
- When `use_car` is called, it delegates the engine-specific work to `self.engine.use_engine()`.
- The car reuses the engine's behaviour without inheriting from it.

### **Aggregation — Weak Association**

If the contained object **can still exist** without the container, the relationship is **aggregation**. The contained object is created somewhere else and passed in.

The classic example: a `Department` has `Professor`s. A professor can exist without a department, and a professor can move between departments.

```python
class Professor:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name

class Department:
    def __init__(self, name, prof):
        self.name = name
        self.prof = prof        # Professor was created elsewhere

prof = Professor("Dr. Durga")
cs_dept = Department("CS", prof)
it_dept = Department("IT", prof)   # same professor, different department

print(cs_dept.prof)
print(it_dept.prof)
```

```
Dr. Durga
Dr. Durga
```

The same `Professor` object is shared across two `Department` objects. That is aggregation.

### **A Quick Rule of Thumb**

- The relationship between an **object and its instance variables** is always **composition**. The instance variable was created when the object was constructed, and lives with the object.
- The relationship between an **object and class-level (static) variables** is always **aggregation**. Static variables exist independently of any object.

```python
class Student:
    collageName = "DurgaSoft"   # static, lives on the class, not on any object

    def __init__(self, name):
        self.name = name        # instance, tied to the object

print(Student.collageName)     # aggregation
s = Student("Durga")           # composition
print(s.name)
```

```
DurgaSoft
Durga
```

### **Examples**

```python
# Example 1: Composition — created inside, dies with the owner
class Heart:
    def beat(self):
        return "thump"

class Person:
    def __init__(self, name):
        self.name = name
        self.heart = Heart()    # composition

p = Person("Karan")
print(p.heart.beat())
# Try: del p; the heart object goes with it.
```

```
thump
```

```python
# Example 2: Aggregation — created outside, lives on its own
class Address:
    def __init__(self, city):
        self.city = city

class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address    # aggregation

a = Address("Mumbai")
p1 = Person("Karan", a)
p2 = Person("Om", a)              # same address, two people
print(p1.address.city, p2.address.city)
print(p1.address is p2.address)   # True
```

```
Mumbai Mumbai
True
```

```python
# Example 3: Rule of thumb — instance var = composition, class var = aggregation
class Config:
    APP_NAME = "MyApp"        # class variable — aggregation

    def __init__(self, debug):
        self.debug = debug     # instance variable — composition

print(Config.APP_NAME)        # accessed through class, lives independently
c = Config(True)
print(c.debug, c.APP_NAME)    # accessed through object
```

```
MyApp
True MyApp
```

```python
# Example 4: Library with Books (composition)
class Book:
    def __init__(self, title):
        self.title = title

class Library:
    def __init__(self):
        self.books = []        # the library owns the list

    def add(self, book):
        self.books.append(book)

lib = Library()
lib.add(Book("Dune"))
lib.add(Book("Foundation"))
print([b.title for b in lib.books])
```

```
['Dune', 'Foundation']
```

```python
# Example 5: Team with Players (aggregation)
class Player:
    def __init__(self, name):
        self.name = name

class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players     # players exist independently

p1 = Player("Karan")
p2 = Player("Om")
t = Team("Backend", [p1, p2])
print([pl.name for pl in t.players])
```

```
['Karan', 'Om']
```

## **Employee Has-A Car — Composition in Practice**

A common real-world pattern: an employee is assigned a company car. The car is passed into the employee constructor, so the car is a real-world object that the employee gets to use. The employee does not own the car's existence — but the relationship is still HAS-A.

```python
class Car:
    def __init__(self, name, model, color) -> None:
        self.name = name
        self.model = model
        self.color = color

    def getInfo(self):
        print("Name: {}, Model {}, Color {}".format(self.name, self.model, self.color))


class Employee:
    def __init__(self, ename, id, car) -> None:
        self.ename = ename
        self.id = id
        self.car = car

    def empInfo(self):
        print(f"Employee name: {self.ename}")
        print(f"Employee id: {self.id}")
        print(f"Employee car info :")
        self.car.getInfo()

car = Car("Range rover", "2.5V", "Black")
e = Employee("Durga", "121", car)
e.empInfo()
```

```
Employee name: Durga
Employee id: 121
Employee car info :
Name: Range rover, Model 2.5V, Color Black
```

This is technically a hybrid — the car was created outside and passed in (which is aggregation), but the employee only has one car and that car is conceptually part of the employee's setup. The real distinction is whether the contained object has meaning without the container.

## **Code Without Composition — A Bad Pattern**

To see why composition helps, here is the same news-app scenario written without composition. Each news class is its own top-level class, and the news aggregator has to deal with each one independently.

```python
class SportsNews:
    def sportsInfo(self):
        print("Sports imformation 1")
        print("Sports imformation 2")
        print("Sports imformation 3")

class MovieNews:
    def movieInfo(self):
        print("Sports imformation 1")
        print("Sports imformation 2")
        print("Sports imformation 3")

class PoliticsNews:
    def politicsInfo(self):
        print("Sports imformation 1")
        print("Sports imformation 2")
        print("Sports imformation 3")

class DurgaNews:
    def __init__(self) -> None:
        self.sports = SportsNews()
        self.movies = MovieNews()
        self.politics = PoliticsNews()

    def getTotalNews(self):
        print("Welcome to durga news")
        self.sports.sportsInfo()
        self.movies.movieInfo()
        self.politics.politicsInfo()


d = DurgaNews()
d.getTotalNews()
```

```
Welcome to durga news
Sports imformation 1
Sports imformation 2
Sports imformation 3
Sports imformation 1
Sports imformation 2
Sports imformation 3
Sports imformation 1
Sports imformation 2
Sports imformation 3
```

`DurgaNews` holds three news categories, each from a different class. The aggregator reaches into each one to fetch its content. The duplication of "Sports imformation 1/2/3" is just for demo purposes.

## **Composition Done Two Ways — Inside vs Outside the Constructor**

There are two styles of composition. The difference is where the contained object is created.

### **Style 1 — Contained Object Created Inside the Container**

The container's `__init__` creates the contained object. The outside world does not see the contained object directly.

```python
class SportsNews:
    def sportsInfo(self):
        print("Sports imformation 1")
        print("Sports imformation 2")
        print("Sports imformation 3")

class MovieNews:
    def movieInfo(self):
        print("Sports imformation 1")
        print("Sports imformation 2")
        print("Sports imformation 3")

class PoliticsNews:
    def politicsInfo(self):
        print("Sports imformation 1")
        print("Sports imformation 2")
        print("Sports imformation 3")

class DurgaNews:
    def __init__(self) -> None:
        self.sports = SportsNews()
        self.movies = MovieNews()
        self.politics = PoliticsNews()

    def getTotalNews(self):
        print("Welcome to durga news")
        self.sports.sportsInfo()
        self.movies.movieInfo()
        self.politics.politicsInfo()


d = DurgaNews()
d.getTotalNews()
```

```
Welcome to durga news
Sports imformation 1
Sports imformation 2
Sports imformation 3
Sports imformation 1
Sports imformation 2
Sports imformation 3
Sports imformation 1
Sports imformation 2
Sports imformation 3
```

This is **composition** in the strictest sense. The `DurgaNews` object owns its three news sources — they are not passed in.

### **Style 2 — Contained Object Created Outside and Passed In**

The contained objects are created first, then handed to the container. This is more like **aggregation** — the contained objects exist independently.

```python
class SportsNews:
    def sportsInfo(self):
        print("Sports imformation 1")
        print("Sports imformation 2")
        print("Sports imformation 3")

class MovieNews:
    def movieInfo(self):
        print("Sports imformation 1")
        print("Sports imformation 2")
        print("Sports imformation 3")

class PoliticsNews:
    def politicsInfo(self):
        print("Sports imformation 1")
        print("Sports imformation 2")
        print("Sports imformation 3")

class DurgaNews:
    def __init__(self, sports, movies, politics) -> None:
        self.sports = sports
        self.movies = movies
        self.politics = politics

    def getTotalNews(self):
        print("Welcome to durga news")
        self.sports.sportsInfo()
        self.movies.movieInfo()
        self.politics.politicsInfo()


sports = SportsNews()
movies = MovieNews()
politics = PoliticsNews()
d = DurgaNews(sports, movies, politics)
d.getTotalNews()
```

```
Welcome to durga news
Sports imformation 1
Sports imformation 2
Sports imformation 3
Sports imformation 1
Sports imformation 2
Sports imformation 3
Sports imformation 1
Sports imformation 2
Sports imformation 3
```

Same output, but the construction is done by the caller. This is the dependency-injection style — the container does not know how to build the contained objects, it just uses them.

## **University Has-A Department, Department Has-A Professor**

A combined example showing both flavors:

- **University has-a Department** — composition. Without a university, the department does not exist.
- **Department has-a Professor** — aggregation. A professor can exist without a department, and a professor can move between departments.

```python
class University:
    def __init__(self, name):
        self.name = name
        self.department = self.Department()

    class Department:
        def __init__(self):
            self.professors = []    # aggregation — list of professor refs

        def add_prof(self, prof):
            self.professors.append(prof)

        def list_profs(self):
            return [p.name for p in self.professors]

class Professor:
    def __init__(self, name):
        self.name = name

u = University("DurgaSoft")
p1 = Professor("Dr. Durga")
p2 = Professor("Dr. Ravi")
u.department.add_prof(p1)
u.department.add_prof(p2)
print(u.department.list_profs())
```

```
['Dr. Durga', 'Dr. Ravi']
```

This pattern shows up in domain models all the time — the entity at the top owns its sub-entities, but the leaf entities (like professors) are independent actors.

## **Composition vs Aggregation — When to Use Each**

| Factor | Composition | Aggregation |
|---|---|---|
| Lifetime | Contained object dies with the container. | Contained object lives independently. |
| Construction | Created inside the container's constructor. | Created outside, passed in. |
| Typical use | Engine inside a Car. Department inside a University. | Department has a Professor. Team has a Player. |
| Symbol | Filled diamond ◆ in UML. | Empty diamond ◇ in UML. |
| Default for instance variables | Yes — instance vars are always composition. | No — used when you want to share an object. |

The general rule:

- If the contained object's existence **requires** the container → **composition**.
- If the contained object can stand on its own → **aggregation**.

## **When to Use HAS-A vs IS-A**

The two patterns answer different design questions:

- **IS-A (inheritance)** — when the new class is a *specialized version* of an existing one. The new class extends what the existing class can do.
  - An `Employee` IS-A `Person`.
  - A `SavingsAccount` IS-A `BankAccount`.
  - A `CarLoan` IS-A `Loan`.
- **HAS-A (composition)** — when the new class *uses* an existing class as part of its data. The new class is not a kind of the existing one.
  - An `Employee` HAS-A `Car`.
  - A `BankAccount` HAS-A `Customer`.
  - A `Car` HAS-A `Engine`.

The decision rule:

- If you want to **extend** existing functionality with more functionality → use IS-A.
- If you want to **use** existing functionality as-is → use HAS-A.

The general design principle in OOP is: **prefer composition over inheritance** unless the relationship is truly a specialization. Composition is more flexible, easier to test, and harder to misuse.

### **Examples**

```python
# Example 1: Composition — Engine inside Car
class Engine:
    def start(self):
        return "engine running"

class Car:
    def __init__(self):
        self.engine = Engine()   # composition

    def start(self):
        return f"car started ({self.engine.start()})"

print(Car().start())
```

```
car started (engine running)
```

```python
# Example 2: Aggregation — Player shared by Teams
class Player:
    def __init__(self, name):
        self.name = name

class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players     # aggregation

p1 = Player("Karan")
p2 = Player("Om")
t1 = Team("Backend", [p1, p2])
t2 = Team("Frontend", [p1])      # same player in two teams
print([pl.name for pl in t1.players])
print([pl.name for pl in t2.players])
```

```
['Karan', 'Om']
['Karan']
```

```python
# Example 3: Composition + aggregation together
class Owner:
    def __init__(self, name):
        self.name = name

class House:
    def __init__(self, address, owner):
        self.address = address
        self.owner = owner         # aggregation — owner exists independently

o = Owner("Durga")
h = House("Mumbai", o)
print(h.address, h.owner.name)
```

```
Mumbai Durga
```

```python
# Example 4: Demonstrating that composition ties lifetimes
class Room:
    def __init__(self, name):
        self.name = name

class House:
    def __init__(self):
        self.rooms = [Room("Kitchen"), Room("Bedroom"), Room("Living")]

h = House()
print([r.name for r in h.rooms])
del h    # when the house goes, the rooms are no longer referenced
print("house destroyed, rooms become eligible for GC")
```

```
['Kitchen', 'Bedroom', 'Living']
house destroyed, rooms become eligible for GC
```

```python
# Example 5: Real-world — Order with line items
class LineItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Order:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def total(self):
        return sum(item.price for item in self.items)

o = Order()
o.add(LineItem("Book", 250))
o.add(LineItem("Pen", 20))
print("total =", o.total())
```

```
total = 270
```

The `Order` composes a list of `LineItem` objects. Each `LineItem` is created outside the order and then handed in — that is technically aggregation per item, but the *list* itself is part of the order's state (composition).

```python
# Example 6: IS-A vs HAS-A side by side
class Address:
    def __init__(self, city):
        self.city = city

class Person:
    def __init__(self, name):
        self.name = name

class Employee(Person):                # IS-A
    def __init__(self, name, address):
        super().__init__(name)
        self.address = address          # HAS-A

e = Employee("Karan", Address("Mumbai"))
print(e.name, e.address.city)
print("isinstance Employee ->", isinstance(e, Employee))
print("isinstance Person   ->", isinstance(e, Person))
```

```
Karan Mumbai
isinstance Employee -> True
isinstance Person   -> True
```

`isinstance(e, Person)` is `True` because of the IS-A relationship. The HAS-A address is a separate object on `e`.

## **Quick Reference Summary**

### **HAS-A vs IS-A**

| Need | Use |
|---|---|
| Extend behaviour (the new class is a kind of the old one) | IS-A (inheritance) — see `python_inheritance.md`. |
| Just use behaviour (the new class has the old one as a part) | HAS-A (composition) — this file. |
| The contained object cannot exist alone | Composition. |
| The contained object can exist alone | Aggregation. |

### **Composition vs Aggregation**

| Aspect | Composition | Aggregation |
|---|---|---|
| Lifetime tied to container | Yes | No |
| Object created inside the container | Yes | No (created outside, passed in) |
| Symbol in UML | Filled diamond ◆ | Empty diamond ◇ |
| Default for instance variables | Yes | No |
| Typical examples | Engine in Car; Department in University | Professor in Department; Player in Team |

### **A Decision Rule of Thumb**

| If the contained object... | Then use |
|---|---|
| Cannot exist without the container | Composition |
| Exists independently and may be shared | Aggregation |
| Is created inside the container's `__init__` | Composition |
| Is created outside and passed in | Aggregation |
| Is an instance variable (default) | Composition |
| Is a class variable (static) | Aggregation |

### **When to Choose HAS-A Over IS-A**

| Scenario | Better choice |
|---|---|
| "A Car is a kind of Vehicle." | IS-A — natural specialization. |
| "A Car has an Engine." | HAS-A — engine is a part, not a kind. |
| "A Library has Books." | HAS-A — books are not kinds of libraries. |
| "A Manager is a kind of Employee." | IS-A — natural role hierarchy. |
| "A Team has Players." | HAS-A — players are not kinds of teams. |

The general design principle: **prefer composition over inheritance**. Inheritance is appropriate only when the child class is genuinely a specialized form of the parent in every meaningful way.

## **Practice and Next Steps**

- Create a `Car` class that has an `Engine` as an instance variable (composition). Call an engine method from a car method.
- Create a `Library` class that has a list of `Book` objects. Add books to the library and list their titles.
- Create a `Department` class that has a `Professor` reference (aggregation). Show that the same professor can belong to multiple departments.
- Build a `University` → `Department` → `Professor` chain with both composition and aggregation at different levels.
- Compare two implementations: one where the news aggregator creates its sources inside, and one where it receives them from outside. Identify which is composition and which is aggregation.
- Build a small `Order` class that has a list of `LineItem` objects. Add a method to compute the total price.
- Build an `Employee` class that has a `Car` (aggregation — the car is passed in). Then try the same with composition (the car is created inside the employee). Compare the two.
- For each of the following, decide whether IS-A or HAS-A is more appropriate, and implement it: `Square` and `Rectangle`, `Car` and `Engine`, `Manager` and `Employee`, `Team` and `Player`.
- Combine IS-A and HAS-A in one design: a `Library` that has a list of `Book` objects, where each `Book` is also its own class.
