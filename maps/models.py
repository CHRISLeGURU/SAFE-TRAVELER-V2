from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=200)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    place_name = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.query}"

class SavedPlace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    category = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"