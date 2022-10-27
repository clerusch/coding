import numpy as np
import matplotlib.pyplot as plt

def gen_ring_pcm(distance):
    pcm = np.eye(distance, dtype=int)
    for i in range(distance):
        pcm[i,i-distance+1] = 1   
    return pcm

def ring_decoder(noisy_message, syndrome):
    d = len(noisy_message)
    pcm = gen_ring_pcm(d)
    candidate = np.array(np.linalg.solve(pcm, syndrome), dtype=int)
    if sum(candidate)>len(candidate)/2:                             # if most entries are 1, its not the shorter path
        shorter = np.array([x+1 for x in candidate], dtype=int) %2
        candidate = shorter
    corrected_message = (noisy_message + candidate)%2
    return corrected_message

def calc_ler(n_runs, distance, per):
    pcm = gen_ring_pcm(distance)
    n_logical_errors = 0
    for _ in range(n_runs):
        error = (np.random.rand(distance) < per).astype(np.uint8)
        syndrome = (pcm@error) % 2
        result = ring_decoder(error,syndrome)
        if sum(result)>0:
            n_logical_errors+=1
    return n_logical_errors/n_runs

def ring_tester(distance):
    pers = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    outputlist = []
    for per in pers:
        noise = np.zeros(distance, dtype=int)
        for i in range(distance): 
            if np.random.rand() < per: noise[i] = 1
        wert = np.random.randint(0,2)
        message = np.array([wert for _ in range(distance)], dtype=int)
        pcm = gen_ring_pcm(distance)
        syndrome = pcm@noise % 2
        noisy_message = np.array([(message[i]+noise[i]) % 2 for i in range(distance)])
        answer = ring_decoder(noisy_message, syndrome)
        outputlist.append((answer==message).all())

    print(outputlist)

for d in [3,5,51]:
    ler = []
    per = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    for p in per:
        ler_new = calc_ler(1000,d,p)
        ler.append(ler_new)
    plt.plot(per, ler,label=d)
    plt.legend()
plt.show()
# If I understand the plots correctly, this manner of 
# correction does not work for arbitrary distance on 
# the ringcode