import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('127.0.0.1',12345))
print("Connected to server")

msg=3
s.sendall(str(msg).encode())

data=s.recv(1024)
print(f'{data.decode()}')