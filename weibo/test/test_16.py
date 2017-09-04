import numpy

n = numpy.empty([2, 2])

print len(n)




Si = [1,2,3,4,5,6,7,8,9,10]
Sj = [1,2,3,4,5,6,7,8,9,10]
S = [val for val in Si if val in Sj]
sim = 0.0
for item in S:
    rank_i = 1 + Si.index(item)
    rank_j = 1 + Sj.index(item)
    
    sim +=  float(rank_i)/float(rank_i + 1) + float(rank_j)/float(rank_j + 1)
print sim