# **Python Dictionary Interview Questions**
## **How to Use This File**
Each question follows the same structure:
- **Problem** — clear statement with example input and output.
- **Brute Force** — the naive approach; correct but slow. Understand this first.
- **Better** — an improved middle-ground approach where one exists.
- **Optimal** — the best solution to present in an interview.
- **Complexity** — time and space for the optimal solution.
- **Interview Tip** — what the interviewer actually wants to hear.
---
## **Q1 — Two Sum (Hashmap Complement Lookup)**
**Problem:** Given a list of integers and a target, return the indices of the two numbers that add up to the target.
```
Input:  nums = [2, 7, 11, 15], target = 9
Output: [0, 1]
```
```python
# Brute Force — check every pair, O(n²)
def two_sum_brute(nums: list[int], target: int) -> list[int]:
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```
```python
# Optimal — hashmap for O(1) complement lookup, O(n)
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}    # value → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
print(two_sum([2, 7, 11, 15], 9))  # [0, 1]
print(two_sum([3, 2, 4],      6))  # [1, 2]
print(two_sum([3, 3],         6))  # [0, 1]
```
**Complexity:** Time O(n) — Space O(n)
**Interview Tip:** The complement is `target - current`. Store what you have seen, not what you need. This is the most asked hashmap problem in all Python interviews — master it. Edge cases: duplicates `[3, 3]`, negative numbers, target of zero.
---
## **Q2 — Group Anagrams**
**Problem:** Given a list of strings, group anagrams together.
```
Input:  ["eat", "tea", "tan", "ate", "nat", "bat"]
Output: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
```
```python
# Brute Force — compare sorted strings pairwise, O(n² * k log k)
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
# Optimal — sorted string as dictionary key, O(n * k log k)
from collections import defaultdict
def group_anagrams(words: list[str]) -> list[list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for word in words:
        key = "".join(sorted(word))
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
**Interview Tip:** The sorted version of a word is its canonical anagram key. All words sharing the same canonical key are anagrams. `defaultdict(list)` avoids the `setdefault` boilerplate. This is among the top 5 most asked hashmap problems.
---
## **Q3 — Top K Frequent Elements**
**Problem:** Given a list of integers and a number `k`, return the `k` most frequent elements.
```
Input:  nums = [1, 1, 1, 2, 2, 3], k = 2
Output: [1, 2]
```
```python
# Brute Force — sort by frequency, O(n log n)
from collections import Counter
def top_k_brute(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    return [item for item, _ in count.most_common(k)]
```
```python
# Optimal — bucket sort by frequency, O(n)
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    count: dict[int, int] = {}
    for num in nums:
        count[num] = count.get(num, 0) + 1
    # Bucket: index = frequency, value = list of numbers with that frequency
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)
    result = []
    for i in range(len(buckets) - 1, 0, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result
    return result
print(top_k_frequent([1, 1, 1, 2, 2, 3], 2))  # [1, 2]
print(top_k_frequent([1], 1))                  # [1]
```
**Complexity:** Time O(n) — Space O(n)
**Interview Tip:** The bucket sort approach is the O(n) answer that impresses interviewers. The key insight: frequency can be at most `n`, so you can index buckets by frequency. Mention `Counter.most_common(k)` as the quick O(n log n) answer first, then offer the O(n) improvement.
---
## **Q4 — Subarray Sum Equals K**
**Problem:** Return the count of contiguous subarrays whose sum equals `k`.
```
Input:  nums = [1, 1, 1], k = 2
Output: 2
```
```python
# Brute Force — check all subarrays, O(n²)
def subarray_sum_brute(nums: list[int], k: int) -> int:
    count = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total == k:
                count += 1
    return count
```
```python
# Optimal — prefix sum + hashmap, O(n)
from collections import defaultdict
def subarray_sum(nums: list[int], k: int) -> int:
    prefix_counts: dict[int, int] = defaultdict(int)
    prefix_counts[0] = 1   # empty prefix
    total = count = 0
    for num in nums:
        total += num
        count += prefix_counts[total - k]
        prefix_counts[total] += 1
    return count
print(subarray_sum([1, 1, 1], 2))    # 2
print(subarray_sum([1, 2, 3], 3))    # 2
print(subarray_sum([-1, -1, 1], 0))  # 1
```
**Complexity:** Time O(n) — Space O(n)
**Interview Tip:** If `prefix[j] - prefix[i] = k`, then subarray `[i+1, j]` sums to `k`. Look up `prefix_sum - k` in the hashmap. This handles negative numbers — sliding window cannot. One of the most frequently asked prefix-sum problems.
---
## **Q5 — Longest Substring Without Repeating Characters**
**Problem:** Find the length of the longest substring without repeating characters.
```
Input:  "abcabcbb"
Output: 3   ("abc")
```
```python
# Brute Force — check all substrings, O(n³)
def length_of_longest_brute(s: str) -> int:
    n = len(s)
    best = 0
    for i in range(n):
        seen = set()
        for j in range(i, n):
            if s[j] in seen:
                break
            seen.add(s[j])
            best = max(best, j - i + 1)
    return best
```
```python
# Optimal — sliding window with dict tracking last seen index, O(n)
def length_of_longest(s: str) -> int:
    last_seen: dict[str, int] = {}
    left = best = 0
    for right, char in enumerate(s):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1    # shrink window past the duplicate
        last_seen[char] = right
        best = max(best, right - left + 1)
    return best
print(length_of_longest("abcabcbb"))  # 3
print(length_of_longest("bbbbb"))     # 1
print(length_of_longest("pwwkew"))    # 3
```
**Complexity:** Time O(n) — Space O(min(n, charset_size))
**Interview Tip:** The dictionary maps each character to its most recently seen index. When a duplicate is found, jump `left` past the previous occurrence — do NOT just increment by 1. This is the most asked sliding window + hashmap combo problem.
---
## **Q6 — Word Frequency Count**
**Problem:** Given a string, count the frequency of each word. Return results sorted by frequency descending, then alphabetically.
```
Input:  "the quick brown fox jumps over the lazy dog the fox"
Output: [("the", 3), ("fox", 2), ("brown", 1), ("dog", 1), ...]
```
```python
# Brute Force — manual loop
def word_count_brute(text: str) -> list[tuple[str, int]]:
    freq: dict[str, int] = {}
    for word in text.split():
        freq[word] = freq.get(word, 0) + 1
    return sorted(freq.items(), key=lambda x: (-x[1], x[0]))
```
```python
# Optimal — Counter, O(n log n)
from collections import Counter
def word_count(text: str) -> list[tuple[str, int]]:
    return sorted(Counter(text.split()).items(), key=lambda x: (-x[1], x[0]))
text = "the quick brown fox jumps over the lazy dog the fox"
for word, count in word_count(text)[:3]:
    print(f"{word} — {count}")
# the — 3
# fox — 2
# brown — 1
```
**Complexity:** Time O(n log n) — Space O(n)
**Interview Tip:** `Counter` is a dict subclass — all dict methods work on it. `.most_common(k)` gives the top k without full sorting in O(n log k). Know both the sorting approach and `most_common` — interviewers often ask for both.
---
## **Q7 — First Non-Repeating Character**
**Problem:** Given a string, find the first character that appears exactly once. Return its index, or -1 if none exists.
```
Input:  "leetcode"
Output: 0  ('l')
Input:  "aabb"
Output: -1
```
```python
# Brute Force — nested scan for each character, O(n²)
def first_unique_brute(s: str) -> int:
    for i, c in enumerate(s):
        if s.count(c) == 1:
            return i
    return -1
```
```python
# Optimal — two-pass with frequency dict, O(n)
def first_unique(s: str) -> int:
    freq: dict[str, int] = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    for i, c in enumerate(s):
        if freq[c] == 1:
            return i
    return -1
print(first_unique("leetcode"))  # 0
print(first_unique("aabb"))      # -1
print(first_unique("aabbc"))     # 4
```
**Complexity:** Time O(n) — Space O(1) — at most 26 keys for lowercase English
**Interview Tip:** Two passes are required — one to build frequencies, one to find the first with count 1. You cannot do it in one pass because "first" requires the full frequency picture. An `OrderedDict` or `Counter` works equally well. Always state the O(1) space argument for the 26-character charset.
---
## **Q8 — Check if Two Strings are Isomorphic**
**Problem:** Two strings are isomorphic if the characters in one can be replaced to get the other, preserving structure.
```
Input:  s = "egg", t = "add"    → True
Input:  s = "foo", t = "bar"    → False
Input:  s = "paper", t = "title" → True
```
```python
# Brute Force — rebuild and compare, O(n)
def is_isomorphic_brute(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    s_to_t: dict[str, str] = {}
    t_to_s: dict[str, str] = {}
    for cs, ct in zip(s, t):
        if cs in s_to_t:
            if s_to_t[cs] != ct:
                return False
        else:
            s_to_t[cs] = ct
        if ct in t_to_s:
            if t_to_s[ct] != cs:
                return False
        else:
            t_to_s[ct] = cs
    return True
```
```python
# Optimal — map both directions simultaneously, O(n)
def is_isomorphic(s: str, t: str) -> bool:
    return len(set(zip(s, t))) == len(set(s)) == len(set(t))
print(is_isomorphic("egg",   "add"))    # True
print(is_isomorphic("foo",   "bar"))    # False
print(is_isomorphic("paper", "title"))  # True
```
**Complexity:** Time O(n) — Space O(1) for fixed charset
**Interview Tip:** You need two dictionaries, not one — mapping both s→t and t→s. A single dict misses cases like "ab" → "aa". The `set(zip(...))` one-liner is elegant but explain the two-dict logic too, since it demonstrates deeper understanding.
---
## **Q9 — Minimum Window Substring**
**Problem:** Find the minimum length substring of `s` that contains all characters of `t`.
```
Input:  s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
```
```python
# Brute Force — check all substrings, O(n³)
from collections import Counter
def min_window_brute(s: str, t: str) -> str:
    t_count = Counter(t)
    best = ""
    for i in range(len(s)):
        for j in range(i + len(t), len(s) + 1):
            window = s[i:j]
            if all(Counter(window)[c] >= t_count[c] for c in t_count):
                if not best or len(window) < len(best):
                    best = window
    return best
```
```python
# Optimal — sliding window with two frequency dicts, O(n)
from collections import Counter
def min_window(s: str, t: str) -> str:
    if not t or not s:
        return ""
    need    = Counter(t)
    window  : dict[str, int] = {}
    formed  = 0
    required = len(need)
    left = best_left = best_right = 0
    best_len = float('inf')
    for right, char in enumerate(s):
        window[char] = window.get(char, 0) + 1
        if char in need and window[char] == need[char]:
            formed += 1
        while formed == required:
            if right - left + 1 < best_len:
                best_len   = right - left + 1
                best_left  = left
                best_right = right
            left_char = s[left]
            window[left_char] -= 1
            if left_char in need and window[left_char] < need[left_char]:
                formed -= 1
            left += 1
    return s[best_left:best_right + 1] if best_len != float('inf') else ""
print(min_window("ADOBECODEBANC", "ABC"))  # BANC
print(min_window("a", "a"))               # a
print(min_window("a", "b"))               # ""
```
**Complexity:** Time O(n + m) — Space O(n + m)
**Interview Tip:** `formed` tracks how many unique characters in `t` have been satisfied. Shrink left as soon as all are satisfied. This is a hard problem — knowing it shows serious preparation. Clearly separate the "expand right" and "shrink left" logic when explaining.
---
## **Q10 — Check if Two Dictionaries are Equal**
**Problem:** Given two dictionaries, determine if they contain the same key-value pairs (regardless of insertion order).
```
Input:  d1 = {"a": 1, "b": 2}, d2 = {"b": 2, "a": 1}
Output: True
```
```python
# Approach 1 — == operator (correct for flat dicts), O(n)
def dicts_equal(d1: dict, d2: dict) -> bool:
    return d1 == d2
print(dicts_equal({"a": 1, "b": 2}, {"b": 2, "a": 1}))  # True
print(dicts_equal({"a": 1},         {"a": 2}))            # False
```
```python
# Approach 2 — deep equality for nested dicts, O(n)
import json
def dicts_deep_equal(d1: dict, d2: dict) -> bool:
    return json.dumps(d1, sort_keys=True) == json.dumps(d2, sort_keys=True)
nested1 = {"a": {"x": 1}, "b": 2}
nested2 = {"b": 2, "a": {"x": 1}}
print(dicts_deep_equal(nested1, nested2))  # True
```
**Complexity:** Time O(n) — Space O(1)
**Interview Tip:** Python's `==` on dicts compares keys and values recursively for nested structures as well. The JSON trick is a quick workaround for deeply nested heterogeneous dicts but is not always reliable (e.g., with non-serialisable types). Know both and state when each applies.
---
## **Q11 — Reverse a Dictionary (Invert Key-Value)**
**Problem:** Swap the keys and values of a dictionary. Assume all values are unique.
```
Input:  {"a": 1, "b": 2, "c": 3}
Output: {1: "a", 2: "b", 3: "c"}
```
```python
# Brute Force — manual loop
def invert_dict_brute(d: dict) -> dict:
    return {v: k for k, v in d.items()}
```
```python
# Optimal — dict comprehension, O(n)
def invert_dict(d: dict) -> dict:
    return {v: k for k, v in d.items()}
print(invert_dict({"a": 1, "b": 2, "c": 3}))  # {1: 'a', 2: 'b', 3: 'c'}
# Handle non-unique values — group keys by value
def invert_dict_multi(d: dict) -> dict[any, list]:
    result: dict = {}
    for k, v in d.items():
        result.setdefault(v, []).append(k)
    return result
data = {"tanvi": "analyst", "rohit": "analyst", "arjun": "engineer"}
print(invert_dict_multi(data))
# {'analyst': ['tanvi', 'rohit'], 'engineer': ['arjun']}
```
**Complexity:** Time O(n) — Space O(n)
**Interview Tip:** The simple case assumes unique values. Always ask "are values unique?" — if not, you need to group keys into a list per value. The `setdefault` pattern for grouping is asked very frequently.
---
## **Q12 — Longest Consecutive Sequence**
**Problem:** Given an unsorted list of integers, return the length of the longest consecutive sequence.
```
Input:  [100, 4, 200, 1, 3, 2]
Output: 4   (sequence 1, 2, 3, 4)
```
```python
# Brute Force — sort and scan, O(n log n)
def longest_consecutive_brute(nums: list[int]) -> int:
    if not nums:
        return 0
    nums.sort()
    best = cur = 1
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1] + 1:
            cur += 1
            best = max(best, cur)
        elif nums[i] != nums[i - 1]:
            cur = 1
    return best
```
```python
# Optimal — hashset; start counting only from sequence starts, O(n)
def longest_consecutive(nums: list[int]) -> int:
    num_set = set(nums)
    best = 0
    for num in num_set:
        if num - 1 not in num_set:         # num is the start of a sequence
            current, length = num, 1
            while current + 1 in num_set:
                current += 1
                length  += 1
            best = max(best, length)
    return best
print(longest_consecutive([100, 4, 200, 1, 3, 2]))         # 4
print(longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1])) # 9
```
**Complexity:** Time O(n) — Space O(n)
**Interview Tip:** Only start counting when `num - 1` is NOT in the set. This ensures each sequence is counted exactly once. The inner while loop runs O(n) total across all iterations — not O(n) per element.
---
## **Q13 — Implement LRU Cache**
**Problem:** Implement a Least Recently Used (LRU) cache with `get(key)` and `put(key, value)`. Both operations must be O(1).
```
LRUCache(2)
put(1, 1) → cache = {1:1}
put(2, 2) → cache = {1:1, 2:2}
get(1)    → 1    (cache = {2:2, 1:1})
put(3, 3) → evicts key 2  (cache = {1:1, 3:3})
get(2)    → -1   (not found)
```
```python
# Brute Force — dict + manual tracking, O(n) for eviction
class LRUCacheBrute:
    def __init__(self, capacity: int):
        self.cap   = capacity
        self.cache: dict[int, int] = {}
        self.order: list[int]      = []
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.order.remove(key)
        self.order.append(key)
        return self.cache[key]
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) == self.cap:
            lru = self.order.pop(0)
            del self.cache[lru]
        self.cache[key] = value
        self.order.append(key)
