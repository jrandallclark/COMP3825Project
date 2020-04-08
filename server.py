#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import pickle

def accept_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Welcome to chat! Enter your name.", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

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

HOST = ''
PORT = 33000
BUFSIZ = 4096
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Listening...")
    ACCEPT_THREAD = Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
