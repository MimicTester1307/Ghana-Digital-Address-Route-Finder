"""
This file contains helper functions that will aid the running program
"""
import os
import re
import requests
from collections import defaultdict
import googlemaps
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('MAPS_API_KEY')
GHANA_POST_URL = "https://ghanapostgps.sperixlabs.org/get-location"
gmaps = googlemaps.Client(key=API_KEY)


def is_valid_input(source_address: str, dest_address: str) -> bool:
    """
    takes the form inputs and validates it by searching for the specified regex pattern
    and ensuring that the length of the input is either 9 or 11.

    :param source_address: the source address the user wants to search from
    :param dest_address: the destination address the user will search for
    :return: bool
    """
    source_match = re.search("^[a-zA-Z0-9]{2}(?:-?\d{3}-?\d{4})$", source_address)
    dest_match = re.search("^[a-zA-Z0-9]{2}(?:-?\d{3}-?\d{4})$", dest_address)

    if (source_match and dest_match) and (len(source_address) == 9 or len(source_address) == 11 and len(dest_address) ==
                                          9 or len(dest_address) == 11):
        return True

    return False


def query_ghpost_api(source_address: str, dest_address: str) -> defaultdict[list[float]] or None:
    """
    queries the Ghana Post GPS API using the obtained digital addresses
    to get the data required to find the routes on a Google Map
    :param source_address: the source address the user wants to search from
    :param dest_address: the destination address the user will search for
    :return: defaultdict[list[float]] or None
    """
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    address_geolocations = defaultdict(list[int])

    source_response = requests.post(GHANA_POST_URL, data=f"address={source_address}", headers=headers).json()
    destination_response = requests.post(GHANA_POST_URL, data=f"address={dest_address}", headers=headers).json()

    if source_response.get('found') and destination_response.get('found'):
        source_lat, source_long = source_response['data']['Table'][0]['CenterLatitude'], \
                                  source_response['data']['Table'][0]['CenterLongitude']
        dest_lat, dest_long = destination_response['data']['Table'][0]['CenterLatitude'], \
                              destination_response['data']['Table'][0]['CenterLongitude']

        address_geolocations['source_address'] = [source_lat, source_long]
        address_geolocations['destination_address'] = [dest_lat, dest_long]

        return address_geolocations
    else:
        return None


def get_location_details(latitude: float, longitude: float) -> tuple or None:
    """"
    queries the Geocoding API to reverse geocode the given latitude and longitude into
    a human-readable address
    :param latitude: coordinate latitude
    :param longitude: coordinate longitude
    :return tuple or None
    """
    location_details = gmaps.reverse_geocode(latlng=(latitude, longitude),
                                             result_type=["premise", "subpremise", "street_address", "route", "intersection", "neighborhood"],
                                             # filters out quite a number of results. Assumption is that system is
                                             # being used for locations within cities
                                             location_type=["APPROXIMATE", "GEOMETRIC_CENTER"])  # Adding GEOMETRIC_CENTER to make up for some inaccuracies and lack of specific coordinates

    # return place id and use for search instead, because the data returned by the API is a lot, and
    # place id is easier to get and is a unique identifier of a place, which I think is more specific
    if len(location_details) > 0:
        return location_details[0].get('place_id'), location_details[0].get('formatted_address')
    return None


