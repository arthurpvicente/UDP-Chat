import socket
import threading
import random

# Constants
PORT = 12000
TIMEOUT = 3  # in seconds

# Globals for sequence tracking
server_expected_sequence = 0
client_sequence = 0
def run():
    """
    Prompting for server IP, creating and starting server and client threads.
    
    This function initializes the server and client threads for chat operation.
    """
    server_ip = input("Enter the server IP (or localhost if running on the same machine): ")
    if server_ip == "localhost":
        server_ip = "127.0.0.1"

    # Starting server and client threads
    server_thread = threading.Thread(target=server)
    client_thread = threading.Thread(target=client, args=(server_ip,))

    server_thread.start()
    client_thread.start()

    server_thread.join()
    client_thread.join()

def server():
    """
    Handling the server-side operations of the chat.
    
    This function is responsible for setting up a UDP server, receiving messages,
    acknowledging received messages, and periodically ignoring received packets.
    """
    global server_expected_sequence

    # Standard server setup
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as serverSocket:
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # It allows socket to reuse a local address and it is useful when I want restart closed socket 
        serverSocket.bind(('', PORT))
        while True:
            message, addr = serverSocket.recvfrom(1024)
            sequence, received_msg = message.decode().split(' ', 1)

            if random.random() > 0.2:  # 80% chance to process the message, 20% to ignore
                if int(sequence) == server_expected_sequence:
                    print(f"message from: {addr[0]} sequence: {sequence} message: {received_msg}")
                    serverSocket.sendto(sequence.encode(), addr)
                    server_expected_sequence = 1 - server_expected_sequence  # Toggle between 0 and 1
                else:
                    serverSocket.sendto(str(1 - server_expected_sequence).encode(), addr)  # Send previous sequence ACK
            else:
                print("Server ignored the message!")

def client(server_ip):
    """
    Handling the client-side operations of the chat.
    
    This function sets up the client side of the UDP chat application, sends messages,
    waits for acknowledgments, and periodically ignores acknowledgments.
    """
    global client_sequence

    # Standard client setup
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as clientSocket:
        clientSocket.settimeout(TIMEOUT)
        while True:
            message = input("Input chat message: ")
            full_msg = f"{client_sequence} {message}"
            
            ack_received = False

            while not ack_received:
                clientSocket.sendto(full_msg.encode(), (server_ip, PORT))
                try:
                    ack, _ = clientSocket.recvfrom(1024)
                    if random.random() > 0.2:  # 80% chance to process the ACK, 20% to ignore
                        if int(ack.decode()) == client_sequence:
                            ack_received = True
                            client_sequence = 1 - client_sequence  # Toggle between 0 and 1
                        else:
                            # Resend the message if the ACK sequence doesn't match
                            continue
                    else:
                        print("Client ignored the ACK!")
                except socket.timeout:
                    # Timeout indicates that the packet may be lost, so we resend
                    continue

if __name__ == "__main__":
    """
    Main execution point of the script.
    
    When this script is run directly, it initializes the UDP chat application.
    """
    run()
