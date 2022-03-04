import socket
import threading
import random 

#Client on the server sides that holds their attributes and waits for data
class ClientData():
    def __init__(self, conn, addr, server):
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
                self.isActive = False
                self.serverObj.processServerSide("SERVERCMD: !DISCONNECT " + self.name)
                print(f"Player {self.name} disconnected.")
                return
            if data:
                self.processData(data)
                print(f"Player {self.name} got data!")
        return

    #Process client side data
    def processData(self, data):
        #Server wide command
        if "SERVERCMD:" in data:
            self.serverObj.processServerSide(data)
        #Set player name
        if "!SETNAME" in data:
            self.name = data.split(" ")[1]
        #Disconnect player
        if data == "!DISCONNECT":
            print(f"Player {self.name} disconnected.")
            self.isActive = False
            self.serverObj.processServerSide("SERVERCMD: !DISCONNECT " + str(self.name))
        #Default send data back to client as well
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
        self.turn = False #turn hasnt started till drawer is chosen
        self.next_drawer = 0 
        
        print(f"Server bind success @{self.address}")
    
    #Add new clients as they connect
    def addClients(self):
        while self.isActive:
            conn, addr = self.server.accept()
            Player = ClientData(conn, addr, self)
            self.clientList.append(Player)
            conn.send(b"Welcome to the server!\n")
            print("\nNew Player Joined!")
            
            
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
                    self.clientList.remove(player)
                    break
            print(f"Server: Disconnected Player {playerNameToRemove}")
        #Broadcast to all players
        if "!BROADCAST" in data:
            message = data.split("!BROADCAST")[1]
            self.sendData(message, True)

        #choose who is drawing 
        if "!DRAWERSELECT" in data:
            self.turn = True
            randomize_drawer = random.randint(1, len(self.clientList))
            self.next_drawer = self.clientList[randomize_drawer-1]
            whosdrawing = self.next_drawer.name + " is now drawing! "
            self.sendData(whosdrawing, True)
            print(self.next_drawer.name + " is now drawing!")

    #Send data
    def sendData(self, data, all=False, playernum=0):
        if all == False:
            self.clientList[playernum].sendClientData(f"{data}")
        else:
            for player in self.clientList:
                player.sendClientData(f"{data}")
    
    #Close server
    def closeServer(self):
        for i in range(len(self.clientList)):
            self.clientList[i].processData("!DISCONNECT")
        self.isActive = False
        self.server.close()

PORT = 9999
server = Server(PORT)

    

"""
HOW IT WORKS:
When the server object detects a new client connecting to it, it creates a server-side object called client
that contains data that allows communication with that specific client, ie IP address and name. It appends this new client
to the list of existing clients to allow other functions to iterate through this list to send data.
Each client begins its own thread and listens for data on their channel, whenever a client recieves data,
it performs the processData command with the data it received, which currently to just printing the data it obtained back
to the client. 
If a client sends data that is prefixed with 'SERVERCMD:', the 'processServerSide' function in the Server object will run
the command instead of the client, and an implemented function is '!DISCONNECT' which will disconnect the client and remove it 
from the client list in the server object.
Add more functionality as you wish, and server wide commands can easily be implemented with 'processServerSide' by any client sending
the correct command, need to do stuff like determining the current drawer and managing the XY coords etc (refer to the diagram)
"""
