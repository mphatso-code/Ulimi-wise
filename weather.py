import os
import requests
import json
import logging
from datetime import datetime
from translations import get_translation

# OpenWeatherMap API key
WEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")

def get_weather_for_location(location):
    """
    Get current weather data for a location
    
    Args:
        location (str): Location name or coordinates
    
    Returns:
        dict: Weather data including temperature, conditions, etc.
    """
    if not WEATHER_API_KEY:
        logging.warning("OpenWeatherMap API key is not set")
        return get_mock_weather_data(location)
    
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': location,
        'appid': WEATHER_API_KEY,
        'units': 'metric'  # Use metric units
    }
    
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            
            # Format the response data
            weather_data = {
                'location': location,
                'temperature': {
                    'current': round(data['main']['temp']),
                    'feels_like': round(data['main']['feels_like']),
                    'min': round(data['main']['temp_min']),
                    'max': round(data['main']['temp_max'])
                },
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind': {
                    'speed': data['wind']['speed'],
                    'direction': data['wind'].get('deg', 0)
                },
                'conditions': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return weather_data
        else:
            logging.error(f"Error fetching weather data: {response.status_code} - {response.text}")
            return get_mock_weather_data(location)
    
    except Exception as e:
        logging.error(f"Exception when fetching weather data: {str(e)}")
        return get_mock_weather_data(location)


def get_weather_forecast(location, days=5):
    """
    Get weather forecast for a location
    
    Args:
        location (str): Location name or coordinates
        days (int): Number of days for forecast (max 5 for free API)
    
    Returns:
        dict: Forecast data for specified number of days
    """
    if not WEATHER_API_KEY:
        logging.warning("OpenWeatherMap API key is not set")
        return {'forecast': [get_mock_weather_data(location) for _ in range(days)]}
    
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': location,
        'appid': WEATHER_API_KEY,
        'units': 'metric',
        'cnt': days * 8  # 8 readings per day (every 3 hours)
    }
    
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            
            # Process and simplify the forecast data
            daily_forecasts = {}
            for item in data['list']:
                date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                
                if date not in daily_forecasts:
                    daily_forecasts[date] = {
                        'date': date,
                        'temperature': {
                            'min': float('inf'),
                            'max': float('-inf'),
                            'avg': 0
                        },
                        'conditions': [],
                        'precipitation': 0,
                        'readings': 0
                    }
                
                forecast = daily_forecasts[date]
                forecast['temperature']['min'] = min(forecast['temperature']['min'], item['main']['temp_min'])
                forecast['temperature']['max'] = max(forecast['temperature']['max'], item['main']['temp_max'])
                forecast['temperature']['avg'] += item['main']['temp']
                forecast['conditions'].append(item['weather'][0]['main'])
                forecast['precipitation'] += item.get('rain', {}).get('3h', 0) + item.get('snow', {}).get('3h', 0)
                forecast['readings'] += 1
            
            # Calculate averages and determine main condition
            for date, forecast in daily_forecasts.items():
                forecast['temperature']['avg'] /= forecast['readings']
                
                # Find most common condition
                condition_counts = {}
                for condition in forecast['conditions']:
                    condition_counts[condition] = condition_counts.get(condition, 0) + 1
                forecast['main_condition'] = max(condition_counts.items(), key=lambda x: x[1])[0]
                
                # Clean up
                del forecast['readings']
                del forecast['conditions']
            
            return {
                'location': location,
                'forecast': list(daily_forecasts.values())
            }
        else:
            logging.error(f"Error fetching forecast data: {response.status_code} - {response.text}")
            return {'forecast': [get_mock_weather_data(location) for _ in range(days)]}
    
    except Exception as e:
        logging.error(f"Exception when fetching forecast data: {str(e)}")
        return {'forecast': [get_mock_weather_data(location) for _ in range(days)]}


