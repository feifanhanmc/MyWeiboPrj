# -*- coding: utf-8 -*-
import json
from weibo import APIClient


class WeiboUser():
    
    def __init__(self, uid, client, client_access_token):
        self.uid = uid
        self.client = client
        self.client_access_token = client_access_token
        
    def test(self):
        try:
            self.client.users.show.get(access_token = self.client_access_token, uid = self.uid)
            return 2
        except Exception,e:
            print e
            if str(e) == 'APIError: 10023: User requests out of rate limit!, request: /2/users/show.json':
                return 1
            else: 
                return 0
            
def get_raw_uids():
    raw_uids = []
    with open('../docs/raw_uids.txt') as fp:
        for line in fp:
            raw_uids.append(line.strip())
    fp.close()
    return raw_uids

def load_client_data(filepath):
    with open(filepath, 'r') as fp:
        try:
            data = json.load(fp)
        except ValueError: 
            data = {}
    fp.close()
    return data
  
def init(index):
    raw_uids = get_raw_uids()
    client_data = load_client_data('../docs/client/client_' + str(index) +'.json')
    client = APIClient( app_key = client_data['APP_KEY'], app_secret = client_data['APP_SECRET'], redirect_uri = client_data['CALLBACK_URL'])
    client_access_token = client_data['access_token']
    return raw_uids, client, client_access_token

i = 12525
bad_uids = []
for index in range(10):
    print 'index : ' + str(index)
    raw_uids, client, client_access_token = init(index)
    for uid in raw_uids[i:]:
        u = WeiboUser(uid, client, client_access_token)
        flag = u.test()
        if flag == 0:
            bad_uids.append(uid)
        elif flag == 1:
            break
        i = i + 1
        
print 'i : ' + str(i)

with open('../docs/bad_uids.txt', 'a+') as fout:
    for bad_uid in bad_uids:
        fout.write(bad_uid + '\n')
fout.close()



