import random
import networkx as nx
import numpy as np
from hextorusdual import draw_graph_with_colored_edges_and_nodes
from pymatching import Matching
import matplotlib.pyplot as plt

def triang_three_colored_graph(m,n):
    """
    Makes an m by n node toric triangular graph with
    three-colored nodes and edges, being the dual
    to a hexagonal toric graph with three-colored
    edges and faces (chain complex boundary) and plots it
    """
    # constants and initialization
    n = 2*n
    rgb = ["r","g","b"]
    rgbset = set(rgb)
    G = nx.triangular_lattice_graph(m,n,periodic=True)

    # color in the nodes abusing triangularity
    for node in G.nodes:
        G.nodes[node]['color'] = rgb[(node[0]-node[1]%2)%3]
        G.nodes[node].update({'fault_ids': 0})
    # color each edge with color its composing nodes dont have
    for edge in G.edges:
        u, v = edge[0], edge[1]
        first_color, second_color = G.nodes[u]['color'], G.nodes[v]['color']
        used_colors = set([first_color, second_color])
        color = next(iter(rgbset - used_colors))
        G.remove_edge(u,v)
        G.add_edge(u,v, color=color, fault_ids=0)

    return G

def relabel_graph(graph):
    for i, node in enumerate(graph.nodes):
        graph = nx.relabel_nodes(graph,{node: i})
    return graph

def gen_error_for_subgraph(graph, per=0.2):
    for edge in graph.edges():
        u,v = edge[0], edge[1]
        if random.random() < per:
            graph[u][v]['fault_ids'] = 1
    return graph

def gen_syndrome_from_subgraph_error(graph, want_array=False):
    syndrome = np.zeros(len(graph.nodes()), dtype= np.uint8)
    print(nx.get_node_attributes(graph, 'fault_ids'))
    for edge in graph.edges:
        u, v = edge[0], edge[1]
        if not (graph[u][v]['fault_ids']) == 0:
            curr_u_fault = graph.nodes[u]['fault_ids']
            graph.nodes[u]['fault_ids'] = (curr_u_fault + 1) %2
            curr_v_fault = graph.nodes[v]['fault_ids']
            graph.nodes[v]['fault_ids'] = (curr_v_fault + 1) %2
            syndrome[u] = (syndrome[u] + 1) %2
            syndrome[v] = (syndrome[v] + 1) %2

    if want_array:
        return syndrome
    else:
        return graph

def decode_subgraph(graph, syndrome, num_first_color_errors=4, num_second_color_errors=2):
    """
    node_colors = nx.get_node_attributes(graph, 'color')
    first_color = node_colors[0]
    first_colored_nodes = set()
    second_colored_nodes = set()
    
    for node in graph.nodes:
        if node_colors[node] == first_color:
            first_colored_nodes.add(node)
        else:
            second_colored_nodes.add(node)

    syndrome = np.zeros(len(node_colors), dtype=np.uint8)
    print(syndrome)
    first_colored_error_nodes = random.sample(first_colored_nodes, num_first_color_errors)
    second_colored_error_nodes = random.sample(second_colored_nodes, num_second_color_errors)
    all_error_nodes = first_colored_error_nodes + second_colored_error_nodes
    for node in all_error_nodes:
        syndrome[node] = 1
    graph[8][12]["fault_ids"] = 1
    graph[4][8]["fault_ids"] = 1
    """
    draw_graph_with_colored_edges_and_nodes(graph, "img/hexcolor/rename.png")
    for u, v, data in graph.edges(data=True):
        print(f"Edge ({u}, {v}) has fault id {data['fault_ids']}")
    
    matching = Matching(graph)
    prediction = matching.decode_to_edges_array(syndrome)
    
    plt.figure()
    Matching.draw(matching)
    plt.savefig("img/hexcolor/matching.png")
    print("The predicted edges are: \n",prediction)