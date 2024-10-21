# Real-Time Weather Monitoring System with Rollups and Aggregates

## Objective

This project is a real-time data processing system that monitors weather conditions and provides summarized insights using rollups and aggregates. The system retrieves data from the OpenWeatherMap API, processes weather updates for selected cities in India, and stores daily summaries in an SQLite database. 

## **Features**

1. **Real-time Weather Data Monitoring**:
   - Retrieves weather data for Indian metro cities: Delhi, Mumbai, Chennai, Bangalore, Kolkata, Hyderabad.
   - Converts temperature values from Kelvin to Celsius for user convenience.

2. **Weather Data Aggregation**:
   - Calculates and stores daily summaries for each city, including:
     - Average temperature.
     - Maximum and minimum temperatures.
     - Dominant weather condition.

3. **Alert System**:
   - Monitors weather data against user-configurable thresholds (e.g., temperature exceeding 35°C) and triggers alerts when thresholds are breached.

4. **Data Storage**:
   - Stores daily weather summaries in an SQLite database (`weather_data.db`).

5. **Visualization**:
   - Generates visualizations for weather trends such as temperature changes over time using Matplotlib.

### **Project Setup**

### **Prerequisites**

- **Python 3.x** installed.
- **OpenWeatherMap API Key** (Sign up for a free API key at [OpenWeatherMap](https://openweathermap.org)).

### **Installation Instructions**

1. **Clone the repository**:

   bash
   git clone https://github.com/your-username/weather-monitoring-system.git
   cd weather-monitoring-system
