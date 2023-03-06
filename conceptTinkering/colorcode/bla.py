import networkx as nx
import matplotlib.pyplot as plt

# Create a graph with existing node attributes
G = nx.Graph()
G.add_node(1, color='red')
G.add_node(2, color='green')
G.add_node(3, color='blue')

# Add new attributes to each node using add_nodes_from()
new_attrs = {'size': 10, 'shape': 'circle'}
for node in G.nodes():
    G.nodes[node].update(new_attrs)

# Print the node attributes
for node, data in G.nodes(data=True):
    print(node, data)
