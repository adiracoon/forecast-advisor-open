import pytest
from fastapi.testclient import TestClient
from open.api.main import app

client = TestClient(app)

START = "2025-09-10"
END   = "2025-09-12"

def _skip_if_bad(resp):
    if resp.status_code != 200:
        pytest.skip(f"external API unavailable or rate-limited (status {resp.status_code})")

def test_weather_basic():
    r = client.get(f"/weather?city=Barcelona&start={START}&end={END}")
    _skip_if_bad(r)
    data = r.json()
    assert "city" in data and "weather" in data
    daily = data["weather"].get("daily")
    assert isinstance(daily, dict)
    for k in ["time","temperature_2m_max","temperature_2m_min","precipitation_probability_mean"]:
        assert k in daily

def test_search_basic():
    r = client.get(f"/search?origin=TLV&dest=Barcelona&start={START}&end={END}")
    _skip_if_bad(r)
    data = r.json()
    for k in ["origin","dest","distance_km","estimated_flight_hours","weather"]:
        assert k in data
    assert isinstance(data["distance_km"], (int,float))
    assert isinstance(data["estimated_flight_hours"], (int,float))
