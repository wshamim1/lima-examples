"""
Weather Tools using LangChain
Provides weather information for cities using LangChain's tool decorator
"""
from langchain.tools import tool
import random

@tool
def get_weather(city: str) -> str:
    """
    Get current weather information for a city.
    
    Args:
        city: The name of the city to get weather for
        
    Returns:
        Current weather information including temperature and conditions
    """
    # Mock weather data - in production, this would call a real weather API
    conditions = ["sunny", "partly cloudy", "cloudy", "rainy", "clear"]
    temperatures = list(range(60, 85))
    
    condition = random.choice(conditions)
    temp = random.choice(temperatures)
    
    return f"The weather in {city} is {condition} with a temperature of {temp}°F"

@tool
def get_forecast(city: str, days: int = 3) -> str:
    """
    Get weather forecast for a city.
    
    Args:
        city: The name of the city to get forecast for
        days: Number of days to forecast (default: 3, max: 7)
        
    Returns:
        Weather forecast information
    """
    if days > 7:
        days = 7
    
    conditions = ["sunny", "partly cloudy", "cloudy", "rainy"]
    forecast_data = []
    
    for day in range(1, days + 1):
        condition = random.choice(conditions)
        temp_high = random.randint(70, 85)
        temp_low = random.randint(55, 65)
        forecast_data.append(f"Day {day}: {condition}, High: {temp_high}°F, Low: {temp_low}°F")
    
    return f"{days}-day forecast for {city}:\n" + "\n".join(forecast_data)

