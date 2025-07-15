from django.contrib.auth.models import AbstractUser
from django.db import models
import json

class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to="profiles/", null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    mother_tongue = models.CharField(max_length=50, default='en')
    learning_language = models.CharField(max_length=50, blank=True)
    religion = models.CharField(max_length=50, blank=True)
    caution_level = models.CharField(max_length=10, choices=[
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')
    ], default='medium')
    theme = models.CharField(max_length=10, choices=[
        ('light', 'Light'), ('dark', 'Dark')
    ], default='dark')
    language_ui = models.CharField(max_length=10, default='en')
    is_synced = models.BooleanField(default=False)
    
    def get_taboos(self):
        return getattr(self, '_taboos', [])
    
    def set_taboos(self, value):
        self._taboos = value

class UserSettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    ai_enabled = models.BooleanField(default=True)
    tts_enabled = models.BooleanField(default=True)
    voice_choice = models.CharField(max_length=20, choices=[
        ('male', 'Male'), ('female', 'Female'), ('neutral', 'Neutral')
    ], default='neutral')
    offline_mode = models.BooleanField(default=False)
    notifications_enabled = models.BooleanField(default=True)
    cache_cleared_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Settings for {self.user.username}"