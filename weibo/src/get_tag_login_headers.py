# -*- coding: utf-8 -*-
import base64
import binascii
import json
import re
import requests
import rsa

class sina_login():
    
    def __init__(self):
        self.username = '13041233988'   #self.username = raw_input('Username : ')
        self.password = 'han8528520258' #self.password = raw_input('Password : ')
        self.login_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
        self.headers = {}
    
    def encode_username(self):
        return base64.encodestring(self.username)[:-1]
    
    def encode_password(self, servertime, nonce, pubkey):
        rsaPubkey = int(pubkey, 16)
        RSAKey = rsa.PublicKey(rsaPubkey, 65537) #创建公钥
        codeStr = str(servertime) + '\t' + str(nonce) + '\n' + str(self.password) #根据js拼接方式构造明文
        pwd = rsa.encrypt(codeStr, RSAKey)  #使用rsa进行加密
        return binascii.b2a_hex(pwd)  #将加密信息转换为16进制。

    def get_prelogin_info(self):
        url = r'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.18)'
        html = requests.get(url).text
        json_str = re.findall(r'\((\{.*?\})\)', html)[0]
        data = json.loads(json_str)
        servertime = data['servertime']
        nonce = data['nonce']
        pubkey = data['pubkey']
        rsakv = data['rsakv']
        return servertime, nonce, pubkey, rsakv
    
    def encode_post_data(self):
        servertime, nonce, pubkey, rsakv = self.get_prelogin_info()
        su = self.encode_username()
        sp = self.encode_password(servertime, nonce, pubkey)
        post_data = {
            'cdult': '3',
            'domain': 'sina.com.cn',
            'encoding': 'UTF-8',
            'entry': 'sso',
            'from': 'null',
            'gateway': '1',
            'nonce': nonce,
            'pagerefer':'',
            'prelt': '0',
            'pwencode': 'rsa2',
            'returntype': 'TEXT',
            'rsakv': rsakv,
            'savestate': '30',
            'servertime': servertime,
            'service': 'sso',
            'sp': sp,
            'sr': '1536*864',
            'su': su,
            'useticket': '0',
            'vsnf': '1'
        }
        return post_data
    
    def login(self):
        post_data = self.encode_post_data()
        session = requests.Session()
        response = session.post(self.login_url, data = post_data, verify=False)
#         response = session.post(self.login_url, data = post_data)
        response_data = json.loads(response.content.decode('gbk'))
        if response_data['retcode'] == '0':
            print 'Login success!'
            cookies = session.cookies.get_dict()
            cookies = [key + "=" + value for key, value in cookies.items()]
            cookies = "; ".join(cookies)
            self.headers['Cookie'] = cookies
        else:
            print 'Login Failed'

    def save_headers(self):
        with open('../docs/tag_headers.json', 'w') as fout:
            json.dump(self.headers, fout)
        fout.close()
    
if __name__ == '__main__':
    s = sina_login()
    s.login()
    s.save_headers()
    
