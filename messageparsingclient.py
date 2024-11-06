import socket
import threading

def listen_for_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"\n{message}")
                print("You: ", end='', flush=True)  # Prompt for new input after server message
        except:
            print("Disconnected from the server.")
            client_socket.close()
            break

def main():
    client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5002))
    print("Connected to server at localhost:5002")

    listen_thread = threading.Thread(target=listen_for_messages, args=(client_socket,))
    listen_thread.start()

    while True:
        message = input("You: ")
        if message.lower() == "exit":
            client_socket.sendall("Client is exiting".encode('utf-8'))
            client_socket.close()
            break
        else:
            client_socket.sendall(message.encode('utf-8'))

if __name__ == "__main__":
    main()
