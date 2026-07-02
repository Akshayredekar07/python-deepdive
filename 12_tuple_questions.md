# **Python Tuple Interview Questions**

## **How to Use This File**

Each question follows the same structure:

- **Problem** — clear statement with example input and output.
- **Brute Force** — the naive approach; correct but slow. Understand this first.
- **Better** — an improved middle-ground approach where one exists.
- **Optimal** — the best solution to present in an interview.
- **Complexity** — time and space for the optimal solution.
- **Interview Tip** — what the interviewer actually wants to hear.

---

## **Q1 — Find All Unique Tuples That Sum to Zero (Three-Tuple Sum)**

**Problem:** Given a list of integers, return all unique triplets as tuples that sum to zero.

```
Input:  [-1, 0, 1, 2, -1, -4]
Output: [(-1, -1, 2), (-1, 0, 1)]
```

```python
# Brute Force — three nested loops, O(n³)
def three_tuple_sum_brute(nums: list[int]) -> list[tuple[int, int, int]]:
    result = set()
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    result.add(tuple(sorted([nums[i], nums[j], nums[k]])))
    return list(result)
```

```python
# Optimal — sort + two-pointer per fixed element, O(n²)
def three_tuple_sum(nums: list[int]) -> list[tuple[int, int, int]]:
    nums.sort()
    result: list[tuple[int, int, int]] = []
    n = len(nums)
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append((nums[i], nums[left], nums[right]))
                while left < right and nums[left]  == nums[left  + 1]: left  += 1
                while left < right and nums[right] == nums[right - 1]: right -= 1
                left  += 1
                right -= 1
            elif total < 0:
                left  += 1
            else:
                right -= 1
    return result

print(three_tuple_sum([-1, 0, 1, 2, -1, -4]))  # [(-1, -1, 2), (-1, 0, 1)]
print(three_tuple_sum([0, 0, 0]))               # [(0, 0, 0)]
```

**Complexity:** Time O(n²) — Space O(1) excluding output

**Interview Tip:** Tuples are the natural return type for triplets because triplets are fixed-length, ordered, and immutable records. Sorting first is essential — state this assumption before coding. The three duplicate-skip guards are what most candidates forget.

---

## **Q2 — Unpack and Swap Using Tuple Unpacking**

**Problem:** Swap two variables without using a third temporary variable.

```
Input:  a = 5, b = 10
Output: a = 10, b = 5
```

```python
# Brute Force — classic temp variable
a, b = 5, 10
temp = a
a    = b
b    = temp
print(a, b)  # 10 5
```

```python
# Optimal — Python tuple unpacking, O(1)
a, b = 5, 10
a, b = b, a
print(a, b)  # 10 5

# Applied — swap two elements in a list
nums = [3, 7, 1, 9]
nums[0], nums[3] = nums[3], nums[0]
print(nums)  # [9, 7, 1, 3]
```

**Complexity:** Time O(1) — Space O(1)

**Interview Tip:** Python evaluates the right-hand side as a tuple before any assignment happens, so no temporary variable is needed. This is used in every two-pointer and sorting algorithm you will write in Python. Be ready to explain *why* it works — it's a tuple pack then unpack.

---

## **Q3 — Return Multiple Values from a Function**

**Problem:** Write a function that returns both the minimum and maximum of a list in a single call.

```
Input:  [4, 2, 9, 1, 7]
Output: (1, 9)
```

```python
# Brute Force — two separate passes
def min_max_brute(nums: list[int]) -> tuple[int, int]:
    return min(nums), max(nums)  # still O(n) but two passes
```

```python
# Optimal — single pass, O(n)
def min_max(nums: list[int]) -> tuple[int, int]:
    lo = hi = nums[0]
    for num in nums[1:]:
        if num < lo:
            lo = num
        elif num > hi:
            hi = num
    return lo, hi

lo, hi = min_max([4, 2, 9, 1, 7])
print(lo, hi)  # 1 9

# Destructuring at call site — a very common Python pattern
minimum, maximum = min_max([4, 2, 9, 1, 7])
print(f"min — {minimum}, max — {maximum}")  # min — 1, max — 9
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** Python functions that appear to return multiple values actually return a single tuple. Interviewers ask this to check whether you understand tuple packing. Always unpack at the call site for readability.

---

## **Q4 — Count Occurrences of Each Element and Return as Sorted Tuples**

**Problem:** Given a list of words, return a list of `(word, count)` tuples sorted by count descending, then alphabetically.

```
Input:  ["apple", "banana", "apple", "cherry", "banana", "apple"]
Output: [("apple", 3), ("banana", 2), ("cherry", 1)]
```

```python
# Brute Force — manual counting with a dict, O(n log n)
def word_frequency_brute(words: list[str]) -> list[tuple[str, int]]:
    freq: dict[str, int] = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return sorted(freq.items(), key=lambda x: (-x[1], x[0]))
```

```python
# Optimal — Counter + most_common, O(n log n)
from collections import Counter

def word_frequency(words: list[str]) -> list[tuple[str, int]]:
    return sorted(Counter(words).items(), key=lambda x: (-x[1], x[0]))

