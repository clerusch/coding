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
            f"\nNoise:{self.noise}"+"\n"+self.stage)
        self.syndrome = np.array([])
        self.noise = np.array([])
        self.stage = "Oh no, how will I survive a physical error?"

    def encode(self, codelength=5):
        self.content = np.array(
            [self.content[0] for _ in range(codelength)])
        self.syndrome = np.array([0 for _ in range(codelength)])
        self.noise = np.array([0 for _ in range(codelength)])
        self.stage = "I am encoded"

    def noisify(self, noisiness=0.2):
        for i in range(len(self.content)):
            if np.random.random() < noisiness:
                self.content[i] = (self.content[i] + 1) % 2
                self.noise[i] = (self.content[i] + 1) % 2
                self.syndrome[i] = (self.syndrome[i] + 1) % 2
                self.syndrome[i-1] = (self.syndrome[i-1] + 1) % 2
        self.stage = "I have been subjected to noise :("

    def decode(self, codelength=5):
        pcm = np.array([[0 for _ in range(codelength)] for _ in range(codelength)])
        for i in range(codelength):
            pcm[i,i] = 1; pcm[i,i-codelength+1] = 1        
        # Ring pcm matrices are square and have full rank, so they're invertible
        noise = np.array([abs(thing) for thing in (inv(pcm)@self.syndrome.T).T], dtype=int)
        print(noise)
        self.content = (self.content + noise) % 2
        self.stage = "Hopefully my corrections were right UwU"

noise = np.array([0,1,1,0,0])
noise2 = np.array([1,0,0,1,1])

pcb = np.array([[1, 1, 0, 0, 0],
                [0, 1, 1, 0, 0],
                [0, 0, 1, 1, 0],
                [0, 0, 0, 1, 1],
                [1, 0, 0, 0, 1]])
print(np.linalg.det(pcb))
# syndrome = pcb@noise
print(pcb@noise)
print((pcb@noise2))
# print(f"This is the Determinant: {np.linalg.det(pcb)}\nThis is not 0 :(")

def testfunction():
    word = ringMessage()
    word.encode()
    word.show()
    word.noisify()
    word.show()
    word.decode()
    word.show()
# testfunction()
def doer(distance):
    amount = 100000
    smoothness = 800
    lErrorCount = []
    pErrorCount = []
    words = [ringMessage(number=i) for i in range(amount)]
    for i in range(amount):
        noisiprob = i/(amount)
        pErrorCount.append(noisiprob)
        words[i].encode(distance)
        real = words[i].content
        words[i].noisify(noisiprob)
        words[i].decode(distance)
        if np.array_equal(real,words[i].content):
            lErrorCount.append(0)
        else: lErrorCount.append(1)
    logical_error_rate = [(sum(lErrorCount[i:i+smoothness])/smoothness) \
        for i in range(0,amount-smoothness,smoothness)] 
    physical_error_rate = [(sum(pErrorCount[i:i+smoothness])/smoothness) \
        for i in range(0,amount-smoothness,smoothness)]
    return physical_error_rate, logical_error_rate

vec1 = np.array([1,0,0,0,1])
vec2 = np.array([1,1,0,0,0])
vec3 = np.array([0,1,1,0,0])
vec4 = np.array([0,0,1,1,0])
vec5 = np.array([0,0,0,1,1])

#print(vec4.T+vec1.T-vec3.T-vec2.T)


"""
a,b = doer(3)
plt.plot(a,b, label="Distance 3")
c,d = doer(5)
plt.plot(c,d, label="Distance 5")
e,f = doer(11)
plt.plot(e,f, label="Distance 11")

plt.legend(loc="upper left")
plt.show()
"""