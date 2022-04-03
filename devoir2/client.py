import socket			
import os
import shutil
import sys


available_socket = socket.socket()	

PORT = 1334
LOCALHOST = '127.0.0.1'
GOODBYE = "Au revoir"

def show_menu():
    print("""Entrez une des commandes ci-dessous: 
    TIME pour avoir le temps
    IP pour avoir l'adresse ip
    OS pour obtenir de l'information sur le systeme d'exploitation
    FICHIER pour obtenir un fichier factice
    EXIT pour quitter""")

def get_chosen_option():
    return str(input("Choix: ")).lower()

def not_valid(request):
    return request not in ("time", "ip", "os", "fichier", "exit")

def show_invalid_request_message():
    print("Commande invalide!")

def is_file_download(request):
    return request == "fichier"

def get_folder_name():
    return "./downloadsFromServer/"

def already_created(folder):
    return os.path.exists(folder)

def delete_created(folder):
    shutil.rmtree(folder)

def create_destination(folder):
    os.mkdir(folder)

def send_using(available_socket, request):
    available_socket.send(request.encode())

def get_response_using(available_socket):
    return available_socket.recv(1024).decode()

def download_and_save_file_to(folder, response):
    f = open(folder+"donneesTelecharges.txt", "a")
    f.write(response)
    f.close()

def show_download_confirmation_to(folder):
    print("Fichier donneesEnregistres.txt cree dans "+folder)

def connect_to_server_using(available_socket):
    available_socket.connect((LOCALHOST, PORT))

def disconnect_from_server_using(available_socket):
    available_socket.close()	
    sys.exit(0)

connect_to_server_using(available_socket)
print(get_response_using(available_socket))
connected_to_server = True

while connected_to_server:
    show_menu()
    request = get_chosen_option()

    if not_valid(request):
        show_invalid_request_message()
        continue
    elif is_file_download(request):
        folder = get_folder_name()
        if already_created(folder):
            delete_created(folder)
        create_destination(folder)
        send_using(available_socket, request)
        download_and_save_file_to(folder, get_response_using(available_socket))
        show_download_confirmation_to(folder)
    else:
        send_using(available_socket, request)
        response = get_response_using(available_socket)
        print(response)
        if response == GOODBYE:
            connected_to_server = False
        
disconnect_from_server_using(available_socket)    
    