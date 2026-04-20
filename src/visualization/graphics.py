import matplotlib.pyplot as plt
import networkx as nx

def plot_performance(sizes, iter_times, dc_times):
    """Plot execution time vs input size for both algorithms."""
    plt.figure(figsize=(10, 5))
    plt.plot(sizes, iter_times, 'o-', label='Iterative', color='blue')
    plt.plot(sizes, dc_times, 's-', label='Divide & Conquer', color='red')
    plt.xlabel('Input Size (n)')
    plt.ylabel('Execution Time (ms)')
    plt.title('Performance Comparison: Iterative vs Divide & Conquer')
    plt.legend()
    plt.grid(True)
    plt.savefig('performance_plot.png')
    plt.show()

def plot_comparisons(n_vals, iter_comps, dc_comps, theory_comps):
    """Plot comparison counts vs input size."""
    plt.figure(figsize=(10, 5))
    plt.plot(n_vals, iter_comps, 'o-', label='Iterative', color='blue')
    plt.plot(n_vals, dc_comps, 's-', label='Divide & Conquer (actual)', color='red')
    plt.plot(n_vals, theory_comps, '--', label='Theoretical D&C (3n/2-2)', color='green')
    plt.xlabel('Input Size (n)')
    plt.ylabel('Number of Comparisons')
    plt.title('Comparison Counts: Actual vs Theoretical')
    plt.legend()
    plt.grid(True)
    plt.savefig('comparisons_plot.png')
    plt.show()

def draw_recursion_tree(root_node):
    """Draw the recursion tree using networkx and matplotlib."""
    G = nx.DiGraph()
    labels = {}

    def add_nodes(node, parent=None):
        if node is None:
            return
        node_id = id(node)
        label = f"[{node.left}..{node.right}]\nmin={node.min:.2f}\nmax={node.max:.2f}"
        labels[node_id] = label
        G.add_node(node_id)
        if parent is not None:
            G.add_edge(parent, node_id)
        add_nodes(node.left_child, node_id)
        add_nodes(node.right_child, node_id)

    add_nodes(root_node)
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)  # for reproducibility
    nx.draw(G, pos, with_labels=False, node_size=3000, node_color='lightblue', arrows=False)
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    plt.title("Recursion Tree for Min-Max (Divide & Conquer)")
    plt.savefig('recursion_tree.png')
    plt.show()