# Algorithm Design /4

## Algorithm 1 — Iterative

```
function iterative_min_max(arr):
    min_val = max_val = arr[0]
    comparisons = 0

    for x in arr[1:]:
        comparisons += 1
        if x < min_val:
            min_val = x
        else:
            comparisons += 1
            if x > max_val:
                max_val = x

    return min_val, max_val, comparisons
```

- Each element is compared against min first
- If not smaller, it is compared against max
- Best case: **n-1** comparisons (sorted descending)
- Worst case: **2(n-1)** comparisons (sorted ascending)

---

## Algorithm 2 — Divide and Conquer

```
function dc_min_max(arr, left, right):

    // Base case 1: single element
    if left == right:
        return (arr[left], arr[left])

    // Base case 2: two elements — 1 comparison
    if right - left == 1:
        comparisons += 1
        if arr[left] < arr[right]:
            return (arr[left], arr[right])
        else:
            return (arr[right], arr[left])

    // Divide
    mid = (left + right) / 2

    // Conquer
    left_min,  left_max  = dc_min_max(arr, left,   mid)
    right_min, right_max = dc_min_max(arr, mid+1,  right)

    // Combine — 2 comparisons
    comparisons += 2
    overall_min = min(left_min,  right_min)
    overall_max = max(left_max,  right_max)

    return overall_min, overall_max
```

---

## Recurrence Relation

```
T(1) = 0          // single element, no comparison needed
T(2) = 1          // one comparison for two elements
T(n) = 2T(n/2) + 2    // two subproblems + 2 merge comparisons
```

---

## Solving the Recurrence

Expanding T(n) for n = 2^k:

```
T(n) = 2T(n/2) + 2
     = 2[2T(n/4) + 2] + 2
     = 4T(n/4) + 4 + 2
     = 4[2T(n/8) + 2] + 6
     = 8T(n/8) + 8 + 4 + 2
     ...
     = (n/2) · T(2) + (n - 2)
     = (n/2) · 1   + (n - 2)
     = 3n/2 - 2
```

**Closed form: T(n) = 3n/2 − 2**

---

## Comparison Table

| n    | Iterative worst (2n-2) | D&C exact (3n/2-2) | Savings |
|------|------------------------|---------------------|---------|
| 8    | 14                     | 10                  | 28.6%   |
| 16   | 30                     | 22                  | 26.7%   |
| 64   | 126                    | 94                  | 25.4%   |
| 256  | 510                    | 382                 | 25.1%   |
| 1024 | 2046                   | 1534                | 25.0%   |

---

## Recursion Tree Diagram (n=8)

```
                    [0..7]
                   /      \
            [0..3]          [4..7]
           /      \        /      \
        [0..1]  [2..3]  [4..5]  [6..7]
```

- Leaf pairs each cost **1 comparison**
- Each internal merge costs **2 comparisons**
- Total for n=8: 4×1 + 3×2 = **10 comparisons** ✓
