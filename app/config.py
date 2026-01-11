import logging
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized Configuration Management.
    The Pydantic Settings is used to load the settings from the environment variables.
    """
    # External API
    OPENWEATHERMAP_API_KEY: str
    
    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432 # Default PostgreSQL port
    DATABASE_URL: str

    # Pydantic config for .env file reading
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore" # Ignore extra variables in the .env file
    )
    
settings = Settings()

# Basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("gntech-api")
