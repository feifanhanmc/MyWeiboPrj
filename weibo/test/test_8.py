# -*- coding: utf-8 -*-

import json
from selenium import webdriver
import requests


def load_headers_data(filepath):
    with open(filepath, 'r') as fp:
        try:
            data = json.load(fp)
        except ValueError: 
            data = {}
    fp.close()
    return data 

# sr_headers = load_headers_data('../docs/sr_headers.json')
# url = 'http://weibo.cn/'
# r = requests.get(url)#, verify=False)
# print r.text.encode('utf8')


# driver = webdriver.Chrome()
# driver.get('https://passport.weibo.cn/signin/login')

#直接在浏览器输入my_url
my_url = 'http://weibo.cn/3195817110?page=1/?Cookie=_T_WM%3D67d4c28916ff862dfe962060fa3ab905%3B+gsid_CTandWM%3D4utCf1861mOx4FCoZH0CPgakb4l%3B+SUB%3D_2A251-sgkDeRhGeVG7lAY8yfOzTWIHXVXBOhsrDV6PUJbkdAKLRXhkW1uqo7DvFdO0fenKhJs0KHLnx-dXQ..&User-Agent=Mozilla%2F5.0+%28Windows+NT+10.0%3B+WOW64%3B+rv%3A51.0%29+Gecko%2F20100101+Firefox%2F51.0'

def test():
    cookies = {}
    cookies['_T_WM']='b002a9e8561a48401b2241b91230bb5f'; 
    cookies['ALF']='1495894406'; 
    cookies['SCF']='AgUCfv9QV6f1ZcKhyYWPuvBlm1MtgRZboilgVrZ_vdhdkNmTOgQKyrdM87nI4vuBf7VKEo0c8XYucRLwvu_IZ2c.'; 
    cookies['SUBP']='0033WrSXqPxfM725Ws9jqgMF55529P9D9WWwFJpbyaDecp-AduTj.ETW5JpX5o2p5NHD95QEe05cS0541hBNWs4Dqcj_i--ci-zEi-z0i--fiKy2iK.Ni--fiKnRiK.Ri--RiKn4i-iWi--fiKy2iKy8'; 
    cookies['SUB']='_2A250BY5HDeRhGeVG7lAY8yfOzTWIHXVXCRIPrDV6PUJbkdBeLU7RkW15hXeu5AXSTFbpc4GtDyll9aVH2A..'; 
    cookies['SUHB']='0LcSkl16XalaiS'; 
    cookies['SSOLoginState']='1493302807'
#     cookies['M_WEIBOCN_PARAMS']='luicode%3D20000174%26uicode%3D20000174'
    cookies['M_WEIBOCN_PARAMS']='luicode=20000174&uicode=20000174'
 
    cookies = [str(key) + '=' + str(value) for key, value in cookies.items()]
    cookies = '; '.join(cookies)

    headers = {}
    headers['Cookie'] = cookies
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'
    return headers
#     with open('../docs/sr_headers.json', 'w') as fout:
#         json.dump(headers, fout)
#     fout.close()


headers = test()
headers = load_headers_data('test_sr_headers.json')
print headers
url = 'http://weibo.cn/3195817110?page=1'
r = requests.get(url , params=headers, verify=False)
# r = requests.get(url , verify=False)
print r.url

