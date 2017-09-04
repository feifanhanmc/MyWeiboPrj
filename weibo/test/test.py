c = u'\u6cb3\u5317 \u5510\u5c71'
a =  c.encode('utf-8')
print a
print str(a)
print isinstance(c, unicode)


list1 = [1, 2, 3, 4, 5]
list2 = [1, 4, 5] 

list3 = list(set(list1) - set(list2))
print list3


import time
t = 'Sun Dec 06 15:18:57 +0800 2009'
t2 = t.replace('+0800 ', '')
print t2
time1 =  time.mktime(time.strptime(t2,"%a %b %d %H:%M:%S %Y"))
time2 =  time.time()
print time1
print time2
print (time2 - time1)/(24 * 3600 * 365)


print float('1279291283')