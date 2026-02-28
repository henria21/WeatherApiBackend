import os
from fastapi import FastAPI, HTTPException, Query
import requests

app = FastAPI(title="Weather Proxy API")

# Configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENWEATHER_API_KEY environment variable is not set")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"  

@app.get("/weather")
async def get_weather(
    location: str,
    include_extra: bool = Query(False, description="Include humidity and wind speed")
):
    """
    Fetch weather for a location.
    Pass 'include_extra=true' to see humidity and wind speed.
    """
    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=data.get("message", "City not found"))

        weather_report = {
            "city": data["name"],
            "temperature": f"{data['main']['temp']}°C",
            "description": data["weather"][0]["description"].capitalize()
        }

        if include_extra:
            weather_report["humidity"] = f"{data['main']['humidity']}%"
            weather_report["wind_speed"] = f"{data['wind']['speed']} m/s"

        return weather_report

    except requests.exceptions.RequestException:
        raise HTTPException(status_code=503, detail="Weather service unavailable")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)  # Fixed: 0.0.0.0 so Docker can reach it
