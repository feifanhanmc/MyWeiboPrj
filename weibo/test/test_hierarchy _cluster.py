# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import ward, dendrogram
from sklearn.metrics.pairwise import cosine_similarity
import numpy

def load_dist():
    tfidf_matrix = [
                    [0,0,1],
                    [0,0.8,0.9],
                    [0.3,0.4,0.1],
                    [0.9,0.3,0.5],
                    [0,1,0],
                    [0,1,1],
                    [0,0.2,0.2],
                    [1,0,0],
                    [1,0,1],
                    [1,1,0],
                    [1,1,1]]
    
    titles = []
    for i in range(len(tfidf_matrix)):
        titles.append(str(i) + str(tfidf_matrix[i]))
    dist = 1 - cosine_similarity(tfidf_matrix)
    numpy.savetxt('test_h_cluster.csv', dist, fmt='%.3f', delimiter=',')
    
    return dist, titles

def load_my_dist():
    statuses_sim = numpy.loadtxt(open('../docs/sim/statuses_sim.csv', 'r'),delimiter=",",skiprows=0) 
    dist = 1 - statuses_sim

    final_uids = []
    with open('../docs/final_uids.txt') as fp:
        for line in fp:
            final_uids.append(line.strip())
    return dist, final_uids
    
def h_cluster(dist): 
    linkage_matrix = ward(dist) # 聚类算法处理之前计算得到的距离，用 linkage_matrix 表示
    return linkage_matrix

def show(linkage_matrix, titles):
    fig, ax = plt.subplots(figsize=(15, 20)) # 设置大小
    ax = dendrogram(linkage_matrix, orientation="right", labels=titles)
    plt.title('Hierarchical Clustering Dendrogram')
    plt.tight_layout() # 展示紧凑的绘图布局
    
    # 注释语句用来保存图片
    plt.savefig('ward_clusters.png', dpi=200) # 保存图片为 ward_clusters

def simple_show(linkage_matrix, titles):
    plt.title('Hierarchical Clustering Dendrogram')
    dendrogram(linkage_matrix, orientation="right", labels=titles)
    plt.savefig('ward_clusters.png')
    
def main():
#     dist, titles = load_dist()
    dist, titles = load_my_dist()
    linkage_matrix = h_cluster(dist)
    
#     print linkage_matrix
    print linkage_matrix.shape
    simple_show(linkage_matrix, titles)
    
main()