```
```python
# Optimal — OrderedDict, O(1) with move_to_end
from collections import OrderedDict
class LRUCache:
    def __init__(self, capacity: int):
        self.cap   = capacity
        self.cache : OrderedDict[int, int] = OrderedDict()
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)   # mark as most recently used
        return self.cache[key]
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.cap:
            self.cache.popitem(last=False)   # remove least recently used (front)
lru = LRUCache(2)
lru.put(1, 1)
lru.put(2, 2)
print(lru.get(1))    # 1
lru.put(3, 3)        # evicts key 2
print(lru.get(2))    # -1
```
**Complexity:** Time O(1) — Space O(capacity)
**Interview Tip:** This is the most popular hashmap + data structure design problem on LeetCode. `OrderedDict.move_to_end()` and `popitem(last=False)` give O(1) operations. If asked for no built-in collections, implement with a doubly-linked list + plain dict.
---
## **Q14 — Four Sum Count**
**Problem:** Given four lists `a`, `b`, `c`, `d` of integers, count how many tuples `(i, j, k, l)` satisfy `a[i] + b[j] + c[k] + d[l] == 0`.
```
Input:  a=[1,2], b=[-2,-1], c=[-1,2], d=[0,2]
Output: 2
```
```python
# Brute Force — four nested loops, O(n⁴)
def four_sum_count_brute(a, b, c, d):
    count = 0
    for x in a:
        for y in b:
            for z in c:
                for w in d:
                    if x + y + z + w == 0:
                        count += 1
    return count
