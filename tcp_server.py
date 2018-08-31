from socket import *

HOST = ''
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
    print("waiting for connecting...")
    tcpCliSock, addr = tcpSerSock.accept()
    print("...connected from:",addr)

    while True:
        data = tcpCliSock.recv(BUFSIZE).decode()
        if not data:
            break
        print(">>", data)
        tcpCliSock.send(("receive "+data).encode())
    tcpCliSock.close()
tcpSerSock.close()
