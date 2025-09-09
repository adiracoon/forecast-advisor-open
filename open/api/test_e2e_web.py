from fastapi.testclient import TestClient
from open.api.main import app

client = TestClient(app)

def test_app_serves_index():
    r = client.get("/app/")
    assert r.status_code == 200
