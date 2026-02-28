# WeatherApiBackend

A FastAPI-based weather proxy service for fetching real-time weather data from OpenWeatherMap API. Built for DevOps course projects with Docker containerization support.

## Table of Contents

- [Installation](#installation)
- [API Key Setup](#api-key-setup)
- [Running Locally](#running-locally)
- [API Usage](#api-usage)
- [Docker Deployment](#docker-deployment)

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Step-by-Step Installation

1. **Clone or download the repository:**
```bash
git clone <repository-url - https://github.com/henria21/WeatherApiBackend>
cd WeatherApiBackend
```

2. **Create a virtual environment:**

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

Verify installation:
```bash
pip list
```

You should see:
- fastapi==0.104.1
- uvicorn==0.24.0
- requests==2.31.0

## API Key Setup

The application requires an OpenWeatherMap API key to fetch weather data.

### Getting Your API Key

1. **Create an account at OpenWeatherMap:**
   - Visit [https://openweathermap.org/api](https://openweathermap.org/api)
   - Click "Sign Up"
   - Complete the registration form
   - Verify your email

2. **Generate API Key:**
   - Log in to your OpenWeatherMap account
   - Go to "API Keys" section in your account settings
   - Copy your default API key

3. **Configure the Application:**

**Option A: Hardcode (Development Only)**
- Open `weather_app.py`
- Replace the `API_KEY` value:
```python
API_KEY = "your_api_key_here"
```

**Option B: Environment Variable (Recommended)**
- Open `weather_app.py`
- Replace the API key section with:
```python
import os
API_KEY = os.getenv("OPENWEATHER_API_KEY", "default_key_if_not_set")
```

**Windows - Set environment variable:**
```bash
set OPENWEATHER_API_KEY=your_api_key_here
python weather_app.py
```

**macOS/Linux - Set environment variable:**
```bash
export OPENWEATHER_API_KEY=your_api_key_here
python weather_app.py
```

## Running Locally

1. **Ensure virtual environment is activated:**

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

2. **Start the application:**
```bash
python weather_app.py
```

You should see output indicating the server is running:
```
INFO:     Uvicorn running on http://127.0.0.1:5000
```

3. **Access the API:**
   - **Base URL:** `http://127.0.0.1:5000`
   - **Interactive Docs (Swagger UI):** `http://127.0.0.1:5000/docs`
   - **Alternative Docs (ReDoc):** `http://127.0.0.1:5000/redoc`

4. **Test the API:**

```bash
# Basic weather request
curl "http://127.0.0.1:5000/weather?location=London"

# With extra data (humidity and wind speed)
curl "http://127.0.0.1:5000/weather?location=London&include_extra=true"
```

## API Usage

### Endpoint

```
GET /weather
```

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `location` | string | Yes | City name (e.g., "London", "New York", "Tokyo") |
| `include_extra` | boolean | No | Include humidity and wind speed (default: false) |

### Example Requests

**Basic weather information:**
```
GET http://127.0.0.1:5000/weather?location=Paris
```

**Response:**
```json
{
  "city": "Paris",
  "temperature": "12.5°C",
  "description": "Cloudy"
}
```

**With humidity and wind speed:**
```
GET http://127.0.0.1:5000/weather?location=Paris&include_extra=true
```

**Response:**
```json
{
  "city": "Paris",
  "temperature": "12.5°C",
  "description": "Cloudy",
  "humidity": "75%",
  "wind_speed": "2.8 m/s"
}
```

### Error Responses

| Status | Description |
|--------|-------------|
| 404 | City not found or invalid location |
| 503 | Weather service unavailable |

## Docker Deployment

### Build and Run Docker Image

```bash
docker build -t weather-api-backend .
docker run -p 5000:5000 weather-api-backend
```

### Using Docker Compose

```bash
docker-compose up
```

The API will be available at `http://localhost:5000`

## Project Structure

```
WeatherApiBackend/
├── weather_app.py          # Main FastAPI application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker image configuration
├── docker-compose.yml     # Docker Compose configuration
├── README.md              # This file
└── LICENSE               # License information
```

## Dependencies

- **FastAPI** - Modern web framework for building APIs
- **Uvicorn** - ASGI web server for running FastAPI
- **Requests** - HTTP library for making API calls to OpenWeatherMap

## Troubleshooting

**Issue: "API key not valid" error**
- Verify your API key is correct
- Check that you've completed email verification on OpenWeatherMap
- Wait a few minutes - new API keys can take time to activate

**Issue: "City not found" error**
- Ensure you're using the correct city name
- Try using the city name without special characters

**Issue: Connection refused**
- Verify the application is running on port 5000
- Check if another application is using port 5000
- Try a different port by modifying `weather_app.py`

## License

See LICENSE file for details.
