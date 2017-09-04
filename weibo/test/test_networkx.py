#-*- coding:utf8-*-
 
import numpy
import pandas
import matplotlib.pyplot as plt
import networkx as nx

def test():
    
#     tags_sim = numpy.loadtxt(open('../docs/sim/tags_sim.csv', 'r'),delimiter=",",skiprows=0)
    tags_sim = numpy.array([[0,3,2],[0,0,1],[0,0,0]])
    
    final_uids = []
    with open('../docs/final_uids.txt') as fp:
        for line in fp:
            final_uids.append(line.strip())
            
    G = nx.Graph()#建立一个空的无向图G
    N = len(tags_sim)
    
    
    for i in N:
        G.add_node(final_uids[i], label = 'aaa')
    for i in range(N):
        j = i + 1
        while j < N :
            G.add_edge(final_uids[i], final_uids[j], weight = tags_sim[i][j])
#             G.add_weighted_edges_from(ebunch, weight)
            j += 1
    nx.draw(G)
    nx.write_gexf(G,'test.gexf')
#     plt.show()
    


def test2():
    Matrix = numpy.matrix([
                            [0,1,2,3],
                            [0,0,4,5],
                            [0,0,0,6],
                            [0,0,0,0]])
    graph = nx.from_numpy_matrix(Matrix) 
    nx.draw(graph)  
    nx.write_gexf(graph,'test.gexf')
    plt.show()

def test3():
    dt = [('weight', float), ('cost', int)]
    A = numpy.matrix([[(1.0, 2)]], dtype = dt)
    G = nx.from_numpy_matrix(A)
    nx.draw(G)  
    nx.write_gexf(G,'test.gexf')
    plt.show()
    
def test4():
    Matrix = numpy.matrix([
                            [0,1,2,3],
                            [0,0,4,5],
                            [0,0,0,6],
                            [0,0,0,0]])
    index = ['a', 'b', 'c', 'd']
    columns = ['a', 'b', 'c', 'd']
    df = pandas.DataFrame(Matrix, index, columns)
#     G = nx.from_pandas_dataframe(df, label = 'sss')
    print df
    G = nx.from_pandas_dataframe(df)
    nx.draw(G)  
    nx.write_gexf(G,'test.gexf')
    plt.show()
    
def test5():
    r = numpy.random.RandomState(seed=5)
    ints = r.random_integers(1, 10, size=(3,2))
    a = ['A', 'B', 'C']
    b = ['D', 'A', 'E']
    print ints
    df = pandas.DataFrame(ints, columns=['weight', 'cost'])
    df[0] = a
    df['b'] = b
    print df

#     Matrix = numpy.matrix([
#                             [0,1,2,3],
#                             [0,0,4,5],
#                             [0,0,0,6],
#                             [0,0,0,0]])
#     index = ['a', 'b', 'c', 'd']
#     columns = ['a', 'b', 'c', 'd']
#     df2 = pandas.DataFrame(Matrix, index, columns)
#     print df2
#     weight1 = [1,2,3,4]
#     weight2 = [2,4,6,8]
    
    G=nx.from_pandas_dataframe(df, 0, 'b', ['weight', 'cost'])
    G=nx.from_pandas_dataframe(df, 0, 'b')
    nx.draw(G)  
    nx.write_gexf(G,'test.gexf')
#     plt.show()    
    
    
def test6():
    final_uids = []
    with open('../docs/final_uids.txt') as fp:
        for line in fp:
            final_uids.append(line.strip())
    
    final_uids = final_uids[:4]
    
    source = []
    target = []
    N = len(final_uids)
    for i in range(N):
        j = i + 1
        while j < N:
            source.append(final_uids[i])
            target.append(final_uids[j])
            j += 1
    
    df = pandas.DataFrame()
    df['source'] = source
    df['target'] = target
    df['weight1'] = [1,2,3,4,5,6]
    df['weight2'] = [2,4,6,8,10,12]
    print df
    G=nx.from_pandas_dataframe(df, 'source', 'target', ['weight1', 'weight2'])
    nx.draw(G)  
    nx.write_gexf(G,'test.gexf')

test2()   
    