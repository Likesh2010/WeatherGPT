from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class WeatherData:
    """
    Normalized weather data used by WeatherGPT.
    """

    location: str

    latitude: float
    longitude: float

    timestamp: Optional[str] = None

    temperature: Optional[float] = None
    feels_like: Optional[float] = None

    condition: Optional[str] = None
    icon: Optional[str] = None

    humidity: Optional[float] = None
    pressure: Optional[float] = None

    wind_speed: Optional[float] = None
    wind_direction: Optional[float] = None

    precipitation: Optional[float] = None
    visibility: Optional[float] = None

    uv: Optional[float] = None

    sunrise: Optional[str] = None
    sunset: Optional[str] = None

    def to_dict(self):
        """
        Convert weather object to dictionary.
        """

        return asdict(self)