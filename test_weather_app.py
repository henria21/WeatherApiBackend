import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
import os
import httpx

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


def make_mock_client(status_code, json_data):
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.json.return_value = json_data

    mock_async_client = AsyncMock()
    mock_async_client.get = AsyncMock(return_value=mock_response)
    mock_async_client.__aenter__ = AsyncMock(return_value=mock_async_client)
    mock_async_client.__aexit__ = AsyncMock(return_value=None)
    return mock_async_client


# ── Tests ──────────────────────────────────────────────────────────────────────

@patch("httpx.AsyncClient", return_value=make_mock_client(200, MOCK_WEATHER_DATA))
def test_basic_weather(mock_client):
    response = client.get("/weather?location=London")
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "London"
    assert data["temperature"] == "15.0°C"
    assert data["description"] == "Clear sky"
    assert "humidity" not in data
    assert "wind_speed" not in data


@patch("httpx.AsyncClient", return_value=make_mock_client(200, MOCK_WEATHER_DATA))
def test_weather_with_extra(mock_client):
    response = client.get("/weather?location=London&include_extra=true")
    assert response.status_code == 200
    data = response.json()
    assert data["humidity"] == "80%"
    assert data["wind_speed"] == "3.5 m/s"


@patch("httpx.AsyncClient", return_value=make_mock_client(404, {"message": "city not found"}))
def test_city_not_found(mock_client):
    response = client.get("/weather?location=InvalidCity123")
    assert response.status_code == 404
    assert response.json()["detail"] == "city not found"


def test_service_unavailable():
    mock_async_client = AsyncMock()
    mock_async_client.get = AsyncMock(side_effect=httpx.RequestError("Connection error"))
    mock_async_client.__aenter__ = AsyncMock(return_value=mock_async_client)
    mock_async_client.__aexit__ = AsyncMock(return_value=None)

    with patch("httpx.AsyncClient", return_value=mock_async_client):
        response = client.get("/weather?location=London")
    assert response.status_code == 503
    assert response.json()["detail"] == "Weather service unavailable"


def test_missing_location_param():
    response = client.get("/weather")
    assert response.status_code == 422  # FastAPI validation error
