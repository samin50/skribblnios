import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "146.169.129.17"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))
    while(True):
        msg = client.recv(2048).decode(FORMAT)
        print(msg)
        if(msg == "end"):
            break



send("55 55")
send("100 55")

send(DISCONNECT_MESSAGE)
print("end")