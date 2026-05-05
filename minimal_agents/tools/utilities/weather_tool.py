from minimal_agents.tools.base import Tool
import requests


class WeatherTool(Tool):
    """Tool for getting weather information."""
    
    name: str = "Weather Tool"
    description: str = "Get current weather for a location. Input should be a city name."
    
    def run(self, input_text: str) -> str:
        """Get weather for the specified location."""
        location = input_text.strip()
        if not location:
            return "Weather error: Please provide a location."

        try:
            geo = self._geocode_location(location)
            if not geo:
                return f"Weather error: Could not find location '{location}'."

            weather = self._get_current_weather(geo["latitude"], geo["longitude"], geo["timezone"])
            if not weather:
                return f"Weather error: Could not fetch weather for '{location}'."

            condition = self._weather_code_to_text(weather["weathercode"])
            temp_c = weather["temperature"]
            wind_kmh = weather["windspeed"]
            timestamp = weather["time"]

            return (
                f"Weather for {geo['name']}, {geo.get('country', 'Unknown')}: "
                f"{temp_c}°C, {condition}. Wind {wind_kmh} km/h. "
                f"Observed at {timestamp} ({geo['timezone']})."
            )
        except requests.RequestException as e:
            return f"Weather error: Network/API request failed: {str(e)}"
        except Exception as e:
            return f"Weather error: {str(e)}"

    def _geocode_location(self, location: str):
        response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": location, "count": 1, "language": "en", "format": "json"},
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        if not results:
            return None
        first = results[0]
        return {
            "name": first.get("name", location),
            "country": first.get("country", ""),
            "latitude": first["latitude"],
            "longitude": first["longitude"],
            "timezone": first.get("timezone", "auto"),
        }

    def _get_current_weather(self, latitude: float, longitude: float, timezone: str):
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": "true",
                "timezone": timezone or "auto",
            },
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("current_weather")

    def _weather_code_to_text(self, code: int) -> str:
        mapping = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            56: "Light freezing drizzle",
            57: "Dense freezing drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            66: "Light freezing rain",
            67: "Heavy freezing rain",
            71: "Slight snow fall",
            73: "Moderate snow fall",
            75: "Heavy snow fall",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail",
        }
        return mapping.get(code, f"Unknown weather code ({code})")