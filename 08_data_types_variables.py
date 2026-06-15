# ── VARIABLES 
print("──── VARIABLES ────")

name = "Karan"                  # student first name
age = 21                        # age in years
cgpa = 8.75                     # semester CGPA out of 10
is_enrolled = True              # currently enrolled in college or not
city = "Pune"                   # home city

print(name)
print(age)
print(cgpa)
print(is_enrolled)
print(city)

# multiple assignment in one line
roll_no, branch, year = 1042, "CSE", 3
print(roll_no, branch, year)

# same value assigned to multiple variables
lab_fees = theory_fees = exam_fees = 500
print(lab_fees, theory_fees, exam_fees)

# variable names are case-sensitive
salary = 50000
Salary = 75000
SALARY = 100000
print(salary, Salary, SALARY)    # three different variables


# ── int ──────

# Use when: storing whole numbers — counts, IDs, scores, quantities

print("──── int ────")

student_id = 1042               # unique roll number
marks_obtained = 87             # marks out of 100
total_students = 60             # headcount in class
year_of_admission = 2022        # calendar year
negative_balance = -3500        # bank overdraft amount

print(student_id)
print(marks_obtained)
print(total_students)
print(year_of_admission)
print(negative_balance)

# Python integers have no size limit
very_large = 999999999999999999999999
print(very_large)

# different number bases for the same value 255
decimal_val  = 255
binary_val   = 0b11111111       # binary  prefix 0b
octal_val    = 0o377            # octal   prefix 0o
hex_val      = 0xFF             # hex     prefix 0x
print(decimal_val, binary_val, octal_val, hex_val)   # all print 255

# base conversion functions
print(bin(10))                  # '0b1010'
print(oct(10))                  # '0o12'
print(hex(255))                 # '0xff'

# arithmetic with ints
fees_per_sem  = 45000
total_sems    = 8
total_fees    = fees_per_sem * total_sems
print("Total fees:", total_fees)

print(type(student_id))         # <class 'int'>


# ── float ────

# Use when: storing decimal numbers — prices, percentages, measurements

print("──── float ────")

product_price  = 1499.99        # price of a laptop bag in rupees
gst_rate       = 0.18           # GST as a fraction
pi_approx      = 3.14159        # mathematical constant
temperature    = 36.6           # body temperature in Celsius
bank_interest  = 7.5            # annual interest rate in percent

print(product_price)
print(gst_rate)
print(pi_approx)
print(temperature)
print(bank_interest)

# scientific (exponential) notation
avogadro      = 6.022e23        # number of molecules in one mole
electron_mass = 9.109e-31       # mass of one electron in kg
print(avogadro)
print(electron_mass)

# float arithmetic
gst_amount = product_price * gst_rate
total_price = product_price + gst_amount
print("GST amount :", gst_amount)
print("Total price:", total_price)

# gotcha: floating point precision
print(0.1 + 0.2)                # 0.30000000000000004 — not exactly 0.3
print(round(0.1 + 0.2, 2))     # 0.3 — use round() for display

# floor division and modulo
attendance   = 87
total_classes = 90
percentage   = (attendance / total_classes) * 100
print("Attendance %:", round(percentage, 2))

print(type(product_price))      # <class 'float'>


# ── complex ──

# Use when: working with signal processing, electrical engineering, physics

print("──── complex ────")

impedance1 = 3 + 4j             # electrical impedance in ohms
impedance2 = 1 + 2j
signal     = 2.5 + 1.5j        # complex signal amplitude
voltage    = 220 + 0j           # AC voltage (imaginary part zero)
wave       = 0 + 5j             # purely imaginary component

print(impedance1)
print(impedance2)
print(signal)

# accessing real and imaginary parts
print(impedance1.real)          # 3.0
print(impedance1.imag)          # 4.0

# arithmetic
total_impedance = impedance1 + impedance2
print("Total impedance:", total_impedance)

product = impedance1 * impedance2
print("Product:", product)

