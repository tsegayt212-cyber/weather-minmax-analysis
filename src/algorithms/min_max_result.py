class MinMaxResult:
    """Container for min, max, and comparison count."""
    def __init__(self, min_val, max_val, comparisons):
        self.min = min_val
        self.max = max_val
        self.comparisons = comparisons

    def __str__(self):
        return f"Min = {self.min:.2f}, Max = {self.max:.2f}, Comparisons = {self.comparisons}"