"""Create a list from user inputs, then sort and print it

Author: Jason Gardiner
Class: CSI-275-01
Assignment: Lab 1 -- Sorting With Python

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


def build_list():
    # build a list from user inputs
    my_list = []
    question = "If you would like to add a float to your list, type a float.\nOtherwise type DONE: "
    user_input = input(question)
    # repeat until the user inputs DONE, not caps sensitive
    while user_input.upper() != "DONE":
        try:
            # if the input is not a float, it will be rejected
            as_float = float(user_input)
            my_list.append(as_float)
        except ValueError:
            print(user_input, "is not a float.")
        user_input = input(question)

    return my_list


def sort_list(my_list):
    # sort the list
    my_list.sort()


def main():
    my_list = build_list()
    sort_list(my_list)
    print(my_list)


if __name__ == "__main__":
    main()
