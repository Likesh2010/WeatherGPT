import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Central configuration for WeatherGPT.
    """

    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    HOST = os.getenv(
        "HOST",
        "0.0.0.0"
    )

    PORT = int(
        os.getenv(
            "PORT",
            "5000"
        )
    )

    WEATHER_API_BASE_URL = os.getenv(
        "WEATHER_API_BASE_URL",
        "https://api.open-meteo.com/v1/forecast"
    )

    GEOCODING_API_BASE_URL = os.getenv(
        "GEOCODING_API_BASE_URL",
        "https://geocoding-api.open-meteo.com/v1/search"
    )

    REQUEST_TIMEOUT = int(
        os.getenv(
            "REQUEST_TIMEOUT",
            "10"
        )
    )