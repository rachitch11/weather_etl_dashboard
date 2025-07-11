# dashboard/app.py
import os
import sys
import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# 🔧 Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from etl.extract import get_weather
from etl.transform import transform_weather_data
from etl.load import load_to_sqlite

# 📄 DB Path
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "db", "weather_data.db"))
st.set_page_config(page_title="🌍 Weather Dashboard", layout="centered")
st.title("🌍 Weather Data Dashboard")
st.caption("📡 Live Weather ETL Dashboard powered by OpenWeather API")
st.text(f"Database Path: {DB_PATH}")

# =======================
# 📁 Load DB Data (once)
# =======================
def load_database():
    if os.path.exists(DB_PATH):
        try:
            with sqlite3.connect(DB_PATH) as conn:
                df = pd.read_sql("SELECT * FROM weather", conn)
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df.sort_values("timestamp", ascending=False)
            return df
        except Exception as e:
            st.error(f"❌ Failed to read database: {e}")
    return pd.DataFrame()

df = load_database()

# =======================
# 🔍 Section 1: Live Search
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

                if st.checkbox("💾 Save this to database?"):
                    load_to_sqlite(live_df, db_path=DB_PATH)
                    st.success("✅ Saved to database")

                    # Reload updated DB
                    df = load_database()

                # Plot weather trends
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

st.markdown("---")

# =======================
# 📁 Section 2: Saved Data
# =======================
if not df.empty and "city" in df.columns:
    st.markdown("### 📍 View Saved City Data")
    cities = df["city"].dropna().unique()
    selected_city = st.selectbox("Select city", cities)
    filtered_df = df[df["city"] == selected_city]

    st.dataframe(filtered_df)

    if not filtered_df.empty:
        st.subheader("📈 Weather Trends for Saved City")
        filtered_df["timestamp"] = pd.to_datetime(filtered_df["timestamp"])
        filtered_df.set_index("timestamp", inplace=True)

        fig, ax = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

        ax[0].plot(filtered_df.index, filtered_df["temperature"], color="red", marker="o")
        ax[0].set_ylabel("🌡️ Temp (°C)")
        ax[0].grid(True)

        ax[1].plot(filtered_df.index, filtered_df["humidity"], color="blue", marker="o")
        ax[1].set_ylabel("💧 Humidity (%)")
        ax[1].grid(True)

        ax[2].plot(filtered_df.index, filtered_df["pressure"], color="green", marker="o")
        ax[2].set_ylabel("📊 Pressure (hPa)")
        ax[2].set_xlabel("🕒 Time")
        ax[2].grid(True)

        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info("No data available for this city.")
else:
    st.info("📂 No saved weather data available yet.")
