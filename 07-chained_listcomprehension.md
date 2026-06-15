# IF elif else in List Comprehension

## Chaining Conditional Expressions

### Traditional if-elif-else Structure
```python
if cond1:
    code1
elif cond2:
    code2
elif cond3:
    code3
else:
    coden
```

### List Comprehension Equivalent
```python
# Chained ternary operators
code1 if cond1 else code2 if cond2 else code3 if cond3 else coden
```

## Examples

### Basic Example
```python
# Traditional approach
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = []
for num in numbers:
    if num < 3:
        result.append("small")
    elif num < 7:
        result.append("medium")
    else:
        result.append("large")

# List comprehension with chained conditionals
result = ["small" if num < 3 else "medium" if num < 7 else "large" for num in numbers]
```

### Grade Classification
```python
scores = [95, 87, 76, 65, 45, 92, 58, 83]

# Using chained conditionals in list comprehension
grades = ["A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 60 else "F" for score in scores]
```

### Age Categories
```python
ages = [5, 15, 25, 35, 65, 75]

categories = ["child" if age < 13 else "teen" if age < 20 else "adult" if age < 65 else "senior" for age in ages]
```