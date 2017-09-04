# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import title_is
from selenium.webdriver.support.ui import WebDriverWait


def login(username, password, driver):
    login_url = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    locator = (By.CLASS_NAME, 'me_name')

    try:
        driver.get(login_url)
        login_name_element = driver.find_element_by_id('username')
        login_name_element.send_keys(username)
        login_password_element = driver.find_element_by_id('password')
        login_password_element.send_keys(password)
        login_password_element.send_keys(Keys.RETURN)
        WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator), 'Login FAILED.')
        print 'Login SUCCEEDED.'
    except Exception,e:
        print e
    
def load_user_html(uids, driver):
    print 'Loading htmls...'
    count = 0
    user_html = []
    uids_succeed = []
    locator = (By.CLASS_NAME, 'username')
    for uid in uids:
        try:
            driver.get('http://weibo.com/' + uid + '/info')
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator), 'Load html<%d>  FAILED.' % count)
            html = (driver.page_source).encode('utf8')
            user_html.append(html)
            uids_succeed.append(uid)
            print 'Load html<%d>  SUCCEEDED.' % count
        except Exception,e:
            print e
        count = count + 1
    return user_html, uids_succeed
    
def write_to_file(user_html, uids_succeed):
    print 'Writting files...'
    count = 0
    with open('../../docs/uids_succeed.txt', 'w') as fout_uid:
        for uid in uids_succeed:
            fout_uid.write(uid + '\n')
    for html in user_html:
        with open('../../docs/user_html/' + uids_succeed[count] + '.txt', 'w') as fout:
            fout.writelines(html)
            fout.close()
            print count
            count = count + 1
    
def main():
    username = '13041233988'
    password = 'han8528520258'
    driver = webdriver.Firefox()
    login(username, password, driver)
    uids = []
    with open('../../docs/uids.csv', 'r') as fp:
        for line in fp:
            uids.append(str(line.strip()))
    user_html, uids_succeed = load_user_html(uids, driver)
    write_to_file(user_html, uids_succeed) 
    print 'Done'
    driver.close()

if __name__ =='__main__':
    main()