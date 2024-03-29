import tkinter as tk
from tkinter import messagebox, filedialog
import pickle
import matplotlib.pyplot as plt
import numpy as np

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

numofpaths = 3
paths = []
colours = ['red', 'blue', 'orange', 'green']

for _ in range(numofpaths):
    paths.append(get_data())

for i in range(numofpaths):
    x, y = zip(*paths[i])
    x = np.array(x)
    y = -np.array(y)
    plt.plot(x, y, color=colours[i], label = f"{i+1}")

plt.legend()
plt.show()
