import socket
import time
from threading import Timer

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('0.0.0.0', 5400))
s.listen()
print('Server is now running.')

def background_controller():
    msg = input("Send message:")
    print(f"sending: {msg}")
    clientSocket.sendall(bytes(msg, "utf-8"))
    Timer(1, background_controller).start()
    

while True:
    clientSocket, address = s.accept()
    clientSocket.send(bytes("connected", "utf-8"))
    
    print(f"Connection from (address) has been established.")
    background_controller()
