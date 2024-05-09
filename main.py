from flask import Flask, render_template, request, flash
import time
from datetime import datetime, timezone,timedelta
import requests,pprint
import os

from os import path
if path.exists('env.py'):
    import env


class WeatherApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.api_key = os.environ.get('API_KEY')
        self.app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')
        self.app.route('/', methods=['GET','POST'])(self.home)

    def calculate_local_time(self, timestamp, timezone_offset):
        utc_time = datetime.utcfromtimestamp(timestamp)
        timezone_offset_seconds = timezone_offset
        local_time = utc_time + timedelta(seconds=timezone_offset_seconds)

        return local_time.strftime('%H:%M')

    def extract_only_time_from_dt_string(self, datetime_string):
        #Parse the datetime string to a datetime object
        dt_object = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S')
        #Extract only the time excluding the date
        only_time = dt_object.strftime('%H:%M')
        return only_time


    def get_weather(self, city):
        url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={self.api_key}&units=metric&cnt=5'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            forecasts = []

            for forecast in data['list']:
                # local_time = self.calculate_local_time(time.time(),data['city']['timezone'])
                local_time = self.calculate_local_time(forecast['dt'], data['city']['timezone'])
                sun_rise = self.calculate_local_time(data['city']['sunrise'],data['city']['timezone'])
                sun_set = self.calculate_local_time(data['city']['sunset'],data['city']['timezone'])
                # data_time = self.calculate_local_time(data['city']['dt'])
                every_3_hours = self.extract_only_time_from_dt_string(forecast['dt_txt'])

                weather = {
                    "temperature": int(forecast['main']['temp']),
                    'icon': forecast['weather'][0]['icon'],
                    "description": forecast['weather'][0]['description'],
                    'humidity': forecast['main']['humidity'],
                    'wind': int(forecast['wind']['speed']),
                    'country': data['city']['country'],
                    'feels_like': int(forecast['main']['feels_like']),
                    # 'data_time': int(forecast['dt']),
                    'sun_rise': sun_rise,
                    'sun_set' : sun_set,
                    'timezone': local_time,
                    'hours': every_3_hours
                }
                forecasts.append(weather)

            return render_template('home.html', forecasts=forecasts, city=city)
        elif response.status_code == 404:
            flash('City not found. Please enter a valid city name', 'error')
        else:
            flash('Error fetching weather data. Please try again', 'error')
        return render_template('home.html')

    def home(self):
        if request.method == 'POST':
            city = request.form['city']

            if city:
                return self.get_weather(city)
            else:
                flash('Please enter a city.', 'error')
        return render_template('home.html')

    def run(self):
        self.app.run(debug=True)
        self.app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1

if __name__ == '__main__':
    weather_app = WeatherApp()
    weather_app.run()
