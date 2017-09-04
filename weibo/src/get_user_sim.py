# -*- coding: utf-8 -*-

import numpy
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
from community.community_louvain import best_partition, modularity


def save_sim(sim, filename):
    numpy.savetxt(filename, sim, fmt = '%.3f', delimiter = ',') 

def load_sim(filename):
    return numpy.loadtxt(open(filename, 'r'),delimiter=",",skiprows=0)
    
def get_user_sim(weight):
    #设置权重,之和等于1
    baseinfo_w = weight[0]
    sr_w = weight[1]
    tags_w = weight[2]
    statuses_w = weight[3]
    
    #加载各部分内容
    baseinfo_sim = load_sim('../docs/sim/baseinfo_sim.csv')
    sr_sim = load_sim('../docs/sim/sr_sim.csv')
    tags_sim = load_sim('../docs/sim/tags_sim.csv')
    statuses_sim = load_sim('../docs/sim/statuses_sim.csv')
    
    user_sim = statuses_w*statuses_sim + tags_w*tags_sim + baseinfo_w*baseinfo_sim + sr_w*sr_sim 
    save_sim(user_sim, '../docs/sim/user_sim.csv')
    return user_sim

def get_user_sim_val(user_sim):
    user_sim_val = [] 
    N = len(user_sim)
    for i in range(N):
        j = i + 1
        while j < N :
            user_sim_val.append(user_sim[i][j])
            j += 1
    user_sim_val.sort()
#     numpy.savetxt('../docs/user_sim_val.txt', user_sim_val, fmt = '%.3f')
    return user_sim_val  

def show_user_sim_val(c):
    Key = []
    for key in c:
        Key.append(key)
    Key = list(set(Key))
    Key.sort()  
    X = []
    Y = []
    for key in Key:
        X.append(key)
        Y.append(c[key])
    plt.plot(X, Y)   #在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）  
    plt.ylabel('count')  #Y轴标签  
    plt.xlabel('user_sim_val')  #X轴标签
    plt.savefig('../docs/user_sim_val.png') #保存图  
    plt.show()  #显示图  

def get_gephi_doc(sim_name, k):
    '''
    :sim_name 实验对象matrix对应的数据源文件名
    :k 因为节点过多，选择前k个节点进行实验
    '''
    sim_matrix = load_sim('../docs/sim/' + sim_name + '.csv')
    matrix = sim_matrix[:k, :k]
    graph = nx.from_numpy_matrix(matrix)
    nx.write_gexf(graph,'../docs/gephi/' + sim_name + '.gexf') 

def init_sim_500():
    baseinfo_sim = load_sim('../docs/sim/baseinfo_sim.csv')
    sr_sim = load_sim('../docs/sim/sr_sim.csv')
    tags_sim = load_sim('../docs/sim/tags_sim.csv')
    statuses_sim = load_sim('../docs/sim/statuses_sim.csv') 
       
    save_sim(baseinfo_sim[:500,:500], '../docs/sim_500/baseinfo_500_sim.csv')
    save_sim(sr_sim[:500,:500], '../docs/sim_500/sr_500_sim.csv')
    save_sim(tags_sim[:500,:500], '../docs/sim_500/tags_500_sim.csv')
    save_sim(statuses_sim[:500,:500], '../docs/sim_500/statuses_500_sim.csv')

def get_weight(eq_list):
    weight_list = []
    total = sum(eq_list)
    for eq in eq_list:
        weight_list.append(eq/total)
    return weight_list

def get_eq(sim_matrix):
    G = nx.from_numpy_matrix(sim_matrix) 
    part = best_partition(G)
    q =  modularity(part, G)
    k = len(list(set(part.values())))
    if k == 1:
        eq = 0
    else:
        eq = float(k * q) / float( k - 1)
    data = {}
    data['eq'] = eq
    data['q'] = q
    data['k'] = k
    return data

def find_best_weight():
    #baseinfo, sr, tags, statuses
    #这部分权重由myGA中的遗传算法搜索得到
    weight = [0.156673, 0.175957, 0.411411, 0.255959]  #假的  
#     weight = [0.8425925925925924, 0.0, 0.046296296296296294, 0.1111111111111111] #真的
    return weight
    
def main():
#     init_sim_500()  #只考虑前500个节点以提高效率
    weight = find_best_weight()
    get_user_sim(weight)
    
main()





