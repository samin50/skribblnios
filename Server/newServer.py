import socket
import threading
import random
import urllib.request
import time

#Client on the server sides that holds their attributes and waits for data
class ClientData():
    def __init__(self, conn, addr, server):
        self.name = None
        self.data = [None, None, 0, 0]
        self.isActive = True
        self.serverProperties = (conn, addr)
        self.serverObj = server
        self.dataThread = threading.Thread(target=self.listenData)
        self.dataThread.start()

    #Wait for data from clients
    def listenData(self):
        while self.isActive:
            try:
                data = self.serverProperties[0].recv(64).decode('utf-8')
            #If player disconnects
            except ConnectionResetError:
                self.isActive = False
                self.serverObj.processServerSide("SERVERCMD: !DISCONNECT " + self.name)
                print(f"Player {self.name} disconnected.")
                return
            if data:
                self.processData(data)
                if "!DRW" not in data:
                    print(f"Server received data from {self.name}")
        return

    #Process client side data
    def processData(self, data):
        #Server wide command
        if "SERVERCMD:" in data:
            self.serverObj.processServerSide(data)
            return
        #Set player name
        if "!SETNAME" in data:
            print(data)
            data = data.split("!SETNAME ")[1]
            data = data.split(" ")
            self.name = data[0]
            self.avatar = data[1]
            #Tell all players about new player
            self.data = [self.name, int(self.avatar), 0, 0]
            self.serverObj.updatePlayers()
            #self.serverObj.sendData("CLIENTCMD: !SENDPLAYER " + self.name + " " +self.avatar, True, self.name)
            return
        #Disconnect player
        if data == "!DISCONNECT":
            self.isActive = False #Disable player
            self.serverObj.processServerSide("SERVERCMD: !DISCONNECT " + str(self.name))
            return
    def getData(self):
        return self.data

    def sendClientData(self, data):
        self.serverProperties[0].send(str.encode(f"Server response: {data}\n"))
    
    def send(self, data):
        self.serverProperties[0].send(str.encode(f"{data}\n"))
    