result = word_frequency(["apple", "banana", "apple", "cherry", "banana", "apple"])
print(result)  # [('apple', 3), ('banana', 2), ('cherry', 1)]
```

**Complexity:** Time O(n log n) — Space O(n)

**Interview Tip:** `dict.items()` returns `(key, value)` tuples. Sorting them with a tuple key like `(-count, name)` achieves descending count then ascending name in one pass. This pattern is asked frequently in string/frequency problems.

---

## **Q5 — Tuple as a Dictionary Key (Coordinate Mapping)**

**Problem:** Given a list of `(x, y)` coordinates, count how many times each coordinate appears.

```
Input:  [(1, 2), (3, 4), (1, 2), (5, 6), (3, 4), (3, 4)]
Output: {(1, 2): 2, (3, 4): 3, (5, 6): 1}
```

```python
# Brute Force — manual loop
def count_coordinates_brute(coords: list[tuple[int, int]]) -> dict[tuple[int, int], int]:
    freq: dict[tuple[int, int], int] = {}
    for coord in coords:
        freq[coord] = freq.get(coord, 0) + 1
    return freq
```

```python
# Optimal — Counter, O(n)
from collections import Counter

def count_coordinates(coords: list[tuple[int, int]]) -> dict[tuple[int, int], int]:
    return dict(Counter(coords))

coords = [(1, 2), (3, 4), (1, 2), (5, 6), (3, 4), (3, 4)]
print(count_coordinates(coords))
# {(1, 2): 2, (3, 4): 3, (5, 6): 1}
```

**Complexity:** Time O(n) — Space O(n)

**Interview Tip:** Tuples are hashable because they are immutable, so they can be used as dictionary keys or set members. Lists cannot. This distinction is one of the most frequently asked conceptual questions about tuples in Python interviews.

---

## **Q6 — Find the Most Frequent Element Using Named Tuples**

**Problem:** Given a list of exam results as `(name, score)` tuples, find the student with the highest score.

```
Input:  [("Durga", 88), ("Karan", 95), ("Tanvi", 91), ("Rohit", 87)]
Output: ("Karan", 95)
```

```python
# Brute Force — manual loop
def top_scorer_brute(results: list[tuple[str, int]]) -> tuple[str, int]:
    best = results[0]
    for r in results[1:]:
        if r[1] > best[1]:
            best = r
    return best
```

```python
# Optimal — max() with key, O(n)
def top_scorer(results: list[tuple[str, int]]) -> tuple[str, int]:
    return max(results, key=lambda r: r[1])

results = [("Durga", 88), ("Karan", 95), ("Tanvi", 91), ("Rohit", 87)]
print(top_scorer(results))  # ('Karan', 95)
```

```python
# Modern — named tuple for readability
from collections import namedtuple

ExamResult = namedtuple("ExamResult", ["student", "score"])

records = [ExamResult("Durga", 88), ExamResult("Karan", 95), ExamResult("Tanvi", 91)]
best = max(records, key=lambda r: r.score)
print(best)          # ExamResult(student='Karan', score=95)
print(best.student)  # Karan
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** Named tuples give you attribute access (`r.score`) on top of regular tuple behaviour. They are immutable, memory-efficient, and a great answer when asked "how would you make a tuple more readable without using a class?"

---

## **Q7 — Zip Two Lists into a List of Tuples**

**Problem:** Given two equal-length lists, pair them element-by-element into tuples.

```
Input:  names = ["Arjun", "Harsha", "Om"], scores = [82, 91, 75]
Output: [("Arjun", 82), ("Harsha", 91), ("Om", 75)]
```

```python
# Brute Force — manual indexing
def zip_lists_brute(a: list, b: list) -> list[tuple]:
    return [(a[i], b[i]) for i in range(len(a))]
```

```python
# Optimal — built-in zip(), O(n)
def zip_lists(a: list, b: list) -> list[tuple]:
    return list(zip(a, b))

names  = ["Arjun", "Harsha", "Om"]
scores = [82, 91, 75]
paired = zip_lists(names, scores)
print(paired)  # [('Arjun', 82), ('Harsha', 91), ('Om', 75)]

# Unzip — reverse the operation
unpacked_names, unpacked_scores = zip(*paired)
print(list(unpacked_names))   # ['Arjun', 'Harsha', 'Om']
print(list(unpacked_scores))  # [82, 91, 75]
```

**Complexity:** Time O(n) — Space O(n)

**Interview Tip:** `zip()` returns an iterator of tuples. The `zip(*paired)` unzip pattern — often called the "transpose" — comes up in matrix and grid problems. Know both directions.

---

## **Q8 — Sort a List of Tuples by Multiple Keys**

**Problem:** Given a list of `(name, age, score)` tuples, sort by score descending, then by name ascending as a tiebreaker.

```
Input:  [("Tanvi", 22, 88), ("Karan", 21, 95), ("Durga", 23, 88), ("Rohit", 20, 72)]
Output: [("Karan", 21, 95), ("Durga", 23, 88), ("Tanvi", 22, 88), ("Rohit", 20, 72)]
```

```python
# Optimal — sort with tuple key, O(n log n)
def sort_records(records: list[tuple]) -> list[tuple]:
    return sorted(records, key=lambda r: (-r[2], r[0]))

data = [("Tanvi", 22, 88), ("Karan", 21, 95), ("Durga", 23, 88), ("Rohit", 20, 72)]
print(sort_records(data))
# [('Karan', 21, 95), ('Durga', 23, 88), ('Tanvi', 22, 88), ('Rohit', 20, 72)]
```

