"""
This file contains helper functions that will aid the running program
"""

import re
import requests
from collections import defaultdict

GHANA_POST_URL = "https://ghanapostgps.sperixlabs.org/get-location"


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


def query_ghpost_api(source_address: str, dest_address: str) -> defaultdict[list[int]] or None:
    """
    This function queries the Ghana Post GPS API using the obtained digital addresses
    to get the data required to find the routes on a Google Map
    :param source_address: the source address the user wants to search from
    :param dest_address: the destination address the user will search for
    :return:
    """
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    address_geolocations = defaultdict(list[int])

    source_response = requests.post(GHANA_POST_URL, data=f"address={source_address}", headers=headers).json()
    destination_response = requests.post(GHANA_POST_URL, data=f"address={dest_address}", headers=headers).json()

    if source_response['found'] and destination_response['found']:
        source_lat, source_long = source_response['data']['Table'][0]['CenterLatitude'], \
                                  source_response['data']['Table'][0]['CenterLongitude']
        dest_lat, dest_long = destination_response['data']['Table'][0]['CenterLatitude'], \
                              destination_response['data']['Table'][0]['CenterLongitude']

        address_geolocations['source_address'] = [source_lat, source_long]
        address_geolocations['destination_address'] = [dest_lat, dest_long]

        return address_geolocations
    else:
        return None

