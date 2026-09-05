class AlertService:
    """
    Generates WeatherGPT analysis alerts.

    These are NOT official government warnings.
    """

    def generate_alerts(
        self,
        weather,
        risk
    ):

        alerts = []


        risk_items = [

            (
                "heat",
                "Heat Alert"
            ),

            (
                "rain",
                "Heavy Rain Alert"
            ),

            (
                "wind",
                "Wind Alert"
            ),

            (
                "flood",
                "Flood Risk Alert"
            )

        ]


        for key, title in risk_items:

            risk_data = risk.get(
                key,
                {}
            )


            level = risk_data.get(
                "level",
                "UNKNOWN"
            )


            if level in [
                "HIGH",
                "EXTREME"
            ]:

                recommendation = (
                    self._recommendation(
                        key,
                        level
                    )
                )


                alerts.append({

                    "type": title,

                    "severity": level,

                    "message":
                        risk_data.get(
                            "description",
                            "Potential weather risk detected."
                        ),

                    "recommendation":
                        recommendation

                })


        return alerts


    def _recommendation(
        self,
        risk_type,
        level
    ):

        recommendations = {

            "heat":
                "Stay hydrated and limit prolonged exposure to extreme heat.",

            "rain":
                "Be prepared for heavy rainfall and avoid unnecessary travel in affected areas.",

            "wind":
                "Secure loose outdoor objects and avoid exposed areas during strong winds.",

            "flood":
                "Avoid flood-prone areas and follow official local safety instructions."

        }


        return recommendations.get(

            risk_type,

            "Monitor weather conditions and follow official guidance."

        )