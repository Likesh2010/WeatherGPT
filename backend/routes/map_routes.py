from flask import Blueprint, request, jsonify

from backend.services.weather_api import WeatherAPIService


map_bp = Blueprint(
    "map",
    __name__,
    url_prefix="/api/weather"
)

weather_service = WeatherAPIService()


@map_bp.route("/map", methods=["GET"])
def get_map_weather():

    try:

        location = request.args.get("location")

        latitude = request.args.get("latitude")
        longitude = request.args.get("longitude")

        # =====================================================
        # LOCATION NAME SEARCH
        # =====================================================

        if location:

            location = location.strip()

            if not location:
                return jsonify({
                    "success": False,
                    "error": {
                        "code": "EMPTY_LOCATION",
                        "message": "Please enter a location."
                    }
                }), 400

            location_data = weather_service.geocode_location(
                location
            )

            latitude = location_data["latitude"]
            longitude = location_data["longitude"]

            location_name = (
                location_data.get("display_name")
                or location_data.get("name")
                or location
            )

        # =====================================================
        # COORDINATE SEARCH
        # =====================================================

        elif latitude is not None and longitude is not None:

            try:
                latitude = float(latitude)
                longitude = float(longitude)

            except (TypeError, ValueError):

                return jsonify({
                    "success": False,
                    "error": {
                        "code": "INVALID_COORDINATES",
                        "message": "Invalid latitude or longitude."
                    }
                }), 400

            location_name = "Selected Location"

        # =====================================================
        # NOTHING PROVIDED
        # =====================================================

        else:

            return jsonify({
                "success": False,
                "error": {
                    "code": "MISSING_LOCATION",
                    "message": (
                        "Please provide a location or "
                        "latitude and longitude."
                    )
                }
            }), 400

        # =====================================================
        # GET WEATHER
        # =====================================================

        weather = weather_service.get_weather_by_coordinates(
            latitude,
            longitude,
            location_name
        )

        # =====================================================
        # RESPONSE
        # =====================================================

        return jsonify({
            "success": True,
            "data": {
                "location": weather.get(
                    "location",
                    location_name
                ),

                "latitude": weather.get(
                    "latitude",
                    latitude
                ),

                "longitude": weather.get(
                    "longitude",
                    longitude
                ),

                "temperature": weather.get(
                    "temperature"
                ),

                "condition": weather.get(
                    "condition"
                ),

                "icon": weather.get(
                    "icon"
                ),

                "humidity": weather.get(
                    "humidity"
                ),

                "wind_speed": weather.get(
                    "wind_speed"
                )
            }
        }), 200

    # =========================================================
    # INVALID LOCATION
    # =========================================================

    except ValueError as error:

        print(f"Map validation error: {error}")

        return jsonify({
            "success": False,
            "error": {
                "code": "INVALID_LOCATION",
                "message": str(error)
            }
        }), 400

    # =========================================================
    # UNEXPECTED ERROR
    # =========================================================

    except Exception as error:

        print(f"Map route error: {error}")

        return jsonify({
            "success": False,
            "error": {
                "code": "MAP_ERROR",
                "message": (
                    "Unable to find weather information."
                )
            }
        }), 500