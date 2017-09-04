# -*- coding: utf-8 -*-
import copy
import numpy
import random
import networkx as nx
import matplotlib.pyplot as plt
from community.community_louvain import best_partition, modularity

class Gas():
    #初始化一些变量
    def __init__(self,popsize,chrosize,xrangemin,xrangemax, varnum):
        self.popsize = popsize
        self.chrosize = chrosize
        self.xrangemin = xrangemin
        self.xrangemax = xrangemax
        self.varnum = varnum
        self.single_chrosize = chrosize / varnum
        self.crossrate = 1
        self.mutationrate = 0.05
        self.load_data()
        
    def load_data(self):    
        self.baseinfo_sim = numpy.loadtxt(open('../docs/sim_500/baseinfo_500_sim.csv', 'r'),delimiter=",",skiprows=0)
        self.sr_sim = numpy.loadtxt(open('../docs/sim_500/sr_500_sim.csv', 'r'),delimiter=",",skiprows=0)
        self.tags_sim = numpy.loadtxt(open('../docs/sim_500/tags_500_sim.csv', 'r'),delimiter=",",skiprows=0)
        self.statuses_sim = numpy.loadtxt(open('../docs/sim_500/statuses_500_sim.csv', 'r'),delimiter=",",skiprows=0)
        
    def initialpop(self):#初始化种群
        pop = []
        for i in range(self.popsize):
            individual = []
            for i in range(self.chrosize):
                individual.append(random.randint(0, 1))
            pop.append(individual)
        return pop
    
    def get_weight(self, list):
        weight_list = []
        total = sum(list)
        for eq in list:
            weight_list.append(eq/total)
        return weight_list

    def get_eq(self, sim_matrix):
        G = nx.from_numpy_matrix(sim_matrix) 
        part = best_partition(G)
        q =  modularity(part, G)
        k = len(list(set(part.values())))
        if k == 1:
            eq = 0
        else:
            eq = float(k * q) / float( k - 1)
        data = {}
        data['eq'] = eq
        data['q'] = q
        data['k'] = k
        return data   
     
    def fun(self,x): #定义函数
        weight = self.get_weight(x)
        baseinfo_w = weight[0]
        sr_w = weight[1]
        tags_w = weight[2]
        statuses_w = weight[3]
        user_sim = baseinfo_w*self.baseinfo_sim + sr_w*self.sr_sim + tags_w*self.tags_sim + statuses_w*self.statuses_sim
        result = self.get_eq(user_sim)
