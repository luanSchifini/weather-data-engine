from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.weather_response import WeatherResponse
from app.services.weather_orchestrator_service import WeatherOrchestratorService

router = APIRouter()


@router.post("/collect/{city_name}", response_model=WeatherResponse, status_code=status.HTTP_201_CREATED)
def collect_weather_data(city_name: str, db: Session = Depends(get_db)):
    """
    Activate the weather data collection pipeline:
    1. Geocoding (Name -> Lat/Lon)
    2. Weather API (Actual Weather)
    3. Persistence (PostgreSQL)
    """
    weather_service = WeatherOrchestratorService(db)
    return weather_service.process_new_collection(city_name)


@router.get("/history", response_model=List[WeatherResponse])
def get_weather_history(limit: int = 20, db: Session = Depends(get_db)):
    """
    Returns the history of the last collections made to the database.
    """
    weather_service = WeatherOrchestratorService(db)
    return weather_service.get_history(limit=limit)
