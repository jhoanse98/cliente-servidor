#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

def getServerNumber():
    #Funcion encargada de calcular el id del servidor
    mac = ':'.join(['{:02x}'.format((get_mac() >> ele) & 0xff) for ele in range(0,8*6,8)][::-1])
    #serverId = (mac+';'+str(uniform(0,(2**160)-1))).encode('ascii')
    serverId = mac.encode('ascii')
    hasher = hashlib.sha1(serverId).digest()
    serverId = int.from_bytes(hasher, "big") 
    return serverId

def update(id0,id1,MAX = 16,MIN = 0):
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
        displaySocket = context.socket(zmq.DEALER)

        displaySocket.connect("tcp://localhost:9999")

        
        if  len(sys.argv )== 6:
            successAddress = sys.argv[1]
            myPort = sys.argv[2]
            clientPort = sys.argv[3]
            ID = sys.argv[4]
            status = sys.argv[5]
            
            
        else:
            print("no hay argumentos suficientes")
            exit()


        predSocket.bind("tcp://*:{}".format(myPort))
        clientSocket.bind("tcp://*:{}".format(clientPort))
        clientSocket.identity= ID.encode()

        poller = zmq.Poller()
        poller.register(predSocket,zmq.POLLIN)
        poller.register(clientSocket,zmq.POLLIN)

        newSocket = None
        if status == 'start':
            successSocket.connect("tcp://{}".format(successAddress))
            displaySocket.send_multipart([ID.encode(), b'start', b' mi sucesor es : ', successAddress.encode(), b'mi puerto es : ', myPort.encode()])
            successSocket.send_multipart([b'id',ID.encode()])
            

            

        elif status == 'new':
            newSocket = context.socket(zmq.DEALER)
            newSocket.identity = ID.encode()
            newSocket.connect("tcp://{}".format(successAddress))
            newSocket.send_multipart([b'new',ID.encode(),myPort.encode()])
            poller.register(newSocket,zmq.POLLIN)
            displaySocket.send_multipart([b'new', ID.encode(), myPort.encode(), successAddress.encode(), newSocket.identity, b'79'])
        else:
            pass

        myInterval = I.empty()
        predID = 0
        print("corriendo server")
        while True:
            socks = dict(poller.poll(2048))
            if predSocket in socks:
                print("PREDSOCKET")
                op,*message = predSocket.recv_multipart()
                print(op,message)
                if op == b'id':
                    #print("recibo algo")
                    #print(message)
                    predID = int(message[0].decode())
                    myInterval = update(int(ID),predID)
                    displaySocket.send_multipart([b'id', str(predID).encode(), ID.encode()])
                    print(myInterval)
                    #print(type(myInterval))

                if op == b'updateSuccs':
                    if message[0].decode()==ID:
                        print("mi sucesor era: {}".format(message[2].decode()))
                        print("mi nuevo sucesor es: {}".format(message[3].decode()))
                        #print(successAddress)
                        successSocket.disconnect("tcp://{}".format(successAddress))
                        time.sleep(5)
                        successAddress="localhost:{}".format(message[1].decode())
                        successSocket.connect("tcp://{}".format(successAddress))
                        #print(successAddress)
                        successSocket.send_multipart([b'idNew', ID.encode()])
                    else:
                        print("mi sucesor no es: {}".format(message[3]))
                        successSocket.send_multipart([b'updateSuccs', message[0], message[1], message[2], message[3]])


                    """
                    displaySocket.send_multipart([ID.encode(), b'updateSuccs', successAddress.encode()])
                    successSocket.disconnect("tcp://{}".format(successAddress))
                    successAddress = "localhost:{}".format(message[1].decode())
                    print(" new success adress {}".format(successAddress))
                    print(myInterval)
                    successSocket.connect("tcp://{}".format(successAddress))
                    successSocket.send_multipart([b'idNew',ID.encode()])
                    displaySocket.send_multipart([b'desconexion de ',successAddress.encode(), str(predID).encode(), str(myInterval).encode(), b'nueva conexion con: ', successAddress.encode(), b'109'])
                    """

                if op == b'idNew':
                    print("update interval")
                    myInterval = update(int(ID),int(message[0].decode()))

                    print(myInterval)

            if clientSocket in socks:
                print("clientSocket")
                who,op,*message = clientSocket.recv_multipart()
                print(who,op,message)
                if op == b'new':
                    newID = int(message[0].decode())
                    newPort = message[1].decode()
                    if newID in myInterval:
                        print("yes")
                        successSocket.send_multipart([b'updateSuccs',str(predID).encode(), message[1], ID.encode(), str(newID).encode()])
                        time.sleep(5)
                        clientSocket.send_multipart([who,b'updatePred',myPort.encode(),successAddress.encode(), clientPort.encode(),str(predID).encode()])

                        """
                        print("yes")
                        print("nuevo puerto de predecesor : {}".format(newPort))
                        displaySocket.send_multipart([ID.encode(), b'escucho a mi predecesor por: ', myPort.encode(), b'mi sucesor es: ', successAddress.encode() ])
                        successSocket.send_multipart([b'updateSuccs',str(newID).encode(),newPort.encode()]) #aqui esta problema 
                        #successSocket.disconnect("tcp://{}".format(successAddress))
                        displaySocket.send_multipart([b'updateSuccs', str(newID).encode(), newPort.encode(),successAddress.encode()])
                        clientSocket.send_multipart([who,b'updatePred',myPort.encode(),successAddress.encode(), clientPort.encode()])
                        
                        print("hola no deberia salir")
                        #successSocket.disconnect("tcp://{}".format(successAddress))
                        """
                        """newSuccsAddrs = "localhost:{}".format(newPort)
                        successSocket.connect("tcp://{}".format(newSuccsAddrs))
                        print(newSuccsAddrs)
                        successSocket.send_multipart([b'test',ID.encode(),b'no deberia estar aqui'])"""
                        
                    else:
                        print("no")
                    predID=newID
                    
            if newSocket and newSocket in socks:
                print('NEWSOCKET')
                status, *message = newSocket.recv_multipart()
                if status == b'updatePred':
                	#newSocket.disconnect("tcp://localhost:{}".format(message[2].decode))
                    #print(message)
                    #print("port: {}".format(message[0].decode()))
                    successAddress = 'localhost:{}'.format(message[0].decode())
                    predID=int(message[3].decode())
                    #print(successAddress)
                    successSocket.connect("tcp://{}".format(successAddress))
                    #print("Id nuevo servidor: {}".format(ID))
                    time.sleep(5)
                    #print(ID)
                    #print(successAddress)
                    successSocket.send_multipart([b'idNew',ID.encode()])
                    #print(ID)
                    #print(successAddress)