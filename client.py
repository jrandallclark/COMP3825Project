#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter, ssl, pickle

def receive():
    while True:
        try:
            msg = conn.recv(BUFSIZ)
            chat_message = msg.decode("utf8")
            msg_list.insert(tkinter.END, chat_message)
        except UnicodeDecodeError:
            online_users = pickle.loads(msg)
            users.delete(0, tkinter.END)
            for x in online_users:
                users.insert(tkinter.END, x)
            
                
        except OSError:
            break

def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    conn.send(bytes(msg, "utf8"))
    if msg == ".exit":
        conn.close()
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

ADDR = '127.0.0.1'
PORT = 8083
HOSTNAME = 'localhost'
SERVER_CERT = 'server.pem'
AUTH = 'client.pem'
names = []


BUFSIZ = 4096
ADDR = ((ADDR, PORT))

socket = socket(AF_INET, SOCK_STREAM)
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=SERVER_CERT)
context.load_cert_chain(certfile=AUTH, keyfile=AUTH)
conn = context.wrap_socket(socket, server_side=False, server_hostname=HOSTNAME)
conn.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop() 