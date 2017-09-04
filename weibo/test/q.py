# -*- coding: utf-8 -*-
from community import best_partition
from community.community_louvain import modularity
import numpy

import matplotlib.pyplot as plt
import networkx as nx


def load_matix():
    user_sim = numpy.loadtxt(open('../docs/sim/user_sim.csv', 'r'),delimiter=",",skiprows=0)
    return user_sim

def main():
    Matrix = load_matix()
    G = nx.from_numpy_matrix(Matrix) 
    part = best_partition(G)
    print part
#     plt.show()
    nx.write_gexf(G,'../docs/test.gexf')
    print modularity(part, G)
    
  
main()  
