import platform
import sys
import socket
from datetime import datetime

def setup_socket(port=1350):
    s = socket.socket()
    s.bind(('', port))
    s.listen()
    return s

# Setup socket
try:
    server_socket = setup_socket()
except Exception as err:
    print(f"[ERROR]: Failed to setup socket.\nDetails: {err}")
    sys.exit(1)

# Main loop and cleanup
try:
    BUFFER_SIZE = 1024
    while True:
        client, client_ip = server_socket.accept()
        client.send(f"Accepted client with addr: '{client_ip[0]}'. Waiting for data...".encode())
        
        # Main logic part
        data = client.recv(1024).decode()
        while data != 'exit':            
            if data == 'time':
                client.send(str(datetime.now().time()).encode())
            elif data == 'ip':
                client.send(str(client_ip).encode())
            elif data == 'os':
                client.send(str(platform.platform()).encode())
            elif data == 'fichier':
                filename="./donnees.txt"
                myfile = open(filename, "rb")
                client.send(myfile)
except InterruptedError: # If we interrupt using CTRL+C
    print("Terminating...")
    server_socket.close()    
except Exception as err:
    print(f"[ERROR]: {err}")
    sys.exit(1)