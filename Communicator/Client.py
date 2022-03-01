import random
import socket
import threading

PORT = 9999
SERVER = "26.168.146.5"

class Client():
    def __init__(self, name, ip, port):
        self.name = name            
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((ip, port))
        self.isActive = True
        #Begin listening for data
        self.listenThread = threading.Thread(target=self.listenData)
        self.listenThread.start()
        self.sendServer("!SETNAME " + name)
    
    #Disable client
    def sendServer(self, data):
        self.server.send(data.encode('utf-8'))
        if data == "!DISCONNECT":
            self.isActive = False 
    
    #Always wait for data
    def listenData(self):
        while self.isActive:
            try:
                data = self.server.recv(1024).decode('utf-8')
                self.processData(data)
            except Exception as e:
                print(e)
    
    #Process recieved data
    def processData(self, data):
        print("\n" + data + '\n')

Player = Client("Player-" + str(random.randint(0, 100)), SERVER, PORT)

if __name__ == "__main__":
    while True:
        data = input("Send data: ")
        Player.sendServer(data)




"""HOW IT WORKS:
The client connects to the server and the first command it sends is a setname command,
current randomly generated

A thread begins to always listen for data from the server

Data is processed by the processData method, current just printing the data to console.

Sending !DISCONNECT will disconnect the current client, and will no longer have responses from the server

"""