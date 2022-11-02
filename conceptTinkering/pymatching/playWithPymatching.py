from pymatching import Matching
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import inspect

p = 0.2
g = nx.Graph()
g.add_edge(0, 1, fault_ids=0, weight=np.log((1-p)/p), error_probability=p)
g.add_edge(1, 2, fault_ids=1, weight=np.log((1-p)/p), error_probability=p)
g.add_edge(2, 3, fault_ids=2, weight=np.log((1-p)/p), error_probability=p)
g.add_edge(3, 4, fault_ids=3, weight=np.log((1-p)/p), error_probability=p)
g.add_edge(4, 5, fault_ids=4, weight=np.log((1-p)/p), error_probability=p)

g.nodes[0]['is_boundary'] = True
g.nodes[5]['is_boundary'] = True

g.add_edge(0, 5, weight=0.0, fault_ids=-1, error_probability=0.0)

p2 = 0.12
g.add_edge(2, 4, fault_ids={2, 3}, weight=np.log((1-p2)/p2), error_probability=p2)

m = Matching(g)
 

m.draw()

# plt.show()

stuff = inspect.getsource(Matching.decode)
with open("what", "w") as text_file:
    text_file.write(stuff)