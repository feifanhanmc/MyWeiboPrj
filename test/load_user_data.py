# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup

    
def parse_user_info(html):
    soup = BeautifulSoup(html, 'lxml')
    uid = ''
    username = soup.h1.string.strip()
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
    return user_info

def load_user_tweets():
    print
    
def write_to_file():
    print
    
def main():
    print

if __name__ =='__main__':
    main()