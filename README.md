Real-Time Weather Monitoring System with Rollups and Aggregates
Objective
This project is a real-time data processing system designed to monitor weather conditions and provide summarized insights using rollups and aggregates. The system retrieves data from the OpenWeatherMap API, processes weather updates for selected cities in India, and stores daily summaries in an SQLite database.

Features
Real-time Weather Data Monitoring:

Retrieves weather data for Indian metro cities: Delhi, Mumbai, Chennai, Bangalore, Kolkata, Hyderabad.
Converts temperature values from Kelvin to Celsius for ease of use.
Weather Data Aggregation:

Calculates and stores daily summaries for each city, including:
Average temperature.
Maximum and minimum temperatures.
Dominant weather condition.
Alert System:

Monitors weather data against user-configurable thresholds (e.g., temperature exceeding 35°C) and triggers alerts when thresholds are breached.
Data Storage:

Stores daily weather summaries in an SQLite database (weather_data.db).
Visualization:

Generates visualizations for weather trends, such as temperature changes over time, using Matplotlib.
Project Setup
Prerequisites
Python 3.x installed.
OpenWeatherMap API Key (Sign up for a free API key at OpenWeatherMap).
