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

    def create_weather_record(self, weather_data: WeatherRequest) -> WeatherRecord:
        new_entry = WeatherRecord(
            city=weather_data.city,
            temperature=weather_data.temperature,
            humidity=weather_data.humidity,
            description=weather_data.description
        )

        self.db.add(new_entry)
        self.db.commit()
        self.db.refresh(new_entry)

        return new_entry

    def get_recent_history(self, limit: int = 20) -> list[WeatherRecord]:
        return (
            self.db.query(WeatherRecord)
            .order_by(desc(WeatherRecord.created_at))
            .limit(limit)
            .all()
        )
