import numpy as np

class Message:
    def __init__(self, bit=0):
        self.content = [bit]
        self.show = lambda: print(self.content)
    def encode(self, codelength=5):
        for _ in range(codelength):
            self.content += self.content[0]
    def noisify(self, noisiness=0.2):
        for char in self.content:
            if np.random.random() < noisiness:
                char = (char+1)%2

word = Message()
word.encode()
word.show()
word.noisify()
word.show()
word.decode()
word.show()