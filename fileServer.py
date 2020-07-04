import socket
import threading            #handle request from users (multiple users)
import os

def RetrFile(name, sock):
    filename = sock.recv(1024).decode('utf-8')
    if os.path.isfile(filename):
        sock.send(("EXISTS " + str(os.path.getsize(filename))).encode('utf-8'))
        userResponse = sock.recv(1024).decode('utf-8')
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
        sock.close()
    else:
        sock.send("ERR")
    sock.close()

def Main():
    host = '192.168.0.103'
    port = 5000
    
    sample = open('./_cache/log_self.txt', 'w')
    print('{}:{}'.format(host,port), file = sample) 
    sample.close()
      
    s = socket.socket()
    s.bind((host,port))
    s.listen(5)
    print("Server Started...")
    while True:
        c, addr = s.accept()
        print("client connected ip:<" + str(addr) + ">")
        t = threading.Thread(target=RetrFile, args=("retrThread", c))
        t.start()    
    s.close()

if __name__ == "__main__":
    Main()