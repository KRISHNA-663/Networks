import socket
import time
print("-----------------------------SELECTIVE REPEAT PROTOCOL-----------------------------\n")
print("--------------------------------SENDER SIDE PROGRAM--------------------------------\n\n\n\n")
sender_addr = ("127.0.0.1", 8080)
receiver_addr = ("127.0.0.1", 8081)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)
num_packets = int(input("Enter the number of packets to transmit: "))
frame_size = 3
window_size = int(input("Enter the Window size: "))
packectloss = int(input("Enter the packet should be lost: "))
print("\n")
sock.sendto(str(num_packets).encode(),receiver_addr)
sock.sendto(str(packectloss).encode(),receiver_addr)
frames = [f"Frame {i}".encode('utf-8').ljust(frame_size) for i in range(num_packets)]
nextpack = 0
seq_num = 0
window_start = 0
def wind(sen):
    header = f"seq_num={sen}".encode('utf-8')
    message = header + b'\n' + frames[sen]
    try:
        print(f"Sent Packet {sen}")
        sock.sendto(message, receiver_addr)
        time.sleep(2)
    except socket.timeout:
        print(f"Timeout occurred, retransmitting frame {sen}")
def startwindow(start):
    global nextpack
    for i in range(start, min(start + window_size, num_packets)):
        header = f"seq_num={i}".encode('utf-8')
        message = header + b'\n' + frames[i]
        try:
            print(f"Sent Packet {i}")
            sock.sendto(message, receiver_addr)
            time.sleep(2)
            nextpack+=1
        except socket.timeout:
            print(f"Timeout occurred, retransmitting frame {i}")
            continue 
startwindow(0)
while window_start < num_packets:
    try:
        ack, _ = sock.recvfrom(1024)
        time.sleep(2)
        ack_seq_num = int(ack.split(b',')[0].split(b'=')[1])
        if ack_seq_num == window_start:
            print(f"Acknowledgment received for frame {ack_seq_num}\n")
            if(nextpack<num_packets):
                wind(nextpack)
                nextpack+=1
            window_start += 1 
        else:
            print(f"Acknowledgment: {ack_seq_num}")
            if(window_start+window_size-1<=ack_seq_num):
                print(f"Timeout occurred for frame {window_start}, retransmitting...\n")
                wind(window_start)
                try:
                    ackn, _ = sock.recvfrom(1024)
                    ack_seq_nums = int(ackn.split(b',')[0].split(b'=')[1])
                except socket.timeout:
                    print()
                if(ack_seq_nums == window_start):
                    print(f"Acknowledgment received for frame {ack_seq_nums}\n")
                    window_start = nextpack
                    startwindow(window_start)                    
    except socket.timeout:
        print(f"Timeout occurred for frame {window_start}, retransmitting...")
        continue 
sock.close()