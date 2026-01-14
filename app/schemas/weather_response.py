from pydantic import Field
from datetime import datetime
from uuid import UUID
from .weather_base import WeatherBase


class WeatherResponse(WeatherBase):
    """
    Pydantic model for outgoing weather data.
    """
    id: UUID = Field(..., description="Unique identifier for the weather data")
    humidity: int = Field(..., description="Relative humidity percentage", example=80)
    pressure: int = Field(..., description="Atmospheric pressure in hPa", example=1013)
    visibility: int = Field(..., description="Visibility in meters", example=10000)
    created_at: datetime = Field(..., description="Timestamp of data collection")

    class Config:
        from_attributes = True
