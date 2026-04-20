# Code Implementation /5

## Project Structure

```
weather-minmax-analysis/
├── main.py                    # Entry point — runs everything
├── data_loader.py             # CSV loading + random data generation
├── iterative_min_max.py       # Iterative algorithm
├── divide_conquer_min_max.py  # Divide & Conquer + recursion tree builder
├── min_max_result.py          # Result container (min, max, comparisons)
├── performance_analyzer.py    # Timing and comparison count tests
├── graphics.py                # Static matplotlib charts
├── animation.py               # Animated GUI (tkinter + matplotlib, 3 tabs)
├── sample_countries.csv       # Real dataset: 100 countries + temperatures
└── reports/                   # Assignment report files (one per criterion)
```

---

## min_max_result.py

Container class returned by both algorithms.

```python
class MinMaxResult:
    def __init__(self, min_val, max_val, comparisons):
        self.min = min_val
        self.max = max_val
        self.comparisons = comparisons

    def __str__(self):
        return f"Min={self.min:.2f}, Max={self.max:.2f}, Comparisons={self.comparisons}"
```

---

## iterative_min_max.py

```python
def find_min_max(arr):
    if not arr:
        return MinMaxResult(float('nan'), float('nan'), 0)
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
    return MinMaxResult(min_val, max_val, comparisons)
```

---

## divide_conquer_min_max.py

```python
class DivideConquerMinMax:
    comparisons = 0

    @classmethod
    def find_min_max(cls, arr):
        cls.comparisons = 0
        if not arr:
            return MinMaxResult(float('nan'), float('nan'), 0)
        pair = cls._find_min_max_rec(arr, 0, len(arr) - 1)
        return MinMaxResult(pair[0], pair[1], cls.comparisons)

    @classmethod
    def _find_min_max_rec(cls, arr, l, r):
        # Base case 1: single element
        if l == r:
            return (arr[l], arr[l])

        # Base case 2: two elements
        if r - l == 1:
            cls.comparisons += 1
            if arr[l] < arr[r]:
                return (arr[l], arr[r])
            else:
                return (arr[r], arr[l])

        # Divide
        mid = (l + r) // 2

        # Conquer
        left_min,  left_max  = cls._find_min_max_rec(arr, l,     mid)
        right_min, right_max = cls._find_min_max_rec(arr, mid+1, r)

        # Combine
        cls.comparisons += 2
        overall_min = left_min  if left_min  < right_min else right_min
        overall_max = left_max  if left_max  > right_max else right_max
        return (overall_min, overall_max)
```

---

## data_loader.py

```python
def load_data(filename=None, size=1000):
    """Returns (List[float], List[str]) — temperatures and labels."""
    if filename:
        try:
            data, labels = load_from_csv(filename)
            print(f"Loaded {len(data)} records from {filename}")
            return data, labels
        except Exception as e:
            print(f"Could not read CSV: {e}")
    return generate_random_data(size)

def load_from_csv(filename):
    temps, labels = [], []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            labels.append(row[0].strip())
            temps.append(float(row[1].strip()))
    return temps, labels

def generate_random_data(size):
    temps  = [random.uniform(-30.0, 50.0) for _ in range(size)]
    labels = [f"Record_{i+1}" for i in range(size)]
    return temps, labels
```

---

## main.py — Flow

```
1. Prompt user for CSV filename and dataset size
2. Load data  →  data_loader.load_data()
3. Run iterative algorithm  →  iterative_min_max.find_min_max()
4. Run D&C algorithm        →  DivideConquerMinMax.find_min_max()
5. Print results + coldest/hottest country
6. Build and print recursion tree for first 8 elements
7. Run performance tests across sizes [500, 1000, 5000]
8. Run comparison count analysis across sizes [1..1024]
9. Launch animated GUI  →  animation.animate(sample, perf_data)
10. Generate HTML report
```

---

## animation.py — GUI Tabs

| Tab | What it shows |
|---|---|
| Bar Chart | Bars change color as array is split and merged |
| Recursion Tree | Nodes light up one by one, showing min/max after resolve |
| Performance | Lines draw themselves point by point left to right |

Controls: ▶ Run, ↺ Reset, Speed slider
Sound: different tones for split / base case / merge / done
