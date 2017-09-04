# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup


soup = BeautifulSoup(open('../docs/user_html/1785235045.txt'),'lxml')
print soup.prettify()
print soup.h1
print soup.h1.string.strip()
# print soup.select('.username')[0].string.strip()
print soup.select('.pf_intro')[0].string.strip()
print soup.select('.W_f18')[0].string.strip()
print soup.select('.W_f18')[1].string.strip()
print soup.select('.W_f18')[2].string.strip()

badge_item_pattern = re.compile('.*alt="(.*)".*height.*medalcard="(\d*)".*', flags = 0)
for badge_item in  soup.select('.bagde_item'):
    print badge_item_pattern.findall(str(badge_item.img))[0][0],badge_item_pattern.findall(str(badge_item.img))[0][1]
    
    
level_info = soup.select('.level_info')[0].select('.info')
# print level_info
# for info in level_info:
#     print info.select('.S_txt1')[0].string.strip()
print (soup.select('.level_info')[0].select('.info'))[1].select('.S_txt1')[0].string.strip()


base_info = soup.select('.WB_innerwrap')
for li in  base_info[6].find_all('li'):
    for span in  li.find_all('span'):
        print span.string.strip()

a_pattern = re.compile('.*span>((?:.|\n)*?)(.*)((?:.|\n)*?)</a>', re.M)
for a in base_info[7].find_all('a'):
    a_content = a_pattern.findall(str(a))[0]
    print a_content[2].strip()


