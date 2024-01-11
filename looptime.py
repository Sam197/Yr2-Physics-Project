import time
import multiprocessing
import random


def main(resultHolder, decimalPlaces):
    '''
    Find how many iterations of calling .random() to get the same number as started with. deciamalPlaces controls
    the number of DP wanted when rounding the random number generated.
    '''

    initalNum = round(random.random(), decimalPlaces)
    iteration = 0
    found = False
    while not found:
        iteration += 1
        num = round(random.random(), decimalPlaces)
        if num == initalNum:
            break

    #Place result to be read by main thread - thread does not destroy itself until result put into the holder
    resultHolder.put(iteration)

if __name__ == "__main__":

    #Can record the compute time, this is nessercery, but it is always fun to have more data
    start = time.time()

    #Multiprocessing is used to reduce compute time, the numOfThreads is set to 25, this is because my CPU has 24 threads
    #And I felt like rounding up to 25. If running this code, change this accordingly
    
    numOfThreads = 25
    resultHolder = multiprocessing.Queue()  #Object for the threads to put thier results in, the queue can only take one object at a time
    decimalPlaces = 5   #How precise to compare numbers to
    
    #Instaniate and start the processes
    processes = [multiprocessing.Process(target=main, args=(resultHolder, decimalPlaces)) for _ in range(numOfThreads)]
    for proc in processes: proc.start()

    results = []

    #.get() command waits until a value is placed in the holder, hence why no while loop is required
    for _ in range(numOfThreads):
        result = resultHolder.get()
        results.append(result)
    
    print(results)
    print(time.time()-start)