def get_weather_recommendations(weather_data, farm_type=None, lang='en'):
    """
    Generate farming recommendations based on weather data
    
    Args:
        weather_data (dict): Weather data from get_weather_for_location
        farm_type (str): Type of farming (crops, livestock, etc.)
        lang (str): Language code for translation
    
    Returns:
        list: Recommendations based on weather conditions
    """
    recommendations = []
    
    if not weather_data:
        return [get_translation("Weather data is not available. Please check your location settings.", lang)]
    
    # Temperature-based recommendations
    temp = weather_data.get('temperature', {}).get('current', 20)
    if temp < 5:
        recommendations.append(get_translation("Low temperature alert! Protect sensitive crops from frost. Consider using row covers or heating in greenhouses.", lang))
    elif temp > 32:
        recommendations.append(get_translation("High temperature alert! Ensure adequate irrigation and consider providing shade for sensitive crops and livestock.", lang))
    
    # Humidity-based recommendations
    humidity = weather_data.get('humidity', 50)
    if humidity > 80:
        recommendations.append(get_translation("High humidity alert! Monitor for fungal diseases. Ensure good air circulation around plants and dry livestock bedding.", lang))
    elif humidity < 30:
        recommendations.append(get_translation("Low humidity alert! Increase irrigation frequency. Watch for water stress in crops.", lang))
    
    # Wind-based recommendations
    wind_speed = weather_data.get('wind', {}).get('speed', 0)
    if wind_speed > 8:
        recommendations.append(get_translation("Strong winds expected! Secure greenhouse structures and provide windbreaks for tender crops. Ensure livestock have shelter.", lang))
    
    # Weather condition-based recommendations
    conditions = weather_data.get('conditions', '').lower()
    
    if 'rain' in conditions or 'drizzle' in conditions:
        recommendations.append(get_translation("Rainy conditions expected. Avoid spraying pesticides or fertilizers that could wash away. Check drainage systems.", lang))
    
    elif 'thunderstorm' in conditions:
        recommendations.append(get_translation("Thunderstorms expected! Ensure livestock have access to shelter. Secure farm equipment and structures.", lang))
    
    elif 'snow' in conditions:
        recommendations.append(get_translation("Snowy conditions expected. Ensure winter crops are properly protected and livestock have warm, dry shelter and adequate feed.", lang))
    
    elif 'clear' in conditions:
        recommendations.append(get_translation("Clear weather is ideal for field operations such as planting, harvesting, or applying treatments if temperature is suitable.", lang))
    
    elif 'clouds' in conditions:
        recommendations.append(get_translation("Cloudy conditions are good for transplanting seedlings to minimize transplant shock.", lang))
    
    # Farm type specific recommendations
    if farm_type:
        farm_type = farm_type.lower()
        
        if 'crop' in farm_type or 'plant' in farm_type:
            if temp > 25 and humidity < 40:
                recommendations.append(get_translation("High evapotranspiration conditions. Increase irrigation for crops to prevent water stress.", lang))
            
            if 'rain' in conditions and humidity > 70:
                recommendations.append(get_translation("Wet conditions increase disease risk. Monitor crops for signs of fungal diseases like powdery mildew or blight.", lang))
        
        elif any(animal in farm_type for animal in ['livestock', 'cattle', 'poultry', 'pig', 'sheep', 'goat']):
            if temp > 30:
                recommendations.append(get_translation("Heat stress risk for livestock. Ensure adequate shade, ventilation, and fresh water. Consider misting systems for cooling.", lang))
            
            if temp < 0:
                recommendations.append(get_translation("Freezing temperatures can affect livestock. Ensure water sources don't freeze and provide extra feed for energy.", lang))
    
    # If no specific recommendations, provide general advice
    if not recommendations:
        recommendations.append(get_translation("Current weather conditions are generally favorable for farming activities. Continue with regular farm management practices.", lang))
    
    return recommendations


def get_mock_weather_data(location):
    """
    Generate mock weather data when API is unavailable
    
    Args:
        location (str): Location name
    
    Returns:
        dict: Mock weather data
    """
    return {
        'location': location,
        'temperature': {
            'current': 22,
            'feels_like': 23,
            'min': 18,
            'max': 25
        },
        'humidity': 65,
        'pressure': 1012,
        'wind': {
            'speed': 4.5,
            'direction': 180
        },
        'conditions': 'Clear',
        'description': 'clear sky',
        'icon': '01d',
        'sunrise': '06:00',
        'sunset': '18:00',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
