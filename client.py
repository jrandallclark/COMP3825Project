#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import json

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print(msg)
            print(msg[0])
            if (msg[0] == '1'):
                names.append(msg[1:])
                print(names)
                users.insert(tkinter.END, msg[1:])
            else:
                msg_list.insert(tkinter.END, msg)
        except OSError:
            break

def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == ".exit":
        client_socket.close()
        top.quit()

def on_closing(event=None):
    my_msg.set(".exit")
    send()

top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar() 
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame) 
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.grid(row=0, column=0)

users_frame = tkinter.Frame(top)
user_scrollbar = tkinter.Scrollbar(users_frame) 
users = tkinter.Listbox(users_frame, height=15, width=20, yscrollcommand=user_scrollbar.set)
user_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
users.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
users_frame.grid(row=0, column=1)

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.grid(row=1, column=0)
send_button = tkinter.Button(top, text="Send", command=send)
send_button.grid(row=1, column=1)

top.protocol("WM_DELETE_WINDOW", on_closing)

HOST = '127.0.0.1'
PORT = 33000
names = []


BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop() 