# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re

soup = BeautifulSoup(open('test_1.html'), 'lxml')




t1 = soup.select('.tip2')[0].contents
print re.findall('(\d*)', t1[0].string)[3]  #微博
print re.findall('(\d*)', t1[2].string)[3]  #关注
print re.findall('(\d*)', t1[4].string)[3]  #粉丝



t2 = soup.select('.c')[:-2]  #最后两项没用,是页面上的一些设置信息（设置:皮肤.图片.条数.隐私  彩版|触屏|语音）
original_num = 0
post_num = 0
for item in t2:
#     print item.text
    r = item.select('.ct')[0].text.encode('utf8')
    time = r.split()[0]
#     if time.

L = ['2015-08-26', '今天', '04月16日']
for l in L:
    if '-' in l:
        print '-'
    elif '今天' in l:
        print '今天'
    elif '月' in l:
        print l[0:2]
        if int(l[0:2]) > 3:
            print 'aaa'
            




