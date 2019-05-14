import zmq
import hashlib
import hash  as hasher
from math import ceil
import os
import json
import sys




def getHashis(archivo,size,MAX_BUFFER = 1024*1024*10):
    l = []
    hashcomplete=hasher.hasheador(archivo,size,MAX_BUFFER).encode()
    l.append(hashcomplete)
    rango = ceil(size/MAX_BUFFER)
    with open(archivo,'rb') as f:
        for i in range(0, rango):
            f.seek(i*MAX_BUFFER)
            data=f.read(MAX_BUFFER)
            hashi=hasher.hashitos(data)
            l.append(hashi.encode())
    return l

if __name__ == "__main__":
    context=zmq.Context()
    socketproxy=context.socket(zmq.REQ)
    socketproxy.connect("tcp://localhost:5555")
    
    MAX_BUFFER=1024*1024*10

    #socketproxy.send_multipart(hashlist)

    servers = {}
    print("=====================================\n")
    print('BIENVENIDO AL SERVIDOR DE ARCHIVOS\n\t')
    print('=====================================')
    identity = input('Ingrese su username:').encode()
    while True:
        print('=====================================')
        opc = input('Ingrese algun comando: (help para ayuda o exit para salir)  \n')
        op = opc.split(' ')
        if op[0] == 'exit':
            #socket.send_multipart([b'',b'exit'])
            #message = socket.recv()
            break
        elif op[0] == 'help':
            print('Lista de Comandos:\n\t')
            print('* send filename\n')
            print('* download filename\n')
        
        elif op[0] == 'send':
            archivo = op[1]
            filename, file_extension = os.path.splitext(archivo)
            size= os.path.getsize(archivo)
            print('Obteniendo lista de servidores')
            hashlist=[b'client',b'send',filename.encode(),file_extension.encode()]
            hashish = getHashis(archivo,size)
            hashlist +=hashish
            
            socketproxy.send_multipart(hashlist)
            status, *response = socketproxy.recv_multipart()
            if status == b'error':
                print(response[0].decode())
            else:
                print("Procesando")
                i = 0
                for r in response:
                    with open(archivo,'rb') as f:
                        f.seek((i*MAX_BUFFER)+1)
                        data=f.read(MAX_BUFFER)
                    hashname=hashish[i+1]
                    if r.decode() in servers:
                        servers[r.decode()].send_multipart([b'sending',hashname,data])
                    else:
                        servers[r.decode()] = context.socket(zmq.DEALER)
                        socket = servers[r.decode()]
                        socket.identity = identity
                        socket.connect("tcp://{}".format(r.decode()))
                        socket.send_multipart([b'sending',hashname,data])
                    i+=1
                print("Terminado\t\n")
                print("Archivo guardado como: {}".format(hashish[0].decode()))
        elif op[0] == 'download':
            indice=0            
            archivo = op[1]
            print('Obteniendo lista de servidores')
            lista = [b'client',b'download',archivo.encode()]
            socketproxy.send_multipart(lista)
            status, *response = socketproxy.recv_multipart()
            if status == b'error':
                print(response[0].decode())
            else:
                servers = {}
                serversend={}
                fullName, *ips = response
                for s in ips:
                    print(s.decode())
                    key,value = s.decode().split(';')
                    servers[key] = value
                print(fullName.decode())
                print(servers.values())
                serverip = [values for values in servers.values()]
                serverhashis=[keys for keys in servers.keys()]
                for ip in serverip:
                	print('hola')
                	print(ip)
                	if ip in serversend:
                		serversend[ip].send_multipart([b'downloading',serverhashis[indice].encode()])
                		print('la ip es:{}, el hash almacenado es:{}'.format(ip, serverhashis[indice]))
                		data=serversend[ip].recv_multipart()
                		with open(fullName, 'ab') as descarga:
                			descarga.write(data[1])
                		indice+=1
                		print(indice)
                	else:
                		serversend[ip]=context.socket(zmq.DEALER)
                		socket=serversend[ip]
                		socket.identity=identity
                		socket.connect("tcp://{}".format(ip))
                		socket.send_multipart([b'downloading', serverhashis[indice].encode()])
                		print('estamos en else')
                		data=serversend[ip].recv_multipart()
                		print('estamos despues de recv')
                		with open(fullName, 'ab') as descarga:
                			descarga.write(data[1])
                		indice+=1
                		print(indice)
