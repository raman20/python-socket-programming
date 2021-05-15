# Fib microservice with coroutines

from socket import *
from collections import deque
from select import select

tasks = deque()
recv_wait = {}
send_wait = {}
def run():
    while any([tasks, recv_wait, send_wait]):

        while not tasks:
            #wait for i/o
            can_recv, can_send, [] = select(recv_wait, send_wait, [])
            for i in can_recv:
                tasks.append(recv_wait.pop(i))
            for i in can_send:
                tasks.append(send_wait.pop(i))

        task = tasks.popleft()
        try:
            why, what = next(task)
            if why == 'recv':
                recv_wait[what] = task
            elif why == 'send':
                send_wait[what] = task
            else:
                raise RuntimeError("Error");

        except StopIteration:
            print("task done")

def fibServer(addr):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(addr)
    sock.listen(5)
    while(True):
        yield 'recv', sock
        client, address = sock.accept()
        print("connection", address)
        tasks.append(fib_handler(client))


def fib_handler(client):
    while True:
        yield 'recv', client
        req = client.recv(100)
        if not req:
            break

        n = int(req)
        result = fib(n)
        resp = str(result).encode('ascii')+b'\n'
        yield 'send', client
        client.send(resp)
    print("closed")


def fib(n):
    if(n <= 2):
        return 1
    else:
        return fib(n-1) + fib(n-2)


if __name__ == "__main__":
    tasks.append(fibServer(('', 9090)))
    run();
