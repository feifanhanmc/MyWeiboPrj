# -*- coding: utf-8 -*-

from weibo import APIClient
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ApiClient():
    def __init__(self):
        self.APP_KEY = '1662499124'
        self.APP_SECRET = '2e2813ca656f7e5e802af260f22f97d0'  
        self.CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
        self.client = APIClient(app_key = self.APP_KEY, app_secret = self.APP_SECRET, redirect_uri = self.CALLBACK_URL)
        self.set_access_token()
        
    def set_access_token(self):
        '''登陆'''
        driver = webdriver.Chrome()
        driver.get(self.client.get_authorize_url())
        username_element = driver.find_element_by_id('userId')
        username_element.clear()
        username_element.send_keys('13041233988')
        password_element = driver.find_element_by_id('passwd')
        password_element.send_keys('han8528520258')
        driver.find_element_by_class_name('oauth_login_form').submit()
        '''授权并解析得到code,这部分本来想继续用selenium操作浏览器，以自动获取access_token，但是这种方法太不稳定了，所幸手动获取'''
        try:
            WebDriverWait(driver, 10).until(EC.title_is(u'微博'))
            code = str(raw_input('Input the code in the current url : '))
        except Exception,e:
            print e
        finally:
            driver.close()
        '''设置access_token'''
        r = self.client.request_access_token(code)
        self.client.set_access_token(r.access_token, r.expires_in)
    
    def get_client(self):
        return self.client
    
    def get_user_data(self):
        user_data = []
        
        return user_data
    
    def get_user_counts(self):
        return
    
    def test(self):
        uid = 2022580163
        user_show =  self.client.users.show.get(uid = uid)
        print user_show
        
if __name__ == '__main__':     
    u = ApiClient()
    u.get_user_data()
    u.test()
