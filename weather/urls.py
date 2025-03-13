from django.urls import path
from .views import home, save_location, delete_location, login_view, saved_locations, edit_location

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('saved_locations/', saved_locations, name='saved_locations'),
    path('save_location/', save_location, name='save_location'),
    path('delete_location/<int:city_id>/', delete_location, name='delete_location'),
    path('edit_location/<int:city_id>/', edit_location, name='edit_location'),  # Add edit URL pattern
]
