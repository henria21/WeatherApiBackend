import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import os

# Set dummy API key before importing app
os.environ["OPENWEATHER_API_KEY"] = "test_api_key"

from weather_app import app

client = TestClient(app)


# Mock response data
MOCK_WEATHER_DATA = {
    "name": "London",
    "main": {
        "temp": 15.0,
        "humidity": 80
    },
    "weather": [{"description": "clear sky"}],
    "wind": {"speed": 3.5}
}


def mock_get_success(*args, **kwargs):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_WEATHER_DATA
    return mock_response


def mock_get_not_found(*args, **kwargs):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"message": "city not found"}
    return mock_response


def mock_get_connection_error(*args, **kwargs):
    import requests
    raise requests.exceptions.RequestException("Connection error")


# ── Tests ──────────────────────────────────────────────────────────────────────

@patch("weather_app.requests.get", side_effect=mock_get_success)
def test_basic_weather(mock_get):
    response = client.get("/weather?location=London")
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "London"
    assert data["temperature"] == "15.0°C"
    assert data["description"] == "Clear sky"
    assert "humidity" not in data
    assert "wind_speed" not in data


@patch("weather_app.requests.get", side_effect=mock_get_success)
def test_weather_with_extra(mock_get):
    response = client.get("/weather?location=London&include_extra=true")
    assert response.status_code == 200
    data = response.json()
    assert data["humidity"] == "80%"
    assert data["wind_speed"] == "3.5 m/s"


@patch("weather_app.requests.get", side_effect=mock_get_not_found)
def test_city_not_found(mock_get):
    response = client.get("/weather?location=InvalidCity123")
    assert response.status_code == 404
    assert response.json()["detail"] == "city not found"


@patch("weather_app.requests.get", side_effect=mock_get_connection_error)
def test_service_unavailable(mock_get):
    response = client.get("/weather?location=London")
    assert response.status_code == 503
    assert response.json()["detail"] == "Weather service unavailable"


def test_missing_location_param():
    response = client.get("/weather")
    assert response.status_code == 422  # FastAPI validation error
