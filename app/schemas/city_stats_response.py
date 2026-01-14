from pydantic import BaseModel, Field


class CityStatsResponse(BaseModel):
    """
    Pydantic model for city weather statistics response.
    Includes aggregated data and the unit of measurement.
    """
    city: str = Field(..., description="Name of the city", examples=["London"])
    unit: str = Field(..., description="Temperature unit (C, F, or K)", examples=["C"])
    average_temp: float = Field(..., description="Average temperature recorded", examples=[15.5])
    max_temp: float = Field(..., description="Maximum temperature recorded", examples=[22.0])
    min_temp: float = Field(..., description="Minimum temperature recorded", examples=[8.0])
    records_count: int = Field(..., description="Total number of records analyzed", examples=[10])

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "city": "London",
                "unit": "C",
                "average_temp": 15.42,
                "max_temp": 21.5,
                "min_temp": 9.2,
                "records_count": 15
            }
        }
    }