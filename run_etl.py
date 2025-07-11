# run_etl.py
from etl.extract import get_weather
from etl.transform import transform_weather_data
from etl.load import load_to_sqlite

def run_etl():
    cities_input = input("Enter cities separated by commas (e.g., Paris, Tokyo, Cairo): ")
    city_list = [c.strip() for c in cities_input.split(",") if c.strip()]

    for city in city_list:
        print(f"🌍 Fetching weather for {city}...")
        raw_data = get_weather(city)
        if raw_data.get("cod") == 200:
            df = transform_weather_data(raw_data, city)
            load_to_sqlite(df)
            print(f"✅ Weather data for {city} saved.\n")
        else:
            print(f"⚠️ Failed to get data for {city}: {raw_data.get('message', 'Unknown error')}")

if __name__ == "__main__":
    run_etl()
