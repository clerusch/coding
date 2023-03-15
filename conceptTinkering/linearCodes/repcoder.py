import numpy as np 
import matplotlib.pyplot as plt 
import sys 

def noisificate(message,per):
    for l in message:
        if np.random.rand() > per:
            l = (l+1)%2

def decoderator(message, syndrome):
    res = np.zeros(len(message))
    if sum(message>(len(message)/2)):
        [res[i] = 1 for i in range(len(res))]
    else: [res[i] = 0 for i in range(len(res))]


def wordgenerator(length=1000):
    """
    Generates a word consisting of 0s and 1s

    Args:
        length(Int): length of word to generate, defaults to 1000

    Returns: 
        generated(str): generated word 
    """
    generated = "" 
    for i in range(length):
        generated += str(np.random.randint(0,2)) 
    return generated 
    
def encoder(word:str,replength:int=3):
    """
    Repetition based encoder
    
    Args: 
        word(str): string we want to encode
    
    Returns: 
        encoded(str): encoded message
    """
    encoded = ""  # this is to prevent those nasty side effects
    for letter in word:
        encoded += letter * replength   # this is the repetition part of the repetition code
    return encoded 

def flip(bit:chr):
    """Performs a binary flip on a character

    Args:
        bit (chr): "0" or "1" to flip

    Returns:
        chr: flipped chr
    """
    if bit == "0": 
        return "1"     
    else: 
        return "0" 

def noisify(message:str, probability:float=0.5):
    """Generates a noisy message

    Args:
        message (str): message that goes through noisy channel
        probability (float): probability of a flip operation on a message, value between 0 and 1

    Returns:
        str: noisified message
    """
    noised = "" 
    for letter in message:
        if np.random.rand() < probability:
            noised += flip(letter) 
        else:
            noised += letter 
    return noised 

def majvote(letter:str):
    """
    `Remember this makes our code only binary`\n
    Performs a binary majority vote

    Args:
        letter we are unsure about
    Returns: Binary majority as string
    """
    return letter.count("0")>letter.count("1")

def decoder(word:str,replength:int=3):
    """
    Repetition code decoder

    Args:
        word(str): string we want to decode
    
    Returns: 
        answer(str): decoded message
    """
    answer = ""  # this is to prevent side effects
    for i in range(0,len(word),replength): 
        if majvote(word[i]): # We could have done a cool trick in c here, since 0 is True and 1 is False
            answer += "0"   # this makes our code only binary tho
        else:
            answer += "1" 
    return answer 

def lercalc(n_runs, distance, per):
    message = encoder("0", distance)
    nle = 0
    print(per)
    for _ in range(n_runs):
        noised = noisify(message, probability=per)
        decoded = decoder(noised, distance)
        print(decoded, message)
        if decoded == message:
            pass
        else: nle += 1
    return nle/n_runs

def main():
    """Performs tests with all numbers up to the given number

    Args:
        number (chr): number to test

    Returns:
        Bool: Wether out tests were successful
    """
    
    # calc_ler(1000, 5, 0.3)
    for d in [3]:
        ler = []
        per = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
        for p in per:
            newler = lercalc(1000,d,p)
            ler.append(newler)
        plt.plot(per, ler,label=d)
    plt.legend()
    plt.show()
     
if __name__ == '__main__':
    if len(sys.argv)<=1:
        main()
    else: 
        main(sys.argv[1])