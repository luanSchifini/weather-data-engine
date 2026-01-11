from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base


class WeatherRecord(Base):
    """
    Database model representing the 'weather_records' table.
    Stores the history of all successful weather collections.
    """
    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=False, index=True)
    temperature = Column(Float, nullable=False)
    humidity = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __str__(self):
        return f"<WeatherRecord(city={self.city}, temperature={self.temperature})>"