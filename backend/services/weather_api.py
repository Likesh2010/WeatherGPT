import requests

from backend.config.config import Config
from backend.utils.data_processing import (
    process_current_weather
)
from backend.utils.helpers import (
    is_valid_coordinate
)


class WeatherAPIService:
    """
    Handles communication with the weather provider.
    """

    def __init__(self):

        self.weather_url = (
            Config.WEATHER_API_BASE_URL
        )

        self.geocoding_url = (
            Config.GEOCODING_API_BASE_URL
        )

        self.timeout = (
            Config.REQUEST_TIMEOUT
        )


    def geocode_location(
        self,
        location
    ):
        """
        Convert location name into coordinates.
        """

        if not location:
            raise ValueError(
                "Location is required."
            )


        params = {

            "name": location,

            "count": 1,

            "language": "en",

            "format": "json"

        }


        response = requests.get(
            self.geocoding_url,
            params=params,
            timeout=self.timeout
        )


        response.raise_for_status()


        data = response.json()


        results = data.get(
            "results",
            []
        )


        if not results:

            raise ValueError(
                "Location not found."
            )


        result = results[0]


        return {

            "location":
                self._format_location_name(
                    result
                ),

            "latitude":
                result.get(
                    "latitude"
                ),

            "longitude":
                result.get(
                    "longitude"
                ),

            "country":
                result.get(
                    "country"
                ),

            "admin1":
                result.get(
                    "admin1"
                )

        }


    def _format_location_name(
        self,
        result
    ):
        """
        Create a readable location name.
        """

        name = result.get(
            "name",
            "Unknown"
        )

        admin = result.get(
            "admin1"
        )

        country = result.get(
            "country"
        )


        parts = [name]


        if admin and admin != name:
            parts.append(admin)


        if country:
            parts.append(country)


        return ", ".join(parts)


    def get_weather_by_coordinates(
        self,
        latitude,
        longitude,
        location_name=None
    ):
        """
        Retrieve current weather using coordinates.
        """

        if not is_valid_coordinate(
            latitude,
            longitude
        ):

            raise ValueError(
                "Invalid coordinates."
            )


        latitude = float(latitude)
        longitude = float(longitude)


        params = {

            "latitude": latitude,

            "longitude": longitude,

            "current": ",".join([

                "temperature_2m",

                "relative_humidity_2m",

                "apparent_temperature",

                "precipitation",

                "weather_code",

                "surface_pressure",

                "wind_speed_10m",

                "wind_direction_10m",

                "visibility"

            ]),

            "daily": ",".join([

                "weather_code",

                "temperature_2m_mean",

                "precipitation_sum",

                "precipitation_probability_max",

                "uv_index_max",

                "sunrise",

                "sunset"

            ]),

            "timezone": "auto"

        }


        response = requests.get(

            self.weather_url,

            params=params,

            timeout=self.timeout

        )


        response.raise_for_status()


        data = response.json()


        if location_name is None:

            location_name = (
                f"{latitude:.4f}, "
                f"{longitude:.4f}"
            )


        return process_current_weather(

            data,

            location_name,

            latitude,

            longitude

        )


    def get_weather_by_location(
        self,
        location
    ):
        """
        Geocode a location and retrieve weather.
        """

        location_data = (
            self.geocode_location(
                location
            )
        )


        return self.get_weather_by_coordinates(

            location_data["latitude"],

            location_data["longitude"],

            location_data["location"]

        )


    def get_raw_weather(
        self,
        latitude,
        longitude
    ):
        """
        Retrieve raw weather data.

        Used by forecast services.
        """

        if not is_valid_coordinate(
            latitude,
            longitude
        ):

            raise ValueError(
                "Invalid coordinates."
            )


        params = {

            "latitude": latitude,

            "longitude": longitude,

            "current": ",".join([

                "temperature_2m",

                "relative_humidity_2m",

                "apparent_temperature",

                "precipitation",

                "weather_code",

                "surface_pressure",

                "wind_speed_10m",

                "wind_direction_10m",

                "visibility"

            ]),

            "hourly": ",".join([

                "temperature_2m",

                "relative_humidity_2m",

                "precipitation",

                "precipitation_probability",

                "weather_code",

                "wind_speed_10m"

            ]),

            "daily": ",".join([

                "weather_code",

                "temperature_2m_mean",

                "precipitation_sum",

                "precipitation_probability_max",

                "uv_index_max",

                "sunrise",

                "sunset"

            ]),

            "forecast_days": 7,

            "timezone": "auto"

        }


        response = requests.get(

            self.weather_url,

            params=params,

            timeout=self.timeout

        )


        response.raise_for_status()


        return response.json()