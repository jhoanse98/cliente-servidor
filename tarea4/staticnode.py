import zmq
import sys
import hashlib
import os
import time
from uuid import getnode as get_mac
from random import uniform
from hasher import hashitos
from math import ceil
import intervals as I
import json


def update(id0,id1,MAX = 70,MIN = 0):
    interval = I.openclosed(id1,id0)
    if interval.is_empty():   
        return I.open(id1,MAX) | I.closed(MIN,id0)
    else:
        return interval


if __name__ == "__main__":

    context = zmq.Context()
    predSocket = context.socket(zmq.PAIR)
    successSocket = context.socket(zmq.PAIR)
    clientSocket = context.socket(zmq.ROUTER)
    #displaySocket = context.socket(zmq.DEALER)
    if  len(sys.argv )== 5:
        status=sys.argv[5]
        clientAddress=sys.argv[4]
        successAddress = sys.argv[3]
        myPort = sys.argv[2]
        ID = sys.argv[1]
    predSocket.bind("tcp://*:{}".format(myPort))
    successSocket.connect("tcp://{}".format(successAddress))
    clientSocket.bind("tcp://*:{}".format(clientAddress))
    PredID=-1

    MAX_BUFFER=1024*1024

    if status=="yes":
        successSocket.send_multipart([b'ID',ID.encode()])
    else:
        pass

    myinterval=I.empty()

    poller = zmq.Poller()
    poller.register(predSocket,zmq.POLLIN)
    poller.register(clientSocket,zmq.POLLIN)
    servidores = []
    while True:
        socks = dict(poller.poll(1024))
        if predSocket in socks:
            op,*message = predSocket.recv_multipart()
            if op==b'ID':
                if int(message[0].decode()) == PredID:
                    pass
                else:
                    PredID = int(message[0].decode())
                    myInterval = update(int(ID),PredID)
                    successSocket.send_multipart([b'ID',ID.encode()])
                    print(myInterval)
        if clientSocket in socks:
            print("clientSocket")
            who,op,*message = clientSocket.recv_multipart()
            print(who,op)
            if op == b'send':        
                fileName, fileExt, mainHash, *hashis = message
                numeroHashis = len(hashis)
                for hashito in hashis:
                    name ,identificador = hashito.decode().split(':')
                    if int(identificador) in myInterval:
                        resultado = name+';'+clientAddress
                        servidores.append(resultado.encode())
                    else:
                        numeroServidores = str(len(servidores))        
                        successSocket.send_multipart([b'doYouHave',hashito,str(numeroHashis).encode(),numeroServidores.encode(),who])
                numeroServidores = len(servidores)
                if numeroServidores == numeroHashis:
                    respuesta = [who,b'ok']+servidores
                    clientSocket.send_multipart(respuesta)
                    servidores = []
            elif op == b'sending':
                #namefile= message[0].decode().split(':')[0]
                namefile= message[0].decode()
                print("Vamos a subir un archivo")
                with open(namefile,'ab') as f:  
                        f.write(message[1])
                clientSocket.send_multipart([who,b'ok'])
            elif op == b'download':
                numeroHashis = len(message)
                for hashito in message:
                    name ,identificador = hashito.decode().split(':')
                    if int(identificador) in myInterval:
                        resultado = name+';'+clientAddress
                        servidores.append(resultado.encode())
                    else:
                        numeroServidores = str(len(servidores))        
                        successSocket.send_multipart([b'doYouHave',hashito,str(numeroHashis).encode(),numeroServidores.encode(),who])
                numeroServidores = len(servidores)
                if numeroServidores == numeroHashis:
                    respuesta = [who,b'ok']+servidores
                    clientSocket.send_multipart(respuesta)
                    servidores = []
            elif op == b'downloading':
                print('se esta bajando un archivo')
                print(message[0])
                with open(message[0],'rb') as target:
                    data=target.read(MAX_BUFFER)
                    clientSocket.send_multipart([who,b'data',data,message[0]])

                
