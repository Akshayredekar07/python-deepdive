# **Python List Interview Questions**

## **How to Use This File**

Each question follows the same structure:

- **Problem** — clear statement with example input and output.
- **Brute Force** — the naive approach; correct but slow. Understand this first.
- **Better** — an improved middle-ground approach where one exists.
- **Optimal** — the best solution to present in an interview.
- **Complexity** — time and space for the optimal solution.
- **Interview Tip** — what the interviewer actually wants to hear.

---

## **Q1 — Two Sum**

**Problem:** Given a list of integers and a target, return the indices of two numbers that add up to the target. Assume exactly one solution exists.

```
Input:  nums = [2, 7, 11, 15], target = 9
Output: [0, 1]
```

```python
# Brute Force — check every pair, O(n²)
def two_sum_brute(nums: list[int], target: int) -> list[int]:
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
```

```python
# Optimal — hashmap for O(1) complement lookup, O(n)
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}       # value → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

print(two_sum([2, 7, 11, 15], 9))   # [0, 1]
print(two_sum([3, 2, 4],      6))   # [1, 2]
print(two_sum([3, 3],         6))   # [0, 1]
```

**Complexity:** Time O(n) — Space O(n)

**Interview Tip:** The complement is `target - current`. Store what you have seen so far, not what you need. State this insight before coding. Edge cases: duplicates (e.g. `[3, 3]`), negative numbers, zero.

---

## **Q2 — Maximum Subarray Sum (Kadane's Algorithm)**

**Problem:** Find the contiguous subarray with the largest sum and return that sum.

```
Input:  [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: 6   (subarray [4, -1, 2, 1])
```

```python
# Brute Force — check all subarrays, O(n²)
def max_subarray_brute(nums: list[int]) -> int:
    max_sum = nums[0]
    n = len(nums)
    for i in range(n):
        current = 0
        for j in range(i, n):
            current += nums[j]
            max_sum = max(max_sum, current)
    return max_sum
```

```python
# Optimal — Kadane's algorithm, O(n)
def max_subarray(nums: list[int]) -> int:
    current_sum = max_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)   # extend or restart
        max_sum     = max(max_sum, current_sum)
    return max_sum

print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # 6
print(max_subarray([5, 4, -1, 7, 8]))                   # 23
print(max_subarray([-2, -4]))                            # -2
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** The decision at every element: "is it better to start fresh from here, or extend what I already have?" That single insight is Kadane's algorithm. If `current_sum` turns negative, starting fresh is always better.

---

## **Q3 — Find the Second Largest Element**

**Problem:** Return the second largest unique element in a list. Return `None` if it does not exist.

```
Input:  [10, 5, 8, 10, 3]
Output: 8
```

```python
# Brute Force — sort and scan, O(n log n)
def second_largest_brute(nums: list[int]) -> int | None:
    unique = list(set(nums))
    if len(unique) < 2:
        return None
    unique.sort()
    return unique[-2]
```

```python
# Optimal — single pass with two variables, O(n)
def second_largest(nums: list[int]) -> int | None:
    first = second = float('-inf')
    for num in nums:
        if num > first:
            second = first
            first  = num
        elif num > second and num != first:
            second = num
    return second if second != float('-inf') else None

print(second_largest([10, 5, 8, 10, 3]))  # 8
print(second_largest([5, 5, 5]))           # None
print(second_largest([1, 2]))              # 1
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** Maintain two variables (`first` and `second`), not a sorted list. The `num != first` check handles duplicates of the largest element.

---

## **Q4 — Move All Zeroes to the End**

**Problem:** Move all zeros to the end of the list while preserving the relative order of non-zero elements. Do this in place.

```
Input:  [0, 1, 0, 3, 12]
Output: [1, 3, 12, 0, 0]
```

```python
# Brute Force — collect non-zeroes and then pad, O(n) but O(n) space
def move_zeroes_brute(nums: list[int]) -> list[int]:
    non_zero = [x for x in nums if x != 0]
    return non_zero + [0] * (len(nums) - len(non_zero))
```

```python
# Optimal — two-pointer in-place, O(n) time O(1) space
def move_zeroes(nums: list[int]) -> None:
    write = 0                           # position to write next non-zero
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1
    # zeros are already at the end from the swaps

nums = [0, 1, 0, 3, 12]
move_zeroes(nums)
print(nums)  # [1, 3, 12, 0, 0]
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** The in-place two-pointer approach is always preferred. `write` tracks where the next non-zero element should go; `read` scans forward. When interviewer says "in-place", space must be O(1).

---

## **Q5 — Remove Duplicates from a Sorted List**

**Problem:** Given a sorted list, remove duplicates in-place and return the new length `k`. The first `k` elements must contain unique values.

```
Input:  [1, 1, 2, 2, 3]
Output: k = 3   (list becomes [1, 2, 3, ...])
```

```python
# Brute Force — use a set and reconstruct, O(n) time O(n) space
def remove_duplicates_brute(nums: list[int]) -> int:
    unique = list(dict.fromkeys(nums))
    for i in range(len(unique)):
        nums[i] = unique[i]
    return len(unique)
```

```python
# Optimal — two-pointer in-place since list is sorted, O(n) O(1)
def remove_duplicates(nums: list[int]) -> int:
    if not nums:
        return 0
    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[read - 1]:
            nums[write] = nums[read]
            write += 1
    return write

