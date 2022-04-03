import platform
import sys
import socket
from datetime import datetime

def setup_socket(port=1334):
    s = socket.socket()
    s.bind(('', port))
    s.listen()
    return s

def send_using(client, response):
    client.send(response)

def get_file_data():
    filename="./donnees.txt"
    my_file = open(filename, "rb")
    my_file_data = my_file.read()
    my_file.close()
    return my_file_data

try:
    server_socket = setup_socket()
except Exception as err:
    print(f"[ERROR]: Failed to setup socket.\nDetails: {err}")
    sys.exit(1)

try:
    BUFFER_SIZE = 1024
    
    while True:
        client, client_ip = server_socket.accept()
        client.send(f"Client connecte avec ip: '{client_ip[0]}'. En attente de requetes".encode())
        connected_to_client = True
        
        while connected_to_client: 
            client.settimeout(20.0)
            clientRequest = client.recv(1024).decode()
            client.settimeout(None)
            print(str(clientRequest))           
            if clientRequest == 'time':
                send_using(client, str(datetime.now().time()).encode())
                print(str(datetime.now().time()))
            elif clientRequest == 'ip':
                send_using(client, client_ip[0].encode())
                print(client_ip[0])
            elif clientRequest == 'os':
                send_using(client, platform.platform().encode())
                print(platform.platform())
            elif clientRequest == 'fichier':
                print("Envoi du fichier complete avec succes")
                send_using(client, get_file_data())
            else:
                send_using(client, "Au revoir".encode())
                print("Fermeture du serveur.")
                server_socket.close()  
                sys.exit(0)
                
except InterruptedError: 
    print("Terminating...")
    server_socket.close()   
    sys.exit(1) 
except socket.timeout:
    print("Client inactif pendant plus de 20 secondes. Fermeture du serveur.")
    server_socket.close()  
    sys.exit(1)
except Exception as err:
    print(f"[ERROR]: {err}")
    server_socket.close()  
    sys.exit(1)