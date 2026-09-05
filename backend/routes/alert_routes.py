from flask import Blueprint, request, jsonify

from backend.services.weather_api import (
    WeatherAPIService
)

from backend.services.risk_analysis import (
    RiskAnalysisService
)

from backend.services.alert_service import (
    AlertService
)


alert_bp = Blueprint(
    "alerts",
    __name__,
    url_prefix="/api/weather"
)


weather_service = (
    WeatherAPIService()
)

risk_service = (
    RiskAnalysisService()
)

alert_service = (
    AlertService()
)


@alert_bp.route(
    "/alerts",
    methods=["GET"]
)
def alerts():

    try:

        latitude = request.args.get(
            "latitude"
        )

        longitude = request.args.get(
            "longitude"
        )

        location = request.args.get(
            "location"
        )


        if location:

            weather = (
                weather_service
                .get_weather_by_location(
                    location
                )
            )

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

        else:

            return jsonify({

                "success": False,

                "error": {

                    "code":
                        "MISSING_LOCATION",

                    "message":
                        "Location or coordinates are required."

                }

            }), 400


        risk = (
            risk_service.analyze(
                weather
            )
        )


        alerts = (
            alert_service.generate_alerts(
                weather,
                risk
            )
        )


        return jsonify({

            "success": True,

            "data": {

                "alerts": alerts,

                "official_alerts": [],

                "notice":
                    "These alerts are WeatherGPT analysis and are not official government warnings."

            }

        })


    except Exception as error:

        print(
            f"Alert error: {error}"
        )


        return jsonify({

            "success": False,

            "error": {

                "code":
                    "ALERT_ERROR",

                "message":
                    "Unable to generate weather alerts."

            }

        }), 500