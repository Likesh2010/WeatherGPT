from flask import Blueprint, request, jsonify

from backend.services.weather_api import WeatherAPIService
from backend.services.risk_analysis import RiskAnalysisService


# Create Blueprint
weather_bp = Blueprint(
    "weather",
    __name__,
    url_prefix="/api/weather"
)


# Initialize services
weather_service = WeatherAPIService()
risk_service = RiskAnalysisService()


@weather_bp.route("/current", methods=["GET"])
def get_current_weather():
    """
    Get current weather information.

    Supported requests:

    /api/weather/current?location=Chennai

    OR

    /api/weather/current?latitude=13.08&longitude=80.27
    """

    try:

        # Get query parameters
        location = request.args.get("location")

        latitude = request.args.get("latitude")

        longitude = request.args.get("longitude")


        # --------------------------------
        # Location-based request
        # --------------------------------

        if location:

            weather = (
                weather_service
                .get_weather_by_location(
                    location
                )
            )


        # --------------------------------
        # Coordinate-based request
        # --------------------------------

        elif (
            latitude is not None
            and
            longitude is not None
        ):

            weather = (
                weather_service
                .get_weather_by_coordinates(
                    latitude,
                    longitude
                )
            )


        # --------------------------------
        # Missing parameters
        # --------------------------------

        else:

            return jsonify({

                "success": False,

                "error": {

                    "code": "MISSING_LOCATION",

                    "message":
                        "Please provide a location or latitude and longitude."

                }

            }), 400


        # --------------------------------
        # Weather Risk Analysis
        # --------------------------------

        risk = risk_service.analyze(
            weather
        )


        # Add risk information
        # to weather response

        weather["risk"] = risk


        # --------------------------------
        # Successful Response
        # --------------------------------

        return jsonify({

            "success": True,

            "data": weather

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
            f"Weather route error: {error}"
        )

        return jsonify({

            "success": False,

            "error": {

                "code": "WEATHER_API_ERROR",

                "message":
                    "Unable to retrieve current weather data."

            }

        }), 500