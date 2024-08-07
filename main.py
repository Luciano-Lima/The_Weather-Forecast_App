from flask import Flask, render_template, request, flash
import time
from datetime import datetime, timezone, timedelta
import requests, pprint
import os

from os import path
if path.exists('env.py'):
    import env
from collections import defaultdict

class WeatherApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.api_key = os.environ.get('API_KEY')
        self.app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')
        # self.app.route('/', methods=['GET', 'POST'])(self.index)
        self.app.add_url_rule('/', 'index', self.index, methods=['GET', 'POST'])

    def calculate_local_time(self, timestamp, timezone_offset):
        utc_time = datetime.utcfromtimestamp(timestamp)
        local_time = utc_time + timedelta(seconds=timezone_offset)

        return local_time.strftime('%Y-%m-%d %H:%M')

    # def extract_only_time_from_dt_string(self, datetime_string):
    #     dt_object = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S')
    #     only_time = dt_object.strftime('%H:%M')
    #     print('ONLY time', only_time)
    #     return only_time

    def group_forecasts_by_day(self, forecasts, timezone_offset):
        forecasts_by_day = defaultdict(list)

        for forecast in forecasts:
            local_time = self.calculate_local_time(forecast['dt'], timezone_offset)
            date, time = local_time.split(' ')
            day_of_week = datetime.strptime(date, '%Y-%m-%d').strftime('%A')[0:3]

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
            forecasts_by_day[day_of_week].append(weather)

        return dict(forecasts_by_day)

    def get_weather(self, city):
        url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={self.api_key}&units=metric'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            forecasts_by_day = self.group_forecasts_by_day(data['list'], data['city']['timezone'])

            return render_template('index.html', forecasts_by_day=forecasts_by_day, city=city)
        elif response.status_code == 404:
            flash('City not found. Please enter a valid city name', 'error')
        else:
            flash('Error fetching weather data. Please try again', 'error')
        return render_template('index.html')


    def index(self):
        if request.method == 'POST':
            city = request.form['city']

            if city:
                return self.get_weather(city)
            else:
                flash('Please enter a city.', 'error')
        return render_template('index.html')

    def run(self):
        self.app.run(debug=True)
        self.app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1

if __name__ == '__main__':
    weather_app = WeatherApp()
    weather_app.run()
