from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import json

User = get_user_model()

class Travel(models.Model):
    TRAVEL_TYPES = [
        ('business', 'Business'),
        ('scientific', 'Scientific'),
        ('vacation', 'Vacation'),
        ('pilgrimage', 'Pilgrimage'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    travel_type = models.CharField(max_length=20, choices=TRAVEL_TYPES)
    start_date = models.DateField(default=timezone.now)
    residence = models.CharField(max_length=200, blank=True)
    objectives = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    advice_data = models.JSONField(null=True, blank=True)
    is_synced = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.city}, {self.country}"
    
    def days_elapsed(self):
        return (timezone.now().date() - self.start_date).days
    
    def get_advice(self):
        if self.advice_data:
            return self.advice_data
        return {'do': [], 'dont': [], 'bonus': ''}

class QuickDestination(models.Model):
    CATEGORIES = [
        ('market', 'Market'),
        ('hotel', 'Hotel'),
        ('restaurant', 'Restaurant'),
        ('religious', 'Religious Place'),
        ('cultural', 'Cultural Site'),
        ('hospital', 'Hospital'),
        ('transport', 'Transport'),
    ]
    
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    visited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.category})"

class TravelAdvice(models.Model):
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE)
    advice_type = models.CharField(max_length=20, choices=[
        ('do', 'Do'), ('dont', 'Don\'t'), ('bonus', 'Bonus Tip')
    ])
    content = models.TextField()
    priority = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['priority', '-created_at']
    
    def __str__(self):
        return f"{self.advice_type}: {self.content[:50]}"

class WeatherSnapshot(models.Model):
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.FloatField(null=True, blank=True)
    uv_index = models.FloatField(null=True, blank=True)
    description = models.CharField(max_length=100)
    advice = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Weather for {self.travel.name} - {self.temperature}°C"