# creating complex with complex()
z = complex(5, -3)              # 5 - 3j
print(z)

# valid: hex real, decimal imaginary
z2 = 0xFF + 2j
print(z2)                       # (255+2j)

print(type(impedance1))         # <class 'complex'>


# ── bool ─────

# Use when: storing yes/no, on/off, pass/fail conditions

print("──── bool ────")

is_logged_in    = True          # user session is active
has_paid_fees   = False         # fee payment status
is_hosteller    = True          # lives on campus
account_active  = True          # bank account not frozen
is_blacklisted  = False         # student not on suspension list

print(is_logged_in)
print(has_paid_fees)
print(is_hosteller)

# bool from comparisons
marks = 72
passed       = marks >= 40
distinction  = marks >= 75
print("Passed     :", passed)
print("Distinction:", distinction)

# bool is a subclass of int — True == 1, False == 0
print(True + True)              # 2
print(True + False)             # 1
print(True * 10)                # 10
print(False * 10)               # 0

# counting True values in a list
attendance_log = [True, True, False, True, False, True, True]
days_present   = sum(attendance_log)
print("Days present:", days_present)       # 5

# gotcha: non-zero values are truthy, zero and empty are falsy
print(bool(0))                  # False
print(bool(1))                  # True
print(bool(-99))                # True
print(bool(""))                 # False
print(bool("Tanvi"))            # True

print(type(is_logged_in))       # <class 'bool'>


# ── str ──────

# Use when: storing text — names, addresses, messages, codes

print("──── str ────")

first_name   = "Tanvi"           # student first name
last_name    = 'Deshmukh'        # student last name (single quotes also valid)
email        = "tanvi@college.edu"
department   = "Computer Science"
address      = """Flat 12, Shivaji Nagar,
Pune, Maharashtra - 411005"""    # triple quotes allow multi-line

print(first_name)
print(last_name)
print(email)
print(department)
print(address)

# concatenation
full_name = first_name + " " + last_name
print(full_name)

# repetition
separator = "-" * 40
print(separator)

# length
print(len(department))          # 16

# indexing — 0-based from left, -1-based from right
s = "Python"
print(s[0])                     # 'P'
print(s[-1])                    # 'n'
print(s[2])                     # 't'

# slicing [start:stop] — stop is exclusive
course_code = "CSE301"
print(course_code[:3])          # 'CSE'
print(course_code[3:])          # '301'
print(course_code[1:4])         # 'SE3'

# common string methods
print(first_name.upper())       # 'TANVI'
print(first_name.lower())       # 'tanvi'
print(email.replace("college", "university"))
print(department.split(" "))    # ['Computer', 'Science']
print("  Arjun  ".strip())      # 'Arjun'

# f-strings for readable formatting (Python 3.6+)
cgpa = 9.1
print(f"Student: {full_name}, CGPA: {cgpa}")

# escape characters
print("Name:\tRohit\nCity:\tNagpur")
print("Path: C:\\Users\\Rohit\\Documents")

# gotcha: strings are immutable
word = "hello"
# word[0] = "H"   # TypeError — cannot change a character in place
word = "H" + word[1:]           # create a new string instead
print(word)                     # 'Hello'

print(type(first_name))         # <class 'str'>


# ── bytes ────

# Use when: handling binary data — files, images, network packets, encryption

print("──── bytes ────")

# creating bytes from a list of integers (each must be 0-255)
raw_packet  = bytes([72, 101, 108, 108, 111])  # ASCII codes for 'Hello'
image_header = bytes([137, 80, 78, 71])        # PNG file magic bytes
checksum    = bytes([0x0A, 0x1B, 0xFF])         # hex values

print(raw_packet)               # b'Hello'
print(image_header)
print(checksum)

# encoding a string to bytes
message = "Namaste"
encoded = message.encode("utf-8")
print(encoded)                  # b'Namaste'

# decoding bytes back to string
decoded = encoded.decode("utf-8")
print(decoded)                  # 'Namaste'

# indexing bytes returns an integer
print(raw_packet[0])            # 72  (not b'H')

