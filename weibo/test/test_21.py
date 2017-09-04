# -*- coding: utf-8 -*-

import numpy
from random import random

A = numpy.zeros((5,5))

for i in range(5):
    j = i + 1
    while j < 5 :
        A[i][j] = random()
        j += 1
numpy.savetxt('aaaaa.csv', A, fmt='%.3f', delimiter=',')
