#include <boost/graph/grid_graph.hpp>
#include <boost/graph/random.hpp>
#include <random>
#include <boost/graph/graph_traits.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/graphviz.hpp>
#include <boost/graph/breadth_first_search.hpp>
#include <boost/property_map/property_map.hpp>

using namespace boost;
using namespace std;
typedef adjacency_list<vecS, vecS, undirectedS> Graph;

bool is5OrLessNeighbor(Graph& g, Graph::vertex_descriptor u, Graph::vertex_descriptor v)
{
    std::vector<int> distance(num_vertices(g)); // distance to each node from u

    breadth_first_search(g, u, visitor(make_bfs_visitor(record_distances(&distance[0], on_tree_edge()))));
    if (distance[v] == 0) return false;
    return distance[v] <= 5; // return true if v is reachable from u in 5 edges or less
}

Graph graphGen (int m, int n){
    int num_nodes = m * n;
    Graph g(num_nodes);
    // let us employ a trick to ensure connectedness:
    // // we will add edges between the first and last nodes of each row
    // // and between the first and last nodes of each column
    // // this will ensure that the graph is connected
    // // and that the graph is a torus
    // for (int i = 0; i < m; i++) {
    //     add_edge(i, i + (m * (n - 1)), g);
    // }
    // for (int i = 0; i < n; i++) {
    //     add_edge(i * m, (i + 1) * m - 1, g);
    // }
    for (int i = 0; i < num_nodes; i++){
        add_edge(i, (i+1)%num_nodes, g);
    }
    // For each vertex in the lattice
    for (int i = 0; i < num_nodes; i++) {
        // For each other vertex in the lattice
        if (out_degree(vertex(i,g),g) <= 2){
            // If the i vertex isn't full yet
            for (int j = 0; j < num_nodes; j++) {
                // Don't check the same vertex
                if (i == j) continue;
                // If the j vertex isn't full yet and isn't a closer than 6th neighbor
                if (out_degree(vertex(j,g),g) <= 2 & out_degree(vertex(i,g),g) <= 2) {
                    // cout << "The boolean is: " << !is6Neighbor(g, i, j) << endl;
                    if (!is5OrLessNeighbor(g, vertex(i, g), vertex(j,g))) {
                        cout << "Adding edge between " << i << " and " << j << endl;
                        add_edge(i,j,g);
                    }
                }

            }
        }
    }
    return g;
}
