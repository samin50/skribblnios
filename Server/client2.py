import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.71"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)
    print("Received message: ")
    print(client.recv(2048).decode(FORMAT))

send("55 55")
input()
send("100 55")
input()

send(DISCONNECT_MESSAGE)
print("end")