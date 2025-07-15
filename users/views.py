from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from .models import CustomUser, UserSettings
from .forms import CustomUserCreationForm, ProfileForm, SettingsForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserSettings.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    
    # Get current travel if any
    current_travel = None
    if hasattr(request.user, 'travel_set'):
        current_travel = request.user.travel_set.filter(is_active=True).first()
    
    context = {
        'form': form,
        'current_travel': current_travel,
    }
    return render(request, 'users/profile.html', context)

@login_required
def settings_view(request):
    settings, created = UserSettings.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            
            # Handle theme change
            if 'theme' in request.POST:
                request.user.theme = request.POST['theme']
                request.user.save()
            
            # Handle language change
            if 'language_ui' in request.POST:
                request.user.language_ui = request.POST['language_ui']
                request.user.save()
            
            messages.success(request, 'Settings updated successfully!')
            return redirect('settings')
    else:
        form = SettingsForm(instance=settings)
    
    context = {
        'form': form,
        'settings': settings,
    }
    return render(request, 'users/settings.html', context)

@csrf_exempt
@login_required
def toggle_theme(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        theme = data.get('theme')
        if theme in ['light', 'dark']:
            request.user.theme = theme
            request.user.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@csrf_exempt
@login_required
def clear_cache(request):
    if request.method == 'POST':
        settings, created = UserSettings.objects.get_or_create(user=request.user)
        settings.cache_cleared_at = timezone.now()
        settings.save()
        return JsonResponse({'status': 'success', 'message': 'Cache cleared successfully!'})
    return JsonResponse({'status': 'error'})

@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(request, username=request.user.username, password=password)
        if user:
            user.delete()
            messages.success(request, 'Account deleted successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid password.')
    return render(request, 'users/delete_account.html')