```
```python
# Optimal — hashmap for pair sums, O(n²)
from collections import defaultdict
def four_sum_count(a: list[int], b: list[int],
                   c: list[int], d: list[int]) -> int:
    ab_sums: dict[int, int] = defaultdict(int)
    for x in a:
        for y in b:
            ab_sums[x + y] += 1
    count = 0
    for z in c:
        for w in d:
            count += ab_sums[-(z + w)]
    return count
print(four_sum_count([1, 2], [-2, -1], [-1, 2], [0, 2]))  # 2
```
**Complexity:** Time O(n²) — Space O(n²)
**Interview Tip:** Split the four lists into two pairs. Store all pair sums from (a, b) in a hashmap; then look up the negation of each (c, d) pair sum. Classic "meet in the middle" reduction from O(n⁴) to O(n²).
---
## **Q15 — Ransom Note**
**Problem:** Given two strings `ransom` and `magazine`, return `True` if you can construct `ransom` using characters from `magazine` (each character used at most once).
```
Input:  ransom = "aa", magazine = "aab"
Output: True
```
```python
# Brute Force — remove characters one by one
def can_construct_brute(ransom: str, magazine: str) -> bool:
    mag = list(magazine)
    for c in ransom:
        if c not in mag:
            return False
        mag.remove(c)
    return True
