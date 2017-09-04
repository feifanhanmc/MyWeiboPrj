# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup as bs

def getHtml(url):
    page=urllib2.urlopen(url)
    html=page.read()
    print html
    return html


def cleanHtml(filename):
    soup=bs(open(filename), 'lxml')
#     print soup.title.string
    fans_div = soup.findAll('div', attrs={'class': 'WB miniblog'})
    print fans_div



# html=getHtml("http://weibo.com/1642880175/")
cleanHtml('yck_html.txt')
# url = 'http://weibo.com/1642880175/'
# print requests.get(url).text