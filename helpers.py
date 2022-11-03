"""
This file contains helper functions that will aid the running program
"""


import re


def is_valid_input(source_address: str, dest_address: str) -> bool:
    """
    This function takes the form inputs and validates it by searching for the specified regex pattern
    and ensuring that the length of the input is either 9 or 11.

    :param source_address: the source address the user wants to search from
    :param dest_address: the destination address the user will search for
    :return: bool
    """
    source_match = re.search("^[A-Z]{2}-[0-9]{3}-[0-9]{4}$||^[A-Z]{2}[0-9]{7}$", source_address)
    dest_match = re.search("^[A-Z]{2}-[0-9]{3}-[0-9]{4}$||^[A-Z]{2}[0-9]{7}$", dest_address)

    if (source_match and dest_match) and (len(source_address) == 9 or len(source_address) == 11 and len(dest_address) ==
                                          9 or len(dest_address) == 11):
        return True

    return False
