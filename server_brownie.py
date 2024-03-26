import socket
import zlib
from threading import Thread

def client_handler(server_socket, client_address, accumulated_messages):
    while True:
        data, client_address = server_socket.recvfrom(4000)
        try:
            decompressed_data = zlib.decompress(data)
            seq_number, content = decompressed_data.decode('utf-8').split(':', 1)
        except zlib.error as e:
            print(f"Decompression error: {e}")
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
                compressed_response_content = zlib.compress(response_content.encode('utf-8'))
                server_socket.sendto(compressed_response_content, client_address)
                print(f"Sent '{char}' back to {client_address}, Seq: {response_seq_number}")
            end_msg = f"{len(message)}:END"
            compressed_end_msg = zlib.compress(end_msg.encode('utf-8'))
            server_socket.sendto(compressed_end_msg, client_address)


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
