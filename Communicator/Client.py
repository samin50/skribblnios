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
        self.isDrawer = True # Had to set true by default to avoid weird server behaviour
        self.isActive = True
        self.server.connect((ip, port))
        self.isActive = True

        #Begin listening for data
        self.listenThread = threading.Thread(target=self.listenData, daemon=True)
        self.listenThread.start()
    
    def sendServer(self, data, requiresDrawer=False):
        #Can only send commands if drawer or for special commands like broadcast
        if self.isActive and (not requiresDrawer or self.isDrawer):
            self.server.send(data.encode('utf-8'))
            
            if data == "SERVERCMD: !DISCONNECT":
                self.isActive = False
                print("You have been disconnected from the server.")
                
            if data == "SERVERCMD: !KILL":
                self.isActive = False
                print("You have closed the server and are no longer connected.")
        else:
            print("COMMAND '" + data + "' rejected, insufficient priviliges.")

           
    
    def setGame(self, game):
        print("gameset")
        self.Game = game

    
            
    #Always wait for data
    def listenData(self):
        while self.isActive:
            try:
                #Causes issues on disconnect from other players as will be waiting for data
                data = self.server.recv(128).decode('utf-8')
                if len(data) > 0:
                    self.processData(data)  
            except Exception as e: #If connection fails
                print(e)
                self.isActive = False
                print("Error in connection to server, connection lost.")
                input()
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
            return
        if("CLIENTCMD: " in data):
            data = data.split("CLIENTCMD: ")[1]
            #First drawer
            if "!SET1STDRAWER" in data:
                self.isDrawer = True
                print("Set player to current drawer")
                return
            #Subsequent drawers
            if "!DRAWERSELECT" in data:
                name = data.split("!DRAWERSELECT ")[1]
                if self.name == name.strip():
                    print("Set player to current drawer")
                    self.isDrawer = True
                else:
                    self.isDrawer = False
                return
            #Switches
            if "!SETSWITCH" in data:
                switches = data.split("!SETSWITCH ")[1]
                codeStr = f"switch_update({switches}, True)"
                self.sendGame(codeStr)
                return
            #Drawing
            if "!DRW" in data:
                coords = data.split("!DRW ")[1]
                coords = coords.split()
                codeStr = f"draw({coords[0]}, {coords[1]}, True)"
                self.sendGame(codeStr)
                return
            else:
                print(f"Client: RECEIVED CLIENT COMMAND FROM SERVER: {data}")
            #When drawer lets go of space
            if "!RESETTRACKER" in data:
                self.sendGame("resetTracker()")
                return
            #When drawer presses clear
            if "!CLEARSCREEN" in data:
                self.sendGame("reset_canvas(True)")
                return
            if "!STARTROUND" in data:
                word = data.split("!STARTROUND ")[1]
                codeStr = f"startRound('{str(word).strip()}')"
                self.sendGame(codeStr)
                return
            if "!FINROUND" in data:
                self.sendGame("endRound()")
                return
            if "!CLEARPLAYERS" in data:
                self.sendGame("clearPlayers()")
                return
            if "!UPDATEPLAYERS" in data:
                playerdata = data.split("!UPDATEPLAYERS ")[1]
                player = playerdata.split(" ")
                codeStr = f"updatePlayers('{player[0]}', {player[1]}, {player[2]}, {player[3].strip()})"
                print(codeStr)
                self.sendGame(codeStr)
                return
            if "!SETTIME" in data:
                self.time = int(data.split("!SETTIME ")[1])
                return
            if "!ROUNDTIME" in data:
                roundtime = float(data.split("!ROUNDTIME ")[1])
                self.sendGame(f"word_reveal({roundtime})")
                return
            if "!SETBRUSHSIZE" in data:
                size = data.split("!SETBRUSHSIZE ")[1]
                codeStr = f"setBrush({size})"
                self.sendGame(codeStr)
                return

            


        #if data == "!COORDINATES":
        #       None
    def sendGame(self, code):
        if self.Game is None:
            return
        try:
            exec("self.Game." + code)
        except Exception as e:
            print(e)

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

