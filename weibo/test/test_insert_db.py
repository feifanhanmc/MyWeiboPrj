# -*- coding: utf-8 -*-
import MySQLdb

db= MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
db.set_character_set('utf8')

cursor = db.cursor()
# cursor.execute('DROP TABLE IF EXISTS TEST')
# sql = """CREATE TABLE TEST (
#          FIRST_NAME  CHAR(20) NOT NULL,
#          LAST_NAME  CHAR(20),
#          AGE INT,  
#          SEX CHAR(1),
#          INCOME FLOAT )"""
# cursor.execute(sql)

uid = '12345'
name = 'saa'
print name
name1 =  name.encode('utf-8')
sql = """INSERT INTO TEST(FIRST_NAME,
         LAST_NAME, AGE, SEX, INCOME)
         VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
try:
    cursor.execute(sql)
    db.commit()
except Exception,e :
    print e
    db.rollback()
    
db.close()