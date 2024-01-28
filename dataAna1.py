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

data = get_data()
x, y = zip(*data)
print(len(x))
print(len(y))
x = np.array(x)
y = -np.array(y)
plt.plot(x,y)
plt.xlabel('X-position (pixels)')
plt.ylabel('Y-position (pixels)')
plt.title('Position of Double Pendulum')
plt.show()
