import socket
import pickle

class Client_side:
   def __init__(self): 
         self.client = socket.socket # type of connection determined by indraneel and ziyad ,# how the serevr string comes in which is also determined by indraneel and ziyad)
         self.host = #determined by Zi and Ind in the server file.
         self.port = 2323
         self.p = self.connect()
         print(self.connect()) # prints that we have connected 

   def getPosition(self):
        return self.position

   def connection_with_self(self):
        try:
            self.client.connect(self.host,self.port)
            return pickle.loads(self.client.recv(1024))
        except:
            pass 

   def send_data(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv())
        except socket.error as error:
            print(error)
