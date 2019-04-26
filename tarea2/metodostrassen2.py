a = [[2, 2, 2, 2, 2, 2, 1, 2],
    [1, 1, 1, 1, 1, 1, 1, 2],
    [0, 0, 0, 0, 1, 0, 1, 2],
    [1, 1, 1, 1, 1, 1, 1, 2],
    [3, 3, 3, 3, 3, 3, 1, 2],
    [2, 2, 2, 2, 2, 2, 1, 2],
    [1, 1, 1, 1, 1, 1, 1, 2],
    [2, 2, 2, 2, 2, 2, 1, 2]
]

b = [[2, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 2],
    [0, 0, 0, 0, 1, 0, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 2],
    [3, 3, 3, 3, 3, 3, 1, 2],
    [2, 2, 2, 2, 2, 2, 1, 2],
    [1, 1, 1, 1, 1, 1, 2, 3],
    [3, 3, 3, 3, 3, 3, 1, 2]
    ]



########################################formulas del metodo strassen #############################################
"""
p1= A*(F-H)
P2= H*(A+B)
P3= E*(C+D)
P4= D*(G-E)
P5= (A+D)*(E+H)
P6= (B-D)*(G+H)
P7= (A-C)*(E+F)


TENIENDO EN CUENTA QUE:


MATRIZ_A= [  A   B   					MATRIZ_B = [   E    F  

		     C   D  ]                                  G    H  ]



########################################### MATRIZ RESULTANTE #####################################################


MATRIZ_RESULTADO = [  P6+P5+P4-P2,   P1+P2 

						P3+P4,        P1+P5-P3-P7 ]




"""






shap=[len(a),len(b[1])]

import numpy as np
from time import time

a=np.array(a)
b=np.array(b)


def multimatriz2(a,b):
	matriz= [a[0][0]*b[0][0]+a[0][1]*b[1][0],
			 a[0][0]*b[0][1]+a[0][1]*b[1][1],
			 a[1][0]*b[0][0]+a[1][1]*b[1][0],
			 a[1][0]*b[0][1]+a[1][1]*b[1][1]]
	return np.array(matriz).reshape(2,2)

def sumamatriz(a,b):
	c=[[a[i][j]+b[i][j] for j in range(len(a[i]))] for i in range(len(a))]
	return c



def restamatriz(a,b):
	c=[[a[i][j]-b[i][j] for j in range(len(a[i]))] for i in range(len(a))]
	return c


def dividematriz(a):
	if len(a) % 2 !=0 or len(a[0]) % 2 != 0:
		raise Exception('Matrices deben ser potencia de 2')
	longimatriz=len(a)
	mitadmatriz=longimatriz//2

	top_left = [[a[i][j] for j in range(mitadmatriz)] for i in range(mitadmatriz)]
	bottom_left = [[a[i][j] for j in range(mitadmatriz)] for i in range(mitadmatriz, longimatriz)]
	top_right = [[a[i][j] for j in range(mitadmatriz, longimatriz)] for i in range(mitadmatriz)]
	bottom_right = [[a[i][j] for j in range(mitadmatriz, longimatriz)] for i in range(mitadmatriz, longimatriz)]

	return top_left, top_right, bottom_left, bottom_right

def obtendimensiones(a):
	return len(a), len(a[0])

contador=0
def strassen(matrizA, matrizB):
	if obtendimensiones(matrizA) != obtendimensiones(matrizB):
		raise Exception("Las matrices deben ser del mismo tamaño")
	if obtendimensiones(matrizA) == (2,2):
		return multimatriz2(matrizA,matrizB)

	
	A,B,C,D = dividematriz(matrizA)
	E,F,G,H = dividematriz(matrizB)

	P1= strassen(A, restamatriz(F,H))
	P2= strassen(sumamatriz(A,B),H)
	P3= strassen(sumamatriz(C,D),E)
	P4= strassen(D, restamatriz(G,E))
	P5= strassen(sumamatriz(A,D),sumamatriz(E,H))
	P6= strassen(restamatriz(B,D), sumamatriz(G,H))
	P7= strassen(restamatriz(A,C), sumamatriz(E,F))

	top_left_matriz=restamatriz(sumamatriz(sumamatriz(P4,P5),P6),P2)
	top_right_matriz= sumamatriz(P1,P2)
	bottom_left_matriz=sumamatriz(P3,P4)
	bottom_right_matriz=restamatriz(restamatriz(sumamatriz(P1,P5),P3),P7)
	resultado=[]

	for i in range(len(top_right_matriz)):
		resultado.append(top_left_matriz[i]+ top_right_matriz[i])
		#print(resultado)
	for i in range(len(bottom_right_matriz)):
		resultado.append(bottom_left_matriz[i]+ bottom_right_matriz[i])

	return resultado
	

a=np.random.rand(64,64)
b=np.random.rand(64,64)
t1=time()
strassen(a,b)
t2=time()
print(t2-t1)
t1=time()
a.dot(b)																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																						
t2=time()
resultante=t2-t1
print("el tiempo resultado es: "+str(resultante))

#print(sumamatriz(a,b))
#print(restamatriz(a,b))