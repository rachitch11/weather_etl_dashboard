# etl/load.py
import sqlite3
import os

def load_to_sqlite(df, db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='weather'")
        if not cursor.fetchone():
            cursor.execute('''
                CREATE TABLE weather (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city TEXT,
                    temperature REAL,
                    humidity REAL,
                    pressure REAL,
                    timestamp TEXT
                )
            ''')

        # Insert data
        df.to_sql("weather", conn, if_exists="append", index=False)
        conn.commit()
        conn.close()
        print("✅ Data inserted successfully into:", db_path)
    except Exception as e:
        print("❌ Error inserting into DB:", e)
