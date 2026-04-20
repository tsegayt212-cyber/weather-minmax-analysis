from src.algorithms.min_max_result import MinMaxResult

def find_min_max(arr):
    """Iterative single‑pass min‑max algorithm."""
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