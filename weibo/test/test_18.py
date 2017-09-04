import time

def get_use_time(t):
    now =  time.time()
    return float(now - t)/float(3600 * 24 * 365) 


print get_use_time(1251284136)
print get_use_time(1477736935)