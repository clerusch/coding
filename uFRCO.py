import numpy as np

class Node:
    def __init__(self,index):
        self.p = None
        self.n = None
        self.edges = []
        self.i = index
    def __eq__(self, other):
        return self.i == other.i
    def __hash__(self):
        return self.i

class Graph:
    def __init__(self, nodes=[]):
        self.nodes = nodes

    def add_node(self, val):
        new_node = Node(val)
        self.nodes.append(new_node)

    def add_edge(self, node1, node2):
        node1.edges.append(node2)
        node2.edges.append(node1)

class Cluster:
    def __init__(self, nodes=[]):
        self.nodes = nodes
        self.start_nodes = [nodes[0]]
    def grow(self):
        new = []
        new += self.nodes
        for node in self.nodes:
            for edge in node.edges:
                if not edge in new:
                    new.append(edge)
        self.nodes = new

def genClustersOnGraph(syndrome):
    number = len(syndrome)
    locations = []
    for i, val in enumerate(syndrome):
        if val == 1:
            locations.append(i)          # here is only 1D, pls FIX
    graph = Graph()
    
    for i in range(number):
        graph.add_node(i)
    for i in range(number):
        graph.add_edge(graph.nodes[i], graph.nodes[i-1])
        # graph.add_edge(graph.nodes[i], graph.nodes[i-int(np.sqrt(number))]) # for size 10 2d
    clusters = []
    for i,location in enumerate(locations):
        clusters.append(Cluster([graph.nodes[location]]))
    return clusters

def growClusters(clusters):
    pass


def tester():
    syndrome = np.zeros(51)
    syndrome[1], syndrome[3] = 1, 1
    syndrome[23], syndrome[25] = 1, 1
    clusters = genClustersOnGraph(syndrome)
    ### This here is the actual grow and merge part, maybe we'll make it a function
    for _ in range(2):
        for cluster in clusters: 
            cluster.grow()
        for j, cluster in enumerate(clusters):
            for i,buster in enumerate(clusters):
                if buster != cluster and any(check in cluster.nodes for check in buster.nodes):
                    cluster.nodes = list(set(cluster.nodes + buster.nodes))
                    cluster.start_nodes.append(buster.start_nodes)
                    clusters.pop(i)
            if len(cluster.start_nodes)%2==0:
                #cluster.solve # haha
                clusters.pop(j)

    # for i in range(1):  # this needs to be a while loop
    #     for cluster in clusters:
    #         cluster.grow()
    print(clusters)
    for cluster in clusters:
        print("this")
        for node in cluster.nodes:
            print(node.i)


    # cluster = Cluster([graph.nodes[1]])
    # for node in cluster.nodes: print(node.i)
    # print(cluster.nodes[0].edges)
    # cluster.grow()
    # for node in cluster.nodes: print(node.i)

tester()