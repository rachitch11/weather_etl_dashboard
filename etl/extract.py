# etl/extract.py
import requests

API_KEY = "b6a9d99e3ef89d19f11fceefe00b1cbe"  # Replace with your API key

def get_weather(city="Delhi"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()
