from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('weather.urls')),  # Include URLs from your weather app
    path('accounts/', include('django.contrib.auth.urls')),  # Include the Django auth URLs for login, logout, etc.
]
