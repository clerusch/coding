#include <boost/graph/grid_graph.hpp>
#include <boost/graph/graph_traits.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/graphviz.hpp>
#include <fstream>

int main() {
    using namespace boost;

    typedef adjacency_list<vecS, vecS, undirectedS> Graph;
    typedef grid_graph<2> Grid;
    typedef graph_traits<Graph>::vertex_descriptor vertex_descriptor;
    typedef Graph::vertices_size_type vertices_size_type;

    const vertices_size_type length_x = 6;
    const vertices_size_type length_y = 4;

    std::array<vertices_size_type, 2> lengths = { length_x, length_y };
    Grid grid({6,4});

    Graph G(length_x * length_y);
    for (vertices_size_type i = 0; i < length_x; ++i) {
        for (vertices_size_type j = 0; j < length_y; ++j) {
            vertex_descriptor u = vertex(j + i * length_y, G);
            if (i % 2 == 0) {  // shift for hexagonal lattice
                if (j > 0) add_edge(u, vertex((j-1) + i * length_y, G), G);
                if (j < length_y-1) add_edge(u, vertex((j+1) + i * length_y, G), G);
                if (i > 0) {
                    if (j > 0) add_edge(u, vertex((j-1) + (i-1) * length_y, G), G);
                    add_edge(u, vertex(j + (i-1) * length_y, G), G);
                }
                if (i < length_x-1) {
                    if (j > 0) add_edge(u, vertex((j-1) + (i+1) * length_y, G), G);
                    add_edge(u, vertex(j + (i+1) * length_y, G), G);
                }
            }
            else {  // shift for hexagonal lattice
                if (j < length_y-1) add_edge(u, vertex((j+1) + i * length_y, G), G);
                if (j > 0) add_edge(u, vertex((j-1) + i * length_y, G), G);
                if (i > 0) {
                    add_edge(u, vertex(j + (i-1) * length_y, G), G);
                    if (j < length_y-1) add_edge(u, vertex((j+1) + (i-1) * length_y, G), G);
                }
                if (i < length_x-1) {
                    add_edge(u, vertex(j + (i+1) * length_y, G), G);
                    if (j < length_y-1) add_edge(u, vertex((j+1) + (i+1) * length_y, G), G);
                }
            }
        }
    }
    std::ofstream dot_file("graph.dot");
    write_graphviz(dot_file, G);
    dot_file.close();

    std::system("dot -Tpng graph.dot -o graph.png");
    std::system("xdg-open graph.png");

    return 0;
}
