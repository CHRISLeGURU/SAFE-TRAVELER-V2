import requests
from django.conf import settings

def get_weather_data(city, country):
    """Get weather data from OpenWeatherMap"""
    
    if not settings.OPENWEATHER_API_KEY:
        return {
            'temperature': 25,
            'humidity': 60,
            'description': 'Clear sky',
            'uv_index': 5,
            'advice': 'Weather data not available'
        }
    
    try:
        # Current weather
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': f"{city},{country}",
            'appid': settings.OPENWEATHER_API_KEY,
            'units': 'metric'
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            
            # Generate weather advice
            advice = generate_weather_advice(temp, humidity, description)
            
            return {
                'temperature': temp,
                'humidity': humidity,
                'description': description.title(),
                'uv_index': 5,  # Default value
                'advice': advice
            }
    
    except Exception as e:
        print(f"Weather API error: {e}")
    
    # Default weather data
    return {
        'temperature': 25,
        'humidity': 60,
        'description': 'Pleasant weather',
        'uv_index': 5,
        'advice': 'Perfect weather for exploring!'
    }

def generate_weather_advice(temperature, humidity, description):
    """Generate weather-based advice"""
    advice = []
    
    if temperature > 30:
        advice.append("Stay hydrated and wear light clothing")
        advice.append("Seek shade during peak hours (11 AM - 3 PM)")
    elif temperature < 10:
        advice.append("Dress warmly in layers")
        advice.append("Protect exposed skin from cold")
    
    if humidity > 80:
        advice.append("High humidity - expect to feel warmer")
    
    if 'rain' in description.lower():
        advice.append("Bring an umbrella or raincoat")
    elif 'sun' in description.lower():
        advice.append("Don't forget sunscreen and sunglasses")
    
    if not advice:
        advice.append("Perfect weather for exploring!")
    
    return " • ".join(advice)