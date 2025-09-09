from fastapi.testclient import TestClient
from open.api.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_ping():
    r = client.get("/ping")
    assert r.status_code == 200
    assert r.json() == {"pong": True}
def test_root():
    r = client.get("/")
    assert r.status_code == 200
    j = r.json()
    assert j.get("status") == "ok"
    assert j.get("name") == "forecast-advisor-open"
