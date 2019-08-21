import socket

LOCALIP = ""
LOCALPORT = 50001
DESTIP = "10.4.211.37"
DESTPORT = 59386


class UDP:
    def __init__(self,localIp = LOCALIP,localPort=LOCALPORT,destIp=DESTIP,destPort=DESTPORT):
        self.localIp = localIp
        self.localPort = localPort
        self.localAdder = (self.localIp, self.localPort)

        self.destIp = destIp
        self.destPort = destPort
        self.destAddr = (self.destIp, self.destPort)

        self.buffSize = 1024

        self.udpClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpSererSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpSererSocket.bind(self.localAdder)

    def __del__(self):
        self.udpClientSocket.close()
        self.udpSererSocket.close()

    def sendToServer(self, data, destIp=DESTIP, destPort=DESTPORT):
        self.udpClientSocket.sendto(data.encode(encoding='UTF-8'), (destIp, destPort))

    def receiveFromServer(self):
        print("waiting for message...")
        try:
            data, addr = self.udpSererSocket.recvfrom(self.buffSize)
        except BaseException:
            print(BaseException)
        else:
            self.destAddr = (addr[0], self.destPort)
            print(data.decode(encoding='UTF-8'), addr)
            return (data.decode(encoding='UTF-8'),addr)
        return (None,None)

    def close(self):
        self.udpClientSocket.close()
        self.udpSererSocket.close()


if __name__ == "__main__":
    udp = UDP()
    data = "123测试"
    udp.sendToServer(data)
    udp.close()
