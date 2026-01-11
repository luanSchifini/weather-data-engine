import requests
from fastapi import HTTPException, status
from app.config import settings, logger
from app.schemas.city_geolocation import CityGeolocation
from app.schemas.weather_request import WeatherRequest


class WeatherCollectorService:
    """
    Service responsible for collecting weather data.
    It orchestrates the conversion of city name to coordinates and retrieves the weather.
    """
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.geo_url = settings.GEOCODING_API_URL
        self.weather_url = settings.WEATHER_API_URL
        self.session = requests.Session()

    def _get_coordinates(self, city_name: str) -> CityGeolocation:
        """Returns the Lat/Lon coordinates from a given city."""
        params = {
            "q": city_name,
            "limit": settings.GEOCODING_LIMIT,
            "appid": self.api_key
        }
        
        try:
            response = self.session.get(self.geo_url, params=params, timeout=settings.API_TIMEOUT)
            response.raise_for_status()
            data = response.json()

            if not data:
                logger.warning(f"City not found in Geocoding: {city_name}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"City '{city_name}' not found."
                )

            return CityGeolocation(
                name=data[0]["name"],
                country=data[0]["country"],
                lat=data[0]["lat"],
                lon=data[0]["lon"]
            )
        except requests.RequestException as e:
            logger.error(f"Geocoding API error: {e}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY, 
                detail="Geocoding service unavailable."
            )

    def _get_weather_data(self, city_geolocation: CityGeolocation) -> WeatherRequest:
        """Fetches real weather data using validated coordinates."""
        params = {
            "lat": city_geolocation.lat,
            "lon": city_geolocation.lon,
            "appid": self.api_key,
            "units": settings.WEATHER_UNITS,
            "lang": settings.WEATHER_LANG
        }

        try:
            response = self.session.get(self.weather_url, params=params, timeout=settings.API_TIMEOUT)
            response.raise_for_status()
            data = response.json()

            return WeatherRequest(
                city=city_geolocation.name,
                temperature=data["main"]["temp"],
                humidity=data["main"]["humidity"],
                description=data["weather"][0]["description"]
            )
        except requests.RequestException as e:
            logger.error(f"Weather API error: {e}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY, 
                detail="Weather service unavailable."
            )

    def execute_collection(self, city_name: str) -> WeatherRequest:
        """Orchestrates the complete workflow."""
        logger.info(f"Starting collection for: {city_name}")

        city_geolocation = self._get_coordinates(city_name)
        weather_data = self._get_weather_data(city_geolocation)

        return weather_data