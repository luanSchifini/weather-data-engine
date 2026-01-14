from sqlalchemy.orm import Session

from app.repositories.weather_repository import WeatherRepository
from app.services.weather_collector import WeatherCollectorService
from app.schemas.weather_response import WeatherResponse

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
        new_record = self.repository.create_weather_record(weather_data_dto)

        return new_record

    def get_history(self, limit: int = 20):
        """Business Logic: Only retrieve data."""
        return self.repository.get_recent_history(limit)