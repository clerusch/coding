import numpy as np

class ringMessage:
    def __init__(self, bit=0):
        self.content = np.array([bit])
        self.show = lambda: print(f"Content:{self.content}\nSyndrome:{self.syndrome}")
        self.syndrome = np.array([])
        self.corrected = np.array([0 for _ in range(5)])
    def encode(self, codelength=5):
        self.content = np.array([self.content[0] for _ in range(codelength)])
        self.syndrome = np.array([0 for _ in range(codelength)])
    def noisify(self, noisiness=0.25):
        for i in range(len(self.content)):
            if np.random.random() < noisiness:
                self.content[i] = (self.content[i] + 1) % 2
                self.syndrome[i] = (self.syndrome[i] + 1) % 2
                self.syndrome[i-1] = (self.syndrome[i-1] + 1) % 2
    def decode(self, codelength=5):
        pcm = np.array([[1,1,0,0,0],[0,1,1,0,0],[0,0,1,1,0],[0,0,0,1,1],[1,0,0,0,1]])
        print(pcm @ self.content.T, self.syndrome.T)
        # self.content = pcm.__invert__ @ self.syndrome.T 
        # for i in range(len(self.content)):
        #     self.content[i] = (self.content[i]+1)%2

word = ringMessage()
word.show()
word.encode()
word.show()
word.noisify()
word.show()
word.decode()
