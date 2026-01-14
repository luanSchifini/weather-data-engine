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
        """
        Creates a new weather record in the database.
        """
        new_weather_record = WeatherRecord(
            city=weather_data.city,
            temperature=weather_data.temperature,
            humidity=weather_data.humidity,
            description=weather_data.description
        )

        self.db.add(new_weather_record)
        self.db.commit()
        self.db.refresh(new_weather_record)

        return new_weather_record

    def get_recent_history(self, limit: int = 20) -> list[WeatherRecord]:
        """
        Returns the history of the last collections made to the database, sorted by creation date.
        The default limit is 20.
        """
        return (
            self.db.query(WeatherRecord)
            .order_by(desc(WeatherRecord.created_at))
            .limit(limit)
            .all()
        )
