import zmq
import sys
import numpy as np
from time import time
from metodostrassen import *

def main():
    if len(sys.argv) != 2:
        print('Debe ser llamado con una identidad')
        exit()
    else:
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        identity = sys.argv[1].encode('ascii')
        socket.identity = identity
        #socket.connect('tcp://localhost:4444')
        socket.connect('tcp://localhost:4444')
        socket.connect('tcp://localhost:4445')
        socket.connect('tcp://localhost:4446')
        socket.connect('tcp://localhost:4447')
        socket.connect('tcp://localhost:4448')
        socket.connect('tcp://localhost:4449')
        socket.connect('tcp://localhost:4450')
        #socket.connect('tcp://localhost:4445')
        #socket.connect('tcp://localhost:4446')                
        # Poller, objeto el cual esta pendiente de algunos sockets
        poller = zmq.Poller()
        poller.register(sys.stdin,zmq.POLLIN)
        poller.register(socket,zmq.POLLIN)
        b=1
        p=1
        #A = np.random.rand(1000,1000)
        #B = np.random.rand(1000,1000)
        #A = np.loadtxt(fname = "matrizA.txt",delimiter=',')
        #T = np.loadtxt(fname = "matrizB.txt",delimiter=',')
        #B = np.loadtxt(fname = "matrizB.txt",delimiter=',')
        
        A=np.random.rand(4096,4096)
        T=np.random.rand(4096,4096)
        aShape = A.shape
        bShape = T.shape
        row = 0
        method = ''
        
        status = True
        print('======================================')
        print('Ingrese el metodo a usar: (1,2,3,4)')
        print('======================================')
        method = input()
        print('Presione Enter para empezar')
        if method == '1' or method == '3' or method == '4':
            result=[]
        else:
            result=0
        t0 = time()

        while status:
            socks = dict(poller.poll())
            if socket in socks:
                sender=socket.recv_multipart()
                #print(np.frombuffer(sender[2]))
                if len(sender) > 1 and (method == '1' or method == '3'):
                    print(sender[0].decode(), sender[1].decode())
                    result.append(np.frombuffer(sender[2]))
                if len(sender) > 1 and method =='2':
                    result+=np.frombuffer(sender[2])
                if method == '2' and row == bShape[0]:
                    result = result.reshape(aShape[0],bShape[1])
                if len(sender) > 1 and method == '4':
                    if(sender[1]==b'falta'):
                        if p == 7:
                            #P6=np.frombuffer(sender[2]).reshape(Ashape,Ashape)

                            socket.send_multipart([method.encode('ascii'),np.array(restamatriz(I,C)).tobytes(), np.array(sumamatriz(E,F)).tobytes(), str(Ashape).encode(), str(Ashape).encode(), str(p).encode()])
                            p+=1
                        if p == 6:
                            #P5=np.frombuffer(sender[2]).reshape(Ashape,Ashape)
                            socket.send_multipart([method.encode('ascii'), np.array(restamatriz(B,D)).tobytes(), np.array(sumamatriz(G,H)).tobytes(), str(Ashape).encode(), str(Ashape).encode(), str(p).encode()])
                            p+=1
                        if p == 5:
                            #P4= np.frombuffer(sender[2]).reshape(Ashape,Ashape)
                            socket.send_multipart([method.encode('ascii'), np.array(sumamatriz(I,D)).tobytes(), np.array(sumamatriz(E,H)).tobytes(), str(Ashape).encode(), str(Ashape).encode(), str(p).encode()])
                            p+=1 
                        if p == 4:
                            #P3 = np.frombuffer(sender[2]).reshape(Ashape,Ashape)
                            socket.send_multipart([method.encode('ascii'), np.array(D).tobytes(), np.array(restamatriz(G,E)).tobytes(), str(Ashape).encode(), str(Ashape).encode(), str(p).encode()])
                            p+=1
                        if p == 3:
                            print("aqui p es igual a 3")
                            #P2= np.frombuffer(sender[2]).reshape(Ashape,Ashape)
                            socket.send_multipart([method.encode('ascii'), np.array(sumamatriz(C,D)).tobytes(), np.array(E).tobytes(),str(Ashape).encode(), str(Ashape).encode(), str(p).encode()])
                            p+=1
                        if p == 2:
                            print("aqui p es igual a 2")
                            #P1=np.frombuffer(sender[2]).reshape(Ashape,Ashape)
                            socket.send_multipart([method.encode('ascii'), np.array(sumamatriz(I,B)).tobytes(), np.array(H).tobytes(), str(Ashape).encode(), str(Ashape).encode(), str(p).encode()])
                            p+=1
                            print(p)
                    else:
                    	pn = int(sender[3].decode())
                    	if pn == 1:
                    		P1=np.frombuffer(sender[2]).reshape(Ashape,Ashape)
                    		b+=1
                    	if pn == 2:
                    		P2=np.frombuffer(sender[2]).reshape(Ashape,Ashape)
                    		b+=1
                    	if pn == 3:
                    		P3=np.frombuffer(sender[2]).reshape(Ashape,Ashape)
                    		b+=1
                    	if pn == 4:
                    		P4=np.frombuffer(sender[2]).reshape(Ashape,Ashape)
                    		b+=1
                    	if pn == 5:
                    		P5=np.frombuffer(sender[2]).reshape(Ashape,Ashape)
                    		b+=1
                    	if pn == 6:
                    		P6=np.frombuffer(sender[2]).reshape(Ashape,Ashape)
                    		b+=1
                    	if pn == 7:
                    		P7=np.frombuffer(sender[2]).reshape(Ashape,Ashape)
                    		b+=1

                    if b==8 and sender[1]==b'ok':
                            top_left_matriz=restamatriz(sumamatriz(sumamatriz(P4,P5),P6),P2)
                            top_right_matriz= sumamatriz(P1,P2)
                            bottom_left_matriz=sumamatriz(P3,P4)
                            bottom_right_matriz=restamatriz(restamatriz(sumamatriz(P1,P5),P3),P7)                        
                            for i in range(len(top_right_matriz)):
                                result.append(top_left_matriz[i]+ top_right_matriz[i])
                            for i in range(len(bottom_right_matriz)):
                                result.append(bottom_left_matriz[i]+ bottom_right_matriz[i])


                    
                    

                if sender[0] == b'finish':
                    status=False                    
                if row < aShape[0] and method=='1':
                    socket.send_multipart([method.encode('ascii'),A[row,:].tobytes(),B.tobytes(),str(bShape[0]).encode(),str(bShape[1]).encode()])
                    row+=1
                if row < bShape[0] and method=='2':
                    socket.send_multipart([method.encode('ascii'),A[:,row].tobytes(),B[row,:].tobytes()])
                    row+=1
                if row < aShape[0] and method=='3':
                    socket.send_multipart([method.encode('ascii'),A[row,:].tobytes(),B.tobytes(),str(bShape[0]).encode(),str(bShape[1]).encode()])
                    row+=1
                    
            
            if(method == '1' and row==0):                          
                socket.send_multipart([method.encode('ascii'),A[row,:].tobytes(),B.tobytes(),str(bShape[0]).encode(),str(bShape[1]).encode()])
                row=+1
            if method == '2' and row==0:
                socket.send_multipart([method.encode('ascii'),A[:,row].tobytes(),B[row,:].tobytes()])
                row=+1
            if method == '3' and row == 0:
                socket.send_multipart([method.encode('ascii'),A[row,:].tobytes(),B.tobytes(),str(bShape[0]).encode(),str(bShape[1]).encode()])
                row=+1
            if method == '4' and p==1:
                I,B,C,D = dividematriz(A)
                E,F,G,H = dividematriz(T)
                Ashape= len(I)
                print(p)
                socket.send_multipart([method.encode('ascii'), np.array(I).tobytes(), np.array(restamatriz(F,H)).tobytes(), str(Ashape).encode(), str(Ashape).encode(), str(p).encode()])
                p+=1

            
            if np.array(result).shape == (aShape[0],bShape[1]):
                socket.send_multipart([b'finish'])
        t1 = time()                
        print('Tiempo Transcurrido\t')
        print(np.array(result))
        print('{}'.format(t1-t0))
                
            
        
        
if __name__ == '__main__':
    main()