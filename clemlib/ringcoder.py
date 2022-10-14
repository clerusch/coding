import numpy as np
from numpy.linalg import inv
import matplotlib.pyplot as plt

class ringMessage:
    def __init__(self, bit=0, name=None, number=0):
        self.number = number
        self.name = name
        self.content = np.array([bit])
        self.show = lambda: print(
            f"Content:{self.content} \nSyndrome:{self.syndrome}"+
            "\n"+self.stage)
        self.syndrome = np.array([])
        self.stage = "Oh no, how will I survive a physical error?"

    def encode(self, codelength=5):
        self.content = np.array(
            [self.content[0] for _ in range(codelength)])
        self.syndrome = np.array([0 for _ in range(codelength)])
        self.stage = "I am encoded"

    def noisify(self, noisiness=0.25):
        for i in range(len(self.content)):
            if np.random.random() < noisiness:
                self.content[i] = (self.content[i] + 1) % 2
                self.syndrome[i] = (self.syndrome[i] + 1) % 2
                self.syndrome[i-1] = (self.syndrome[i-1] + 1) % 2
        self.stage = "I have been subjected to noise :("

    def decode(self, codelength=5):
        pcm = np.array([[0 for _ in range(codelength)] for _ in range(codelength)])
        for i in range(codelength):
            pcm[i,i] = 1; pcm[i,i-codelength+1] = 1
        #this here  is what pcm looks like for codelength 5
        pcb = np.array([[1, 1, 0, 0, 0],
                        [0, 1, 1, 0, 0],
                        [0, 0, 1, 1, 0],
                        [0, 0, 0, 1, 1],
                        [1, 0, 0, 0, 1]])
        # Ring pcm matrices are square and have full rank, so they're invertible
        noise = np.array((inv(pcm)@self.syndrome.T).T, dtype=int)
        self.content = (self.content + noise) % 2
        self.stage = "Hopefully my corrections were right UwU"
        
amount = 100000
smoothness = 1000
lErrorCount = []
pErrorCount = []
words = [ringMessage(number=i) for i in range(amount)]
for i in range(amount):
    noisiprob = i/(amount)
    pErrorCount.append(noisiprob)
    words[i].encode(5)
    real = words[i].content
    words[i].noisify(noisiprob)
    words[i].decode(5)
    if np.array_equal(real,words[i].content):
        lErrorCount.append(0)
    else: lErrorCount.append(1)

logical_error_rate = [(sum(lErrorCount[i:i+smoothness])/smoothness) \
    for i in range(0,amount-smoothness,smoothness)] 
physical_error_rate = [(sum(pErrorCount[i:i+smoothness])/smoothness) \
    for i in range(0,amount-smoothness,smoothness)]

plt.plot(physical_error_rate,logical_error_rate)
plt.savefig(f"Samplesize={amount}smoothness={smoothness}")
plt.show()