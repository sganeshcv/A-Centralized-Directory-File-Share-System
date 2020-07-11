import socket
import argparse
import os
import threading           #to run the server search commands commands that we receve

parser = argparse.ArgumentParser(description="This is the client for the multi threaded socket server")
parser.add_argument('--host', metavar='host', type=str, nargs = '?', default=socket.gethostname)
parser.add_argument('--port', metavar='port', type=int, nargs = '?', default=9999)
args = parser.parse_args()

print("Connecting to directory: {} on port {}".format(args.host,args.port))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
    try:
        sck.connect((args.host, args.port))
    except Exception as e:
        raise SystemExit("Failed to connect {} on port {} reason {}".format(args.host,args.port,e))
    print("Connecting to the centralized directory!!")
    sample = open('./_cache/log_self.txt', 'r')
    Lines = sample.readlines()
    host_ip = (Lines[0].split(":")[0])
    host_port = (Lines[0].split(":")[1].split("\n")[0])
    sample.close()
    sck.sendall(("{}:{}".format(host_ip,host_port)).encode('utf-8'))
    sck.recv(1024)
    while True:
        print("Performing Update to the Centralized Directory")
        sck.sendall("Updating".encode('utf-8'))
        sck.recv(1024)
        files = filter(os.path.isfile, os.listdir( os.curdir ) )  # files only
        for file in files:
            sck.sendall(str(file).encode('utf-8'))
            data = sck.recv(1024)
        sck.sendall("Updatedone".encode('utf-8'))            
        print("Update Complete")
        print("Menu:")
        print("1. Make a Request")
        print("2. Exit")
        msg = input("choose option: ")
        sck.sendall(msg.encode('utf-8'))
        if msg == "exit" or msg == "2":
            print("Exiting the Program!!")
            break
        elif msg == "1":
            file_name = input("Enter the name of the file you are looking for: ")
            sck.sendall(file_name.encode('utf-8'))
            data = sck.recv(1024)
            sck.sendall("ok".encode())
            if data.decode:
                data = sck.recv(1024)
                print("\nServer responce was : {}".format(data.decode('utf-8')))
                v = input("\nDo you wish to connect to the system? (Y/N):")
                if v == "Y":
                    os.system("gnome-terminal -- python3 peerConnect.py")
            else:
                data = sck.recv(1024)
                print("\nServer responce was : {}".format(data.decode('utf-8')))
            
        print("\nRestarting Connection\n")
    sck.close()
