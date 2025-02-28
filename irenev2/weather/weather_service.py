import requests
from django.conf import settings
from datetime import datetime

def get_openweather_data(city):
    # Current weather API
    current_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.OPENWEATHER_API_KEY}&units=metric'
    current_response = requests.get(current_url)
    current_data = current_response.json()

    # 5-day/3-hour forecast API
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={settings.OPENWEATHER_API_KEY}&units=metric'
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()

    if current_data.get('cod') != 200 or forecast_data.get('cod') != '200':
        return None

    # Extract hourly temperatures for the next 24 hours from the forecast
    hourly_data = forecast_data['list'][:8]  # 8 data points for 24 hours (3-hour intervals)
    temperatures = [hour['main']['temp'] for hour in hourly_data]

    return {
        'temperature': current_data['main']['temp'],
        'description': current_data['weather'][0]['description'],
        'humidity': current_data['main']['humidity'],
        'wind_speed': current_data['wind']['speed'],
        'hourly_temperatures': temperatures
    }

def get_weatherapi_data(city):
    url = f'http://api.weatherapi.com/v1/current.json?key={settings.WEATHERAPI_API_KEY}&q={city}'
    response = requests.get(url)
    data = response.json()
    if 'error' in data:
        return None
    return {
        'temperature': data['current']['temp_c'],
        'description': data['current']['condition']['text'],
        'humidity': data['current']['humidity'],
        'wind_speed': data['current']['wind_kph']
    }

def get_tomorrowio_data(city):
    url = f'https://api.tomorrow.io/v4/timelines?location={city}&fields=temperature,humidity,windSpeed&apikey={settings.TOMORROWIO_API_KEY}'
    response = requests.get(url)
    data = response.json()
    if data.get('error'):
        return None
    return {
        'temperature': data['data']['timelines'][0]['intervals'][0]['values']['temperature'],
        'description': 'N/A',
        'humidity': data['data']['timelines'][0]['intervals'][0]['values']['humidity'],
        'wind_speed': data['data']['timelines'][0]['intervals'][0]['values']['windSpeed']
    }

def get_weather_data(city):
    data_openweather = get_openweather_data(city)
    data_weatherapi = get_weatherapi_data(city)
    data_tomorrowio = get_tomorrowio_data(city)

    if not data_openweather and not data_weatherapi and not data_tomorrowio:
        return None

    temperature = sum(filter(None, [data_openweather.get('temperature', 0), data_weatherapi.get('temperature', 0), data_tomorrowio.get('temperature', 0)])) / 3
    humidity = sum(filter(None, [data_openweather.get('humidity', 0), data_weatherapi.get('humidity', 0), data_tomorrowio.get('humidity', 0)])) / 3
    wind_speed = sum(filter(None, [data_openweather.get('wind_speed', 0), data_weatherapi.get('wind_speed', 0), data_tomorrowio.get('wind_speed', 0)])) / 3
    description = data_openweather.get('description', data_weatherapi.get('description', data_tomorrowio.get('description', 'N/A')))

    return {
        'temperature': round(temperature, 2),
        'description': description,
        'humidity': round(humidity, 2),
        'wind_speed': round(wind_speed, 2),
    }
