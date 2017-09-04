# -*- coding: utf-8 -*-
import json
import time
import urllib2
import re
import MySQLdb
from weibo import APIClient


class WeiboUser():
    
    def __init__(self, uid, headers_data, client, client_access_token):
        self.uid = uid
        self.headers = headers_data
        self.client = client
        self.client_access_token = client_access_token
        self.user = {'uid': str(self.uid)}
        

    def get_user_data(self):
        self.get_user_show()
#         self.get_user_timeline()
#         self.get_friendships_friends_ids()
        self.get_user_tag()

    def get_user_show(self):
        try:
            user_show =  self.client.users.show.get(access_token = self.client_access_token, uid = self.uid)
            self.user['name'] = user_show['name'].encode('utf-8')
            self.user['gender'] = user_show['gender'].encode('utf-8')
            self.user['description'] = user_show['description']
            self.user['created_at'] = time.mktime(time.strptime(user_show['created_at'].replace('+0800 ', ''),"%a %b %d %H:%M:%S %Y"))
            
            self.user['statuses_count'] = user_show['statuses_count']
            self.user['friends_count'] = user_show['friends_count']#关注数
            self.user['followers_count'] = user_show['followers_count']#粉丝数
            self.user['bi_followers_count'] = user_show['bi_followers_count'] 
            
            self.user['province'] = user_show['province'].encode('utf-8')
            self.user['city'] = user_show['city'].encode('utf-8')
            self.user['location'] = user_show['location'].encode('utf-8')
        except Exception,e:
            print e
            bad_uids.append(self.uid)

        
    
    def get_friendships_friends_ids(self):
        #目前查看他人关注/粉丝列表，系统仅支持展示前5页.
        '''
        url = 'http://weibo.com/2022580163/follow'
        req = urllib2.Request(url, headers = self.headers)
        html = urllib2.urlopen(req).read()
        
        uids_raw = re.findall('uid=(\d{10})', html, re.M)
        uids = list(set(uids_raw))
        '''
        
    def get_user_timeline(self):
        return 
    
    def get_user_tag(self):
        self.user['tag'] = ''
        if self.uid not in bad_uids:
            url = 'http://weibo.com/' + self.uid + '/info'
            req = urllib2.Request(url, headers = self.headers)
            html = urllib2.urlopen(req).read()
            try:
                t1 =  re.findall('"ns":"","domid":"Pl_Official_PersonalInfo__5(.*)', html, flags = 0)[0]
                t2 = re.findall('S_line3(.*)</script>', t1, flags = re.M)[0]
                t3 = re.findall('/span>(.*?)/a>', t2, flags = re.M)
                for item in t3:
                    self.user['tag'] += item.replace('\\r\\n\\t\\t\\t\\t\\t\\t\\t\\t', '').replace('\\t\\t\\t\\t\\t\\t\\t\\t<\\', '') + ' '
            except Exception,e:
                print e
        print self.user['tag']
    
def save_data(users):
    db= MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')

    cursor = db.cursor()
    for user in users:
        sqli = 'INSERT INTO USER(UID, NAME, GENDER, DESCRIPTION, CREATED_AT, \
                                STATUSES_COUNT, FRIENDS_COUNT, FOLLOWERS_COUNT, BI_FOLLOWERS_COUNT, \
                                PROVINCE, CITY ,LOCATION, TAG) \
                                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        try:
            cursor.execute(sqli,(user['uid'], user['name'], user['gender'], user['description'], user['created_at'], \
                                user['statuses_count'], user['friends_count'], user['followers_count'], user['bi_followers_count'],\
                                user['province'], user['city'], user['location'], user['tag']))
            db.commit()
        except Exception,e :
            print e
            db.rollback()
    db.close()

    
def get_raw_uids():
    raw_uids = []
    with open('../docs/raw_uids.txt') as fp:
        for line in fp:
            raw_uids.append(line.strip())
    return raw_uids

def save_uids(filename, uids):
    with open(filename, 'w') as fout:
        for uid in uids:
            fout.write(uid + '\n')
    fout.close()

def load_headers_or_client_data(filepath):
    with open(filepath, 'r') as fp:
        try:
            data = json.load(fp)
        except ValueError: 
            data = {}
    fp.close()
    return data    

def init():
    raw_uids = get_raw_uids()
    headers_data = load_headers_or_client_data('../docs/headers.json')
    client_data = load_headers_or_client_data('../docs/client.json')
    client = APIClient( app_key = client_data['APP_KEY'], app_secret = client_data['APP_SECRET'], redirect_uri = client_data['CALLBACK_URL'])
    client_access_token = client_data['access_token']
    return raw_uids, headers_data, client, client_access_token

if __name__ == '__main__':
    users = []
    bad_uids = []
    raw_uids, headers_data, client, client_access_token = init()
    for uid in raw_uids:
        u = WeiboUser(uid, headers_data, client, client_access_token)
        u.get_user_data()
        if not uid in bad_uids:
            users.append(u.user)
    uids = list(set(raw_uids) - set(bad_uids))
    save_uids('../docs/uids.txt', uids)        
    save_data(users)

