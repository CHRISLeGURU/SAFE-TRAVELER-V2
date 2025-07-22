from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from travels.models import Travel
from translate.models import TranslationHistory
from maps.models import SearchHistory
from travels.services.weather_service import get_weather_data
from travels.services.gemini_service import generate_travel_advice

def home_view(request):
    if request.user.is_authenticated:
        return authenticated_home(request)
    else:
        return render(request, 'home/home_guest.html')

@login_required
def authenticated_home(request):
    # Get user's active travel
    active_travel = Travel.objects.filter(user=request.user, is_active=True).first()
    
    # Get user statistics
    total_travels = Travel.objects.filter(user=request.user).count()
    total_translations = TranslationHistory.objects.filter(user=request.user).count()
    total_searches = SearchHistory.objects.filter(user=request.user).count()
    
    # Get weather data for current location
    weather_data = None
    if active_travel:
        weather_data = get_weather_data(active_travel.city, active_travel.country)
    
    # Get recent travels
    recent_travels = Travel.objects.filter(user=request.user)[:3]
    
    # Get quick advice for active travel
    quick_advice = []
    if active_travel and active_travel.advice_data:
        advice_data = active_travel.advice_data
        if isinstance(advice_data, dict):
            quick_advice = advice_data.get('do', [])[:3]  # Show top 3 tips
    
    context = {
        'active_travel': active_travel,
        'total_travels': total_travels,
        'total_translations': total_translations,
        'total_searches': total_searches,
        'weather_data': weather_data,
        'recent_travels': recent_travels,
        'quick_advice': quick_advice,
    }
    return render(request, 'home/home.html', context)

@csrf_exempt
@login_required
def get_weather_update(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        city = data.get('city')
        country = data.get('country')
        
        weather_data = get_weather_data(city, country)
        
        return JsonResponse({
            'status': 'success',
            'weather': weather_data
        })
    
    return JsonResponse({'status': 'error'})

@csrf_exempt
@login_required
def get_quick_destinations(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        category = data.get('category')
        lat = data.get('lat', 0)
        lng = data.get('lng', 0)
        
        # Mock destinations based on category
        destinations = {
            'market': [
                {'name': 'Central Market', 'distance': '0.5 km', 'rating': 4.2},
                {'name': 'Local Bazaar', 'distance': '1.2 km', 'rating': 4.0},
            ],
            'hotel': [
                {'name': 'Grand Hotel', 'distance': '0.8 km', 'rating': 4.5},
                {'name': 'Budget Inn', 'distance': '1.5 km', 'rating': 3.8},
            ],
            'restaurant': [
                {'name': 'Local Cuisine', 'distance': '0.3 km', 'rating': 4.7},
                {'name': 'Street Food Court', 'distance': '0.7 km', 'rating': 4.3},
            ],
            'religious': [
                {'name': 'Main Mosque', 'distance': '1.0 km', 'rating': 4.8},
                {'name': 'Cathedral', 'distance': '1.8 km', 'rating': 4.6},
            ],
            'cultural': [
                {'name': 'Museum of History', 'distance': '2.0 km', 'rating': 4.4},
                {'name': 'Art Gallery', 'distance': '1.5 km', 'rating': 4.1},
            ]
        }
        
        return JsonResponse({
            'status': 'success',
            'destinations': destinations.get(category, [])
        })
    
    return JsonResponse({'status': 'error'})
