import pytest
from uuid import uuid4
from unittest.mock import MagicMock
from fastapi import status, HTTPException

from app.services.weather_orchestrator_service import WeatherOrchestratorService
from app.repositories.weather_repository import WeatherRepository

class TestWeatherEndpoints:
    """
    Integration tests for Weather Endpoints.
    """
    @pytest.fixture(autouse=True)
    def setup_data(self):
        """
        Setup shared test data for all tests in this class.
        """
        self.city_name = "Turin"
        self.record_id = str(uuid4())
        self.base_payload = {
            "id": self.record_id,
            "city": self.city_name,
            "country": "IT",
            "temperature": 11.05,
            "description": "moderate rain",
            "humidity": 60,
            "lat": 45.133,
            "lon": 7.367,
            "feels_like": 9.78,
            "pressure": 1021,
            "visibility": 10000,
            "created_at": "2023-10-27T10:00:00"
        }

    def test_given_city_name_when_collect_weather_data_then_returns_201(self, client, mocker):
        """
        Given a city name,
        When the weather data is collected,
        Then returns 201 with all weather fields.
        """
        # Arrange
        mocker.patch.object(
            WeatherOrchestratorService, 
            "process_new_collection", 
            return_value=self.base_payload
        )

        # Act
        response = client.post(f"/weather/collect/{self.city_name}")
        data = response.json()
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert data["id"] == self.record_id
        assert data["city"] == self.city_name
        assert data["temperature"] == 11.05

    def test_given_invalid_city_name_when_collect_weather_data_then_returns_404(self, client, mocker):
        """
        Given an invalid city name,
        When the weather data collection is requested,
        Then returns status 404 with error detail.
        """
        # Arrange
        invalid_city = "InvalidCityNameXYZ"
        mocker.patch.object(
            WeatherOrchestratorService, 
            "process_new_collection", 
            side_effect=HTTPException(status_code=404, detail=f"City '{invalid_city}' not found.")
        )

        # Act
        response = client.post(f"/weather/collect/{invalid_city}")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == f"City '{invalid_city}' not found."

    def test_given_no_data_when_get_history_then_returns_empty_list(self, client, mocker):
        """
        Given no weather records in database,
        When the history is requested,
        Then returns an empty list with status 200.
        """
        # Arrange
        mocker.patch.object(WeatherOrchestratorService, "get_history", return_value=[])
        
        # Act
        response = client.get("/weather/history")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_given_existing_records_when_get_history_then_returns_list(self, client, mocker):
        """
        Given records in database,
        When the history is requested,
        Then returns a list of records.
        """
        # Arrange
        mocker.patch.object(
            WeatherOrchestratorService, 
            "get_history", 
            return_value=[self.base_payload]
        )

        # Act
        response = client.get("/weather/history")
        data = response.json()

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(data) == 1
        assert data[0]["city"] == self.city_name

    def test_given_invalid_limit_when_get_history_then_returns_422(self, client):
        """
        Given an invalid limit parameter (e.g., a string),
        When the history is requested,
        Then returns status 422 Unprocessable Entity.
        """
        # Act
        response = client.get(f"/weather/history?limit=not-a-number")
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_given_invalid_unit_when_get_history_then_returns_422(self, client):
        """
        Given an invalid unit code (not C, F or K),
        When history is requested,
        Then returns 422 Unprocessable Entity.
        """
        # Act
        response = client.get("/weather/history?unit=Z")

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_given_valid_id_when_get_weather_record_by_id_then_returns_200(self, client, mocker):
        """
        Given a valid and existing weather record ID,
        When get weather record by ID,
        Then returns the full record with status 200.
        """
        # Arrange
        mock_record_obj = MagicMock()
        mock_record_obj.id = self.record_id
        mock_record_obj.city = self.city_name

        for k, v in self.base_payload.items():
            setattr(mock_record_obj, k, v)

        mocker.patch.object(WeatherRepository, "get", return_value=mock_record_obj)

        response = client.get(f"/weather/{self.record_id}")
        data = response.json()
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert data["id"] == self.record_id
        assert data["city"] == self.city_name

    def test_given_non_existent_id_when_get_weather_record_by_id_then_returns_404(self, client, mocker):
        """
        Given an ID that does not exist in the database,
        When get weather record by ID,
        Then returns status 404 with error detail.
        """
        # Arrange
        fake_id = uuid4()
        mocker.patch.object(WeatherRepository, "get", return_value=None)

        # Act
        response = client.get(f"/weather/{fake_id}")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Weather record not found"

    def test_given_valid_id_when_delete_weather_record_then_returns_200(self, client, mocker):
        """
        Given a valid and existing weather record ID,
        When a delete weather record,
        Then returns the deleted record data with status 200.
        """
        # Arrange
        mock_deleted_obj = MagicMock()
        mock_deleted_obj.id = self.record_id
        mock_deleted_obj.city = self.city_name
        # Preenchendo campos obrigatórios do response model
        for k, v in self.base_payload.items():
            setattr(mock_deleted_obj, k, v)

        mocker.patch.object(WeatherRepository, "delete", return_value=mock_deleted_obj)

        # Act
        response = client.delete(f"/weather/{self.record_id}")
        data = response.json()
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert data["id"] == self.record_id

    def test_given_non_existent_id_when_delete_weather_record_then_returns_404(self, client, mocker):
        """
        Given an ID that does not exist in the database,
        When a delete weather record,
        Then returns status 404.
        """
        # Arrange
        fake_id = uuid4()
        mocker.patch.object(WeatherRepository, "delete", return_value=None)

        # Act
        response = client.delete(f"/weather/{fake_id}")
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_given_city_with_data_when_get_stats_in_fahrenheit_then_returns_200_converted(self, client, mocker):
        """
        Given a city with records,
        When stats are requested in Fahrenheit,
        Then returns 200 with all values converted correctly.
        """
        # Arrange
        unit = "F"
        expected_analytics = {
            "city": self.city_name,
            "unit": unit,
            "average_temp": 68.0,
            "max_temp": 77.0,
            "min_temp": 59.0,
            "records_count": 3
        }
        
        mocker.patch.object(
            WeatherOrchestratorService, 
            "get_city_analytics", 
            return_value=expected_analytics
        )

        # Act
        response = client.get(f"/weather/stats/{self.city_name}?unit={unit}")
        data = response.json()

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert data["unit"] == "F"
        assert data["average_temp"] == 68.0
        assert data["city"] == self.city_name

    def test_given_empty_city_when_get_stats_then_returns_404(self, client, mocker):
        """
        Given a city without records,
        When stats are requested,
        Then returns 404 Not Found.
        """
        # Arrange
        unknown_city = "Atlantis"
        mocker.patch.object(
            WeatherOrchestratorService, 
            "get_city_analytics", 
            return_value=None
        )

        # Act
        response = client.get(f"/weather/stats/{unknown_city}")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "no data found" in response.json()["detail"].lower()
