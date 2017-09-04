# -*- coding: utf-8 -*-
from collections import Counter

import numpy

import matplotlib.pyplot as plt  

tags_sim_val = [0.667,0.667,0.672,0.672,0.673,0.674,0.689,0.695,0.697,0.698,0.701,0.706,0.706,0.707,0.708,0.709,0.710,0.711,0.711,0.715,0.718,0.721,0.721,0.722,0.732,0.736,0.741,0.755,0.799,0.827,0.886,0.912,0.916]

# a = [1,2,3,4,5]
# numpy.savetxt('test_19.txt', a, fmt = '%.6f')
def test():
#     c = {0.1:5, 0.2:2, 0.4:1}
    c = dict(Counter(tags_sim_val))
    print c
    X = []
    Y = []
    Key = []
    for key in c:
        Key.append(key)
    Key = list(set(Key))
    Key.sort()  
    for key in Key:
        X.append(key)
        Y.append(c[key])
    print X
    print Y
    plt.plot(X, Y)   #在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）  
    plt.ylabel('num')  #Y轴标签  
    plt.ylabel('tags_sim_val')  #X轴标签
    plt.show()  #显示图  
test()