nums = [1, 1, 2, 2, 3]
k = remove_duplicates(nums)
print(k)         # 3
print(nums[:k])  # [1, 2, 3]
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** This only works because the list is sorted — equal elements are adjacent. Always state this assumption. The `write` pointer marks the next position for a unique element.

---

## **Q6 — Rotate a List**

**Problem:** Rotate a list to the right by `k` positions.

```
Input:  [1, 2, 3, 4, 5], k = 2
Output: [4, 5, 1, 2, 3]
```

```python
# Brute Force — rotate one step at a time, O(n * k)
def rotate_brute(nums: list[int], k: int) -> None:
    n = len(nums)
    k = k % n
    for _ in range(k):
        last = nums[-1]
        for i in range(n - 1, 0, -1):
            nums[i] = nums[i - 1]
        nums[0] = last
```

```python
# Better — slice and rebuild, O(n) time O(n) space
def rotate_slice(nums: list[int], k: int) -> None:
    n = len(nums)
    k = k % n
    nums[:] = nums[-k:] + nums[:-k]
```

```python
# Optimal — three reverses, O(n) time O(1) space
def rotate(nums: list[int], k: int) -> None:
    n = len(nums)
    k = k % n

    def reverse(left: int, right: int) -> None:
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left  += 1
            right -= 1

    reverse(0, n - 1)   # reverse entire list
    reverse(0, k - 1)   # reverse first k elements
    reverse(k, n - 1)   # reverse the rest

nums = [1, 2, 3, 4, 5]
rotate(nums, 2)
print(nums)  # [4, 5, 1, 2, 3]
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** Always apply `k = k % n` first to handle cases where `k >= n`. The three-reverse trick is the expected O(1)-space answer. Explain each step: reverse all, reverse first k, reverse rest.

---

## **Q7 — Find Missing Number**

**Problem:** Given a list of `n` distinct integers in the range `[0, n]`, find the one missing number.

```
Input:  [3, 0, 1]
Output: 2
```

```python
# Brute Force — sort and scan, O(n log n)
def missing_number_brute(nums: list[int]) -> int:
    nums.sort()
    for i, num in enumerate(nums):
        if i != num:
            return i
    return len(nums)
```

```python
# Better — use a set for O(1) lookup, O(n) time O(n) space
def missing_number_set(nums: list[int]) -> int:
    num_set = set(nums)
    for i in range(len(nums) + 1):
        if i not in num_set:
            return i
    return -1
```

```python
# Optimal — math: expected sum minus actual sum, O(n) O(1)
def missing_number(nums: list[int]) -> int:
    n = len(nums)
    expected = n * (n + 1) // 2
    return expected - sum(nums)

print(missing_number([3, 0, 1]))  # 2
print(missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1]))  # 8
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** The math approach is clean and O(1) space. You can also XOR all indices and values — the result is the missing number. Mention both to show depth.

```python
# XOR alternative — also O(n) O(1)
def missing_number_xor(nums: list[int]) -> int:
    result = len(nums)
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result
```

---

## **Q8 — Product of Array Except Self**

**Problem:** Return a list where each element is the product of all elements in the original list except the one at that index. Do not use division.

```
Input:  [1, 2, 3, 4]
Output: [24, 12, 8, 6]
```

```python
# Brute Force — for each index multiply all others, O(n²)
def product_except_self_brute(nums: list[int]) -> list[int]:
    n      = len(nums)
    result = []
    for i in range(n):
        product = 1
        for j in range(n):
            if j != i:
                product *= nums[j]
        result.append(product)
    return result
```

```python
# Optimal — prefix and suffix products, O(n) O(1) extra space
def product_except_self(nums: list[int]) -> list[int]:
    n      = len(nums)
    result = [1] * n

    # Left pass: result[i] holds product of all elements to the left
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix   *= nums[i]

    # Right pass: multiply by product of all elements to the right
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix    *= nums[i]

    return result

print(product_except_self([1, 2, 3, 4]))   # [24, 12, 8, 6]
print(product_except_self([-1, 1, 0, -3])) # [0, 0, 3, 0]
```

**Complexity:** Time O(n) — Space O(1) extra (the output list does not count)

**Interview Tip:** The trick is that `result[i] = prefix_product[i] * suffix_product[i]`. By computing both in the same output array you avoid extra space. The "no division" constraint rules out the simpler approach.

---

## **Q9 — Maximum Product Subarray**

**Problem:** Find the contiguous subarray with the largest product and return that product.

```
Input:  [2, 3, -2, 4]
Output: 6   (subarray [2, 3])

Input:  [-2, 3, -4]
Output: 24  (subarray [-2, 3, -4])
```

```python
# Brute Force — check all subarrays, O(n²)
def max_product_brute(nums: list[int]) -> int:
    n       = len(nums)
    max_prod = nums[0]
    for i in range(n):
        product = 1
        for j in range(i, n):
            product  *= nums[j]
            max_prod  = max(max_prod, product)
    return max_prod
```

```python
# Optimal — track both max and min (negative * negative = positive), O(n)
def max_product(nums: list[int]) -> int:
    max_prod = min_prod = result = nums[0]
    for num in nums[1:]:
        candidates = (num, max_prod * num, min_prod * num)
        max_prod   = max(candidates)
        min_prod   = min(candidates)
        result     = max(result, max_prod)
    return result

print(max_product([2, 3, -2, 4]))   # 6
print(max_product([-2, 3, -4]))     # 24
print(max_product([0, 2]))          # 2
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** The key difference from the maximum sum subarray: negative numbers can become positive when multiplied by another negative. Always track both the running maximum and minimum. This is the most commonly missed insight.

---

## **Q10 — Find All Duplicates in a List**

**Problem:** Given a list of integers where each value is in range `[1, n]` and each integer appears once or twice, return all duplicates. Do this in O(n) time and O(1) extra space.

```
Input:  [4, 3, 2, 7, 8, 2, 3, 1]
Output: [2, 3]
```

```python
# Brute Force — use a Counter, O(n) time O(n) space
from collections import Counter