# gotcha: bytes are immutable
# raw_packet[0] = 100           # TypeError

print(type(raw_packet))         # <class 'bytes'>


# ── bytearray 

# Use when: you need mutable binary data — modifying buffers, building packets

print("──── bytearray ────")

sensor_data  = bytearray([10, 20, 30, 40])     # temperature readings from sensor
frame_buffer = bytearray([0xFF, 0x00, 0xAB])   # pixel data buffer
network_buf  = bytearray(b"GET /index.html")    # HTTP request bytes

print(sensor_data)
print(frame_buffer)

# mutation — this is what makes bytearray different from bytes
sensor_data[0] = 99             # update first reading
print(sensor_data)              # bytearray(b'c\x14\x1e(')

sensor_data.append(50)          # add a new reading
print(list(sensor_data))        # [99, 20, 30, 40, 50]

# gotcha: values must stay in 0-255
# sensor_data.append(300)       # ValueError: byte must be in range(0, 256)

print(type(sensor_data))        # <class 'bytearray'>


# ── range ────

# Use when: generating a sequence of integers for loops or indexing

print("──── range ────")

# range(stop) — 0 to stop-1
first_five = range(5)
print(list(first_five))         # [0, 1, 2, 3, 4]

# range(start, stop) — start to stop-1
roll_numbers = range(1, 61)     # roll numbers 1 to 60
print(list(range(1, 11)))       # first 10

# range(start, stop, step)
even_marks = range(0, 101, 2)  # 0 2 4 ... 100
odd_roll   = range(1, 20, 2)   # 1 3 5 ... 19
countdown  = range(10, 0, -1)  # 10 9 8 ... 1

print(list(range(0, 11, 2)))
print(list(range(10, 0, -1)))

# iterating with range
for i in range(1, 6):
    print(f"Student {i}: Rohit_{i}")

# indexing is allowed
r = range(100)
print(r[0])                     # 0
print(r[99])                    # 99
# print(r[100])                 # IndexError: range object index out of range

# gotcha: range is immutable
# r[0] = 99                     # TypeError

# memory efficiency — range does not store all values
big_range = range(0, 10_000_000)
print(type(big_range))          # <class 'range'>


# ── list ─────

# Use when: you need an ordered, changeable collection of items

print("──── list ────")

subjects      = ["Maths", "Physics", "Chemistry", "Python"]   # course subjects
marks_list    = [87, 92, 78, 95]                               # corresponding marks
student_data  = ["Drishya", 20, 9.2, True]                    # mixed types allowed
empty_cart    = []                                             # empty list to fill later
top_students  = ["Karan", "Tanvi", "Arjun", "Rohit", "Tanvi"] # duplicates allowed

print(subjects)
print(marks_list)
print(student_data)

# indexing and slicing
print(subjects[0])              # 'Maths'
print(subjects[-1])             # 'Python'
print(subjects[1:3])            # ['Physics', 'Chemistry']

# mutation
marks_list[0] = 90              # update Maths marks
subjects.append("English")      # add at end
subjects.insert(1, "Biology")   # insert at index 1
print(subjects)
print(marks_list)

# removing elements
subjects.remove("Biology")      # remove by value
popped = marks_list.pop()       # remove and return last element
print(popped)                   # 95
print(marks_list)

# useful list methods
marks_list.sort()
print(marks_list)               # ascending sort
print(min(marks_list), max(marks_list), sum(marks_list))

# list comprehension
squared = [m ** 2 for m in marks_list]
print(squared)

# gotcha: assigning list to another variable copies the reference, not the data
original = [1, 2, 3]
alias    = original             # both point to the same list
alias[0] = 99
print(original)                 # [99, 2, 3] — original also changed!

safe_copy = original.copy()     # or original[:]
safe_copy[0] = 0
print(original)                 # [99, 2, 3] — unchanged now

print(type(subjects))           # <class 'list'>


# ── tuple ────

# Use when: data must not change after creation — coordinates, config, records

