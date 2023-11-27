import socket
import pickle


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_host = '127.0.0.1'  
server_port = 12345       
server_socket.bind((server_host, server_port))
server_socket.listen(5)


employee_data = {}

def add_employee(employee):
    employee_data[employee['id']] = employee

def get_employee(employee_id):
    return employee_data.get(employee_id)

def update_employee(employee):
    if employee['id'] in employee_data:
        employee_data[employee['id']] = employee
        return True
    return False

def delete_employee(employee_id):
    if employee_id in employee_data:
        del employee_data[employee_id]
        return True
    return False

def list_employees():
    return list(employee_data.values())

while True:
    print("Waiting for a connection...")
    client_socket, client_addr = server_socket.accept()
    print(f"Connection established with {client_addr}")

    request = client_socket.recv(1024).decode('utf-8')

    if request == 'add':
        employee = pickle.loads(client_socket.recv(1024))
        add_employee(employee)
        client_socket.send(b"Employee added successfully!")

    elif request == 'get':
        employee_id = int(client_socket.recv(1024).decode('utf-8'))
        employee = get_employee(employee_id)
        if employee:
            client_socket.send(pickle.dumps(employee))
        else:
            client_socket.send(b"Employee not found!")

    elif request == 'update':
        employee = pickle.loads(client_socket.recv(1024))
        success = update_employee(employee)
        if success:
            client_socket.send(b"Employee updated successfully!")
        else:
            client_socket.send(b"Employee not found!")

    elif request == 'delete':
        employee_id = int(client_socket.recv(1024).decode('utf-8'))
        success = delete_employee(employee_id)
        if success:
            client_socket.send(b"Employee deleted successfully!")
        else:
            client_socket.send(b"Employee not found!")

    elif request == 'list':
        employees = list_employees()
        client_socket.send(pickle.dumps(employees))

    else:
        client_socket.send(b"Invalid request!")

    client_socket.close()
