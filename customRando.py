'''
Implimenttion of the Cliff PRNG. Is an extract of a larger file I made a while ago, please don't judge my bad code
'''

from time import time
from math import log, e, log10
from os.path import exists

def getSeed() -> float: 
    '''
    Get current seed stored in memory, if no seed is stored or the file does not exist, seed defults to time.time()
    '''
    if exists("seed.txt"):
        with open("seed.txt", 'r') as infile:
            seed = infile.read()
        try:
            seed = float(seed)
        except:
            seed = time()
    else:
        seed = time()

    return seed

def setSeed(seed) -> None:
    '''
    Stores seed into memory, this will then be used in later random calculations
    '''
    seed = str(seed)[:12]
    with open("seed.txt", "w") as outfile:
        outfile.write(seed)

def random(seed = None, saveSeed = True) -> float:
    '''
    Returns a float between 0.0 and 1.0 using 'Cliff Random Number Generator'
    Will use set seed if one is set, and the number generated from this set seed will become the new base seed
    Save seed determines if a new seed will be saved after a random number is generated.
    '''
    if seed == None:
        seed = getSeed()
    rando = abs((100*log(seed, e))%1)
    if saveSeed:
        setSeed(rando)
    return rando

print(random(0.5))

def randomInt(lowerBound, upperBound) -> int:
    '''
    Returns a random int in the range of the specified bounds (Bounds Inclusive)
    low <= x <= high
    '''
    if lowerBound >= upperBound:
        raise Exception("Invalid Bounds, Lowerbound must be less than the upperbound")
    numFound = False
    while not numFound:
        tryNum = random()                                #Puts every in digit seprartly in a list missing out first decimal point on purpose
        digits = list(int(i) for i in str(tryNum)[3:])   #This is just to encourage zeros in answers as the likelyhood of getting
        outNum = ""                                      #0.0... is less than getting 0.X0... where X is a random digit 
        for i in range(len(str(upperBound))):
            outNum += str(digits[i])
        if lowerBound <= int(outNum) <= upperBound:
            numFound = True
            return int(outNum)

def randomNumbers(length, upperBound = 9) -> list:
    '''
    Returns a list of a specified length with digits between 0 and 9 (inclusive) or 0 <= x <= upperbound (if specified). 
    Note: This method is much quicker than using randomInts for digits between 0 and 9
    '''
    numsFound = False
    outList = []
    newList = []
    while not numsFound:
        del newList
        newList = list(int(i) for i in str(random())[3:])
        for item in newList:
            if len(outList) == length:
                numsFound = True
                break
            if item <= upperBound:
                outList.append(item)

    return outList        

def randomInts(lowerBound, upperBound, length) -> list:
    '''
    Returns a list of spesified length with ints between specified bounds.
    Note: If looking to get random units (0-9 inclusive) use randomNumbers as it is much quicker.
    '''
    outlist = []
    for i in range(length):
        outlist.append(randomInt(lowerBound, upperBound))
    return outlist

def randomFloats(length) -> list:
    '''
    Returns a list of specified length contaning random floats generated from random()
    Note: This method is quicker than calling random x times in a loop.
    :-)
    '''
    outList = []
    seed = random()
    outList.append(seed)
    for i in range(length-1):
        seed = random(seed, False)
        outList.append(seed)
    random(seed)      #Get new seed for random generator
    return outList
