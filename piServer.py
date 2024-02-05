import socket
import time

bufferSize = 1024
msgFromServer = "Hello"
serverPort = 2222
serverIP = '127.0.0.1'
toSend = msgFromServer.encode('utf-8')
RPISocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RPISocket.bind((serverIP, serverPort))

print("UP")
msg, addr = RPISocket.recvfrom(bufferSize)
msg = msg.decode('utf-8')
print(msg)
RPISocket.sendto(toSend, addr)