**Complexity:** Time O(n log n) — Space O(n)

**Interview Tip:** Python's `sorted()` is stable — ties in the primary key preserve insertion order. Using `(-score, name)` as the sort key achieves descending score + ascending name without writing a custom comparator. This is asked in almost every data-processing Python interview.

---

## **Q9 — Tuple Unpacking with Star Expression**

**Problem:** Given a tuple of exam scores, extract the first score, last score, and all middle scores separately.

```
Input:  (55, 72, 88, 91, 63, 47)
Output: first=55, last=47, middle=[72, 88, 91, 63]
```

```python
# Brute Force — manual indexing
scores = (55, 72, 88, 91, 63, 47)
first  = scores[0]
last   = scores[-1]
middle = list(scores[1:-1])
```

```python
# Optimal — starred unpacking, O(n)
scores = (55, 72, 88, 91, 63, 47)
first, *middle, last = scores

print(f"first — {first}")    # first — 55
print(f"last — {last}")      # last — 47
print(f"middle — {middle}")  # middle — [72, 88, 91, 63]

# Applied — route parsing
route = ("Mumbai", "Pune", "Satara", "Kolhapur", "Goa")
origin, *stops, destination = route
print(f"{origin} → ... → {destination}")  # Mumbai → ... → Goa
print(f"stops — {stops}")                 # stops — ['Pune', 'Satara', 'Kolhapur']
```

**Complexity:** Time O(n) — Space O(n)

**Interview Tip:** The `*middle` star expression collects remaining elements into a list. It works with any iterable, not just tuples. Frequently asked to test whether a candidate knows Python unpacking syntax beyond the basics.

---

## **Q10 — Convert List of Tuples to a Dictionary**

**Problem:** Given a list of `(key, value)` tuples, convert it to a dictionary.

```
Input:  [("name", "Harsha"), ("age", 24), ("city", "Bangalore")]
Output: {"name": "Harsha", "age": 24, "city": "Bangalore"}
```

```python
# Brute Force — manual loop
def tuples_to_dict_brute(pairs: list[tuple]) -> dict:
    result = {}
    for k, v in pairs:
        result[k] = v
    return result
```

```python
# Optimal — dict() constructor, O(n)
def tuples_to_dict(pairs: list[tuple]) -> dict:
    return dict(pairs)

pairs = [("name", "Harsha"), ("age", 24), ("city", "Bangalore")]
print(tuples_to_dict(pairs))
# {'name': 'Harsha', 'age': 24, 'city': 'Bangalore'}

# Reverse — dict to list of tuples
d = {"name": "Harsha", "age": 24}
pairs_back = list(d.items())
print(pairs_back)  # [('name', 'Harsha'), ('age', 24)]
```

**Complexity:** Time O(n) — Space O(n)

**Interview Tip:** `dict(pairs)` and `dict.items()` are the two sides of the same conversion. Interviewers ask this to test whether you know the relationship between dictionaries and tuples in Python.

---

## **Q11 — Immutability: Detect Whether an Object Can Be a Dictionary Key**

**Problem:** Given a list of objects, return those that can be used as dictionary keys.

```
Input:  [1, "hello", [1,2], (3,4), {1:2}, (1,[2,3]), frozenset({1,2})]
Output: [1, "hello", (3, 4), frozenset({1, 2})]
```

```python
# Optimal — check hashability with hash(), O(n)
def hashable_items(objects: list) -> list:
    result = []
    for obj in objects:
        try:
            hash(obj)
            result.append(obj)
        except TypeError:
            pass
    return result

items = [1, "hello", [1, 2], (3, 4), {1: 2}, (1, [2, 3]), frozenset({1, 2})]
print(hashable_items(items))
# [1, 'hello', (3, 4), frozenset({1, 2})]
```

**Complexity:** Time O(n) — Space O(n)

**Interview Tip:** A tuple is hashable only if ALL its elements are hashable. `(1, [2, 3])` is unhashable because the list inside is mutable. This is a classic conceptual question — interviewers want to hear the word "hashable" and understand that immutability enables it.

---

## **Q12 — Find the Diagonal Elements of a Matrix Using Tuples**

**Problem:** Given an `n × n` matrix, return the main diagonal elements as a tuple.

```
Input:  [[1,2,3],[4,5,6],[7,8,9]]
Output: (1, 5, 9)
```

```python
# Brute Force — manual indexing
def diagonal_brute(matrix: list[list[int]]) -> tuple[int, ...]:
    return tuple(matrix[i][i] for i in range(len(matrix)))
```

```python
# Optimal — zip with enumerate, O(n)
def diagonal(matrix: list[list[int]]) -> tuple[int, ...]:
    return tuple(row[i] for i, row in enumerate(matrix))

m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(diagonal(m))  # (1, 5, 9)

# Anti-diagonal
def anti_diagonal(matrix: list[list[int]]) -> tuple[int, ...]:
    n = len(matrix)
    return tuple(matrix[i][n - 1 - i] for i in range(n))

print(anti_diagonal(m))  # (3, 5, 7)
```

**Complexity:** Time O(n) — Space O(n)

**Interview Tip:** Returning as a tuple signals the result is a fixed-length, ordered, immutable record — the right type for a diagonal. Interviewers will sometimes specifically ask for a tuple return to check whether you know when to prefer it over a list.

---

