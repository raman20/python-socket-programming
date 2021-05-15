# Fib microservice with threading

from os import truncate
from socket import *
from threading import Thread


def fibServer(addr):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(addr)
    sock.listen(5)
    while(True):
        client, address = sock.accept()
        print("connection", address)
        Thread(target=fib_handler, args=(client,), name=str(addr)).start()


def fib_handler(client):
    while True:
        req = client.recv(100)
        if not req:
            break

        n = int(req)
        result = fib(n)
        resp = str(result).encode('ascii')+b'\n'
        client.send(resp)
    print("closed")


def fib(n):
    if(n <= 2):
        return 1
    else:
        return fib(n-1) + fib(n-2)


if __name__ == "__main__":
    fibServer(('', 9090))
