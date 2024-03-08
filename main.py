import tkinter as tk
from tkinter import messagebox, filedialog
import pickle
import cv2
import numpy as np
from time import sleep
from tkwindows import Tkwindows
from client import Client
import copy

class Manager:
    '''Object that controlls the program's behavoir'''

    #Colours to be detected by the program, Hue, Sat, Val, Range, Contorsize
    COLOURS = {'Black': (73, 58, 43, 56, 244),
               'Green': (43, 165, 111, 32, 30),
               'Yellow': (47, 255, 175, 30, 30),
               'Purple': (144, 125, 123, 30, 30),
               'Blue': (101, 203, 185, 40, 30),
               'Pink': (169, 92, 168, 30, 30)}
    
    #Colours for bounding boxes for each colour, in BGR not RGB 
    COLOUR_BB_BGR_VALUES = {'Black': (0,0,0),
                            'Green': (0,255,0),
                            'Yellow': (0,255,255),
                            'Purple': (207,17,156),
                            'Blue': (255,0,0),
                            'Pink': (255,0,255)}

    EMPTYDATADICT = {'Black': [], 'Green': [], 'Yellow': [],
                    'Purple': [], 'Blue': [], 'Pink': []}

    def __init__(self, colours = COLOURS):
        self._cam = cv2.VideoCapture(0)
        self._tkwindow = Tkwindows(self)
        self._colours = colours
        self._rolling = False
        self._dataAqu = False
        #Deep copy is used as the shallow copy achieved by .copy() will stil mutate the EMPTY dict
        self._data = copy.deepcopy(self.EMPTYDATADICT)
        self._numofrolls = 0
        self._centrecoords = (None, None)
        self._rollforward = True
        self._running = True
        self._piClient = Client()

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
                pickle.dump((self._numofrolls, self._centrecoords, self._data), out)
            messagebox.showinfo('Save', 'Saved Sucessfully')
        except:
            messagebox.showinfo("Did Not Save", "Unspecified Error") 
        if messagebox.askyesno('Clear Data?', 'Would you like to clear the saved data?'):
            #Deleting and instantiating the data object may seem unnessarcery when you could you .clear()
            #Ran into some predictable reference issues tho, so this method will do.       
            del self._data  
            self._data = copy.deepcopy(self.EMPTYDATADICT)
            self._numofrolls = 0
        root.destroy()

    def toggleRoll(self):
        '''Toggle Bowl Rolling'''
        if self._tkwindow.rollButtonState == 'Start Rolling':
            self._tkwindow.setRollButton('Stop Rolling')
            self._rolling = True
        else:
            self._tkwindow.setRollButton('Start Rolling')
            self._rolling = False

    def toggleDataAqu(self):
        '''Toggle the data aqu'''
        if self._tkwindow.dataAquButtonState == 'Start Data Aqu':
            self._tkwindow.setDataAquButton('Stop Data Aqu')
            self._dataAqu = True
        else:
            self._tkwindow.setDataAquButton('Start Data Aqu')
            self._dataAqu = False
            if messagebox.askquestion("Save data?", "Would you like to save the data?") == 'yes':
                self._saveData()
            #self._data.clear()
    
    def _getColour(self, colour, frame, hsvImage, fcen = False):
        '''Updates the cv2 logic, reading and finding specified colour in webcame frame'''

        hue, sat, val, ran, contourCutOff = self._colours[colour]

        mask = cv2.inRange(hsvImage, np.array([hue-ran, sat-ran, val-ran]), np.array([hue+ran, sat+ran, val+ran]))

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #Find the areas highlighted in mask

        #Only highlight a contour if it is big enough, removes highlighting small areas not wanted
        if len(contours) != 0:
            for countour in contours:
                if cv2.contourArea(countour) > contourCutOff:
                    x, y, w, h = cv2.boundingRect(countour)
                    cv2.rectangle(frame, (x,y), (x+w, y+h), self.COLOUR_BB_BGR_VALUES[colour], 3)
                    if self._dataAqu:
                        self._data[colour].append((x+w/2, y+h/2))
                    elif fcen:
                        return (x+w/2, y+h/2)

            # cv2.imshow('mask', mask)
            # cv2.imshow('frame', frame)
            # cv2.imshow('hsv', hsvImage)

        if cv2.waitKey(1) & 0xFF == ord('q'):  #Q stops the mainloop
            self._running = False

    def rollDice(self):
        #sleep(0.5)
        # if self._rollforward:
        #     self._piClient.sendmsg('s-1000')
        #     self._rollforward = False
        # elif not self._rollforward:
        #     self._piClient.sendmsg('s--1000')
        #     self._rollforward = True
        self._piClient.sendmsg('s--1000')
        sleep(1.1)
        self._piClient.sendmsg('s-0')
        sleep(0.5)

    def getCentre(self):
        self._dataAqu = False
        messagebox.showinfo('Get Centre', 'Place a Black facing die up in centre of bowl')
        centre = self._getColour('Black', self._frame, self._hsvImage, True)
        messagebox.showinfo('Centre Coords', f'Centre of bowl is at x: {centre[0]}, y: {centre[1]}')  
        self._centrecoords = (centre[0], centre[1])      

    def run(self):
        '''Run the program'''

        self._tkwindow.tkUpdate()

        while self._running:
            self._tkwindow.tkUpdate()

            _, self._frame = self._cam.read()
            self._hsvImage = cv2.cvtColor(self._frame, cv2.COLOR_BGR2HSV) #Convert to hsv colour space

            if self._rolling:
                self.rollDice()
                self._numofrolls += 1
            for colour in self._colours.keys():
                self._getColour(colour, self._frame, self._hsvImage)
            
            cv2.imshow('Image', self._frame)

        #Clean up
        self._piClient.sendmsg('sa')
        self._cam.release()    
        cv2.destroyAllWindows()
        #self._saveData()

if __name__ == '__main__':
    manager = Manager()
    manager.run()
