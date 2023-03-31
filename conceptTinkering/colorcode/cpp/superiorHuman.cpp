#include <boost/graph/grid_graph.hpp>
#include <boost/graph/graph_traits.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/graphviz.hpp>
#include <fstream>


int main(){

    using namespace boost;
    typedef adjacency_list<vecS, vecS, undirectedS> Graph;
    typedef grid_graph<2> Grid;
    typedef graph_traits<Graph>::vertex_descriptor vertex_descriptor;
    typedef Graph::vertices_size_type vertices_size_type;

    Graph graph_generator(int m, int n){
        const vertices_size_type length_x = m;
        const vertices_size_type length_y = n;

        std::array<vertices_size_type, 2> lengths = { length_x, length_y };
        Grid grid({m,n});

        Graph G(length_x * length_y);
        
        return G;
    }
    Graph G = graph_generator(12,4);
    std::ofstream dot_file("graph.dot");
    write_graphviz(dot_file, G);
    dot_file.close();

    std::system("dot -Tpng graph.dot -o graph.png");
    std::system("xdg-open graph.png");

}