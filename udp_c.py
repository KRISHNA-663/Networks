import socket

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect(('localhost',12345))

while True:
    cd,ca=s.recvfrom(1024)
    print(cd)
