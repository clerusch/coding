import networkx as nx
import matplotlib.pyplot as plt

g = nx.Graph()

g.add_nodes_from([i for i in range(1,8)])
g.add_edge(1,2,color='blue')
g.add_edge(1,6,color='green')
g.add_edge(7,6,color='green')
g.add_edge(2,7,color='blue')
g.add_edge(5,6,color='green')
g.add_edge(5,4,color='red')
g.add_edge(4,7,color='red')
g.add_edge(4,3,color='red')
g.add_edge(3,2,color='blue')

pos = nx.spring_layout(g)
edge_colors = [g[u][v]['color'] for u, v in g.edges()]
nx.draw(g, pos, edge_color=edge_colors, with_labels=True)
plt.show()

# dualg = nx.complement(g)
# pos = nx.spring_layout(dualg)
# edge_colors = [g[u][v]['color'] for u, v in dualg.edges()]
# nx.draw(dualg)
# plt.show()
