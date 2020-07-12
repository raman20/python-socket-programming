import socket
import threading
import pymongo

db = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = db['chatdb']
user = mydb['users']

HEADER = 1024
PORT = 9090
FORMAT = "utf-8"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
DISCONNECT_MSG = 'disconnect'
ACTIVE_USERS = {}

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn,addr):
    print(f"[NEW CONNECTION] -> {addr} connected")

    connected = True
    while connected:
        user = conn.recv(1024).decode(FORMAT)
        while not user in ACTIVE_USERS:
            conn.send("1".encode(FORMAT))
            user = conn.recv(1024).decode(FORMAT)
        else:
            conn.send("".encode(FORMAT))
        recv_conn = ACTIVE_USERS[user]
        msg = conn.recv(1024).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False
        print(f"[{addr}] {msg}")
        recv_conn.send(msg.encode(FORMAT))
        conn.send('[MESSAGE RECEIVED]'.encode(FORMAT))

    conn.close()

def auth(mac,conn):
    u = user.find_one({"mac":mac})
    if u:
        conn.send(" ".encode(FORMAT))
        ACTIVE_USERS[u.get("mac")] = conn
        return True
    return False

def create_new_user(mac,conn):
    conn.send('new'.encode(FORMAT))
    username = conn.recv(1024).decode(FORMAT)
    while user.find_one({"user":username}):
        conn.send("1".encode("utf-8"))
        username=conn.recv(1024).decode("utf-8")
    else:
        conn.send("".encode("utf-8"))
    user.insert_one({
        "_id":user.count()+1,
        "mac":mac,
        "username":username
        })
    ACTIVE_USERS[username] = conn

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        mac = conn.recv(1024).decode(FORMAT)
        if auth(mac,conn):
            thread = threading.Thread(target=handle_client,args=(conn,addr))
            thread.start()
        else:
            create_new_user(mac,conn)
            thread = threading.Thread(target=handle_client,args=(conn,addr))
            thread.start()

        print(f"[ACTIVE CONNECTION] -> {threading.activeCount()-1}")
        

print("[STARTING]......")
start()