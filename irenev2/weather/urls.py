from django.urls import path
from .views import home, save_location, delete_location

urlpatterns = [
    path('', home, name='home'),
    path('save_location/', save_location, name='save_location'),
    path('delete_location/<int:city_id>/', delete_location, name='delete_location'),
]
