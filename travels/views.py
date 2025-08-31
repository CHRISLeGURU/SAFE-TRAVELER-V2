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

@login_required
def travel_edit(request, travel_id):
    travel = get_object_or_404(Travel, id=travel_id, user=request.user)
    
    if request.method == 'POST':
        form = TravelForm(request.POST, instance=travel)
        if form.is_valid():
            updated_travel = form.save()
            
            # Regenerate advice if destination changed
            if form.has_changed() and any(field in form.changed_data for field in ['city', 'country', 'travel_type']):
                try:
                    advice = generate_travel_advice(
                        updated_travel.city, 
                        updated_travel.country, 
                        updated_travel.travel_type
                    )
                    updated_travel.advice_data = advice
                    updated_travel.save()
                except Exception as e:
                    print(f"Error regenerating advice: {e}")
            
            messages.success(request, f'Travel "{updated_travel.name}" updated successfully!')
            return redirect('travel_detail', travel_id=updated_travel.id)
    else:
        form = TravelForm(instance=travel)
    
    context = {
        'form': form,
        'travel': travel,
        'is_editing': True,
    }
    return render(request, 'travels/travel_form.html', context)

@login_required
def travel_delete(request, travel_id):
    travel = get_object_or_404(Travel, id=travel_id, user=request.user)
    
    if request.method == 'POST':
        travel_name = travel.name
        was_active = travel.is_active
        
        # If deleting active travel, suggest another one
        next_travel = None
        if was_active:
            next_travel = Travel.objects.filter(
                user=request.user
            ).exclude(id=travel_id).first()
            
            if next_travel:
                next_travel.is_active = True
                next_travel.save()
        
        travel.delete()
        
        if was_active and next_travel:
            messages.success(
                request, 
                f'Travel "{travel_name}" deleted. "{next_travel.name}" is now your active travel.'
            )
        else:
            messages.success(request, f'Travel "{travel_name}" deleted successfully.')
        
        return redirect('travel_list')
    
    # Count related objects for confirmation
    destinations_count = travel.quickdestination_set.count()
    advice_count = travel.traveladvice_set.count()
    
    context = {
        'travel': travel,
        'destinations_count': destinations_count,
        'advice_count': advice_count,
    }
    return render(request, 'travels/travel_delete.html', context)

@login_required
def travel_edit(request, travel_id):
    travel = get_object_or_404(Travel, id=travel_id, user=request.user)
    
    if request.method == 'POST':
        form = TravelForm(request.POST, instance=travel)
        if form.is_valid():
            updated_travel = form.save()
            
            # Regenerate AI advice if destination changed
            if form.has_changed() and any(field in form.changed_data for field in ['city', 'country', 'travel_type']):
                try:
                    advice = generate_travel_advice(
                        updated_travel.city, 
                        updated_travel.country, 
                        updated_travel.travel_type
                    )
                    updated_travel.advice_data = advice
                    updated_travel.save()
                except Exception as e:
                    print(f"Error regenerating advice: {e}")
            
            messages.success(request, f'Travel "{updated_travel.name}" updated successfully!')
            return redirect('travel_detail', travel_id=updated_travel.id)
    else:
        form = TravelForm(instance=travel)
    
    context = {
        'form': form,
        'travel': travel,
        'is_edit': True,
    }
    return render(request, 'travels/travel_form.html', context)

@login_required
def travel_delete(request, travel_id):
    travel = get_object_or_404(Travel, id=travel_id, user=request.user)
    
    if request.method == 'POST':
        travel_name = travel.name
        was_active = travel.is_active
        
        # Delete the travel (cascade will handle related objects)
        travel.delete()
        
        # If deleted travel was active, suggest activating another one
        if was_active:
            next_travel = Travel.objects.filter(user=request.user).first()
            if next_travel:
                next_travel.is_active = True
                next_travel.save()
                messages.info(request, f'"{next_travel.name}" is now your active travel.')
        
        messages.success(request, f'Travel "{travel_name}" deleted successfully!')
        return redirect('travel_list')
    
    context = {
        'travel': travel,
    }
    return render(request, 'travels/travel_delete.html', context)

@login_required
def travel_edit(request, travel_id):
    travel = get_object_or_404(Travel, id=travel_id, user=request.user)
    
    if request.method == 'POST':
        form = TravelForm(request.POST, instance=travel)
        if form.is_valid():
            updated_travel = form.save()
            
            # Regenerate advice if destination changed
            if form.has_changed() and any(field in form.changed_data for field in ['city', 'country', 'travel_type']):
                try:
                    advice = generate_travel_advice(
                        updated_travel.city, 
                        updated_travel.country, 
                        updated_travel.travel_type
                    )
                    updated_travel.advice_data = advice
                    updated_travel.save()
                except Exception as e:
                    print(f"Error regenerating advice: {e}")
            
            messages.success(request, f'Travel "{updated_travel.name}" updated successfully!')
            return redirect('travel_detail', travel_id=updated_travel.id)
    else:
        form = TravelForm(instance=travel)
    
    context = {
        'form': form,
        'travel': travel,
        'is_editing': True,
    }
    return render(request, 'travels/travel_form.html', context)

@login_required
def travel_delete(request, travel_id):
    travel = get_object_or_404(Travel, id=travel_id, user=request.user)
    
    if request.method == 'POST':
        travel_name = travel.name
        was_active = travel.is_active
        
        # If deleting active travel, suggest another one to activate
        next_travel = None
        if was_active:
            next_travel = Travel.objects.filter(
                user=request.user
            ).exclude(id=travel_id).first()
        
        # Delete the travel (cascade will handle related objects)
        travel.delete()
        
        # Activate next travel if the deleted one was active
        if was_active and next_travel:
            next_travel.is_active = True
            next_travel.save()
            messages.success(
                request, 
                f'Travel "{travel_name}" deleted. "{next_travel.name}" is now your active travel.'
            )
        else:
            messages.success(request, f'Travel "{travel_name}" deleted successfully.')
        
        return redirect('travel_list')
    
    # For GET request, show confirmation page
    context = {
        'travel': travel,
        'related_count': {
            'destinations': travel.quickdestination_set.count(),
            'advice': travel.traveladvice_set.count(),
            'weather': travel.weathersnapshot_set.count(),
        }
    }
    return render(request, 'travels/travel_delete.html', context)