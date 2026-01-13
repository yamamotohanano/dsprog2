import sqlite3
from datetime import datetime

DB_NAME = "weather.db"

def get_conn():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS weather_forecast (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        area_code TEXT,
        area_name TEXT,
        date TEXT,
        weather TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_weather(area_code, area_name, date, weather):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO weather_forecast
        (area_code, area_name, date, weather, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (area_code, area_name, date, weather, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_weather_from_db(area_code):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT date, weather FROM weather_forecast
        WHERE area_code = ?
        ORDER BY date DESC
        LIMIT 3
    """, (area_code,))
    rows = cur.fetchall()
    conn.close()
    return rows
