# Report Quality /5

## Project Overview

This project implements, analyzes, and visualizes two algorithms for finding the
minimum and maximum temperature values in a weather dataset:

- **Iterative Min-Max** — single-pass scan
- **Divide and Conquer Min-Max** — recursive halving

The project uses real country temperature data (100 countries) and synthetic random
data to compare both algorithms experimentally and theoretically.

---

## Summary of Findings

### 1. Correctness
Both algorithms produce identical results on all tested datasets. ✓

### 2. Comparison Count
The Divide and Conquer algorithm uses exactly **3n/2 - 2** comparisons, which is:
- ~25% fewer than iterative worst case (2n - 2)
- Deterministic — same count regardless of input order
- Provably optimal — no comparison-based algorithm can do better

### 3. Time Complexity
Both algorithms are **O(n)**. D&C is slower in Python due to function call overhead,
but the comparison count advantage holds in all languages.

### 4. Space Complexity
- Iterative: **O(1)** — no extra memory
- D&C: **O(log n)** — recursion stack, negligible in practice

### 5. Visualization
The project includes a full animated GUI with 3 tabs:
- Bar chart showing array split and merge step by step
- Recursion tree with nodes lighting up as the algorithm visits them
- Performance chart with animated line drawing

---

## Tools & Technologies

| Tool | Purpose |
|---|---|
| Python 3.x | Main programming language |
| tkinter | GUI window and tab controls |
| matplotlib | Charts and animations embedded in GUI |
| numpy | Tone generation for sound effects |
| pygame | Sound playback (split / merge / done tones) |
| networkx | Static recursion tree graph |
| csv module | Reading sample_countries.csv |
| random module | Generating synthetic test data |

---

## File Organization

```
weather-minmax-analysis/
├── main.py
├── data_loader.py
├── iterative_min_max.py
├── divide_conquer_min_max.py
├── min_max_result.py
├── performance_analyzer.py
├── graphics.py
├── animation.py
├── sample_countries.csv
├── THEORETICAL_ANALYSIS.md
└── reports/
    ├── 01_Problem_Understanding.md
    ├── 02_Algorithm_Design.md
    ├── 03_Code_Implementation.md
    ├── 04_Arrays_and_Core_Concepts.md
    ├── 05_Time_and_Space_Analysis.md
    ├── 06_Experimentation_with_Data.md
    └── 07_Report_Quality.md
```

---

## How to Run

```bash
# Install dependencies
pip install matplotlib numpy pygame networkx

# Run the project
python main.py
```

When prompted:
- Enter `sample_countries.csv` to use real data
- Press Enter to generate random data (default 1000 records)

The animated GUI opens automatically after the terminal output.

---

## Conclusion

The Divide and Conquer algorithm is the **theoretically optimal** solution to the
min-max problem, achieving the proven lower bound of 3n/2 - 2 comparisons.

For practical Python use with small datasets, the iterative approach runs faster
due to lower overhead. For large datasets in compiled languages (C, Java), D&C
would be preferred for its reduced comparison count and deterministic behavior.

This project demonstrates the algorithm through real data, theoretical analysis,
experimental verification, and interactive animated visualization.
