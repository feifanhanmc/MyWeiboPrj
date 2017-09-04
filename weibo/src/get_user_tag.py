# -*- coding: utf-8 -*-
import json
import re
import urllib
import urllib2

import MySQLdb


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
    db = MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')

    cursor = db.cursor()
    sql = 'SELECT UID  FROM RAW_USER_TAG'
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
 
def get_user_tag(uid, headers_data):
    tag =  ''
    url = 'http://weibo.com/' + uid + '/info'
    
    try:
        req = urllib2.Request(url, headers = headers_data)
        html = urllib2.urlopen(req).read()
        
#         print req.get_full_url()
#         print url + '?' + urllib.urlencode(headers_data)
#         http://weibo.com/1686731963/info?Cookie=SUB%3D_2A250BML1DeRhGeVG7lAY8yfOzTWIHXVXc7M9rDV_PUNbm9BeLVn5kW-VFI5xeqY9YHogTE_yZ2Sjxs2V7Q..%3B+SUBP%3D0033WrSXqPxfM725Ws9jqgMF55529P9D9WWDiKTb6OizVrvnWIXaHhoh5NHD95Q01h-E1Ke4eoq4Ws4DqcjJi--Xi-i2i-27i--4iKLsi-24i--fi-2Xi-2Ni--NiKnRi-zNwLQt%3B+ALF%3D1524753958%3B+SCF%3DAm6DtC65WFoDkjQjTkUOuQWzMt_X4h6Va_c8aPK3uz_7QFK6nQQyY7fK96boQ-DQvSo8DJV4N5KJAswuOGsgteI.%3B+ALC%3Dac%253D0%2526bt%253D1493217958%2526cv%253D5.0%2526et%253D1524753958%2526scf%253D%2526uid%253D3852939269%2526vf%253D0%2526vs%253D0%2526vt%253D0%2526es%253D7271b1949c4c7f935ce60c051b7fa8d7%3B+sso_info%3Dv02m6alo5qztKWRk5ClkKSQpZCTgKWRk6SljpSYpZCTpKWRk5SlkJOQpZCTnKWRk5yljoOgpZCjnbqWopm1mpaQvYyzoLWMo6SzjpOIto6QwMA%3D%3B+tgc%3DTGT-Mzg1MjkzOTI2OQ%3D%3D-1493217957-gz-FE3DA37FD446F311C9163FB3EE50BB51-1%3B+LT%3D1493217958

        t1 =  re.findall('"ns":"","domid":"Pl_Official_PersonalInfo__5(.*)', html, flags = 0)[0]
        t2 = re.findall('S_line3(.*)</script>', t1, flags = re.M)[0]
        t3 = re.findall('/span>(.*?)/a>', t2, flags = re.M)
        
        for item in t3:
            tag += item.replace('\\r\\n\\t\\t\\t\\t\\t\\t\\t\\t', '').replace('\\t\\t\\t\\t\\t\\t\\t\\t<\\', '') + ' '
        return tag
    except Exception,e:
        if hasattr(e, 'code'):
            # HTTP Error 501: Not Implemented     HTTP Error 414: Request-URI Too Large
            return False
        print uid + ' : ' + str(e)
        return ' '

def init():
    headers_data = load_headers_data('../docs/tag_headers.json')
    uids = get_uids()
    db_uids = get_db_uids()
    temp_uids = list(set(uids) - set(db_uids)) 
    return temp_uids, headers_data


def save_data(users):
    db= MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')

    cursor = db.cursor()
    for user in users:
        sqli = 'INSERT INTO RAW_USER_TAG(UID, TAG) \
                                VALUES(%s, %s)'
        try:
            cursor.execute(sqli,(user['uid'], user['tag']))
            db.commit()
        except Exception,e :
            print e
            db.rollback()
    db.close()
    
users_tag = []
temp_uids, headers_data = init() 
for uid in temp_uids:
    user_tag = {}
    user_tag['uid'] = str(uid)
    result = get_user_tag(uid, headers_data)
    if not result:
        print u'服务器错误,等会儿再试'
        break
    else:
        user_tag['tag'] = result
    users_tag.append(user_tag)

save_data(users_tag)