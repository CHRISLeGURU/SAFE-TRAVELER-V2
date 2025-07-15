from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('clear-cache/', views.clear_cache, name='clear_cache'),
    path('delete-account/', views.delete_account, name='delete_account'),
]