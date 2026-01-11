from pydantic import BaseModel, Field


class CityGeolocation(BaseModel):
    """
    Schema for internal mapping of a city Geolocation.
    """
    name: str = Field(..., description="City name", example="Florianópolis")
    country: str = Field(..., description="City country code (ISO 3166)", example="BR")
    lat: float = Field(..., description="City latitude", example=-27.5945)
    lon: float = Field(..., description="City longitude", example=-48.5487)
