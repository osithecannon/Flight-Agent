import os
import requests

DUFFEL_TOKEN = os.getenv("DUFFEL_ACCESS_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {DUFFEL_TOKEN}",
    "Duffel-Version": "v2",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def search_flights(origin: str, destination: str, departure_date: str):
    url = "https://api.duffel.com/air/offer_requests"
    payload = {
        "data": {
            "slices": [{"origin": origin, "destination": destination, "departure_date": departure_date}],
            "passengers": [{"type": "adult"}],
            "cabin_class": "economy"
        }
    }
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

def search_stays(lat: float, lng: float, check_in: str, check_out: str):
    url = "https://api.duffel.com/stays/search"
    payload = {
        "data": {
            "location": {
                "geographic_coordinates": {"latitude": lat, "longitude": lng, "radius": 10}
            },
            "check_in_date": check_in,
            "check_out_date": check_out,
            "rooms": [{"adults": 1}]
        }
    }
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()