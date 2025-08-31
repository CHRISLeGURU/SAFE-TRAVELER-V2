from django.urls import path
from . import views

urlpatterns = [
    path('', views.travel_list, name='travel_list'),
    path('new/', views.travel_new, name='travel_new'),
    path('<int:travel_id>/', views.travel_detail, name='travel_detail'),
    path('<int:travel_id>/edit/', views.travel_edit, name='travel_edit'),
    path('<int:travel_id>/delete/', views.travel_delete, name='travel_delete'),
    path('set-active/', views.set_active_travel, name='set_active_travel'),
    path('<int:travel_id>/refresh-advice/', views.refresh_advice, name='refresh_advice'),
]