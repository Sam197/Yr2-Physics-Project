import tkinter as tk
from tkinter import messagebox, filedialog
import random
import pickle
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

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

def save_as_string(data):
    root = tk.Tk()
    root.withdraw()
    root.filename = filedialog.asksaveasfile(mode = "w", defaultextension = ".txt")
    try:
        with open(root.filename.name, 'w') as outFile:
            outFile.write(data)
        messagebox.showinfo('Save', 'Saved Sucessfully')
    except:
        messagebox.showinfo("Did Not Save", "Unspecified Error") 
    root.destroy()

def bin_save(data):
    from bitstring import BitArray
    bin_file = open('file.bin', 'wb')
    b = BitArray(bin=data)
    b.tofile(bin_file)
    bin_file.close()

out = []
d = get_data()
# for datum in d:
#     seed = datum[0]
#     random.seed(seed)
#     out.append(random.random())
#     seed = datum[1]
#     random.seed(seed)
#     out.append(random.random())

# fig, ax = plt.subplots(1, 2, figsize=(10, 4))
# x, y = zip(*d)
# xpos = defaultdict(int)
# ypos = defaultdict(int)
# for p in x: xpos[p] += 1
# for p in y: ypos[p] += 1
# print({k: v for k, v in sorted(xpos.items(), key=lambda item: item[1])})
# print({k: v for k, v in sorted(ypos.items(), key=lambda item: item[1])})
# print(xpos[-1], ypos[-1])


# ax[0].hist(x, edgecolor='black')
# ax[1].hist(y, edgecolor='black', color='yellow')
plt.hist(d, bins=100, edgecolor='Black', color='Pink')
plt.show()

#print(out)
# print(len(out))
# dictt = defaultdict(int)
# for datum in out:
#     datum = int(datum)
#     dictt[datum] += 1
# print(foo := dict(sorted(dict(dictt).items())))
# foobar = {k: v for k, v in sorted(foo.items(), key=lambda item: item[1])}
# print(foobar)


# plt.bar(foo.keys(), foo.values(), 2, color='orange')
# plt.show()
#save_as_string(out)
#bin_save(out)


