'''
Modification of pend track 3. This script allows the script to be used as a module aswell as a standalone program
'''
# pylint: disable=no-member
import tkinter as tk
from tkinter import messagebox, filedialog
import random
#from os import exists
import pickle
import cv2
import numpy as np

class Tkwindows:
    '''Object that stores the tkinter window'''

    def __init__(self, managerObj):

        self._manager = managerObj

        self._root = tk.Tk()
        self._root.title("HSV Picker")
        self._root.protocol('WM_DELETE_WINDOW', self.__closeWindow)   #When window is closed, tells the main loop in manager to stop

        self._hueS = tk.Scale(self._root, label = 'Hue Value', from_ = 0, to_ = 180, orient=tk.HORIZONTAL, length = 200, tickinterval = 45)
        self._hueS.pack()
        self._satS = tk.Scale(self._root, label = 'Saturation Value', from_ = 0, to_ = 255, orient = tk.HORIZONTAL, length = 200, tickinterval = 50)
        self._satS.pack()
        self._valS = tk.Scale(self._root, label = 'Value Value', from_ = 0, to_ = 255, orient=tk.HORIZONTAL, length = 200, tickinterval = 50)
        self._valS.pack()
        self._rangeS = tk.Scale(self._root, label = 'Detection Range', from_ = 0 , to = 255, orient = tk.HORIZONTAL, length = 200, tickinterval = 50)
        self._rangeS.pack()
        self._contorCutOff = tk.Scale(self._root, label = 'Min contour size', from_ = 0, to_ = 1000, orient = tk.HORIZONTAL, length = 200, tickinterval = 250)
        self._contorCutOff.pack()
        self._start = tk.Button(self._root, command = self._manager.toggleDataAqu, text="Start")
        self._start.pack()

    def __closeWindow(self):
        '''Make sure the program stops when window closes'''
        self._manager.stopMainloop()
        self._root.destroy()

    @property
    def buttonState(self):
        '''Return the current state of the start/stop button'''
        return self._start['text']
    
    def setButton(self, txt):
        '''Set the text on the button'''
        self._start.config(text=txt)

    @property
    def hsvrc_values(self):
        '''Return the Hue, Saturation, Value, Range and Contour Cuttoff values'''
        return self._hueS.get(), self._satS.get(), self._valS.get(), self._rangeS.get(), self._contorCutOff.get()

    def set_hsvrc_values(self, h, s, v, r, c):
        self._hueS.set(h)
        self._satS.set(s)
        self._valS.set(v)
        self._rangeS.set(r)
        self._contorCutOff.set(c)

    def tkUpdate(self):
        '''Tick the tkwindow'''
        self._root.title(f"Data points {2*len(self._manager._data)}")
        self._root.update()

class Manager:
    '''Object that controlls the program's behavoir'''

    def __init__(self, ui = False):
        self._UI = ui
        self._cam = cv2.VideoCapture(0)
        if self._UI:
            self._tkwindow = Tkwindows(self)
            #if exists('prevVales.txt'):
            with open('prevValues.txt', 'r') as inFile:
                values = tuple(inFile.read().split())
            self._tkwindow.set_hsvrc_values(*values)
        self._dataAqu = False
        self._data = []
        self._running = True
        self._frame = None
        self._mask = None

    def stopMainloop(self):
        '''Stop the program'''
        with open('prevValues.txt', 'w') as outFile:
            h ,s, v, r, c = self._tkwindow.hsvrc_values
            outFile.write(f"{h} {s} {v} {r} {c}")
        self._running = False

    def _saveData(self):
        '''Save collected data as a pickled file'''
        root = tk.Tk()
        root.withdraw()
        root.filename = filedialog.asksaveasfile(mode = "w", defaultextension = ".pickle")
        try:
            with open(root.filename.name, 'wb') as out:
                pickle.dump(self._data, out)
            messagebox.showinfo('Save', 'Saved Sucessfully')
        except:
            messagebox.showinfo("Did Not Save", "Unspecified Error") 
        root.destroy()

    def toggleDataAqu(self):
        '''Toggle the data aqu'''
        if self._tkwindow.buttonState == 'Start':
            self._tkwindow.setButton('Stop')
            self._dataAqu = True
        else:
            self._tkwindow.setButton('Start')
            self._dataAqu = False
            if messagebox.askquestion("Save data?", "Would you like to save the data?") == 'yes':
                self._saveData()
            if messagebox.askquestion('Keep Data', 'Would you like to keep the current data in memory?') != 'yes':
                self._data.clear()
                
    def _maintick(self, hue, sat, val, ran, contourCutOff):
        '''Handles the core functionality required for the pendulum tracking'''
        _, self._frame = self._cam.read()
        hsvImage = cv2.cvtColor(self._frame, cv2.COLOR_BGR2HSV) #Convert to hsv colour space
        self._mask = cv2.inRange(hsvImage, np.array([hue-ran, sat-ran, val-ran]), np.array([hue+ran, sat+ran, val+ran]))
        contours, _ = cv2.findContours(self._mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #Find the areas highlighted in mask
        if len(contours) != 0:
            for countour in contours:
                if cv2.contourArea(countour) > contourCutOff:
                    return cv2.boundingRect(countour)
        return None
    
    def _tick(self):
        '''Update the cv2 windows - for use when script ran as __main__'''
        hue, sat, val, ran, contourCutOff = self._tkwindow.hsvrc_values
        res = self._maintick(hue, sat, val, ran, contourCutOff)
        if res != None:
            x, y, w, h = res
            cv2.rectangle(self._frame, (x,y), (x+w, y+h), (0,0,255), 3)
            if self._dataAqu:
                self._data.append((x+w/2, y+h/2))

        cv2.imshow('mask', self._mask)
        cv2.imshow('frame', self._frame)
        #cv2.imshow('hsv', hsvImage)

        if cv2.waitKey(1) & 0xFF == ord('q'):  #Q stops the mainloop
            self._running = False

    def run(self):
        '''Run the program'''

        self._tkwindow.tkUpdate()

        while self._running:
            self._tick()
            self._tkwindow.tkUpdate()

        #Clean up
        self._cam.release()    
        cv2.destroyAllWindows()
    
    def randomNumber(self, hsvrc_values):
        '''Returns a random number, using the pendulum as a seed. Reutrns a regular random number if pendulumn not '''
        res = self._maintick(*hsvrc_values)
        if res == None:
            return random.random()
        x, y, w, h = res
        seed = (x+y)/(w+h)
        random.seed(seed)
        return random.random()

if __name__ == '__main__':
    manager = Manager(True)
    manager.run()
else:
    manager = Manager(False)
