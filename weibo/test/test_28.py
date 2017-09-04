# -*- coding: utf-8 -*-

from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt

l = [u'\u65c5\u6e38', u'\u5a31\u4e50', u'\u7f8e\u98df', u'\u97f3\u4e50', u'\u65c5\u6e38']
t = []
c = dict(Counter(l))

for key, value in c.items():
    t.append((key, value))

print t
wc = WordCloud(font_path="simhei.ttf", background_color="white").generate_from_frequencies(t)
plt.imshow(wc)
plt.axis("off")
plt.show()


