# Import socket module
import socket			
import os
import shutil
# Create a socket object
availableSocket = socket.socket()	


# Define the port on which you want to connect
port = 1337
localhost = '127.0.0.1'

def showMenu():
    print("Entrez une des commandes ci-dessous: ")
    print("TIME pour avoir le temps")
    print("IP pour avoir l'adresse ip")
    print("OS pour obtenir de l'information sur le systeme d'exploitation")
    print("FICHIER pour obtenir un fichier factice")
    print("EXIT pour quitter")

def getChosenOption():
    return str(input("Choix: ")).lower()

def notValid(request):
    return request not in ("time", "ip", "os", "fichier", "exit")

def showInvalidRequestMessage():
    print("Commande invalide!")

def isFileDownload(request):
    return request == "fichier"

def getFolderName():
    return "./downloadsFromServer/"

def alreadyCreated(folder):
    return os.path.exists(folder)

def deleteCreated(folder):
    shutil.rmtree(folder)

def createDestination(folder):
    os.mkdir(folder)

def sendUsing(availableSocket, request):
    availableSocket.send(request.encode())

def getResponseUsing(availableSocket):
    return availableSocket.recv(1024).decode()

def downloadAndSaveFileTo(folder, response):
    f = open(folder+"donneesTelecharges.txt", "a")
    f.write(response)
    f.close()

def showDownloadConfirmationTo(folder):
    print("Fichier donneesEnregistres.txt cree dans "+folder)

def show(response):
    print(response)

def connectToServerUsing(availableSocket):
    availableSocket.connect((localhost, port))

def disconnectFromServerUsing(availableSocket):
    availableSocket.close()	

connectToServerUsing(availableSocket)
show(getResponseUsing(availableSocket))
connectedToServer = True

while connectedToServer:
    showMenu()
    request = getChosenOption()

    if notValid(request):
        showInvalidRequestMessage()
        continue
    elif isFileDownload(request):
        folder = getFolderName()
        if alreadyCreated(folder):
            deleteCreated(folder)
        createDestination(folder)
        sendUsing(availableSocket, request)
        downloadAndSaveFileTo(folder, getResponseUsing(availableSocket))
        showDownloadConfirmationTo(folder)
    else:
        sendUsing(availableSocket, request)
        show(getResponseUsing(availableSocket))
        
disconnectFromServerUsing(availableSocket)    
    