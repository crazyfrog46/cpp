# my_app/weather_icons.py

def get_icon_code(description):
    """Returns the weather icon code based on the weather description."""
    icon_mapping = {
        'clear sky': 'day-sunny',
        'few clouds': 'cloudy',
        'scattered clouds': 'cloudy',
        'broken clouds': 'cloudy',
        'light rain': 'rain',
        'moderate rain': 'rain',
        'heavy rain': 'rain',
        'very heavy rain': 'rain',
        'extreme rain': 'rain',
        'shower rain': 'rain',
        'light intensity drizzle': 'rain',
        'drizzle': 'rain',
        'light snow': 'snow',
        'snow': 'snow',
        'heavy snow': 'snow',
        'sleet': 'snow',
        'fog': 'fog',
        'mist': 'fog',
        'haze': 'fog',
        'smoke': 'fog',
        'dust': 'fog',
        'ash': 'fog',
        'sand': 'fog',
        'thunderstorm': 'thunderstorm',
        'tornado': 'tornado',
        'clear': 'day-sunny',  # Generic clear weather
        'partly cloudy': 'cloudy',
        'overcast': 'cloudy',
        'rain and snow': 'rain-snow',
    }

    description = description.lower()
    return icon_mapping.get(description, 'cloudy')  # Default to cloudy if description is unknown

def get_bg_color(description):
    """Returns the background color for a given weather description."""
    color_mapping = {
        'clear sky': '#87CEEB',  # Sky Blue for clear skies
        'few clouds': '#B0E0E6',  # Powder Blue for few clouds
        'scattered clouds': '#B0E0E6',
        'broken clouds': '#A9A9A9',  # Dark Gray for overcast
        'light rain': '#00BFFF',  # Deep Sky Blue for light rain
        'moderate rain': '#1E90FF',  # Dodger Blue for moderate rain
        'heavy rain': '#4682B4',  # Steel Blue for heavy rain
        'shower rain': '#4682B4',
        'snow': '#ADD8E6',  # Light Blue for snow
        'light snow': '#ADD8E6',
        'fog': '#C0C0C0',  # Silver for fog
        'mist': '#C0C0C0',
        'haze': '#D3D3D3',  # Light Gray for haze
        'thunderstorm': '#FF6347',  # Tomato for thunderstorms
        'tornado': '#FF4500',  # Orange Red for tornado
        'partly cloudy': '#D3D3D3',  # Light Gray for partly cloudy
        'overcast': '#A9A9A9',  # Dark Gray for overcast
    }

    description = description.lower()
    return color_mapping.get(description, '#F0F8FF')  # Light Alice Blue if description is unknown
