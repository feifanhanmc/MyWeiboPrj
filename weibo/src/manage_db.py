# -*- coding: utf-8 -*-
import MySQLdb


def init_raw_user_show():
    db= MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')
    
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS RAW_USER_SHOW')
    sql = """CREATE TABLE RAW_USER_SHOW (
        UID    VARCHAR(10) PRIMARY KEY,
        NAME    VARCHAR(30),
        GENDER    VARCHAR(1),
        CREATED_AT    VARCHAR(10),
        BI_FOLLOWERS_COUNT    VARCHAR(5),
        PROVINCE    VARCHAR(5),
        CITY    VARCHAR(5),
        LOCATION    VARCHAR(20))"""
    cursor.execute(sql)
    db.close()
    
def init_raw_user_tag():
    db= MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')
    
    cursor = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS RAW_USER_TAG')
    sql = """CREATE TABLE RAW_USER_TAG (
        UID    VARCHAR(10) PRIMARY KEY,
        TAG VARCHAR(100))"""
    cursor.execute(sql)
    db.close()
 
def init_raw_user_sr():
    db= MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')
    
    cursor = db.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS RAW_USER_SR')
    sql = """CREATE TABLE RAW_USER_SR (
        UID    VARCHAR(10) PRIMARY KEY,
        STATUSES_COUNT VARCHAR(10),
        FRIENDS_COUNT VARCHAR(10),
        FOLLOWERS_COUNT VARCHAR(10),
        POST_RATE VARCHAR(10),
        STATUSES TEXT(100000))"""
    cursor.execute(sql)
    db.close()    

def init_raw_user():
    db= MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')
    
    cursor = db.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS RAW_USER')
    sql = """CREATE TABLE RAW_USER (
        UID    VARCHAR(10) PRIMARY KEY,
        NAME    VARCHAR(30),
        GENDER    VARCHAR(1),
        CREATED_AT    VARCHAR(10),
        BI_FOLLOWERS_COUNT    VARCHAR(5),
        PROVINCE    VARCHAR(5),
        CITY    VARCHAR(5),
        LOCATION    VARCHAR(20),
        TAG VARCHAR(100),
        STATUSES_COUNT VARCHAR(10),
        FRIENDS_COUNT VARCHAR(10),
        FOLLOWERS_COUNT VARCHAR(10),
        POST_RATE VARCHAR(10),
        STATUSES TEXT(100000))"""
    cursor.execute(sql)
    db.close()   

def get_db_uids():
    db_uids = []
    db = MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')

    cursor = db.cursor()
    sql = 'SELECT UID  FROM RAW_USER'
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for item in results:
            db_uids.append(item[0])
        db.commit()
    except Exception,e :
        print e
        db.rollback()
    db.close()
    
    return db_uids

def save_data(users):
    db = MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')

    cursor = db.cursor()
    for user in users:
        sqli = 'INSERT INTO RAW_USER(UID, NAME, GENDER, CREATED_AT, BI_FOLLOWERS_COUNT, PROVINCE, CITY ,LOCATION,\
        TAG, STATUSES_COUNT, FRIENDS_COUNT, FOLLOWERS_COUNT, POST_RATE, STATUSES) \
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        try:
            cursor.execute(sqli,(user['uid'], user['name'], user['gender'], user['created_at'],user['bi_followers_count'],user['province'], user['city'], user['location'],\
                                 user['tag'], user['statuses_count'], user['friends_count'], user['followers_count'], user['post_rate'], user['statuses']))
            db.commit()
        except Exception,e :
            print user['uid'] + ' : ' + str(e)
            db.rollback()
    db.close()
    
