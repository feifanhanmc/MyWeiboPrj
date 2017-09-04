# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
 
text_from_file_with_apath = open('test_29.txt').read()
 
wordlist_after_jieba = jieba.cut(text_from_file_with_apath, cut_all = True)
print wordlist_after_jieba
print type(wordlist_after_jieba)

wl_space_split = " ".join(wordlist_after_jieba)
print wl_space_split
print type(wl_space_split) 

my_wordcloud = WordCloud(font_path="simhei.ttf").generate(wl_space_split)
 
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()