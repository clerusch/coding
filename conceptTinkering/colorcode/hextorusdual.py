import networkx as nx
import matplotlib.pyplot as plt
from pymatching import Matching
from hextorus import tor_hex48_color_encode, draw_graph_with_colored_edges
from threecolorize import make_a_base_graph
import numpy as np
import random
from typing import List, FrozenSet
import time

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

def draw_graph_with_colored_edges_and_nodes(G, file=None, name=None):
    """
    Draws a graph who's nodes and edges have colors
    """
    pos = nx.get_node_attributes(G, 'pos')
    node_colors = [data['color'] for _, data in G.nodes(data=True)] 
    edge_colors = [G[u][v]['color'] for u, v in G.edges()]

    plt.figure()
    if name:
        plt.title(name)
    if pos: 
        nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors)
    elif not pos:
        nx.draw(G, with_labels=True, node_color=node_colors, edge_color=edge_colors)
    if nx.get_edge_attributes(G,"fault_ids"):
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "fault_ids"))
    if file:
        plt.savefig(file)
    else:
        plt.show()

def subtile(Graph, color):
    """
    Graph: nx Graph
    Color: color in format "r","g", "b"
    Returns: tiled graph (does not edit original)
    """
    G = Graph.copy()
    for edge in G.edges:
        u, v = edge[0], edge[1]
        if G.edges[u,v]['color'] != color:
            G.remove_edge(u,v)
    G.remove_nodes_from(list(nx.isolates(G)))
    return G

def relabel_graph(graph):
    for i, node in enumerate(graph.nodes):
        graph = nx.relabel_nodes(graph,{node: i})
    return graph

def decode_subgraph(graph, syndrome, num_first_color_errors=4, num_second_color_errors=2):
    # node_colors = nx.get_node_attributes(graph, 'color')
    # first_color = node_colors[0]
    # first_colored_nodes = set()
    # second_colored_nodes = set()
    
    # for node in graph.nodes:
    #     if node_colors[node] == first_color:
    #         first_colored_nodes.add(node)
    #     else:
    #         second_colored_nodes.add(node)

    # syndrome = np.zeros(len(node_colors), dtype=np.uint8)
    # print(syndrome)
    # first_colored_error_nodes = random.sample(first_colored_nodes, num_first_color_errors)
    # second_colored_error_nodes = random.sample(second_colored_nodes, num_second_color_errors)
    # all_error_nodes = first_colored_error_nodes + second_colored_error_nodes
    # for node in all_error_nodes:
    #     syndrome[node] = 1
    # graph[8][12]["fault_ids"] = 1
    # graph[4][8]["fault_ids"] = 1
    draw_graph_with_colored_edges_and_nodes(graph, "img/hexcolor/rename.png")
    for u, v, data in graph.edges(data=True):
        print(f"Edge ({u}, {v}) has fault id {data['fault_ids']}")
    
    matching = Matching(graph)
    prediction = matching.decode_to_edges_array(syndrome)
    
    plt.figure()
    Matching.draw(matching)
    plt.savefig("img/hexcolor/matching.png")
    print("The predicted edges are: \n",prediction)

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

def find_6_loops(graph: nx.Graph) -> List[FrozenSet[any]]:
    cycles = set()
    for node in graph.nodes:
        for node1 in graph.neighbors(node):
            for node2 in graph.neighbors(node1):
                for node3 in graph.neighbors(node2):
                    for node4 in graph.neighbors(node3):
                        for node5 in graph.neighbors(node4):
                            for node6 in graph.neighbors(node5):
                                if node6 == node:
                                    cycles.add(frozenset([node, node1, node2, node3, node4, node5]))
    faces = [cycle for cycle in cycles if len(cycle) == 6]
    return faces

def find_face_color(graph: nx.Graph, face: FrozenSet) -> str:
    rgb = set(['r','g','b'])
    boundary_colors = set()
    for node in face:
        for node2 in face:
            if node2 in graph.neighbors(node):
                boundary_colors.add(graph[node][node2]['color'])
    face_color = rgb - boundary_colors
    face_color = face_color.pop()
    return face_color
        

def dual_of_three_colored_graph(graph: nx.Graph) -> nx.Graph:
    """
    takes: nx graph with colored edges (does not edit it)
    returns: dual of that graph with colored edges and nodes
    """
    dual_graph = nx.Graph()
    fakeone = relabel_graph(triang_three_colored_graph(4,6))
    pos = nx.get_node_attributes(fakeone, 'pos')
    faces = find_6_loops(graph)
    # init nodes
    for i, face in enumerate(faces):
        dual_graph.add_node(i, color = 'black')
        color_of_face = find_face_color(graph, face)
        dual_graph.nodes[i]['color'] = color_of_face
        #### just to check things and visualize them
        # for node in face:
        #     graph.nodes[node]['color'] = color_of_face
        # draw_graph_with_colored_edges_and_nodes(graph, "img/hexcolor/testloops.png")
        # for node in face:
        #     graph.nodes[node]['color'] = 'black'
    # connect nodes
    for i, face in enumerate(faces):
        otherfaces = faces[:i]+faces[((i+1)%(len(faces)+1)):]
        for j, face2 in enumerate(otherfaces):
            lap_nodes = set(face & face2)
            # print(f"comparing face:\n {face} \n and face2: \n {face2}.\n The overlap is:\n{lap_nodes}")
            if lap_nodes:
                # A three-colorable graph will only ever have two nodes between two faces
                node1 = lap_nodes.pop()
                node2 = lap_nodes.pop()
                connecting_color = graph[node1][node2]['color']
                # we are iterating not over the list of faces, but over the list of otherfaces
                # what is j?
                second_face_pos = [k for k in range(len(faces)) if faces[k] == otherfaces[j]].pop()
                #
                dual_graph.add_edge(i,second_face_pos, color = connecting_color)
                
    
    return dual_graph

def main():
    origG = make_a_base_graph()
    draw_graph_with_colored_edges_and_nodes(triang_three_colored_graph(4,6), "img/hexcolor/triangshould.png")
    dual = dual_of_three_colored_graph(origG)
    ########## visualizing part
    draw_graph_with_colored_edges_and_nodes(dual, "img/hexcolor/dual.png")
 
if __name__ == "__main__":
    main()