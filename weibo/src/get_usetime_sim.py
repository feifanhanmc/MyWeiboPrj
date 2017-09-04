# -*- coding: utf-8 -*-

import time

import MySQLdb
import numpy


def load_user_gender():
    db  = MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')
    cursor = db.cursor()
    
    sql = """SELECT CREATED_AT FROM RAW_USER ORDER BY UID ASC"""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception,e:
        print e
    db.close()
    return results

def process_usetime(results):
    max_min =  results.max() - results.min()
    N = len(results)
    usetime_sim = numpy.zeros((N, N))
    
    for i in range(N):
        j = i + 1
        while j < N :
            usetime_sim[i][j] = 1.0 - ((abs(results[i][0] - results[j][0])) / max_min)
            j += 1
    return usetime_sim

def save_usetime_sim(usetime_sim):
    numpy.savetxt('../docs/sim/usetime_sim.csv', usetime_sim, fmt = '%.3f', delimiter = ',') 

def main():    
    results = load_user_gender()
    usetime_sim = process_usetime(numpy.array(results, dtype = 'float'))
    save_usetime_sim(usetime_sim)
    
main()