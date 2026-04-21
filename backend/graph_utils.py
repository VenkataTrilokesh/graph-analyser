import networkx as nx

def parse_graph(text):
    G = nx.Graph()

    lines = [
        l.strip() for l in text.splitlines()
        if l.strip() and not l.startswith('#') and not l.startswith('%')
    ]

    for line in lines:
        parts = line.replace(',', ' ').split()
        if len(parts) < 2:
            continue

        u, v = int(parts[0]), int(parts[1])
        G.add_edge(u, v)

    return G