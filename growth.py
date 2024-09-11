import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# Set your OpenWeather API key
API_KEY = '4c10b56a6a4f1f4f74ce5d582a2f69db'

# Plant database with ideal conditions (sample based on your provided plants)
plant_database = {
    'Spider Plant': {'temp': (15, 30), 'humidity': (40, 80), 'pm25': (0, 25), 'pm10': (0, 50), 'co': (0, 50), 'no2': (0, 50), 'so2': (0, 30), 'o3': (0, 40), 'growth_rate': 0.03},
    'Aloe Vera': {'temp': (20, 35), 'humidity': (20, 60), 'pm25': (0, 15), 'pm10': (0, 30), 'co': (0, 50), 'no2': (0, 40), 'so2': (0, 20), 'o3': (0, 25), 'growth_rate': 0.02},
    'Areca Palm': {'temp': (18, 35), 'humidity': (40, 70), 'pm25': (0, 30), 'pm10': (0, 50), 'co': (0, 60), 'no2': (0, 60), 'so2': (0, 40), 'o3': (0, 35), 'growth_rate': 0.05},
    'Money Plant': {'temp': (18, 32), 'humidity': (30, 60), 'pm25': (0, 20), 'pm10': (0, 40), 'co': (0, 50), 'no2': (0, 40), 'so2': (0, 20), 'o3': (0, 25), 'growth_rate': 0.03},
    'Snake Plant': {'temp': (15, 30), 'humidity': (30, 70), 'pm25': (0, 20), 'pm10': (0, 40), 'co': (0, 50), 'no2': (0, 50), 'so2': (0, 20), 'o3': (0, 30), 'growth_rate': 0.02},
    'Gerbera Daisy': {'temp': (16, 25), 'humidity': (50, 80), 'pm25': (0, 30), 'pm10': (0, 60), 'co': (0, 40), 'no2': (0, 40), 'so2': (0, 20), 'o3': (0, 35), 'growth_rate': 0.04},
    'Chrysanthemum': {'temp': (18, 30), 'humidity': (40, 70), 'pm25': (0, 25), 'pm10': (0, 50), 'co': (0, 45), 'no2': (0, 50), 'so2': (0, 25), 'o3': (0, 30), 'growth_rate': 0.05},
    'Rubber Plant': {'temp': (15, 30), 'humidity': (40, 80), 'pm25': (0, 25), 'pm10': (0, 50), 'co': (0, 50), 'no2': (0, 50), 'so2': (0, 30), 'o3': (0, 40), 'growth_rate': 0.03},
    'Bamboo Palm': {'temp': (18, 35), 'humidity': (50, 70), 'pm25': (0, 20), 'pm10': (0, 40), 'co': (0, 45), 'no2': (0, 40), 'so2': (0, 20), 'o3': (0, 30), 'growth_rate': 0.04},
    'Ficus': {'temp': (15, 32), 'humidity': (40, 80), 'pm25': (0, 25), 'pm10': (0, 50), 'co': (0, 50), 'no2': (0, 45), 'so2': (0, 25), 'o3': (0, 35), 'growth_rate': 0.03},
    'Tulsi': {'temp': (20, 35), 'humidity': (40, 80), 'pm25': (0, 30), 'pm10': (0, 50), 'co': (0, 40), 'no2': (0, 50), 'so2': (0, 35), 'o3': (0, 40), 'growth_rate': 0.06},
    'Neem': {'temp': (18, 38), 'humidity': (30, 80), 'pm25': (0, 30), 'pm10': (0, 50), 'co': (0, 45), 'no2': (0, 60), 'so2': (0, 40), 'o3': (0, 45), 'growth_rate': 0.07},
    'Peace Lily': {'temp': (15, 32), 'humidity': (40, 80), 'pm25': (0, 20), 'pm10': (0, 40), 'co': (0, 50), 'no2': (0, 45), 'so2': (0, 30), 'o3': (0, 35), 'growth_rate': 0.04},
    'Boston Fern': {'temp': (15, 28), 'humidity': (50, 90), 'pm25': (0, 30), 'pm10': (0, 50), 'co': (0, 40), 'no2': (0, 50), 'so2': (0, 30), 'o3': (0, 30), 'growth_rate': 0.03},
    'Golden Pothos': {'temp': (18, 30), 'humidity': (40, 70), 'pm25': (0, 20), 'pm10': (0, 40), 'co': (0, 50), 'no2': (0, 40), 'so2': (0, 20), 'o3': (0, 25), 'growth_rate': 0.03},
    'English Ivy': {'temp': (10, 25), 'humidity': (40, 80), 'pm25': (0, 15), 'pm10': (0, 30), 'co': (0, 40), 'no2': (0, 30), 'so2': (0, 25), 'o3': (0, 30), 'growth_rate': 0.02}
}