def find_duplicates_brute(nums: list[int]) -> list[int]:
    return [num for num, count in Counter(nums).items() if count == 2]
```

```python
# Optimal — negate value at index to mark visited; O(n) O(1) space
def find_duplicates(nums: list[int]) -> list[int]:
    result = []
    for num in nums:
        idx = abs(num) - 1           # map value to index (values start at 1)
        if nums[idx] < 0:
            result.append(abs(num))  # already visited → it is a duplicate
        else:
            nums[idx] = -nums[idx]   # mark as visited by negating
    return result

print(find_duplicates([4, 3, 2, 7, 8, 2, 3, 1]))  # [2, 3]
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** Using the list itself as a hash map by negating values at target indices is a classic O(1)-space technique. It works when values are in the range `[1, n]`. Mention the constraint before presenting this approach.

---

## **Q11 — Best Time to Buy and Sell Stock**

**Problem:** Given a list of prices where `prices[i]` is the price on day `i`, return the maximum profit you can make by buying on one day and selling on a later day. Return 0 if no profit is possible.

```
Input:  [7, 1, 5, 3, 6, 4]
Output: 5   (buy at 1, sell at 6)
```

```python
# Brute Force — try every buy/sell pair, O(n²)
def max_profit_brute(prices: list[int]) -> int:
    max_p = 0
    n     = len(prices)
    for i in range(n):
        for j in range(i + 1, n):
            max_p = max(max_p, prices[j] - prices[i])
    return max_p
```

```python
# Optimal — single pass tracking minimum price seen so far, O(n)
def max_profit(prices: list[int]) -> int:
    min_price  = float('inf')
    max_profit = 0
    for price in prices:
        min_price  = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    return max_profit

print(max_profit([7, 1, 5, 3, 6, 4]))  # 5
print(max_profit([7, 6, 4, 3, 1]))     # 0  (prices only decrease)
print(max_profit([1, 2]))              # 1
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** You do not need to track which day you buy or sell — just the minimum price seen so far and the best profit so far. Ask "can I sell and rebuy multiple times?" to clarify the single-transaction constraint.

---

## **Q12 — Subarray Sum Equals K**

**Problem:** Given a list of integers and an integer `k`, return the total number of contiguous subarrays whose sum equals `k`.

```
Input:  nums = [1, 1, 1], k = 2
Output: 2
```

```python
# Brute Force — check all subarrays, O(n²)
def subarray_sum_brute(nums: list[int], k: int) -> int:
    count = 0
    n     = len(nums)
    for i in range(n):
        total = 0
        for j in range(i, n):
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
    total = 0
    count = 0
    for num in nums:
        total += num
        count += prefix_counts[total - k]   # subarrays ending here with sum k
        prefix_counts[total] += 1
    return count

print(subarray_sum([1, 1, 1], 2))         # 2
print(subarray_sum([1, 2, 3], 3))         # 2
print(subarray_sum([-1, -1, 1], 0))       # 1
```

**Complexity:** Time O(n) — Space O(n)

**Interview Tip:** The insight is: if `prefix_sum[j] - prefix_sum[i] = k`, then subarray `[i+1, j]` sums to `k`. So look up `prefix_sum - k` in the hashmap. This approach handles negative numbers, which sliding window cannot.

---

## **Q13 — Three Sum**

**Problem:** Find all unique triplets in the list that sum to zero.

```
Input:  [-1, 0, 1, 2, -1, -4]
Output: [[-1, -1, 2], [-1, 0, 1]]
```

```python
# Brute Force — three nested loops, O(n³)
def three_sum_brute(nums: list[int]) -> list[list[int]]:
    result = set()
    n      = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    result.add(tuple(sorted([nums[i], nums[j], nums[k]])))
    return [list(t) for t in result]
```

```python
# Optimal — sort + two-pointer per fixed element, O(n²)
def three_sum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    result = []
    n      = len(nums)
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:   # skip duplicates for first element
            continue
        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left]  == nums[left  + 1]: left  += 1
                while left < right and nums[right] == nums[right - 1]: right -= 1
                left  += 1
                right -= 1
            elif total < 0:
                left  += 1
            else:
                right -= 1
    return result

print(three_sum([-1, 0, 1, 2, -1, -4]))  # [[-1, -1, 2], [-1, 0, 1]]
print(three_sum([0, 0, 0]))              # [[0, 0, 0]]
```

**Complexity:** Time O(n²) — Space O(1) excluding output

**Interview Tip:** Sorting first is essential. The three duplicate-skip steps (one for `i`, one for `left`, one for `right`) are the parts most candidates forget. Mention them explicitly.

---

## **Q14 — Container With Most Water**

**Problem:** Given a list of heights representing vertical lines, find two lines that together with the x-axis form a container that holds the most water.

```
Input:  [1, 8, 6, 2, 5, 4, 8, 3, 7]
Output: 49
```

```python
# Brute Force — check all pairs, O(n²)
def max_water_brute(height: list[int]) -> int:
    n      = len(height)
    result = 0
    for i in range(n):
        for j in range(i + 1, n):
            water  = min(height[i], height[j]) * (j - i)
            result = max(result, water)
    return result
