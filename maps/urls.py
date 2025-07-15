from django.urls import path
from . import views

urlpatterns = [
    path('', views.map_view, name='map'),
    path('search/', views.search_places, name='search_places'),
    path('save/', views.save_place, name='save_place'),
    path('directions/', views.get_directions, name='get_directions'),
]