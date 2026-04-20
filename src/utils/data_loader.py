import csv
import random
from typing import List, Tuple

def load_from_csv(filename: str) -> Tuple[List[float], List[str]]:
    """Read temperatures and labels from CSV. Expects columns: label, temperature."""
    temps = []
    labels = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        for row in reader:
            if len(row) < 2:
                continue
            try:
                label = row[0].strip()
                val = float(row[1].strip())
                temps.append(val)
                labels.append(label)
            except ValueError:
                continue
    return temps, labels

def generate_random_data(size: int) -> Tuple[List[float], List[str]]:
    """Generate random temperatures between -30 and 50 with generic labels."""
    temps = [random.uniform(-30.0, 50.0) for _ in range(size)]
    labels = [f"Record_{i+1}" for i in range(size)]
    return temps, labels

def load_data(filename: str = None, size: int = 1000) -> Tuple[List[float], List[str]]:
    """Load data from CSV if filename given, else generate random.
    Returns (temperatures, labels) tuple.
    """
    if filename:
        try:
            data, labels = load_from_csv(filename)
            print(f"Loaded {len(data)} records from {filename}")
            return data, labels
        except Exception as e:
            print(f"Could not read CSV: {e}")
            print(f"Generating random data of size {size}")
    return generate_random_data(size)
