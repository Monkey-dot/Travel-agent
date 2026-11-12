import json
import requests
from langchain_core.tools import tool

with open('flights.json', 'r') as f:
    flights_data = json.load(f)
with open('hotels.json', 'r') as f:
    hotels_data = json.load(f)
with open('places.json', 'r') as f:
    places_data = json.load(f)

@tool
def search_flights(source_city: str, destination_city: str) -> dict:
    """Search for the cheapest flight between two cities."""
    available_flights = [
        f for f in flights_data 
        if f['from'].lower() == source_city.lower() and f['to'].lower() == destination_city.lower()
    ]
    if not available_flights:
        return {"error": f"No flights found."}
    return sorted(available_flights, key=lambda x: x['price'])[0]

@tool
def search_hotels(city: str, min_stars: int = 3) -> list:
    """Find top hotel recommendations in a city based on star rating."""
    available_hotels = [
        h for h in hotels_data 
        if h['city'].lower() == city.lower() and h['stars'] >= min_stars
    ]
    if not available_hotels:
        return [{"error": "No hotels found."}]
    return sorted(available_hotels, key=lambda x: x['price_per_night'])[:2]

@tool
def search_places(city: str) -> list:
    """Discover top-rated tourist attractions in the destination city."""
    city_places = [
        p for p in places_data 
        if p['city'].lower() == city.lower()
    ]
    return sorted(city_places, key=lambda x: x['rating'], reverse=True)[:3]

@tool
def get_weather(latitude: float, longitude: float) -> str:
    """Get the 3-day weather forecast for a location using Open-Meteo API."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max&timezone=auto"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temps = data['daily']['temperature_2m_max'][:3]
        return " | ".join([f"Day {i+1}: {temps[i]}°C" for i in range(len(temps))])
    return "Weather data unavailable."

@tool
def estimate_budget(flight_cost: float, hotel_nightly_rate: float, days: int, daily_local_expenses: float = 2500) -> dict:
    """Calculate the estimated total trip budget in INR."""
    total_hotel = hotel_nightly_rate * days
    total_local = daily_local_expenses * days
    return {
        "Flight Cost": f"₹{flight_cost}",
        "Hotel Cost": f"₹{total_hotel}",
        "Food & Travel (Local)": f"₹{total_local}",
        "Estimated Total Budget": f"₹{flight_cost + total_hotel + total_local}"
    }

travel_tools = [search_flights, search_hotels, search_places, get_weather, estimate_budget]
