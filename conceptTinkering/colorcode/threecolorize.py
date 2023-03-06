import networkx as nx
import random 
import matplotlib.pyplot as plt

def draw(G):
    pos = nx.get_node_attributes(G, 'pos') #nx.kamada_kawai_layout(G)
    edge_colors = [G[u][v]['color'] for u, v in G.edges()]
    nx.draw(G, pos, with_labels=True, edge_color=edge_colors)

    plt.show()

def colorize_graph_black(G):
    for edge in G.edges():
        u = edge[0]
        v = edge[1]
        G.remove_edge(u,v)
        G.add_edge(u,v,color='black')

def three_colorize_a_black_graph(G):
    rgb = set("r")
    rgb.add("g")
    rgb.add("b")
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
        # we also need to check if adding this color would make a 3-colored 6 cycle somehow

        if remaining_colors:
            picked_color = random.sample(remaining_colors, 1)[0]
            G.remove_edge(first_node, second_node)
            G.add_edge(first_node, second_node, color=picked_color)


def three_colorize_a_black_graph(G):
    """
    Takes an nx graph with some black edges and colors
    it with red, green and blue such that all nodes are
    connected to each of the colors exactly once
    """
    rgb = set("r")
    rgb.add("g")
    rgb.add("b")
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
        # we also need to check if adding this color would make a 3-colored 6 cycle somehow

        if remaining_colors:
            picked_color = random.sample(remaining_colors, 1)[0]
            G.remove_edge(first_node, second_node)
            G.add_edge(first_node, second_node, color=picked_color)