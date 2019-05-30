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

        
        if  len(sys.argv )== 7:
            successAddress = sys.argv[1]
            myPort = sys.argv[2]
            clientPort = sys.argv[3]
            successAddressClient=sys.argv[4]
            ID = sys.argv[5]
            status = sys.argv[6]
            
            
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
            newSocket.send_multipart([b'new',ID.encode(),myPort.encode(),clientPort.encode()])
            poller.register(newSocket,zmq.POLLIN)
            displaySocket.send_multipart([b'new', ID.encode(), myPort.encode(), successAddress.encode(), newSocket.identity, b'79'])
        else:
            pass

        myInterval = I.empty()
        predID = 0
        print("corriendo server")
        while True:
            socks = dict(poller.poll(1024))
            if predSocket in socks:
                print("PREDSOCKET")
                op,*message = predSocket.recv_multipart()
                print(op,message)
                if op == b'id':
                    predID = int(message[0].decode())
                    myInterval = update(int(ID),predID)
                    displaySocket.send_multipart([b'id', str(predID).encode(), ID.encode()])
                    print(myInterval)

                if op == b'updateSuccs':
                    if message[0].decode()==ID:
                        print("mi sucesor era: {}".format(message[2].decode()))
                        print("mi nuevo sucesor es: {}".format(message[3].decode()))
                        #print(successAddress)
                        successSocket.disconnect("tcp://{}".format(successAddress))
                        successAddress="localhost:{}".format(message[1].decode())
                        successAddressClient="localhost:{}".format(message[4].decode())
                        time.sleep(5)
                        successSocket.connect("tcp://{}".format(successAddress))
                        #print(successAddress)
                        successSocket.send_multipart([b'idNew', ID.encode()])

                    else:
                        print("mi sucesor no es: {}".format(message[3].decode()))
                        print("mi succesor es:{}".format(successAddress))
                        successSocket.send_multipart([b'updateSuccs', message[0], message[1], message[2], message[3],message[4]])

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
                    NewsuccessAddressClient=message[2].decode()
                    if newID in myInterval:
                        print("yes")
                        successSocket.send_multipart([b'updateSuccs',str(predID).encode(), message[1], ID.encode(), str(newID).encode(),message[2]])
                        time.sleep(5)
                        clientSocket.send_multipart([who,b'updatePred',myPort.encode(),successAddress.encode(), successAddressClient.encode(),str(predID).encode()])
                        predID=newID
                    else:
                        print("je ne sais pas")
                        print(successAddressClient)
                        clientSocket.send_multipart([who, b'newConnection', successAddressClient.encode(),clientPort.encode()]) 
                
                    
            if newSocket and newSocket in socks:
                print('NEWSOCKET')
                status, *message = newSocket.recv_multipart()
                if status == b'updatePred':
                    print(successAddress)
                    successAddress = 'localhost:{}'.format(message[0].decode())
                    print("yo soy {} y mi sucesor es:{}".format(ID,successAddress))
                    predID=int(message[3].decode())
                    successAddressClient=message[2].decode()
                    successSocket.connect("tcp://{}".format(successAddress))
                    time.sleep(5)
                    print(ID)
                    successSocket.send_multipart([b'idNew',ID.encode()])
                if status == b'newConnection':
                    print("no esta, toca nueva conexion")
                    print(message[1].decode())
                    print(successAddress)
                    newSocket.disconnect("tcp://localhost:{}".format(message[1].decode()))
                    print(message[0].decode())
                    newSocket.connect("tcp://{}".format(message[0].decode()))
                    time.sleep(5)
                    newSocket.send_multipart([b'new',ID.encode(),myPort.encode(),successAddressClient.encode()])