## **Q13 — Flatten a List of Tuples**

**Problem:** Given a list of tuples, flatten it into a single list.

```
Input:  [(1, 2), (3, 4), (5, 6)]
Output: [1, 2, 3, 4, 5, 6]
```

```python
# Brute Force — nested loop
def flatten_tuples_brute(pairs: list[tuple]) -> list[int]:
    result = []
    for t in pairs:
        for item in t:
            result.append(item)
    return result
```

```python
# Optimal — itertools.chain.from_iterable, O(n)
import itertools

def flatten_tuples(pairs: list[tuple]) -> list[int]:
    return list(itertools.chain.from_iterable(pairs))

print(flatten_tuples([(1, 2), (3, 4), (5, 6)]))  # [1, 2, 3, 4, 5, 6]

# One-liner with comprehension
flat = [item for t in [(1, 2), (3, 4), (5, 6)] for item in t]
print(flat)  # [1, 2, 3, 4, 5, 6]
```

**Complexity:** Time O(n) — Space O(n)

**Interview Tip:** `itertools.chain.from_iterable` is the most efficient approach for large data. The list comprehension form is more readable for smaller inputs. Know both and explain the tradeoff.

---

## **Q14 — Group Anagrams Using Tuple Keys**

**Problem:** Given a list of strings, group anagrams together. Return groups as lists.

```
Input:  ["eat", "tea", "tan", "ate", "nat", "bat"]
Output: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
```

```python
# Brute Force — O(n² * k) comparing every pair
def group_anagrams_brute(words: list[str]) -> list[list[str]]:
    groups: list[list[str]] = []
    used = [False] * len(words)
    for i, w in enumerate(words):
        if used[i]:
            continue
        group = [w]
        used[i] = True
        for j in range(i + 1, len(words)):
            if not used[j] and sorted(w) == sorted(words[j]):
                group.append(words[j])
                used[j] = True
        groups.append(group)
    return groups
```

```python
# Optimal — sort each word → use as tuple key, O(n * k log k)
from collections import defaultdict

def group_anagrams(words: list[str]) -> list[list[str]]:
    groups: dict[tuple, list[str]] = defaultdict(list)
    for word in words:
        key = tuple(sorted(word))   # tuple key — immutable, hashable
        groups[key].append(word)
    return list(groups.values())

result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
for g in result:
    print(sorted(g))
# ['ate', 'eat', 'tea']
# ['nat', 'tan']
# ['bat']
```

**Complexity:** Time O(n * k log k) — Space O(n * k)

**Interview Tip:** The sorted characters form a canonical tuple key. Using a tuple (not a list) is required here because dictionary keys must be hashable. This is one of the most frequently asked string-grouping problems in Python interviews.

---

## **Q15 — Find All Pairs with a Given Sum (Returning Tuples)**

**Problem:** Return all unique pairs as tuples whose sum equals a target.

```
Input:  nums = [1, 5, 3, 7, 4, 2], target = 6
Output: [(1, 5), (2, 4)]
```

```python
# Brute Force — check every pair, O(n²)
def find_pairs_brute(nums: list[int], target: int) -> list[tuple[int, int]]:
    result = set()
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                result.add((min(nums[i], nums[j]), max(nums[i], nums[j])))
    return list(result)
```

```python
# Optimal — hashset complement lookup, O(n)
def find_pairs(nums: list[int], target: int) -> list[tuple[int, int]]:
    seen   = set()
    result = set()
    for num in nums:
        complement = target - num
        if complement in seen:
            result.add((min(num, complement), max(num, complement)))
        seen.add(num)
    return sorted(result)

print(find_pairs([1, 5, 3, 7, 4, 2], 6))  # [(1, 5), (2, 4)]
print(find_pairs([1, 1, 1, 1],        2))  # [(1, 1)]
```

**Complexity:** Time O(n) — Space O(n)

**Interview Tip:** Storing pairs as `(min, max)` tuples inside a set deduplicates them automatically. Tuples are hashable so they can live in a set; lists cannot. Always ask: "Can the input contain duplicates?"

---

## **Q16 — Enumerate with Tuples**

**Problem:** Given a list of product names, return a list of `(index, name)` tuples starting at 1.

```
Input:  ["notebook", "pen", "stapler"]
Output: [(1, "notebook"), (2, "pen"), (3, "stapler")]
```

```python
# Brute Force — manual counter
def indexed_items_brute(items: list[str]) -> list[tuple[int, str]]:
    return [(i + 1, item) for i, item in enumerate(items)]
```

```python
# Optimal — enumerate with start, O(n)
def indexed_items(items: list[str]) -> list[tuple[int, str]]:
    return list(enumerate(items, start=1))

products = ["notebook", "pen", "stapler"]
print(indexed_items(products))
# [(1, 'notebook'), (2, 'pen'), (3, 'stapler')]

# Unpack in loop
for rank, name in enumerate(products, start=1):
    print(f"{rank}. {name}")
```

**Complexity:** Time O(n) — Space O(n)

**Interview Tip:** `enumerate()` returns tuples of `(index, value)`. Always prefer it over maintaining a manual counter. This is a fundamental Python idiom every interviewer expects you to know.

---

## **Q17 — Check Whether a Tuple is a Palindrome**

**Problem:** Return `True` if a tuple reads the same forwards and backwards.

