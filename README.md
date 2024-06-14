# UDP Chat Application

## Overview
This Python script implements a simple UDP chat application using socket programming. The application consists of a server and a client, both of which run concurrently as separate threads.

## Dependencies
- Python 3.x
- socket module
- threading module
- random module

## Usage
1. Run the script.
2. Enter the server IP address when prompted.
3. Start sending messages from both the client and server sides.

## Code Structure
1. **Constants**:
   - `PORT`: The port number used for communication (default: 12000).
   - `TIMEOUT`: Timeout duration for socket operations (default: 3 seconds).

2. **Global Variables**:
   - `server_expected_sequence`: Tracks the expected sequence number on the server side.
   - `client_sequence`: Tracks the sequence number on the client side.

3. **Functions**:
   - `run()`: Initializes and starts the server and client threads.
   - `server()`: Handles server-side operations including receiving messages, acknowledging, and periodically ignoring packets.
   - `client(server_ip)`: Handles client-side operations including sending messages, waiting for acknowledgments, and periodically ignoring acknowledgments.

4. **Main Execution**:
   - The `__name__` variable is checked to ensure that the script is being run directly.
   - If so, it calls the `run()` function to start the UDP chat application.

## Server Operation
- The server waits for messages from clients.
- It processes received messages with an 80% chance, acknowledging them and toggling the expected sequence number.
- Periodically, with a 20% chance, it ignores received messages.

## Client Operation
- The client sends messages to the server.
- It waits for acknowledgments and retries sending if no acknowledgment is received within the timeout period.
- Periodically, with a 20% chance, it ignores received acknowledgments.

## Notes
- The script uses UDP (User Datagram Protocol) for communication, which is connectionless and unreliable. Hence, acknowledgments and retransmissions are implemented to handle packet loss.
- The random module is used to simulate packet loss by introducing randomness in acknowledgment processing.
- The script assumes local testing with a predefined server IP address.
#
