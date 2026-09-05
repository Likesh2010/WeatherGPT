import csv
import os

import requests

from backend.config.config import Config
from backend.utils.data_processing import process_current_weather
from backend.utils.helpers import is_valid_coordinate


class WeatherAPIService:

    FALLBACK_LOCATIONS = {
        "chennai": {
            "name": "Chennai",
            "display_name": "Chennai, Tamil Nadu, India",
            "latitude": 13.08784,
            "longitude": 80.27847,
            "country": "India",
            "country_code": "IN",
            "admin1": "Tamil Nadu",
            "admin2": None,
            "timezone": "Asia/Kolkata"
        },
        "mumbai": {
            "name": "Mumbai",
            "display_name": "Mumbai, Maharashtra, India",
            "latitude": 19.0760,
            "longitude": 72.8777,
            "country": "India",
            "country_code": "IN",
            "admin1": "Maharashtra",
            "admin2": None,
            "timezone": "Asia/Kolkata"
        },
        "delhi": {
            "name": "Delhi",
            "display_name": "Delhi, India",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "country": "India",
            "country_code": "IN",
            "admin1": "Delhi",
            "admin2": None,
            "timezone": "Asia/Kolkata"
        },
        "bengaluru": {
            "name": "Bengaluru",
            "display_name": "Bengaluru, Karnataka, India",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "country": "India",
            "country_code": "IN",
            "admin1": "Karnataka",
            "admin2": None,
            "timezone": "Asia/Kolkata"
        },
        "hyderabad": {
            "name": "Hyderabad",
            "display_name": "Hyderabad, Telangana, India",
            "latitude": 17.3850,
            "longitude": 78.4867,
            "country": "India",
            "country_code": "IN",
            "admin1": "Telangana",
            "admin2": None,
            "timezone": "Asia/Kolkata"
        },
        "kolkata": {
            "name": "Kolkata",
            "display_name": "Kolkata, West Bengal, India",
            "latitude": 22.5726,
            "longitude": 88.3639,
            "country": "India",
            "country_code": "IN",
            "admin1": "West Bengal",
            "admin2": None,
            "timezone": "Asia/Kolkata"
        },
        "pune": {
            "name": "Pune",
            "display_name": "Pune, Maharashtra, India",
            "latitude": 18.5204,
            "longitude": 73.8567,
            "country": "India",
            "country_code": "IN",
            "admin1": "Maharashtra",
            "admin2": None,
            "timezone": "Asia/Kolkata"
        },
        "jaipur": {
            "name": "Jaipur",
            "display_name": "Jaipur, Rajasthan, India",
            "latitude": 26.9124,
            "longitude": 75.7873,
            "country": "India",
            "country_code": "IN",
            "admin1": "Rajasthan",
            "admin2": None,
            "timezone": "Asia/Kolkata"
        }
    }

    def __init__(self):
        self.weather_base_url = Config.WEATHER_API_BASE_URL
        self.geocoding_base_url = Config.GEOCODING_API_BASE_URL
        self.timeout = Config.REQUEST_TIMEOUT

    def _fallback_location_data(self, location):
        normalized = str(location or "").strip().lower()
        if not normalized:
            return None

        exact = self.FALLBACK_LOCATIONS.get(normalized)
        if exact:
            return exact

        for key, data in self.FALLBACK_LOCATIONS.items():
            if key in normalized or normalized in key:
                return data

        return None

    def _get_fallback_sample_rows(self):
        data_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "data",
                "sample_weather_data.csv"
            )
        )

        with open(data_path, newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            return list(reader)

    def _build_fallback_weather_response(
        self,
        latitude,
        longitude,
        location_name=None
    ):
        rows = self._get_fallback_sample_rows()

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (TypeError, ValueError):
            latitude = 13.08
            longitude = 80.27

        matching_row = None
        for row in rows:
            lat_delta = abs(float(row["latitude"]) - latitude)
            lon_delta = abs(float(row["longitude"]) - longitude)
            if lat_delta <= 0.2 and lon_delta <= 0.2:
                matching_row = row
                break

        if matching_row is None:
            matching_row = rows[0]

        current_time = matching_row["timestamp"]
        today_date = current_time.split("T")[0]

        daily_times = [
            row["timestamp"].split("T")[0]
            for row in rows[:7]
        ]

        daily_temps = [float(row["temperature"]) for row in rows[:7]]
        daily_precip = [float(row["precipitation"]) for row in rows[:7]]
        daily_rain_probability = [float(row["rain_probability"]) for row in rows[:7]]
        daily_codes = [0 for _ in rows[:7]]

        hourly_times = [
            f"{today_date}T{hour:02d}:00"
            for hour in range(24)
        ]
        hourly_temps = [float(matching_row["temperature"]) for _ in range(24)]
        hourly_precip = [float(matching_row["precipitation"]) for _ in range(24)]
        hourly_rain_probability = [float(matching_row["rain_probability"]) for _ in range(24)]
        hourly_humidity = [float(matching_row["humidity"]) for _ in range(24)]
        hourly_wind = [float(matching_row["wind_speed"]) for _ in range(24)]
        hourly_codes = [0 for _ in range(24)]

        return {
            "current": {
                "time": current_time,
                "temperature_2m": float(matching_row["temperature"]),
                "apparent_temperature": float(matching_row["feels_like"]),
                "relative_humidity_2m": int(float(matching_row["humidity"])),
                "precipitation": float(matching_row["precipitation"]),
                "weather_code": 0,
                "surface_pressure": float(matching_row["pressure"]),
                "wind_speed_10m": float(matching_row["wind_speed"]),
                "wind_direction_10m": 180,
                "visibility": float(matching_row["visibility"])
            },
            "daily": {
                "time": daily_times,
                "temperature_2m_mean": daily_temps,
                "precipitation_sum": daily_precip,
                "precipitation_probability_max": daily_rain_probability,
                "uv_index_max": [5 for _ in daily_times],
                "sunrise": [f"{date}T06:00" for date in daily_times],
                "sunset": [f"{date}T18:00" for date in daily_times],
                "weather_code": daily_codes,
            },
            "hourly": {
                "time": hourly_times,
                "temperature_2m": hourly_temps,
                "precipitation": hourly_precip,
                "precipitation_probability": hourly_rain_probability,
                "relative_humidity_2m": hourly_humidity,
                "weather_code": hourly_codes,
                "wind_speed_10m": hourly_wind,
            },
            "location": location_name or "Selected Location",
            "latitude": latitude,
            "longitude": longitude,
        }

    # ---------------------------------------------------------
    # GEOCODING
    # ---------------------------------------------------------
    def geocode_location(self, location):
        """
        Convert a city/location name into latitude and longitude.
        Uses Open-Meteo Geocoding API.
        """

        if not location or not location.strip():
            raise ValueError("Location cannot be empty.")

        location = location.strip()

        # First attempt:
        # Search exactly what the user entered.
        params = {
            "name": location,
            "count": 10,
            "language": "en",
            "format": "json"
        }

        try:
            response = requests.get(
                self.geocoding_base_url,
                params=params,
                timeout=self.timeout
            )

            response.raise_for_status()
            data = response.json()

        except (requests.RequestException, ValueError):
            fallback = self._fallback_location_data(location)
            if fallback:
                return fallback
            raise ValueError(
                "Unable to connect to location service."
            )

        results = data.get("results", [])

        # -----------------------------------------------------
        # SECOND ATTEMPT FOR INDIA
        # -----------------------------------------------------
        # Since this project is primarily intended for India,
        # try India-specific search if the first search fails.
        if not results:
            india_params = {
                "name": location,
                "count": 10,
                "language": "en",
                "format": "json",
                "countryCode": "IN"
            }

            try:
                response = requests.get(
                    self.geocoding_base_url,
                    params=india_params,
                    timeout=self.timeout
                )

                response.raise_for_status()
                data = response.json()

                results = data.get("results", [])

            except requests.RequestException:
                results = []

        if not results:
            fallback = self._fallback_location_data(location)
            if fallback:
                return fallback
            raise ValueError(
                f"Location '{location}' could not be found."
            )

        # -----------------------------------------------------
        # RESULT SELECTION
        # -----------------------------------------------------
        #
        # Prefer actual populated places instead of villages,
        # administrative regions, etc.
        #
        preferred_results = []

        preferred_feature_codes = {
            "PPLC",
            "PPLA",
            "PPLA2",
            "PPLA3",
            "PPLA4",
            "PPL"
        }

        for result in results:
            feature_code = str(
                result.get("feature_code", "")
            ).upper()

            if feature_code in preferred_feature_codes:
                preferred_results.append(result)

        if preferred_results:
            results = preferred_results

        # -----------------------------------------------------
        # TRY TO FIND AN EXACT NAME MATCH
        # -----------------------------------------------------
        exact_match = None

        for result in results:
            result_name = str(
                result.get("name", "")
            ).strip().lower()

            if result_name == location.lower():
                exact_match = result
                break

        result = exact_match if exact_match else results[0]

        # -----------------------------------------------------
        # COORDINATES
        # -----------------------------------------------------
        latitude = result.get("latitude")
        longitude = result.get("longitude")

        if not is_valid_coordinate(latitude, longitude):
            raise ValueError(
                "Invalid coordinates returned for location."
            )

        latitude = float(latitude)
        longitude = float(longitude)

        # -----------------------------------------------------
        # LOCATION INFORMATION
        # -----------------------------------------------------
        name = result.get("name") or location
        admin1 = result.get("admin1")
        admin2 = result.get("admin2")
        country = result.get("country")
        country_code = result.get("country_code")

        # Build a readable display name.
        display_parts = [name]

        if admin1:
            display_parts.append(admin1)

        if country:
            display_parts.append(country)

        display_name = ", ".join(display_parts)

        return {
            "name": name,
            "display_name": display_name,
            "latitude": latitude,
            "longitude": longitude,
            "country": country,
            "country_code": country_code,
            "admin1": admin1,
            "admin2": admin2,
            "timezone": result.get("timezone")
        }

    # ---------------------------------------------------------
    # WEATHER BY COORDINATES
    # ---------------------------------------------------------
    def get_weather_by_coordinates(
        self,
        latitude,
        longitude,
        location_name=None
    ):
        """
        Get current weather using latitude and longitude.
        """

        try:
            latitude = float(latitude)
            longitude = float(longitude)

        except (TypeError, ValueError):
            raise ValueError(
                "Latitude and longitude must be valid numbers."
            )

        if not is_valid_coordinate(latitude, longitude):
            raise ValueError(
                "Invalid latitude or longitude."
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

            "daily": ",".join([
                "weather_code",
                "temperature_2m_mean",
                "precipitation_sum",
                "precipitation_probability_max",
                "uv_index_max",
                "sunrise",
                "sunset"
            ]),

            "hourly": ",".join([
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "precipitation_probability",
                "weather_code",
                "wind_speed_10m"
            ]),

            "timezone": "auto",
            "forecast_days": 7
        }

        try:
            response = requests.get(
                self.weather_base_url,
                params=params,
                timeout=self.timeout
            )

            response.raise_for_status()
            data = response.json()

        except (requests.RequestException, ValueError):
            data = self._build_fallback_weather_response(
                latitude,
                longitude,
                location_name=(
                    location_name
                    or "Selected Location"
                )
            )

        return process_current_weather(
            data,
            location_name=(
                location_name
                or "Selected Location"
            ),
            latitude=latitude,
            longitude=longitude
        )

    # ---------------------------------------------------------
    # WEATHER BY LOCATION NAME
    # ---------------------------------------------------------
    def get_weather_by_location(self, location):
        """
        Search a city name, get coordinates, then retrieve weather.
        """

        location_data = self.geocode_location(location)

        return self.get_weather_by_coordinates(
            location_data["latitude"],
            location_data["longitude"],
            location_data.get("display_name")
            or location_data.get("name")
            or location
        )

    # ---------------------------------------------------------
    # RAW WEATHER DATA
    # ---------------------------------------------------------
    def get_raw_weather(self, latitude, longitude):
        """
        Get raw Open-Meteo weather response.
        Used by forecast and other backend services.
        """

        try:
            latitude = float(latitude)
            longitude = float(longitude)

        except (TypeError, ValueError):
            raise ValueError(
                "Latitude and longitude must be valid numbers."
            )

        if not is_valid_coordinate(latitude, longitude):
            raise ValueError(
                "Invalid latitude or longitude."
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

            "daily": ",".join([
                "weather_code",
                "temperature_2m_mean",
                "precipitation_sum",
                "precipitation_probability_max",
                "uv_index_max",
                "sunrise",
                "sunset"
            ]),

            "hourly": ",".join([
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "precipitation_probability",
                "weather_code",
                "wind_speed_10m"
            ]),

            "timezone": "auto",
            "forecast_days": 7
        }

        try:
            response = requests.get(
                self.weather_base_url,
                params=params,
                timeout=self.timeout
            )

            response.raise_for_status()
            return response.json()

        except (requests.RequestException, ValueError):
            return self._build_fallback_weather_response(
                latitude,
                longitude,
                location_name="Selected Location"
            )