```

```python
# Optimal — two-pointer shrink from outside in, O(n)
def max_water(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    result      = 0
    while left < right:
        water  = min(height[left], height[right]) * (right - left)
        result = max(result, water)
        if height[left] < height[right]:
            left  += 1    # move the shorter side inward
        else:
            right -= 1
    return result

print(max_water([1, 8, 6, 2, 5, 4, 8, 3, 7]))  # 49
print(max_water([1, 1]))                         # 1
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** The key insight: move the pointer on the shorter side inward, because keeping it would only reduce both width and height. Proving this greedy choice is correct is what interviewers want to hear.

---

## **Q15 — Trapping Rain Water**

**Problem:** Given an elevation map, calculate how much water it can trap after rain.

```
Input:  [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
Output: 6
```

```python
# Brute Force — for each position compute left_max and right_max, O(n²)
def trap_brute(height: list[int]) -> int:
    n = len(height)
    water = 0
    for i in range(n):
        left_max  = max(height[:i + 1])
        right_max = max(height[i:])
        water    += min(left_max, right_max) - height[i]
    return water
```

```python
# Better — precompute left and right max arrays, O(n) time O(n) space
def trap_precompute(height: list[int]) -> int:
    n         = len(height)
    left_max  = [0] * n
    right_max = [0] * n
    left_max[0]     = height[0]
    right_max[n-1]  = height[n-1]
    for i in range(1, n):
        left_max[i] = max(left_max[i-1], height[i])
    for i in range(n-2, -1, -1):
        right_max[i] = max(right_max[i+1], height[i])
    return sum(min(left_max[i], right_max[i]) - height[i] for i in range(n))
```

```python
# Optimal — two-pointer, O(n) time O(1) space
def trap(height: list[int]) -> int:
    left, right       = 0, len(height) - 1
    left_max, right_max = 0, 0
    water             = 0
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    return water

print(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))  # 6
print(trap([4, 2, 0, 3, 2, 5]))                      # 9
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** Water at any position is `min(left_max, right_max) - height[i]`. The two-pointer approach uses this: whichever side is smaller can be processed safely since the other side is guaranteed to be at least as tall. Present all three approaches in order.

---

## **Q16 — Find the Majority Element**

**Problem:** Given a list of `n` elements, find the element that appears more than `n / 2` times. A majority element always exists.

```
Input:  [3, 2, 3]
Output: 3

Input:  [2, 2, 1, 1, 1, 2, 2]
Output: 2
```

```python
# Brute Force — count each element, O(n²)
def majority_element_brute(nums: list[int]) -> int:
    n = len(nums)
    for num in nums:
        if nums.count(num) > n // 2:
            return num
    return -1
```

```python
# Better — hashmap frequency count, O(n) O(n)
from collections import Counter

def majority_element_counter(nums: list[int]) -> int:
    count = Counter(nums)
    return max(count, key=count.get)
```

```python
# Optimal — Boyer-Moore Voting Algorithm, O(n) O(1)
def majority_element(nums: list[int]) -> int:
    candidate = None
    count      = 0
    for num in nums:
        if count == 0:
            candidate = num
        count += 1 if num == candidate else -1
    return candidate

print(majority_element([3, 2, 3]))              # 3
print(majority_element([2, 2, 1, 1, 1, 2, 2])) # 2
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** Boyer-Moore Voting is the answer interviewers want when they say O(1) space. The intuition: votes for the majority element will always outlast votes against it, since it appears more than half the time.

---

## **Q17 — Find Peak Element**

**Problem:** A peak element is one that is strictly greater than its neighbours. Return any peak element's index. Treat elements outside the list as negative infinity.

```
Input:  [1, 2, 3, 1]
Output: 2   (index of element 3)
```

```python
# Brute Force — linear scan, O(n)
def find_peak_brute(nums: list[int]) -> int:
    n = len(nums)
    for i in range(n):
        left_ok  = (i == 0     or nums[i] > nums[i - 1])
        right_ok = (i == n - 1 or nums[i] > nums[i + 1])
        if left_ok and right_ok:
            return i
    return -1
```

```python
# Optimal — binary search, O(log n)
def find_peak(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[mid + 1]:
            right = mid        # peak is on the left side (including mid)
        else:
            left = mid + 1     # peak is on the right side
    return left

print(find_peak([1, 2, 3, 1]))     # 2
print(find_peak([1, 2, 1, 3, 5]))  # 1 or 4 (any valid peak)
```

**Complexity:** Time O(log n) — Space O(1)

**Interview Tip:** The binary search works because: if `nums[mid] < nums[mid+1]`, there must be a peak to the right (the values are rising). This is a non-intuitive application of binary search — state the reasoning clearly.

---

## **Q18 — Merge Two Sorted Lists**

**Problem:** Merge two sorted lists into one sorted list.

```
Input:  [1, 3, 5], [2, 4, 6]
Output: [1, 2, 3, 4, 5, 6]
```

```python
# Brute Force — concatenate and sort, O(n log n)
def merge_brute(a: list[int], b: list[int]) -> list[int]:
    return sorted(a + b)
```

```python
# Optimal — two-pointer merge, O(n + m) time O(n + m) space
def merge_sorted(a: list[int], b: list[int]) -> list[int]:
    result   = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i]); i += 1
        else:
            result.append(b[j]); j += 1
    result.extend(a[i:])
    result.extend(b[j:])
    return result

print(merge_sorted([1, 3, 5], [2, 4, 6]))    # [1, 2, 3, 4, 5, 6]
print(merge_sorted([1, 2, 3], []))            # [1, 2, 3]
print(merge_sorted([],        [4, 5]))        # [4, 5]
```

**Complexity:** Time O(n + m) — Space O(n + m)

**Interview Tip:** The two-pointer approach directly uses the sorted property. `extend()` for the remaining tail avoids a loop. This same pattern applies to merge sort's merge step.

---

## **Q19 — Sort a List of 0s, 1s, and 2s (Dutch National Flag)**

**Problem:** Sort a list containing only 0, 1, and 2 in-place in one pass.

```
Input:  [2, 0, 2, 1, 1, 0]
Output: [0, 0, 1, 1, 2, 2]
```

```python
# Brute Force — count and overwrite, O(n)
def sort_colors_brute(nums: list[int]) -> None:
    count = [nums.count(0), nums.count(1), nums.count(2)]
    idx   = 0
    for val, c in enumerate(count):
        for _ in range(c):
            nums[idx] = val
            idx += 1
```

```python
# Optimal — Dutch National Flag (three-pointer), one pass O(n) O(1)
def sort_colors(nums: list[int]) -> None:
    low = mid = 0
    high = len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:                         # nums[mid] == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1                 # do not increment mid — check the swapped value

nums = [2, 0, 2, 1, 1, 0]
sort_colors(nums)
print(nums)  # [0, 0, 1, 1, 2, 2]
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** This is Dijkstra's Dutch National Flag algorithm. Three regions: `[0, low)` = 0s, `[low, mid)` = 1s, `(high, end]` = 2s. Do NOT increment `mid` when swapping with `high` — you need to inspect the swapped-in value.

---

## **Q20 — Flatten a Nested List**

**Problem:** Given a nested list of integers (any depth), return a flat list of all integers.

```
Input:  [1, [2, [3, 4], 5], 6]
Output: [1, 2, 3, 4, 5, 6]
```

```python
# Brute Force — recursive, O(n)
def flatten_recursive(lst: list) -> list[int]:
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten_recursive(item))
        else:
            result.append(item)
    return result

