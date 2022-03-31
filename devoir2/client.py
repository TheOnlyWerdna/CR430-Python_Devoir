import socket			
import os
import shutil
import sys

PORT = 1338
LOCALHOST = '127.0.0.1'
EXITMESSAGE="Deconnecte du serveur. Au revoir."
INVALIDCOMMANDMESSAGE="Commande invalide!"
FILENAME="donneesTelecharges.txt"
EXITCOMMAND="exit"
FILESAVEDIN="Fichier " +FILENAME+ " cree dans "
FILECOMMAND="file"
TIMECOMMAND="time"
IPCOMMAND="ip"
OSCOMMAND="os"
CHOICE="Choix: "
APPENDTOFILE="a"
DOWNLOADFOLDERNAME="./downloadsFromServer/"
MAXDATASIZE=1024
MENU="""
Entrez une des commandes ci-dessous: 
TIME pour avoir le temps.
IP pour avoir l'adresse ip.
OS pour obtenir de l'information sur le systeme d'exploitation.
FICHIER pour obtenir un fichier factice.
EXIT pour quitter.
"""
availableSocket = socket.socket()
	

def getChosenOption():
    return str(input(CHOICE)).lower()

def notValid(request):
    return request not in (TIMECOMMAND, IPCOMMAND, OSCOMMAND, FILECOMMAND, EXITCOMMAND)

def isFileDownload(request):
    return request == FILECOMMAND

def getFolderName():
    return DOWNLOADFOLDERNAME

def alreadyCreated(folder):
    return os.path.exists(folder)

def deleteCreated(folder):
    shutil.rmtree(folder)

def createDestination(folder):
    os.mkdir(folder)

def sendUsing(availableSocket, request):
    availableSocket.send(request.encode())

def getResponseUsing(availableSocket):
    return availableSocket.recv(MAXDATASIZE).decode()

def downloadAndSaveFileTo(folder, response):
    f = open(folder+FILENAME, APPENDTOFILE)
    f.write(response)
    f.close()

def showDownloadConfirmationTo(folder):
    print(FILESAVEDIN+folder)

def show(response):
    print(response)

def connectToServerUsing(availableSocket):
    availableSocket.connect((LOCALHOST, PORT))

def disconnectFromServerUsing(availableSocket):
    availableSocket.close()	

def userSendsExit(request):
    return request == EXITCOMMAND

def stopClient():
    sys.exit(0)

connectToServerUsing(availableSocket)
show(getResponseUsing(availableSocket))
connectedToServer = True

while connectedToServer:
    show(MENU)
    request = getChosenOption()

    if notValid(request):
        show(INVALIDCOMMANDMESSAGE)
        continue
    elif isFileDownload(request):
        if alreadyCreated(getFolderName()):
            deleteCreated(getFolderName())
        createDestination(getFolderName())
        sendUsing(availableSocket, request)
        downloadAndSaveFileTo(getFolderName(), getResponseUsing(availableSocket))
        showDownloadConfirmationTo(getFolderName())
    elif userSendsExit(request):
        show(EXITMESSAGE)
        sendUsing(availableSocket, request)
        disconnectFromServerUsing(availableSocket)
        stopClient()
    else:
        sendUsing(availableSocket, request)
        show(getResponseUsing(availableSocket))
        
disconnectFromServerUsing(availableSocket)    
    