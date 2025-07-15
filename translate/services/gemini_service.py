import os
import json
import google.generativeai as genai
from django.conf import settings

# Configure Gemini
genai.configure(api_key=settings.GOOGLE_API_KEY)

def get_translation_with_context(text, source_lang, target_lang, context="general"):
    """Get translation with cultural context from Gemini"""
    
    prompt = f"""
    A traveler heard this phrase: "{text}"
    Source language: {source_lang}
    Target language: {target_lang}
    Context: {context}
    
    Please provide a JSON response with:
    {{
        "translation": "Accurate translation",
        "cultural_context": "Brief cultural explanation if relevant",
        "response_suggestion": "Suggested polite response",
        "pronunciation_tip": "How to pronounce the response (phonetic)"
    }}
    
    Make the response helpful for a traveler.
    """
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        response_text = response.text.strip()
        print(f"Raw Gemini response: {response_text}")  # Added debug log
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        return json.loads(response_text)
        
    except Exception as e:
        print(f"Translation error: {e}")
        return {
            "translation": f"Translation: {text}",
            "cultural_context": "Context not available",
            "response_suggestion": "Thank you",
            "pronunciation_tip": "Pronunciation guide not available"
        }

def chat_with_ai(message, context="general"):
    """Chat with Gemini AI for travel assistance"""
    
    prompt = f"""
    You are a helpful travel assistant. A traveler is asking: "{message}"
    Context: {context}
    
    Provide a helpful, friendly response focused on travel assistance. 
    Include practical advice, cultural tips, or language help as appropriate.
    Keep responses concise but informative.
    """
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        print(f"Chat error: {e}")
        return "I'm sorry, I'm having trouble responding right now. Please try again."

def get_language_help(phrase, target_language):
    """Get help with learning phrases in target language"""
    
    prompt = f"""
    A traveler wants to learn how to say "{phrase}" in {target_language}.
    
    Please provide:
    1. The translation
    2. Phonetic pronunciation
    3. When/how to use it appropriately
    4. Any cultural notes
    
    Format as a helpful explanation.
    """
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        return f"I can help you learn {target_language} phrases. Please try again."