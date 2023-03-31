#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/breadth_first_search.hpp>
#include <iostream>

using namespace boost;

typedef adjacency_list<vecS, vecS, undirectedS> Graph;
typedef graph_traits<Graph>::vertex_descriptor Vertex;

bool can_reach_in_fewer_than_6_edges(Vertex a, Vertex b, const Graph& g)
{
    std::vector<int> distance(num_vertices(g)); // distance to each node from a

    breadth_first_search(g, a, visitor(make_bfs_visitor(record_distances(&distance[0], on_tree_edge()))));

    return distance[b] < 6; // return true if b is reachable from a in fewer than 6 edges
}

int main()
{
    Graph g(6); // create a small example graph

    add_edge(0, 1, g);
    add_edge(0, 2, g);
    add_edge(1, 2, g);
    add_edge(1, 3, g);
    add_edge(2, 4, g);
    add_edge(3, 4, g);
    add_edge(3, 5, g);
    add_edge(4, 5, g);

    Vertex a = 0;
    Vertex b = 5;

    bool can_reach = can_reach_in_fewer_than_6_edges(a, b, g);

    std::cout << "Node " << a << " can" << (can_reach ? "" : "not") << " reach node " << b << " in fewer than 6 edges" << std::endl;

    return 0;
}
