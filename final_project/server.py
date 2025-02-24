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

# Server host/port information
HOST = "localhost"
PORT = 10000


class ChatroomServer:
    """A threaded TCP server for a chat program."""

    def __init__(self, host, port):
        """Initialize the server with the specified host and port."""
        self.host = host
        self.port = port
        self.clients = {}  # Dictionary to store client information
        self.thread_count = 0  # Keep track of active threads

    def handle_client(self, connection, address):
        """Thread function to handle communication with a single client."""
        print(f"New connection from {address}")

        # Receive the screen name of the client
        data = connection.recv(1024)
        screen_name = data.decode('utf-8')

        # Add client information to the global dictionary
        self.clients[screen_name] = connection

        try:
            while True:
                # Receive message length
                raw_len = connection.recv(4)
                if not raw_len:
                    break
                int_len = int.from_bytes(raw_len, byteorder='big')
                # Receive the actual message
                data = b''
                while len(data) < int_len:
                    packet = connection.recv(int_len - len(data))
                    if not packet:
                        raise ValueError("Incomplete message received")
                    data += packet
                message = json.loads(data.decode('utf-8'))

                # Determine message type and handle accordingly
                if " " in message:
                    msg_text, junk = message.split(' ', 1)
                else:
                    msg_text = message

                # Determine whether or not to EXIT
                should_exit = False
                if message.endswith("EXIT"):
                    message = message[:-4]  # Remove "EXIT" from the end
                    should_exit = True

                if message:
                    if (msg_text.startswith('@')
                            and msg_text[1:] in self.clients):
                        recipient = msg_text[1:]
                        self.private_message(screen_name, msg_text[1:],
                                             message, recipient)
                    else:
                        self.broadcast_message(screen_name, message)
                if should_exit:
                    del self.clients[screen_name]
                    connection.close()
                    self.broadcast_message("Server",
                                           f"{screen_name} has disconnected")
                    break
        except Exception as e:
            print(f"Error: {e}")
            del self.clients[screen_name]
            connection.close()
        finally:
            self.thread_count -= 1

    def broadcast_message(self, sender, message):
        """Broadcast a message to all connected clients."""
        for client in self.clients.values():
            client.sendall(self.encode_message(["BROADCAST", sender, message]))

    def private_message(self, sender, recipient, message, recipient_name):
        """Send a private message to a specific client."""
        if recipient_name in self.clients:
            self.clients[recipient_name].sendall(
                self.encode_message(["PRIVATE", sender, message]))
            self.clients[sender].sendall(
                self.encode_message(["PRIVATE", recipient, message]))
        else:
            self.clients[sender].sendall(
                self.encode_message(["ERROR", "Target for private message is"
                                              "not connected to server"]))

    def encode_message(self, message):
        """Encode message to be sent over socket."""
        try:
            encoded_message = json.dumps(message).encode('utf-8')
            raw_len = len(encoded_message).to_bytes(4, byteorder='big')
            return raw_len + encoded_message
        except Exception as e:
            print(f"Error: {e}")

    def start(self):
        """Start the server."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            if self.thread_count < 10:
                connection, address = server_socket.accept()
                # Start a new thread for each client
                threading.Thread(target=self.handle_client,
                                 args=(connection, address)).start()
                self.thread_count += 1
            else:
                # Maximum thread count reached, wait and try again
                continue


if __name__ == "__main__":
    chat_server = ChatroomServer(HOST, PORT)
    chat_server.start()
