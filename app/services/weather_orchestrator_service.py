from sqlalchemy.orm import Session

from app.repositories import WeatherRepository
from app.services import WeatherCollectorService
from app.schemas import WeatherResponse
from app.utils import convert_temperature


class WeatherOrchestratorService:
    """
    Orchestrator service for weather data.
    It orchestrates the complete workflow for weather data collection and persistence.
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = WeatherRepository(db)
        self.collector = WeatherCollectorService()

    def process_new_collection(self, city_name: str) -> WeatherResponse:
        """
        Business Logic:
        1. Collect external data.
        2. Save to history.
        3. Return processed data.
        """
        # Collection - External
        weather_data_dto = self.collector.execute_collection(city_name)

        # Persistence - Internal
        new_record = self.repository.create(weather_data_dto)
        return new_record

    def get_history(self, city: str = None, limit: int = 20, unit: str = "C"):
        """
        Business Logic:
        1. Retrieve recent history from the database.
        2. Convert temperatures to the desired unit on-the-fly.
        """
        records = self.repository.get_recent_history(city=city, limit=limit)
        
        # Apply conversion on-the-fly
        for record in records:
            record.temperature = convert_temperature(record.temperature, unit)
            record.feels_like = convert_temperature(record.feels_like, unit)
        
        return records

    def get_city_analytics(self, city: str, unit: str = "C"):
        """
        Business Logic:
        1. Retrieve city analytics from the database.
        2. Convert aggregated temperatures to the desired unit.
        """
        stats = self.repository.get_city_stats(city)
        if not stats:
            return None
        
        # Convert aggregated values to the desired unit
        stats["average_temp"] = convert_temperature(stats["average_temp"], unit)
        stats["max_temp"] = convert_temperature(stats["max_temp"], unit)
        stats["min_temp"] = convert_temperature(stats["min_temp"], unit)
        stats["unit"] = unit.upper()
        
        return stats