print(flatten_recursive([1, [2, [3, 4], 5], 6]))  # [1, 2, 3, 4, 5, 6]
```

```python
# Optimal — iterative using a stack; avoids recursion limit issues
def flatten(lst: list) -> list[int]:
    stack  = list(lst)[::-1]   # reverse so we pop from left
    result = []
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(item[::-1])
        else:
            result.append(item)
    return result

print(flatten([1, [2, [3, 4], 5], 6]))  # [1, 2, 3, 4, 5, 6]
```

```python
# Python 3.12+ — also fine for shallow nesting
import itertools

def flatten_one_level(lst: list) -> list:
    return list(itertools.chain.from_iterable(lst))
```

**Complexity:** Time O(n) — Space O(n)

**Interview Tip:** Always prefer the iterative approach for production code — Python's default recursion limit is 1000 and deeply nested structures will hit it. Mention this proactively.

---

## **Q21 — Maximum Sum of Subarray of Size K (Sliding Window)**

**Problem:** Find the maximum sum of any contiguous subarray of exactly size `k`.

```
Input:  nums = [2, 1, 5, 1, 3, 2], k = 3
Output: 9   (subarray [5, 1, 3])
```

```python
# Brute Force — recompute sum for every window, O(n * k)
def max_sum_k_brute(nums: list[int], k: int) -> int:
    n      = len(nums)
    result = float('-inf')
    for i in range(n - k + 1):
        result = max(result, sum(nums[i:i + k]))
    return result
```

```python
# Optimal — sliding window with running sum, O(n)
def max_sum_k(nums: list[int], k: int) -> int:
    window_sum = sum(nums[:k])
    max_sum    = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]   # add new, remove old
        max_sum     = max(max_sum, window_sum)
    return max_sum

print(max_sum_k([2, 1, 5, 1, 3, 2], 3))  # 9
print(max_sum_k([2, 3, 4, 1, 5],    2))  # 7
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** The sliding window avoids recomputing the entire sum each time — just add the new element and subtract the element that left the window. This is the core sliding window pattern.

---

## **Q22 — Find All Pairs with a Given Sum**

**Problem:** Return all unique pairs in a list that sum to a given target.

```
Input:  nums = [1, 5, 3, 7, 4, 2], target = 6
Output: [(1, 5), (2, 4)]
```

```python
# Brute Force — check every pair, O(n²)
def find_pairs_brute(nums: list[int], target: int) -> list[tuple]:
    result = set()
    n      = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                result.add(tuple(sorted([nums[i], nums[j]])))
    return list(result)
```

```python
# Optimal — hashset lookup, O(n)
def find_pairs(nums: list[int], target: int) -> list[tuple[int, int]]:
    seen   = set()
    result = set()
    for num in nums:
        complement = target - num
        if complement in seen:
            result.add((min(num, complement), max(num, complement)))
        seen.add(num)
    return list(result)

print(find_pairs([1, 5, 3, 7, 4, 2], 6))  # [(1, 5), (2, 4)]
print(find_pairs([1, 1, 1, 1],        2))  # [(1, 1)]
```

**Complexity:** Time O(n) — Space O(n)

**Interview Tip:** Storing results as tuples with `(min, max)` ordering inside a set automatically handles deduplication. Always ask "can there be duplicates in the input?" to shape your approach.

---

