# Import socket module
import socket			
import os
# Create a socket object
s = socket.socket()		

# Define the port on which you want to connect
port = 1339

# connect to the server on local computer
s.connect(('127.0.0.1', port))
response = s.recv(1024).decode()
print(response)
connectedToServer = True

while connectedToServer:
    print("Entrez une des commandes ci-dessous: ")
    print("TIME pour avoir le temps")
    print("IP pour avoir l'adresse ip")
    print("OS pour obtenir de l'information sur le systeme d'exploitation")
    print("FICHIER pour obtenir un fichier factice")
    print("EXIT pour quitter")
    requestToServer = str(input("Choix: ")).lower()

    if requestToServer not in ("time", "ip", "os", "fichier", "exit"):
        print("Commande invalide!")
        continue
    elif requestToServer == "fichier":
        folderToCreate = "./downloadsFromServer/"
        os.mkdir(folderToCreate)
        s.send(requestToServer.encode())
        response = s.recv(1024).decode()
        f = open(folderToCreate+"donneesTelecharges.txt", "a")
        f.write(response)
        f.close()
        print("Fichier donneesEnregistres.txt cree dans "+folderToCreate)
    else:
        s.send(requestToServer.encode())
        response = s.recv(1024).decode()
        print(response)
        
    
    
# close the connection
s.close()	
	
