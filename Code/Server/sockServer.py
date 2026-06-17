import socket
import time
from threading import Timer
from threading import Thread
from threading import Lock

##Don't send data at the same time from different threads
send_lock = Lock()

def connect():
    clientSocket, address = s.accept()
    with send_lock:
        clientSocket.sendall(bytes("connected\n", "utf-8"))
    return clientSocket, address
    
def send(clientSocket):
    while True:
        msg = input("Send message:") + "\n"
        with send_lock:
            clientSocket.sendall(bytes(msg, "utf-8"))

def listen():
    while True:
        data = clientSocket.recv(1024)
        if not data:
            print("Client disconnected.")
            break
        print("Recieved:", data.decode("utf-8"))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 6967))
s.listen(1)

print('Server is now running.')

clientSocket, address = connect()
print(f"Connection from {address} has been established.")

listener_thread = Thread(target=listen, daemon=True)
sender_thread   = Thread(target=send, daemon=True)

    
try:
    listener_thread.start()
    sender_thread.start()
    while True:
        clientSocket, address = connect()
except KeyboardInterrupt:
    pass
finally:
    print("Shutdown...")
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    
    
