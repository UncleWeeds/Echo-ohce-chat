import socket

def send_char_with_ack(client_socket, message, server_address, server_port, max_retries=5):
    retries = 0
    while retries < max_retries:
        print(f"Sending: {message}")
        client_socket.sendto(message.encode('utf-8'), (server_address, server_port))
        try:
            ack, _ = client_socket.recvfrom(4000)
            ack_msg = ack.decode('utf-8')
            if ack_msg.startswith("ACK:"):
                print(f"Received {ack_msg}")
                return  
        except socket.timeout:
            print("Timeout, resending...")
            retries += 1
    
    print(f"Failed to receive ACK after {max_retries} attempts. Moving on.")

def send_end_signal_and_receive_reversed(client_socket, end_signal_message, server_address, server_port):
    print(f"Sending: {end_signal_message}")
    client_socket.sendto(end_signal_message.encode('utf-8'), (server_address, server_port))

    reversed_message = ""
    while True:
        try:
            data, _ = client_socket.recvfrom(4000)
            _, char = data.decode('utf-8').split(':', 1)
            if char == "END":
                break  
            reversed_message += char
        except socket.timeout:
            print("Timeout while receiving reversed message. Ending connection.")
            break
        except ValueError:
            print("Error processing received data. Possibly incorrect format.")
            break

    print(f"Reversed Message: {reversed_message}")

def main():
    server_address = 'localhost'
    server_port = 12345
    message = input("Enter your message: ")
    end_signal = f"{len(message)}:END"

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.settimeout(2)

        for i, char in enumerate(message):
            send_char_with_ack(client_socket, f"{i}:{char}", server_address, server_port, max_retries=5)

        send_end_signal_and_receive_reversed(client_socket, end_signal, server_address, server_port)

if __name__ == "__main__":
    main()



