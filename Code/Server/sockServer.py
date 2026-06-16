import socket
import time
from threading import Timer
from threading import Thread

def connect():
    clientSocket, address = s.accept()
    clientSocket.sendall(bytes("connected\n", "utf-8"))
    return clientSocket, address
    
def send():
    while True:
        msg = input("Send message:") + "\n"
        clientSocket.sendall(bytes(msg, "utf-8"))

def listen(clientSocket):
    while True:
        data = clientSocket.recv(1024)
        if not data:
            print("Client disconnected.")
            break
        print("Recieved:", data.decode("utf-8"))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 6751))
s.listen(1)

print('Server is now running.')

clientSocket, address = connect()
print(f"Connection from {address} has been established.")

listener_thread = Thread(target=listen, args=(clientSocket,), daemon=True)

    
try:
    listener_thread.start()
    send(clientSocket)
    while True:
        clientSocket, address = connect()
        
        #listener_thread.start()
        background_controller()
        listen()
        
    
    
except KeyboardInterrupt:
    pass
finally:
    print("Shutdown...")
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    
    
