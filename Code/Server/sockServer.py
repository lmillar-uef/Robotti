import socket
import time
from threading import Timer
from threading import Thread

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('0.0.0.0', 8702))
s.listen()
print('Server is now running.')

def background_controller():
    msg = input("Send message:")
    clientSocket.send(bytes(msg, "utf-8"))
    Timer(1, background_controller).start()

def listen():
    #process msg
    print(clientSocket.recv(1024).decode("utf-8"))

listener_thread = Thread(target=listen, daemon=True)

    
try:
    while True:
        clientSocket, address = s.accept()
        clientSocket.send(bytes("connected", "utf-8"))
        print(f"Connection from {address} has been established.")
        listener_thread.start()
        background_controller()
        
    
    
except KeyboardInterrupt:
    print("Shutdown...")
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    
    
