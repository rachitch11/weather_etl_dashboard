# etl/transform.py
import pandas as pd
from datetime import datetime

def transform_weather_data(data, city):
    return pd.DataFrame([{
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
