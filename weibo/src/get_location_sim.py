# -*- coding: utf-8 -*-

import MySQLdb
import numpy

def load_user_location():
    db  = MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')
    cursor = db.cursor()
    
    sql = """SELECT UID, PROVINCE, CITY FROM RAW_USER ORDER BY UID ASC"""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception,e:
        print e
    db.close()
    return results

def process_location(results):
    N = len(results)
    location_sim = numpy.zeros((N, N))
    
    for i in range(N):
        j = i + 1
        while j < N:
            if results[i][1] == results[j][1]:
                if results[i][2] == results[j][2]:
                    location_sim[i][j] = 1.0
                else:
                    location_sim[i][j] = 0.666667
            j += 1
    return location_sim


def save_location_sim(location_sim):
    numpy.savetxt('../docs/sim/location_sim.csv', location_sim, fmt = '%.3f', delimiter = ',')  

def main():    
    results = load_user_location()
    location_sim = process_location(results)
    save_location_sim(location_sim)
    
main()