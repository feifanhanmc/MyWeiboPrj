# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt


def get_q():
    data = []
    data.append((0,0))
    data.append((2,0))
    data.append((3,0.02))
    data.append((4,0.04))
    data.append((5,0.33))
    data.append((6,0.356))
    data.append((7,0.356))
    data.append((8,0.348))
    data.append((9,0.34))
    data.append((10,0.33))
    return data

def draw(data):
    X = []
    Y = []
    for d in data:
        X.append(d[0])
        Y.append(d[1])
    plt.plot(X, Y,'b-o')
#     for d in data:
#         plt.scatter(d[0], d[1])
    
    plt.show()

def q2eq(data):
    data_eq = []
    for d in data:
        k = d[0]
        q = d[1]
        if k != 0:
            data_eq.append((k,(k*q)/(k - 1)))
        else:
            data_eq.append((k,q))
    return data_eq

def main():
    data_q = get_q()
    data_eq = q2eq(data_q)
    draw(data_eq)
    print data_eq


main()