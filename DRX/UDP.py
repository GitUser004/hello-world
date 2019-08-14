import socket

class UDP():
    def __init__(self):
        self.localIp = ""
        self.localPort = 59386
        self.localAdder = (self.localIp,self.localPort)

        # self.destIp = "10.4.211.37"
        self.destIp = "192.168.208.129"
        self.destPort = 50001
        self.destAddr = (self.destIp,self.destPort)

        self.buffSize = 1024

        self.udpClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpSererSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpSererSocket.bind(self.localAdder)

    def sendToServer(self, data):
        self.udpClientSocket.sendto(data.encode(encoding='UTF-8'), self.destAddr)

    def receiveFromServer(self):
        print("waiting for message...")
        try:
            data, addr = self.udpSererSocket.recvfrom(self.buffSize)
        except BaseException:
            print(BaseException)
        else:
            self.destAddr = (addr[0],self.destPort)
            print(data.decode(encoding='UTF-8'), addr)
            return data.decode(encoding='UTF-8')
        return None

    def close(self):
        self.udpClientSocket.close()
        self.udpSererSocket.close()

if __name__ == "__main__":
    udp = UDP()
    data = "123测试"
    udp.sendToServer(data)
    udp.close()
