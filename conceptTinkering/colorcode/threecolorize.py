import networkx as nx
import random 
import matplotlib.pyplot as plt

def draw(G, filename=None):
    pos = nx.get_node_attributes(G, 'pos') #nx.kamada_kawai_layout(G)
    edge_colors = [G[u][v]['color'] for u, v in G.edges()]
    nx.draw(G, pos, with_labels=True, edge_color=edge_colors)
    if filename:
        plt.savefig(filename)
    else:
        plt.show()

def colorize_graph_black(G):
    for u, v, attr in G.edges(data=True):
        G[u][v]['color'] = 'black'

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
            if color != 'black':
                first_colors.add(color)
        for edge2 in G.edges(second_node):
            sorted_key = tuple(sorted(edge2))
            color = edge_colors.get(sorted_key, None)
            if color != 'black':
                second_colors.add(color)
        remaining_colors = rgb - first_colors - second_colors
        # we also need to check if adding this color would make a 3-colored 6 cycle somehow

        if remaining_colors:
            picked_color = random.sample(remaining_colors, 1)[0]
            G[first_node][second_node]['color'] = picked_color

def tor_hex48_color_encode(G: nx.Graph,m=6,n=4):
    """
    G: nx Graph
    n,m: how many by how many hexagon, default to 6 and 4 like in delfosse
    """
    rgb_list = ['r', 'g', 'b']
    # initialize all edge colors to black
    for u, v, attr in G.edges(data=True):
        G[u][v]['color'] = 'black'
    
    # colorizing algorithm
    
    # horizontal edges
    for i in range(int(n/2)):
            for j in range(m):
                first_coordinate = (2*i,2*j)
                second_coordinate = (2*i+1,2*j)
                G[first_coordinate][second_coordinate]['color'] = rgb_list[j%3]
    for i in range(int(n/2)):
        for j in range(m):
            first_coordinate = (2*i+1,2*j+1)
            second_coordinate = ((2*i+2)%n,2*j+1)
            G[first_coordinate][second_coordinate]['color'] = rgb_list[(j-1)%3]
    # left ladder edges
    for i in range(int(n/2)):
        for j in range(2*m):
            first_coordinate = (2*i,j)
            second_coordinate = (2*i,(j+1)%(2*m))
            G[first_coordinate][second_coordinate]['color'] = rgb_list[(1-j)%3]
    # right ladder edges
    for i in range(int(n/2)):
        for j in range(2*m):
            first_coordinate = (2*i+1,j)
            second_coordinate = (2*i+1,(j+1)%(2*m))
            G[first_coordinate][second_coordinate]['color'] = rgb_list[(1-j)%3]

def make_a_base_graph(m=6,n=4) -> nx.Graph:
    G = nx.hexagonal_lattice_graph(m, n, periodic=True)
    colorize_graph_black(G)
    tor_hex48_color_encode(G,m,n)
    for node in G.nodes:
        G.nodes[node]['color'] = 'black'
        G.nodes[node]['fault_ids'] = 0
    return G

def main():
    G = nx.hexagonal_lattice_graph(6, 4, periodic=True)
    colorize_graph_black(G)
    draw(G, "img/hexcolor/original.png")
    tor_hex48_color_encode(G,6,4)
    draw(G, "img/hexcolor/normal_colorizer.png")

if __name__ == "__main__":
    main()