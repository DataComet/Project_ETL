import requests, json, os, configparser
import pandas as pd
from datetime import datetime as dt 
import os
import configparser
import io

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
 
# Initializes configuration from the config.ini file
config = configparser.ConfigParser()
config.read(CURR_DIR_PATH + "/config.ini")
 
# Fetches the api key from your config.ini file
API_KEY = config.get("DEV", "API_KEY")

# Initializes configuration from the config.ini file
config = configparser.ConfigParser()
config.read(CURR_DIR_PATH + "/config.ini")

# Fetches the api key from your config.ini file
API_KEY = config.get("DEV", "API_KEY")

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather/"

WEATHER_URL = "https://api.openweathermap.org/data/2.5/forecast?"

cnt = 40

geo_locations = {

    "Vienna": (48.210033, 16.363449),
    "Simbabwe": (-17.824858, 31.053028),
    "Kiev": (50.450001, 30.523333),
    "Hokuto": (35.84, 138.40),
    "Hjärup": (55.67, 13.13),
    "Melbourne": (-37.83, 144.87),
    "Ljubljana": (46.056946, 14.505751),
    "Vitoria": (-20.3194, -40.3378),
    "Valencia": (39.466667, -0.375000),
    "Konstanz": (47.6603, 9.1758),
    "Fraser Island": (-25.216667, 153.133331),
    "Crown Point": (41.416981, -87.365314)

}

def save_response(path, json_data):
    file = io.open(path, "w")
    file.write(str(json_data))
    file.close()

def request_new_weather_data():
    # For every city, fetch and store weather data

    data = []

    for city in geo_locations:
        
        (lat, lon) = geo_locations[city]

        # The parameters for the REST API call
        params = {
            "lat": lat,
            "lon": lon,
            "cnt" : cnt,
            "appid": API_KEY
        }

        # Fetching the data using HTTP method GET
        # URL using the params parameter will become:
        #   https://api.openweathermap.org/data/2.5/weather?lat=...&lon=...&appid=<your_key>
        r = requests.get(WEATHER_URL, params=params)
        

        if r.status_code == 200:
            # print(r.json())
            json_response = r.json()
            save_response(CURR_DIR_PATH + f"/{city}_json_data.json", json_response)


        
        #print("url:", r.url) # Should ressemble link from above, else check params dictionary
        #print("http code:", r.status_code) # Should be 200, else check key
        #if r.status_code == 200: # If connection is successful (200: http ok)
            #json_data = r.json() # Get result in json
            #jsonString = json.dumps(json_data)
            #jsonFile = open("json_data.json", "w")
            #jsonFile.write(str(jsonString))
            #jsonFile.close()

            json_forcast = json_response["list"]
            for json_data in json_forcast:
                weather_data = {
                    "Country": city,
                    "Precipitation": json_data["weather"][0]['main'],
                    "Precipitation description": json_data["weather"][0]['description'], # [0] because for some reason it's a single element list?
                    "Temperature": json_data["main"]['temp'],
                    "Air pressure": json_data["main"]['pressure'],
                    "clouds": json_data["clouds"],
                    "Date":  dt.fromtimestamp(json_data["dt"])
                }
                data.append(weather_data)
    df = pd.DataFrame.from_dict(data)
    df.to_json(CURR_DIR_PATH + f"/../harmonized/{str(dt.today().date()).replace(' ', '_')}.json")
    


        #daily = []
        
        #print("url:", r.url) # Should ressemble link from above, else check params dictionary
        #print("http code:", r.status_code) # Should be 200, else check key
        #if r.status_code == 200: # If connection is successful (200: http ok)
            #json_data = r.json() # Get result in json
            # Create a dictionary to represent the stored data
            # To view all accessible data see: https://openweathermap.org/current#current_JSON

            # weather_data = {
            #     "Country": json_data["sys"]['country'],
            #     "Precipitation": json_data["weather"][0]['main'],
            #     #"Precipitation description": json_data["weather"][0]['description'], # [0] because for some reason it's a single element list?
            #     #"Temperature": json_data["main"]['temp'],
            #     #"Air pressure": json_data["main"]['pressure'],
            #     "clouds": json_data["clouds"],
            #     "Date":  dt.fromtimestamp(json_data["dt"])
            # }
            # # Flattens dictionaries (normalize) because a dataframe can't contain nested dictionaries
            # # E.g. Internal dictionary {"weather": {"temp": 275, "max_temp": 289}}
            # # becomes {"weather.temp": 275, "weather.max_temp", 289}
            # weather_data = pd.json_normalize(weather_data) 
            # df = pd.DataFrame(weather_data)
            # print(df)

            #x = 0


            #for i in json_data['list']:
                #daily.append(i["main"]['pressure'])
                #daily.append(i["main"]['temp'])
                #daily.append(i["weather"][0]['main'])
                #daily.append(dt.fromtimestamp(i['dt']))
                #x += 1
                #print(x, daily)
            #df = pd.DataFrame.from_dict(daily)
            #daily = pd.json_normalize(daily) 
            #df = pd.DataFrame.from_dict(daily)
            #print(df)
     
            # weather_data = {
            #     "Country":json_data['city']['country'],
            #     "City": json_data["city"]['name'],
            #     "Precipitation": json_data['list'][0]["weather"][0]['main'],
            #     "Precipitation description": json_data['list'][0]["weather"][0]['description'], # [0] because for some reason it's a single element list?
            #     "Temperature": json_data['list'][0]["main"]['temp']-273,
            #     "Air pressure": json_data['list'][0]["main"]['pressure'],
            #     "clouds": json_data['list'][0]["clouds"],
            #     "Date":  dt.fromtimestamp(json_data['list'][0]["dt"])
            #}
            #for key,value in weather_data.items():
                #(key,value)
            # # Flattens dictionaries (normalize) because a dataframe can't contain nested dictionaries
            # # E.g. Internal dictionary {"weather": {"temp": 275, "max_temp": 289}}
            # # becomes {"weather.temp": 275, "weather.max_temp", 289}
            # weather_data = pd.json_normalize(weather_data) 
            # df = pd.DataFrame.from_dict(weather_data)
            # print(df)
# data = request_new_weather_data()

# def get_daily_data(_d=data):
#     daily= []
#     for i in json_data:

request_new_weather_data()