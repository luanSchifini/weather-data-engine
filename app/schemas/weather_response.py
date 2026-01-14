from pydantic import Field
from datetime import datetime
from uuid import UUID
from .weather_base import WeatherBase


class WeatherResponse(WeatherBase):
    """
    Data object for outgoing weather data.
    """
    id: UUID = Field(..., description="Unique identifier for the weather data")
    created_at: datetime = Field(..., description="Timestamp of data collection")

    class Config:
        from_attributes = True
