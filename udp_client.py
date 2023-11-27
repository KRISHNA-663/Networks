import socket
import pickle


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


server_address = ('127.0.0.1', 12345)

try:
    while True:
        print("\nEmployee Management System")
        print("1. Get Employee by ID")
        print("2. Get All Employees")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            employee_id = int(input("Enter employee ID: "))
            request = {"action": "get_employee", "employee_id": employee_id}

        elif choice == "2":
            request = {"action": "get_all_employees"}

        elif choice == "3":
            print("Exiting the system.")
            break

        else:
            print("Invalid choice. Please try again.")
            continue

       
        client_socket.sendto(pickle.dumps(request), server_address)

        
        data, _ = client_socket.recvfrom(1024)
        response = pickle.loads(data)
        print(response)

except KeyboardInterrupt:
    print("\nClient interrupted.")

finally:
    
    client_socket.close()