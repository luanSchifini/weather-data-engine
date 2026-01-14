from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import logger
from app.schemas.weather_response import WeatherResponse
from app.schemas.weather_request import WeatherRequest
from app.repositories.weather_repository import WeatherRepository
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
def get_weather_history(city: str = None, limit: int = 20, db: Session = Depends(get_db)):
    """
    Returns the history of the last collections made to the database.
    """
    weather_service = WeatherOrchestratorService(db)
    return weather_service.get_history(city=city, limit=limit)


@router.delete("/{weather_id}", response_model=WeatherResponse)
def delete_weather_record(weather_id: UUID, db: Session = Depends(get_db)):
    """
    Delete a weather record.
    """
    repository = WeatherRepository(db)
    weather_record = repository.delete(weather_id)
    if not weather_record:
        logger.error(f"DeleteWeatherRecordEndpoint: Weather record not found for id: {weather_id}")
        raise HTTPException(status_code=404, detail="Weather record not found")

    return weather_record


@router.get("/{weather_id}", response_model=WeatherResponse)
def get_weather_record(weather_id: UUID, db: Session = Depends(get_db)):
    """
    Get a specific weather record by ID.
    """
    repository = WeatherRepository(db)
    weather_record = repository.get(weather_id)
    if not weather_record:
        raise HTTPException(status_code=404, detail="Weather record not found")
    
    return weather_record
