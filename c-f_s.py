
from socket import *
server_port = 12000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('127.0.0.1', 12345))
server_socket.listen()
print('server is ready')
while True:
    connection_socket , addr = server_socket.accept()
    celsius_temperature = connection_socket.recv(1024).decode()
    celsius_temperature = float(celsius_temperature)
# Convert Celsius to Fahrenheit
    fahrenheit_temperature = (celsius_temperature * 9/5) + 32
# Send the converted temperature back to the client
    connection_socket.send(str(fahrenheit_temperature).encode())
    print(f'Celsius Temperature: {celsius_temperature}, Fahrenheit Temperature:{fahrenheit_temperature}')
    connection_socket.close()