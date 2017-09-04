# -*- coding: utf-8 -*-

from numpy import linalg as LA  
from sklearn.cluster import KMeans  
from sklearn.datasets import make_blobs  
from sklearn.metrics.pairwise import rbf_kernel  
from sklearn.preprocessing import normalize  

import matplotlib.pyplot as plt  
import numpy as np  




def load_my_similarity_matrix():
    tags_sim =  np.loadtxt(open('../docs/sim/tags_sim.csv', 'r'),delimiter=",",skiprows=0)
    return tags_sim

def get_W():
    W = load_my_similarity_matrix()[:50,:50]
    return (W + W.T)/2.0
    
def get_D(W):  
    points_num = len(W)
    D = np.diag(np.zeros(points_num))
    for i in range(points_num):
        D[i][i] = sum(W[i])
    return D

def get_eig_vec(L, cluster_num):
    eigval, eigvec = np.linalg.eig(L)
    dim = len(eigval)
    dict_eigval = dict(zip(eigval,range(0,dim)))
    k_eig = np.sort(eigval)[0:cluster_num]
    ix = [dict_eigval[k] for k in k_eig]
    return eigval[ix], eigvec[:, ix]
    
    
    
def main():
#     cluster_num = 5
#     W = get_W()
#     D = get_D(W)
#     L = D - W
#     eigval,eigvec = get_eig_vec(L, cluster_num)
#     clf = KMeans(n_clusters=cluster_num)
#     s = clf.fit(eigvec)
#     C = s.labels_
#     centers = getCenters(data,C)
#     plot(data,s.labels_,centers,cluster_num)
    D = np.diag(np.zeros(5))
    print D
    
    
main()    
    
    