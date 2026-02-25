# WeatherApiBackend

A FastAPI-based weather proxy service for fetching real-time weather data from OpenWeatherMap API. Built for DevOps course projects with Docker containerization support.

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **Weather Data**: Fetch current weather information by location
- **Optional Fields**: Include humidity and wind speed with query parameter
- **Error Handling**: Robust error handling for invalid locations and service unavailability
- **Docker Support**: Fully containerized application with docker-compose

## Getting Started

### Prerequisites

- Python 3.9+
- Docker and Docker Compose (optional)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd WeatherApiBackend
```

2. Create a virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running Locally

```bash
python weather_app.py
```

The API will be available at `http://127.0.0.1:8000`

Access the interactive API documentation at `http://127.0.0.1:8000/docs`

### Docker

Build and run with Docker:
```bash
docker build -t weather-api-backend .
docker run -p 8000:8000 weather-api-backend
```

Or use Docker Compose:
```bash
docker-compose up
```

## API Usage

### Get Weather Information

```
GET /weather?location=<city_name>&include_extra=<true|false>
```

**Parameters:**
- `location` (required): City name (e.g., "Tel Aviv", "New York")
- `include_extra` (optional): Set to `true` to include humidity and wind speed (default: false)

**Example Requests:**

Basic weather:
```
GET /weather?location=TelAviv
```

With extra data:
```
GET /weather?location=TelAviv&include_extra=true
```

**Example Response:**
```json
{
  "city": "Tel Aviv",
  "temperature": "18.5°C",
  "description": "Clear sky",
  "humidity": "62%",
  "wind_speed": "3.1 m/s"
}
```

## Project Structure

```
WeatherApiBackend/
├── weather_app.py          # Main application file
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker container configuration
├── docker-compose.yml     # Docker Compose orchestration
├── README.md              # This file
└── LICENSE               # License file
```

## Dependencies

- **FastAPI**: Web framework for building APIs
- **uvicorn**: ASGI web server
- **requests**: HTTP library for API calls

See `requirements.txt` for complete list and versions.

## Environment Configuration

The application uses:
- OpenWeatherMap API Key: Built-in (for development)
- Host: 127.0.0.1 (localhost)
- Port: 8000

For production use, consider:
- Moving API key to environment variables
- Changing host to 0.0.0.0 for container deployment

## Error Handling

- **404**: City not found or invalid location
- **503**: Weather service unavailable

## License

See LICENSE file for details.
