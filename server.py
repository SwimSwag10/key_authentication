from http import client
import socket
import threading

# if you're running this online this HOST should be your own ip. Find with ifconfig
# when someone connects to your server they need to add the public ip. Find at myip.is
HOST = '127.0.0.1'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

# broadcast - broadcast is done to find clients trying to connect
def broadcast(message):
  for client in clients:
    client.send(message)

# handle - client is send to handle
def handle(client):
  while True:
    try:
      message = client.recv(1024)
      print(f"{nicknames[clients.index(client)]} says {message}")
      broadcast(message)
    except:
      index = clients.index(client)
      clients.remove(client)
      clients.close()
      nickname = nicknames[index]
      # this might be wrong. May have to use pop instead of remove.
      nicknames.remove(nickname)
      break

# recieve - wait for connections
def receive():
  while True:
    client, address = server.accept() 
    print(f'connected with {str(address)}!')

    client.send("NICK".enconde("utf-8"))
    nickname = client.recv(1024)

    nicknames.append(nickname)
    clients.append(client)

    print(f"Nickname of the client is {nickname}")
    print(f"-------- THIS IS A TEST FOR ENCODING --------".encode("utf-8"))
    broadcast(f"{nickname} connected to the server!\n".encode("utf-8"))
    client.send(f"Connected to the server".encode("utf-8"))

    # the comman adter the client for args is to ge the computer to recognize that this is a tuple
    thread = threading.Thread(target=handle, args=(client,))
    thread.start()

print("Server running...")
# we are calling the receive method because this is calling the handle method which is calling the broadcast method
receive()