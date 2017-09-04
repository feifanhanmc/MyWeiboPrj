# -*- coding: utf-8 -*-

import json
import time   

from selenium import webdriver          
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui     


driver = webdriver.Chrome()   
wait = ui.WebDriverWait(driver,10)

username = 'henanliuyihua@sina.cn'
password = 'iloveU0201' 
 
try:
    driver.get("https://passport.weibo.cn/signin/login")  
    
    time.sleep(3)
    elem_user = driver.find_element_by_id('loginName')
    elem_user.send_keys(username)
    elem_pwd = driver.find_element_by_id('loginPassword')
    elem_pwd.send_keys(password)
    elem_pwd.send_keys(Keys.ENTER)
    #重点: 暂停时间输入验证码  
#     time.sleep(20)  
           
#     elem_sub = driver.find_element_by_name("submit")  
#     elem_sub.click()              #点击登陆  
    time.sleep(2)  
    cookies = {}
    for c in driver.get_cookies():
        cookies[c['name']] = c['value']

    cookies = [str(key) + '=' + str(value) for key, value in cookies.items()]
    cookies = '; '.join(cookies)

    headers = {}
    headers['Cookie'] = cookies
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'
    print headers
    with open('test_sr_headers.json', 'w') as fout:
        json.dump(headers, fout)
    fout.close()
except Exception,e:        
    print "Error: ",e  
finally:      
    print u'End LoginWeibo!\n\n' 
#     driver.close()