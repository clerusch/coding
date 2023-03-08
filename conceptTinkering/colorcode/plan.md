# plan for error generation and inheritance

- take random nodes on original graph and flag them +1)%2
- all faces that are bounded by that node get an error flag during face generation
- subgraphs then decode as normal
## for decoding
- rename subgraph nodes into [0..len(subgraph.nodes)]
- keep og names as property
## further planning
- thresholding