## **Q23 — Rearrange List Alternating Positive and Negative**

**Problem:** Rearrange the list so that positive and negative numbers alternate. Assume equal counts of positive and negative numbers. The first position should be a positive number.

```
Input:  [3, 1, -2, -5, 2, -4]
Output: [3, -2, 1, -5, 2, -4]
```

```python
# Brute Force — separate, interleave, O(n) time O(n) space
def rearrange_brute(nums: list[int]) -> list[int]:
    pos = [x for x in nums if x > 0]
    neg = [x for x in nums if x < 0]
    result = []
    for p, n in zip(pos, neg):
        result.extend([p, n])
    return result
```

```python
# Optimal — two-pointer in-place on sorted list, O(n log n) due to sort
def rearrange(nums: list[int]) -> list[int]:
    pos = [x for x in nums if x >= 0]
    neg = [x for x in nums if x <  0]
    result = [0] * len(nums)
    for i, (p, n) in enumerate(zip(pos, neg)):
        result[2 * i]     = p
        result[2 * i + 1] = n
    return result

print(rearrange([3, 1, -2, -5, 2, -4]))  # [3, -2, 1, -5, 2, -4]
```

**Complexity:** Time O(n) — Space O(n)

**Interview Tip:** Always clarify: "Should I preserve original order?" and "Are there equal counts of positives and negatives?" The answer shapes the entire approach.

---

## **Q24 — Longest Consecutive Sequence**

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
    longest = current = 1
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1] + 1:
            current += 1
            longest  = max(longest, current)
        elif nums[i] != nums[i - 1]:
            current = 1
    return longest
```

```python
# Optimal — hashset; only start counting from the beginning of a sequence, O(n)
def longest_consecutive(nums: list[int]) -> int:
    num_set = set(nums)
    longest = 0
    for num in num_set:
        if num - 1 not in num_set:       # num is the start of a sequence
            current = num
            length  = 1
            while current + 1 in num_set:
                current += 1
                length  += 1
            longest = max(longest, length)
    return longest

print(longest_consecutive([100, 4, 200, 1, 3, 2]))  # 4
print(longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1])) # 9
```

**Complexity:** Time O(n) — Space O(n)

**Interview Tip:** The key: only start counting when `num - 1` is NOT in the set. This ensures each sequence is counted exactly once and the inner while loop runs in amortised O(n) total.

---

## **Q25 — First Missing Positive**

**Problem:** Given an unsorted list of integers, find the smallest missing positive integer. Must be O(n) time and O(1) space.

```
Input:  [3, 4, -1, 1]
Output: 2

Input:  [1, 2, 0]
Output: 3
```

```python
# Brute Force — check 1, 2, 3 ... until missing, O(n²)
def first_missing_brute(nums: list[int]) -> int:
    i = 1
    while True:
        if i not in nums:
            return i
        i += 1
```

```python
# Better — use a set, O(n) time O(n) space
def first_missing_set(nums: list[int]) -> int:
    num_set = set(nums)
    i = 1
    while i in num_set:
        i += 1
    return i
```

```python
# Optimal — use the list itself as a hash map (index placement), O(n) O(1)
def first_missing_positive(nums: list[int]) -> int:
    n = len(nums)
    # Step 1: place each number in its correct index position (num at index num-1)
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            nums[nums[i] - 1], nums[i] = nums[i], nums[nums[i] - 1]
    # Step 2: first index where nums[i] != i+1 is the answer
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1

print(first_missing_positive([3, 4, -1, 1]))  # 2
print(first_missing_positive([1, 2, 0]))       # 3
print(first_missing_positive([7, 8, 9]))       # 1
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** This is a hard LeetCode problem. The insight: the answer must be in `[1, n+1]`. Use the list as a hash map by cyclic placement. The while loop total runs O(n) across all iterations.

---

## **Q26 — Spiral Order Traversal of a Matrix**

**Problem:** Given an `m × n` matrix, return all elements in spiral order.

```
Input:  [[1,2,3],[4,5,6],[7,8,9]]
Output: [1,2,3,6,9,8,7,4,5]
```

```python
# Brute Force — track visited cells with a boolean matrix, O(m*n) O(m*n)
def spiral_brute(matrix: list[list[int]]) -> list[int]:
    if not matrix:
        return []
    m, n    = len(matrix), len(matrix[0])
    visited = [[False] * n for _ in range(m)]
    result  = []
    dr = [0,  1,  0, -1]
    dc = [1,  0, -1,  0]
    r = c = di = 0
    for _ in range(m * n):
        result.append(matrix[r][c])
        visited[r][c] = True
        nr, nc = r + dr[di], c + dc[di]
        if 0 <= nr < m and 0 <= nc < n and not visited[nr][nc]:
            r, c = nr, nc
        else:
            di = (di + 1) % 4
            r, c = r + dr[di], c + dc[di]
    return result
```

```python
# Optimal — shrink boundaries layer by layer, O(m*n) O(1) extra space
def spiral_order(matrix: list[list[int]]) -> list[int]:
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for col in range(left, right + 1):   result.append(matrix[top][col])
        top += 1
        for row in range(top, bottom + 1):   result.append(matrix[row][right])
        right -= 1
        if top <= bottom:
            for col in range(right, left - 1, -1): result.append(matrix[bottom][col])
            bottom -= 1
        if left <= right:
            for row in range(bottom, top - 1, -1): result.append(matrix[row][left])
            left += 1
    return result

print(spiral_order([[1,2,3],[4,5,6],[7,8,9]]))  # [1,2,3,6,9,8,7,4,5]
print(spiral_order([[1,2],[3,4]]))              # [1,2,4,3]
```

