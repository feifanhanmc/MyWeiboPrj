# -*- coding: utf-8 -*-

import csv

import MySQLdb
from numpy import transpose
from sklearn.cluster.k_means_ import KMeans


def load_data(filename):
    uids = []
    vectors = []
    with open(filename, 'r') as fp:
        for row in csv.reader(fp):
            uids.append(row[0])
            vectors.append(row[1:])
    fp.close()
    return uids, vectors


def KMeans_cluster(vectors):
    clf = KMeans(n_clusters = 10)
    clf.fit(vectors)
    return clf.labels_  

def init_cluster_result():
    db= MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS CLUSTER_RESULT')
    sql = """CREATE TABLE CLUSTER_RESULT (
        UID    VARCHAR(10) PRIMARY KEY,
        CLUSTER1    VARCHAR(5),
        CLUSTER2    VARCHAR(5),
        CLUSTER3    VARCHAR(5),
        CLUSTER4    VARCHAR(5),
        CLUSTER5    VARCHAR(5),
        CLUSTER6    VARCHAR(5),
        CLUSTER7    VARCHAR(5),
        CLUSTER8    VARCHAR(5),
        CLUSTER9    VARCHAR(5),
        CLUSTER10    VARCHAR(5))"""
    cursor.execute(sql)
    db.close() 
    
def save_cluster_result(uids, labels):
    users = []
    for i in range(len(uids)):
        user = []
        user.append(uids[i])
        user.extend(labels[i])
        users.append(user)
    db= MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')
    cursor = db.cursor()
    for user in users:
        sqli = 'INSERT INTO CLUSTER_RESULT(UID, CLUSTER1, CLUSTER2, CLUSTER3, CLUSTER4, CLUSTER5, CLUSTER6, CLUSTER7, CLUSTER8, CLUSTER9, CLUSTER10) \
                                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        try:
            cursor.execute(sqli,(str(user[0]), str(user[1]), str(user[2]), str(user[3]), str(user[4]), str(user[5]), str(user[6]), str(user[7]), str(user[8]), str(user[9]), str(user[10])))
            db.commit()
        except Exception,e :
            print e
            db.rollback()
    db.close()
    
def main():   
    uids, vectors = load_data('../docs/users.csv')
    labels = []
    for i in range(10):
        print 'Index : ' + str(i)
        labels.append(KMeans_cluster(vectors))
    
    labels = transpose(labels)  
    save_cluster_result(uids, labels)

# init_cluster_result()
main()    
