import os
import json
from groq import Groq
from app.calendar_service import get_free_dates
from app.duffel_service import search_flights, search_stays

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def run_travel_agent(prompt: str, origin: str, dest: str, lat: float, lng: float, search_start: str, search_end: str):
    # 1. Fetch free days from Google Calendar
    free_days = get_free_dates(search_start, search_end)
    if not free_days:
        return "No free days found in your Google Calendar for this range."
    
    departure_date = free_days[0]
    
    # 2. Query Duffel API for flights and accommodations
    flights_data = search_flights(origin, dest, departure_date)
    stays_data = search_stays(lat, lng, departure_date, search_end)
    
    # 3. Truncate payload string lengths safely for the LLM context limit
    flights_str = json.dumps(flights_data)[:3000]
    stays_str = json.dumps(stays_data)[:3000]
    
    # 4. Reason through options using Groq and gpt-oss-120b
    system_prompt = (
        "You are an expert AI travel concierge. Analyze the JSON flight and hotel search "
        "results against the user's specific travel prompt and constraints. Recommend the best flight "
        "and stay combination and clearly explain your rationale."
    )
    
    user_context = f"""
    User Preferences: {prompt}
    Target Departure Date: {departure_date}
    Available Flights Payload: {flights_str}
    Available Stays Payload: {stays_str}
    """
    
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_context}
        ],
        temperature=0.2
    )
    
    return response.choices[0].message.content