```
Input:  (1, 2, 3, 2, 1)
Output: True

Input:  (1, 2, 3)
Output: False
```

```python
# Brute Force — compare element by element
def is_palindrome_brute(t: tuple) -> bool:
    n = len(t)
    for i in range(n // 2):
        if t[i] != t[n - 1 - i]:
            return False
    return True
```

```python
# Optimal — slicing, O(n)
def is_palindrome(t: tuple) -> bool:
    return t == t[::-1]

print(is_palindrome((1, 2, 3, 2, 1)))   # True
print(is_palindrome((1, 2, 3)))          # False
print(is_palindrome(()))                 # True  (empty tuple is palindrome)
print(is_palindrome((5,)))               # True  (single element)
```

**Complexity:** Time O(n) — Space O(n) for the reversed copy

**Interview Tip:** Tuple slicing `t[::-1]` creates a new reversed tuple. The comparison is element-by-element. Mention edge cases: empty tuple, single element. The same approach works for strings — good to note aloud.

---

## **Q18 — Merge and Deduplicate Multiple Tuples**

**Problem:** Given multiple tuples, merge them and return a single sorted tuple of unique elements.

```
Input:  (3, 1, 4), (1, 5, 9), (2, 6, 5)
Output: (1, 2, 3, 4, 5, 6, 9)
```

```python
# Brute Force — concatenate and deduplicate manually
def merge_tuples_brute(*tuples: tuple) -> tuple:
    combined = []
    seen = set()
    for t in tuples:
        for item in t:
            if item not in seen:
                combined.append(item)
                seen.add(item)
    return tuple(sorted(combined))
```

```python
# Optimal — set union then sort, O(n log n)
def merge_tuples(*tuples: tuple) -> tuple:
    return tuple(sorted(set().union(*tuples)))

print(merge_tuples((3, 1, 4), (1, 5, 9), (2, 6, 5)))
# (1, 2, 3, 4, 5, 6, 9)
```

**Complexity:** Time O(n log n) — Space O(n)

**Interview Tip:** Tuples support `+` concatenation and conversion to/from sets. `set().union(*tuples)` is more readable than chaining `|`. Return type is tuple because the result is a fixed, ordered, immutable sequence — common in coordinate and range problems.

---

## **Q19 — Find Intersection of Two Tuples**

**Problem:** Return the common elements of two tuples as a sorted tuple (no duplicates).

```
Input:  (1, 2, 3, 4, 5), (3, 4, 5, 6, 7)
Output: (3, 4, 5)
```

```python
# Brute Force — nested loop, O(n * m)
def intersection_brute(a: tuple, b: tuple) -> tuple:
    return tuple(sorted(set(x for x in a if x in b)))
```

```python
# Optimal — set intersection, O(n + m)
def intersection(a: tuple, b: tuple) -> tuple:
    return tuple(sorted(set(a) & set(b)))

print(intersection((1, 2, 3, 4, 5), (3, 4, 5, 6, 7)))  # (3, 4, 5)
print(intersection((1, 2, 3), (4, 5, 6)))               # ()
```

**Complexity:** Time O(n + m) — Space O(n + m)

**Interview Tip:** Converting to sets first gives O(1) lookup, reducing intersection to O(n + m). The result is re-wrapped in a tuple because it's a finite, ordered sequence — a natural tuple use case.

---

## **Q20 — Product of Tuple Elements**

**Problem:** Compute the product of all elements in a tuple without importing anything.

```
Input:  (2, 3, 4, 5)
Output: 120
```

```python
# Brute Force — explicit loop
def product_brute(t: tuple[int, ...]) -> int:
    result = 1
    for num in t:
        result *= num
    return result
```

```python
# Optimal — functools.reduce, O(n)
from functools import reduce
import operator

def product(t: tuple[int, ...]) -> int:
    return reduce(operator.mul, t, 1)

print(product((2, 3, 4, 5)))  # 120
print(product(()))             # 1  (empty product is 1 by convention)
print(product((0, 5, 10)))    # 0
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** `reduce(operator.mul, t, 1)` is the idiomatic functional approach. The initial value `1` handles the empty tuple case. Interviewers sometimes ask for this to check familiarity with `functools`. Python 3.8+ also has `math.prod()` for this exact purpose.

---

## **Q21 — Rotate a Tuple by K Positions**

**Problem:** Return a new tuple rotated to the right by `k` positions.

```
Input:  (1, 2, 3, 4, 5), k = 2
Output: (4, 5, 1, 2, 3)
```

```python
# Brute Force — convert to list, rotate, convert back
def rotate_tuple_brute(t: tuple, k: int) -> tuple:
    lst = list(t)
    n   = len(lst)
    k   = k % n
    return tuple(lst[-k:] + lst[:-k])
```

```python
# Optimal — tuple slicing, O(n)
def rotate_tuple(t: tuple, k: int) -> tuple:
    n = len(t)
    k = k % n
    return t[-k:] + t[:-k]

