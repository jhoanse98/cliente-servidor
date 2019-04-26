import zmq
import sys
from mX import *
from metodostrassen import *
import numpy as np
def main():
    if len(sys.argv) != 2:
        print('Debe ser llamado con un puerto')
        exit()
    else:
        context = zmq.Context()
        socket = context.socket(zmq.ROUTER)
        port = sys.argv[1]
        socket.bind('tcp://*:{}'.format(port))
        print('Server Alive')

        while True:
            ident,*result= socket.recv_multipart()
            #print(result[0].decode(), np.frombuffer(result[1]), np.frombuffer(result[2]), result[3].decode(), result[4].decode())
            if(result[0] == b'1'):
                print("ejecutando metodo 1")
                bShape = [int(result[3].decode()),int(result[4].decode())]
                result = method1(result[1],result[2],bShape)
                socket.send_multipart([ident,bytes(port,'ascii'),b'ok',result.tobytes()])
            elif(result[0] == b'2'):
                result = method2(result[1],result[2])
                socket.send_multipart([ident,bytes(port,'ascii'),b'ok',result.tobytes()])
            if(result[0] == b'3'):
                bShape = [int(result[3].decode()),int(result[4].decode())]
                result = method1(result[1],result[2],bShape)
                socket.send_multipart([ident,bytes(port,'ascii'),b'ok',result.tobytes()])
            elif result[0] == b'finish':
                socket.send_multipart([ident,b'finish'])
            if(result[0] == b'4'):
                print("ejecutando metodo 4")
                shapes = [int(result[3].decode()), int(result[4].decode())]
                Pn=strassen(result[1],result[2],True, shapes)
                socket.send_multipart([ident, bytes(port,'ascii'), b'ok', np.array(Pn).tobytes()])
            

if __name__ == '__main__':
    main()