```
```python
# Optimal — Counter subtraction, O(n + m)
from collections import Counter
def can_construct(ransom: str, magazine: str) -> bool:
    mag_count = Counter(magazine)
    for c in ransom:
        if mag_count[c] == 0:
            return False
        mag_count[c] -= 1
    return True
print(can_construct("aa", "aab"))  # True
print(can_construct("aa", "ab"))   # False
```
**Complexity:** Time O(n + m) — Space O(1) for fixed alphabet
**Interview Tip:** Subtracting character counts is the correct approach — it naturally handles duplicate characters. You can also use `Counter(ransom) - Counter(magazine) == {}` but the explicit loop makes the logic clearer under interview pressure.
---
## **Q16 — Continuous Subarray Sum (Multiple of K)**
**Problem:** Return `True` if there is a subarray of length at least 2 whose sum is a multiple of `k`.
```
Input:  nums = [23, 2, 4, 6, 7], k = 6
Output: True  (subarray [2, 4])
```
```python
# Brute Force — check all subarrays of length ≥ 2, O(n²)
def check_subarray_sum_brute(nums: list[int], k: int) -> bool:
    for i in range(len(nums)):
        total = nums[i]
        for j in range(i + 1, len(nums)):
            total += nums[j]
            if total % k == 0:
                return True
    return False
```
```python
# Optimal — prefix sum mod k in hashmap, O(n)
def check_subarray_sum(nums: list[int], k: int) -> bool:
    # Maps remainder → earliest index where it appeared
    seen: dict[int, int] = {0: -1}
    prefix = 0
    for i, num in enumerate(nums):
        prefix = (prefix + num) % k
        if prefix in seen:
            if i - seen[prefix] >= 2:   # subarray length at least 2
                return True
        else:
            seen[prefix] = i
    return False
print(check_subarray_sum([23, 2, 4, 6, 7], 6))  # True
print(check_subarray_sum([23, 2, 6, 4, 7], 6))  # True
print(check_subarray_sum([23, 2, 6, 4, 7], 13)) # False
```
**Complexity:** Time O(n) — Space O(k)
**Interview Tip:** If two prefix sums have the same remainder mod k, the subarray between them is a multiple of k. The `i - seen[prefix] >= 2` check enforces the minimum length of 2. Initialize `{0: -1}` to handle the case where the entire prefix is a multiple.
---
## **Q17 — Find All Duplicate Keys After Merging Dictionaries**
**Problem:** Given a list of dictionaries, find all keys that appear in more than one dictionary.
```
Input:  [{"a":1,"b":2}, {"b":3,"c":4}, {"c":5,"d":6}]
Output: ["b", "c"]
```
```python
# Brute Force — nested comparison, O(n² * k)
def duplicate_keys_brute(dicts: list[dict]) -> list[str]:
    all_keys: list[str] = []
    for d in dicts:
        all_keys.extend(d.keys())
    return sorted({k for k in all_keys if all_keys.count(k) > 1})
```
```python
# Optimal — frequency count of keys, O(n * k)
from collections import Counter
def duplicate_keys(dicts: list[dict]) -> list[str]:
    all_keys = [k for d in dicts for k in d.keys()]
    return sorted(k for k, count in Counter(all_keys).items() if count > 1)
data = [{"a": 1, "b": 2}, {"b": 3, "c": 4}, {"c": 5, "d": 6}]
print(duplicate_keys(data))  # ['b', 'c']
```
**Complexity:** Time O(n * k) — Space O(n * k)
**Interview Tip:** Flatten all keys into one list and count. `Counter` on the flattened list is the idiomatic Python answer. This pattern generalises to any "find duplicates across collections" problem.
---
## **Q18 — Number of Subarrays with Bounded Maximum**
**Problem:** Count subarrays where the maximum element is in the range `[left, right]`.
```
Input:  nums = [2, 1, 4, 3], left = 2, right = 3
Output: 3
```
```python
# Brute Force — check all subarrays, O(n²)
def num_subarray_bounded_max_brute(nums: list[int], left: int, right: int) -> int:
    count = 0
    for i in range(len(nums)):
        max_val = 0
        for j in range(i, len(nums)):
            max_val = max(max_val, nums[j])
            if left <= max_val <= right:
                count += 1
            elif max_val > right:
                break
    return count
