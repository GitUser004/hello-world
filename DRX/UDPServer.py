import socket
from time import ctime

HOST = ''
PORT = 50001
BUFSIZE = 1024
ADDR = (HOST, PORT)

udpSererSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSererSocket.bind(ADDR)

while True:
    print("waiting for message...")
    data, addr = udpSererSocket.recvfrom(BUFSIZE)
    print(data.decode(encoding='UTF-8'), addr)
    # udpSererSocket.sendto(("your message [%s] %s" %(ctime(), data.decode())).encode(), addr)
    # print("receive msaage and return to :",addr)


udpSererSocket.close()