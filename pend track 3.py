'''
A rewrite of pend track2, this time with NO GLOBAL VARIABLES!! WOOOOOO. The logic behind the detection of the pendulum is the same however
'''
# pylint: disable=no-member
import tkinter as tk
from tkinter import messagebox, filedialog
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

    def tkUpdate(self):
        '''Tick the tkwindow'''
        self._root.title(f"Data points {2*len(self._manager._data)}")
        self._root.update()

class Manager:
    '''Object that controlls the program's behavoir'''

    def __init__(self):
        self._cam = cv2.VideoCapture(0)
        self._tkwindow = Tkwindows(self)
        self._dataAqu = False
        self._data = []
        self._running = True

    def stopMainloop(self):
        '''Stop the program'''
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
            self._data.clear()
    
    def _tick(self):
        '''Updates the cv2 logic, reading and finding specified colour in webcame frame'''
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
                    if self._dataAqu:
                        self._data.append((x+w/2, y+h/2))

        cv2.imshow('mask', mask)
        cv2.imshow('frame', frame)
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

if __name__ == '__main__':
    manager = Manager()
    manager.run()
