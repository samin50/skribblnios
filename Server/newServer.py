import socket
import threading

#Client on the server sides that holds their attributes and waits for data
class Client():
    def __init__(self, name, index, conn, addr, server):
        self.name = name
        self.index = index
        self.isActive = True
        self.serverProperties = (conn, addr)
        self.serverObj = server
        self.dataThread = threading.Thread(target=self.listenData)
        self.dataThread.start()
    
    #Wait for data from clients
    def listenData(self):
        while self.isActive:
            try:
                data = self.serverProperties[0].recv(1024).decode('utf-8')
            #If player disconnects
            except ConnectionResetError:
                print(f"Player {self.name} disconnected.")
                self.isActive = False
                self.serverObj.processServerSide("SERVERCMD: !DISCONNECT " + self.index)
                return
            if data:
                print(f"Player {self.name} got data!")
                self.processData(data)
        return

    #Process client side data
    def processData(self, data):
        if "SERVERCMD:" in data:
            self.serverObj.processServerSide(data)
        if data == "!DISCONNECT":
            print(f"Player {self.name} disconnected.")
            self.isActive = False
            self.serverObj.processServerSide("SERVERCMD: !DISCONNECT " + str(self.name))
        #Data processing for each client
        self.sendClientData(data)
        return

    def sendClientData(self, data):
        self.serverProperties[0].send(str.encode(f"Server response: {data}"))


class Server():
    def __init__(self, PORT):
        self.address = socket.gethostbyname(socket.gethostname())
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isActive = True
        self.server.bind((self.address, PORT))
        self.clientList = []
        self.server.listen()
        self.listenThread = threading.Thread(target=self.addClients)
        self.listenThread.start()
        print(f"Server bind success @{self.address}")
    
    #Add new clients as they connect
    def addClients(self):
        while self.isActive:
            index = len(self.clientList)
            Name = index
            conn, addr = self.server.accept()
            Player = Client(Name, index, conn, addr, self)
            self.clientList.append(Player)
            conn.send(b"Welcome to the server!\n")
            
            
    #Process individual clients for data
    def processClientSide(self, data, all=True, player=0):
        if all==True:
            for i in range(len(self.clientList)):
                self.clientList[i].processData(data)
            else:
                self.clientList[player].processData(data)
        return

    #Process data on server side
    def processServerSide(self, data):
        data = data.split("SERVERCMD: ")[1]
        print(f"Server: RECEIVED SERVER COMMAND: {data}")
        if data == "!KILL":
            self.closeServer()
        if "!DISCONNECT" in data:
            #Remove player from list based on name
            playerNameToRemove = data.split(" ")[1]
            for player in self.clientList:
                if player.name == playerNameToRemove:
                    self.clientList.remove(playerNameToRemove)
                    break
            print(f"Server: Disconnected Player {playerNameToRemove}")

        return

    #Send data
    def sendData(self, data, all=False, player=0):
        if all == False:
            self.clientList[player][0].send(str.encode(f"Server response: {data}"))
        else:
            for i in range(len(self.clientList)):
                self.clientList[i][0].send(str.encode(f"Server response: {data}"))
    
    #Close server
    def closeServer(self):
        for i in range(len(self.clientList)):
            self.clientList[i].processData("!DISCONNECT")
        self.isActive = False
        self.server.close()

PORT = 9999
server = Server(PORT)

    

