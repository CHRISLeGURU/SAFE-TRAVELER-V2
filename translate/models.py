from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TranslationHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source_language = models.CharField(max_length=20)
    target_language = models.CharField(max_length=20)
    original_text = models.TextField()
    translated_text = models.TextField()
    context = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.source_language} -> {self.target_language}: {self.original_text[:50]}"

class VoiceChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=100, unique=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Chat session {self.session_id} - {self.user.username}"

class VoiceChatMessage(models.Model):
    session = models.ForeignKey(VoiceChatSession, on_delete=models.CASCADE)
    message_type = models.CharField(max_length=10, choices=[
        ('user', 'User'),
        ('ai', 'AI')
    ])
    text_content = models.TextField()
    audio_file = models.FileField(upload_to='chat_audio/', null=True, blank=True)
    language_detected = models.CharField(max_length=20, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.message_type}: {self.text_content[:50]}"