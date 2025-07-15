from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Travel, QuickDestination, TravelAdvice
from .forms import TravelForm
from .services.gemini_service import generate_travel_advice
from .services.weather_service import get_weather_data

@login_required
def travel_list(request):
    travels = Travel.objects.filter(user=request.user)
    active_travel = travels.filter(is_active=True).first()
    
    context = {
        'travels': travels,
        'active_travel': active_travel,
        'total_travels': travels.count(),
    }
    return render(request, 'travels/travel_list.html', context)

@login_required
def travel_new(request):
    if request.method == 'POST':
        form = TravelForm(request.POST)
        if form.is_valid():
            travel = form.save(commit=False)
            travel.user = request.user
            
            # Set as active if it's the first travel or user chooses to
            if not Travel.objects.filter(user=request.user, is_active=True).exists():
                travel.is_active = True
            
            travel.save()
            
            # Generate AI advice in background
            try:
                advice = generate_travel_advice(
                    travel.city, 
                    travel.country, 
                    travel.travel_type
                )
                travel.advice_data = advice
                travel.save()
            except Exception as e:
                print(f"Error generating advice: {e}")
            
            messages.success(request, f'Travel "{travel.name}" created successfully!')
            return redirect('travel_detail', travel_id=travel.id)
    else:
        form = TravelForm()
    
    return render(request, 'travels/travel_form.html', {'form': form})

@login_required
def travel_detail(request, travel_id):
    travel = get_object_or_404(Travel, id=travel_id, user=request.user)
    destinations = QuickDestination.objects.filter(travel=travel)
    
    # Get weather data
    weather_data = get_weather_data(travel.city, travel.country)
    
    context = {
        'travel': travel,
        'destinations': destinations,
        'weather_data': weather_data,
        'destinations_count': destinations.count(),
        'days_elapsed': travel.days_elapsed(),
    }
    return render(request, 'travels/travel_detail.html', context)

@csrf_exempt
@login_required
def set_active_travel(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        travel_id = data.get('travel_id')
        
        # Deactivate all travels
        Travel.objects.filter(user=request.user).update(is_active=False)
        
        # Activate selected travel
        travel = get_object_or_404(Travel, id=travel_id, user=request.user)
        travel.is_active = True
        travel.save()
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@csrf_exempt
@login_required
def refresh_advice(request, travel_id):
    if request.method == 'POST':
        travel = get_object_or_404(Travel, id=travel_id, user=request.user)
        
        try:
            advice = generate_travel_advice(
                travel.city, 
                travel.country, 
                travel.travel_type
            )
            travel.advice_data = advice
            travel.save()
            
            return JsonResponse({
                'status': 'success',
                'advice': advice
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({'status': 'error'})