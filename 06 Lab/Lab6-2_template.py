""" Your mission is to build a TCP server that parses a simple text protocol
that uses framing technique #5 from class to tell us how much data is coming.
Messages being sent and received by the server should be in the following
format.

Author: Jason Gardiner
Class: CSI-275-01
Assignment: Lab 6 -- Framing with Length Fields

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for
- the purpose of future plagiarism checking)
"""

import socket

HOST = "localhost"
PORT = 45000


def recvall(sock, length):
    """Call recv until all data has been received."""
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('expected %d bytes but only received'
                           ' %d bytes before the socket closed'
                           % (length, len(data)))
        data += more
    return data


class LengthServer:
    """Create and run a server that returns the length of received strings."""

    def __init__(self, host, port):
        """Create a TCP Socket for the server and bind it."""

        # Create the socket for the server to connect to,
        # and assemble the given address
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_address = (host, port)

        self.server_socket.bind(self.listen_address)

    def calc_length(self):
        """Receive a message and send back the number of bytes."""

        self.server_socket.listen()

        while True:

            print("Waiting for connection...")
            connected_socket, address = self.server_socket.accept()

            while True:
                # Wait for and decode the message
                print("Waiting for message...")
                length_bytes = connected_socket.recv(4)
                if not length_bytes:
                    break
                else:
                    msg_str = ""
                    rtn_msg_str = ""

                    # Determine message length and receive it
                    length_int = int.from_bytes(length_bytes, "big")
                    try:
                        msg_str = recvall(connected_socket,
                                          length_int).decode("ascii")
                    except EOFError:
                        rtn_msg_str = "Length Error"

                    # Verification
                    if len(msg_str) >= length_int:
                        rtn_msg_str = f"I received {len(msg_str)} bytes."
                    else:
                        rtn_msg_str = "Length Error"

                    print(rtn_msg_str)

                    # Add the length
                    rtn_msg_len = len(rtn_msg_str).to_bytes(4, 'big')
                    rtn_msg_raw = rtn_msg_str.encode("ascii")
                    rtn_msg_raw = rtn_msg_len + rtn_msg_raw

                    connected_socket.sendall(rtn_msg_raw)

                    connected_socket.close()
                    break


if __name__ == "__main__":
    server = LengthServer(HOST, PORT)
    server.calc_length()