print(rotate_tuple((1, 2, 3, 4, 5), 2))   # (4, 5, 1, 2, 3)
print(rotate_tuple((1, 2, 3, 4, 5), 7))   # (4, 5, 1, 2, 3)  (7 % 5 = 2)
print(rotate_tuple((1, 2, 3, 4, 5), 0))   # (1, 2, 3, 4, 5)
```

**Complexity:** Time O(n) — Space O(n)

**Interview Tip:** Always apply `k = k % n` first to handle cases where `k >= n`. Tuple slicing creates new tuples, so this is O(n) space. Since tuples are immutable, you cannot do this in-place — the new tuple is the intended result.

---

## **Q22 — Find the Second Largest in a Tuple**

**Problem:** Return the second largest unique value in a tuple. Return `None` if it does not exist.

```
Input:  (10, 5, 8, 10, 3)
Output: 8
```

```python
# Brute Force — sort unique values, O(n log n)
def second_largest_brute(t: tuple[int, ...]) -> int | None:
    unique = sorted(set(t))
    return unique[-2] if len(unique) >= 2 else None
```

```python
# Optimal — single pass with two variables, O(n)
def second_largest(t: tuple[int, ...]) -> int | None:
    first = second = float('-inf')
    for num in t:
        if num > first:
            second = first
            first  = num
        elif num > second and num != first:
            second = num
    return second if second != float('-inf') else None

print(second_largest((10, 5, 8, 10, 3)))  # 8
print(second_largest((5, 5, 5)))          # None
print(second_largest((1, 2)))             # 1
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** Maintain two variables, not a sorted copy. The `num != first` check correctly handles duplicates of the maximum. This is identical to the list version — the point is to show you understand that tuples support iteration and comparison even though they are immutable.

---

## **Q23 — Check if One Tuple is a Subsequence of Another**

**Problem:** Return `True` if all elements of `sub` appear in `main` in the same order (not necessarily contiguous).

```
Input:  main = (1, 3, 5, 7, 9), sub = (1, 5, 9)
Output: True

Input:  main = (1, 3, 5, 7, 9), sub = (5, 1)
Output: False
```

```python
# Brute Force — nested loop, O(n * m)
def is_subsequence_brute(main: tuple, sub: tuple) -> bool:
    it = iter(main)
    return all(elem in it for elem in sub)
```

```python
# Optimal — two-pointer, O(n + m)
def is_subsequence(main: tuple, sub: tuple) -> bool:
    i = j = 0
    while i < len(main) and j < len(sub):
        if main[i] == sub[j]:
            j += 1
        i += 1
    return j == len(sub)

print(is_subsequence((1, 3, 5, 7, 9), (1, 5, 9)))  # True
print(is_subsequence((1, 3, 5, 7, 9), (5, 1)))      # False
print(is_subsequence((1, 2, 3), ()))                 # True  (empty is always a subsequence)
```

**Complexity:** Time O(n + m) — Space O(1)

**Interview Tip:** The `iter()` brute force is clever but obscures the O(n) logic. The two-pointer makes the reasoning explicit and is easier to explain. The empty subsequence case should be mentioned proactively.

---

## **Q24 — Convert a Nested Tuple to a Flat List**

**Problem:** Given a nested tuple of arbitrary depth, flatten it into a list.

```
Input:  (1, (2, (3, 4), 5), 6)
Output: [1, 2, 3, 4, 5, 6]
```

```python
# Brute Force — recursive
def flatten_nested_brute(t) -> list:
    result = []
    for item in t:
        if isinstance(item, tuple):
            result.extend(flatten_nested_brute(item))
        else:
            result.append(item)
    return result
```

```python
# Optimal — iterative stack to avoid recursion limit, O(n)
def flatten_nested(t) -> list:
    stack  = list(t)[::-1]
    result = []
    while stack:
        item = stack.pop()
        if isinstance(item, tuple):
            stack.extend(reversed(item))
        else:
            result.append(item)
    return result

print(flatten_nested((1, (2, (3, 4), 5), 6)))  # [1, 2, 3, 4, 5, 6]
print(flatten_nested((1, 2, 3)))               # [1, 2, 3]
```

**Complexity:** Time O(n) — Space O(n)

**Interview Tip:** Same principle as flattening a nested list. Python's default recursion limit is 1000 — for deeply nested structures, the iterative stack is safer. Mention this proactively; it shows production awareness.

---

## **Q25 — LRU Cache Key Using Tuple (Function Memoization)**

**Problem:** Implement a simple memoization cache for a function that takes multiple arguments. Use a tuple as the cache key.

```
Input:  fibonacci(10)
Output: 55
```

```python
# Brute Force — recursive without cache, O(2^n)
def fib_brute(n: int) -> int:
    if n <= 1:
        return n
    return fib_brute(n - 1) + fib_brute(n - 2)
```

```python
# Optimal — memoization with tuple keys, O(n)
def make_memoized(func):
    cache: dict[tuple, int] = {}
    def wrapper(*args):
        key = args   # args is already a tuple
        if key not in cache:
            cache[key] = func(*args)
        return cache[key]
    return wrapper

@make_memoized
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(10))   # 55
print(fib(35))   # 9227465  (instant with cache)
```

```python
# Production — functools.lru_cache does the same
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_cached(n: int) -> int:
    if n <= 1:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)
```

**Complexity:** Time O(n) — Space O(n)

**Interview Tip:** `*args` in a function is always a tuple. This makes it naturally hashable — a perfect dictionary key. `lru_cache` from `functools` uses the same principle internally. Knowing this connection between tuples and memoization is a strong interview signal.

---

## **Q26 — Find All Pythagorean Triplets in a Range**

**Problem:** Find all unique `(a, b, c)` tuples where `a² + b² = c²` and all values are within `[1, n]`.

