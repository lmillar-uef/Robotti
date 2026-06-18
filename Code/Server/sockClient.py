import socket 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connectSock(ip = "10.239.227.76", port = 6966):
    s.connect((ip, port))
    
def sendMessage(msg):
    print(f"sending: {msg}")
    s.sendall(bytes((msg + "\n"), "utf-8"))
    
def listenSock():
    return s.recv(1024).decode("utf-8").strip()

def shutDown():
    s.close()
    print("shutdown")
    
