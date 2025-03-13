import requests
from django.conf import settings

def get_openweather_data(city):
    current_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={settings.OPENWEATHER_API_KEY}&units=metric'
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={settings.OPENWEATHER_API_KEY}&units=metric'
    
    try:
        current_response = requests.get(current_url)
        forecast_response = requests.get(forecast_url)
        current_data = current_response.json()
        forecast_data = forecast_response.json()

        if current_data.get('cod') != 200 or forecast_data.get('cod') != '200':
            return None

        hourly_data = forecast_data['list'][:8]  # 8 data points for 24 hours (3-hour intervals)
        temperatures = [hour['main']['temp'] for hour in hourly_data]

        return {
            'temperature': current_data['main']['temp'],
            'description': current_data['weather'][0]['description'],
            'humidity': current_data['main']['humidity'],
            'wind_speed': current_data['wind']['speed'],
            'icon_code': current_data['weather'][0]['icon'],
            'hourly_temperatures': temperatures
        }
    except requests.RequestException:
        return None

def get_weatherapi_data(city):
    url = f'http://api.weatherapi.com/v1/current.json?key={settings.WEATHERAPI_API_KEY}&q={city}'
    try:
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
    except requests.RequestException:
        return None

def get_tomorrowio_data(city):
    url = f'https://api.tomorrow.io/v4/timelines?location={city}&fields=temperature,humidity,windSpeed&apikey={settings.TOMORROWIO_API_KEY}'
    try:
        response = requests.get(url)
        data = response.json()
        if 'data' not in data or 'timelines' not in data['data']:
            return None
        return {
            'temperature': data['data']['timelines'][0]['intervals'][0]['values']['temperature'],
            'description': 'N/A',
            'humidity': data['data']['timelines'][0]['intervals'][0]['values']['humidity'],
            'wind_speed': data['data']['timelines'][0]['intervals'][0]['values']['windSpeed']
        }
    except requests.RequestException:
        return None

def get_weather_data(city):
    data_openweather = get_openweather_data(city)
    data_weatherapi = get_weatherapi_data(city)
    data_tomorrowio = get_tomorrowio_data(city)

    data_openweather = data_openweather or {}
    data_weatherapi = data_weatherapi or {}
    data_tomorrowio = data_tomorrowio or {}

    if not (data_openweather or data_weatherapi or data_tomorrowio):
        return None

    temperature_values = [data.get('temperature') for data in [data_openweather, data_weatherapi, data_tomorrowio] if data.get('temperature') is not None]
    humidity_values = [data.get('humidity') for data in [data_openweather, data_weatherapi, data_tomorrowio] if data.get('humidity') is not None]
    wind_speed_values = [data.get('wind_speed') for data in [data_openweather, data_weatherapi, data_tomorrowio] if data.get('wind_speed') is not None]

    temperature = sum(temperature_values) / len(temperature_values) if temperature_values else 0
    humidity = sum(humidity_values) / len(humidity_values) if humidity_values else 0
    wind_speed = sum(wind_speed_values) / len(wind_speed_values) if wind_speed_values else 0

    description = data_openweather.get('description') or data_weatherapi.get('description') or data_tomorrowio.get('description') or 'N/A'
    icon_code = data_openweather.get('icon_code', '01d')

    return {
        'temperature': round(temperature, 2),
        'description': description,
        'humidity': round(humidity, 2),
        'wind_speed': round(wind_speed, 2),
        'icon_code': icon_code
    }
