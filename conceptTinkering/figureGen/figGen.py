import networkx as nx 
import numpy as np 
import matplotlib.pyplot as plt 
from pymatching import Matching

n=7
g = nx.grid_2d_graph(n,n)
# pos = {(i,j): (i,j) for i in range(n) for j in range(n)}
nx.draw(g)
plt.savefig("img/figures/bla_5_graph.png")