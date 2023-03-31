#include "honey_graph_gen.hpp"
#include <fstream>
#include <iostream>
using namespace std;
using namespace boost;

int main(){
    Graph g = graphGen(12,4);

    std::ofstream dot_file("graph.dot");
    write_graphviz(dot_file, g);
    dot_file.close();
    std::system("dot -Tpng graph.dot -o graph.png");
    std::system("xdg-open graph.png");
}