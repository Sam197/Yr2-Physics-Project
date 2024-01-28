import tkinter as tk
import pickle
from tkinter import messagebox, filedialog

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

def main():
    loaded = False
    data = []
    while not loaded:
        data += get_data()
        if messagebox.askquestion("Load more?", "Would you like to load more data?") == 'no':
            loaded = True
    save_Data(data)
    print(len(data))

if __name__ == '__main__':
    main()
