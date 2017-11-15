# -*- coding: utf-8 -*-

import json

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from weibo import APIClient

class ApiClient():
    def __init__(self, APP_INFO, index):
        self.index = index
        self.username = '*********'
        self.password = '*********'        
        self.CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'        

        self.APP_KEY = APP_INFO[0]
        self.APP_SECRET = APP_INFO[1] 


        
        self.client = APIClient(app_key = self.APP_KEY, app_secret = self.APP_SECRET, redirect_uri = self.CALLBACK_URL)
        self.set_access_token()
        
    def set_access_token(self):
        '''登陆'''
        driver = webdriver.Chrome()
        driver.get(self.client.get_authorize_url())
        username_element = driver.find_element_by_id('userId')
        username_element.clear()
        username_element.send_keys(self.username)
        password_element = driver.find_element_by_id('passwd')
        password_element.send_keys(self.password)
        driver.find_element_by_class_name('oauth_login_form').submit()
        '''授权并解析得到code,这部分本来想继续用selenium操作浏览器，以自动获取access_token，但是这种方法太不稳定了，所幸手动获取'''
        try:
#             WebDriverWait(driver, 10).until(EC.title_is(u'微博'))
            WebDriverWait(driver, 5)
            code = str(raw_input('Input the code in the current url : '))
        except Exception,e:
            print e
        finally:
            driver.close()
        '''设置access_token'''
        r = self.client.request_access_token(code)
        self.client.set_access_token(r.access_token, r.expires_in)
    
    def save_client(self):
        client = {
            'access_token': self.client.access_token,
            'APP_KEY': self.APP_KEY,
            'APP_SECRET': self.APP_SECRET,
            'CALLBACK_URL': self.CALLBACK_URL
        }
        with open('../docs/client/client_' + str(self.index) + '.json', 'w') as fout:
            json.dump(client, fout)
        fout.close()
        
if __name__ == '__main__':  
    APPS_INFO = []
    APPS_INFO.append(('1662499124','2e2813ca656f7e5e802af260f22f97d0' ))
    APPS_INFO.append(('1626843849','67885717e11e487d91ba3786ca8a79e0' ))
    APPS_INFO.append(('4164980443','22b8a631b8422e6f5082b195f3d94e3c' ))
    APPS_INFO.append(('2463094762','47ec3b6d0f616eabd59b55323a8291a6' ))
    APPS_INFO.append(('1521911455','2b7b86bc07668f17697a6c7f9f828f00' ))
    APPS_INFO.append(('3397568816','bce317fe6e746c34b1b8193ba083b462' ))
    APPS_INFO.append(('1477388327','514671d643ae6289d503eefc4c38f3f8' ))
    APPS_INFO.append(('1548704306','4a5e0870ffc475e38918f048f924daca' ))
    APPS_INFO.append(('1772462163','4583c955ce5a56968b2a8885255df45b' ))
    APPS_INFO.append(('4285217320','5abe1831d71a6a97dbc7d4aeddd09bcb' ))
    
    
    
    for index in range(len(APPS_INFO)):
        u = ApiClient(APPS_INFO[index], index)
        u.save_client()
