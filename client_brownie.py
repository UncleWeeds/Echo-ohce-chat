import socket
import zlib

def send_char_with_ack(client_socket, message, server_address, server_port):
    while True:
        compressed_message = zlib.compress(message.encode('utf-8'))
        print(f"Sending: {message}")
        client_socket.sendto(compressed_message, (server_address, server_port))
        try:
            ack, _ = client_socket.recvfrom(4000)
            ack_msg = ack.decode('utf-8')
            if ack_msg.startswith("ACK:"):
                print(f"Received {ack_msg}")
                break
        except socket.timeout:
            print("Timeout, resending...")

def send_end_signal_and_receive_reversed(client_socket, end_signal_message, server_address, server_port):
    print(f"Sending: {end_signal_message}")
    compressed_end_signal = zlib.compress(end_signal_message.encode('utf-8'))
    client_socket.sendto(compressed_end_signal, (server_address, server_port))

    reversed_message = ""
    while True:
        try:
            data, _ = client_socket.recvfrom(4000)
            decompressed_data = zlib.decompress(data)
            _, char = decompressed_data.decode('utf-8').split(':', 1)
            if char == "END":
                break
            reversed_message += char
        except socket.timeout:
            print("Timeout while receiving reversed message. Ending connection.")
            break
        except zlib.error as e:
            print(f"Decompression error: {e}")
            break

    print(f"Reversed Message: {reversed_message}")


def main():
    server_address = 'localhost'
    server_port = 12345
    message = input("Enter your message: ")
    clump_size = 10

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.settimeout(2) 

        for i in range(0, len(message), clump_size):
            clump = message[i:i+clump_size]
            send_char_with_ack(client_socket, f"{i}:{clump}", server_address, server_port)

        end_signal = f"{len(message)}:END"
        send_end_signal_and_receive_reversed(client_socket, end_signal, server_address, server_port)

if __name__ == "__main__":
    main()
