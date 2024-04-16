from flask import Flask,render_template, request
import requests
import os

from os import path
if path.exists('env.py'):
    import env

class WeatherApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.api_key = os.environ.get('API_KEY')
        self.app.route('/', methods=['GET', 'POST'])(self.get_weather)


    def get_weather(self):
        return render_template('home.html')

    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    weather_app = WeatherApp()
    weather_app.run()