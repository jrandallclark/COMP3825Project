#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import ssl, pickle

def accept_connections():
    while True:
        client, client_address = socket.accept()
        conn = context.wrap_socket(client, server_side=True)
        print("%s:%s has connected." % client_address)
        conn.send(bytes("Welcome to chat! Enter your name.", "utf8"))
        addresses[conn] = client_address
        Thread(target=handle_client, args=(conn,)).start()

def handle_client(client):
    name = client.recv(BUFSIZ).decode("utf8")
    names.append(name)
    welcome = 'Welcome %s! If you ever want to quit, type .exit to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    user_list = pickle.dumps(names)
    broadcast(user_list)

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes(".exit", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.close()
            names.remove(clients[client])   
            user_list = pickle.dumps(names)
            del clients[client]
            broadcast(user_list)
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

def broadcast(msg, prefix=""):
    for sock in clients:
        try:
            sock.send(bytes(prefix, "utf8")+msg)
        except BrokenPipeError:
            print('Broken pipe')
            del clients[sock]

clients = {}
addresses = {}
names = []

ADDR = '127.0.0.1'
PORT = 8083
BUFSIZ = 4096
CERT = 'server.pem'
KEY = 'server.pem'
CERTS_LIST = 'client.pem'

socket = socket(AF_INET, SOCK_STREAM)
socket.bind((ADDR, PORT))

if __name__ == "__main__":
    socket.listen(5)
    print("Listening...")
    
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(certfile=CERT, keyfile=KEY)
    context.load_verify_locations(cafile=CERTS_LIST)

    ACCEPT_THREAD = Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    socket.close()
