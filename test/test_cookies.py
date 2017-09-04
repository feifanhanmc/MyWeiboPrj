import urllib2
import json

url = 'http://weibo.com/2022580163/info'
headers = json.load(open('headers.json'))
req = urllib2.Request(url, headers = headers)
html = urllib2.urlopen(req).read()
print html