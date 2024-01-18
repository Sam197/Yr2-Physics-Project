'''
Code for detecting a colour from a webcam image using open-cv2. There is a tkinter window with sliders to
pick the hsv colour values wanted to isolate from the image. cv2 displays two images, the image from the cam
with a bounding rect around the isolated pixels, if there are any, and the mask used to find and isolate the
pixels. Data is exported as a pickle file. This script contains no data anaylsis 
'''
# pylint: disable=no-member
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import pickle
import cv2
import numpy as np
from time import time


def start_data_aqu():
    '''
    Starts the aquastion of data
    '''
    global data_aqu
    global data

    data_aqu = True
    data.clear()

def stop_data_aqu():
    '''
    Stops the aquastion of data
    '''
    global data_aqu
    global data
    data_aqu = False
    print(data)
    if messagebox.askquestion("Save data?", "Would you like to save the data?"):
        save_data(data)

def save_data(the_data):
    '''
    Saves the data
    '''
    root = tk.Tk()
    root.withdraw()
    root.filename = filedialog.asksaveasfile(mode = "w", defaultextension = ".pickle")
    try:
        with open(root.filename.name, 'wb') as out:
            pickle.dump(the_data, out)
        messagebox.showinfo('Save', 'Saved Sucessfully')
    except:
        messagebox.showinfo("Did Not Save", "Unspecified Error") 
    root.destroy()

def cv2Main():
    '''
    The main loop for running open-cv to access the webcam and find a bounding box of a certain colour
    '''

    global hueS            #I don't like globals, but this was the easiest way of doing this
    global satS            #Not necessarily the correct way tho.....
    global valS
    global rangeS
    global contorCutOff
    global data_aqu
    global data

    data_aqu = False
    data = []

    cap = cv2.VideoCapture(0)  #Get webcam, 0 is default cam

    while True:
        start = time()
        ret, frame = cap.read()

        hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Convert to hsv colour space

        #Get the values from the sliders in tk window
        hue = hueS.get()
        sat = satS.get()
        val = valS.get()
        ran = rangeS.get()

        mask = cv2.inRange(hsvImage, np.array([hue-ran, sat-ran, val-ran]), np.array([hue+ran, sat+ran, val+ran]))

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #Find the areas highlighted in mask

        #Only highlight a contour if it is big enough, removes highlighting small areas not wanted
        if len(contours) != 0:
            for countour in contours:
                if cv2.contourArea(countour) > contorCutOff.get():
                    x, y, w, h = cv2.boundingRect(countour)
                    cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 3)
                    print(x,y)
                    if data_aqu:    #Get the data
                        data.append((x+w/2, y+h/2))

        cv2.imshow('mask', mask)
        cv2.imshow('frame', frame)
        #cv2.imshow('hsv', hsvImage)

        if cv2.waitKey(1) & 0xFF == ord('q'):  #Q key quits out of the loop
            break

        #print(time()-start)

    cap.release()

    cv2.destroyAllWindows()

def main():
    '''
    The main func for the tk window. Hue, Saturation and Value all correspond to HSV values in the input image to be
    isolated in the mask of the image. The range is to spescify the range for the HSV values to be isolated, so a range
    of 0 will give a mask with no isolation and no colour will exactly match the HSV colour specified - and a range of 255
    will give a mask of all white, as all colours will fall within the range. The contourCutOff is selecting how small, or
    big, we want a collection of isolated pixels to be before we draw a box around them. This 'cleans' up the image, not
    letting small 1 pixel detections being mistakenly identified as the pendulum.
    '''

    global hueS  #Not the globals again :-(
    global satS
    global valS
    global rangeS
    global contorCutOff

    def butfunc():
        '''Target for the button'''
        if start['text'] == "Start":
            start.config(text="Stop")
            start_data_aqu()
        else:
            start.config(text="Start")
            stop_data_aqu()

    #Create window and add widgets
    root = tk.Tk()
    root.title("HSV Picker")

    hueS = tk.Scale(root, label = 'Hue Value', from_ = 0, to_ = 180, orient=tk.HORIZONTAL, length = 200, tickinterval = 45)
    hueS.pack()
    satS = tk.Scale(root, label = 'Saturation Value', from_ = 0, to_ = 255, orient = tk.HORIZONTAL, length = 200, tickinterval = 50)
    satS.pack()
    valS = tk.Scale(root, label = 'Value Value', from_ = 0, to_ = 255, orient=tk.HORIZONTAL, length = 200, tickinterval = 50)
    valS.pack()
    rangeS = tk.Scale(root, label = 'Detection Range', from_ = 0 , to = 255, orient = tk.HORIZONTAL, length = 200, tickinterval = 50)
    rangeS.pack()
    contorCutOff = tk.Scale(root, label = 'Min contour size', from_ = 50, to_ = 1000, orient = tk.HORIZONTAL, length = 200, tickinterval = 100)
    contorCutOff.pack()
    start = tk.Button(root, command = butfunc, text="Start")
    start.pack()

    tk.mainloop() #Mainloop hogs the thread.

    #This kept throwing an error, then it hit me, you can't call a widget that's been yeeted out of existance
    # with open("Prev values.txt", 'w', encoding='utf8') as out:
    #     out.write(f"Hue {hueS.get()}, Sat {satS.get()}, Val {valS.get()}, Range {rangeS.get()}, Contour Cutoff {contorCutOff.get()}")

if __name__ == '__main__':
    #Starting the open-cv logic in a seperate thread since tk.mainloop() blocks the thread, mainloop() is kept in the main
    #thread as I read somewhere that tkinter doesn't like not being in the main thread. It is possible to use tk.update() which isn't thread 
    #blocking, but this could lead to instablities if it is not called often enough. While in theory this shouldn't be a problem, not gonna take
    #that chance. The number of globals could have been reduced if classes were used.

    cam = threading.Thread(target = cv2Main, daemon=True)
    cam.start()
    main()
    

