"""Make a threaded chatroom server and client

Author: Jason Gardiner
Class: CSI-275-01
Assignment: Final Project

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for
- the purpose of future plagiarism checking)"""

import socket
import threading
import json
import time

# Server host/port information
HOST = "localhost"
PORT = 10000


class ChatroomClient:
    """A simple TCP client for the chat program."""

    def __init__(self, host, port):
        """Initialize the client with the specified host and port."""
        self.screen_name = ""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

    def start(self):
        """Start the client."""
        # Get a valid screen name
        is_screen_name_valid = False
        while not is_screen_name_valid:
            self.screen_name = input("Enter your screen name (no spaces): ")
            if self.screen_name:
                if " " not in self.screen_name:
                    is_screen_name_valid = True

        self.client_socket.sendall(self.screen_name.encode('utf-8'))

        # Start a thread to receive messages from the server
        threading.Thread(target=self.receive_messages, daemon=True).start()

        is_connected = True

        while is_connected:
            # Get a message and send it
            message = input("Type your message: ")
            self.client_socket.sendall(self.encode_message(message))

            # Determine if the client is disconnecting
            if message.endswith("EXIT"):
                time.sleep(1)
                self.client_socket.close()
                is_connected = False
                print("Successfully disconnected from server.")
            else:
                # Wait for 1 second before prompting for another message
                time.sleep(1)

    def receive_messages(self):
        """Receive messages from the server."""
        try:
            while True:
                # Receive message length
                raw_len = self.client_socket.recv(4)
                if not raw_len:
                    break
                int_len = int.from_bytes(raw_len, byteorder='big')
                # Receive the actual message
                data = b''
                while len(data) < int_len:
                    packet = self.client_socket.recv(int_len - len(data))
                    if not packet:
                        raise ValueError("Incomplete message received")
                    data += packet
                message = json.loads(data.decode('utf-8'))
                print(message)
        except Exception as e:
            print(f"Error receiving message: {e}")

    def encode_message(self, message):
        """Encode message to be sent over socket."""
        encoded_message = json.dumps(message).encode('utf-8')
        raw_len = len(encoded_message).to_bytes(4, byteorder='big')
        return raw_len + encoded_message


if __name__ == "__main__":
    client = ChatroomClient(HOST, PORT)
    client.start()
