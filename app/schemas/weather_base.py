from pydantic import BaseModel, Field


class WeatherBase(BaseModel):
    """
    Core Weather data model, shared across requests and responses.
    """
    city: str = Field(..., description="City name", example="Florianópolis")
    temperature: float = Field(..., description="Temperature in Celsius", example=25.5)
    humidity: int = Field(..., description="Relative humidity percentage", example=80)
    description: str = Field(..., description="Weather description (PT-BR)", example="céu limpo")
