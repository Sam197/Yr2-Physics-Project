'''
Measure the time between key board events to 17 dp (may depend on
machine being used)
'''
import keyboard
import tkinter as tk
import pickle
from tkinter import messagebox, filedialog

print("Start")


#Record all events until esc key pressed
events = keyboard.record('esc')
print(events)
intervals = []
for i, event in enumerate(events):
    if i == len(events)-1:
        break
    interval = events[i+1].time - events[i].time
    intervals.append(interval)
    # random.seed(interval)
    # print(random.random())

print(intervals)
    
root = tk.Tk()
#root.withdraw()
root.filename = filedialog.asksaveasfile(mode = "w", defaultextension = ".pickle")
try:
    with open(root.filename.name, 'wb') as out:
        pickle.dump(intervals, out)
    messagebox.showinfo('Save', 'Saved Sucessfully')
except:
    messagebox.showinfo("Did Not Save", "Unspecified Error") 
root.destroy()

