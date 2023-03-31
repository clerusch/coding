# TODO
## Things we can still do today
- Write something about how boundaries of faces are edges and boundaries of edges are nodes and how syndromes are boundary maps or shit
## Things we need to ask about
- if a valid correction is just anything that sums the error to a sum of hyperfaces how do i find that? I can't just generate all possible sums of faces, that would scale terribly
- how do i even correctly scale the color hextorus
- how many logicals does it contain -> what does that mean for thresholding?
- 


<!-- # Plan for C++
## Make a HexTorus Graph
- Make a Hexagonal m by n toric honeycomb lattice (6x4)
- Add the right colors to edges 

## Make a dual Graph
- Initialize a "Face" Node for each 6-loop
- Find Face Color and assign it to that node
- Inherit Face Errors by iterating over Comprising og Nodes errors
- Connect dual nodes by seeing which have to overlapping comprising og nodes
## Subtile dual Graph
- Filter out edges of wrong colors
- Remove isolate nodes

# Plan for lifting
- iterate over node
- if there is an edge between node and one from othernodes:
    - create a new cycle instance
    - add nodes to cycle, follow othernode through otherothernodes
    - do while there are valid guys in other^n_nodes (assuming there are no open walks, which i think is valid)
    - AND operator all face sets that are in the cycle

## what the problem is
- ok so currently our cycles are totally fucked
- how do we even find this?
    - change clusterfinder to:
        - "when i get back to og node, this was a cluster"
        - essentially guess and trial and error and call it ML
        



## further planning
- thresholding -->