import urllib2
import json
from bs4 import BeautifulSoup
import re

url = 'http://weibo.com/1816011541/info'
headers = json.load(open('../docs/headers.json'))
req = urllib2.Request(url, headers = headers)
html = urllib2.urlopen(req).read()
# print html
# 
# soup = BeautifulSoup(html, 'lxml')
# print soup.prettify()
tag = ''
t1 =  re.findall('"ns":"","domid":"Pl_Official_PersonalInfo__57(.*)', html, flags = 0)[0]
t2 = re.findall('S_line3(.*)</script>', t1, flags = re.M)[0]
t3 = re.findall('/span>(.*?)/a>', t2, flags = re.M)

for item in t3:
    tag = tag + item.replace('\\r\\n\\t\\t\\t\\t\\t\\t\\t\\t', '').replace('\\t\\t\\t\\t\\t\\t\\t\\t<\\', '') + ' '
print tag
