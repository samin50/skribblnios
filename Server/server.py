import socket
import threading
import time
import pickle

SIZE = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR)


def handle_client(conn, addr, player_id):
  print(f"[NEW CONNECTION] {addr} connected.")

  connected = True
  runtime = 0

  while connected:
    runtime += 1
    if(runtime == 1):
      conn.send(str.encode("Welcome to the game!!"))

    msg = conn.recv(1024).decode(FORMAT)

    if msg == DISCONNECT_MESSAGE:
      connected = False

    print(f"[{addr}] {msg}")
    conn.send(str.encode("    Time is     "))
    conn.send("Msg received biatch".encode(FORMAT))

  conn.close()



def start(player_id):
  server.listen(2)
  print(f"[LISTENING] Server is listening on {SERVER}")
  while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr, player_id))
    thread.start()
    player_id += 1
    print(f"[ACTIVE CONNECTIONS] {player_id}")

if __name__ == '__main__':
  print("[STARTING] server is starting...")
  start(0)

# To select player, randomly choose a number from 1-5 and put in the code to 
# match with the player id



# Code for broadcasting message to all clients
# my_clients = [] 
# def addclientsthread(sock): 
#     global my_clients
#     conn, addr = sock.accept()
#     my_clients += [conn]
#     print('Client connected on ' + addr[0])
#     start_new_thread(clientthread, (conn,))

# def sendallclients(message): 
#     for client in my_clients : 
#         client.send(message)