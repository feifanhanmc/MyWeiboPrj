# -*- coding: utf-8 -*-
import json
import time

import MySQLdb
from weibo import APIClient


class WeiboUser():
    
    def __init__(self, uid, client, client_access_token):
        self.uid = uid
        self.client = client
        self.client_access_token = client_access_token
        self.user = {'uid': str(self.uid)}
        
    def get_user_show(self):
        try:
            user_show =  self.client.users.show.get(access_token = self.client_access_token, uid = self.uid)
            self.user['name'] = user_show['name'].encode('utf-8')
            self.user['gender'] = user_show['gender'].encode('utf-8')
            self.user['created_at'] = time.mktime(time.strptime(user_show['created_at'].replace('+0800 ', ''),"%a %b %d %H:%M:%S %Y"))

            self.user['bi_followers_count'] = user_show['bi_followers_count'] 
            
            self.user['province'] = user_show['province'].encode('utf-8')
            self.user['city'] = user_show['city'].encode('utf-8')
            self.user['location'] = user_show['location'].encode('utf-8')
            return True
        except Exception,e:
            print self.uid + ' : ' + str(e)
            return False
            
            
def get_uids():
    uids = []
    with open('../docs/uids.txt') as fp:
        for line in fp:
            uids.append(line.strip())
    fp.close()
    return uids

def get_db_uids():
    db_uids = []
    db = MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')

    cursor = db.cursor()
    sql = 'SELECT UID  FROM RAW_USER_SHOW'
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

def load_client_data(filepath):
    with open(filepath, 'r') as fp:
        try:
            data = json.load(fp)
        except ValueError: 
            data = {}
    fp.close()
    return data
  
def init(index):
    uids = get_uids()
    db_uids = get_db_uids()
    temp_uids = list(set(uids) - set(db_uids))
    client_data = load_client_data('../docs/client/client_' + str(index) + '.json')
    client = APIClient( app_key = client_data['APP_KEY'], app_secret = client_data['APP_SECRET'], redirect_uri = client_data['CALLBACK_URL'])
    client_access_token = client_data['access_token']
    return temp_uids, client, client_access_token
            
def save_data(users):
    db= MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')

    cursor = db.cursor()
    for user in users:
        sqli = 'INSERT INTO RAW_USER_SHOW(UID, NAME, GENDER, CREATED_AT, BI_FOLLOWERS_COUNT, PROVINCE, CITY ,LOCATION) \
                                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
        try:
            cursor.execute(sqli,(user['uid'], user['name'], user['gender'], user['created_at'],user['bi_followers_count'],\
                                user['province'], user['city'], user['location']))
            db.commit()
        except Exception,e :
            print e
            db.rollback()
    db.close()
 

   
users_show = []
i = 0
for index in range(10):
    print 'index : ' + str(index)
    temp_uids, client, client_access_token = init(index)
    for uid in temp_uids[i:]:
        u = WeiboUser(uid, client, client_access_token)
        if u.get_user_show():
            users_show.append(u.user)
        else:
            break
        i = i + 1
    
save_data(users_show)

