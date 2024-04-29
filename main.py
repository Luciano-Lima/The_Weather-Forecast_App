from flask import Flask, render_template, request, flash
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



    def get_weather(self, city):
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            pprint.pprint(data)
            weather = {
                "temperature": data['main']['temp'],
                "icon": data['weather'][0]['icon'],
                "description": data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind': data['wind']['speed'],
                'country': data['sys']['country']
            }
            return render_template('home.html', weather=weather, city=city)
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
