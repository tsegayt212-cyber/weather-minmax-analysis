import time
from src.utils.data_loader import generate_random_data
from src.algorithms.iterative_min_max import find_min_max as iterative_minmax
from src.algorithms.divide_conquer_min_max import DivideConquerMinMax

def test_method(name, method, sizes=[500, 1000, 5000]):
    """Run performance test on a given min‑max function."""
    print(f"\n=== {name} ===")
    for size in sizes:
        data, _labels = generate_random_data(size)
        for _ in range(3):
            method(data)
        start = time.perf_counter()
        result = method(data)
        elapsed = time.perf_counter() - start
        print(f"Size {size:5d}: {result}, Time = {elapsed*1000:.3f} ms")

def compare_comparisons():
    """Compare theoretical and actual comparisons."""
    print("\n=== Comparison Counts (theoretical vs actual) ===")
    sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    print("n\tIterative\tDC Actual\tDC Theory (3n/2-2)")
    for n in sizes:
        data, _labels = generate_random_data(n)
        iter_res = iterative_minmax(data)
        dc_res = DivideConquerMinMax.find_min_max(data)
        theory = int(1.5 * n - 2)
        print(f"{n}\t{iter_res.comparisons}\t\t{dc_res.comparisons}\t\t{theory}")