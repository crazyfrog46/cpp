from django.shortcuts import render, redirect
from .weather_service import get_weather_data
from .models import WeatherData, SavedLocation
from django.db.models import Q

def get_icon_code(description):
    """Returns the weather icon code based on the weather description."""
    icon_mapping = {
        'clear sky': 'day-sunny',
        'few clouds': 'cloudy',
        'scattered clouds': 'cloudy',
        'broken clouds': 'cloudy',
        'shower rain': 'rain',
        'rain': 'rain',
        'thunderstorm': 'thunderstorm',
        'snow': 'snow',
        'mist': 'fog',
    }
    description = description.lower()
    return icon_mapping.get(description, 'cloudy')  # Default to cloudy if description is unknown

def get_background_color(description):
    """Returns a background color based on the weather description."""
    background_mapping = {
        'clear sky': '#87CEEB',  # Light blue for clear skies
        'few clouds': '#B3E5FC',  # Light blue for few clouds
        'scattered clouds': '#B0BEC5',  # Gray for scattered clouds
        'broken clouds': '#90A4AE',  # Darker gray for broken clouds
        'shower rain': '#76D7C4',  # Light rain color
        'rain': '#2980B9',  # Blue for rain
        'thunderstorm': '#9B59B6',  # Purple for thunderstorm
        'snow': '#D5DBDB',  # Light gray for snow
        'mist': '#BDC3C7',  # Gray for mist
    }
    description = description.lower()
    return background_mapping.get(description, '#AED6F1')  # Default light blue if description is unknown

def home(request):
    city = ''  # Default to empty for initial load
    weather = None  # Initially no weather data
    
    # Check if form is submitted
    if request.method == 'POST':
        city = request.POST.get('city', '').strip()  # Get the city from form input
        if city:  # If a city is entered
            weather_data = get_weather_data(city)
            if weather_data:
                # Get the icon code and background color
                icon_code = get_icon_code(weather_data['description'])
                bg_color = get_background_color(weather_data['description'])
                
                # Delete any existing weather data for the city to ensure only one record per city
                WeatherData.objects.filter(city=city).delete()
                
                # Create a new weather data entry
                weather = WeatherData.objects.create(
                    city=city,
                    temperature=weather_data['temperature'],
                    description=weather_data['description'],
                    humidity=weather_data['humidity'],
                    wind_speed=weather_data['wind_speed'],
                    icon_code=icon_code,
                    bg_color=bg_color,
                )

    # Get the saved locations to display
    saved_locations = SavedLocation.objects.all()

    return render(request, 'weather/home.html', {
        'weather': weather,
        'city': city,
        'saved_locations': saved_locations,
    })

def save_location(request):
    if request.method == "POST":
        city_name = request.POST.get("city_name")
        if city_name and not SavedLocation.objects.filter(city_name=city_name).exists():
            # Only save if the city is not already saved
            SavedLocation.objects.create(city_name=city_name)
    return redirect("home")  # Redirect to home after saving

def delete_location(request, city_id):
    try:
        location = SavedLocation.objects.get(id=city_id)
        location.delete()
    except SavedLocation.DoesNotExist:
        pass
    return redirect("home")  # Redirect to home after deleting
