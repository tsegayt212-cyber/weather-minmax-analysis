# Use of Arrays & Core Concepts /4

## Arrays

All temperature data is stored as a Python `List[float]` — Python's dynamic array.

### How arrays are used

| Usage | Code Example |
|---|---|
| Store all temperatures | `temps = [22.5, 12.3, 25.1, ...]` |
| Index-based access | `arr[l]`, `arr[r]`, `arr[mid]` |
| Subarray slicing (visualization) | `arr[left:right+1]` |
| Parallel label array | `labels = ["Afghanistan", "Albania", ...]` |
| Random generation | `[random.uniform(-30.0, 50.0) for _ in range(size)]` |

### Why arrays?
- O(1) random access by index — essential for D&C which jumps to `arr[mid]`
- Contiguous memory layout — cache-friendly for sequential scans
- No extra memory allocation during recursion (indices passed, not copies)

---

## Core Concept 1 — Recursion

The D&C algorithm is purely recursive. Each call reduces the problem size by half.

```python
def _find_min_max_rec(cls, arr, l, r):
    ...
    mid = (l + r) // 2
    left_result  = cls._find_min_max_rec(arr, l,     mid)   # recurse left
    right_result = cls._find_min_max_rec(arr, mid+1, r)     # recurse right
    ...
```

Recursion depth = **log₂(n)** — for n=1024, only 10 stack frames deep.

---

## Core Concept 2 — Base Cases

Two base cases stop the recursion:

```python
# Base case 1: single element — no comparison needed
if l == r:
    return (arr[l], arr[l])

# Base case 2: two elements — exactly 1 comparison
if r - l == 1:
    cls.comparisons += 1
    if arr[l] < arr[r]:
        return (arr[l], arr[r])
    else:
        return (arr[r], arr[l])
```

The two-element base case is the key to efficiency — it handles a pair with just
**1 comparison** instead of 2.

---

## Core Concept 3 — Divide, Conquer, Combine

| Step | What happens | Cost |
|---|---|---|
| Divide | `mid = (l + r) // 2` | O(1) |
| Conquer | Two recursive calls on halves | 2 × T(n/2) |
| Combine | Compare left_min vs right_min, left_max vs right_max | 2 comparisons |

---

## Core Concept 4 — Object-Oriented Programming

```python
class DivideConquerMinMax:
    comparisons = 0          # class-level state (shared across calls)

    @classmethod
    def find_min_max(cls, arr): ...

    @classmethod
    def _find_min_max_rec(cls, arr, l, r): ...

    @classmethod
    def build_tree(cls, arr): ...   # builds RecNode tree for visualization
```

```python
class RecNode:
    """Node in the recursion tree."""
    def __init__(self, left, right):
        self.left        = left
        self.right       = right
        self.min         = None
        self.max         = None
        self.left_child  = None
        self.right_child = None
```

---

## Core Concept 5 — File I/O and CSV Parsing

```python
with open(filename, 'r') as f:
    reader = csv.reader(f)
    next(reader)          # skip header row
    for row in reader:
        label = row[0].strip()
        value = float(row[1].strip())
```

The CSV file `sample_countries.csv` has the format:
```
country,temperature
Afghanistan,22.5
Albania,12.3
...
```

---

## Core Concept 6 — Separation of Concerns

Each module has a single responsibility:

| Module | Responsibility |
|---|---|
| `data_loader.py` | Load / generate data only |
| `iterative_min_max.py` | Iterative algorithm only |
| `divide_conquer_min_max.py` | D&C algorithm + tree building |
| `min_max_result.py` | Result data structure only |
| `performance_analyzer.py` | Timing and comparison tests |
| `graphics.py` | Static charts only |
| `animation.py` | Animated GUI only |
| `main.py` | Orchestration only |
