# -*- coding: utf-8 -*-

import MySQLdb
import numpy
from scipy.cluster.hierarchy import ward, dendrogram, fcluster
from wordcloud import WordCloud

import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter


def load_dist(k):
    user_sim = numpy.loadtxt(open('../docs/sim/user_sim.csv', 'r'),delimiter=",",skiprows=0) 
    dist = 1 - user_sim

    final_uids = []
    with open('../docs/final_uids.txt') as fp:
        for line in fp:
            final_uids.append(line.strip())
    titles = final_uids
    return dist[:k, :k], titles[:k], user_sim[:k, :k]

def h_cluster(dist, cluster_num): 
    linkage_matrix = ward(dist) # 聚类算法处理之前计算得到的距离，用 linkage_matrix 表示
    nodes_list = list(fcluster(linkage_matrix, t = cluster_num, criterion='maxclust')) #已经确定了最后会产生 t = cluster_num 个簇 
    return linkage_matrix, nodes_list

def get_gexf_file(matrix, nodes_list, titles, k, cluster_num):
    graph = nx.from_numpy_matrix(matrix)
    
    nodes = []
    for i in range(k):
#         nodes.append((titles[i],{'color': str( float(result[i])/float(6) )}))
        nodes.append((i,{'color': str( float(nodes_list[i])/float(cluster_num) )}))
    graph.add_nodes_from(nodes)
    nx.write_gexf(graph,'../docs/user_sim.gexf')
    
def show(linkage_matrix, titles):
    plt.title('Hierarchical Clustering Dendrogram')
    dendrogram(linkage_matrix, orientation="right", labels=titles)
    plt.savefig('../docs/ward_clusters.png')

def load_user_tags():
    db  = MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')
    cursor = db.cursor()
    
    sql = """SELECT UID, TAG FROM RAW_USER ORDER BY UID ASC"""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception,e:
        print e
    db.close()
    return results

def show_recommend(words_list, key):
    t = []
    c = dict(Counter(words_list))
    
    for k, value in c.items():
        t.append((k, value))

    wc = WordCloud(font_path="simhei.ttf", background_color="white", max_font_size=80, random_state=42).generate_from_frequencies(t)   #这个字体一定要加上，因为wordcloud默认不支持中文，贼坑。其实在源码里改其默认的字体也行。
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig('../docs/wordcloud_imgs/' + str(key) + '.png', dpi=600)
    
def recommend(titles, nodes_list):
    results = load_user_tags()
    user_tags = {}
    for r in results:
        user_tags[r[0]] = r[1]
    
    uids_dict = {}
    for i in range(len(nodes_list)):
        if not uids_dict.has_key(nodes_list[i]):
            uids_dict[nodes_list[i]] = []
        uids_dict[nodes_list[i]].append(titles[i])
        
    tags_dict = {}
    for key in  uids_dict:
        if not tags_dict.has_key(key):
            tags_dict[key] = []
        for uid in uids_dict[key]:
            tags_dict[key].extend(user_tags[uid].split())
    
    for key, tags in tags_dict.items():
        print key
        tags_list = []
        for tag in tags:
            tags_list.append(tag.decode('utf8'))
        show_recommend(tags_list, key)
    
def main():
    #测试时只取前k个，一共3759个
    cluster_num = 6 #假的
#     cluster_num = 2 #真的
    k = 1200
    dist, titles, user_sim = load_dist(k)
    linkage_matrix ,nodes_list = h_cluster(dist, cluster_num)
    
#     show(linkage_matrix, titles)
    recommend(titles, nodes_list)
    get_gexf_file(user_sim, nodes_list, titles, k, cluster_num)
    
main()
