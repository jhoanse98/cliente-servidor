import sys
import numpy as np

params = sys.argv
a = np.loadtxt(fname = "matrizA.txt",delimiter=',')
b = np.loadtxt(fname = "matrizB.txt",delimiter=',')
if(a.shape[1] !=b.shape[0]):
    print('Las columnas de A no son iguales a las Filas de B')

def method1(a,b):
    assert(a.shape[1]==b.shape[0])
    c = []
    for row in a:
    	print(row)
    	c.append(row.dot(b))
    return np.array(c)

print(a)

print(method1(a,b))