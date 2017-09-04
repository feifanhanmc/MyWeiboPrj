# -*- coding: utf-8 -*-

import codecs
import re

import MySQLdb
import jieba
import numpy
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity


def load_user_statuses():
    db  = MySQLdb.connect('localhost', 'root', 'root', 'myweiboprj')
    db.set_character_set('utf8')
    cursor = db.cursor()
    
    sql = """SELECT UID, STATUSES FROM RAW_USER ORDER BY UID ASC"""
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception,e:
        print e
    db.close()
    return results

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
    
    for item in results:
        output = ''
        uids.append(item[0])
        seg_list = jieba.lcut(item[1], cut_all = False)
        
        for word in seg_list:
            if word.encode('utf8') not in stop_words:
                #进一步过滤掉字符、数字、英文，只保留中文内容
                word = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%\w]", "", word)
                output += word.encode('utf8') + ' ' 
        statuses.append(output)
    return uids, statuses

def compute_TFIDF(corpus):
    vectorizer = CountVectorizer(max_features=20000) #将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频  
    transformer = TfidfTransformer() #该类会统计每个词语的tf-idf权值   
    
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus)) #第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵  
    
    #解决直接打印列表时，中文表现为unicode编码问题
    pre_words = vectorizer.get_feature_names() #获取词袋模型中的所有词语 
    words_num = len(pre_words)
    words = []
    for word in pre_words:
        words.append(word.encode('utf8'))
    words = str(words).decode('string_escape')
    
    weight = tfidf.toarray() #将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重 
    return weight, words, words_num

def process_statuses_sim(N, pre_statuses_sim):
    #把pre_statuses_sim对角线以及左下角清零
    for i in range(N):
        j = i
        while j < N:
            pre_statuses_sim[j][i] = 0.0
            j += 1
    statuses_sim = pre_statuses_sim
    return statuses_sim

def save_statuses_sim(statuses_sim):
    numpy.savetxt('../docs/sim/statuses_sim.csv', statuses_sim, fmt = '%.3f', delimiter = ',')  

def main():    
    results = load_user_statuses()
    uids, statuses = process_statuses(results)
    weight, words, words_num =  compute_TFIDF(statuses)    #注意，这里的words是一个字符串，虽然看起来像列表
    statuses_sim = process_statuses_sim(len(results), cosine_similarity(weight))
    save_statuses_sim(statuses_sim)
    
    print weight.shape      #(9599L, 848L)
    print statuses_sim.shape       #(9599L, 9599L)
    
main()