class Server():
    def __init__(self, PORT, roundLength):
        self.roundLength = roundLength
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.settimeout(3600)
        self.isActive = True
        self.players = []
        try:
            self.address = urllib.request.urlopen('https://ident.me').read().decode('utf-8')
            self.server.bind((self.address, PORT))
        except Exception as e:
            print(e)
            print(f"Failed to bind to public IP: {self.address}, will now try binding to local IP.")
            self.address = socket.gethostbyname(socket.gethostname())
            self.server.bind((self.address, PORT))
        self.clientList = []
        self.server.listen()
        self.listenThread = threading.Thread(target=self.addClients)
        self.listenThread.start()
        self.next_drawer = None
        self.currentWord = None
        print(f"Server bind success @{self.address}")
    
    def startTimer(self):
        self.timer_thread = threading.Thread(target=self.roundTimer,daemon=True)
        self.timer_thread.start() 

    def roundTimer(self):
        self.sendData("CLIENTCMD: !STARTROUND " , True)
        time.sleep(self.roundLength)
        self.sendData("CLIENTCMD: !ENDROUND " , True)
    
    def updatePlayers(self):
        self.sendData("CLIENTCMD: !CLEARPLAYERS " , True)
        self.players = self.sortPlayers(self.players)
        for player in self.players:
            self.sendData(f"CLIENTCMD: !UPDATEPLAYERS {str(player)}" , True)
    
    def sortPlayers(self, players):
        players.sort(key=lambda list: list[2], reverse=True)
        for i in range(len(players)):
            players[i][3] = i+1
        return players

    
    #Add new clients as they connect
    def addClients(self):
        while self.isActive:
            try:
                conn, addr = self.server.accept()
                Player = ClientData(conn, addr, self)
                
                self.clientList.append(Player)
                conn.send(b"Welcome to the server!\n")
                print("New Player Joined!\n")
                if(len(self.clientList) == 1 ):
                    self.next_drawer = self.clientList[0]
                    conn.send(b'CLIENTCMD: !SET1STDRAWER')  #set first drawer
            
                
            except Exception as e:
                print(e)
                print("Server closed.")
                return
            
            
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

        #Draw function
        if "!DRW" in data:
            coords = data.split("!DRW ")[1]
            self.sendData("CLIENTCMD: !DRW " + coords, True, self.next_drawer.name)
        else:    
            print(f"Server: RECEIVED SERVER COMMAND: {data}")

        if "!RESETTRACKER" in data:
            self.sendData("CLIENTCMD: !RESETTRACKER", True, self.next_drawer.name)

        if "!CLEAR" in data:
            self.sendData("CLIENTCMD: !CLEAR", True, self.next_drawer.name)
        #Broadcast to all players
        #universal server commands
       

        if "!DISCONNECT" in data:
            #Remove player from list based on name
            playerNameToRemove = data.split("!DISCONNECT ")[1]
            for player in self.clientList:
                if player.name.strip() == playerNameToRemove.strip():
                    try:
                        player.sendClientData("Server: You have been disconnected.\n")
                    except:
                        print(player.name + " was forcibly disconnected on their side.")
                    player.isActive = False
                    self.clientList.remove(player)
                    # If the current drawer leaves, select a new one
                    if (player == self.next_drawer) and (len(self.clientList) > 0):
                        self.processServerSide("SERVERCMD: !DRAWERSELECT")
                    print(f"Server: Disconnected Player {playerNameToRemove}")
                    break
                self.updatePlayers()
                return
        #Chat function
        if "!BROADCAST" in data:
            message = data.split("!BROADCAST ")[1]
            name = message.split(": ")[0]
            if self.currentWord in message:
                self.sendData(f"!BROADCAST SERVER: Player {name} guessed the word!", True)
            self.sendData(data, True, name)
            return

        #Switch function  
        if "!SETSWITCH" in data:
            switches = data.split("!SETSWITCH ")[1]
            self.sendData("CLIENTCMD: !SETSWITCH " + switches, True, self.next_drawer.name)

        #choose who is drawing 
        if "!DRAWERSELECT" in data:
            temp = random.choice(self.clientList)
            while temp == self.next_drawer:
                temp = random.choice(self.clientList)
            self.next_drawer = temp
            #if self.next_drawer.name 
            whosdrawing = ("CLIENTCMD: !DRAWERSELECT " + self.next_drawer.name)
            self.sendData(whosdrawing, True)
            return   

        if data == "!KILL":
            self.closeServer()

        if "!DISCONNECT" in data:
            #Remove player from list based on name
            playerNameToRemove = data.split("!DISCONNECT ")[1]
            for player in self.clientList:
                if player.name.strip() == playerNameToRemove.strip():
                    try:
                        player.sendClientData("Server: You have been disconnected.\n")
                    except:
                        print(player.name + " was forcibly disconnected on their side.")
                    player.isActive = False
                    self.clientList.remove(player)
                    print(f"Server: Disconnected Player {playerNameToRemove}")
                    break
            return

        #     if "!COOORDINATES" in data:
            #     return_xy(self.next_drawer)
            #for when shan and shaheen done fpga and game
        if "!STARTROUND " in data:
            self.currentWord = data.split("!STARTROUND ")[1]
            print("Word set to: " + self.currentWord)
            self.sendData("CLIENTCMD: !STARTROUND", True, self.next_drawer.name)
            self.startTimer()


    #Send data
    def sendData(self, data, all=False, playerName=""):
        if all == False:
            for player in self.clientList:
                if player.name == playerName:
                    player.send(f"{data}")
        else:
            for player in self.clientList:
                #Ignore the player that did the broadcast if specified
                if player.name != playerName:
                    player.send(f"{data}")
    
    #Close server
    def closeServer(self):
        print("Closing server.")
        self.isActive = False
        while len(self.clientList) > 0:
            self.clientList[0].processData("!DISCONNECT")
        self.server.close()
        

if __name__ == "__main__":
    PORT = 9999
    roundLength = int(input("What will be the length of each round in the game? (seconds): "))
    server = Server(PORT, roundLength)

    

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
