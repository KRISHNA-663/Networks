import socket

ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ss.connect(('127.0.0.1',12345))

msg=3
ss.sendall(str(msg).encode())

data=ss.recv(1024)
print(f'{data.decode()}')