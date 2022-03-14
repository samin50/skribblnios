import random
import socket
import threading

class Client():
    def __init__(self, name, ip, port, gameInstance=None):
        self.gameInstance = gameInstance
        self.name = name            
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((ip, port))
        self.isActive = True

        #Begin listening for data
        self.listenThread = threading.Thread(target=self.listenData, daemon=True)
        self.listenThread.start()
        self.sendServer("!SETNAME " + name)
    
    def sendServer(self, data):
        if self.isActive:
            self.server.send(data.encode('utf-8'))
            
            if data == "!DISCONNECT":
                self.isActive = False
                print("you have now disconnected from the server")
                
            if data == "SERVERCMD: !KILL":
                self.isActive = False
                print("you have now closed the server and no longer connected")
            
    #Always wait for data
    def listenData(self):
        while self.isActive:
            try:
                #Causes issues on disconnect from other players as will be waiting for data
                data = self.server.recv(1024).decode('utf-8')
                if len(data) > 0:
                    self.processData(data)
            #If connection fails
            except Exception as e:
                self.isActive = False
                print("Error in connection to server, connection lost.")
                input()
        return
    def setGame(self, game):
        self.Game = game
        return
    #Process recieved data
    def processData(self, data):
        print("\n" + data + '\n')

if __name__ == "__main__":
    PORT = 9999
    SERVER = '26.168.146.5'
    Player = Client("Player-" + str(random.randint(0, 100)), SERVER, PORT)
    while True:
        data = input("Send data: ")
        Player.sendServer(data)




"""HOW IT WORKS:
The client connects to the server and the first command it sends is a setname command,
current randomly generated

A thread begins to always listen for data from the server

Data is processed by the processData method, current just printing the data to console.

Sending !DISCONNECT will disconnect the current client, and will no longer have responses from the server

command examples:

x -> Server Response: x
!DISCONNECT -> diconnects player
SERVERCMD: !BROADCAST x -> sends message x to all currently connected players

"""
