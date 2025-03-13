from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .weather_service import get_weather_data
from .models import WeatherData, SavedLocation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import SavedLocation
import requests

def get_icon_code(description):
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
    return icon_mapping.get(description.lower(), 'cloudy')

def get_background_color(description):
    background_mapping = {
        'clear sky': '#87CEEB',  # Light blue
        'few clouds': '#B3E5FC',  # Light blue
        'scattered clouds': '#B0BEC5',  # Gray
        'broken clouds': '#90A4AE',  # Darker gray
        'shower rain': '#76D7C4',  # Light rain
        'rain': '#2980B9',  # Blue
        'thunderstorm': '#9B59B6',  # Purple
        'snow': '#D5DBDB',  # Light gray
        'mist': '#BDC3C7',  # Gray
    }
    return background_mapping.get(description.lower(), '#AED6F1')  # Default light blue

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Home view
@login_required
def home(request):
    city = ''
    weather = None

    if request.method == 'POST':
        city = request.POST.get('city', '').strip()
        if city:
            weather_data = get_weather_data(city)
            if weather_data:
                
                icon_code = weather_data['icon_code']
                bg_color = get_background_color(weather_data['description'])
                WeatherData.objects.filter(city=city).delete()
                weather = WeatherData.objects.create(
                    city=city,
                    temperature=weather_data['temperature'],
                    description=weather_data['description'],
                    humidity=weather_data['humidity'],
                    wind_speed=weather_data['wind_speed'],
                    icon_code=icon_code,
                    bg_color=bg_color,
                )

    saved_locations = SavedLocation.objects.all()
    has_saved_locations = saved_locations.exists()  # Check if any saved locations exist

    return render(request, 'weather/home.html', {
        'weather': weather,
        'city': city,
        'saved_locations': saved_locations,
        'has_saved_locations': has_saved_locations,  # Pass this to the template
    })

# Save location
@login_required
def save_location(request):
    if request.method == "POST":
        city_name = request.POST.get("city_name").strip()

        if city_name and not SavedLocation.objects.filter(city_name=city_name).exists():
            SavedLocation.objects.create(city_name=city_name)
            messages.success(request, f"{city_name} has been saved!")
        else:
            messages.warning(request, f"{city_name} is already saved!")

    return redirect("home")

# Delete location
@login_required
def delete_location(request, city_id):
    try:
        location = SavedLocation.objects.get(id=city_id)
        location.delete()
        messages.success(request, "Location deleted successfully!")
    except SavedLocation.DoesNotExist:
        messages.error(request, "Location not found!")

    return redirect("saved_locations")



def get_current_weather(city_name):
    weather_data = get_weather_data(city_name)
    if weather_data:
        return {
            'description': weather_data['description'],
            'temperature': weather_data['temperature'],
            'humidity': weather_data['humidity'],
            'wind_speed': weather_data['wind_speed'],
        }
    else:
        return None

@login_required
def saved_locations(request):
    locations = SavedLocation.objects.all()
    for location in locations:
        weather_data = get_current_weather(location.city_name)
        if weather_data:
            location.current_weather = weather_data['description']
            location.current_temperature = weather_data['temperature']
    return render(request, 'weather/saved_locations.html', {'locations': locations})

# Edit location
@login_required
def edit_location(request, city_id):
    try:
        location = SavedLocation.objects.get(id=city_id)
    except SavedLocation.DoesNotExist:
        messages.error(request, "Location not found!")
        return redirect("saved_locations")

    if request.method == "POST":
        new_city_name = request.POST.get("city_name").strip()
        if new_city_name and new_city_name != location.city_name:
            # Check if the new city name already exists in the saved locations
            if not SavedLocation.objects.filter(city_name=new_city_name).exists():
                location.city_name = new_city_name
                location.save()
                messages.success(request, f"Location updated to {new_city_name}!")
            else:
                messages.warning(request, f"{new_city_name} is already saved!")
        else:
            messages.warning(request, "Please enter a valid city name.")

        return redirect("saved_locations")

    return render(request, "weather/edit_location.html", {"location": location})