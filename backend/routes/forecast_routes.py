from flask import Blueprint, request, jsonify

from backend.services.weather_api import WeatherAPIService
from backend.services.forecast_service import ForecastService


# Create Blueprint
forecast_bp = Blueprint(
    "forecast",
    __name__,
    url_prefix="/api/weather"
)


# Initialize services
weather_service = WeatherAPIService()
forecast_service = ForecastService()


@forecast_bp.route("/forecast", methods=["GET"])
def get_forecast():
    """
    Get weather forecast.

    Supported requests:

    /api/weather/forecast?location=Chennai

    OR

    /api/weather/forecast?latitude=13.08&longitude=80.27
    """

    try:

        # --------------------------------
        # Get query parameters
        # --------------------------------

        location = request.args.get("location")

        latitude = request.args.get("latitude")

        longitude = request.args.get("longitude")


        # --------------------------------
        # Location-based request
        # --------------------------------

        if location:

            location_data = (
                weather_service
                .geocode_location(
                    location
                )
            )


            latitude = (
                location_data["latitude"]
            )

            longitude = (
                location_data["longitude"]
            )


        # --------------------------------
        # Validate coordinates
        # --------------------------------

        if (
            latitude is None
            or
            longitude is None
        ):

            return jsonify({

                "success": False,

                "error": {

                    "code":
                        "MISSING_COORDINATES",

                    "message":
                        "Please provide a location or latitude and longitude."

                }

            }), 400


        # --------------------------------
        # Get forecast
        # --------------------------------

        forecast = (
            forecast_service
            .get_forecast(
                latitude,
                longitude
            )
        )


        # --------------------------------
        # Successful Response
        # --------------------------------

        return jsonify({

            "success": True,

            "data": forecast

        }), 200


    # --------------------------------
    # Invalid input
    # --------------------------------

    except ValueError as error:

        return jsonify({

            "success": False,

            "error": {

                "code": "INVALID_LOCATION",

                "message": str(error)

            }

        }), 400


    # --------------------------------
    # Unexpected error
    # --------------------------------

    except Exception as error:

        print(
            f"Forecast route error: {error}"
        )

        return jsonify({

            "success": False,

            "error": {

                "code": "FORECAST_ERROR",

                "message":
                    "Unable to retrieve forecast data."

            }

        }), 500