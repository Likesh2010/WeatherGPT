class RiskAnalysisService:
    """
    Rule-based weather risk analysis.

    This is the initial WeatherGPT intelligence layer.
    An ML model can be integrated later.
    """


    def analyze_heat(
        self,
        temperature,
        feels_like
    ):

        temperature = (
            feels_like
            if feels_like is not None
            else temperature
        )


        if temperature is None:

            return {

                "level": "UNKNOWN",

                "score": None,

                "description":
                    "Insufficient temperature data."

            }


        if temperature >= 45:

            return {

                "level": "EXTREME",

                "score": 100,

                "description":
                    "Extreme heat conditions detected."

            }


        if temperature >= 40:

            return {

                "level": "HIGH",

                "score": 80,

                "description":
                    "High heat conditions detected."

            }


        if temperature >= 35:

            return {

                "level": "MODERATE",

                "score": 55,

                "description":
                    "Moderate heat conditions detected."

            }


        return {

            "level": "LOW",

            "score": 20,

            "description":
                "No significant heat risk detected."

        }


    def analyze_rain(
        self,
        precipitation,
        rain_probability
    ):

        precipitation = (
            precipitation or 0
        )

        rain_probability = (
            rain_probability or 0
        )


        if (
            precipitation >= 50
            or rain_probability >= 90
        ):

            return {

                "level": "EXTREME",

                "score": 95,

                "description":
                    "Very high rainfall potential detected."

            }


        if (
            precipitation >= 25
            or rain_probability >= 70
        ):

            return {

                "level": "HIGH",

                "score": 75,

                "description":
                    "High rainfall potential detected."

            }


        if (
            precipitation >= 10
            or rain_probability >= 50
        ):

            return {

                "level": "MODERATE",

                "score": 50,

                "description":
                    "Moderate rainfall potential detected."

            }


        return {

            "level": "LOW",

            "score": 15,

            "description":
                "No significant rainfall risk detected."

        }


    def analyze_wind(
        self,
        wind_speed
    ):

        if wind_speed is None:

            return {

                "level": "UNKNOWN",

                "score": None,

                "description":
                    "Insufficient wind data."

            }


        if wind_speed >= 90:

            return {

                "level": "EXTREME",

                "score": 100,

                "description":
                    "Extremely strong winds detected."

            }


        if wind_speed >= 35:

            return {

                "level": "HIGH",

                "score": 80,

                "description":
                    "Strong winds detected."

            }


        if wind_speed >= 20:

            return {

                "level": "MODERATE",

                "score": 50,

                "description":
                    "Moderately strong winds detected."

            }


        return {

            "level": "LOW",

            "score": 15,

            "description":
                "No significant wind risk detected."

        }


    def analyze_flood(
        self,
        precipitation,
        rain_probability
    ):

        if (
            precipitation is None
            and
            rain_probability is None
        ):

            return {

                "level": "UNKNOWN",

                "score": None,

                "description":
                    "Insufficient data for flood-risk assessment."

            }


        precipitation = (
            precipitation or 0
        )

        rain_probability = (
            rain_probability or 0
        )


        if precipitation >= 50:

            return {

                "level": "HIGH",

                "score": 80,

                "description":
                    "Heavy precipitation may increase local flood risk."

            }


        if precipitation >= 25:

            return {

                "level": "MODERATE",

                "score": 50,

                "description":
                    "Moderate precipitation may contribute to localized flooding."

            }


        return {

            "level": "LOW",

            "score": 15,

            "description":
                "No significant precipitation-based flood signal detected."

        }


    def analyze(
        self,
        weather,
        forecast=None
    ):
        """
        Perform complete risk analysis.
        """

        heat = self.analyze_heat(

            weather.get(
                "temperature"
            ),

            weather.get(
                "feels_like"
            )

        )


        rain = self.analyze_rain(

            weather.get(
                "precipitation"
            ),

            weather.get(
                "rain_probability"
            )

        )


        wind = self.analyze_wind(

            weather.get(
                "wind_speed"
            )

        )


        flood = self.analyze_flood(

            weather.get(
                "precipitation"
            ),

            weather.get(
                "rain_probability"
            )

        )


        scores = [

            item["score"]

            for item in [
                heat,
                rain,
                wind,
                flood
            ]

            if item["score"] is not None

        ]


        if not scores:

            overall = {

                "level": "UNKNOWN",

                "score": None

            }

        else:

            score = max(scores)


            if score >= 90:

                level = "EXTREME"

            elif score >= 70:

                level = "HIGH"

            elif score >= 40:

                level = "MODERATE"

            else:

                level = "LOW"


            overall = {

                "level": level,

                "score": round(
                    score,
                    2
                )

            }


        return {

            "overall": overall,

            "heat": heat,

            "rain": rain,

            "wind": wind,

            "flood": flood

        }