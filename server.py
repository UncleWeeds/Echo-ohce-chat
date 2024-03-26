import socket
from threading import Thread

def client_handler(server_socket, client_address, accumulated_messages):
    while True:
        try:
            data, _ = server_socket.recvfrom(4000)
            decoded_data = data.decode('utf-8')
            seq_number, content = decoded_data.split(':', 1) 
        except ValueError as e:
            print(f"Error parsing message from {client_address}: {e}")
            continue  
        except Exception as e:
            print(f"Unexpected error receiving data from {client_address}: {e}")
            continue

        if client_address not in accumulated_messages:
            accumulated_messages[client_address] = ""

        if content != "END":
            print(f"Received '{content}' from {client_address}, Seq: {seq_number}")
            accumulated_messages[client_address] += content
            ack_msg = f"ACK:{seq_number}"
            server_socket.sendto(ack_msg.encode('utf-8'), client_address)
        else:
            message = accumulated_messages.pop(client_address, "")
            print(f"Received 'END' signal from {client_address}, preparing to send reversed message.")
            for i, char in enumerate(message[::-1]):
                response_seq_number = f"{i}"
                response_content = f"{response_seq_number}:{char}"
                server_socket.sendto(response_content.encode('utf-8'), client_address)
                print(f"Sent '{char}' back to {client_address}, Seq: {response_seq_number}")
            end_msg = f"{len(message)}:END"
            server_socket.sendto(end_msg.encode('utf-8'), client_address)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 12345))
    print("UDP Server listening on localhost:12345")

    accumulated_messages = {}
    while True:
        _, client_address = server_socket.recvfrom(4000)
        Thread(target=client_handler, args=(server_socket, client_address, accumulated_messages), daemon=True).start()

if __name__ == "__main__":
    main()


