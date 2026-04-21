from collections import Counter
import itertools

# ---------- Helper: ensure JSON-safe keys ----------
def stringify_dict(d):
    return {str(k): v for k, v in d.items()}


# ---------- 1-WL ----------
def run_1wl(G):
    colors = {v: G.degree[v] for v in G.nodes()}
    iterations = [stringify_dict(colors)]

    for _ in range(len(G.nodes())):
        new_colors = {}

        for v in G.nodes():
            neigh = sorted(colors[u] for u in G.neighbors(v))
            new_colors[v] = hash((colors[v], tuple(neigh)))

        if new_colors == colors:
            break

        colors = new_colors
        iterations.append(stringify_dict(colors))

    return {
        "iterations": iterations,
        "final_colors": stringify_dict(colors)
    }


# ---------- k-WL (k >= 2) ----------
def run_kwl(G, k):
    nodes = list(G.nodes())
    tuples = list(itertools.product(nodes, repeat=k))

    def tuple_key(t):
        return tuple(t)

    colors = {}

    # ---- Initial coloring ----
    for t in tuples:
        degrees = tuple(G.degree[v] for v in t)

        adj_pattern = tuple(
            1 if G.has_edge(t[i], t[j]) else 0
            for i in range(k) for j in range(i+1, k)
        )

        eq_pattern = tuple(
            1 if t[i] == t[j] else 0
            for i in range(k) for j in range(i+1, k)
        )

        colors[tuple_key(t)] = hash((degrees, adj_pattern, eq_pattern))

    # ---- Convert tuple colors → node colors ----
    def node_colors_from_tuple(colors):
        freq = {v: {} for v in nodes}

        for t in tuples:
            c = colors[tuple_key(t)]
            for v in t:
                freq[v][c] = freq[v].get(c, 0) + 1

        result = {}
        for v in nodes:
            result[v] = max(freq[v], key=freq[v].get)

        return result

    iterations = [stringify_dict(node_colors_from_tuple(colors))]

    # ---- Refinement loop ----
    for _ in range(50):
        new_colors = {}

        for t in tuples:
            neighbor_multiset = []

            for i in range(k):
                for nbr in G.neighbors(t[i]):
                    new_t = list(t)
                    new_t[i] = nbr
                    neighbor_multiset.append(colors[tuple_key(tuple(new_t))])

            neighbor_multiset.sort()

            new_colors[tuple_key(t)] = hash((
                colors[tuple_key(t)],
                tuple(neighbor_multiset)
            ))

        if new_colors == colors:
            break

        colors = new_colors
        iterations.append(stringify_dict(node_colors_from_tuple(colors)))

    return {
        "iterations": iterations,
        "final_tuple_colors": {
            str(k): v for k, v in colors.items()   # 🔥 FIX HERE
        }
    }


# ---------- Dispatcher ----------
def run_wl(G, k):
    if k == 1:
        return run_1wl(G)
    return run_kwl(G, k)


# ---------- Compare ----------
def compare_graphs(G1, G2, k):
    r1 = run_wl(G1, k)
    r2 = run_wl(G2, k)

    cert1 = Counter(r1["iterations"][-1].values())
    cert2 = Counter(r2["iterations"][-1].values())

    return {
        "isomorphic": cert1 == cert2,
        "iter1": r1["iterations"],
        "iter2": r2["iterations"]
    }