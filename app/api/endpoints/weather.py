from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import logger
from app.database import get_db
from app.schemas.weather_response import WeatherResponse
from app.services.weather_collector import WeatherCollectorService
from app.services.weather_repository import WeatherRepository

router = APIRouter()


@router.post(
    "/weather/collect/{city_name}",
    response_model=WeatherResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Weather"]
)
def collect_weather_data(city_name: str, db: Session = Depends(get_db)):
    """
    Activate the weather data collection pipeline:
    1. Geocoding (Name -> Lat/Lon)
    2. Weather API (Actual Weather)
    3. Persistence (PostgreSQL)
    """
    try:
        collector = WeatherCollectorService()
        weather_data = collector.execute_collection(city_name)
        
        repository = WeatherRepository(db)
        record = repository.create_weather_record(weather_data)
        
        return record
    except Exception as e:
        logger.error(f"Unexpected error processing {city_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="An unexpected error occurred while processing the request."
        )


@router.get("/weather/history", response_model=List[WeatherResponse], tags=["Weather"])
def get_weather_history(limit: int = 20, db: Session = Depends(get_db)):
    """
    Returns the history of the last collections made to the database.
    """
    repository = WeatherRepository(db)
    return repository.get_recent_history(limit=limit)
