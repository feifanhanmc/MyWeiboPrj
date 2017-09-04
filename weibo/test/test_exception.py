import json
import urllib2
from bs4 import BeautifulSoup
import requests

def load_headers_data(filepath):
    with open(filepath, 'r') as fp:
        try:
            data = json.load(fp)
        except ValueError: 
            data = {}
    fp.close()
    return data 

url = 'http://weibo.com/1131043414/info'
headers_data = load_headers_data('../docs/headers.json')

r = requests.get(url, headers = headers_data)
print r.status_code


# try:
#     req = urllib2.Request(url, headers = headers_data)
#     html = urllib2.urlopen(req).read()
#     soup = BeautifulSoup(html, 'lxml')
#     print soup.title
# # except urllib2.URLError, e:
# except Exception, e:
#     print e