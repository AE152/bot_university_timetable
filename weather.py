import requests
import os
from pprint import pprint
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def get_weather():
   r = requests.get( f"https://api.openweathermap.org/data/2.5/weather?lat=55.01342&lon=82.9493&appid={os.getenv('TOKENWEATHER')}&units=metric")
   data = r.json()

   cur_weather = data["main"]["temp"]
   wind = data["wind"]["speed"]
   weath = data["weather"][0]["description"]
   return(f"{cur_weather}°C\n{weath}")

get_weather()