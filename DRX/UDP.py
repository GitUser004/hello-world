import socket

class UDP():
    def __init__(self):
        self.localIp = ""
        self.localPort = 59386
        self.localAdder = (self.localIp,self.localPort)

        self.destIp = "10.4.211.37"
        self.destPort = 50001
        self.destAddr = (self.destIp,self.destPort)

        self.buffSize = 1024

        self.udpClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpSererSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpSererSocket.bind(self.localAdder)

    def sendToServer(self, data):
        self.udpClientSocket.sendto(data.encode(), self.destAddr)

    def receiveFromServer(self):
        print("waiting for message...")
        data, addr = self.udpSererSocket.recvfrom(self.buffSize)
        self.destAddr = addr
        print(data.decode(), addr)
        return data.decode()

    def close(self):
        self.udpClientSocket.close()
        self.udpSererSocket.close()

if __name__ == "__main__":
    udp = UDP()
    data = "1234测试"
    udp.sendToServer(data)
    udp.close()
