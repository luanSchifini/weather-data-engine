from app.config import logger
from uuid import UUID
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.models.weather_record import WeatherRecord
from app.schemas import WeatherRequest


class WeatherRepository:
    """
    Repository for weather data operations.
    """
    def __init__(self, db: Session):
        self.db = db


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


    def get(self, weather_id: UUID) -> WeatherRecord:
        """
        Returns an existing weather record from the database.
        """
        weather_record = self.db.query(WeatherRecord).filter(WeatherRecord.id == weather_id).first()
        if not weather_record:
            logger.error(f"GetWeatherRecordRepository: Weather record not found for id: {weather_id}")
            return None

        return weather_record


    def get_recent_history(self, city: str = None, limit: int = 20) -> list[WeatherRecord]:
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