**Complexity:** Time O(m * n) — Space O(1) extra

**Interview Tip:** Four boundaries (`top`, `bottom`, `left`, `right`) shrink after each direction. The guards `if top <= bottom` and `if left <= right` handle single-row and single-column edge cases.

---

## **Q27 — Find K-th Largest Element**

**Problem:** Find the k-th largest element in an unsorted list. Note: k-th largest, not k-th distinct.

```
Input:  [3, 2, 1, 5, 6, 4], k = 2
Output: 5
```

```python
# Brute Force — sort and index, O(n log n)
def kth_largest_brute(nums: list[int], k: int) -> int:
    return sorted(nums)[-k]
```

```python
# Better — min-heap of size k, O(n log k)
import heapq

def kth_largest_heap(nums: list[int], k: int) -> int:
    return heapq.nlargest(k, nums)[-1]
```

```python
# Optimal — QuickSelect average O(n), worst O(n²)
import random

def kth_largest(nums: list[int], k: int) -> int:
    target = len(nums) - k

    def quickselect(left: int, right: int) -> int:
        pivot_idx = random.randint(left, right)
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
        pivot = nums[right]
        store = left
        for i in range(left, right):
            if nums[i] <= pivot:
                nums[i], nums[store] = nums[store], nums[i]
                store += 1
        nums[store], nums[right] = nums[right], nums[store]
        if store == target:
            return nums[store]
        elif store < target:
            return quickselect(store + 1, right)
        else:
            return quickselect(left, store - 1)

    return quickselect(0, len(nums) - 1)

print(kth_largest([3, 2, 1, 5, 6, 4], 2))  # 5
print(kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))  # 4
```

**Complexity:** Time O(n) average — Space O(1)

**Interview Tip:** For most interviews the heap approach `heapq.nlargest(k, nums)[-1]` is sufficient. Mention QuickSelect for full marks. The heap approach is O(n log k) which is better than sorting when k is small.

---

## **Q28 — Check if One List is a Subset of Another**

**Problem:** Return `True` if every element of `subset` appears in `main_list` (considering duplicates).

```
Input:  main = [1, 2, 3, 4, 5], subset = [2, 4]
Output: True

Input:  main = [1, 2, 2, 3],    subset = [2, 2, 2]
Output: False  (only two 2s available)
```

```python
# Brute Force — nested loop, O(n * m)
def is_subset_brute(main: list[int], subset: list[int]) -> bool:
    temp = list(main)
    for item in subset:
        if item in temp:
            temp.remove(item)
        else:
            return False
    return True
```

```python
# Optimal — Counter comparison handles duplicates, O(n + m)
from collections import Counter

def is_subset(main: list[int], subset: list[int]) -> bool:
    main_count   = Counter(main)
    subset_count = Counter(subset)
    return all(main_count[k] >= subset_count[k] for k in subset_count)

print(is_subset([1, 2, 3, 4, 5], [2, 4]))     # True
print(is_subset([1, 2, 2, 3],    [2, 2, 2]))   # False
print(is_subset([1, 2, 3],       []))           # True
```

**Complexity:** Time O(n + m) — Space O(n + m)

**Interview Tip:** Using `Counter` handles the duplicate-count case that a simple `set` check misses. This is the most common mistake in this problem.

---

## **Q29 — Maximum Circular Subarray Sum**

**Problem:** Find the maximum sum of a subarray in a circular list (the subarray can wrap around).

```
Input:  [1, -2, 3, -2]
Output: 3

Input:  [5, -3, 5]
Output: 10   (wraps around: 5 + 5)
```

```python
# Brute Force — double the list and apply Kadane's, O(n²)
def max_circular_brute(nums: list[int]) -> int:
    n = len(nums)
    doubled = nums + nums
    max_sum = nums[0]
    for i in range(n):
        current = 0
        for j in range(i, i + n):
            current += doubled[j]
            max_sum  = max(max_sum, current)
    return max_sum
```

```python
# Optimal — Kadane's on original + total sum minus Kadane's on negated list, O(n)
def max_circular(nums: list[int]) -> int:
    def kadane(arr: list[int]) -> int:
        cur = best = arr[0]
        for num in arr[1:]:
            cur  = max(num, cur + num)
            best = max(best, cur)
        return best

    max_straight = kadane(nums)
    total        = sum(nums)
    min_subarray = kadane([-x for x in nums])   # min subarray = -(max of negated)
    max_circular_val = total + min_subarray

    if max_circular_val == 0:    # all elements are negative — skip circular case
        return max_straight
    return max(max_straight, max_circular_val)

print(max_circular([1, -2, 3, -2]))  # 3
print(max_circular([5, -3, 5]))      # 10
print(max_circular([-3, -2, -3]))    # -2
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** The key insight: the circular subarray either does NOT wrap (standard Kadane's) or DOES wrap. When it wraps, the answer is `total_sum - min_subarray_sum`. The `min_subarray` is found by running Kadane's on the negated list.

---

## **Q30 — Next Permutation**

**Problem:** Rearrange the list in-place into the next lexicographically greater permutation. If the largest permutation, rearrange to the smallest (ascending order).

```
Input:  [1, 2, 3]   → [1, 3, 2]
Input:  [3, 2, 1]   → [1, 2, 3]
Input:  [1, 1, 5]   → [1, 5, 1]
```

```python
# Brute Force — generate all permutations and find the next one.
# Impractical for large inputs — O(n! * n).
```

```python
# Optimal — four-step algorithm, O(n) O(1) space
def next_permutation(nums: list[int]) -> None:
    n = len(nums)

    # Step 1: Find the rightmost element smaller than its right neighbour
    i = n - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1

    if i >= 0:
        # Step 2: Find the smallest element to the right of i that is larger than nums[i]
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
        # Step 3: Swap them
        nums[i], nums[j] = nums[j], nums[i]

    # Step 4: Reverse the suffix after index i to get the next smallest arrangement
    left, right = i + 1, n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left  += 1
        right -= 1

