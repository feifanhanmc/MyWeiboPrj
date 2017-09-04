# -*- coding: utf-8 -*-

import MySQLdb
import numpy

def load_user_sr():
    db  = MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')
    cursor = db.cursor()
    
    sql = """SELECT BI_FOLLOWERS_COUNT, FRIENDS_COUNT, FOLLOWERS_COUNT, STATUSES_COUNT ,POST_RATE FROM  RAW_USER ORDER BY UID ASC"""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception,e:
        print e
    db.close()
    return results

def process_sr_sim(pre_weight):
    weight_T = []
    max = pre_weight.max(axis=0)
    n =len(max)
    for i in range(n):
        weight_T.append(pre_weight[:, i] / float(max[i]))
    weight = numpy.array(weight_T).T
    
    normalize_num = n**0.5
    N = len(weight)
    sr_sim = numpy.zeros((N, N))
    for i in range(N):
        j = i + 1
        while j < N:
            sr_sim[i][j] = 1 - ( numpy.linalg.norm(weight[i] - weight[j]) / float(normalize_num) )
            j += 1
    return sr_sim

def save_sr_sim(sr_sim):
    numpy.savetxt('../docs/sim/sr_sim.csv', sr_sim, fmt = '%.3f', delimiter = ',') 

def main():    
    results = load_user_sr()
    pre_weight = numpy.array(results, dtype = numpy.float64)
    #不应当使用余弦相似度，应该使用欧氏距离（首先把BI_FOLLOWERS_COUNT, FRIENDS_COUNT, FOLLOWERS_COUNT, STATUSES_COUNT ,POST_RATE都归一化到[0,1]之间）
    sr_sim = process_sr_sim(pre_weight)
    save_sr_sim(sr_sim)
    
main()