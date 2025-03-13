from django.db import models
from django.utils import timezone

class WeatherData(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    description = models.CharField(max_length=255)
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    # New fields for icon and background color
    icon_code = models.CharField(max_length=100, blank=True, null=True)
    bg_color = models.CharField(max_length=7, blank=True, null=True)  # Color in hex (e.g., #87CEEB)

    def __str__(self):
        return self.city

class SavedLocation(models.Model):
    city_name = models.CharField(max_length=100, unique=True)  # Ensure no duplicates
    created_at = models.DateTimeField(auto_now_add=True)  # Removed the default argument
    temperature = models.FloatField(null=True, blank=True)  # Store temperature
    description = models.CharField(max_length=255, null=True, blank=True)  # Store weather description
    humidity = models.FloatField(null=True, blank=True)  # Store humidity
    wind_speed = models.FloatField(null=True, blank=True)  # Store wind speed
    icon_code = models.CharField(max_length=100, null=True, blank=True)  # Store weather icon code
    bg_color = models.CharField(max_length=7, null=True, blank=True)  # Store background color

    def __str__(self):
        return self.city_name
