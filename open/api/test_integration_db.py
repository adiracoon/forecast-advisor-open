from fastapi.testclient import TestClient
from sqlmodel import Session, select
import importlib, os, types
def reload_with_db(db_url: str):
    os.environ["DATABASE_URL"] = db_url
    import open.api.main as m
    return importlib.reload(m)
def test_forecast_logs_row(tmp_path, monkeypatch):
    dbp = tmp_path / "itest.db"
    m = reload_with_db(f"sqlite:///{dbp}")
    c = TestClient(m.app)
    r = c.post("/api/forecast", json={"city":"Haifa","date":"2025-09-10"})
    assert r.status_code == 200
    j = r.json()
    assert j["city"] == "Haifa"
    assert "temp_c" in j and "summary" in j
    with Session(m.engine) as ses:
        rows = list(ses.exec(select(m.ForecastQuery)))
        assert len(rows) == 1
        row = rows[0]
        assert row.city == "Haifa"
        assert isinstance(row.temp_c, (int,float))
