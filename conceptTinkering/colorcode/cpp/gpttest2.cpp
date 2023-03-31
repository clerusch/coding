#include <fstream>
#include <boost/graph/graphviz.hpp>
#include <iostream>
#include <boost/graph/adjacency_list.hpp>

using namespace std;

// define the graph type
typedef boost::adjacency_list<boost::setS, boost::vecS, boost::undirectedS, boost::property<boost::vertex_index_t, int, Vertex>> Graph;

// define the vertex type and property
struct Vertex {
    int id;
};

// define the edge type and property
struct Edge {
};

int main() {
    int n = 48;

    // initialize the graph
    Graph G(n);

    // set the id property for each vertex
    for (int i = 0; i < n; i++) {
        G[i].id = i;
    }

    std::cout << "Graph created with " << boost::num_vertices(G) << " nodes." << std::endl;

    std::ofstream dot_file("graph.dot");
    boost::write_graphviz(dot_file, G);
    dot_file.close();

    std::system("dot -Tpng graph.dot -o graph.png");
    std::system("xdg-open graph.png");

    return 0;
}
