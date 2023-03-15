from pymatching import Matching
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

p = 0.2
w = np.log((1-p)/p)
g = nx.Graph ()

g. add_edge (0, 1, fault_ids =0, weight =w, error_probability =p)
g. add_edge (1, 2, fault_ids =1, weight =w, error_probability =p)
g. add_edge (2, 3, fault_ids =2, weight =w, error_probability =p)
g. add_edge (3, 4, fault_ids =3, weight =w, error_probability =p)
g. add_edge (4, 5, fault_ids =4, weight =w, error_probability =p)

p2 = 0.12
w2 = np.log((1-p2) / p2)
g. add_edge (2, 4, fault_ids ={2 , 3}, weight =w2 , error_probability =p2)

g._node[0][ ' is_boundary ' ] = True
g._node[5][ ' is_boundary ' ] = True

g. add_edge (0, 5, weight =0.0 , fault_ids =set (), error_probability =0.0)

m = Matching(g)
m.draw()
plt.show()