#         print 'eq',result['eq'], 'q', result['q'], 'k', result['k'], 'weight', weight
        return result['eq']
    
    def get_fitness(self,X):  #适应度函数
        fitness = []
        for x in X:
            fitness.append(self.fun(x))
        return fitness
    
    def selection(self,popsel,fitvalue): #选择
        new_fitvalue = []
        totalfit = sum(fitvalue)
        accumulator = 0.0
        for val in fitvalue: 
            #对每一个适应度除以总适应度，然后累加，这样可以使适应度大
            #的个体获得更大的比例空间。
            new_val =(val*1.0/totalfit)            
            accumulator += new_val
            new_fitvalue.append(accumulator)            
        ms = []
        for i in xrange(self.popsize):
            #随机生成0,1之间的随机数
            ms.append(random.random()) 
        ms.sort() #对随机数进行排序
        fitin = 0
        newin = 0
        newpop = popsel
        while newin < self.popsize:
            #随机投掷，选择落入个体所占轮盘空间的个体
            if(ms[newin] < new_fitvalue[fitin]):
                newpop[newin] = popsel[fitin]
                newin = newin + 1
            else:
                fitin = fitin + 1
        #适应度大的个体会被选择的概率较大
        #使得新种群中，会有重复的较优个体
        pop = newpop
        return pop
    
    def crossover(self,pop): #交叉
        for i in xrange(self.popsize-1):
            #近邻个体交叉，若随机数小于交叉率
            if(random.random()<self.crossrate):
                #随机选择交叉点
                singpoint =random.randint(0,self.chrosize)
                temp1 = []
                temp2 = []
                #对个体进行切片，重组
                temp1.extend(pop[i][0:singpoint])
                temp1.extend(pop[i+1][singpoint:self.chrosize])
                temp2.extend(pop[i+1][0:singpoint])
                temp2.extend(pop[i][singpoint:self.chrosize])
                pop[i]=temp1
                pop[i+1]=temp2
        return pop
    
    def mutation(self,pop): #变异
        for i in xrange(self.popsize):
            #反转变异，随机数小于变异率，进行变异
            if (random.random()< self.mutationrate):
                mpoint = random.randint(0,self.chrosize-1)
                #将随机点上的基因进行反转。
                if(pop[i][mpoint]==1):
                    pop[i][mpoint] = 0
                else:
                    pop[i][mpoint] =1
        return pop
    
    def elitism(self,pop,popbest,nextbestfit,fitbest):#精英保留
        #输入参数为上一代最优个体，变异之后的种群，
        #上一代的最优适应度，本代最优适应度。这些变量是在主函数中生成的。
        if nextbestfit-fitbest <0:  
            #满足精英策略后，找到最差个体的索引，进行替换。         
            pop_worst = nextfitvalue.index(min(nextfitvalue))
            pop[pop_worst] = popbest
        return pop
    
    def get_declist(self,chroms): #解码
        chroms = numpy.array(chroms)
        chroms_1 = chroms[:,:self.single_chrosize]
        chroms_2 = chroms[:,self.single_chrosize : self.single_chrosize * 2]
        chroms_3 = chroms[:,self.single_chrosize * 2 : self.single_chrosize * 3]
        chroms_4 = chroms[:,self.single_chrosize * 3 :]
        
        step = (self.xrangemax - self.xrangemin)/float(2**self.single_chrosize-1)
        self.chroms_declist =[]
        for i in xrange(self.popsize):
            chrom_1_dec = self.xrangemin + step*self.chromtodec(chroms_1[i])  
            chrom_2_dec = self.xrangemin + step*self.chromtodec(chroms_2[i])
            chrom_3_dec = self.xrangemin + step*self.chromtodec(chroms_3[i])  
            chrom_4_dec = self.xrangemin + step*self.chromtodec(chroms_4[i])    
            self.chroms_declist.append((chrom_1_dec, chrom_2_dec, chrom_3_dec, chrom_4_dec))
        return self.chroms_declist
    
    def chromtodec(self,chrom): #二进制转十进制
        m = 1
        r = 0
        for i in xrange(self.single_chrosize):
            r = r + m * chrom[i]
            m = m * 2
        return r
    
if __name__ == '__main__':
    
    generation = 50 # 遗传代数
    #引入Gas类，传入参数：种群大小，编码长度，变量范围, 变量个数
    mainGas = Gas(30, 30 , 0 , 1, 4) 
    
    pop = mainGas.initialpop()  #种群初始化
    pop_best = [] #每代最优个体

    for i in xrange(generation): 
        print 'index', i
        #在遗传代数内进行迭代
        declist = mainGas.get_declist(pop)#解码
        fitvalue =mainGas.get_fitness(declist)#适应度函数
        #选择适应度函数最高个体
        popbest = pop[fitvalue.index(max(fitvalue))]
        #对popbest进行深复制，以为后面精英选择做准备
        popbest =copy.deepcopy(popbest)
        #最高适应度
        fitbest = max(fitvalue)
        #保存每代最高适应度值
        pop_best.append(fitbest)        
        #进行算子操作，并不断更新pop
        mainGas.selection(pop,fitvalue)  #选择
        mainGas.crossover(pop) # 交叉
        mainGas.mutation(pop)  #变异
        #精英策略前的准备对变异之后的pop，求解最大适应度
        nextdeclist = mainGas.get_declist(pop) 
        nextfitvalue =mainGas.get_fitness(nextdeclist)        
        nextbestfit = max(nextfitvalue) 
        #精英策略，比较深复制的个体适应度和变异之后的适应度
        mainGas.elitism(pop,popbest,nextbestfit,fitbest)

    t = [x for x in xrange(generation)]
    s = pop_best
    print s
    plt.plot(t,s)
    plt.xlabel('Generation')
    plt.ylabel('EQ')
    plt.show()
    plt.savefig('myGA.png') #保存图  
    plt.close()
