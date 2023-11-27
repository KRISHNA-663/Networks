import socket

ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.bind(('127.0.0.1',12345))
ss.listen()

c_d,c_a=ss.accept()

print("address",c_a)
data=c_d.recv(1024)

da=int(data)*80;


c_d.sendall(str(da).encode())

ss.close()
