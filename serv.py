import socket 
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('127.0.0.1',12345))
s.listen()
print("server is listening")

cd,ca=s.accept()
print('address: ',cd)

while True:
    data=ca.recv(1024)
    if not data:
        break
    print('received from client:',data)
    ca.send('hello'.encode())
    s.close()
