import numpy as np;
import matplotlib as plt;
import sys;
import random;

def wordgenerator(length=1000):
    """
    Generates a word consisting of 0s and 1s

    Args:
        length(Int): length of word to generate, defaults to 1000

    Returns: 
        generated(str): generated word 
    """
    generated = "";#.join([chr(np.random.randint(0,2)+48) for i in range(length)]);
    for i in range(length):
        generated += str(np.random.randint(0,2));
    return generated;
    
def encoder(Word:str):
    """
    Repetition based encoder
    
    Args: 
        Word(str): string we want to encode
    
    Returns: 
        encoded(str): encoded message
    """
    encoded = ""; # this is to prevent side effects
    for letter in Word:
        encoded += letter * 3;  # this is the repetition part of the repetition code
    return encoded;

def flip(bit:chr):
    """Performs a binary flip on a character

    Args:
        bit (chr): "0" or "1" to flip

    Returns:
        chr: flipped chr
    """
    if bit == "0": 
        return "1";    
    else: 
        return "0";

def noisify(message:str, probability:float=0.5):
    """Generates a noisy message

    Args:
        message (str): message that goes through noisy channel
        probability (float): probability of a flip operation on a message, value between 0 and 1

    Returns:
        str: noisified message
    """
    noised = "";
    for letter in message:
        if np.random.rand() < probability:
            noised += flip(letter);
        else:
            noised += letter;
    return noised;

def majvote(letter:str):
    """
    `Remember this makes our code only binary`\n
    Performs a binary majority vote

    Args:
        letter we are unsure about
    Returns: Binary majority as string
    """
    return letter.count("0")>letter.count("1")

def decoder(Word:str):
    """
    Repetition code decoder

    Args:
        Word(str): string we want to decode
    
    Returns: 
        answer(str): decoded message
    """
    answer = ""; # this is to prevent side effects
    for i in range(0,len(Word),3): 
        if majvote(Word[i]): # We could have done a cool trick in c here, since 0 is True and 1 ist False
            answer += "0";  # this makes our code only binary tho
        else:
            answer += "1";
    return answer;
    
def test(number:int):
    """Tests encoding/decoding for a random word of length number

    Args:
        number (int): amount of discrete probabilities to check
    Returns: Bool: Wether test was successful
    """
    for i in range(number):
        word = wordgenerator();
        coded  = encoder(word);
        answer = decoder(noisify(coded,probability=(i/1000)));  
        if not answer == word: return False;
        else: pass;
    return True;

def main(number):
    """Performs tests with all numbers up to the given number

    Args:
        number (chr): number to test

    Returns:
        Bool: Wether out tests were successful
    """
    # this is kind of useless
    for _ in range(50):
        print(majvote("000111000"));
     
if __name__ == '__main__':
    main(sys.argv[1])