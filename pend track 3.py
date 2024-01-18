import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import pickle
import cv2
import numpy as np

class Tkwindows:

    def __init__(self, managerObj):

        self._manager = managerObj

        self._root = tk.Tk()
        self._root.title("HSV Picker")

        self._hueS = tk.Scale(self._root, label = 'Hue Value', from_ = 0, to_ = 180, orient=tk.HORIZONTAL, length = 200, tickinterval = 45)
        self._hueS.pack()
        self._satS = tk.Scale(self._root, label = 'Saturation Value', from_ = 0, to_ = 255, orient = tk.HORIZONTAL, length = 200, tickinterval = 50)
        self._satS.pack()
        self._valS = tk.Scale(self._root, label = 'Saturaton Value', from_ = 0, to_ = 255, orient=tk.HORIZONTAL, length = 200, tickinterval = 50)
        self._valS.pack()
        self._rangeS = tk.Scale(self._root, label = 'Detection Range', from_ = 0 , to = 255, orient = tk.HORIZONTAL, length = 200, tickinterval = 50)
        self._rangeS.pack()
        self._contorCutOff = tk.Scale(self._root, label = 'Min contour size', from_ = 0, to_ = 1000, orient = tk.HORIZONTAL, length = 200, tickinterval = 250)
        self._contorCutOff.pack()
        self._start = tk.Button(self._root, command = self._manager.toggleDataAqu, text="Start")
        self._start.pack()

    @property
    def buttonState(self):
        return self._start['text']
    
    def setButton(self, txt):
        self._start.config(text=txt)

    @property
    def hsvrc_values(self):
        return self._hueS.get(), self._satS.get(), self._valS.get(), self._rangeS.get(), self._contorCutOff.get()

    def tkUpdate(self):
        pass

class Manager:

    def __init__(self):
        self._tkwindow = Tkwindows(self)
        self._dataAqu = False
        self._cam = cv2.VideoCapture(0)
        self._data = []      
        self._running = True  

    def _saveData(self):
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
        if self._tkwindow.buttonState == 'Start':
            self._tkwindow.setButton('Stop')
            self._dataAqu = True
        else:
            self._tkwindow.setButton('Start')
            self._dataAqu = False
            if messagebox.askquestion("Save data?", "Would you like to save the data?") == 'yes':
                self._saveData()
            self._data.clear()
    
    def _tick(self):
        ret, frame = self._cam.read()

        hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Convert to hsv colour space

        #Get the values from the sliders in tk window
        hue, sat, val, ran, contourCutOff = self._tkwindow.hsvrc_values

        mask = cv2.inRange(hsvImage, np.array([hue-ran, sat-ran, val-ran]), np.array([hue+ran, sat+ran, val+ran]))

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #Find the areas highlighted in mask

        #Only highlight a contour if it is big enough, removes highlighting small areas not wanted
        if len(contours) != 0:
            for countour in contours:
                if cv2.contourArea(countour) > contourCutOff:
                    x, y, w, h = cv2.boundingRect(countour)
                    cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 3)
                    print(x,y)
                    if self._dataAqu:    #Get the data
                        self._data.append((x+w/2, y+h/2))

        cv2.imshow('mask', mask)
        cv2.imshow('frame', frame)
        #cv2.imshow('hsv', hsvImage)

        if cv2.waitKey(1) & 0xFF == ord('q'):  #Q key quits out of the loop
            self._running = False

    def run(self):

        while self._running:
            self._tkwindow.tkUpdate()
            self._tick()

manager = Manager()
manager.run()
