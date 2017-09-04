# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup

def read_user_html(uids_path, user_html_path):
    user_html = []
    with open(uids_path, 'r') as uids_fp:
        for line in uids_fp:
            uid = str(line.strip())
            with open(user_html_path + uid + '.txt', 'r') as html_fp:
                user_html.append({uid: html_fp.read()})
    return user_html

def parse_user_info(user_html):
    user_info = []
    for item in user_html:
        user_info.append(parse_single_user_info(item))
    return user_info

def parse_single_user_info(item):
    uid = item.keys()[0]
    print uid
    html = item[uid]
    
    soup = BeautifulSoup(html, 'lxml')
    user_info = {}
    try:
        username = soup.h1.string.strip()
        print username
        intro = soup.select('.pf_intro')[0].string.strip()
        follow_num = soup.select('.W_f18')[0].string.strip()
        fans_num = soup.select('.W_f18')[1].string.strip()
        tweets_num = soup.select('.W_f18')[2].string.strip()
        exp = (soup.select('.level_info')[0].select('.info'))[1].select('.S_txt1')[0].string.strip()
        badges = []
        tags = []
        base_info = {}
        tweets = load_user_tweets()
        follow = []
        fans = []

    
        user_info = {
            'uid':          uid,
            'username':     username,
            'intro':        intro,
            'follow_num':   follow_num,
            'fans_num':     fans_num,
            'tweets_num':   tweets_num,
            'bagdes':       badges,
            'exp':          exp,
            'tags':         tags,
            'base_info':    base_info,
            'tweets':       tweets,
            'follow':       follow,
            'fans':         fans 
        }
    except:
        print 'error'
        print '可能是爬取内容的时候，出现了问题'
    return user_info

def load_user_tweets():
    print
    
def write_to_file(user_info):
    with open('../../docs/user_info.txt', 'w') as fout:
        for item in user_info:
            fout.write(item)
        fout.close()
def main():
    user_html = read_user_html('../../docs/uids_succeed.txt', '../../docs/user_html/')
    user_info = parse_user_info(user_html)
    write_to_file(user_info)

    
if __name__ =='__main__':
    main()