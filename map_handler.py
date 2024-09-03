# map_handler.py
import requests
from dotenv import load_dotenv
import os

load_dotenv()
LOCATIONIQ_API_KEY = os.getenv("API_KEY")

def dummy_get_start_end_coordinates():

    start_lat = 9.12  # Ex start lat
    start_lon =  78.99 # Ex start long
    end_lat =  9.56 # Ex end lat
    end_lon = 80.52 # Ex end long

    return (start_lat, start_lon), (end_lat, end_lon)

def get_coordinates(address):

    url = f"https://us1.locationiq.com/v1/search.php"
    params = {
        'key': LOCATIONIQ_API_KEY,
        'q': address,
        'format': 'json'
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()[0]
        return (float(data['lat']), float(data['lon']))
    else:
        print("Error: Unable to fetch coordinates.")
        return None

def display_map_and_select_points():
    start_address = "Statue of Liberty, New York, NY"
    end_address = "Central Park, New York, NY"

    start_coords = get_coordinates(start_address)
    end_coords = get_coordinates(end_address)

    if start_coords and end_coords:
        print(f"Start Point: {start_coords}, End Point: {end_coords}")
        return start_coords, end_coords
    else:
        raise Exception("Failed to get coordinates for the specified addresses.")

# coords = display_map_and_select_points()


