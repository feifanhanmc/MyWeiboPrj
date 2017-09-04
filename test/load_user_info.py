# -*- coding: utf-8 -*-
import base64
import json

import requests


class load_user_info:
    
    def __init__(self):
        self.cookies = []
        self.username = '13041233988'
        self.password = 'han8528520258'
        
    def login_get_cookie(self):
        username = base64.b64encode(self.username.encode('utf-8')).decode('utf-8')
        password = self.password
        login_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
        postData = {
            'entry': 'sso',
            'gateway': '1',
            'from': 'null',
            'savestate': '30',
            'userticket': '0',
            'pagerefer': '',
            'vsnf': '1',
            'su': username,
            'service': 'sso',
            'sp': password,
            'sr': '1440*900',
            'encoding': 'UTF-8',
            'cdult': '3',
            'domain': 'sina.com.cn',
            'prelt': '0',
            'returntype': 'TEXT',
        }
        session = requests.Session()
        print session.cookies
        response = session.post(login_url, data = postData)
        
        print session.cookies
        jsonStr = response.content.decode('gbk')
        info = json.loads(jsonStr)
        if info['retcode'] == '0':
            print'登陆成功'
            # 把cookies添加到headers中，必须写这一步，否则后面调用API失败
            weibo_com_session = requests.Session()
            ret = weibo_com_session.get(info['crossDomainUrlList'][0])
#             print ret.content
            cookies = ret.cookies.get_dict('.weibo.com', '/')
            cookies = [key + '=' + value for key, value in cookies.items()]
            cookies = '; '.join(cookies)
            
            self.cookies = cookies
            
            print cookies
        else:
            print '登录失败，原因： %s' % info['reason']
        return session
    
    def load_info(self):
        url = 'http://weibo.com/1669879400/info'
        r = requests.get(url).content
#         print r
#         print r.text.encode('utf-8').decode('gbk')
m = load_user_info()
m.login_get_cookie()
# print '111' + m.cookies
m.load_info()
