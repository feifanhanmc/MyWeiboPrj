# -*- coding: utf-8 -*-
from sklearn.metrics.pairwise import cosine_similarity


tfidf_matrix = [[0,0,0],
                [0,0,1],
                [0,1,0],
                [0,1,1],
                [1,0,0],
                [1,0,1],
                [1,1,0],
                [1,1,1]]

dist = 1 - cosine_similarity(tfidf_matrix)

A = []
for i in dist:
    a = []
    for j in i:
        temp =  '%0.3f' % j
        a.append(temp)
    A.append(a)

for i in  A:
    print i 

