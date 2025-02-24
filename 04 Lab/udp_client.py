"""Connect a UDP socket to a server to transmit data.

Author: Jason Gardiner
Class: CSI-275-01
Assignment: Lab 4 -- UDP Sockets

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for
- the purpose of future plagiarism checking)


Student code for Lab/HW 2.

Champlain College CSI-235, Spring 2019
The following code was written by Joshua Auerbach (jauerbach@champlain.edu)
"""

import socket
import constants
import random


class TimeOutError(Exception):
    """Exception raised for timing out."""

    pass


class UDPClient:
    """Create a connection to a server and send them some data."""

    def __init__(self, host, port, bool_id=False):
        """Initialize class variables."""
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (host, port)
        self.udp_socket.connect(self.server_address)
        self.bool_id = bool_id

    def send_message_by_character(self, my_message):
        """Send a message to the server you connected to."""
        if not self.bool_id:
            final_received_msg = ""
            for char in my_message:
                current_wait_time = constants.INITIAL_TIMEOUT

                while True:
                    try:
                        self.udp_socket.settimeout(current_wait_time)
                        self.udp_socket.sendto(char.encode('ascii'),
                                               self.server_address)
                        received_msg_raw, from_address = (
                            self.udp_socket.recvfrom(self.server_address[1]))
                        if received_msg_raw:
                            break
                    except socket.timeout:
                        current_wait_time *= 2
                        if current_wait_time > constants.MAX_TIMEOUT:
                            raise TimeOutError

                received_msg_str = received_msg_raw.decode()
                final_received_msg += received_msg_str

            return final_received_msg
        else:
            final_received_msg = ""
            for char in my_message:
                current_wait_time = constants.INITIAL_TIMEOUT
                char_id = random.randrange(0, constants.MAX_ID)

                while True:
                    try:
                        self.udp_socket.settimeout(current_wait_time)
                        self.udp_socket.sendto((str(char_id)
                                                + "|"
                                                + char).encode('ascii'),
                                               self.server_address)
                        received_msg_raw, from_address = (
                            self.udp_socket.recvfrom(self.server_address[1]))

                        received_id, received_msg_split = (
                            received_msg_raw.decode("ascii").split('|'))

                        if str(received_id) == str(char_id):
                            final_received_msg += received_msg_split
                            break
                    except socket.timeout:
                        current_wait_time *= 2
                        if current_wait_time > constants.MAX_TIMEOUT:
                            raise TimeOutError

            return final_received_msg


def main():
    """Run some basic tests on the required functionality.

    for more extensive tests run the autograder!
    """
    client = UDPClient(constants.HOST, constants.ECHO_PORT)
    print(client.send_message_by_character("hello world"))

    client = UDPClient(constants.HOST, constants.REQUEST_ID_PORT, True)
    print(client.send_message_by_character("hello world"))


if __name__ == "__main__":
    main()
