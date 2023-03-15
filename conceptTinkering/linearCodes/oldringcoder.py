import numpy as np
## lets decode a logical 0 or 1

m = np.array([[1,1,0,0,0],
              [0,1,1,0,0],
              [0,0,1,1,0],
              [0,0,0,1,1]])
actual = np.array([0,1,0,0,0])
#print(m@actual)

def encoder(bit):
    return np.array([[bit] for _ in range(5)])

def noisify(message, noisiness=0.3):
    syndrome = np.array([[0],[0],[0],[0],[0]])
    for count, bit in enumerate(message):
        if np.random.rand() < noisiness:
            bit = (bit+1)%2
            syndrome[count-1][0] += 1
            if count < len(syndrome):
                syndrome[count+1][0] += 1
            else: 
                syndrome[0][0] += 1
    for a in syndrome:
            a[0] = a[0] % 2
    
    return message, syndrome

def decoder(message,syndrome):
    pcm = np.array([[1,1,0,0,0],[0,1,1,0,0],[0,0,1,1,0],[0,0,0,1,1],[1,0,0,0,1]])
    guessed_error = pcm.__invert__ @ syndrome
    answer = message + guessed_error
    for a in answer:
        a = a%2
    return answer
test, syndrome = noisify(encoder(0)) 
print(test, syndrome)
#print(decoder(test, syndrome))