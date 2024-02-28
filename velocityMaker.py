import tkinter as tk
from tkinter import filedialog, messagebox
from math import sqrt
import matplotlib.pyplot as plt
import pickle

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

def save_Data(data):
    root = tk.Tk()
    root.withdraw()
    root.filename = filedialog.asksaveasfile(mode = "w", defaultextension = ".pickle")
    try:
        with open(root.filename.name, 'wb') as out:
            pickle.dump(data, out)
        messagebox.showinfo('Save', 'Saved Sucessfully')
    except:
        messagebox.showinfo("Did Not Save", "Unspecified Error") 
    root.destroy()

data = get_data()
# vels = []

# for i, datum in enumerate(data):
#     if i == 0:
#         continue
#     xdisp = sqrt((datum[0]-data[i-1][0])**2)
#     ydisp = sqrt((datum[1]-data[i-1][1])**2)
#     vels.append(xdisp+datum[0]/0.01)
#     vels.append(ydisp+datum[1]/0.01)

#save_Data(vels)

xvels = []
yvels = []

for i, datum in enumerate(data):
    if i == 0:
        continue
    # xdisp = sqrt((datum[0]-data[i-1][0])**2)
    # ydisp = sqrt((datum[1]-data[i-1][1])**2)
    # xvels.append(xdisp+datum[0]/0.01)
    # yvels.append(ydisp+datum[1]/0.01) 
    xdisp = (datum[0]-data[i-1][0])
    ydisp = (datum[1]-data[i-1][1])
    xvels.append(xdisp/0.01)
    yvels.append(ydisp/0.01)   

#save_Data(xvels+yvels)

fig, axs = plt.subplots(1, 2)
fig.suptitle('Histograms of X and Y Velocites in Arbitrary Velocity Units')
fig.supylabel('Density')
axs[0].hist(xvels, color = 'salmon', edgecolor = 'black', bins = 1000)
#axs[0].xlim = (-2, 2)
axs[0].set_xlabel('X Velocity (A.U)')
axs[1].hist(yvels, color = 'slategray', edgecolor = 'black', bins = 1000)
axs[1].set_xlabel('Y Velocity (A.U)')
plt.show()
