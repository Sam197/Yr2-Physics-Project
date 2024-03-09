# Yr2-Physics-Project
Welcome to the GitHub repo for our Year 2 Physics Project 'How Random Can you Get?' The repo is split into folders containing their respective expirment's code. There is also a misc folder containing extra scripts written that don't belong to any of the expirements. A lot of the code in the repo is superfluous, and badly written, so please don't judge too much :).

# Double Pendulum
This folder contains all the code used to track the double pendulum and some data analysis code aswell. In addtion, 'Long collect full.pickle' is a pickled python list containing the raw data collected from the double pendulum. Pend track 3.5 and pt35 are the final iterations of the pendulum tracking software

# Keystrokes

# Dice Rolling
This folder contains all the code used to roll and track dice. tkwindows and client are dependancies for main.py and all run on a (semi) powerful computer, with piServer.py running on a raspberry pi, and only handling socket requests and sending spin commands to the motor used. The code to control the motor from the raspberry pi was taken from mDEV.py from this repo https://github.com/Freenove/Freenove_Three-wheeled_Smart_Car_Kit_for_Raspberry_Pi.
