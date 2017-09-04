# -*- coding: utf-8 -*-

import MySQLdb
import numpy
import matplotlib.pyplot as plt
from collections import Counter

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

def cal_sim(Si, Sj):
    sim = 0.0
    S = [val for val in Si if val in Sj]
    for item in S:
        rank_i = 10 - Si.index(item)
        rank_j = 10 - Sj.index(item)
        sim +=  float(rank_i)/float(rank_i + 1) + float(rank_j)/float(rank_j + 1)    
    return sim

def get_tags(results):
    tags = []
    for r in results:
        tag = r[1]
        if len(tag.split()) != 0:
            tags.append(tag) 
    return tags

def get_sim_0_n(sim_matrix_sum, tags, s):
    N = len(tags) 
    rank = tags.index(s)
    sim_0_n = sim_matrix_sum[rank]
    return sim_0_n / float(N)

def get_normalize_num():
    s = [1,2,3,4,5,6,7,8,9,10]
    return cal_sim(s, s)

def process_tags(results):
    normalize_num = get_normalize_num() #15.9602453102
    
    N = len(results)
    tags_sim = numpy.zeros((N, N))
    for i in range(N):
        j = i + 1
        while j < N :
            Si = results[i][1].split()
            Sj = results[j][1].split()
            tags_sim[i][j] = cal_sim(Si, Sj) / normalize_num
            j += 1
    return tags_sim

def save_tags_sim(tags_sim):
    numpy.savetxt('../docs/sim/tags_sim.csv', tags_sim, fmt = '%.3f', delimiter = ',') 

def show_tags_sim_val(c):
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
    plt.xlabel('tags_sim_val')  #X轴标签
    plt.savefig('../docs/tags_sim_val.png') #保存图  
    plt.show()  #显示图  
    

def get_tags_sim_val(tags_sim):
    tags_sim_val = [] 
    N = len(tags_sim)
    for i in range(N):
        j = i + 1
        while j < N :
            tags_sim_val.append(tags_sim[i][j])
            j += 1
    tags_sim_val.sort()
    numpy.savetxt('../docs/tags_sim_val.txt', tags_sim_val, fmt = '%.3f')
    return tags_sim_val    

def show_tags_sim(tags_sim):
    plt.spy(tags_sim)
    plt.show()
    plt.savefig('../docs/tags_sim.png') #保存图  

        
def main():    
    results = load_user_tags()
    tags_sim = process_tags(results)
    save_tags_sim(tags_sim)

main()


# tags_sim = numpy.loadtxt(open('../docs/sim/tags_sim.csv', 'r'),delimiter=",",skiprows=0)  
# show_tags_sim_val(Counter(get_tags_sim_val(tags_sim)))


