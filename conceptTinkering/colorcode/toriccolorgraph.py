import networkx as nx
from networkx.algorithms import coloring
import matplotlib.pyplot as plt
import random 

g = nx.Graph()

# we want a 48 node toric color code, like in the delfosse paper
g.add_nodes_from([i for i in range(1,49)])
def connectionmaker(g):
    rgb = set("r")
    rgb.add("g")
    rgb.add("b")
    for count, node1 in enumerate(g.nodes):
        print(count)
        # node already fully connected
        neighbors = list(g.neighbors(node1))
        if len(neighbors) == 3:
            continue
        
        # make a set of colors node is looking for
        wanted_colors = set()
        for neighbor in g[node1]:
            edge = g[node1][neighbor]
            color = edge.get('color', None)
            wanted_colors.add(color)
        wanted_colors = rgb - wanted_colors

        # loop through all other nodes
        for node2 in g.nodes:
            ########## !!!!!!!!!!!!!!!! ################
            #### THIS IS THE BAD EFFICIENCY BLOCK ####
            ### But it needs to be here because neighbors change ###
            node1_fourth_neighbors = set()
            for n1 in g.neighbors(node1):
                node1_fourth_neighbors.add(n1)
                for n2 in g.neighbors(n1):
                    node1_fourth_neighbors.add(n2)
                    for n3 in g.neighbors(n2):
                        node1_fourth_neighbors.add(n3)
                        for n4 in g.neighbors(n3):
                            node1_fourth_neighbors.add(n4)
            ########## !!!!!!!!!!!!!!!! ################
            # check we're not comparing the same node with itself
            if node2 == node1 or node2 in node1_fourth_neighbors:
                continue
            # check existing edges on node2 for color conflicts
            if len(g.adj[node2]) == 3:
                continue
            conflicted_colors = set()
            for neighbor in g[node2]:
                edge = g[node2][neighbor]
                color = edge.get('color', None)
                if color in wanted_colors:
                    conflicted_colors.add(color)
            # we only want to make connections if they're valid
            valid_colors = wanted_colors-conflicted_colors
            if not valid_colors:
                continue
            
            # pick a color and connect node1 node2 with that color
            picked_color = random.sample(valid_colors, 1)[0]
            g.add_edge(node1, node2, color=picked_color)
            wanted_colors.remove(picked_color)
    return True

connectionmaker(g)
# draw the graph
pos = nx.spring_layout(g)
edge_colors = [g[u][v]['color'] for u, v in g.edges()]
nx.draw(g, pos, with_labels=True, edge_color=edge_colors)

plt.show()

        