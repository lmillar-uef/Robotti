import socket 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connectSock(ip = "10.239.227.76", port = 5400):
    s.connect((ip, port))
    
def listenSock():
    return s.recv(1024).decode("utf-8")
