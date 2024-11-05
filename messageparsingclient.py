import socket
import threading 
import sys

clients=[]

def handle_clients(client_socket,client_address):

    print(f"Client {client_address} has connected to the server")

    clients.append(client_socket)

    while True:
        try:
         message=client_socket.recv(1024).decode()

         if message:
            broadcast(client_socket,message)
        except:
           break

    print("Disconnected from connection")

    clients.remove(client_socket)
    client_socket.close()

def broadcast(client_socket,message):
   for client in clients:
      try:
        if client!=client_socket:
            client.send(message.encode('utf-8'))
      except:
         clients.remove(client)
         client.close()

server_socket=socket.socket(socket.AF_INET6,socket.SOCK_STREAM)

host="localhost"
port=5002

server_socket.bind((host,port))

server_socket.listen()

while True:
   client_socket,addr=server_socket.accept()
   thread=threading.Thread(target=handle_clients,args=(client_socket,addr))
   thread.start()