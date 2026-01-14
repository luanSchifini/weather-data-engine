from fastapi import Query
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import logger
from app.schemas import WeatherResponse, CityStatsResponse
from app.repositories import WeatherRepository
from app.services import WeatherOrchestratorService

router = APIRouter()


@router.get("/history", response_model=List[WeatherResponse])
def get_weather_history(
    city: str = None, 
    limit: int = 20, 
    unit: str = Query("C", regex="^(C|F|K|c|f|k)$"),
    db: Session = Depends(get_db)
):
    weather_service = WeatherOrchestratorService(db)
    return weather_service.get_history(city=city, limit=limit, unit=unit)


@router.get("/stats/{city_name}", response_model=CityStatsResponse)
def get_city_stats(
    city_name: str, 
    unit: str = Query("C", regex="^(C|F|K|c|f|k)$"),
    db: Session = Depends(get_db)
):
    weather_service = WeatherOrchestratorService(db)
    stats = weather_service.get_city_analytics(city_name, unit)
    
    if not stats:
        raise HTTPException(status_code=404, detail=f"No data found for city: {city_name}")
        
    return stats


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


