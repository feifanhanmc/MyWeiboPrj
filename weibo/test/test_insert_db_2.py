# -*- coding: utf-8 -*-
import MySQLdb

db= MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
db.set_character_set('utf8')

cursor = db.cursor()
# cursor.execute('DROP TABLE IF EXISTS TEST2')
# sql = """CREATE TABLE TEST2 (
#         UID    CHAR(10) PRIMARY KEY,
#         NAME  CHAR(20))"""
# cursor.execute(sql)

uid = '12345'
name = 'aaa'
user = []
user.append(uid)
user.append(name)
# print name
# name1 =  name.encode('utf-8')
# sql = """INSERT INTO TEST2(UID,NAME) VALUES (%s, 'aaa')""" % ('12345')    #正确
# sql = """INSERT INTO TEST2(UID,NAME) VALUES (%s, %s)""" %("12345", "aaa")  #错误
# sql = """INSERT INTO TEST2(UID,NAME) VALUES (%s, %s)""" % ('12345', '111')    #正确
sqli = """INSERT INTO TEST2(UID,NAME) VALUES (%s, %s)"""
try:
    cursor.execute(sqli,(uid, name))
    db.commit()
except Exception,e :
    print e
    db.rollback()
    
db.close()