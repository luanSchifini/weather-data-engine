from pydantic import Field
from .weather_base import WeatherBase

class WeatherRequest(WeatherBase):
    """
    Pydantic model for incoming weather data.
    """
    humidity: int = Field(..., description="Relative humidity percentage", example=80)
    pressure: int = Field(..., description="Atmospheric pressure in hPa", example=1013)
    visibility: int = Field(..., description="Visibility in meters", example=10000)
