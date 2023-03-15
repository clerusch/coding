import networkx as nx
list_of_lists = [[1, 2, 3], [3, 4, 5], [6, 7, 8], [9, 10], [10, 11]]
unique_items = set([item for sublist in list_of_lists for item in sublist])
result = []
for l in list_of_lists:
    if all(item not in unique_items - set(l) for item in l):
        result.append(l)
        unique_items = unique_items.union(set(l))
    elif all(item not in set(l) for l in result):
        result.append(l)
        unique_items = unique_items.union(set(l))
print(result)