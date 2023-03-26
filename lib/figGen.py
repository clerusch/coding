import networkx as nx 
import numpy as np 
import matplotlib.pyplot as plt 
from pymatching import Matching

g = nx.Graph()
g.add_node(1, node_shape='o', color='green')
g.add_node(2, node_shape='s', color='red')
g.add_node(3, node_shape='o', color='blue')
g.add_node(4, node_shape='s', color='blue')
g.add_node(5, node_shape='o', color='blue')
g.add_node(6, node_shape='s', color='red')
g.add_edge(1,2)
g.add_edge(3,2)
g.add_edge(3,4)
g.add_edge(4,5)
g.add_edge(5,6)
g.add_edge(6,1)
pos = nx.spring_layout(g)
labels = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}
node_colors = [data['color'] for _, data in g.nodes(data=True)] 
for node in g.nodes:
    nx.draw_networkx_nodes(g, pos, nodelist=[node], \
        node_shape=nx.get_node_attributes(g, "node_shape")[node],\
            node_color=nx.get_node_attributes(g, "color")[node])
nx.draw(g, pos, labels=labels, node_color=node_colors)
plt.savefig("img/figures/ring_3_graph.png")
