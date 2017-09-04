# -*- coding: utf-8 -*-

import json
import time

from selenium import webdriver          
from selenium.webdriver.common.keys import Keys   
from selenium.webdriver.support import ui


driver = webdriver.Chrome()   
wait = ui.WebDriverWait(driver,10)

my_users = []
my_users.append(('15876409741','8u9ab7obz'))
my_users.append(('18873454820','han123321'))
my_users.append(('13650289916','8ugrgoe88'))
my_users.append(('14773439455','8v196t4mq'))
my_users.append(('15876425150','8v7g4uz7'))
my_users.append(('15220317740','8vmlq3oij'))
my_users.append(('18219275020','8vu9a7y51'))
my_users.append(('17008954526','8wgh41ao4'))
my_users.append(('17008950683','8wu5weagw'))
my_users.append(('15876475369','8x6ysyqll'))
my_users.append(('18473483566','8x86y6sw6'))
my_users.append(('17184957481','8xf3ghut2'))

for index in range(len(my_users)):
    try:
        driver.get("https://passport.weibo.cn/signin/login")
        time.sleep(3)
        elem_user = driver.find_element_by_id('loginName')
        elem_user.send_keys(my_users[index][0])
        elem_pwd = driver.find_element_by_id('loginPassword')
        elem_pwd.send_keys(my_users[index][1])
        
        elem_pwd.send_keys(Keys.ENTER)  
        
        time.sleep(20)  
        cookies = {}
        for c in driver.get_cookies():
            cookies[c['name']] = c['value']
    
        cookies = [str(key) + '=' + str(value) for key, value in cookies.items()]
        cookies = '; '.join(cookies)
    
        headers = {}
        headers['Cookie'] = cookies
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'
        with open('../docs/sr_headers/sr_headers_' + str(index) + '.json', 'w') as fout:
            json.dump(headers, fout)
        fout.close()
        time.sleep(2)
    except Exception,e:        
        print "Error: ",e  

driver.close()