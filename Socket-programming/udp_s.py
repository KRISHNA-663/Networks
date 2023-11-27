import socket

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('localhost',12345))
while True:

    cd,ca=s.recvfrom(1024)
    print(cd)
    print(ca)
    s.sendto(cd,ca)
    s.close()
