'''
Measure the time between key board events to 17 dp (may depend on
machine being used)
'''
import keyboard

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
