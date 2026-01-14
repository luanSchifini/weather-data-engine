import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from fastapi import status

from app.services.weather_orchestrator_service import WeatherOrchestratorService
from app.repositories.weather_repository import WeatherRepository


def test_given_city_name_when_collect_weather_data_then_returns_201(client, mocker):
    """
    Given a city name,
    When the weather data is collected,
    Then returns 201 with all weather fields.
    """
    # Arrange
    city = "Turin"
    record_id = str(uuid4())
    expected_response = {
        "id": record_id,
        "city": city,
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

    mocker.patch.object(WeatherOrchestratorService, "process_new_collection", return_value=expected_response)

    # Act
    response = client.post(f"/weather/collect/{city}")
    data = response.json()
    
    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert data["id"] == record_id
    assert data["city"] == city
    assert data["temperature"] == 11.05
    assert data["description"] == "moderate rain"


def test_given_invalid_city_name_when_collect_weather_data_then_returns_404(client, mocker):
    """
    Given an invalid city name,
    When the weather data collection is requested,
    Then returns status 404 with error detail.
    """
    # Arrange
    invalid_city = "InvalidCityNameXYZ"
    from fastapi import HTTPException
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


def test_given_no_data_when_get_history_then_returns_empty_list(client, mocker):
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


def test_given_existing_records_when_get_history_then_returns_list(client, mocker):
    """
    Given records in database,
    When the history is requested,
    Then returns a list of records.
    """
    # Arrange
    mock_record = {
        "id": str(uuid4()),
        "city": "London",
        "country": "GB",
        "temperature": 15.0,
        "description": "cloudy",
        "humidity": 50,
        "lat": 51.5,
        "lon": -0.1,
        "feels_like": 14.0,
        "pressure": 1012,
        "visibility": 10000,
        "created_at": "2023-10-27T10:00:00"
    }
    mocker.patch.object(WeatherOrchestratorService, "get_history", return_value=[mock_record])

    # Act
    response = client.get("/weather/history")
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 1
    assert data[0]["city"] == "London"
    assert data[0]["temperature"] == 15.0


def test_given_invalid_limit_when_get_history_then_returns_422(client):
    """
    Given an invalid limit parameter (e.g., a string),
    When the history is requested,
    Then returns status 422 Unprocessable Entity.
    """
    # Arrange
    invalid_limit = "not-a-number"

    # Act
    response = client.get(f"/weather/history?limit={invalid_limit}")
    
    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_given_valid_uuid_when_get_weather_record_by_id_then_returns_200(client, mocker):
    """
    Given a valid and existing weather record ID,
    When get weather record by ID,
    Then returns the full record with status 200.
    """
    # Arrange
    record_id = uuid4()
    mock_record = MagicMock()
    mock_record.id = record_id
    mock_record.city = "London"
    mock_record.country = "GB"
    mock_record.temperature = 15.0
    mock_record.description = "cloudy"
    mock_record.humidity = 50
    mock_record.lat = 51.50
    mock_record.lon = -0.12
    mock_record.feels_like = 14.0
    mock_record.pressure = 1012
    mock_record.visibility = 10000

    mocker.patch.object(WeatherRepository, "get", return_value=mock_record)

    # Act
    response = client.get(f"/weather/{record_id}")
    data = response.json()
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert data["id"] == str(record_id)
    assert data["city"] == "London"
    assert data["country"] == "GB"
    assert data["humidity"] == 50
    assert data["lat"] == 51.50


def test_given_non_existent_uuid_when_get_weather_record_by_id_then_returns_404(client, mocker):
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


def test_given_valid_uuid_when_delete_weather_record_then_returns_200(client, mocker):
    """
    Given a valid and existing weather record ID,
    When a delete weather record,
    Then returns the deleted record data with status 200.
    """
    # Arrange
    record_id = uuid4()
    mock_deleted_record = MagicMock()
    mock_deleted_record.id = record_id
    mock_deleted_record.city = "Rome"
    mock_deleted_record.country = "IT"
    mock_deleted_record.temperature = 22.0
    mock_deleted_record.description = "sunny"
    mock_deleted_record.humidity = 40
    mock_deleted_record.lat = 41.9
    mock_deleted_record.lon = 12.5
    mock_deleted_record.feels_like = 22.0
    mock_deleted_record.pressure = 1013
    mock_deleted_record.visibility = 10000

    mocker.patch.object(WeatherRepository, "delete", return_value=mock_deleted_record)

    # Act
    response = client.delete(f"/weather/{record_id}")
    data = response.json()
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert data["id"] == str(record_id)
    assert data["city"] == "Rome"
    assert data["description"] == "sunny"


def test_given_non_existent_uuid_when_delete_weather_record_then_returns_404(client, mocker):
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
    assert response.json()["detail"] == "Weather record not found"


def test_given_city_with_data_when_get_stats_in_fahrenheit_then_returns_201_converted(client, mocker):
    """
    Given a city with records,
    When stats are requested in Fahrenheit,
    Then returns 200 with all values converted correctly.
    """
    # Arrange
    city = "London"
    unit = "F"
    # Mock de retorno do serviço já processado (20°C -> 68°F)
    mock_analytics = {
        "city": "London",
        "unit": "F",
        "average_temp": 68.0,
        "max_temp": 77.0,
        "min_temp": 59.0,
        "records_count": 3
    }
    
    mocker.patch.object(WeatherOrchestratorService, "get_city_analytics", return_value=mock_analytics)

    # Act
    response = client.get(f"/weather/stats/{city}?unit={unit}")
    data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert data["unit"] == "F"
    assert data["average_temp"] == 68.0
    assert data["city"] == city


def test_given_empty_city_when_get_stats_then_returns_404(client, mocker):
    """
    Given a city without records,
    When stats are requested,
    Then returns 404 Not Found.
    """
    # Arrange
    city = "Atlantis"
    mocker.patch.object(WeatherOrchestratorService, "get_city_analytics", return_value=None)

    # Act
    response = client.get(f"/weather/stats/{city}")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "no data found" in response.json()["detail"].lower()


def test_given_invalid_unit_when_get_history_then_returns_422(client):
    """
    Given an invalid unit code (not C, F or K),
    When history is requested,
    Then returns 422 Unprocessable Entity (Validation Error).
    """
    # Act
    response = client.get("/weather/history?unit=Z")

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_given_multiple_records_when_get_city_stats_then_calculates_correct_aggregates(db_session):
    """
    Given multiple records for the same city in DB,
    When get_city_stats is called in repository,
    Then returns correct AVG, MAX, MIN.
    """
    # Arrange
    repo = WeatherRepository(db_session)
    city = "TestCity"
    
    # Criando registros manuais para teste de agregação (10, 20, 30 graus)
    for temp in [10.0, 20.0, 30.0]:
        from app.models.weather_record import WeatherRecord
        record = WeatherRecord(
            city=city, country="TS", lat=0, lon=0,
            temperature=temp, feels_like=temp, humidity=50,
            pressure=1000, description="test", visibility=10000
        )
        db_session.add(record)
    db_session.commit()

    # Act
    stats = repo.get_city_stats(city)

    # Assert
    assert stats is not None
    assert stats["average_temp"] == 20.0  # (10+20+30)/3
    assert stats["max_temp"] == 30.0
    assert stats["min_temp"] == 10.0
    assert stats["records_count"] == 3


def test_given_no_records_when_get_city_stats_then_returns_none(db_session):
    """
    Given an empty database,
    When get_city_stats is called,
    Then returns None.
    """
    # Arrange
    repo = WeatherRepository(db_session)

    # Act
    stats = repo.get_city_stats("NonExistent")

    # Assert
    assert stats is None