def integrate_db():  
    db= MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')
    
    cursor = db.cursor()
    sql_select_show = """SELECT * FROM RAW_USER_SHOW"""
    sql_select_tag = """SELECT * FROM RAW_USER_TAG"""
    sql_select_sr = """SELECT * FROM RAW_USER_SR"""
    
    try:
        cursor.execute(sql_select_show)
        results_show = {}
        for item in  cursor.fetchall():
            results_show[item[0]] = item
            
        cursor.execute(sql_select_tag)
        results_tag = {}
        for item in  cursor.fetchall():
            results_tag[item[0]] = item
        
        results_sr = {}
        cursor.execute(sql_select_sr)
        for item in  cursor.fetchall():
            results_sr[item[0]] = item
        
    except Exception,e :
        print e
        db.rollback()
    db.close()
    
    
    uid_show = []
    uid_tag = []
    uid_sr = []
    for key in results_show:
        uid_show.append(key)
    for key in results_tag:
        uid_tag.append(key) 
    for key in results_sr:
        uid_sr.append(key) 
    
    db_uids = get_db_uids()
    uids = [item for item in uid_show if item in uid_tag if item in uid_sr]
    print len(uids)
    temp_uids = list(set(uids) - set(db_uids)) 
    
    users = []
    for uid in temp_uids:
        user = {}
        user['uid'] = uid
        
        user_show = results_show[uid]
        user['name'] = user_show[1]
        user['gender'] = user_show[2]
        user['created_at'] = user_show[3]
        user['bi_followers_count'] = user_show[4]
        user['province'] = user_show[5]
        user['city'] = user_show[6]
        user['location'] = user_show[7]
        
        user['tag'] = results_tag[uid][1]
        
        user_sr = results_sr[uid]
        user['statuses_count'] = user_sr[1]
        user['friends_count'] = user_sr[2]
        user['followers_count'] = user_sr[3]
        user['post_rate'] = user_sr[4]
        user['statuses'] = user_sr[5]
        users.append(user)
    
    save_data(users)

def get_total_row_nums():
    db= MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')
    cursor = db.cursor()
    
    sql_select_user = """SELECT * FROM RAW_USER"""
    sql_select_show = """SELECT * FROM RAW_USER_SHOW"""
    sql_select_tag = """SELECT * FROM RAW_USER_TAG"""
    sql_select_sr = """SELECT * FROM RAW_USER_SR"""
    
    try:
        cursor.execute(sql_select_user)
        print 'raw_user : ' + str(len(cursor.fetchall()))
        
        cursor.execute(sql_select_show)
        print 'raw_user_show : ' + str(len(cursor.fetchall()))
        
        cursor.execute(sql_select_tag)
        print 'raw_user_tag : ' + str(len(cursor.fetchall()))
        
        cursor.execute(sql_select_sr)
        print 'raw_user_sr : ' + str(len(cursor.fetchall()))
    except Exception,e :
        print e
        db.rollback()
    db.close() 

def remove_inactive_user():
    db= MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')
    cursor = db.cursor()
    
    sql = "DELETE FROM RAW_USER WHERE POST_RATE = '-1'"
    try:
        cursor.execute(sql)
        db.commit()
    except Exception,e :
        print e
        db.rollback()
    db.close()            


def remove_no_tag_user():
    db= MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')
    cursor = db.cursor()
    
    sql = "DELETE FROM RAW_USER WHERE TAG = ' '"
    try:
        cursor.execute(sql)
        db.commit()
    except Exception,e :
        print e
        db.rollback()
    db.close()            

def remove_one_tag_user():
    db= MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')
    cursor = db.cursor()
    
    select_sql = """SELECT UID, TAG FROM RAW_USER"""
    delete_sql = "DELETE FROM RAW_USER WHERE UID = %s "
    uids = []
    try:
        cursor.execute(select_sql)
        for u in cursor.fetchall():
            if len(u[1].split()) == 1:
                uids.append(u[0])
        print uids
        for uid in uids:
            cursor.execute(delete_sql, (uid,)) 
        db.commit() 
    except Exception,e :
        print e
        db.rollback()
    db.close() 


def remove_no_location_user():
    db= MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')
    cursor = db.cursor()
    
    sql = "DELETE FROM RAW_USER WHERE PROVINCE = '100' OR PROVINCE = '400'"
    try:
        cursor.execute(sql)
        db.commit()
    except Exception,e :
        print e
        db.rollback()
    db.close()  
    
def get_final_uids():
    db = MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')
    cursor = db.cursor()
    
    sql_select_user = """SELECT UID FROM RAW_USER ORDER BY UID ASC"""
    final_uids = []
    try:
        cursor.execute(sql_select_user)
        for r in cursor.fetchall():
            final_uids.append(r[0])
        
    except Exception,e :
        print e
        db.rollback()
    db.close() 
    with open('../docs/final_uids.txt', 'w') as fout:
        for uid in final_uids:
            fout.write(uid + '\n')
    fout.close()

# init_raw_user_show()
# init_raw_user_tag()
# init_raw_user_sr()
# init_raw_user()
# integrate_db()
# get_total_row_nums()    #raw_user : 9599    raw_user_show : 11971    raw_user_tag : 12370    raw_user_sr : 11480
# remove_inactive_user()
# remove_no_tag_user()
# remove_no_location_user()
# remove_one_tag_user()
get_final_uids()



