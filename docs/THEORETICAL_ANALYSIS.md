# Theoretical Analysis: Min-Max Finding Algorithms

## Table of Contents
1. [Recurrence Relations](#recurrence-relations)
2. [Solving the Recurrence](#solving-the-recurrence)
3. [Comparison Count Proof](#comparison-count-proof)
4. [Complexity Analysis](#complexity-analysis)
5. [Mathematical Proofs](#mathematical-proofs)

---

## 1. Recurrence Relations

### 1.1 Divide and Conquer Recurrence

Let T(n) represent the number of comparisons needed to find min and max of n elements.

**Base Cases:**
- T(1) = 0 (single element, no comparisons)
- T(2) = 1 (two elements, one comparison)

**Recursive Case (n > 2):**
```
T(n) = T(⌊n/2⌋) + T(⌈n/2⌉) + 2
```

**Explanation:**
- Split array into two halves: left (⌊n/2⌋ elements) and right (⌈n/2⌉ elements)
- Recursively find min/max in left half: T(⌊n/2⌋) comparisons
- Recursively find min/max in right half: T(⌈n/2⌉) comparisons
- Merge results: 2 comparisons (one for min, one for max)

**Simplified (assuming n is power of 2):**
```
T(n) = 2T(n/2) + 2
T(2) = 1
T(1) = 0
```

---

## 2. Solving the Recurrence

### 2.1 Method 1: Recursion Tree

```
Level 0:                    T(n)                    → 2 comparisons
                           /    \
Level 1:            T(n/2)      T(n/2)              → 2×2 = 4 comparisons
                    /   \        /   \
Level 2:      T(n/4) T(n/4) T(n/4) T(n/4)          → 4×2 = 8 comparisons
                ...
Level k:      T(1)  T(1)  ...  T(1)                → n/2 leaves, T(2) pairs
```

**Analysis:**
- Height of tree: log₂(n) levels
- At each level i (except leaves): 2^i nodes, each contributing 2 comparisons
- Total internal comparisons: 2 + 4 + 8 + ... + 2^(log₂(n)-1) = 2(n/2 - 1) = n - 2
- Leaf level: n/2 pairs, each needs 1 comparison = n/2
- **Total: T(n) = n/2 + (n - 2) = 3n/2 - 2**

### 2.2 Method 2: Substitution

Assume T(n) = cn + d for some constants c and d.

Substitute into recurrence:
```
T(n) = 2T(n/2) + 2
cn + d = 2(c(n/2) + d) + 2
cn + d = cn + 2d + 2
d = 2d + 2
d = -2
```

Using base case T(2) = 1:
```
c(2) + d = 1
2c - 2 = 1
c = 3/2
```

Therefore: **T(n) = (3/2)n - 2 = 3n/2 - 2**

### 2.3 Method 3: Master Theorem

Recurrence: T(n) = 2T(n/2) + 2

Master Theorem form: T(n) = aT(n/b) + f(n)
- a = 2 (number of subproblems)
- b = 2 (size reduction factor)
- f(n) = 2 (merge cost)

Compare f(n) with n^(log_b(a)) = n^(log₂(2)) = n^1 = n:
- f(n) = 2 = O(n^0)
- Since f(n) = O(n^(log_b(a) - ε)) for ε = 1

**Case 1 applies**: T(n) = Θ(n^(log_b(a))) = Θ(n)

More precisely: T(n) = 3n/2 - 2 = Θ(n)

---

## 3. Comparison Count Proof

### 3.1 Divide and Conquer: 3n/2 - 2

**Theorem**: The divide-and-conquer algorithm performs exactly 3n/2 - 2 comparisons for n elements (when n is a power of 2).

**Proof by Inducti