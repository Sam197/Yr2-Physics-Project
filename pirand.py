import tkinter as tk
from tkinter import messagebox, filedialog
import random
from math import log, e
import pickle
import matplotlib.pyplot as plt
import numpy as np

# a = np.array([int(i) for i in pi])
# print(len(a))
# print(a)

# plt.hist(a)
# plt.show()

class Pirandom:

    def __init__(self):
        with open('pi.txt', 'r') as inFile:
            self.pi = inFile.read()
            self.index = 0
    
    def pirandom(self, seed) -> float:
        '''
        Generate a random number 0-9 inclusive
        '''
        #Obfuscate the index of pi to be chosen
        self.index += ((100*log(seed, e)%1)*(100*log(self.index+1, e)%1)*43)
        self.index += seed
        while self.index > 100000:  #Keep index in bounds of digits of pi
            self.index -= 100000
        return int(self.pi[round(self.index)])

def get_data():

    root = tk.Tk()
    root.withdraw()
    root.filename = filedialog.askopenfile(mode='r')
    try:
        with open(root.filename.name, 'rb') as ins:
            data = pickle.load(ins)
        messagebox.showinfo('Loaded', 'Loaded Sucessfully')
    except:
        messagebox.showinfo("Did Not Load", "Unspecified Error") 
    root.destroy()
    return data

data = get_data()
#x, y = zip(*data)
daa = data
b = []
f = Pirandom()

# for i in daa:
#     random.seed(i)
#     b.append(random.random())
a = np.array([f.pirandom(i) for i in daa])
# for i in a:
#     random.seed(int(i))
#     b.append(random.random())

plt.hist(a, bins=10, color='orange', edgecolor='black')
plt.title('Histogram of Pirand output seeded by double pendulum positions')
plt.xlabel('Pirand Output')
plt.ylabel('Density')
#plt.hist(b, bins = 10, edgecolor='yellow')
plt.show()

outstr = ''
for i in a:
    outstr += str(int(i)%2)
print(outstr)