nums = [1, 2, 3]; next_permutation(nums); print(nums)  # [1, 3, 2]
nums = [3, 2, 1]; next_permutation(nums); print(nums)  # [1, 2, 3]
nums = [1, 1, 5]; next_permutation(nums); print(nums)  # [1, 5, 1]
```

**Complexity:** Time O(n) — Space O(1)

**Interview Tip:** The algorithm has four clear steps. State each one before coding. If `i` is -1 (entire list is descending) we skip the swap and just reverse — this gives the smallest permutation.

---

## **Complexity Summary Table**

| # | Problem | Brute Force | Optimal | Key Technique |
|---|---|---|---|---|
| 1 | Two Sum | O(n²) | O(n) | Hashmap complement lookup |
| 2 | Maximum Subarray Sum | O(n²) | O(n) | Kadane's algorithm |
| 3 | Second Largest Element | O(n log n) | O(n) | Two-variable scan |
| 4 | Move Zeroes to End | O(n) O(n) | O(n) O(1) | Two-pointer in-place |
| 5 | Remove Duplicates Sorted | O(n) O(n) | O(n) O(1) | Two-pointer write/read |
| 6 | Rotate a List | O(n * k) | O(n) O(1) | Three-reverse trick |
| 7 | Find Missing Number | O(n log n) | O(n) O(1) | Math sum or XOR |
| 8 | Product Except Self | O(n²) | O(n) O(1) | Prefix + suffix product |
| 9 | Maximum Product Subarray | O(n²) | O(n) | Track max and min both |
| 10 | Find All Duplicates | O(n²) | O(n) O(1) | Negate-at-index marking |
| 11 | Best Time to Buy Stock | O(n²) | O(n) | Track running minimum |
| 12 | Subarray Sum Equals K | O(n²) | O(n) | Prefix sum + hashmap |
| 13 | Three Sum | O(n³) | O(n²) | Sort + two-pointer |
| 14 | Container With Most Water | O(n²) | O(n) | Two-pointer, move shorter |
| 15 | Trapping Rain Water | O(n²) | O(n) O(1) | Two-pointer with max tracking |
| 16 | Majority Element | O(n²) | O(n) O(1) | Boyer-Moore Voting |
| 17 | Find Peak Element | O(n) | O(log n) | Binary search on slope |
| 18 | Merge Two Sorted Lists | O(n log n) | O(n + m) | Two-pointer merge |
| 19 | Sort 0s 1s 2s | O(n) | O(n) O(1) | Dutch National Flag |
| 20 | Flatten Nested List | O(n) | O(n) | Iterative stack |
| 21 | Max Sum Subarray Size K | O(n * k) | O(n) | Fixed sliding window |
| 22 | All Pairs with Given Sum | O(n²) | O(n) | Hashset complement |
| 23 | Alternate Positive Negative | O(n) | O(n) | Separate and interleave |
| 24 | Longest Consecutive Sequence | O(n log n) | O(n) | Hashset + start-of-sequence |
| 25 | First Missing Positive | O(n²) | O(n) O(1) | Cyclic index placement |
| 26 | Spiral Matrix Traversal | O(m*n) O(m*n) | O(m*n) O(1) | Four shrinking boundaries |
| 27 | K-th Largest Element | O(n log n) | O(n) avg | QuickSelect / min-heap |
| 28 | Check Subset | O(n * m) | O(n + m) | Counter comparison |
| 29 | Max Circular Subarray Sum | O(n²) | O(n) | Kadane's + total - min |
| 30 | Next Permutation | O(n! * n) | O(n) O(1) | Four-step suffix trick |

---

## **Interview Strategy**

Follow this approach every time a list problem is asked:

1. **Clarify** — ask about: duplicates, negative numbers, empty input, sorted or unsorted, in-place requirement, integer overflow.
2. **State brute force** — say the complexity out loud even if you will not code it. Shows problem understanding.
3. **Identify the pattern** — most list problems map to one of the six patterns below.
4. **Code the optimal** — write clean functions with type hints and meaningful variable names.
5. **Test with edge cases** — empty list, single element, all same values, all negative, k = length of list.
6. **State complexity** — always give both time and space at the end.

| Pattern | When to use |
|---|---|
| Two-pointer (opposite ends) | Sorted lists, pairs/triplets summing to target, containers |
| Two-pointer (same direction) | Remove duplicates, move elements, partition |
| Sliding window (fixed) | Max/min sum of k elements |
| Sliding window (variable) | Longest/shortest subarray with condition |
| Prefix sum + hashmap | Subarray sum equals target, count of subarrays |
| Hashmap / Counter | Frequency counting, complement lookup, anagrams |
| Kadane's | Maximum/minimum subarray sum or product |
| Binary search | Sorted list, finding boundaries, peak finding |
| Greedy + two-pointer | Trapping water, container problem |
| QuickSelect / Heap | K-th largest/smallest element |