from backend.services.weather_api import (
    WeatherAPIService
)

from backend.utils.data_processing import (
    process_forecast
)


class ForecastService:

    def __init__(self):

        self.weather_api = (
            WeatherAPIService()
        )


    def get_forecast(
        self,
        latitude,
        longitude
    ):
        """
        Retrieve and process forecast data.
        """

        raw_data = (
            self.weather_api.get_raw_weather(
                latitude,
                longitude
            )
        )


        return process_forecast(
            raw_data
        )