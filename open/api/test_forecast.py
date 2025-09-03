from fastapi.testclient import TestClient
from open.api.main import app, engine
from sqlmodel import SQLModel, Session, select
from open.api.models import Forecast

client = TestClient(app)

def reset_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

def test_forecast_crud_db():
    reset_db()
    r = client.post("/forecasts", json={"title": "t", "value": 1.23})
    assert r.status_code == 201
    fid = r.json()["id"]
    r = client.get("/forecasts")
    assert r.status_code == 200 and len(r.json()) == 1
    r = client.get(f"/forecasts/{fid}")
    assert r.status_code == 200 and r.json()["title"] == "t"
