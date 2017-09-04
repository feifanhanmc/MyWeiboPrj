# -*- coding: utf-8 -*-


'''准备公共数据'''

import json
import os
import re
import urllib2

from bs4 import BeautifulSoup


def load_uids(filepath):
    uids = []
    with open(filepath) as fp:
        for line in fp:
            uid = str(line.strip())
            uids.append(uid)
    fp.close()
    return uids

def load_headers(filepath):
    with open(filepath, 'r') as fp:
        try:
            headers = json.load(fp)
        except ValueError: 
            headers = {}
    fp.close()
    return headers

'''main'''
def main():
    uids = load_uids('../../docs/uid.txt')
    headers = load_headers('../../docs/headres.json')
    userdata = []
    for uid in uids:
        u = user(uid, headers)
        userdata.append(u.get_user_data()) 
    print userdata
    
'''user类'''
class user():
    def __init__(self, uid, headers):
        self.headers = headers
        self.uid = uid
        self.username = ''
    
    def get_user_data(self):
#         self.load_user_tweets()
        self.load_user_info()
        
        data = {'username': self.username}
        return data
    
    def load_user_info(self):
        url = 'http://weibo.com/' + self.uid + '/info'
        req = urllib2.Request(url, headers = self.headers)
        html = urllib2.urlopen(req).read()
        self.prase_user_info(html)
        print html
    
    def prase_user_info(self, html):
        soup = BeautifulSoup(html, 'lxml')
        self.username = ''#soup.h1.string.strip()
    
    def output(self, content, out_path, save_mode="w"):
        prefix = os.path.dirname(out_path)
        if not os.path.exists(prefix):
            os.makedirs(prefix)
        fout = open(out_path, save_mode)
        fout.write(content)
        fout.close()
        
def get_friendships_friends_ids(friends_count):
    headers = load_headers('../../docs/headres.json')
    url = 'http://weibo.com/2022580163/follow'
    req = urllib2.Request(url, headers =headers)
    html = urllib2.urlopen(req).read()
    
    uids_raw = re.findall('uid=(\d{10})', html, re.M)
    uids = list(set(uids_raw))
    print uids
    print len(uids)
    
if __name__ == '__main__':
    get_friendships_friends_ids