```
Input:  n = 20
Output: [(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (9, 12, 15), (12, 16, 20)]
```

```python
# Brute Force — three nested loops, O(n³)
def pythagorean_triplets_brute(n: int) -> list[tuple[int, int, int]]:
    result = []
    for a in range(1, n + 1):
        for b in range(a, n + 1):
            for c in range(b, n + 1):
                if a * a + b * b == c * c:
                    result.append((a, b, c))
    return result
```

```python
# Optimal — fix c, use set for O(1) lookup, O(n²)
def pythagorean_triplets(n: int) -> list[tuple[int, int, int]]:
    squares = {i * i: i for i in range(1, n + 1)}
    result  = []
    for a in range(1, n + 1):
        for b in range(a, n + 1):
            c_sq = a * a + b * b
            if c_sq in squares and squares[c_sq] <= n:
                result.append((a, b, squares[c_sq]))
    return result

print(pythagorean_triplets(20))
# [(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (9, 12, 15), (12, 16, 20)]
```

**Complexity:** Time O(n²) — Space O(n)

**Interview Tip:** Tuples are the natural type for triplets because `(a, b, c)` is an ordered, fixed-size mathematical object. Using a set of squares for lookup reduces the innermost loop from O(n) to O(1). Always keep `a ≤ b ≤ c` to avoid duplicate triplets.

---

## **Q27 — Tuple Comparison and Lexicographic Ordering**

**Problem:** Given a list of `(priority, task_name)` tuples, find the task that should be processed first (highest priority; break ties alphabetically).

```
Input:  [(2, "report"), (1, "email"), (2, "backup"), (3, "deploy")]
Output: (3, "deploy")
```

```python
# Optimal — max() with default tuple comparison, O(n)
def highest_priority(tasks: list[tuple[int, str]]) -> tuple[int, str]:
    return max(tasks)   # tuples compare lexicographically: first by priority, then name

tasks = [(2, "report"), (1, "email"), (2, "backup"), (3, "deploy")]
print(highest_priority(tasks))  # (3, 'deploy')

# Min-priority (break ties: alphabetically first = processes first)
print(min(tasks))  # (1, 'email')
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** Python compares tuples element by element from left to right — exactly like lexicographic string comparison. This makes `(priority, name)` tuples work correctly with `min()` and `max()` out of the box. Heavily used in priority-queue problems with `heapq`.

---

## **Q28 — Sliding Window Maximum Using Deque, Return as Tuple**

**Problem:** Given a list and window size `k`, return the maximum of each window as a tuple.

```
Input:  nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
Output: (3, 3, 5, 5, 6, 7)
```

```python
# Brute Force — recompute max each window, O(n * k)
def sliding_max_brute(nums: list[int], k: int) -> tuple[int, ...]:
    return tuple(max(nums[i:i + k]) for i in range(len(nums) - k + 1))
```

```python
# Optimal — monotonic deque, O(n)
from collections import deque

def sliding_max(nums: list[int], k: int) -> tuple[int, ...]:
    dq: deque[int] = deque()   # stores indices; front = max of current window
    result = []
    for i, num in enumerate(nums):
        while dq and dq[0] < i - k + 1:   # remove indices outside window
            dq.popleft()
        while dq and nums[dq[-1]] < num:   # remove smaller elements from back
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return tuple(result)

print(sliding_max([1, 3, -1, -3, 5, 3, 6, 7], 3))  # (3, 3, 5, 5, 6, 7)
print(sliding_max([1],                           1))  # (1,)
```

**Complexity:** Time O(n) — Space O(k)

**Interview Tip:** The result is a tuple because it is a fixed-length output record. The monotonic deque keeps only the indices of potentially useful (decreasing) elements. This is among the hardest sliding window problems — if you can explain the deque invariant, that is a strong signal.

---

## **Q29 — Reconstruct a Matrix from Row and Column Sums**

**Problem:** Given the row sums and column sums, return any valid matrix as a list of tuples (rows). Each value must be non-negative.

```
Input:  row_sums = [3, 8], col_sums = [4, 7]
Output: [(3, 0), (1, 7)]  — one valid answer
```

```python
# Greedy — assign min(row_sum, col_sum) at each cell, O(m * n)
def reconstruct_matrix(row_sums: list[int], col_sums: list[int]) -> list[tuple[int, ...]]:
    m, n = len(row_sums), len(col_sums)
    row_s = row_sums[:]
    col_s = col_sums[:]
    matrix = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            val = min(row_s[i], col_s[j])
            matrix[i][j] = val
            row_s[i]    -= val
            col_s[j]    -= val
    return [tuple(row) for row in matrix]

print(reconstruct_matrix([3, 8], [4, 7]))
# [(3, 0), (1, 7)]
```

**Complexity:** Time O(m * n) — Space O(m * n)

**Interview Tip:** Each row is returned as a tuple because rows are fixed-length ordered records — the natural tuple use case. The greedy strategy of taking `min(row_remaining, col_remaining)` always produces a valid solution when one exists.

---

## **Q30 — Encode and Decode a Sequence as a Run-Length Tuple**

**Problem:** Encode a list using run-length encoding: consecutive identical elements become `(count, value)` tuples. Also write the decoder.

```
Input:  [1, 1, 1, 2, 2, 3, 1, 1]
Output encoded:   [(3, 1), (2, 2), (1, 3), (2, 1)]
Output decoded:   [1, 1, 1, 2, 2, 3, 1, 1]
```

```python
# Optimal — single pass encoder, O(n)
from itertools import groupby

