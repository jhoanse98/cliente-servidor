import numpy as np
import sys
from time import time

#REFS : https://ipsen.math.ncsu.edu/ps/OT113_Ipsen.pdf
# https://catonmat.net/mit-linear-algebra-part-three


#Metodo que consiste en multiplicar cada columna de A con toda la matriz B
#con el fin de obtener cada una de las filas de la matriz resultado
def method1(a,b):
    assert(a.shape[1]==b.shape[0])
    c = []
    for row in a:
        c.append(row.dot(b))
    return np.array(c)

#Metodo que consiste en la suma de los productos cruz entre cada columna de A 
# y cada Fila de B para hallar C
def method2(a,b):
    assert(a.shape[1]==b.shape[0])
    c = 0
    r= 0.0
    while c < a.shape[1]:
        col = a[:,c]
        row = b[c,:]    
        r+=np.outer(col,row)
        c+=1
    return r

# Metodo que consiste en calcular los productos puntos entre cada fila de A 
# y cada columna de B para encontrar cada elemento de C 
def method3(a,b):
    assert(a.shape[1]==b.shape[0])
    r= []
    for row in a:
        l = []
        for col in range(b.shape[1]):
            l.append(np.inner(row,b[:,col]))
        r.append(l)
    return np.array(r)

def main():

    """print("CLASSIC METHOD")
    t0 = time()
    print(a.dot(b))
    t1 = time()
    r0 = t1-t0
    print('Time: {}'.format(r0))
    print("METHOD 1")
    t0 = time()
    c = method1(a,b)
    print(c)
    t1 = time()
    r1 = t1-t0
    print('Time: {}'.format(r1))
    print("METHOD 2")
    t0 = time()
    c = method2(a,b)
    print(c)
    t1 = time()
    r2 = t1-t0
    print('Time: {}'.format(r2))
    print("METHOD 3")
    t0 = time()
    c = method3(a,b)
    print(c)
    t1 = time()
    r3 = t1-t0
    print('Time: {}'.format(r3))
    print('METODO MAS RAPIDO')
    print(np.amin(np.array([r0,r1,r2,r3])))"""
    #a = np.array_split(a, 2)
    #b = np.array_split(b, 2)
    a = np.random.rand(1300,5000)
    b = np.random.rand(5000,2000)
    print("METHOD 1")
    t0 = time()
    c = method1(a,b)
    #print(c)
    t1 = time()
    r1 = t1-t0
    print('Time: {}'.format(r1))
    print("METHOD 2")
    t0 = time()
    c = method2(a,b)
    #print(c)
    t1 = time()
    r2 = t1-t0
    print('Time: {}'.format(r2))
    print("METHOD 3")
    t0 = time()
    c = method3(a,b)
    #print(c)
    t1 = time()
    r3 = t1-t0
    print('Time: {}'.format(r3))
    #a = np.array_split(A, 2)
    #b = np.array_split(B, 2)
    print('METODO MAS RAPIDO')
    print(np.amin(np.array([r1,r2,r3])))
        

        


if __name__ == "__main__":
    main()