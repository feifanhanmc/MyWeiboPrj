# coding: utf-8
import requests
import json
import base64
def login(username, password):
    username = base64.b64encode(username.encode('utf-8')).decode('utf-8')
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
    loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    session = requests.Session()
    res = session.post(loginURL, data = postData)
    jsonStr = res.content.decode('gbk')
    info = json.loads(jsonStr)
    print info
    if info["retcode"] == "0":
        print("登录成功")
        # 把cookies添加到headers中，必须写这一步，否则后面调用API失败
        weibo_com_session = requests.Session()
        ret = weibo_com_session.get(info['crossDomainUrlList'][0])
        print ret.content
        cookies = ret.cookies.get_dict('.weibo.com', '/')
        cookies = [key + "=" + value for key, value in cookies.items()]
        cookies = "; ".join(cookies)
        print cookies
    else:
        print("登录失败，原因： %s" % info["reason"])
    return session
if __name__ == '__main__':
    session = login('13041233988', 'han8528520258')