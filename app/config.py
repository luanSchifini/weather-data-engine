import logging
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized Settings Management.
    The Pydantic Settings is used to load the settings from the environment variables.
    """
    # External API - OpenWeather
    OPENWEATHER_API_KEY: str
    GEOCODING_API_URL: str = "http://api.openweathermap.org/geo/1.0/direct"
    WEATHER_API_URL: str = "https://api.openweathermap.org/data/2.5/weather"
    
    # API Request Configuration
    WEATHER_UNITS: str = "metric"
    WEATHER_LANG: str = "pt_br"
    API_TIMEOUT: int = 10
    GEOCODING_LIMIT: int = 1
    
    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432  # Default PostgreSQL port
    DATABASE_URL: str

    # Pydantic config for .env file reading
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Ignore extra variables in the .env file
    )
    
settings = Settings()

# Basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("gntech-api")
