import os
import time
import requests
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load API key and configurations
load_dotenv()

API_KEY = "API KEY" 
LOCATIONS = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
INTERVAL = 300

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_summary (
            date TEXT,
            avg_temp REAL,
            max_temp REAL,
            min_temp REAL,
            dominant_condition TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Fetch weather data from OpenWeatherMap
def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    print(response.json())  # Print the full response for debugging
    return response.json()

# Convert temperature from Kelvin to Celsius
def kelvin_to_celsius(temp_kelvin):
    return temp_kelvin - 273.15

# Parse relevant weather data
def parse_weather_data(data):
    main_condition = data['weather'][0]['main']
    temp = kelvin_to_celsius(data['main']['temp'])
    feels_like = kelvin_to_celsius(data['main']['feels_like'])
    timestamp = data['dt']
    return {
        'condition': main_condition,
        'temp': temp,
        'feels_like': feels_like,
        'timestamp': timestamp
    }

# Calculate daily weather rollups and aggregates
def calculate_daily_summary(weather_data):
    df = pd.DataFrame(weather_data)
    avg_temp = df['temp'].mean()
    max_temp = df['temp'].max()
    min_temp = df['temp'].min()
    dominant_condition = df['condition'].mode()[0]
    return avg_temp, max_temp, min_temp, dominant_condition

# Check alert thresholds for temperature
def check_alerts(current_temp, threshold=35):
    if current_temp > threshold:
        print("Alert: Temperature exceeded threshold!")

# Store daily summaries in the database
def store_summary(date, avg_temp, max_temp, min_temp, dominant_condition):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO daily_summary (date, avg_temp, max_temp, min_temp, dominant_condition)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, avg_temp, max_temp, min_temp, dominant_condition))
    conn.commit()
    conn.close()

# Plot weather trend (visualization)
def plot_weather_trend(dates, temps):
    plt.plot(dates, temps)
    plt.xlabel('Date')
    plt.ylabel('Temperature')
    plt.title('Weather Trend')
    plt.show()

# Main logic for continuous weather monitoring
def run_weather_monitoring():
    init_db()  # Initialize database
    weather_data = []

    while True:
        for city in LOCATIONS:
            data = get_weather_data(city)
            if 'weather' not in data:  # Check if weather data was returned
                print(f"Error fetching data for {city}: {data.get('message', 'Unknown error')}")
                continue
            weather = parse_weather_data(data)
            weather_data.append(weather)
            check_alerts(weather['temp'])

        # Simulate daily rollup (you could trigger this daily in production)
        avg_temp, max_temp, min_temp, dominant_condition = calculate_daily_summary(weather_data)
        store_summary(time.strftime('%Y-%m-%d'), avg_temp, max_temp, min_temp, dominant_condition)

        # Visualization (optional)
        dates = [time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(item['timestamp'])) for item in weather_data]
        temps = [item['temp'] for item in weather_data]
        plot_weather_trend(dates, temps)

        time.sleep(INTERVAL)

# Run the system
if __name__ == "__main__":
    run_weather_monitoring()
