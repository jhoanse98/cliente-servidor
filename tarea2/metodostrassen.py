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
# implementacion hecha con base a: https://github.com/stanislavkozlovski/Algorithms/blob/master/Coursera/algorithms_stanford/Strassen%20Matrix%20Multiplication/python/strassen.py

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
	a=np.array(a)
	b=np.array(b)
	matriz= a.dot(b)
	return np.array(matriz).reshape(128,128)

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
def strassen(matrizA, matrizB, bol, shapes):
	if bol and len(shapes)>1:
		matrizA = np.frombuffer(matrizA).reshape(shapes)
		matrizB = np.frombuffer(matrizB).reshape(shapes)
	if obtendimensiones(matrizA) != obtendimensiones(matrizB):
		raise Exception("Las matrices deben ser del mismo tamaño")
	if obtendimensiones(matrizA) == (128,128):
		return multimatriz2(matrizA,matrizB)

	
	A,B,C,D = dividematriz(matrizA)
	E,F,G,H = dividematriz(matrizB)
	
	P1= strassen(A, restamatriz(F,H), False,[-1])
	P2= strassen(sumamatriz(A,B),H, False,[-1])
	P3= strassen(sumamatriz(C,D),E,False,[-1])
	P4= strassen(D, restamatriz(G,E),False,[-1])
	P5= strassen(sumamatriz(A,D),sumamatriz(E,H), False, [-1])
	P6= strassen(restamatriz(B,D), sumamatriz(G,H), False, [-1])
	P7= strassen(restamatriz(A,C), sumamatriz(E,F), False, [-1])


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
	



#pri}}}}}}}}}}}}nt(sumamatriz(a,b))
#print(restamatriz(a,b))