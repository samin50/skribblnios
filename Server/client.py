import socket

HEADER = 64
PORT = 9999
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "26.168.146.5"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)
    print("Received message: ")
    print(client.recv(2048).decode(FORMAT))

send("55 55")
send("100 55")
send("SERVERCMD: lessgoooo")

send(DISCONNECT_MESSAGE)
print("end")
