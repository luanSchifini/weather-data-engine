from uuid import UUID
from typing import List, Optional
from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from app.config import logger
from app.models.weather_record import WeatherRecord
from app.schemas import WeatherRequest


class WeatherRepository:
    """
    Repository for weather data operations.
    """
    def __init__(self, db: Session):
        self.db = db


    def get_recent_history(self, city: str = None, limit: int = 20) -> List[WeatherRecord]:
        """
        Returns the history of the last collections made to the database, sorted by creation date.
        The default limit is 20.
        """
        query = self.db.query(WeatherRecord)

        if city:
            query = query.filter(WeatherRecord.city.ilike(city))

        return (
            query
            .order_by(desc(WeatherRecord.created_at))
            .limit(limit)
            .all()
        )


    def get_city_stats(self, city: str) -> Optional[dict]:
        """
        Calculates aggregated statistics for a specific city.
        Returns average, maximum, minimum temperature and record count.
        """
        stats = self.db.query(
            func.avg(WeatherRecord.temperature).label("average_temp"),
            func.max(WeatherRecord.temperature).label("max_temp"),
            func.min(WeatherRecord.temperature).label("min_temp"),
            func.count(WeatherRecord.id).label("records_count")
        ).filter(WeatherRecord.city.ilike(city)).first()

        # If no records are found, stats.records_count will be 0 or stats will be None
        if not stats or stats.records_count == 0:
            return None

        return {
            "city": city,
            "average_temp": float(stats.average_temp),
            "max_temp": float(stats.max_temp),
            "min_temp": float(stats.min_temp),
            "records_count": stats.records_count
        }


    def get(self, weather_id: UUID) -> WeatherRecord:
        """
        Returns an existing weather record from the database.
        """
        weather_record = self.db.query(WeatherRecord).filter(WeatherRecord.id == weather_id).first()
        if not weather_record:
            logger.error(f"GetWeatherRecordRepository: Weather record not found for id: {weather_id}")
            return None

        return weather_record


    def create(self, weather_data: WeatherRequest) -> WeatherRecord:
        """
        Creates a new weather record in the database.
        """
        new_weather_record = WeatherRecord(**weather_data.model_dump())
        self.db.add(new_weather_record)
        self.db.commit()
        self.db.refresh(new_weather_record)

        return new_weather_record


    def delete(self, weather_id: UUID) -> WeatherRecord:
        """
        Deletes an existing weather record in the database.
        """
        weather_record = self.db.query(WeatherRecord).filter(WeatherRecord.id == weather_id).first()
        if not weather_record:
            logger.error(f"DeleteWeatherRecordRepository: Weather record not found for id: {weather_id}")
            return None

        self.db.delete(weather_record)
        self.db.commit()

        return weather_record
