import socket
from uuid import getnode as get_mac

HEADER = 1024
PORT = 5050
FORMAT = "utf-8"
SERVER = "192.168.43.73"
ADDR = (SERVER,PORT)
DISCONNECT_MSG = 'disconnect'
RECV_NAME = None


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


def connect():
    client.connect(ADDR)
    send(str(msg(get_mac())).encode("utf-8"))
    recv_data = recv()
    if recv_data == 'new':
        username = input('[NEW USER DETECTED] choose a username to register yourself:-> ')
        send(username)
        while recv():
            username = input("[TRY ANOTHER USERNAME]:-> ")
        print("[REGISTERED SUCCESFULLY]")

def send(message,user=None):
    if not user:
        client.send(message)
        print(recv())
    client.send(message,user)
    print(recv())

def recv():
    return client.recv(1024).decode(FORMAT)

connect()
print('type "exit" to end connection or "new" for new receiver')
while True:
    user = input("[USER]>>>")
    client.send(user.encode(FORMAT))
    while recv():
        user = input(f"{user} is not available try again:-> ")
        client.send(user.encode(FORMAT))
    msg = input("[MSG]>>> ")
    if msg != 'exit':
        if user:
            send(msg,user)
            continue
        send(msg)
    else:
        send(DISCONNECT_MSG)
        break
