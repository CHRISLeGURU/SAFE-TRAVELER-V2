import speech_recognition as sr
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

def transcribe_audio(audio_file):
    """Transcribe audio file to text using Google Speech Recognition"""
    
    recognizer = sr.Recognizer()
    
    try:
        # Convert Django file to BytesIO
        audio_data = audio_file.read()
        audio_io = io.BytesIO(audio_data)
        
        # Use speech_recognition with the audio data
        with sr.AudioFile(audio_io) as source:
            audio = recognizer.record(source)
            
        # Recognize speech
        text = recognizer.recognize_google(audio)
        
        # Detect language (simplified - in production use proper language detection)
        language = detect_language(text)
        
        return {
            'text': text,
            'language': language,
            'confidence': 0.9  # Mock confidence score
        }
        
    except sr.UnknownValueError:
        return {
            'text': '',
            'language': 'unknown',
            'confidence': 0.0,
            'error': 'Could not understand audio'
        }
    except sr.RequestError as e:
        return {
            'text': '',
            'language': 'unknown', 
            'confidence': 0.0,
            'error': f'Recognition service error: {e}'
        }
    except Exception as e:
        return {
            'text': '',
            'language': 'unknown',
            'confidence': 0.0,
            'error': f'Audio processing error: {e}'
        }

def detect_language(text):
    """Simple language detection based on text patterns"""
    
    # Simple heuristics for common languages
    if any(word in text.lower() for word in ['the', 'and', 'is', 'are', 'to', 'from']):
        return 'en'
    elif any(word in text.lower() for word in ['le', 'la', 'de', 'et', 'est', 'que']):
        return 'fr'
    elif any(word in text.lower() for word in ['el', 'la', 'de', 'y', 'es', 'que']):
        return 'es'
    elif any(word in text.lower() for word in ['na', 'ya', 'ni', 'wa', 'kwa']):
        return 'sw'  # Swahili
    else:
        return 'unknown'

def process_audio_stream(audio_stream):
    """Process real-time audio stream"""
    
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)
            
        text = recognizer.recognize_google(audio)
        language = detect_language(text)
        
        return {
            'text': text,
            'language': language,
            'confidence': 0.9
        }
        
    except Exception as e:
        return {
            'text': '',
            'language': 'unknown',
            'confidence': 0.0,
            'error': str(e)
        }