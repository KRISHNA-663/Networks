import socket
import time

print("-----------------------------SELECTIVE REPEAT PROTOCOL-----------------------------\n")
print("-------------------------------RECEIVER SIDE PROGRAM-------------------------------\n\n\n\n")

receiver_addr = ("127.0.0.1", 8081)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(receiver_addr)

expected_seq_num = 0
received_packets = []
out_of_order_packets = {}

# Set a timeout only for the initial setup
sock.settimeout(20)

print("Receiver is waiting for packets...\n\n\n\n")

# Use a loop to handle potential TimeoutError during setup
while True:
    try:
        denum, add = sock.recvfrom(1024)
        num_pack = int(denum.decode())
        deloss, ad = sock.recvfrom(1024)
        losspack = int(deloss.decode())
        break  # Break the loop if the control information is received without a TimeoutError
    except socket.timeout:
        print("Timeout occurred during setup. Retrying...\n")

# Disable the timeout for the rest of the reception process
sock.settimeout(None)

seq_num = 0

while len(received_packets) < num_pack:
    try:
        data, sender_addr = sock.recvfrom(1024)
        time.sleep(2)

        try:
            seq_num = int(data.split(b'\n')[0].split(b'=')[1])
        except (IndexError, ValueError):
            print("Corrupted or incomplete packet received, discarding and requesting retransmission\n")
            continue

        if seq_num != losspack:
            print(f"Packet Received {seq_num}")

            if seq_num == expected_seq_num:
                received_packets.append(data.split(b'\n')[1])
                ack = f"ack_seq_num={seq_num}".encode('utf-8')
                sock.sendto(ack, sender_addr)
                print(f"Acknowledgment sent for packet {seq_num}\n")
                time.sleep(2)
                expected_seq_num += 1

                while expected_seq_num in out_of_order_packets:
                    received_packets.append(out_of_order_packets.pop(expected_seq_num).split(b'\n')[1])
                    expected_seq_num += 1
            else:
                out_of_order_packets[seq_num] = data
                ack = f"ack_seq_num={seq_num}".encode('utf-8')
                print(f"Send acknowledgment for packet {seq_num}, expecting {expected_seq_num}\n")
                sock.sendto(ack, sender_addr)
                time.sleep(2)
        else:
            losspack = -1

    except socket.error as e:
        break


