import numpy

a = numpy.array([[0,0,0],
                [0,0,1],
                [0,0.8,0.9],
                [0.3,0.4,0.1],
                [0.9,0.3,0.5],
                [0,1,0],
                [0,1,1],
                [1,0,0],
                [1,0,1],
                [1,1,0],
                [1,1,1]])
a = numpy.array([[-2.220446049250313081e-16,9.088026410008442912e-01,9.316726994522224192e-01,9.080388384239780342e-01],
                 [9.088026410008442912e-01,0.000000000000000000e+00,6.603912352521551510e-01,9.141445839795560024e-01],
                 [9.316726994522224192e-01,6.603912352521551510e-01,0.000000000000000000e+00,8.219131127067036413e-01],
                 [9.080388384239780342e-01,9.141445839795560024e-01,8.219131127067036413e-01,0.000000000000000000e+00],
                 [9.869789842249688805e-01,9.458472071402481696e-01,9.393475395191194233e-01,9.154428315793267101e-01]])

b = a

numpy.savetxt('../docs/test_a.csv', a, delimiter = ',') 
numpy.savetxt('../docs/test_b.csv', b, fmt = '%.6f', delimiter = ',') 







