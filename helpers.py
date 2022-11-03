"""
This file contains helper functions that will aid the running program
"""


import re

'''
This function takes the form inputs and validates it by searching for the specified regex pattern
and ensuring that the length of the input is either 9 or 11.

:param digital_address: the source or destination user address the user wants to search for
:return: bool
'''


def is_valid_input(digital_address: str) -> bool:
    match = re.search("^[A-Z]{2}-[0-9]{3}-[0-9]{4}$||^[A-Z]{2}[0-9]{7}$", digital_address)
    if match and (len(digital_address) == 9 or len(digital_address) == 11):
        return True
    return False