def rle_encode(nums: list[int]) -> list[tuple[int, int]]:
    return [(sum(1 for _ in g), k) for k, g in groupby(nums)]

def rle_decode(encoded: list[tuple[int, int]]) -> list[int]:
    return [val for count, val in encoded for _ in range(count)]

data    = [1, 1, 1, 2, 2, 3, 1, 1]
encoded = rle_encode(data)
print(encoded)          # [(3, 1), (2, 2), (1, 3), (2, 1)]
print(rle_decode(encoded))  # [1, 1, 1, 2, 2, 3, 1, 1]
```

**Complexity:** Time O(n) — Space O(n)

**Interview Tip:** `(count, value)` tuples are the natural representation for run-length encoding because each run is a fixed pair. `itertools.groupby` is the idiomatic Python tool. This pattern appears in string compression, network protocol encoding, and data serialisation problems.

---

## **Complexity Summary Table**

| # | Problem | Brute Force | Optimal | Key Technique |
|---|---|---|---|---|
| 1 | Three-Tuple Sum | O(n³) | O(n²) | Sort + two-pointer |
| 2 | Swap Using Tuple Unpacking | O(1) | O(1) | Tuple pack/unpack |
| 3 | Return Multiple Values | O(n) two-pass | O(n) one-pass | Tuple return + unpack |
| 4 | Word Frequency Sorted Tuples | O(n log n) | O(n log n) | Counter + sort key |
| 5 | Tuple as Dictionary Key | O(n) | O(n) | Hashability of tuples |
| 6 | Top Scorer with Named Tuple | O(n) | O(n) | max() + namedtuple |
| 7 | Zip Two Lists | O(n) | O(n) | zip() + zip(*) transpose |
| 8 | Sort Tuples Multi-Key | O(n log n) | O(n log n) | Tuple sort key |
| 9 | Star Unpacking | O(n) | O(n) | `first, *mid, last` |
| 10 | List of Tuples → Dict | O(n) | O(n) | dict() constructor |
| 11 | Hashability Check | O(n) | O(n) | hash() + TypeError |
| 12 | Diagonal as Tuple | O(n) | O(n) | enumerate() |
| 13 | Flatten Tuples | O(n) | O(n) | itertools.chain |
| 14 | Group Anagrams | O(n² k) | O(nk log k) | Tuple key + defaultdict |
| 15 | Pairs with Given Sum | O(n²) | O(n) | Hashset complement |
| 16 | Enumerate with Index | O(n) | O(n) | enumerate(start=1) |
| 17 | Palindrome Tuple | O(n) | O(n) | Slicing t[::-1] |
| 18 | Merge + Deduplicate | O(n log n) | O(n log n) | set.union + sort |
| 19 | Intersection of Tuples | O(n·m) | O(n + m) | Set intersection |
| 20 | Product of Elements | O(n) | O(n) | functools.reduce |
| 21 | Rotate Tuple by K | O(n) | O(n) | Tuple slicing |
| 22 | Second Largest | O(n log n) | O(n) | Two-variable scan |
| 23 | Subsequence Check | O(n·m) | O(n + m) | Two-pointer |
| 24 | Flatten Nested Tuple | O(n) | O(n) | Iterative stack |
| 25 | Memoization Cache Key | O(2^n) | O(n) | Tuple as cache key |
| 26 | Pythagorean Triplets | O(n³) | O(n²) | Set of squares |
| 27 | Tuple Lexicographic Order | O(n) | O(n) | Default tuple comparison |
| 28 | Sliding Window Maximum | O(n·k) | O(n) | Monotonic deque |
| 29 | Reconstruct from Row/Col Sums | O(m·n) | O(m·n) | Greedy min assignment |
| 30 | Run-Length Encoding | O(n) | O(n) | groupby() + tuple pairs |

---

## **Interview Strategy**

Follow this approach every time a tuple-related problem is asked:

1. **Clarify immutability** — confirm whether in-place modification is needed. If yes, you need a list. If no, a tuple may be the right return type.
2. **State why tuple** — tuples are the right choice for: fixed-length records, dictionary keys, function returns with multiple values, set members, and coordinate/point data.
3. **Identify the pattern** — most tuple problems map to one of the patterns below.
4. **Code cleanly** — use unpacking, `zip()`, `enumerate()`, and tuple constructors. Avoid indexing with magic numbers.
5. **Edge cases** — empty tuple, single-element tuple (remember the trailing comma: `(5,)`), tuples containing mutable objects.
6. **State complexity** — always give both time and space.

| Pattern | When to use |
|---|---|
| Tuple as dict/set key | When grouping or deduplicating multi-field records |
| Named tuple | When field names improve readability over numeric indices |
| Tuple unpacking / star | When extracting parts of a sequence cleanly |
| zip() / zip(*) | Pairing two sequences or transposing a matrix |
| Sorting with tuple key | Multi-key sorting: `(-primary, secondary)` |
| Return multiple values | Any function that logically computes two or more results |
| Tuple comparison | Priority queue, lexicographic ordering, tie-breaking |
| Immutability as feature | Cache keys, set members, `frozenset` analogue for pairs |