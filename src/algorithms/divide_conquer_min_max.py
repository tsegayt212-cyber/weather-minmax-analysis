from src.algorithms.min_max_result import MinMaxResult

class RecNode:
    """Node for recursion tree."""
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.min = None
        self.max = None
        self.left_child = None
        self.right_child = None

class DivideConquerMinMax:
    comparisons = 0
    root = None

    @classmethod
    def find_min_max(cls, arr):
        cls.comparisons = 0
        if not arr:
            return MinMaxResult(float('nan'), float('nan'), 0)
        pair = cls._find_min_max_rec(arr, 0, len(arr)-1)
        return MinMaxResult(pair[0], pair[1], cls.comparisons)

    @classmethod
    def _find_min_max_rec(cls, arr, l, r):
        if l == r:
            return (arr[l], arr[l])
        if r - l == 1:
            cls.comparisons += 1
            if arr[l] < arr[r]:
                return (arr[l], arr[r])
            else:
                return (arr[r], arr[l])
        mid = (l + r) // 2
        left_min, left_max = cls._find_min_max_rec(arr, l, mid)
        right_min, right_max = cls._find_min_max_rec(arr, mid+1, r)
        cls.comparisons += 2
        overall_min = left_min if left_min < right_min else right_min
        overall_max = left_max if left_max > right_max else right_max
        return (overall_min, overall_max)

    @classmethod
    def build_tree(cls, arr):
        cls.comparisons = 0
        cls.root = cls._build_tree_rec(arr, 0, len(arr)-1)
        return cls.root

    @classmethod
    def _build_tree_rec(cls, arr, l, r):
        node = RecNode(l, r)
        if l == r:
            node.min = node.max = arr[l]
            return node
        if r - l == 1:
            cls.comparisons += 1
            if arr[l] < arr[r]:
                node.min, node.max = arr[l], arr[r]
            else:
                node.min, node.max = arr[r], arr[l]
            return node
        mid = (l + r) // 2
        node.left_child = cls._build_tree_rec(arr, l, mid)
        node.right_child = cls._build_tree_rec(arr, mid+1, r)
        cls.comparisons += 2
        node.min = node.left_child.min if node.left_child.min < node.right_child.min else node.right_child.min
        node.max = node.left_child.max if node.left_child.max > node.right_child.max else node.right_child.max
        return node

def print_tree(node, depth=0):
    """Print recursion tree."""
    if node is None:
        return
    indent = "  " * depth
    print(f"{indent}[{node.left}..{node.right}] min={node.min:.2f} max={node.max:.2f}")
    print_tree(node.left_child, depth+1)
    print_tree(node.right_child, depth+1)