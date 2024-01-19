import numpy as np
import matplotlib.pyplot as plt
import random
import customRando

#data = np.random.randn(1000000)
data = customRando.randomFloats(100000)
print(np.mean(np.array(data)))

# fig = plt.figure()
# ax = fig.add_subplot()

a = plt.hist(data, bins=10, edgecolor='Black', color='Blue', alpha=0.7)
#print(a)
#print(a[0])
#print(np.mean(a[0]))

plt.show()