print("──── tuple ────")

dob          = (15, 8, 2002)         # date of birth: day, month, year
college_loc  = (18.5204, 73.8567)    # GPS coordinates of college (lat, lon)
rgb_primary  = (255, 0, 0)           # red color as RGB
db_config    = ("localhost", 5432, "students_db")  # host, port, db name
single_item  = (42,)                 # gotcha: trailing comma required for single-element tuple

print(dob)
print(college_loc)
print(rgb_primary)
print(db_config)
print(single_item)
print(type(single_item))             # <class 'tuple'>

# indexing and slicing — same as list
print(dob[2])                        # 2002 — year
print(db_config[0])                  # 'localhost'
print(rgb_primary[:2])               # (255, 0)

# tuple unpacking
day, month, year = dob
print(f"Born on {day}/{month}/{year}")

host, port, db = db_config
print(f"Connecting to {db} at {host}:{port}")

# gotcha: tuples are immutable
# dob[0] = 1                         # TypeError: 'tuple' object does not support item assignment

# tuples can be used as dictionary keys; lists cannot
location_map = {college_loc: "COEP Pune"}
print(location_map)

# count and index methods
grades_tuple = ("A", "B", "A", "C", "A", "B")
print(grades_tuple.count("A"))       # 3
print(grades_tuple.index("C"))       # 3

print(type(dob))                     # <class 'tuple'>


# ── set ──────

# Use when: you need unique items and order does not matter

print("──── set ────")

enrolled_students = {"Karan", "Tanvi", "Rohit", "Arjun", "Karan"}  # duplicates dropped
elective_a = {"Python", "ML", "Data Science"}
elective_b = {"Web Dev", "Python", "Cloud"}
visited_pages = {"home", "about", "contact"}
empty_set  = set()                   # use set(), not {} (that creates an empty dict)

print(enrolled_students)             # 'Karan' appears only once
print(elective_a)
print(empty_set)

# adding and removing
enrolled_students.add("Drishya")
enrolled_students.discard("Arjun")  # discard does not raise error if missing
enrolled_students.remove("Rohit")   # remove raises KeyError if missing
print(enrolled_students)

# set operations
common_electives  = elective_a & elective_b   # intersection
all_electives     = elective_a | elective_b   # union
only_in_a         = elective_a - elective_b   # difference
not_in_both       = elective_a ^ elective_b   # symmetric difference

print("Common  :", common_electives)
print("All     :", all_electives)
print("Only A  :", only_in_a)
print("Unique  :", not_in_both)

# membership test — O(1) on average
print("Python" in elective_a)       # True
print("Java"   in elective_a)       # False

# gotcha: sets are unordered — no indexing
# print(elective_a[0])              # TypeError: 'set' object is not subscriptable

# removing duplicates from a list using set
attendance = ["Karan", "Tanvi", "Karan", "Rohit", "Tanvi", "Drishya"]
unique_attendees = list(set(attendance))
print(unique_attendees)

print(type(enrolled_students))       # <class 'set'>


# ── frozenset 

# Use when: you need an immutable set — to use as dict key or inside another set

print("──── frozenset ────")

core_subjects    = frozenset({"Maths", "Physics", "Chemistry"})
allowed_branches = frozenset(["CSE", "ECE", "IT", "MECH"])
prime_digits     = frozenset([2, 3, 5, 7])
even_digits      = frozenset([0, 2, 4, 6, 8])

print(core_subjects)
print(allowed_branches)
print(prime_digits)

# set operations work on frozenset too
print(prime_digits & even_digits)   # intersection: {2}
print(prime_digits | even_digits)   # union

# frozenset as dictionary key — regular set cannot be a key
branch_fees = {
    frozenset(["CSE", "IT"]):   90000,
    frozenset(["ECE", "MECH"]): 85000,
}
print(branch_fees)

# frozenset inside a set
groups = {frozenset(["Karan", "Tanvi"]), frozenset(["Rohit", "Arjun"])}
print(groups)

