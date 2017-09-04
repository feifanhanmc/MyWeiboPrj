# -*- coding: utf-8 -*-

import MySQLdb
import numpy


def load_user_gender():
    db  = MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')
    cursor = db.cursor()
    
    sql = """SELECT GENDER FROM RAW_USER ORDER BY UID ASC"""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception,e:
        print e
    db.close()
    return results

def process_gender(results):
    N = len(results)
    gender_sim = numpy.zeros((N, N))
    for i in range(N):
        j = i + 1
        while j < N :
            if results[i][0] == results[j][0]:
                gender_sim[i][j] = 1.0
            j += 1
    return gender_sim

def save_gender_sim(tags_sim):
    numpy.savetxt('../docs/sim/gender_sim.csv', tags_sim, fmt = '%.3f', delimiter = ',') 

def main():    
    results = load_user_gender()
    gender_sim = process_gender(results)
    save_gender_sim(gender_sim)
    
main()