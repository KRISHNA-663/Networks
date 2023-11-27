import socket
import pickle

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_host = '127.0.0.1'  
server_port = 12345       
client_socket.connect((server_host, server_port))

while True:
    print("Welcome to EMPLOYEE MANAGEMENT SYSTEM")
    print("Pick any option from the below,") 
    print("Options:")
    print("1. Add Employee")
    print("2. Get Employee")
    print("3. Update Employee")
    print("4. Delete Employee")
    print("5. List Employees")
    print("6. Quit")
    
    choice = input("Enter your choice: ")

    if choice == '1':
        employee = {}
        employee['id'] = int(input("Enter employee ID: "))
        employee['name'] = input("Enter employee name: ")
        employee['position'] = input("Enter employee position: ")
        client_socket.send('add'.encode('utf-8'))
        client_socket.send(pickle.dumps(employee))
        response = client_socket.recv(1024)
        print(response.decode('utf-8'))

    elif choice == '2':
        employee_id = int(input("Enter employee ID to retrieve: "))
        client_socket.send('get'.encode('utf-8'))
        client_socket.send(str(employee_id).encode('utf-8'))
        response = pickle.loads(client_socket.recv(1024))
        if response:
            print(response)
        else:
            print("Employee not found!")

    elif choice == '3':
        employee = {}
        employee['id'] = int(input("Enter employee ID to update: "))
        employee['name'] = input("Enter updated employee name: ")
        employee['position'] = input("Enter updated employee position: ")
        client_socket.send('update'.encode('utf-8'))
        client_socket.send(pickle.dumps(employee))
        response = client_socket.recv(1024)
        print(response.decode('utf-8'))

    elif choice == '4':
        employee_id = int(input("Enter employee ID to delete: "))
        client_socket.send('delete'.encode('utf-8'))
        client_socket.send(str(employee_id).encode('utf-8'))
        response = client_socket.recv(1024)
        print(response.decode('utf-8'))

    elif choice == '5':
        client_socket.send('list'.encode('utf-8'))
        employees = pickle.loads(client_socket.recv(1024))
        if employees:
            for employee in employees:
                print(employee)
        else:
            print("No employees found!")

    elif choice == '6':
        client_socket.close()
        break

    else:
        print("Invalid choice. Please try again.")
