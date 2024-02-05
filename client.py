import socket
import time

class Client:

    IP = '169.254.243.173'
    PORT = 2222
    PROTOCOL = 'utf-8'
    BUFFERSIZE = 1024

    def __init__(self, ip = IP, port = PORT):
        self._ip = ip
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def sendmsg(self, msg):

        self._socket.sendto(msg.encode(self.PROTOCOL), (self._ip, self._port))
        data, _ = self._socket.recvfrom(self.BUFFERSIZE)
        return data.decode(self.PROTOCOL)


# msgFromClient = 'Goodbye'
# toSend = msgFromClient.encode('utf-8')
# serverAddr = ('169.254.243.173', 2222)
# bufferSize = 1024

# clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# print("Sending")
# clientSocket.sendto(toSend, serverAddr)
# print("Reciecving")
# data, addr = clientSocket.recvfrom(bufferSize)
# data = data.decode('utf-8')

# print(f"From server {data}")
# print("Server IP", addr[0])
# print("Server Port", addr[1])
    
# c = Client()
# print(c.sendmsg('s-1000'))
# time.sleep(1)
# print(c.sendmsg('s-500'))
# time.sleep(1)
# print(c.sendmsg('s-100'))
# time.sleep(1)
# print(c.sendmsg('s-0'))
# print(c.sendmsg('sa'))


