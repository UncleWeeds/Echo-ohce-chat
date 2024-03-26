import socket
from threading import Thread

def send_with_ack(server_socket, message, client_address, max_retries=10):
    retries = 0
    while retries < max_retries:
        server_socket.sendto(message.encode('utf-8'), client_address)
        try:
            ack, _ = server_socket.recvfrom(4000)
            ack_msg = ack.decode('utf-8')

            if ack_msg == "ACK":
                print(f"ACK received for: {message}")
                return True
        except socket.timeout:
            print("Timeout, resending...")
            retries += 1
    print(f"Failed to receive ACK for {message} after {max_retries} attempts.")
    return False

def client_handler(server_socket, client_address, accumulated_messages):
    while True:
        try:
            data, _ = server_socket.recvfrom(4000)
            decoded_data = data.decode('utf-8')
            seq_number, content = decoded_data.split(':', 1)
        except ValueError as e:
            continue
        except TimeoutError:
            continue
        except Exception as e:
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
            #print(f"{accumulated_messages[client_address]}")
            print(f"Received 'END' signal from {client_address}, preparing to send reversed message.")
            for i, char in enumerate(message[::-1]):
                response_seq_number = f"{i}:{char}"
                if not send_with_ack(server_socket, response_seq_number, client_address):
                    break  
            end_msg = "5:END"
            send_with_ack(server_socket, end_msg, client_address)
            #server_socket.sendto(end_msg.encode('utf-8'), client_address)
        

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 12345))
    server_socket.settimeout(5)  
    print("UDP Server listening on localhost:12345")

    accumulated_messages = {}

    while True:
        try:
            _, client_address = server_socket.recvfrom(4000)
            Thread(target=client_handler, args=(server_socket, client_address, accumulated_messages), daemon=True).start()
        except socket.timeout:
            #print("wow ok")
            continue
        except Exception as e:
            print(f"Unexpected error: {e}")
            break 

if __name__ == "__main__":
    main()


