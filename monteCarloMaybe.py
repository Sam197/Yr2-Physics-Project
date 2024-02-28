import random
from math import sqrt
import numpy as np

NUMOFPOINTS = 100000000

# points = [(random.random(), random.random())for _ in range(NUMOFPOINTS)]
# circ = 0

# for point in points:
#     if sqrt((point[0]-0.5)**2 + (point[1]-0.5)**2) <= 0.5:
#         circ += 1

# area = circ/NUMOFPOINTS
# print(area/(0.5**2))

points = np.random.rand(2, NUMOFPOINTS)
#print(points)
#print((points[0]-0.5)**2 + (points[1]-0.5)**2)

dist = np.sqrt((points[0]-0.5)**2 + (points[1]-0.5)**2)
print(len(dist))
#print(dist)
dist = dist[dist <= 0.5]
#print(dist)
print(len(dist))

area = len(dist)/NUMOFPOINTS
print(area/(0.5**2))