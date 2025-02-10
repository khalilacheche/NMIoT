import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

from threading import Thread
import json
from src.threads import SharedData
from time import sleep


class WeatherManager (Thread):
    def __init__(self, ):
        Thread.__init__(self)
        self.daily_data = SharedData()
        self.daily_data.update([{
            "date": 0,
            "temp_min": 0,
            "temp_max": 0,
            "weather_code": 0,
        }])


        self.current_data = SharedData()
        self.current_data.update([{
            "temperature": 0,
            "apparent_temperature": 0,
            "weather_code": 0,
        }])
    
    def run(self):
        while True:
            self.fetch_data()
            sleep(3600)
    

    def fetch_data(self):
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)

        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 47.0432,
            "longitude": 1.1831,
            "current": ["temperature_2m", "apparent_temperature", "weather_code"],
            "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "precipitation_probability_max"]
        }


        responses = openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]


        current = response.Current()
        current_temperature_2m = current.Variables(0).Value()
        current_apparent_temperature = current.Variables(1).Value()
        current_weather_code = current.Variables(2).Value()
        self.current_data.update([{
            "temperature": current_temperature_2m,
            "apparent_temperature": current_apparent_temperature,
            "weather_code": current_weather_code,
        }])




        daily = response.Daily()
        daily_weather_code = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
        daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
        daily_precipitation_probability_max = daily.Variables(3).ValuesAsNumpy()

        daily_data = {"date": pd.date_range(
            start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
            end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = daily.Interval()),
            inclusive = "left"
        )}

        daily_data["weather_code"] = daily_weather_code
        daily_data["temp_max"] = daily_temperature_2m_max
        daily_data["temp_min"] = daily_temperature_2m_min
        daily_data["precipitation_probability_max"] = daily_precipitation_probability_max
        daily_dataframe = pd.DataFrame(data = daily_data)
        daily_dataframe["date"] = daily_dataframe["date"].dt.strftime("%d/%m")
        recs = daily_dataframe.to_dict(orient = "records")
        self.daily_data.update(recs)


    