```
```python
# Optimal — count subarrays ending at each position, O(n)
def num_subarray_bounded_max(nums: list[int], left: int, right: int) -> int:
    def count_at_most(bound: int) -> int:
        count = start = 0
        for i, num in enumerate(nums):
            if num > bound:
                start = i + 1
            count += i - start + 1
        return count
    return count_at_most(right) - count_at_most(left - 1)
print(num_subarray_bounded_max([2, 1, 4, 3], 2, 3))  # 3
print(num_subarray_bounded_max([2, 9, 2, 5, 6], 2, 8)) # 7
```
**Complexity:** Time O(n) — Space O(1)
**Interview Tip:** The inclusion-exclusion trick: `count(max ≤ right) - count(max ≤ left-1)` gives you subarrays where max is exactly in `[left, right]`. Counting "subarrays with max ≤ bound" using a running start pointer is a clean sliding approach.
---
## **Q19 — Design a Dictionary with Expiry (TTL Cache)**
**Problem:** Design a dictionary where each key expires after a given TTL (time-to-live) in seconds.
```
put("session_1", "active", ttl=2)
get("session_1") → "active"   (within 2 seconds)
# after 2 seconds:
get("session_1") → None
```
```python
import time
class TTLCache:
    def __init__(self):
        self._store: dict[str, tuple] = {}   # key → (value, expiry_time)
    def put(self, key: str, value, ttl: float) -> None:
        self._store[key] = (value, time.time() + ttl)
    def get(self, key: str):
        if key not in self._store:
            return None
        value, expiry = self._store[key]
        if time.time() > expiry:
            del self._store[key]   # lazy deletion
            return None
        return value
    def cleanup(self) -> None:
        now = time.time()
        expired = [k for k, (_, exp) in self._store.items() if now > exp]
        for k in expired:
            del self._store[k]
cache = TTLCache()
cache.put("token_abc", "admin", ttl=1)
print(cache.get("token_abc"))  # admin
time.sleep(1.1)
print(cache.get("token_abc"))  # None
```
**Complexity:** get/put O(1) — cleanup O(n)
**Interview Tip:** Lazy deletion on `get()` avoids a background sweep but leaves stale keys in memory. The `cleanup()` method handles bulk eviction. This design question tests whether you understand that a dict stores metadata alongside values — a real production pattern in session stores and token caches.
---
## **Q20 — Flatten a Nested Dictionary**
**Problem:** Given a deeply nested dictionary, flatten it so all keys are at the top level, with parent keys joined by a dot separator.
```
Input:  {"a": {"b": {"c": 1}}, "d": 2}
Output: {"a.b.c": 1, "d": 2}
```
```python
# Brute Force — recursive
def flatten_dict_brute(d: dict, parent: str = "") -> dict:
    result = {}
    for key, value in d.items():
        full_key = f"{parent}.{key}" if parent else key
        if isinstance(value, dict):
            result.update(flatten_dict_brute(value, full_key))
        else:
            result[full_key] = value
    return result
```
```python
# Optimal — iterative with a stack, O(n)
def flatten_dict(d: dict) -> dict:
    result  = {}
    stack   = [("", d)]
    while stack:
        prefix, current = stack.pop()
        for key, value in current.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                stack.append((full_key, value))
            else:
                result[full_key] = value
    return result
nested = {"a": {"b": {"c": 1}, "d": 2}, "e": 3}
print(flatten_dict(nested))
# {'a.b.c': 1, 'a.d': 2, 'e': 3}
```
**Complexity:** Time O(n) — Space O(n)
**Interview Tip:** Avoid recursion for deeply nested configs — use an iterative stack. This exact problem appears in JSON processing, Kubernetes config flattening, and environment variable expansion. Mention the separator as a parameter for flexibility.
---
## **Q21 — Find K Keys with Highest Values**
**Problem:** Given a dictionary mapping products to sales figures, return the `k` products with the highest sales.
```
Input:  {"notebook": 450, "pen": 1200, "stapler": 300, "folder": 780}, k = 2
Output: ["pen", "folder"]
```
```python
# Brute Force — sort all items, O(n log n)
def top_k_keys_brute(d: dict[str, int], k: int) -> list[str]:
    return sorted(d, key=d.get, reverse=True)[:k]
```
```python
# Optimal — heapq.nlargest, O(n log k)
import heapq
def top_k_keys(d: dict[str, int], k: int) -> list[str]:
    return heapq.nlargest(k, d, key=d.get)
