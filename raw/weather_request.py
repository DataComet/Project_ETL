import requests, json
import pandas as pd
from datetime import datetime as dt 
import os
import configparser
 
# Initializes configuration from the config.ini file
config = configparser.ConfigParser()
config.read(CURR_DIR_PATH + "/config.ini")
 
# Fetches the api key from your config.ini file
API_KEY = config.get("DEV", "API_KEY")
 


WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather/"



geo_locations = {
    "Nagano": (36.65, 138.18333)
}


def request_new_weather_data():
    # For every city, fetch and store weather data
    for city in geo_locations:
        (lat, lon) = geo_locations[city]

        # The parameters for the REST API call
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY
        }

        # Fetching the data using HTTP method GET
        # URL using the params parameter will become:
        #   https://api.openweathermap.org/data/2.5/weather?lat=...&lon=...&appid=<your_key>
        r = requests.get(WEATHER_URL, params=params)
        
        
        print("url:", r.url) # Should ressemble link from above, else check params dictionary
        print("http code:", r.status_code) # Should be 200, else check key
        if r.status_code == 200: # If connection is successful (200: http ok)
            json_data = r.json() # Get result in json

            # Create a dictionary to represent the stored data
            # To view all accessible data see: https://openweathermap.org/current#current_JSON
            weather_data = {
                "Precipitation": json_data["weather"][0]['main'],
                "Precipitation description": json_data["weather"][0]['description'], # [0] because for some reason it's a single element list?
                "Temperature": json_data["main"]['temp'],
                "Air pressure": json_data["main"]['pressure'],
                "clouds": json_data["clouds"],
                "Date":  dt.fromtimestamp(json_data["dt"])
            }
            # Flattens dictionaries (normalize) because a dataframe can't contain nested dictionaries
            # E.g. Internal dictionary {"weather": {"temp": 275, "max_temp": 289}}
            # becomes {"weather.temp": 275, "weather.max_temp", 289}
            weather_data = pd.json_normalize(weather_data) 
            print(weather_data)


request_new_weather_data()