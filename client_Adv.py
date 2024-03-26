import socket

def send_char_with_ack(client_socket, message, server_address, server_port, max_retries=10):
    retries = 0
    while retries < max_retries:
        print(f"Sending: {message}")
        client_socket.sendto(message.encode('utf-8'), (server_address, server_port))
        try:
            ack, _ = client_socket.recvfrom(4000)
            ack_msg = ack.decode('utf-8')
            if ack_msg.startswith("ACK:"):
                print(f"Received {ack_msg}")
                return True
        except socket.timeout:
            print("Timeout, resending...")
            retries += 1
    
    print(f"Failed to receive ACK after {max_retries} attempts. Moving on.")
    return False

def receive_and_ack(client_socket, server_address, server_port, max_retries=10):
    retries = 0
    while retries < max_retries:
        try:
            data, _ = client_socket.recvfrom(4000)
            message = data.decode('utf-8')
            seq_number, char = message.split(':', 1)
            if char != "END":
                print(f"Received: {seq_number}:{char}")
                ack_msg = f"ACK"
                client_socket.sendto(ack_msg.encode('utf-8'), (server_address, server_port))
                return seq_number, char
            else:
                return seq_number, "END"
        except socket.timeout:
            print(f"Timeout while waiting for message. Retrying {retries+1}/{max_retries}...")
            retries += 1
    print("Maximum retries reached. Ending connection.")
    return None, None


def send_end_signal_and_receive_reversed(client_socket, end_signal_message, server_address, server_port):
    print(f"Sending: {end_signal_message}")
    client_socket.sendto(end_signal_message.encode('utf-8'), (server_address, server_port))

    reversed_message = ""
    seq_numbers_received = []

    while True:
        seq_number, char = receive_and_ack(client_socket, server_address, server_port)
        if char == "END":
            ack_msg = f"ACK"
            client_socket.sendto(ack_msg.encode('utf-8'), (server_address, server_port))
            break
        if seq_number not in seq_numbers_received:
            reversed_message += char
            seq_numbers_received.append(seq_number)  
        else:
            print(f"ACK has not been received by the server, Duplicate received for sequence number: {seq_number}. Skipping...and sending the ACK again")

    print(f"Reversed Message: {reversed_message}")

def main():
    server_address = 'localhost'
    server_port = 12345
    message = input("Enter your message: ")
    end_signal = f"{len(message)}:END"

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.settimeout(2)

        for i, char in enumerate(message):
            if not send_char_with_ack(client_socket, f"{i}:{char}", server_address, server_port):
                print("Stopping due to unsuccessful ACK.")
                return

        send_end_signal_and_receive_reversed(client_socket, end_signal, server_address, server_port)

if __name__ == "__main__":
    main()