# gotcha: frozenset is immutable
# core_subjects.add("Biology")      # AttributeError: 'frozenset' object has no attribute 'add'

print(type(core_subjects))           # <class 'frozenset'>


# ── dict ─────

# Use when: storing key-value pairs — records, configs, lookups, mappings

print("──── dict ────")

student = {
    "name"    : "Rohit Sharma",     # full name
    "roll_no" : 1042,               # unique identifier
    "branch"  : "CSE",              # department
    "cgpa"    : 8.9,                # current CGPA
    "active"  : True                # enrollment status
}

subject_marks = {"Maths": 88, "Python": 95, "Physics": 79}

config = {
    "host"    : "localhost",
    "port"    : 5432,
    "db_name" : "college_db"
}

empty_dict = {}                      # empty dict

print(student)
print(subject_marks)

# accessing values
print(student["name"])               # 'Rohit Sharma'
print(student.get("cgpa"))          # 8.9
print(student.get("email", "N/A"))  # 'N/A' — safe access with default

# adding and updating
student["email"] = "rohit@college.edu"   # add new key
student["cgpa"]  = 9.1                   # update existing key
print(student)

# removing
removed = student.pop("active")     # remove key and return value
print("Removed:", removed)          # True
del student["email"]
print(student)

# iterating
for subject, mark in subject_marks.items():
    print(f"  {subject}: {mark}")

print(list(subject_marks.keys()))
print(list(subject_marks.values()))

# gotcha: duplicate keys — last value wins silently
config2 = {"host": "localhost", "host": "192.168.1.1"}
print(config2)                       # {'host': '192.168.1.1'}

# dict from two lists using zip
students_list = ["Karan", "Tanvi", "Arjun"]
marks_values  = [88, 95, 79]
result_dict   = dict(zip(students_list, marks_values))
print(result_dict)

# dict comprehension
doubled_marks = {name: mark * 2 for name, mark in result_dict.items()}
print(doubled_marks)

# nested dict
hostel = {
    "Karan"  : {"room": 201, "floor": 2},
    "Tanvi"  : {"room": 305, "floor": 3},
}
print(hostel["Karan"]["room"])       # 201

print(type(student))                 # <class 'dict'>


# ── NoneType ─

# Use when: representing the absence of a value — unset, missing, or default

print("──── NoneType ────")

pending_result = None               # result not yet uploaded
no_address     = None               # optional field left blank
uninitialized  = None               # will be assigned later

print(pending_result)               # None
print(type(pending_result))         # <class 'NoneType'>

# checking for None — always use 'is', not '=='
if pending_result is None:
    print("Result not yet published")

if no_address is not None:
    print(no_address)
else:
    print("Address not provided")

# functions with no return statement return None
def greet(name):
    print(f"Hello, {name}")

return_val = greet("Drishya")
print(return_val)                   # None

# None as a sentinel / default argument
def get_student(roll_no, default=None):
    data = {1042: "Karan", 1043: "Tanvi"}
    return data.get(roll_no, default)

print(get_student(1042))            # 'Karan'
print(get_student(9999))            # None

# gotcha: None is falsy but is not the same as 0, False, or ""
print(None == False)                # False
print(None == 0)                    # False
print(None is None)                 # True


# ── TYPE CASTING ───────────────────────────────────────────────────────────────

# Use when: converting a value from one type to another for operations or display

print("──── TYPE CASTING ────")

# int()
print(int(3.99))                    # 3    — truncates, does not round
print(int(True))                    # 1
print(int(False))                   # 0
print(int("42"))                    # 42
# print(int("3.14"))                # ValueError — decimal string not accepted
# print(int(3 + 5j))               # TypeError  — complex not accepted

# float()
print(float(10))                    # 10.0
print(float(True))                  # 1.0
print(float("3.14"))                # 3.14
print(float("10"))                  # 10.0
# print(float("ten"))               # ValueError

# complex()
print(complex(10))                  # (10+0j)
print(complex(3, 5))                # (3+5j)
print(complex(True, False))         # (1+0j)

