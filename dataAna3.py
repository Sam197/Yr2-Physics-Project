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

data = get_data()
print(data)
outdata = []
for datum in data:
    datum = str(datum)
    try:
        outdata.append(int(str(datum)[-5:]))
    except ValueError:
        continue

print(outdata)
ostr = ""
for d in outdata:
    random.seed(d)
    ostr += str(round(random.random()))

print(ostr)
