"""Create a server to take an input and sort it in the designated way.

Author: Jason Gardiner
Class: CSI-275-01
Assignment: Lab 5 -- Sorting Server

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

HOST = "localhost"
PORT = 20000


class SortServer:
    """Create and run a server to sort a given string in a given way."""

    def __init__(self, host, port):
        """Create a TCP Socket for the server and bind it."""

        # Create the socket for the server to connect to,
        # and assemble the given address
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_address = (host, port)

        self.server_socket.bind(self.listen_address)

    def run_server(self):
        """Run the server so it can sort some lists."""

        self.server_socket.listen()

        while True:

            print("Waiting for connection...")
            connected_socket, address = self.server_socket.accept()

            while True:
                # Wait for and decode the message
                print("Waiting for message...")
                msg_raw = connected_socket.recv(4096)
                if not msg_raw:
                    break
                else:
                    # Decode the message
                    msg_str = msg_raw.decode('ascii')

                    # Parse the message for accuracy,
                    # if it fails a test, make it return error
                    return_msg_str = ""
                    sort_type = "a"

                    # Grab the sorting type if it exists
                    if msg_str.__contains__("|"):
                        sort_type = msg_str[-1]
                        msg_str = msg_str[:len(msg_str)-2]
                        sort_options = ["a", "d", "s"]
                        if sort_type not in sort_options:
                            return_msg_str = "ERROR"

                    if not msg_str.startswith("LIST"):
                        return_msg_str = "ERROR"
                    separated_msg = msg_str.split(" ")
                    if separated_msg.__len__() < 2:
                        return_msg_str = "ERROR"
                    separated_msg.pop(0)  # Remove the LIST from separated_msg
                    for item in separated_msg:
                        if not item.strip("-").replace(".", "", 1).isdigit():
                            return_msg_str = "ERROR"
                    if not return_msg_str == "ERROR":
                        # If no issues arose, sort the string
                        return_msg_str = "SORTED"
                        return_list = []
                        # If it isn't sorted as string, convert to numbers
                        if not sort_type == "s":
                            for item in separated_msg:
                                if item.__contains__('.'):
                                    return_list.append(float(item))
                                else:
                                    return_list.append(int(item))
                        else:
                            return_list = separated_msg

                        # Check sort type for if it is descending order
                        if sort_type == "d":
                            return_list.sort(reverse=True)
                        else:
                            return_list.sort()

                        for item in return_list:
                            return_msg_str += f" {str(item)}"

                    connected_socket.sendto(return_msg_str.encode('ascii'), address)


if __name__ == "__main__":
    server = SortServer(HOST, PORT)
    server.run_server()
