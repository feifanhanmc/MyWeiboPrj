# -*- coding: utf-8 -*-

import json
import re
import urllib2
import MySQLdb
from bs4 import BeautifulSoup

def load_headers_data(filepath):
    with open(filepath, 'r') as fp:
        try:
            data = json.load(fp)
        except ValueError: 
            data = {}
    fp.close()
    return data 

def get_uids():
    uids = []
    with open('../docs/uids.txt') as fp:
        for line in fp:
            uids.append(line.strip())
    fp.close()
    return uids

def get_db_uids():
    db_uids = []
    db = MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj', charset="utf8")
    db.set_character_set('utf8')
    
    cursor = db.cursor()
    sql = 'SELECT UID  FROM RAW_USER_SR'
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

def get_user_sr(uid, sr_headers):
    user_sr = {}
    user_sr['uid'] = uid
    user_sr['statuses'] =  ''

    try:
        
        index = 1
        original_num = 0
        post_num = 0
        while (index != -1) and (index <= 3):
            print 'index : ' + str(index)
              
            url = 'http://weibo.cn/' + str(uid) + '?page=' + str(index)
            req = urllib2.Request(url, headers = sr_headers)
            html = urllib2.urlopen(req).read()
            soup =BeautifulSoup(html, 'lxml')
            
            #解析微博数、粉丝数、关注数
            if index == 1:
                t1 = soup.select('.tip2')[0].contents
                user_sr['statuses_count'] =  str(re.findall('(\d*)', t1[0].string)[3])  #微博
                user_sr['friends_count'] = str(re.findall('(\d*)', t1[2].string)[3])  #关注
                user_sr['followers_count'] =  str(re.findall('(\d*)', t1[4].string)[3])  #粉丝
            
            #解析微博文本
            t2 = soup.select('.c')[1:]  #第一项没用（手机微博触屏版,点击前往）
            t2 = t2[:-2]    #最后两项没用,是页面上的一些设置信息（设置:皮肤.图片.条数.隐私  彩版|触屏|语音）
            
            for item in t2:
                text = emoji_re.sub(r'[EMOJI]', item.text)
                time = item.select('.ct')[0].text.encode('utf8').split()[0]
                if '-' in time:     #'2015-08-26'
                    index = -1
                    break
                elif ( '月' in time ) and ( int(time[0:2]) < 3 ) :   #'04月16日'    #收集今年三月份以后的微博
                    index = -1
                    break
                else:
                    user_sr['statuses'] += text
                        
                    if item.select('.cmt'):
                        post_num += 1
                    else:
                        original_num += 1
            
            if len(t2) < 10:
                index = -1
                         
            if index != -1 :
                index = index + 1         
        if (post_num + original_num) == 0:
            user_sr['post_rate'] = -1
        else:
            user_sr['post_rate'] = '%0.4f' % (float(post_num) / float(post_num + original_num))
        return user_sr
    except Exception,e:
        print uid + ' : ' + str(e)
        return False

def init():
    uids = get_uids()
    db_uids = get_db_uids()
    temp_uids = list(set(uids) - set(db_uids))
    sr_headers = load_headers_data('../docs/sr_headers.json')
    return temp_uids, sr_headers
    
def save_data(users):
    db = MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')

    cursor = db.cursor()
    for user in users:
        sqli = 'INSERT INTO RAW_USER_SR(UID, STATUSES_COUNT, FRIENDS_COUNT, FOLLOWERS_COUNT, POST_RATE, STATUSES) VALUES(%s, %s, %s, %s, %s, %s)'
        try:
            cursor.execute(sqli,(user['uid'], user['statuses_count'], user['friends_count'], user['followers_count'], user['post_rate'], user['statuses']))
            db.commit()
        except Exception,e :
            print user['uid'] + ' : ' + str(e)
            db.rollback()
    db.close()


emoji_re = re.compile(u'('
    u'\ud83c[\udf00-\udfff]|'
    u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
    u'[\u2600-\u26FF\u2700-\u27BF])+', 
    re.UNICODE)

users_sr = []    
temp_uids, sr_headers = init()
temp_uids = ['3195817110']
for uid in temp_uids:
    print uid
    result = get_user_sr(uid, sr_headers)
    if not result:
        break
    else:
        users_sr.append(result)
        
print users_sr    
# save_data(users_sr)

