import numpy as np
import sys
from time import time

#REFS : https://ipsen.math.ncsu.edu/ps/OT113_Ipsen.pdf
# https://catonmat.net/mit-linear-algebra-part-three


#Metodo que consiste en multiplicar cada columna de A con toda la matriz B
#con el fin de obtener cada una de las filas de la matriz resultado
def method1(a,b,bShape):
    a = np.frombuffer(a)
    b = np.frombuffer(b).reshape(bShape)
    return a.dot(b)
    

#Metodo que consiste en la suma de los productos cruz entre cada columna de A 
# y cada Fila de B para hallar C
def method2(a,b):
    a = np.frombuffer(a)
    b = np.frombuffer(b)
    return np.outer(a,b)

# Metodo que consiste en calcular los productos puntos entre cada fila de A 
# y cada columna de B para encontrar cada elemento de C 
def method3(a,b,bShape):
    a = np.frombuffer(a)
    b = np.frombuffer(b).reshape(bShape)
    r= []
    for col in range(b.shape[1]):
        r.append(np.inner(a,b[:,col]))
    return r

def main():
    a = np.loadtxt(fname = "matrizA.txt",delimiter=',')
    b = np.loadtxt(fname = "matrizB.txt",delimiter=',')
    if(a.shape[1] !=b.shape[0]):
        print('Las columnas de A no son iguales a las Filas de B')
    else:
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
        a = np.random.rand(10,10)
        print(a)
        #b = np.random.rand(5000,2000)
        ba = a.tobytes()
        print(np.frombuffer(ba).reshape(a.shape))
        """print("METHOD 1")
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
        print(np.amin(np.array([r1,r2,r3])))"""
        

        


if __name__ == "__main__":
    main()