# dashboard/app.py

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

# 🔧 Add root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from etl.extract import get_weather
from etl.transform import transform_weather_data

# 📄 Streamlit page setup
st.set_page_config(page_title="🌍 Live Weather Dashboard", layout="centered")
st.title("🌍 Weather Data Dashboard")
st.caption("📡 Powered by OpenWeather API — live data only")

# =======================
# 🔍 Live City Search Only
# =======================
st.markdown("### 🔍 Search Weather for Any City")
city_input = st.text_input("Enter a city name")

if city_input:
    if st.button("🔍 Fetch Weather"):
        with st.spinner("Fetching weather data..."):
            data = get_weather(city_input)
            if data.get("cod") == 200:
                live_df = transform_weather_data(data, city_input)
                st.success(f"✅ Weather fetched for {city_input}")
                st.dataframe(live_df)

                # 📈 Plot chart
                st.subheader(f"📊 Weather Trends for {city_input}")
                live_df["timestamp"] = pd.to_datetime(live_df["timestamp"])
                live_df.set_index("timestamp", inplace=True)

                fig, ax = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

                ax[0].plot(live_df.index, live_df["temperature"], color="red", marker="o")
                ax[0].set_ylabel("🌡️ Temp (°C)")
                ax[0].grid(True)

                ax[1].plot(live_df.index, live_df["humidity"], color="blue", marker="o")
                ax[1].set_ylabel("💧 Humidity (%)")
                ax[1].grid(True)

                ax[2].plot(live_df.index, live_df["pressure"], color="green", marker="o")
                ax[2].set_ylabel("📊 Pressure (hPa)")
                ax[2].set_xlabel("🕒 Time")
                ax[2].grid(True)

                plt.tight_layout()
                st.pyplot(fig)
            else:
                st.error(f"❌ API Error: {data.get('message', 'Unknown error')}")
