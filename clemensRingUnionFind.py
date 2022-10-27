import numpy as np
import pandas as pd

syndrome = [1,0,0,0,1]


class cluster:
    def __init__(self, base):
        # self.name = name
        self.flares = np.array([base],dtype=int)
        self.ancillas = np.array([base], dtype=int)
    def grow_cluster(self):
        self.ancillas = np.append(self.ancillas,self.ancillas[-1]+1) ## grow right
        self.ancillas = np.append(np.array([self.ancillas[0]-1]),self.ancillas) ## grow left

clusters = {}
# for index,element in enumerate(syndrome):
#     if element == 1:
#         varnames[index] = 1
# print(varnames)
for index, flare in enumerate(syndrome):
    if flare == 1:
        clusters[cluster(index)] = index
print(clusters)
# c1 = cluster("c1", 1)
# c2 = cluster("c2", 19)
# c3 = cluster("c3" , 19)
# print(c1,c2)
# thing = np.array([i for i in range(20)])
# # joined_cluster = cluster("joined", 0)
# n = len(thing)
# ## next we gotta
# def cluster_finder():
#     while not bool(set((c1.ancillas+n)%n)&set((c2.ancillas+n)%n)): # kind of large memory overhead here
#         c1.grow_cluster()
#         c2.grow_cluster()
#         print(c1.ancillas,c2.ancillas)
#     if c1.ancillas[-1]>=c2.ancillas[0]:
#         joined_cluster.ancillas = np.unique(np.concatenate(((c1.ancillas+n)%n,(c2.ancillas+n)%n)))
#         joined_cluster.flares = np.concatenate(((c1.flares+n)%n, (c2.flares+n)%n))
#     else:
#         joined_cluster.ancillas = np.unique(np.concatenate(((c2.ancillas+n)%n, (c1.ancillas+n)%n)))
#         joined_cluster.flares = np.concatenate(((c2.flares+n)%n, (c1.flares+n)%n))
#     return True

# cluster_finder()
# print(joined_cluster.ancillas, joined_cluster.flares)

# s = set()
# liste = []
# def test(e):
#     if e in s:
#         return False
#     else:
#         s.add(e)
#         return True
# list(filter(test, liste))
