✅  Weather Data ETL + Dashboard 

```markdown
 🌦️ Weather Data ETL + Dashboard

A complete ETL + dashboard system that fetches live weather data from the OpenWeather API, stores it in a local SQLite DB, and visualizes the data in a Streamlit dashboard with dynamic city input.

📌 Overview

Built to:
- Fetch real-time weather for any city
- Store historical data locally
- View temperature, humidity, and pressure trends
- Support both script-based ETL and UI-based data fetch

 🚀 Features

- Modular ETL system (extract, transform, load)
- Live API fetch via OpenWeatherMap
- Stores data in SQLite
- Visualizes trends using Altair/Plotly
- Search city directly from dashboard
- Save city data from UI or terminal

 🛠 Tech Stack

- Python 3.10+
- Streamlit
- SQLite
- Pandas
- Altair / Plotly
- Requests (API calls)

 📂 Folder Structure

weather_etl_dashboard/
├── etl/
│ ├── extract.py
│ ├── transform.py
│ └── load.py
├── db/
│ └── weather_data.db
├── dashboard/
│ └── app.py
├── run_etl.py
├── requirements.txt

bash
Copy
Edit

 📦 Installation

```bash
python run_etl.py           # To load initial data
streamlit run dashboard/app.py
demolink https://weatheretldashboard.streamlit.app/
