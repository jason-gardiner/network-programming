"""Student code for Lab/HW1.

    Run python autograder.py

Champlain College CSI-235, Spring 2019
The following code was written by Joshua Auerbach (jauerbach@champlain.edu)
Host class __init__ function by Jason Reeves 1/4/2021 (reeves@champlain.edu)

Implement functions for detecting valid ip addresses,
detecting valid hostnames, checking if a hostname exists,
and matching hostnames to ip addresses

Author: Jason Gardiner
Class: CSI-275-01
Assignment: Lab 2 -- Host Names and IP Addresses

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


class InvalidEntryError(Exception):
    """Exception raised for invalid entries in the hosts file."""

    pass


def is_valid_ip_address(ip_address):
    """Return whether the given ip_address is a valid IPv4 address or not.

    Args:
        ip_address (str): ip_address to test

    Returns:
        bool: True if ip_address is valid IPv4 address, False otherwise.

    """
    #   *** YOUR CODE HERE ***

    octets = str(ip_address).split(".")
    # Count number of tests passed
    number_of_passed_tests = 0

    # Make sure there are 4 octets
    if len(octets) == 4:
        number_of_passed_tests += 1

    # Check if each octet is between 0 and 255
    for octet in octets:
        # Confirm int conversion is possible
        if octet.isdigit():
            if 0 <= int(octet) <= 255:
                number_of_passed_tests += 1

    if number_of_passed_tests == 5:
        return True

    return False


def is_valid_hostname(hostname):
    """Return whether the given hostname is valid or not.

    Host names may contain only alphanumeric characters, minus signs ("-"),
    and periods (".").  They must begin with an alphabetic character and end
    with an alphanumeric character.

    Args:
        hostname (str): hostname to test

    Returns:
        bool: True if hostname is valid, False otherwise.

    """
    #   *** YOUR CODE HERE ***

    # If the string is empty, it is not valid
    if not hostname:
        return False

    # If the name doesn't start with an alphabetic character
    if not hostname[0].isalpha():
        return False

    # If the name doesn't end with an alphanumeric character
    if not hostname[len(hostname) - 1].isalnum():
        return False

    # Entire string only includes '-' '.' and alphanumeric characters
    for i in hostname:
        if not (i == '-' or i == '.' or i.isalnum()):
            return False

    return True


class Hosts:
    """The Hosts class handles translating hostnames to ip addresses."""

    def __init__(self, hosts_file):
        """Initialize the Hosts class.

        Imports all of the host names and addresses
        from the provided hosts_file. If the file does
        not follow the proper format or contains
        invalid IP addresses, hostnames, or aliases,
        an InvalidEntryError is raised.

        If successful, this function fills two lists
        (self.ips and self.hostnames) that together
        represent IP/hostname and IP/alias mappings
        in the parsed file. The hostname at index i
        in self.hostnames will correspond to the IP
        at index i in self.ips.

        For example, if the first line of a hosts file
        maps localhost to 127.0.0.1, then
        self.hostnames[0] = 'localhost' and
        self.ips[0] = '127.0.0.1'.
        """
        f = open(hosts_file, "r")

        self.ips = []
        self.hostnames = []

        line = f.readline()
        while line:
            # If the line is a comment, skip it
            if line[0] == "#":
                line = f.readline()
                continue

            # If the line is blank, skip it
            if line[0] == "\n":
                line = f.readline()
                continue

            # The first 16 characters represent the IP address
            ip_address = line[0:16]
            print(f"IP = {ip_address}")
            # Make sure to remove any trailing whitespace!
            if not is_valid_ip_address(ip_address.rstrip()):
                print("Bad IP")
                raise InvalidEntryError

            # The hostname is the first string
            # starting from the 17th character,
            # and aliases are anything after that
            rest_of_line = line[16:].split(" ")
            # hostname = rest_of_line[0]
            has_hostname = False
            for hostname in rest_of_line:
                print(hostname.rstrip())
                # If we see a comment, the rest of the line should be tossed
                if hostname.rstrip() == "#":
                    print("We're done here")
                    break
                if not is_valid_hostname(hostname.rstrip()):
                    print("Bad Hostname")
                    if hostname.rstrip() != "":
                        raise InvalidEntryError
                else:
                    # If we reach here, the line is valid, so
                    # add it to our mapping
                    has_hostname = True
                    self.ips.append(ip_address.rstrip())
                    self.hostnames.append(hostname.rstrip())

            # If we didn't find a hostname before,
            # raise an error
            if not has_hostname:
                raise InvalidEntryError

            # Read the next line
            line = f.readline()

    def contains_entry(self, hostname):
        """Return whether or not a given hostname exists."""
        #   *** YOUR CODE HERE ***

        for name in self.hostnames:
            if name == hostname:
                return True

        return False

    def get_ip(self, hostname):
        """Return the IP for a given hostname.

        If the hostname does not exist in the file,
        None is returned.
        """
        #   *** YOUR CODE HERE ***

        index = 0
        for name in self.hostnames:
            if name == hostname:
                return self.ips[index]
            else:
                index += 1
