import socket
import time
from threading import Timer
from threading import Thread

def connect():
    clientSocket, address = s.accept()
    clientSocket.send(bytes("connected", "utf-8"))
    return clientSocket, address
    
def background_controller():
    msg = input("Send message:")
    clientSocket.send(bytes(msg, "utf-8"))
    Timer(1, background_controller).start()

def listen():
    #process msg
    print(clientSocket.recv(1024).decode("utf-8"))
    Timer(1, listen).start()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('0.0.0.0', 7549))
s.listen()
print('Server is now running.')

#clientSocket, address = connect()
#listener_thread = Thread(target=listen, daemon=True)
    
try:
    while True:
        clientSocket, address = connect()
        print(f"Connection from {address} has been established.")
        #listener_thread.start()
        background_controller()
        listen()
        
    
    
except KeyboardInterrupt:
    pass
finally:
    print("Shutdown...")
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    
    
