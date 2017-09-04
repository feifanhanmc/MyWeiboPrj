# -*- coding: utf-8 -*-

import csv
import os
from os.path import isfile

import MySQLdb
from numpy import transpose
import numpy


def load_cluster_result():
    uids = []
    cluster_result = []
    db = MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')

    cursor = db.cursor()
    sql = 'SELECT *  FROM CLUSTER_RESULT'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for item in results:
            uids.append(item[0])
            cluster_result.append(list(item[1:]))
        db.commit()
    except Exception,e :
        print e
        db.rollback()
    db.close()
    return uids, cluster_result

uids, cluster_result = load_cluster_result()
trans_cluster_result = transpose(cluster_result)

weight = numpy.zeros( (len(uids),len(uids) ))
for I in range(10):
    result = trans_cluster_result[I]
    for i in range(len(uids)):
        j = i + 1
        while j < len(uids):
            if result[i] == result[j]:
                weight[i][j] += 1
            j += 1

filename = '../docs/weight.csv'
if isfile(filename):
    os.remove(filename)
with open(filename, 'ab+') as fout:
    writer = csv.writer(fout)
    writer.writerows(weight)
fout.close() 


total_num = ( len(weight) * (len(weight) - 1))/2 
num_10 = 0
num_9 = 0
num_8 = 0
num_7 = 0
num_6 = 0
num_5 = 0
num_4 = 0
num_3 = 0
num_2 = 0
num_1 = 0
       
for i in range(len(weight)):
    for j in range(len(weight)):
        if weight[i][j] == 10.0 :
            num_10 += 1
        elif weight[i][j] == 9.0 :
            num_9 += 1
        elif weight[i][j] == 8.0 :
            num_8 += 1
        elif weight[i][j] == 7.0 :
            num_7 += 1
        elif weight[i][j] == 6.0 :
            num_6 += 1
        elif weight[i][j] == 5.0 :
            num_5 += 1
        elif weight[i][j] == 4.0 :
            num_4 += 1
        elif weight[i][j] == 3.0 :
            num_3 += 1
        elif weight[i][j] == 2.0 :
            num_2 += 1
        elif weight[i][j] == 1.0 :
            num_1 += 1    

            
print float(num_10)/total_num
print float(num_9)/total_num
print float(num_8)/total_num
print float(num_7)/total_num
print float(num_6)/total_num
print float(num_5)/total_num
print float(num_4)/total_num
print float(num_3)/total_num
print float(num_2)/total_num
print float(num_1)/total_num
'''
0.0591830484841
0.0332134227933
0.0527217402173
0.0270376252145
0.0497446100972
0.0361550121638
0.0608202923464
0.048572950054
0.0665370219103
0.10965150518'''




