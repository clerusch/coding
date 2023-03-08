import networkx as nx
import matplotlib.pyplot as plt
from pymatching import Matching
from hextorus import tor_hex48_color_encode, draw_graph_with_colored_edges
from threecolorize import make_a_base_graph
import numpy as np
import random
from typing import List, FrozenSet
import time

def colorize_graph_black(G):
    for u, v, attr in G.edges(data=True):
        G[u][v]['color'] = 'black'

def draw_graph_with_colored_edges_and_nodes(G: nx.Graph, file: str=None, name: str=None) -> bool:
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
    return True

def flag_color_graph(graph: nx.Graph, per=0.1) -> bool:
    """
    Changes input graph such that with probability p
    on each nodes errors happen
    """
    for node in graph.nodes:
        if random.random()< per:
            graph.nodes[node]['fault_ids'] = 1
            graph.nodes[node]['color'] = 'y'
    return True

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
    faces = find_6_loops(graph)
    # init nodes
    for i, face in enumerate(faces):
        dual_graph.add_node(i, color = 'black')
        color_of_face = find_face_color(graph, face)
        dual_graph.nodes[i]['color'] = color_of_face
        # This is the part for error -> syndrome inheritance to the dual graph
        dual_graph.nodes[i]['fault_ids'] = 0
        for node in face:
            if graph.nodes[node]['fault_ids'] == 1:
                dual_graph.nodes[i]['fault_ids'] = (dual_graph.nodes[i]['fault_ids']+1)%2
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

def subtile(Graph: nx.Graph, color: str) -> nx.Graph:
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

def decode_subtile(graph: nx.Graph) -> List[any]:
    """
    churns out an error edges prediction from syndrome fault_ids
    on a graph
    """
    # we'll leave og alone for now
    renamed_copy = graph.copy()
    print(renamed_copy.nodes)
    # make renamed_copy usable (hopefully)
    for i, node in enumerate(graph.nodes):
        renamed_copy.nodes[node]['og_name'] = node
        renamed_copy = nx.relabel_nodes(renamed_copy,{node: i})
    print(renamed_copy.nodes)
    matching = Matching(renamed_copy)
    # generate syndrome on renamed_copy
    syndrome = np.zeros(len(graph.nodes), dtype=np.uint8)
    for node in renamed_copy.nodes:
        if renamed_copy.nodes[node]['fault_ids'] == 1:
            syndrome[node] = 1
    print(syndrome)
    # predict edges on the renamed_copy
    prediction = matching.decode_to_edges_array(syndrome)
    # rename nodes to be actually usable
    print(prediction)
    for edge in prediction:
        for i in range(len(edge)):
            edge[i] = renamed_copy.nodes[edge[i]]['og_name']
    
    return prediction

def make_a_shower(graph: nx.Graph) -> nx.Graph:
    shower = graph.copy()
    for node in shower.nodes:
        if shower.nodes[node]['fault_ids'] == 1:
            shower.nodes[node]['color'] = 'y'
    return shower

def main():
    origG = make_a_base_graph()
    flag_color_graph(origG, 0.05)
    ### dualizing stuff and making error show-ers
    dual = dual_of_three_colored_graph(origG)
    dual_shower = make_a_shower(dual)
    subr = subtile(dual, 'r')
    subr_shower = make_a_shower(subr)
    subg = subtile(dual, 'g')
    subg_shower = make_a_shower(subg)
    subb = subtile(dual, 'b')
    subb_shower = make_a_shower(subb)
    ########## visualizing part
    draw_graph_with_colored_edges_and_nodes(origG, "img/hexcolor/original.png")
    draw_graph_with_colored_edges_and_nodes(dual_shower, "img/hexcolor/dual.png")
    for i, graph in enumerate([subr_shower, subg_shower, subb_shower]):      
        draw_graph_with_colored_edges_and_nodes(graph, f"img/hexcolor/{i}.png")
        print(decode_subtile(graph))

if __name__ == "__main__":
    main()