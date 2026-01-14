from datetime import datetime
from pydantic import BaseModel, Field


class WeatherBase(BaseModel):
    """
    Pydantic model for core Weather data, shared across requests and responses.
    """
    city: str = Field(..., description="City name", example="Florianópolis")
    country: str = Field(..., description="Country name", example="Brazil")
    lat: float = Field(..., description="Latitude", example=-27.6037)
    lon: float = Field(..., description="Longitude", example=-48.5772)
    description: str = Field(..., description="Weather description (PT-BR)", example="céu limpo")
    temperature: float = Field(..., description="Temperature in Celsius", example=25.5)
    feels_like: float = Field(..., description="Feels like temperature in Celsius", example=26.5)
