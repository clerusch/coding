import networkx as nx
import matplotlib.pyplot as plt
import random

# Convert the square grid to a hexagonal grid
G = nx.hexagonal_lattice_graph(5, 6, periodic=True)
rgb = set("r")
rgb.add("g")
rgb.add("b")

# draw the graph
def draw(G):
    pos = nx.spring_layout(G)
    edge_colors = [G[u][v]['color'] for u, v in G.edges()]
    nx.draw(G, pos, with_labels=True, edge_color=edge_colors)

    plt.show()

# for edge in G.edges:
#     node1, node2 = edge
#     onecolors = set()
#     twocolors = set()
#     for neighbor in G[node1]:
#         edge = G[node1][neighbor]
#         color = edge.get('color', None)
#         onecolors.add(color)
#     for neighbor in G[node2]:
#         edge = G[node2][neighbor]
#         color = edge.get('color', None)     
#         twocolors.add(color)    
#     valid_colors = rgb - onecolors - twocolors
#     if valid_colors:
#         picked_color = random.sample(valid_colors, 1)[0]
#         #G.add_edge(node1, node2, color=picked_color)
#         G[node1][node2]['color'] = picked_color

# battle plan:
# go through all edges and check which colors the composing nodes edges already has
for edge in G.edges():
    u = edge[0]
    v = edge[1]
    G.remove_edge(u,v)
    G.add_edge(u,v,color='black')
    #G[u][v]['color']= 'black'


for edge in G.edges():
    edge_colors = nx.get_edge_attributes(G, 'color')
    first_node = edge[0]
    second_node = edge[1]
    first_colors = set()
    second_colors = set()
    for edge1 in G.edges(first_node):
        sorted_key = tuple(sorted(edge1))
        color = edge_colors.get(sorted_key, None)
        if color == 'black':
            continue
        first_colors.add(color)
    for edge2 in G.edges(second_node):
        sorted_key = tuple(sorted(edge2))
        color = edge_colors.get(sorted_key, None)
        if color == 'black':
            continue
        second_colors.add(color)
    remaining_colors = rgb - first_colors - second_colors
    if remaining_colors:
        picked_color = random.sample(remaining_colors, 1)[0]
        G.remove_edge(first_node, second_node)
        G.add_edge(first_node, second_node, color=picked_color)
        #draw(G)
        # G[first_node][second_node]['color'] = picked_color

draw(G)

