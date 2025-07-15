from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class WeatherCache(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.FloatField()
    description = models.CharField(max_length=100)
    uv_index = models.FloatField(default=0)
    cached_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['city', 'country']
    
    def __str__(self):
        return f"{self.city}, {self.country} - {self.temperature}°C"

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"