"""Create a class that can receive until a given delimiter.

Author: Jason Gardiner
Class: CSI-275-01
Assignment: Lab 7 -- File Framing

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

import argparse
import socket
import os
import constants


class UploadError(Exception):
    """Error when uploading."""

    pass


class UploadClient:
    """Use a socket to upload a file to a server."""

    def __init__(self, hostname, port):
        """Create a tcp socket to connect to the server."""
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.tcp_sock.connect((hostname, port))

        # Allow the buffer to hold data in between function calls
        self.recv_buffer = b''

    def close(self):
        """Close the tcp socket."""
        self.tcp_sock.close()

    def recv_all(self, length):
        """Receive all the data of a given message length."""
        data = b''
        while len(data) < length:
            more = self.tcp_sock.recv(length - len(data))
            if not more:
                raise EOFError('was expecting %d bytes but only received'
                               ' %d bytes before the socket closed'
                               % (length, len(data)))
            data += more
        return data

    def recv_until_delimiter(self, delimiter):
        """Receive all the data until the delimiter."""
        data = b''
        # newest_msg = b''
        is_msg_done = False
        while not is_msg_done:
            # If we have a buffer, deal with that, otherwise get a new message
            if self.recv_buffer:
                newest_msg = self.recv_buffer
                self.recv_buffer = b''
            else:
                newest_msg = self.tcp_sock.recv(constants.MAX_BYTES)

            # If the socket is closed, raise an error
            if not newest_msg:
                raise EOFError('Socket closed')

            # If the newest message has a delimiter,
            # we need to slice off the buffer
            if newest_msg.__contains__(delimiter):
                newest_msg, temp_buffer = newest_msg.split(delimiter, 1)
                self.recv_buffer = temp_buffer
                is_msg_done = True

            # Append the most recent message to the data
            data += newest_msg
        # Send out the data
        return data

    def upload_file(self, file_path):
        """Upload a file to the class's server.

        The function handles Q4 of the original assignment.
        """
        # Open the file
        file = open(file_path, "rb")

        # Read the whole thing into memory
        file_data = file.read()

        # Prep the first line to send
        header = "UPLOAD " + os.path.basename(file_path) + " " \
                 + str(len(file_data)) + "\n"
        print(f"Sending {header}")

        self.tcp_sock.sendall(header.encode("ascii"))

        # Send the file data
        self.tcp_sock.sendall(file_data)

        # Wait for a response
        return_msg = self.recv_until_delimiter(b"\n").decode("ascii")
        if return_msg == "ERROR":
            raise UploadError
        else:
            print("Upload successful")

    def list_files(self):
        """Run a command to get a list of files from the server."""
        self.tcp_sock.send("LIST\n".encode('UTF-8'))
        try:
            server_msg = self.recv_until_delimiter(b'\n\n')
        except EOFError:
            server_msg = "ERROR"
        file_names_sizes = server_msg.decode("utf-8").split('\n')

        data_export = []

        for item in file_names_sizes:
            # Split each string by space
            file_name, size = item.split()
            # Convert size to integer
            size = int(size)
            # Append a tuple of (file_name, size) to data_export
            data_export.append((file_name, size))

        return data_export


def main():
    """Run some basic tests on the required functionality.

    for more extensive tests run the autograder!
    """
    parser = argparse.ArgumentParser(description="TCP File Uploader")
    parser.add_argument("host", help="interface the server listens at;"
                                     " host the client sends to")
    parser.add_argument("-p", metavar="PORT", type=int,
                        default=constants.UPLOAD_PORT,
                        help=f"TCP port (default {constants.UPLOAD_PORT})")
    args = parser.parse_args()
    upload_client = UploadClient(args.host, args.p)
    upload_client.upload_file("upload_client.py")
    print(upload_client.list_files())
    upload_client.close()


if __name__ == "__main__":
    main()
