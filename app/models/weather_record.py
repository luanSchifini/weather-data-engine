from uuid import uuid4
from sqlalchemy import Column, Integer, String, Float, DateTime, Uuid
from sqlalchemy.sql import func
from app.database import Base


class WeatherRecord(Base):
    """
    Represents a weather record in the database.
    """
    __tablename__ = "weather_records"

    id = Column(Uuid, primary_key=True, index=True, default=uuid4)
    city = Column(String, nullable=False, index=True)
    country = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)

    description = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    feels_like = Column(Float, nullable=False)
    humidity = Column(Integer, nullable=False)
    pressure = Column(Integer, nullable=False)
    visibility = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __str__(self):
        return f"<WeatherRecord(city={self.city}, temperature={self.temperature})>"