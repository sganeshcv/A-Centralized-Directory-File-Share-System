# A-Centralized-P2P-Directory-System
The Project consists of two main parts/process:
The Central Directory 
The Peers
The Central Directory is implemented in the python file “centralDirectory”. The project demo was done by running this file in loaclhost(127.0.0.1). 
Command:  python3 centralizedDirectory.py --host 127.0.0.1 --port 5555

The peers has to run multiple files as they have to get connected to the network and then they have to connect to the centralized directory running in the localhost. 
Command to connect to the network(host: 192.168.0.103, port: 3300):
            python3 peer.py --host 192.168.0.103 --port 3300
Command to connect to the centralizedDirectory running in localhost:
            python3 node.py --host 127.0.0.1 --port 5555

After the peers are connected to the Directory, it gets updated and then the peer can make requests for any file. If the system/peer who has the file is connected to the Directory it will return the address of that peer to the one who requested. Now the peer can choose whether to connect to the new peer to download the file or not. All it has to do is enter the ip address and the port of the destination in the newly prompted bash shell. 
