import os
os.environ.setdefault("DATABASE_URL","sqlite:///./ci.db")
from typing import List, Optional
import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel, Session, select, create_engine
from .models import Forecast

app = FastAPI()
app.mount("/app", StaticFiles(directory="open/web", html=True), name="app")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@db:5432/postgres"
)
engine = create_engine(os.getenv("DATABASE_URL","sqlite:///./ci.db"))

def get_session():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/forecasts", response_model=Forecast, status_code=201)
async def create_forecast(f: Forecast, session: Session = Depends(get_session)):
    session.add(f)
    session.commit()
    session.refresh(f)
    return f

@app.get("/forecasts", response_model=List[Forecast])
async def list_forecasts(session: Session = Depends(get_session)):
    return session.exec(select(Forecast)).all()

@app.get("/forecasts/{fid}", response_model=Forecast)
async def get_forecast(fid: int, session: Session = Depends(get_session)):
    f = session.get(Forecast, fid)
    if not f:
        raise HTTPException(status_code=404, detail="not found")
    return f
