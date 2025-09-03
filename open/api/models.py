from typing import Optional
from sqlmodel import SQLModel, Field

class Forecast(SQLModel, table=True):
    __tablename__ = "forecasts"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    value: float
