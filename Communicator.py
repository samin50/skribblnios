import socket
import pickle

class Client_side:
   def __init__(user): 
         user.client = socket.socket # type of connection determined by indraneel and ziyad ,# how the serevr string comes in which is also determined by indraneel and ziyad)
         user.host = #determined by Zi and Ind in the server file.
         user.port = 2323
         user.p = user.connect()
         print(user.connect()) # prints that we have connected 

   def getPosition(user):
        return user.position

   def connection_with_user(user):
        try:
            user.client.connect(user.host,user.port)
            return pickle.loads(user.client.recv(1024))
        except:
            pass 

   def send_data(user, data):
        try:
            user.client.send(pickle.dumps(data))
            return pickle.loads(user.client.recv())
        except socket.error as error:
            print(error)

