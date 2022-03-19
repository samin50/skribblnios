import random
import socket
import threading

PORT = 9999
SERVER = '146.169.183.125'

class Client():
    def __init__(self, name, ip, port): #game
        self.Game = None
        self.name = name            
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server.settimeout(600)
        self.isDrawer = False
        self.isActive = True
        try:
            self.server.connect((ip, port))
        except:
            print("Unable to connect to server, check IP or if server is running.")
            return
        

        #Begin listening for data
        self.listenThread = threading.Thread(target=self.listenData)
        self.listenThread.start()
        self.sendServer("!SETNAME " + name, False)
    
    def sendServer(self, data, requiresDrawer=False):
        #Can only send commands if drawer or for special commands like broadcast
        if not requiresDrawer or (self.isActive and self.isDrawer):
            self.server.send(data.encode('utf-8'))
            
            if data == "SERVERCMD: !DISCONNECT":
                self.isActive = False
                print("you have now disconnected from the server")
                
            if data == "SERVERCMD: !KILL":
                self.isActive = False
                print("you have now closed the server and no longer connected")
        else:
            print("COMMAND '" + data + "' rejected, insufficient priviliges.")

           
    
    def setGame(self, game):
        self.Game = game

    
            
    #Always wait for data
    def listenData(self):
        i = 0
        j = 0 
        while self.isActive:
            
            i+=1
            try:
                #Causes issues on disconnect from other players as will be waiting for data
                data = self.server.recv(64).decode('utf-8')
                j+=1
                if len(data) > 0:
                    self.processData(data)  #If connection fails
            except Exception as e:
                print(e)
                self.isActive = False
                print("Error in connection to server, connection lost.")
                input()
         
            if(i+j == 10000):
                 self.isActive = False
                 print("you have now disconnected from the server")
                 
        return
    def setGame(self, game):
        self.Game = game
        return
    #Process recieved data
    #listening to the server
    def processData(self, data):
        #Chat messages
        if "!BROADCAST" in data:
            message = data.split("!BROADCAST ")[1]
            codeStr = "addOtherMessages('" + message[:-1] + "')"
            self.sendGame(codeStr)
        if("CLIENTCMD: " in data):
            data = data.split("CLIENTCMD: ")[1]
            print(f"Client: RECEIVED CLIENT COMMAND FROM SERVER: {data}")
            #First drawer
            if "!SET1STDRAWER" in data:
                self.isDrawer = True
                print("Set player to current drawer")
            #Subsequent drawers
            if "!DRAWERSELECT" in data:
                name = data.split("!DRAWERSELECT ")[1]
                if self.name == name.strip():
                    print("Set player to current drawer")
                    self.isDrawer = True
                else:
                    self.isDrawer = False
            #Switches
            if "!SETSWITCH" in data:
                switches = data.split("!SETSWITCH ")[1]
                codeStr = f"switch_update({switches}, True)"
                print(codeStr)
                self.sendGame(codeStr)
            #Drawing
            if "!DRW" in data:
                coords = data.split("!DRW ")[1]
                coords = coords.split()
                codeStr = f"draw({coords[0]}, {coords[1]}, True)"
                print(codeStr)
                self.sendGame(codeStr)
            #When drawer lets go of space
            if "!RESETTRACKER" in data:
                self.sendGame("resetTracker()")

        #if data == "!COORDINATES":
        #       None
    def sendGame(self, code):
        if self.Game is None:
            return
        exec("self.Game." + code)

    def isDrawing(self):
        return self.isDrawer
              

if __name__ == "__main__":
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

