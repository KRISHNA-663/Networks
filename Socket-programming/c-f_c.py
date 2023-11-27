

from socket import *

server_port = 12000
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('127.0.0.1',12345))
celsius_temperature = input('Enter Temperature in Celsius: ')
client_socket.send(celsius_temperature.encode())

fahrenheit_temperature = client_socket.recv(1024).decode()
print(f'Fahrenheit Temperature: {fahrenheit_temperature}')
client_socket.close()