# bool()
print(bool(0))                      # False
print(bool(1))                      # True
print(bool(""))                     # False
print(bool("Arjun"))                # True
print(bool([]))                     # False
print(bool([1, 2]))                 # True
print(bool(None))                   # False

# str()
print(str(100))                     # '100'
print(str(3.14))                    # '3.14'
print(str(True))                    # 'True'
print(str(None))                    # 'None'
print(str(3 + 5j))                  # '(3+5j)'

# real-world: concatenating int with string
student_name  = "Drishya"
rank          = 1
message       = "Topper: " + student_name + " | Rank: " + str(rank)
print(message)

# converting user input (always a string) to a number
raw_input   = "89"                  # simulates input()
marks_int   = int(raw_input)
bonus       = marks_int + 5
print(f"Marks with bonus: {bonus}")


# ── DYNAMIC TYPING ─────────────────────────────────────────────────────────────

# Use when: understanding how Python reassigns types at runtime

print("──── DYNAMIC TYPING ────")

x = 100                             # x is int
print(type(x))                      # <class 'int'>

x = 3.14                            # x is now float — same variable
print(type(x))                      # <class 'float'>

x = "Karan"                         # x is now str
print(type(x))                      # <class 'str'>

x = [1, 2, 3]                       # x is now list
print(type(x))                      # <class 'list'>

# type() and id() to inspect a variable
a = 50000
print(f"Value: {a}, Type: {type(a)}, ID: {id(a)}")

a = a + 1
print(f"Value: {a}, Type: {type(a)}, ID: {id(a)}")  # new id — new object created


# ── IMMUTABILITY AND INTERNING ─────────────────────────────────────────────────

# Use when: understanding memory reuse and why changing one variable affects another

print("──── IMMUTABILITY AND INTERNING ────")

# small integers are cached — same object in memory
a = 10
b = 10
print(a is b)                       # True — same object
print(id(a), id(b))                 # same address

a = a + 1
print(a is b)                       # False — new object for 11
print(id(a), id(b))                 # different addresses

# string interning
s1 = "python"
s2 = "python"
print(s1 is s2)                     # True — Python reuses the string literal

s1 = s1 + " rocks"
print(s1 is s2)                     # False — concatenation creates a new object

# booleans are always the same singleton object
t1 = True
t2 = True
print(t1 is t2)                     # True

# None is a singleton
n1 = None
n2 = None
print(n1 is n2)                     # True


# ── CONSTANTS (CONVENTION) ─────────────────────────────────────────────────────

# Use when: values should never change — use ALL_CAPS by naming convention

print("──── CONSTANTS ────")

MAX_STUDENTS     = 60               # maximum seats in a classroom
PI               = 3.14159265       # mathematical constant
GST_RATE         = 0.18             # current GST percentage
BASE_URL         = "https://api.college.edu/v1"
PASSING_MARKS    = 40               # minimum marks to pass

print(MAX_STUDENTS)
print(PI)
print(GST_RATE)
print(BASE_URL)
print(PASSING_MARKS)

# Python will not stop reassignment — convention only
# MAX_STUDENTS = 999    # this works but should never be done


# ── DATA TYPES SUMMARY ─────────────────────────────────────────────────────────

print("──── DATA TYPES SUMMARY ────")

all_types = {
    "int"       : 42,
    "float"     : 3.14,
    "complex"   : 3 + 5j,
    "bool"      : True,
    "str"       : "Tanvi",
    "bytes"     : bytes([72, 105]),
    "bytearray" : bytearray([10, 20]),
    "range"     : range(5),
    "list"      : [1, 2, 3],
    "tuple"     : (1, 2, 3),
    "set"       : {1, 2, 3},
    "frozenset" : frozenset({1, 2}),
    "dict"      : {"key": "val"},
    "NoneType"  : None,
}

for type_name, value in all_types.items():
    print(f"  {type_name:<12} | {str(type(value).__name__):<12} | {value}")