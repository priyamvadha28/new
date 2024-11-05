import threading
import socket
import sys

lock=threading.Lock()

def receive_messages(client_socket):

    while True:
        try:
                message=client_socket.recv(1024).decode()
                if message:
                    with lock:
                        sys.stdout.write("\r\033[K")

                        print(f"Message from Server:{message}")

                        print("YOU:",end='',flush=True)
        except:
            client_socket.close()
            break

client_socket=socket.socket(socket.AF_INET6,socket.SOCK_STREAM)

host="localhost"
port=5002

client_socket.connect((host,port))

thread=threading.Thread(target=receive_messages,args=(client_socket,))
thread.start()

while True:
    try:
        message=input("YOU:")
        if message.lower()=="exit":
            client_socket.send("Client is exiting".encode('utf-8'))
            client_socket.close()
            break
        else:
            client_socket.send(message.encode('utf-8'))
    except:
        client_socket.close()
        break