sales = {"notebook": 450, "pen": 1200, "stapler": 300, "folder": 780}
print(top_k_keys(sales, 2))  # ['pen', 'folder']
```
**Complexity:** Time O(n log k) — Space O(k)
**Interview Tip:** `heapq.nlargest(k, iterable, key=...)` is O(n log k) — better than full sort O(n log n) when k is small. `d.get` as the key function reads values from the dict. This pattern covers "top products", "most active users", and "highest scoring students".
---
## **Q22 — Verify a Sudoku Board**
**Problem:** Determine if a partially filled 9×9 Sudoku board is valid. Validate rows, columns, and 3×3 boxes.
```
Input:  a 9×9 grid with '1'–'9' and '.' for empty cells
Output: True or False
```
```python
# Optimal — three sets of dicts, O(81) = O(1)
from collections import defaultdict
def is_valid_sudoku(board: list[list[str]]) -> bool:
    rows    = defaultdict(set)
    cols    = defaultdict(set)
    boxes   = defaultdict(set)
    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val == ".":
                continue
            box_id = (r // 3, c // 3)
            if (val in rows[r] or val in cols[c] or val in boxes[box_id]):
                return False
            rows[r].add(val)
            cols[c].add(val)
            boxes[box_id].add(val)
    return True
```
**Complexity:** Time O(1) — Space O(1) — board is always 9×9
**Interview Tip:** Three dictionaries of sets — one per row, column, and box. The box key `(r // 3, c // 3)` is the cleanest way to identify the 3×3 region without extra logic. This problem tests whether you know when dicts/sets are cleaner than arrays.
---
## **Q23 — Map Sum Pairs**
**Problem:** Implement a data structure where `insert(key, val)` adds a key-value pair and `sum(prefix)` returns the total of all values whose keys start with that prefix.
```
insert("apple", 3)
sum("ap")     → 3
insert("app", 2)
sum("ap")     → 5
```
```python
# Brute Force — scan all keys on each sum call
class MapSumBrute:
    def __init__(self):
        self.store: dict[str, int] = {}
    def insert(self, key: str, val: int) -> None:
        self.store[key] = val
    def sum(self, prefix: str) -> int:
        return sum(v for k, v in self.store.items() if k.startswith(prefix))
```
```python
# Optimal — prefix dict caches all prefix sums, O(k) insert O(1) sum
class MapSum:
    def __init__(self):
        self.store  : dict[str, int] = {}
        self.prefix : dict[str, int] = {}
    def insert(self, key: str, val: int) -> None:
        delta = val - self.store.get(key, 0)
        self.store[key] = val
        for i in range(1, len(key) + 1):
            self.prefix[key[:i]] = self.prefix.get(key[:i], 0) + delta
    def sum(self, prefix: str) -> int:
        return self.prefix.get(prefix, 0)
ms = MapSum()
ms.insert("apple", 3)
print(ms.sum("ap"))     # 3
ms.insert("app", 2)
print(ms.sum("ap"))     # 5
```
**Complexity:** insert O(k) — sum O(1) — Space O(n * k)
**Interview Tip:** The delta trick (`val - previous_val`) correctly handles re-insertions with updated values. This is a trie problem solved with a hashmap — knowing both implementations is impressive.
---
## **Q24 — Count Pairs with Difference K**
**Problem:** Given a list and integer `k`, count pairs `(i, j)` where `i < j` and `nums[i] - nums[j] == k`.
```
Input:  nums = [3, 1, 4, 1, 5], k = 2
Output: 2   (pairs (3,1) and (5,3) — but counting by index, not value)
```
```python
# Brute Force — check every pair, O(n²)
def count_pairs_brute(nums: list[int], k: int) -> int:
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if abs(nums[i] - nums[j]) == k:
                count += 1
    return count
```
```python
# Optimal — frequency map, O(n)
from collections import Counter
def count_pairs(nums: list[int], k: int) -> int:
    freq  = Counter(nums)
    count = 0
    for num in freq:
        if k == 0:
            count += freq[num] * (freq[num] - 1) // 2  # pairs within same value
        elif num + k in freq:
            count += freq[num] * freq[num + k]
    return count
print(count_pairs([3, 1, 4, 1, 5], 2))  # 3
print(count_pairs([1, 1, 1, 1],    0))  # 6
```
**Complexity:** Time O(n) — Space O(n)
**Interview Tip:** Handle `k == 0` separately — pairs come from within the same value group, computed by `C(freq, 2)`. For `k > 0`, look up `num + k` in the frequency map. Always ask "is k signed or unsigned?" (i.e., do you want ordered or unordered pairs).
---
## **Q25 — Clone a Graph (Adjacency Dict)**
**Problem:** Given a graph represented as an adjacency dictionary, return a deep copy.
```
Input:  {1: [2, 3], 2: [1], 3: [1]}
Output: {1: [2, 3], 2: [1], 3: [1]}  — completely independent copy
```
```python
# Optimal — BFS with a visited dict mapping original → clone, O(V + E)
from collections import deque
def clone_graph(graph: dict[int, list[int]]) -> dict[int, list[int]]:
    if not graph:
        return {}
    cloned: dict[int, list[int]] = {}
    queue = deque([next(iter(graph))])
    while queue:
        node = queue.popleft()
        if node in cloned:
            continue
        cloned[node] = []
        for neighbour in graph[node]:
            cloned[node].append(neighbour)
            if neighbour not in cloned:
                queue.append(neighbour)
    return cloned
original = {1: [2, 3], 2: [1], 3: [1]}
copy = clone_graph(original)
copy[1].append(4)
print(original)  # {1: [2, 3], 2: [1], 3: [1]}  — original unchanged
print(copy)      # {1: [2, 3, 4], 2: [1], 3: [1]}
```
**Complexity:** Time O(V + E) — Space O(V + E)
**Interview Tip:** The visited dict serves two purposes: prevents revisiting nodes and maps each original node to its clone. This is the "deep copy of a graph" pattern — the dict is both the clone storage and the visited set.
---
## **Q26 — Alien Dictionary (Topological Sort)**
**Problem:** Given a sorted list of words in an alien language, determine the order of characters.
```
Input:  ["wrt", "wrf", "er", "ett", "rftt"]
Output: "wertf"
```
```python
# Optimal — build adjacency dict and BFS topological sort, O(V + E)
from collections import defaultdict, deque
def alien_order(words: list[str]) -> str:
    # Build character adjacency from adjacent word pairs
    graph   : dict[str, set] = {c: set() for word in words for c in word}
    in_degree: dict[str, int] = {c: 0     for word in words for c in word}
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""   # invalid: longer word before prefix
        for j in range(min_len):
            if w1[j] != w2[j]:
                if w2[j] not in graph[w1[j]]:
                    graph[w1[j]].add(w2[j])
                    in_degree[w2[j]] += 1
                break
    queue  = deque(c for c in in_degree if in_degree[c] == 0)
    result = []
    while queue:
        c = queue.popleft()
        result.append(c)
        for neighbour in graph[c]:
            in_degree[neighbour] -= 1
            if in_degree[neighbour] == 0:
                queue.append(neighbour)
    return "".join(result) if len(result) == len(in_degree) else ""
print(alien_order(["wrt", "wrf", "er", "ett", "rftt"]))  # wertf
```
**Complexity:** Time O(V + E) — Space O(V + E)
**Interview Tip:** Use a dict of sets for the adjacency list — cleaner than nested lists. The in-degree dict powers Kahn's BFS topological sort. If `len(result) < len(characters)`, there is a cycle — return empty string.
---
## **Q27 — Random Pick with Blacklist**
**Problem:** Given a range `[0, n)` and a blacklist, implement `pick()` that returns a random number not in the blacklist in O(1).
```
Blacklist: [2, 3], n = 5 → valid picks from {0, 1, 4}
```
```python
import random
class RandomPick:
    def __init__(self, n: int, blacklist: list[int]):
        b_set  = set(blacklist)
        self.m = n - len(blacklist)   # size of valid range
        # Remap blacklisted numbers in [0, m) to valid numbers in [m, n)
        self.remap: dict[int, int] = {}
        valid = iter(i for i in range(self.m, n) if i not in b_set)
        for b in blacklist:
            if b < self.m:
                self.remap[b] = next(valid)
    def pick(self) -> int:
        r = random.randrange(self.m)
        return self.remap.get(r, r)
picker = RandomPick(5, [2, 3])
results = [picker.pick() for _ in range(1000)]
print(set(results))  # only {0, 1, 4}
```
**Complexity:** __init__ O(b) — pick O(1) — Space O(b)
**Interview Tip:** The key insight: shrink the valid range to `[0, m)` where `m = n - |blacklist|`, then remap any blacklisted number inside `[0, m)` to an unchosen number outside it. This makes `pick()` a single `randrange` call.
---
## **Q28 — Find All Pairs that Differ by Exactly One Bit**
**Problem:** Given a dictionary mapping binary strings to labels, find all pairs of keys that differ by exactly one bit.
```
Input:  {"1010": "A", "1110": "B", "0010": "C", "1011": "D"}
Output: [("1010", "1110"), ("1010", "0010"), ("1010", "1011")]
```
```python
# Brute Force — compare every pair, O(n² * k)
def one_bit_pairs_brute(d: dict[str, str]) -> list[tuple[str, str]]:
    keys   = list(d.keys())
    result = []
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            diffs = sum(a != b for a, b in zip(keys[i], keys[j]))
            if diffs == 1:
                result.append((keys[i], keys[j]))
    return result
```
```python
# Optimal — for each key, flip each bit and check dict, O(n * k)
def one_bit_pairs(d: dict[str, str]) -> list[tuple[str, str]]:
    result = []
    seen   = set()
    for key in d:
        for i in range(len(key)):
            # flip bit at position i
            flipped = key[:i] + ("0" if key[i] == "1" else "1") + key[i+1:]
            if flipped in d and (flipped, key) not in seen:
                result.append((key, flipped))
                seen.add((key, flipped))
    return result
data = {"1010": "A", "1110": "B", "0010": "C", "1011": "D"}
print(one_bit_pairs(data))
# [('1010', '1110'), ('1010', '0010'), ('1010', '1011')]
```
**Complexity:** Time O(n * k) — Space O(n * k)
**Interview Tip:** O(1) dictionary lookup turns an O(n² * k) brute force into O(n * k) by generating all single-bit neighbours and checking membership. This generalises to Hamming distance and nearest-neighbour problems.
---
## **Q29 — Time-Based Key-Value Store**
**Problem:** Design a store that supports `set(key, value, timestamp)` and `get(key, timestamp)` — return the value with the largest timestamp ≤ given timestamp.
```
set("score", "100", 1)
set("score", "150", 3)
get("score", 2) → "100"
get("score", 4) → "150"
```
```python
import bisect
class TimeMap:
    def __init__(self):
        self.store: dict[str, list[tuple[int, str]]] = {}
    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store.setdefault(key, []).append((timestamp, value))
    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""
        entries = self.store[key]
        # Binary search for largest timestamp ≤ given timestamp
        lo, hi = 0, len(entries) - 1
        result = ""
        while lo <= hi:
            mid = (lo + hi) // 2
            if entries[mid][0] <= timestamp:
                result = entries[mid][1]
                lo = mid + 1
            else:
                hi = mid - 1
        return result
tm = TimeMap()
tm.set("score", "100", 1)
tm.set("score", "150", 3)
print(tm.get("score", 2))  # 100
print(tm.get("score", 4))  # 150
print(tm.get("score", 0))  # ""
```
**Complexity:** set O(1) — get O(log n) — Space O(n)
**Interview Tip:** A dictionary of sorted lists with binary search is the canonical solution. Timestamps are inserted in ascending order (problem constraint), so no sorting is needed. `bisect_right` can replace the manual binary search. This is a medium-hard problem that tests dict + binary search together.
---
## **Q30 — Word Pattern Match**
**Problem:** Given a pattern string and a sentence, return `True` if the sentence follows the same structure as the pattern.
```
Input:  pattern = "abba", s = "dog cat cat dog"
Output: True
Input:  pattern = "abba", s = "dog cat cat fish"
Output: False
Input:  pattern = "aaaa", s = "dog cat cat dog"
Output: False
```
```python
# Optimal — bidirectional hashmap, O(n)
def word_pattern(pattern: str, s: str) -> bool:
    words = s.split()
    if len(pattern) != len(words):
        return False
    char_to_word: dict[str, str] = {}
    word_to_char: dict[str, str] = {}
    for c, w in zip(pattern, words):
        if c in char_to_word:
            if char_to_word[c] != w:
                return False
        else:
            if w in word_to_char:   # different char already mapped to this word
                return False
            char_to_word[c] = w
            word_to_char[w] = c
    return True
print(word_pattern("abba", "dog cat cat dog"))   # True
print(word_pattern("abba", "dog cat cat fish"))  # False
print(word_pattern("aaaa", "dog cat cat dog"))   # False
print(word_pattern("ab",   "dog dog"))           # False
```
**Complexity:** Time O(n) — Space O(n)
**Interview Tip:** You need two dicts, not one — mapping char→word AND word→char. A single dict misses the case where two different characters map to the same word (e.g. "aaaa" → "dog cat cat dog"). This is the same principle as the Isomorphic Strings problem.
---
## **Complexity Summary Table**
|
#
|
 Problem 
|
 Brute Force 
|
 Optimal 
|
 Key Technique 
|
|
---
|
---
|
---
|
---
|
---
|
|
 1 
|
 Two Sum 
|
 O(n²) 
|
 O(n) 
|
 Complement hashmap 
|
|
 2 
|
 Group Anagrams 
|
 O(n² k) 
|
 O(nk log k) 
|
 Sorted key + defaultdict 
|
|
 3 
|
 Top K Frequent Elements 
|
 O(n log n) 
|
 O(n) 
|
 Bucket sort by frequency 
|
|
 4 
|
 Subarray Sum Equals K 
|
 O(n²) 
|
 O(n) 
|
 Prefix sum + hashmap 
|
|
 5 
|
 Longest Non-Repeating Substring 
|
 O(n³) 
|
 O(n) 
|
 Sliding window + last-seen dict 
|
|
 6 
|
 Word Frequency Count 
|
 O(n log n) 
|
 O(n log n) 
|
 Counter + sort key 
|
|
 7 
|
 First Non-Repeating Character 
|
 O(n²) 
|
 O(n) 
|
 Two-pass frequency dict 
|
|
 8 
|
 Isomorphic Strings 
|
 O(n) 
|
 O(n) 
|
 Bidirectional mapping 
|
|
 9 
|
 Minimum Window Substring 
|
 O(n³) 
|
 O(n) 
|
 Sliding window + two Counters 
|
|
 10 
|
 Equal Dictionaries 
|
 O(n) 
|
 O(n) 
|
 == operator or JSON 
|
|
 11 
|
 Invert Dictionary 
|
 O(n) 
|
 O(n) 
|
 Dict comprehension 
|
|
 12 
|
 Longest Consecutive Sequence 
|
 O(n log n) 
|
 O(n) 
|
 Hashset start-of-sequence 
|
|
 13 
|
 LRU Cache 
|
 O(n) get/put 
|
 O(1) 
|
 OrderedDict 
|
|
 14 
|
 Four Sum Count 
|
 O(n⁴) 
|
 O(n²) 
|
 Pair sum hashmap 
|
|
 15 
|
 Ransom Note 
|
 O(n * m) 
|
 O(n + m) 
|
 Counter subtraction 
|
|
 16 
|
 Continuous Subarray Sum (mod K) 
|
 O(n²) 
|
 O(n) 
|
 Prefix mod + earliest index 
|
|
 17 
|
 Duplicate Keys Across Dicts 
|
 O(n² k) 
|
 O(n k) 
|
 Counter of flattened keys 
|
|
 18 
|
 Subarrays with Bounded Max 
|
 O(n²) 
|
 O(n) 
|
 Inclusion-exclusion 
|
|
 19 
|
 TTL Cache Design 
|
 O(1) / O(n) 
|
 O(1) / O(n) 
|
 Lazy deletion with expiry 
|
|
 20 
|
 Flatten Nested Dictionary 
|
 O(n) 
|
 O(n) 
|
 Iterative stack 
|
|
 21 
|
 Top K Keys by Value 
|
 O(n log n) 
|
 O(n log k) 
|
 heapq.nlargest 
|
|
 22 
|
 Valid Sudoku 
|
 O(81) 
|
 O(1) 
|
 Dict of sets per row/col/box 
|
|
 23 
|
 Map Sum Pairs 
|
 O(n * k) sum 
|
 O(k) insert O(1) sum 
|
 Prefix sum dict 
|
|
 24 
|
 Count Pairs Difference K 
|
 O(n²) 
|
 O(n) 
|
 Frequency map 
|
|
 25 
|
 Clone a Graph 
|
 O(V + E) 
|
 O(V + E) 
|
 BFS + visited dict 
|
|
 26 
|
 Alien Dictionary 
|
 O(V + E) 
|
 O(V + E) 
|
 Adjacency dict + topo sort 
|
|
 27 
|
 Random Pick with Blacklist 
|
 O(b) init 
|
 O(1) pick 
|
 Remap dict 
|
|
 28 
|
 One-Bit-Differ Pairs 
|
 O(n² k) 
|
 O(n k) 
|
 Flip + dict lookup 
|
|
 29 
|
 Time-Based Key-Value Store 
|
 O(n) get 
|
 O(log n) get 
|
 Dict of sorted lists + binary search 
|
|
 30 
|
 Word Pattern Match 
|
 O(n) 
|
 O(n) 
|
 Bidirectional char-word mapping 
|

---
## **Interview Strategy**
Follow this approach every time a dictionary problem is asked:
1. **Clarify** — ask about: duplicate keys/values, size constraints, nested structure, key types, concurrent access.
2. **State brute force** — say the complexity out loud even if you will not code it. Shows problem understanding.
3. **Identify the pattern** — most dict problems map to one of the patterns below.
4. **Code cleanly** — use `defaultdict`, `Counter`, and `get(key, default)` instead of manual existence checks.
5. **Edge cases** — empty dict, single element, all duplicates, keys with zero frequency, negative numbers.
6. **State complexity** — always give both time and space.
|
 Pattern 
|
 When to use 
|
|
---
|
---
|
|
 Complement hashmap 
|
 Pair/triplet sum problems 
|
|
 Frequency dict (Counter) 
|
 Anagrams, duplicates, top-k, window valid checks 
|
|
 Prefix sum + hashmap 
|
 Subarray sum equals K, multiples of K 
|
|
 Two-directional mapping 
|
 Isomorphism, word pattern, bijection checks 
|
|
 Sorted-key grouping 
|
 Group anagrams, group by property 
|
|
 Sliding window + last-seen 
|
 Longest non-repeating, minimum window 
|
|
 OrderedDict 
|
 LRU cache, maintain insertion order + O(1) eviction 
|
|
 Dict as adjacency list 
|
 Graph traversal, topological sort 
|
|
 Bucket by value 
|
 Top K frequent, bucket sort 
|
|
 Dict of sorted lists + binary search 
|
 Time-stamped queries, range lookups 
|