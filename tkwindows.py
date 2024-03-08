import tkinter as tk

class Tkwindows:
    '''Object that stores the tkinter window'''

    def __init__(self, managerObj):

        self._manager = managerObj

        self._root = tk.Tk()
        self._root.title("HSV Picker")
        self._root.protocol('WM_DELETE_WINDOW', self.__closeWindow)   #When window is closed, tells the main loop in manager to stop

        self._getCentreButton = tk.Button(self._root, command = self._manager.getCentre, text = 'Get Centre Coords')
        self._getCentreButton.pack()
        self._startRoll = tk.Button(self._root, command = self._manager.toggleRoll, text="Start Rolling")
        self._startRoll.pack()
        self._toggleDataAqu = tk.Button(self._root, command = self._manager.toggleDataAqu, text = 'Start Data Aqu')
        self._toggleDataAqu.pack()
        self._toggleBothBtn = tk.Button(self._root, command = self.__toggleBoth, text = 'Toggle Both')
        self._toggleBothBtn.pack()

    def __toggleBoth(self):
        '''Toggle both Roll and DataAqu'''
        self._manager.toggleRoll()
        self._manager.toggleDataAqu()

    def __closeWindow(self):
        '''Make sure the program stops when window closes'''
        self._manager.stopMainloop()
        self._root.destroy()

    @property
    def rollButtonState(self):
        '''Return the current state of the start/stop button'''
        return self._startRoll['text']

    @property
    def dataAquButtonState(self):
        return self._toggleDataAqu['text']
    
    def setRollButton(self, txt):
        '''Set the text on the button'''
        self._startRoll.config(text=txt)

    def setDataAquButton(self, txt):
        '''Set the text on the button'''
        self._toggleDataAqu.config(text=txt)

    def tkUpdate(self):
        '''Tick the tkwindow'''
        self._root.title(f"Rolling: {self._manager._rolling}, Collecting Data: {self._manager._dataAqu}, Rolls: {self._manager._numofrolls}")
        self._root.update()
