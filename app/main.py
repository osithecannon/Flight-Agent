from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import run_travel_agent

app = FastAPI(title="Groq-Powered Flight & Stay Agent")

class TravelRequest(BaseModel):
    prompt: str
    origin: str          # e.g., "LOS" or "JFK"
    destination: str     # e.g., "LHR"
    lat: float           # Destination latitude (e.g., 51.5074)
    lng: float           # Destination longitude (e.g., -0.1278)
    search_start: str    # "YYYY-MM-DD"
    search_end: str      # "YYYY-MM-DD"

@app.post("/plan")
def plan_trip(req: TravelRequest):
    result = run_travel_agent(
        req.prompt, req.origin, req.destination, 
        req.lat, req.lng, req.search_start, req.search_end
    )
    return {"recommendation": result}