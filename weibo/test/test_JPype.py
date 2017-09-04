# -*- coding: utf-8 -*-

from jpype import *  
import os.path  
s = "可能要孤独终老了 ​​​🙃"
# s = 'sss'
jarpath = os.path.join(os.path.abspath('.'), 'D:/Work/Git/MyWeiboPrj/weibo/docs/jar_path/')  
startJVM(getDefaultJVMPath(),"-ea", "-Djava.class.path=%s" % (jarpath + 'myutils8.jar'))
  
print isinstance(s, unicode)    #False

print isinstance(s, str)    #True

JDClass = JClass("jpype.MyUtils") 
jd = JDClass()  
s = s.decode('utf8')
print s
jprint = java.lang.System.out.println 
# print JDClass.test(s) 
result =  jd.remove4BytesUTF8Char(s)
print isinstance(result, unicode)    #True

print isinstance(result, str)    #False
jprint(jd.remove4BytesUTF8Char(s).encode('utf8'))
shutdownJVM()  