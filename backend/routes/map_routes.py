from flask import Blueprint, request, jsonify

from backend.services.weather_api import (
    WeatherAPIService
)


map_bp = Blueprint(
    "map",
    __name__,
    url_prefix="/api/weather"
)


weather_service = (
    WeatherAPIService()
)


@map_bp.route(
    "/map",
    methods=["GET"]
)
def map_weather():

    try:

        latitude = request.args.get(
            "latitude"
        )

        longitude = request.args.get(
            "longitude"
        )


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
                        "Latitude and longitude are required."

                }

            }), 400


        weather = (
            weather_service
            .get_weather_by_coordinates(
                latitude,
                longitude
            )
        )


        return jsonify({

            "success": True,

            "data": {

                "location":
                    weather.get(
                        "location"
                    ),

                "latitude":
                    weather.get(
                        "latitude"
                    ),

                "longitude":
                    weather.get(
                        "longitude"
                    ),

                "temperature":
                    weather.get(
                        "temperature"
                    ),

                "condition":
                    weather.get(
                        "condition"
                    ),

                "supported_layers": [

                    "standard_map"

                ]

            }

        })


    except Exception as error:

        print(
            f"Map error: {error}"
        )


        return jsonify({

            "success": False,

            "error": {

                "code":
                    "MAP_ERROR",

                "message":
                    "Unable to retrieve map weather information."

            }

        }), 500