import socket
import argparse
import threading
import os
import sys
import glob

parser = argparse.ArgumentParser(description="This is the server for the multi threaded socket demo!")
parser.add_argument('--host', metavar='host', type=str, nargs = '?', default=socket.gethostname)
parser.add_argument('--port', metavar='port', type=int, nargs = '?', default=9999)
args = parser.parse_args()
clientslist = {}
list_flag = 0

print("Running the server: {} on port {}".format(args.host,args.port))

sck = socket.socket()
sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    sck.bind((args.host, args.port))
    sck.listen(5)
except Exception as e:
        raise SystemExit("Failed to bind {} on port {} reason {}".format(args.host,args.port,e))

def search_file(file_name):
    folder_path = './log'
    file = ""
    val = False
    for filename in glob.glob(os.path.join(folder_path, '*.txt')):
        with open(filename, 'r') as f:
            if file_name in f.read():
                file = str(f.name)
                val = True
                print("Found in")
                print(file)
                break
                
    return val,str(file)

def on_new_client(client, connection):
    ip = connection[0]
    port = connection[1]
    print("THe new connection was made from IP: {}, and port: {}!".format(ip,port))
    msg = client.recv(1024)
    hname = msg.decode()
    client.sendall("ak".encode())
    while True:        
        msg = client.recv(1024)
        print("The client @ {}:{} said: {}".format(ip,port,msg.decode()))
        fname = './log/{}.txt'.format(hname)
        if os.path.exists(fname):
            os.remove(fname)
        try:
            sample = open(fname, 'w+')
        except Exception as e:
            print("Unable to keep log reason {}".format(e))
        client.sendall("okk".encode())
        msg = client.recv(1024)
        while msg.decode() != "Updatedone":
            sample.write(msg.decode()+"\n")
            client.sendall(msg)
            msg = client.recv(1024)
        sample.close()
        print("The client @ {}:{} said: {}".format(ip,port,msg.decode()))
        
        msg = client.recv(1024)
        if msg.decode() == 'exit' or msg.decode() == '2':
            break
        print("The client @ {}:{} said: {}".format(ip,port,msg.decode()))
        if(msg.decode()== "1"):
            file_name = client.recv(1024).decode()
            print("The client @ {}:{} is searching for: {}".format(ip,port,file_name))
            res = search_file(file_name)
            client.sendall(("{}".format(res[0])).encode())
            client.recv(1024)
            if res[0]:
                res_ip_port = res[1].split("log/")[1].split(".txt")[0] 
                res_ip = res_ip_port.split(":")[0]
                res_port = res_ip_port.split(":")[1]
                if(res_ip == str(ip) and res_port == str(port)):
                    client.sendall(("Requested file is present in your system").encode())
                else:    
                    client.sendall(("Requested file is present in system:\nIP:{}, port:{}".format(res_ip,res_port)).encode())
            else:
                msg = "File not found in any servers!!"
                client.sendall(msg.encode())
            
        # reply = "You told me: {}".format(msg.decode())
        # client.sendall(reply.encode('utf-8'))
        
    print("The client from ip: {}, and port: {}, has gracefully diconnected!".format(ip,port))
    if os.path.exists(fname):
        os.remove(fname)
    del clientslist[connection]
    if bool(clientslist):
        print("The list of connected clients:")
        print(clientslist.keys())
    else:
        print("Client list is empty!!")
        print("Server Still running!!")
    client.close()
    
while True:
    try: 
        client, ip = sck.accept()
        clientslist.update({ip:client})
        threading._start_new_thread(on_new_client,(client, ip))
    except KeyboardInterrupt:
        files = glob.glob('./log/*')
        for f in files:
            os.remove(f)
        print(": Gracefully shutting down the server!")
        print(clientslist.keys())
        break
    except Exception as e:
        print(": Well I did not anticipate this: {}".format(e))
        break

sck.close()