# Function to get weather data (current, forecast, and historical)
def get_weather_data(lat, lon):
    # Get current weather
    url_current = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    weather_current = requests.get(url_current).json()
    
    # Get forecast weather
    url_forecast = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    weather_forecast = requests.get(url_forecast).json()
    
    return weather_current, weather_forecast

# Function to get air pollution data
def get_air_pollution(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)
    return response.json()

# Function to evaluate plant growth health based on weather and pollution data
def evaluate_growth(plant, weather, pollution, initial_height, plant_age_months):
    temp = weather['main']['temp']
    humidity = weather['main']['humidity']
    
    # Get pollution data (PM2.5, NO2, etc.)
    pm25 = pollution['list'][0]['components']['pm2_5']
    no2 = pollution['list'][0]['components']['no2']
    
    # Get plant's ideal growth conditions
    ideal_conditions = plant_database.get(plant, {})
    
    # Check environmental conditions against ideal conditions
    temp_check = ideal_conditions['temp'][0] <= temp <= ideal_conditions['temp'][1]
    humidity_check = ideal_conditions['humidity'][0] <= humidity <= ideal_conditions['humidity'][1]
    pm25_check = ideal_conditions['pm25'][0] <= pm25 <= ideal_conditions['pm25'][1]
    no2_check = ideal_conditions['no2'][0] <= no2 <= ideal_conditions['no2'][1]
    
    # Growth health score (based on percentage of conditions met)
    growth_health_score = sum([temp_check, humidity_check, pm25_check, no2_check]) / 4
    
    # Plant's growth rate and adjusted by its age (older plants grow slower)
    growth_rate = ideal_conditions['growth_rate'] * (1 - (plant_age_months / 100))  # Slows down as plant ages
    
    # Calculate predicted growth (in cm) for the past and next months
    past_growth = initial_height * growth_rate * growth_health_score * -1  # Previous month
    future_growth = initial_height * growth_rate * growth_health_score      # Next month
    
    return growth_health_score, past_growth, future_growth

# Streamlit app layout
st.title('Plant Growth Health Verification 🌱')
st.write("This app verifies the growth health of plants based on current weather and air quality conditions, with predictions for past and future growth.")

# User input: city, plant, initial height, and plant age
city = st.text_input("Enter the city name:", "Chennai")
plant = st.selectbox("Select a plant to verify:", list(plant_database.keys()))
initial_height = st.number_input("Enter the initial height of the plant (in cm):", min_value=0, value=10)
plant_age_months = st.slider("Select the plant's age (in months):", min_value=1, max_value=60, value=6)

# Fetch data and evaluate growth
if st.button('Check Growth Health'):
    # Get geolocation for the city (geocoding API)
    url_geocode = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    geocode_data = requests.get(url_geocode).json()

    # Check if 'coord' is in the response, handle the error
    if 'coord' in geocode_data:
        lat = geocode_data['coord']['lat']
        lon = geocode_data['coord']['lon']
        
        # Get weather and pollution data
        weather_current, weather_forecast = get_weather_data(lat, lon)
        pollution = get_air_pollution(lat, lon)
        
        # Display current weather data
        st.subheader(f"Current Weather in {city}")
        st.write(f"Temperature: {weather_current['main']['temp']} °C")
        st.write(f"Humidity: {weather_current['main']['humidity']} %")
        st.write(f"Pressure: {weather_current['main']['pressure']} hPa")
        st.write(f"Wind Speed: {weather_current['wind']['speed']} m/s")
        
        # Display air pollution data
        st.subheader(f"Air Quality in {city}")
        st.write(f"PM2.5: {pollution['list'][0]['components']['pm2_5']} µg/m³")
        st.write(f"NO2: {pollution['list'][0]['components']['no2']} µg/m³")
        
        # Evaluate plant growth health and predict growth for past and next months
        growth_health_score, past_growth, future_growth = evaluate_growth(
            plant, weather_current, pollution, initial_height, plant_age_months
        )
        
        # Display growth health score and growth predictions
        st.subheader(f"Growth Health of {plant}")
        st.write(f"Growth Health Score: {growth_health_score * 100:.2f}%")
        st.write(f"Estimated Growth in the Past Month: {past_growth:.2f} cm")
        st.write(f"Estimated Growth in the Next Month: {future_growth:.2f} cm")
    
    else:
        st.error("City not found. Please check the city name and try again.")
