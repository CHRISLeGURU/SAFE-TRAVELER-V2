import requests
import os
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def generate_speech(text, language='en', voice_id=None):
    """Generate speech using ElevenLabs API"""
    
    if not settings.ELEVENLABS_API_KEY:
        return None
    
    # Default voice IDs for different languages
    voice_mapping = {
        'en': 'EXAVITQu4vr4xnSDxMaL',  # Bella
        'fr': 'XrExE9yKIg1WjnnlVkGX',  # Matilda  
        'es': 'MF3mGyEYCl7XYWbV9V6O',  # Elli
    }
    
    if not voice_id:
        voice_id = voice_mapping.get(language, voice_mapping['en'])
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": settings.ELEVENLABS_API_KEY
    }
    
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            # Save audio file
            audio_content = ContentFile(response.content)
            filename = f"tts_{hash(text)}.mp3"
            file_path = default_storage.save(f"audio/{filename}", audio_content)
            return default_storage.url(file_path)
        else:
            print(f"TTS API error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"TTS error: {e}")
        return None

def get_available_voices():
    """Get list of available voices from ElevenLabs"""
    
    if not settings.ELEVENLABS_API_KEY:
        return []
    
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {"xi-api-key": settings.ELEVENLABS_API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('voices', [])
    except Exception as e:
        print(f"Error fetching voices: {e}")
    
    return []