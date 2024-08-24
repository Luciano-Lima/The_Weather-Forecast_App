from flask import Flask, render_template, request, flash
# import time
from datetime import datetime, timezone, timedelta
import requests
import os

from os import path
from collections import defaultdict

#load enviroment variables
if path.exists('env.py'):
    import env

class WeatherApp:
     # Initialize Flask app
    def __init__(self):
        self.app = Flask(__name__)
        self.api_key = os.environ.get('API_KEY')
        self.app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')
        # Define the route for the home page
        self.app.add_url_rule('/', 'index', self.index, methods=['GET', 'POST'])


    def calculate_local_time(self, timestamp, timezone_offset):
        """
        Convert UTC timestamp to local time using the provided timezone offset.
        """
        utc_time = datetime.utcfromtimestamp(timestamp) # Convert timestamp to UTC time
        local_time = utc_time + timedelta(seconds=timezone_offset) # Apply timezone offset
        return local_time.strftime('%Y-%m-%d %H:%M')


    def get_current_day(self):
        return datetime.now().strftime('%a')  # Short day name like 'Sat'


    def group_forecasts_by_day(self, forecasts, timezone_offset):
        """
        Group weather forecasts by day, skipping past times of the current day.
        """
        forecasts_by_day = defaultdict(list) # Create a dictionary to hold forecasts by day
        current_utc_time = datetime.now(timezone.utc) # Get the current UTC time
        current_local_time = current_utc_time + timedelta(seconds=timezone_offset) # Convert to local time
        current_day = current_local_time.strftime('%a')  # Get current day abbreviation (e.g. Saturday, 'Sat')
        current_time = current_local_time.strftime('%H:%M')  # Get the current time in hours and minutes

        skip_current_day = True  #Skip the current day in the forecast

        for forecast in forecasts:
            # Calculate local time for each forecast
            local_time = self.calculate_local_time(forecast['dt'], timezone_offset)
            date, time = local_time.split(' ')
            day_of_week = datetime.strptime(date, '%Y-%m-%d').strftime('%a')

            if day_of_week == current_day and time < current_time:
                continue # Skip past times of the current day

            if skip_current_day and day_of_week == current_day:
                skip_current_day = False  # Start including days after the current day

            weather = {
                'day': day_of_week,
                "time": time,
                "temperature": int(forecast['main']['temp']),
                "icon": forecast['weather'][0]['icon'],
                "description": forecast['weather'][0]['description'],
                "humidity": forecast['main']['humidity'],
                "wind": int(forecast['wind']['speed']),
                "feels_like": int(forecast['main']['feels_like']),
                "dt_time": local_time,
            }
            # Group the forecast by the day of the week
            forecasts_by_day[day_of_week].append(weather)

        return dict(forecasts_by_day) # Convert defaultdict to a regular dictionary


    def get_weather(self, city):
        """
        Fetch weather data from the OpenWeatherMap API for the given city.
        """
        # API URLs for 5-day forecast and current weather
        forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={self.api_key}&units=metric'
        current_weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric'

        forecast_response = requests.get(forecast_url)
        current_weather_response = requests.get(current_weather_url)

        current_day = datetime.now().strftime('%a')

        if forecast_response.status_code == 200 and current_weather_response.status_code == 200:
            forecast_data = forecast_response.json()
            current_weather_data = current_weather_response.json()

            # Group the forecasts by day
            forecasts_by_day = self.group_forecasts_by_day(forecast_data['list'], forecast_data['city']['timezone'])

            # Extracting current weather details
            current_weather = {
                'temperature': int(current_weather_data['main']['temp']),
                'feels_like': int(current_weather_data['main']['feels_like']),
                'icon': current_weather_data['weather'][0]['icon'],
                'description': current_weather_data['weather'][0]['description'],
                'humidity': current_weather_data['main']['humidity'],
                'wind': int(current_weather_data['wind']['speed']),
                'dt_time': self.calculate_local_time(current_weather_data['dt'], forecast_data['city']['timezone']),
                'time': datetime.now().strftime('%H:%M')  # Get the current time
            }

            return render_template('index.html', forecasts_by_day=forecasts_by_day, city=city, current_weather=current_weather,current_day=current_day)
        elif forecast_response.status_code == 404 or current_weather_response.status_code == 404:
            flash('City not found. Please enter a valid city name', 'error') # Handle city not found error
        else:
            flash('Error fetching weather data. Please try again', 'error') # Handle other errors
        return render_template('index.html')


    def index(self):
        """
        Handle the root URL of the application.
        """
        if request.method == 'POST':
            city = request.form['city'] # Get the city name from the form input
            if city:
                return self.get_weather(city) # Fetch and display weather for the entered city
            else:
                flash('Please enter a city.', 'error') # Handle empty city input
        return render_template('index.html')

    def run(self):
        """
        Run the Flask app.
        """
        self.app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1 # Disable caching for static files
        self.app.run() # Start the Flask development server

# Initialize and run the WeatherApp
weather_app = WeatherApp()

if __name__ == '__main__':
    weather_app.run()
