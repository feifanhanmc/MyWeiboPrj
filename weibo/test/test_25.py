# -*- coding: utf-8 -*-
import random


popsize = 10
mutationrate = 0.1
xrangemax = 2 
xrangemin = -1
chrosize = 10 
popsize = 10
def chromtodec(chrom, chrosize): #二进制转十进制
    m = 1
    r = 0
    for i in xrange(chrosize):
        r = r + m * chrom[i]
        m = m * 2
    return r

def get_declist(chroms): #解码
    step =(xrangemax - xrangemin)/float(2**chrosize-1)
    chroms_declist =[]
    for i in xrange(popsize):
        print chroms[i]
        chrom_dec = xrangemin+step*chromtodec(chroms[i], chrosize)  
        chroms_declist.append(chrom_dec)      
    return chroms_declist
    
def mutation(pop): #变异
    for i in xrange(popsize):
        print 'index', i
        #反转变异，随机数小于变异率，进行变异
        n = random.random()
        print 'n', n
        if (n < mutationrate):
            mpoint = random.randint(0,chrosize-1)
            print 'mpoint', mpoint
            #将随机点上的基因进行反转。
            if(pop[i][mpoint]==1):
                pop[i][mpoint] = 0
            else:
                pop[i][mpoint] =1

    return pop

def main():
    pop =  [[0, 0, 0, 1, 1, 1, 0, 0, 1, 0], 
            [1, 0, 0, 0, 1, 1, 0, 1, 0, 0], #1
            [1, 0, 1, 1, 0, 1, 0, 1, 1, 0], 
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 1], 
            [0, 1, 0, 1, 0, 1, 1, 0, 0, 0], 
            [1, 1, 0, 1, 0, 0, 1, 0, 0, 0], 
            [0, 0, 0, 0, 0, 1, 0, 1, 1, 1], 
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1], 
            [0, 0, 1, 1, 1, 0, 1, 0, 1, 1], #8
            [0, 0, 0, 1, 1, 0, 0, 0, 1, 1]] #9

#     print get_declist(pop)
    r =  mutation(pop)
    for i in  r:
        print i

main()


