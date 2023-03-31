#include "honey_graph_gen.hpp"
#include <iostream>
#include <fstream>
using namespace std;

int main(){
    Graph g = graphGen(12,4);
    std::ofstream dot_file("graph.dot");
    write_graphviz(dot_file, g);
    dot_file.close();
    std::system("dot -Tpng graph.dot -o graph.png");
    std::system("xdg-open graph.png");
}