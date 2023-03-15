# plan for lifting
- iterate over node
- if there is an edge between node and one from othernodes:
    - create a new cycle instance
    - add nodes to cycle, follow othernode through otherothernodes
    - do while there are valid guys in other^n_nodes (assuming there are no open walks, which i think is valid)
    - AND operator all face sets that are in the cycle

### what the problem is
- ok so currently our cycles are totally fucked
- how do we even find this?
    - change clusterfinder to:
        - "when i get back to og node, this was a cluster"
        - essentially guess and trial and error and call it ML
        



## further planning
- thresholding