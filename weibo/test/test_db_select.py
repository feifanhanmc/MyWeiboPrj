# -*- coding: utf-8 -*-
import MySQLdb


db = MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
db.set_character_set('utf8')
db_uids = []
cursor = db.cursor()
sql = 'SELECT * from RAW_USER ORDER BY UID ASC'
try:
    cursor.execute(sql)
    result =  cursor.fetchall()
    db.commit()
except Exception,e :
    print e
    db.rollback()
db.close()


for item in  result[:10]:
    print item[0]
# 1000432103
# 1001236733
# 1001616281
# 1002798397
# 1003024017
# 1003125555
# 1003273015
# 1003843290
# 1004107845
# 1004201170