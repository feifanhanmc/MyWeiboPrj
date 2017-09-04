# -*- coding: utf-8 -*-

'''
results = {
    uid: [name, gender, created_at, bi_followers_count, province, city, location, tag, statuses_count, friends_count, followers_count, post_rate, statuses],
    uid: [name, gender, created_at, bi_followers_count, province, city, location, tag, statuses_count, friends_count, followers_count, post_rate, statuses]...
}'''
import codecs
import csv
import os
from os.path import isfile
import re
import time

import MySQLdb
import jieba
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


def load_user_data():
    db  = MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')
    cursor = db.cursor()
    
#     sql = """SELECT * FROM RAW_USER"""
    sql = """SELECT * FROM RAW_USER"""
    try:
        cursor.execute(sql)
        results = {} 
        for item in cursor.fetchall():
            results[item[0]] = list(item[1:])
    except Exception,e:
        print e
    db.close()
    return results

def process_tags(results):
    tags = []
    for key in results:
        for tag in results[key][7].split():
            tags.append(tag)
#     return str(list(set(tags))).decode('string_escape') #错误的使用啊，把列表转成了字符串str
    return list(set(tags))

def load_stop_words(filename):
    stop_words = []
    with codecs.open(filename, 'r') as fp:
        for line in fp:
            stop_words.append(line.strip())
    fp.close()
    return stop_words

def process_statuses(results):
    uids = []
    statuses = []
    stop_words = load_stop_words('../docs/stop_words.txt')
    jieba.load_userdict("../docs/user_dict.txt") 
    
    for key in results:
        output = ''
        uids.append(key)
        seg_list = jieba.lcut(results[key][12], cut_all = False)
        
        for word in seg_list:
            if word.encode('utf8') not in stop_words:
                #进一步过滤掉字符、数字、英文，只保留中文内容
                word = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", word)
                output += word.encode('utf8') + ' ' 
        statuses.append(output)
    return uids, statuses

def compute_TFIDF(corpus):
    vectorizer = CountVectorizer() #将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频  
    transformer = TfidfTransformer() #该类会统计每个词语的tf-idf权值   
    
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus)) #第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵  
    
    #解决直接打印列表时，中文表现为unicode编码问题
    pre_words = vectorizer.get_feature_names() #获取词袋模型中的所有词语 
    words = []
    for word in pre_words:
        words.append(word.encode('utf8'))
    words = str(words).decode('string_escape')
    
    weight = tfidf.toarray() #将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重 
    return weight, words

def get_max_count(results):
    list_bi_followers_count = []
    list_statuses_count = []
    list_friends_count = []
    list_followers_count = []
    
    for key in results:
        r = results[key]
        list_bi_followers_count.append(int(r[3]))
        list_statuses_count.append(int(r[8]))
        list_friends_count.append(int(r[9]))
        list_followers_count.append(int(r[10]))
    max_bi_followers_count = max(list_bi_followers_count)
    max_statuses_count = max(list_statuses_count)
    max_friends_count = max(list_friends_count)
    max_followers_count = max(list_followers_count)
    return max_bi_followers_count, max_statuses_count, max_friends_count, max_followers_count

def main():    
    results = load_user_data()
    uids, statuses = process_statuses(results)
    tags = process_tags(results)    #注意，由于使用了list(set(tags))方法，所以tags列表中的顺序不固定
    weight, words =  compute_TFIDF(statuses)    #注意，这里的words是一个字符串，虽然看起来像列表
    t = time.time()
    max_bi_followers_count, max_statuses_count, max_friends_count, max_followers_count = get_max_count(results)
    
    users = []
    for i in range(len(uids)):
        user = []
        r = results[uids[i]]
        user.append(uids[i]) 
        if r[1] == 'm':
            user.append(0.1)
        else:
            user.append(0.0)
        user.append(0.1 * (t - float(r[2]) ) / (3600 * 24 * 365))
        user.append((float(r[3])/max_bi_followers_count))
        user.append((float(r[8])/max_statuses_count))
        user.append((float(r[9])/max_friends_count))
        user.append((float(r[10])/max_followers_count))
        user.append(int(r[4]) * 0.01)
        for tag in tags:
            if tag in r[7]:
                user.append(0.618)
            else:
                user.append(0.0)
        user.extend(weight[i])
        users.append(user)
        
    filename = '../docs/users.csv'
    if isfile(filename):
        os.remove(filename)
    with open(filename, 'ab+') as fout:
        writer = csv.writer(fout)
        writer.writerows(users)
    fout.close()
    
    
main()

