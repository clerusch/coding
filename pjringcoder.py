import numpy as np
from pymatching import Matching
import matplotlib.pyplot as plt

def calc_ler(n_runs, distance,per):
    pcm=np.eye(distance)
    for i in range(distance):
        pcm[i][(i+1)%distance] = 1
    matching=Matching(pcm)
    matching.draw()
    n_logical_errors=0
    for _ in range(n_runs):
        error = (np.random.rand(distance) < per).astype(np.uint8)
        syndrome=(pcm@error)% 2
        correction = matching.decode(syndrome)
        result = (correction + error)%2
        if sum(result)>0:
            n_logical_errors+=1
    return(n_logical_errors/n_runs)

calc_ler(1000, 5, 0.3)
# for d in [3,5,9]:
#     ler = []
#     per = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
#     for p in per:
#         ler_new = calc_ler(1000,d,p)
#         ler.append(ler_new)
#     plt.plot(per, ler,label=d)
plt.legend()
plt.show()








