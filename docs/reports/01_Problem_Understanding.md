# Problem Understanding /3

## Problem Statement

Given a dataset of country temperature records, find the **minimum** and **maximum**
temperature values efficiently.

The naive approach scans the array and compares every element against both min and max,
resulting in up to **2(n-1)** comparisons. The goal is to reduce this using the
**Divide and Conquer** strategy, which provably achieves **3n/2 - 2** comparisons —
roughly 25% fewer.

---

## Real-World Context

This project uses a dataset of average annual temperatures from 100 countries
(stored in `sample_countries.csv`). Finding the coldest and hottest country is a
direct application of the min-max problem.

Example from the dataset:
- Coldest: **Canada → -5.30°C**
- Hottest: **Niger → 29.10°C**

---

## Input / Output

| | Description |
|---|---|
| Input | Array of floating-point temperatures (from CSV or randomly generated) |
| Output | Minimum value, Maximum value, Number of comparisons made |

---

## Why Minimize Comparisons?

In large datasets (millions of sensor readings, satellite data, etc.):
- Fewer comparisons = fewer CPU cycles
- The min-max problem has a proven lower bound of **3n/2 - 2** comparisons
- Divide and Conquer reaches this lower bound — it is the **optimal** algorithm

---

## Problem Constraints

- Array size n ≥ 1
- Values are real numbers (floats), can be negative (e.g. -30°C)
- Both min and max must be found in a **single pass** through the recursion
- Comparison count must be tracked exactly
