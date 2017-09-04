# -*- coding: utf-8 -*-
import numpy
import networkx as nx

def matrix2gexf(matrix):
    graph = nx.from_numpy_matrix(matrix) 
#     nx.draw(graph)  
    nx.write_gexf(graph,'../docs/user_sim.gexf')

def load_user_sim():
    return numpy.loadtxt(open('../docs/sim/user_sim.csv', 'r'),delimiter=",",skiprows=0)            

def main():
    user_sim = load_user_sim()[:500,:500]
    matrix2gexf(user_sim)

main()
