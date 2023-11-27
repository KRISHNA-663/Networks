import socket
import pickle


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


server_address = ('127.0.0.1', 12345)
server_socket.bind(server_address)


employees = {
    1: {"id": 1, "name": "John Doe", "position": "Manager"},
    2: {"id": 2, "name": "Jane Smith", "position": "Developer"},
    
}

print("Server is ready to receive data...")

while True:
    try:
        
        data, client_address = server_socket.recvfrom(1024)

        
        request = pickle.loads(data)

        if request["action"] == "get_employee":
            employee_id = request["employee_id"]
            if employee_id in employees:
                response = employees[employee_id]
            else:
                response = {"error": "Employee not found"}

        elif request["action"] == "get_all_employees":
            response = employees

        else:
            response = {"error": "Invalid action"}

       
        server_socket.sendto(pickle.dumps(response), client_address)

    except KeyboardInterrupt:
        print("\nServer interrupted.")
        break


server_socket.close()