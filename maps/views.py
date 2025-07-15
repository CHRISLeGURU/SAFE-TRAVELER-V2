from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from .models import SearchHistory, SavedPlace

@login_required
def map_view(request):
    recent_searches = SearchHistory.objects.filter(user=request.user)[:5]
    saved_places = SavedPlace.objects.filter(user=request.user)
    
    context = {
        'recent_searches': recent_searches,
        'saved_places': saved_places,
    }
    return render(request, 'maps/map.html', context)

@csrf_exempt
@login_required
def search_places(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('query')
        lat = data.get('lat')
        lng = data.get('lng')
        
        # Save search history
        SearchHistory.objects.create(
            user=request.user,
            query=query,
            latitude=lat,
            longitude=lng
        )
        
        # Here you would integrate with a real places API
        # For now, return mock data
        places = [
            {
                'name': f"Restaurant near {query}",
                'address': "123 Main Street",
                'lat': lat + 0.001,
                'lng': lng + 0.001,
                'category': 'restaurant',
                'rating': 4.5
            },
            {
                'name': f"Hotel near {query}",
                'address': "456 Hotel Avenue",
                'lat': lat - 0.001,
                'lng': lng - 0.001,
                'category': 'hotel',
                'rating': 4.2
            }
        ]
        
        return JsonResponse({
            'status': 'success',
            'places': places
        })
    
    return JsonResponse({'status': 'error'})

@csrf_exempt
@login_required
def save_place(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        place = SavedPlace.objects.create(
            user=request.user,
            name=data.get('name'),
            address=data.get('address', ''),
            latitude=data.get('lat'),
            longitude=data.get('lng'),
            category=data.get('category', ''),
            notes=data.get('notes', '')
        )
        
        return JsonResponse({
            'status': 'success',
            'place_id': place.id
        })
    
    return JsonResponse({'status': 'error'})

@csrf_exempt
@login_required
def get_directions(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        start_lat = data.get('start_lat')
        start_lng = data.get('start_lng')
        end_lat = data.get('end_lat')
        end_lng = data.get('end_lng')
        
        # Mock directions response
        # In production, integrate with Google Directions API or similar
        directions = {
            'distance': '2.3 km',
            'duration': '8 minutes',
            'steps': [
                'Head north on Main Street',
                'Turn right on Broadway',
                'Continue for 1.5 km',
                'Destination will be on your left'
            ]
        }
        
        return JsonResponse({
            'status': 'success',
            'directions': directions
        })
    
    return JsonResponse({'status': 'error'})