import socket

def Main():
    host = input("Enter host ip: ")
    port = int(input("Enter port number: "))
    
    s = socket.socket()
    
    try:
        s.connect((host, port))
    except Exception as e:
        raise SystemExit("Failed to connect {} on port {} \nreason: {}".format(host,port,e))
    
    filename = input("Filename ? -> ")
    if filename != 'q':
        s.send(filename.encode('utf-8'))
        data = s.recv(1024).decode('utf-8')
        if data[:6] == 'EXISTS':
            filesize = float(data[6:])
            message = input("File Exists, "+str(filesize)+"bytes, Download ?? (Y/N) -> ")
            if message == 'Y':
                s.send(("OK").encode('utf-8'))
                f = open("new_"+filename, 'wb')
                data = s.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print("{0:.2f}".format((totalRecv/float(filesize))*100)+ "% \done")
                print("Donwload Complete!")
                print("Now your Present Working Directory contains: ")
                
        else:
            print("File doesn't exist!")
    s.close()

if __name__ == "__main__":
    Main()