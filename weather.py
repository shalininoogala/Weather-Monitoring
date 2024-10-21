import os
import time
import requests
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import logging
from datetime import datetime

# Load API key and configurations from environment variables
load_dotenv()

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_KEY = os.getenv("OPENWEATHER_API_KEY")
ALERT_EMAIL = os.getenv("ALERT_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")  # Default SMTP server
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))  # Default SMTP port
LOCATIONS = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
INTERVAL = int(os.getenv("INTERVAL", 300))  # Default 5 minutes in seconds
TEMP_THRESHOLD = float(os.getenv("TEMP_THRESHOLD", 35))  # Default threshold: 35°C

def init_db():
    """Initialize the SQLite database and create the daily_summary table."""
    with sqlite3.connect('weather_data.db') as conn:
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

def get_weather_data(city):
    """Fetch weather data for a specified city from the OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data for {city}: {e}")
        return None

def kelvin_to_celsius(temp_kelvin):
    """Convert temperature from Kelvin to Celsius."""
    return temp_kelvin - 273.15

def parse_weather_data(data):
    """Parse relevant weather data from the API response."""
    if data:
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
    return None

def calculate_daily_summary(weather_data):
    """Calculate daily weather rollups and aggregates."""
    df = pd.DataFrame(weather_data)
    avg_temp = df['temp'].mean()
    max_temp = df['temp'].max()
    min_temp = df['temp'].min()
    dominant_condition = df['condition'].mode()[0]
    return avg_temp, max_temp, min_temp, dominant_condition

def check_alerts(current_temp):
    """Check if the current temperature exceeds the defined threshold."""
    if current_temp > TEMP_THRESHOLD:
        send_alert(f"Temperature Alert! The current temperature is {current_temp:.2f}°C")

def send_alert(message):
    """Send an email alert for temperature warnings."""
    if ALERT_EMAIL and EMAIL_PASSWORD:
        msg = MIMEMultipart()
        msg['From'] = ALERT_EMAIL
        msg['To'] = ALERT_EMAIL
        msg['Subject'] = "Weather Alert"

        msg.attach(MIMEText(message, 'plain'))

        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(ALERT_EMAIL, EMAIL_PASSWORD)
            server.sendmail(ALERT_EMAIL, ALERT_EMAIL, msg.as_string())
            server.quit()
            logging.info("Alert email sent successfully!")
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
    else:
        logging.warning("Email alerts not configured. Please set ALERT_EMAIL and EMAIL_PASSWORD.")

def store_summary(date, avg_temp, max_temp, min_temp, dominant_condition):
    """Store daily summaries in the SQLite database."""
    with sqlite3.connect('weather_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO daily_summary (date, avg_temp, max_temp, min_temp, dominant_condition)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, avg_temp, max_temp, min_temp, dominant_condition))
        conn.commit()

def plot_weather_trend(dates, temps):
    """Plot the weather trend using Matplotlib."""
    plt.figure(figsize=(10, 5))
    plt.plot(dates, temps, marker='o')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title('Weather Trend')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('weather_trend.png')  # Save the plot as a file
    plt.show()

def run_weather_monitoring():
    """Main logic for continuous weather monitoring."""
    init_db()  # Initialize the database
    weather_data = []

    while True:
        for city in LOCATIONS:
            data = get_weather_data(city)
            weather = parse_weather_data(data)
            if weather:
                weather_data.append(weather)
                check_alerts(weather['temp'])

        if weather_data:
            current_date = datetime.now().strftime('%Y-%m-%d')
            avg_temp, max_temp, min_temp, dominant_condition = calculate_daily_summary(weather_data)
            store_summary(current_date, avg_temp, max_temp, min_temp, dominant_condition)

            # Visualization
            dates = [datetime.fromtimestamp(item['timestamp']).strftime('%Y-%m-%d %H:%M:%S') for item in weather_data]
            temps = [item['temp'] for item in weather_data]
            plot_weather_trend(dates, temps)

            # Clear data for the next day's summary
            weather_data.clear()

        time.sleep(INTERVAL)

# Run the system
if __name__ == "__main__":
    run_weather_monitoring()
