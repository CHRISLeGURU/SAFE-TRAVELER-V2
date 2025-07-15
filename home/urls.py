from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('weather/', views.get_weather_update, name='get_weather_update'),
    path('destinations/', views.get_quick_destinations, name='get_quick_destinations'),
]