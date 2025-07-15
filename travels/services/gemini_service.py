import os
import json
import google.generativeai as genai
from django.conf import settings

# Configure Gemini
genai.configure(api_key=settings.GOOGLE_API_KEY)

def generate_travel_advice(city, country, travel_type):
    """Generate travel advice using Gemini AI"""
    
    prompt = f"""
    You are a cultural travel expert. A traveler is planning a {travel_type} trip to {city}, {country}.
    
    Please provide specific, practical advice in the following format (respond in valid JSON):
    
    {{
        "do": [
            "Specific thing they should do",
            "Another specific recommendation",
            "Cultural practice to follow"
        ],
        "dont": [
            "Specific thing to avoid",
            "Cultural taboo to respect", 
            "Behavior that might offend"
        ],
        "bonus": "One valuable insider tip specific to this location and trip type"
    }}
    
    Make sure all advice is:
    - Specific to {city}, {country}
    - Culturally sensitive and accurate
    - Practical and actionable
    - Appropriate for a {travel_type} trip
    """
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        # Clean the response text to extract JSON
        response_text = response.text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        advice_data = json.loads(response_text)
        return advice_data
        
    except Exception as e:
        print(f"Error generating advice: {e}")
        # Return default advice structure
        return {
            "do": [
                "Research local customs and traditions",
                "Learn basic greetings in the local language",
                "Respect local dress codes and cultural norms"
            ],
            "dont": [
                "Assume your cultural norms apply everywhere",
                "Take photos without permission",
                "Ignore local laws and regulations"
            ],
            "bonus": f"For {travel_type} trips to {city}, consider connecting with local professionals or communities."
        }

def get_translation_advice(text, source_lang, target_lang, context="general"):
    """Get translation and cultural context from Gemini"""
    
    prompt = f"""
    A traveler heard this phrase in {source_lang}: "{text}"
    They speak {target_lang}.
    Context: {context}
    
    Please provide a JSON response with:
    {{
        "translation": "Accurate translation in {target_lang}",
        "cultural_context": "Brief explanation of cultural meaning or context",
        "response_suggestion": "Suggested polite response in {target_lang}",
        "pronunciation_tip": "How to pronounce the response"
    }}
    """
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        response_text = response.text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        return json.loads(response_text)
        
    except Exception as e:
        return {
            "translation": "Translation not available",
            "cultural_context": "Context not available",
            "response_suggestion": "Thank you",
            "pronunciation_tip": "Pronunciation guide not available"
        }