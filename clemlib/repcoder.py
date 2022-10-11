import numpy as np 
import matplotlib.pyplot as plt 
import sys 

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

def main(number):
    """Performs tests with all numbers up to the given number

    Args:
        number (chr): number to test

    Returns:
        Bool: Wether out tests were successful
    """
    # this is kind of useless
    for _ in range(50):
        print(majvote("000111000")) 
     
if __name__ == '__main__':
    main(sys.argv[1])