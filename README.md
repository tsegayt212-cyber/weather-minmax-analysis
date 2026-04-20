# Divide & Conquer Min-Max Temperature Analysis

> 🎬 **Demo video** — see `demo/demo.mp4` locally or watch via the link below after uploading to YouTube/Google Drive.

A Python project that implements and visualizes the **Divide and Conquer** algorithm for finding minimum and maximum values in a weather temperature dataset.

## Project Overview

This project compares two algorithms for the min-max problem:
- **Iterative** — single-pass scan, O(n) time, O(1) space, up to 2(n-1) comparisons
- **Divide & Conquer** — recursive halving, O(n) time, O(log n) space, exactly **3n/2 - 2** comparisons (proven optimal)

The project includes an interactive animated GUI with 6 tabs, a world map visualization, and auto-generated HTML and Word reports.

---

## Project Structure

```
weather-minmax-analysis/
├── src/
│   ├── algorithms/
│   │   ├── divide_conquer_min_max.py   # D&C algorithm + recursion tree builder
│   │   ├── iterative_min_max.py        # Iterative algorithm
│   │   └── min_max_result.py           # Result container
│   ├── visualization/
│   │   ├── animation.py                # Animated GUI (tkinter + matplotlib)
│   │   └── graphics.py                 # Static matplotlib charts
│   └── utils/
│       ├── data_loader.py              # CSV loading + random data generation
│       └── performance_analyzer.py     # Timing and comparison count tests
├── data/
│   └── sample_countries.csv            # 100 countries with temperatures
├── docs/
│   ├── reports/                        # Per-criterion assignment reports
│   ├── REPORT.md                       # Full assignment report
│   ├── ASSIGNMENT_REPORT.md            # Summary report
│   └── THEORETICAL_ANALYSIS.md        # Theoretical complexity analysis
├── output/                             # Generated charts and reports (git-ignored)
├── main.py                             # Entry point
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Features

- **6-tab animated GUI**
  - Data Overview — all countries bar chart with min/max highlighted
  - D&C Animation — step-by-step array split & merge with country labels
  - Recursion Tree — top-down tree nodes lighting up as algorithm runs
  - Performance — animated execution time comparison chart
  - Comparisons — iterative vs D&C vs theoretical 3n/2-2
  - World Map — countries plotted on a world map colored by temperature

- **Controls**: Run, Pause/Resume, Reset, Speed slider (100ms–2500ms)
- **Sound effects** on each algorithm step (split, base case, merge, done)
- **HTML report** auto-generated after each run
- **Word report** generated via `generate_word_report.py`

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/weather-minmax-analysis.git
cd weather-minmax-analysis

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py
```

When prompted:
- Enter `data/sample_countries.csv` to use real country data
- Press Enter to generate random data (specify size, default 1000)

To generate the Word report:
```bash
python generate_word_report.py
```

---

## Algorithm Analysis

| Algorithm | Comparisons (worst) | Comparisons (best) | Space | Deterministic |
|---|---|---|---|---|
| Iterative | 2(n-1) | n-1 | O(1) | No |
| Divide & Conquer | 3n/2-2 | 3n/2-2 | O(log n) | Yes |

The D&C algorithm achieves the **proven lower bound** of 3n/2-2 comparisons — no comparison-based algorithm can do better.

**Recurrence relation:** `T(n) = 2T(n/2) + 2` → solves to `T(n) = 3n/2 - 2`

---

## Dataset

`data/sample_countries.csv` contains average annual temperatures for 100 countries.

| Column | Description |
|---|---|
| country | Country name |
| temperature | Average annual temperature (°C) |

Sample:
```
country,temperature
Canada,-5.3
Niger,29.1
Finland,1.2
```

---

## Requirements

- Python 3.8+
- matplotlib
- numpy
- tkinter (built-in)
- pygame (optional, for sound)
- python-docx (for Word report generation)

---

## Academic Context

**Course:** Design and Analysis of Algorithms  
**Institution:** Aksum University — Department of Computer Science  
**Assignment:** Group Project — Divide and Conquer Algorithm  
**Submitted to:** Instructor Equbay

---

## References

- Cormen, T. H. et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
- Knuth, D. E. (1998). *The Art of Computer Programming, Vol. 3*. Addison-Wesley.
