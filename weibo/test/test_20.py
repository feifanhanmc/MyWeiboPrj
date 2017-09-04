import numpy
import matplotlib.pyplot as plt

a = numpy.array([[0, 1, 2],
                 [3, 4, 0],
                 [2, 1, 3]])

location = a.argmax(axis=1)
print a.max()
i =  location[0] -1 
j =  location[1]
print i, j
print a[i][j]
plt.spy(a)
plt.show()