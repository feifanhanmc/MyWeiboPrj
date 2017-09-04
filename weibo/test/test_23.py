#-*- coding:utf8-*-
import numpy
import networkx as nx
import matplotlib.pyplot as plt

def test2():
    Matrix = numpy.loadtxt(open('aaaaa.csv', 'r'),delimiter=",",skiprows=0)

    graph = nx.from_numpy_matrix(Matrix) 
#     nx.draw(graph)  
    nx.write_gexf(graph,'bbbbb.gexf')
#     plt.show()


test2()