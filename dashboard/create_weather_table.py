import sqlite3
import os

# Get absolute DB path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db", "weather_data.db")
print("Using DB at:", db_path)

# Ensure db/ directory exists
os.makedirs(os.path.join(BASE_DIR, "db"), exist_ok=True)

# Connect to DB
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        temperature REAL,
        humidity REAL,
        pressure REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# Insert sample data
cursor.execute('''
    INSERT INTO weather (temperature, humidity, pressure)
    VALUES (?, ?, ?)
''', (29.7, 68.5, 1009.3))

cursor.execute('''
    INSERT INTO weather (temperature, humidity, pressure)
    VALUES (?, ?, ?)
''', (30.2, 65.0, 1011.8))

conn.commit()
conn.close()

print("✅ Table created and sample data inserted.")
