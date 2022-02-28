import socket
import threading

class Server():
    def __init__(self, PORT):
        self.address = socket.gethostbyname(socket.gethostname())
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.server.setblocking(False)
        self.server.bind((self.address, PORT))
        self.clientList = []
        self.server.listen(2)
        self.listenThread = threading.Thread(target=self.listenClients)
        self.listenThread.start()
        self.dataThread = threading.Thread(target=self.listenData)
        self.dataThread.start()
        print(f"Server bind success @{self.address}")
    
    #Add new clients as they connect
    def listenClients(self):
        while True:
            conn, addr = self.server.accept()
            self.clientList.append([conn, addr])

    #Wait for data
    def listenData(self):
        while True:
            for i in range(len(self.clientList)):
                data = self.clientList[i][0].recv(1024).decode('utf-8')
                #If data is available from anyone
                if data:
                    print("data")
                if data == "!DISCONNECT":
                    print("Disconnected!")
                    self.closeServer()
                    return
    
    #Close server
    def closeServer(self):
        self.dataThread.join()
        self.listenThread.join()
        self.server.close()

PORT = 9999
server = Server(PORT)

    

