import sys
from mpl_toolkits import mplot3d
from clemlib.repcoder import *

def fidelity(noises:list[float], codelengths:list[int]):
    fidelities = []
    for noise in noises:
        for codelength in codelengths:
            pass

def test(number:int,codelength:int,noise:float):
    """Generates a List of successes and failures in sending a message

    Args:
        number (int): amount of discrete probabilities to check
    Returns: 
        howgood([Bool]): when it was successful
    """
    howgood=[]
    for i in range(number):
        word = wordgenerator(10) 
        coded  = encoder(word,codelength) 
        answer = decoder(noisify(coded,noise),codelength)   
        if not answer == word: howgood += [False] 
        else: howgood += [True] 
    return howgood 

def transprob(howgood:list[bool],step:int=1000):
    """
    Generates a list of probabilities from a sucess/failure list

    Args:
        howgood (list[bool): list of successes/failures
        c (int): Steps of probability averaging
    
    Returns:
        [float]: list of probabilities for success
    """
    probabilities = [] 
    for i in range(0,len(howgood),step):   
        curr = howgood[i:i+step] 
        trues = curr.count(True)+1 
        falses = curr.count(False)+1 
        probabilities += [(trues/falses)/step] 
    return sum(probabilities)/len(probabilities)

def plotter(howgood):
    """
    Plots the probabilities of successful transmission
    """
    """x = np.outer(np.linspace(-2, 2, 10), np.ones(10))
    y = x.copy().T
    z = fidelity(x,y)
    fig = plt.figure() 

    syntax for 3-D plotting
    ax = plt.axes(projection ='3d')
    
    # syntax for plotting
    ax.plot_surface(x, y, z, cmap ='viridis', edgecolor ='green')
    ax.set_title('Surface plot geeks for geeks')
    """
    plt.plot([i for i in range(int(len(howgood)/1000))],transprob(howgood)) 
    plt.show() 
def main():
    plotter(test(5000,3,0.5)) 
    pass 

if __name__ == '__main__':
    main()
