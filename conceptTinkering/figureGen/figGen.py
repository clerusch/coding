import networkx as nx 
import numpy as np 
import matplotlib.pyplot as plt 
from pymatching import Matching

ring_matrix = np.array([[1,1,0],
                        [0,1,1],
                        [1,0,1]])

# ring_graph = nx.from_numpy_array(ring_matrix)
Matching = Matching(ring_matrix)
Matching.draw()
# nx.draw(ring_graph)
plt.savefig("img/figures/ring_graph.png")