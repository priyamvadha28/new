import socket
import threading

clients = []

def handle_clients(client_socket, client_address):
    print(f"Client {client_address} has connected to the server")
    clients.append(client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"Received from {client_address}: {message}")
                broadcast(client_socket, message)  # Send to all other clients
        except:
            break

    print(f"Disconnected from {client_address}")
    clients.remove(client_socket)
    client_socket.close()

def broadcast(sender_socket, message):
    #print(f"Broadcasting message: {message}")
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(f"Broadcast: {message}".encode('utf-8'))
            except:
                clients.remove(client)
                client.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5002))
    server_socket.listen()
    print("Server started on localhost:5002")

    while True:
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(target=handle_clients, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
