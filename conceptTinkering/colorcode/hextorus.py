import networkx as nx
import matplotlib.pyplot as plt

def draw_graph_with_colored_edges(G, filename=None):
    pos = nx.get_node_attributes(G, 'pos')
    edge_colors = [G[u][v]['color'] for u, v in G.edges()]
    nx.draw(G, pos, with_labels=True, edge_color=edge_colors)
    
    if filename:
        plt.savefig(filename)
    else:
        plt.show()

def tor_hex48_color_encode(G: nx.Graph,n=8,m=6):
    """
    G: nx Graph
    n,m: how many by how many hexagon, default to 8 and 6
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





def main():
    G = nx.hexagonal_lattice_graph(6, 8, periodic=True)
    tor_hex48_color_encode(G)
    draw_graph_with_colored_edges(G)

if __name__ == "__main__":
    main()