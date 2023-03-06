import networkx as nx

G = nx.Graph()  # Initialize a graph

# Add nodes
G.add_node(0)
G.add_node(1)
G.add_node(2)

# Add edges with attributes
G.add_edge(0, 1, weight=1)
G.add_edge(1, 2, weight=2)
G.add_edge(2, 0, weight=3)

# Add attributes to existing edge
for u, v, attr in G.edges(data=True):
    if (u, v) == (0, 1):
        G[u][v]['color'] = 'red'

# Print edges with attributes
print("Edges with attributes:")
for u, v, attr in G.edges(data=True):
    print(f"({u}, {v}): {attr}")

