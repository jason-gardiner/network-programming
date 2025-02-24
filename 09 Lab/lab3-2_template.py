"""Send data to a special server via json to be sorted.

Author: Jason Gardiner
Class: CSI-275-01
Assignment: Lab 9 -- JSON Client/Server

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

import json
import socket
import zlib


def build_list():
    """Collect input from the user and return it as a list.

    Only numeric input will be included; strings are rejected.
    """
    #  Create a list to store our numbers
    unsorted_list = []

    # Create a variable for input
    user_input = ""

    # Ask for sorting preference
    user_input = input("Please specify sorting preference (a, d, s).")
    unsorted_list.append(user_input)

    while user_input != "done":
        # Prompt the user for input
        user_input = input("Please enter a number, or 'done' to stop.")

        # Validate our input, and add it to out list
        # if it's a number
        try:
            # Were we given an integer?
            unsorted_list.append(int(user_input))
        except ValueError:
            try:
                # Were we given a floating-point number?
                unsorted_list.append(float(user_input))
            except ValueError:
                # Non-numeric input - if it's not "done",
                # reject it and move on
                if user_input != "done":
                    print("ERROR: Non-numeric input provided.")
                continue

    # Once we get here, we're done - return the list
    return unsorted_list


def sort_list(unsorted_list):
    """Send the list to the server via json to be sorted."""
    # Transform list into json and encode it
    json_unsorted_list = json.dumps(unsorted_list).encode("utf-8")

    # Compress the json data
    json_compressed = zlib.compress(json_unsorted_list)

    # Print the sizes before and after compression
    print(f'Size before compression: {len(json_unsorted_list)}\n'
          f'Size after compression: {len(json_compressed)}')

    # Create socket and send encoded message
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(('localhost', 7778))

    my_socket.sendall(json_compressed)

    # Receive, decompress, and decode list
    json_recv_msg = zlib.decompress(my_socket.recv(4096)).decode("utf-8")

    # Transform from json
    list_recv_msg = json.loads(json_recv_msg)

    # Close socket
    my_socket.close()

    print(list_recv_msg)


def main():
    """Call the build_list and sort_list functions, and print the result."""
    number_list = build_list()
    sort_list(number_list)


if __name__ == "__main__":
    main()
