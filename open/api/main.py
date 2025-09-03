from typing import List
from fastapi import FastAPI, HTTPException, Query
from math import radians, sin, cos, asin, sqrt
from open.adapters.geocoding import geocode_city
from open.adapters.weather import daily_weather

_db = []
app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/weather")
async def weather(city: str, start: str = Query(...), end: str = Query(...)):
    loc = await geocode_city(city)
    if not loc:
        raise HTTPException(404, detail="city not found")
    wx = await daily_weather(loc["lat"], loc["lon"], start, end)
    return {"city": loc, "weather": wx}

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    c = 2*asin(sqrt(a))
    return R*c

@app.get("/search")
async def search(origin: str, dest: str, start: str, end: str):
    o = await geocode_city(origin)
    d = await geocode_city(dest)
    if not o or not d:
        raise HTTPException(404, detail="origin or dest not found")
    wx = await daily_weather(d["lat"], d["lon"], start, end)
    dist_km = haversine_km(o["lat"], o["lon"], d["lat"], d["lon"])
    flight_hours = round(dist_km / 800.0 + 0.5, 2)
    return {
        "origin": o,
        "dest": d,
        "distance_km": round(dist_km, 1),
        "estimated_flight_hours": flight_hours,
        "weather": wx,
        "cost_of_living_index": None,
        "hotel_price_band": None,
        "attractions": [],
        "season_photos": [],
    }
@app.get("/ping")
async def ping():
    return {"pong": True}
@app.get("/")
async def root():
    return {"name": "forecast-advisor-open", "status": "ok"}

from .models import Forecast

@app.post("/forecasts", response_model=Forecast, status_code=201)
async def create_forecast(f: Forecast):
    f.id = len(_db) + 1
    _db.append(f)
    return f

@app.get("/forecasts", response_model=list[Forecast])
async def list_forecasts():
    return _db

@app.get("/forecasts/{fid}", response_model=Forecast)
async def get_forecast(fid: int):
    for f in _db:
        if f.id == fid:
            return f
    raise HTTPException(status_code=404, detail="not found")
