# -*- coding: utf-8 -*-

import json
from weibo import APIClient
import requests

class WeiboUser():
    
    def __init__(self, uid, client, client_access_token):
        self.uid = uid
        self.client = client
        self.client_access_token = client_access_token
        
    def test(self):
        try:
            url = 'http://i2.api.weibo.com/2/darwin/platform/user/user_by_relation.json'
            data = {}
            data['access_token'] = self.client_access_token
            data['uid'] = self.uid
            data['relation_type'] = 'school'
            r = requests.get(url, data)
            print r
#             i2.api.weibo.com/2/darwin/platform/user/user_by_relation.json?access_token=2.00lVXkMEAyfVoB99a5ffec2epwLmqB&uid=3852939269&relation_type=school
            
            
#             print self.client.darwin.platform.user.user_by_relation.get(access_token = self.client_access_token, uid = self.uid, relation_type = 'school')
        except Exception,e:
            print e
            

def load_client_data(filepath):
    with open(filepath, 'r') as fp:
        try:
            data = json.load(fp)
        except ValueError: 
            data = {}
    fp.close()
    return data
  
def init(index):
    client_data = load_client_data('../docs/client/client_' + str(index) +'.json')
    client = APIClient( app_key = client_data['APP_KEY'], app_secret = client_data['APP_SECRET'], redirect_uri = client_data['CALLBACK_URL'])
    client_access_token = client_data['access_token']
    return client, client_access_token



index = 0  #输入不同值运用相应的应用数据[0,6]
uid = '3852939269'
client, client_access_token = init(index)

u = WeiboUser(uid, client, client_access_token)
u.test()

