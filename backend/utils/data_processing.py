from backend.utils.helpers import safe_get


WEATHER_CODES = {

    0: "Clear sky",

    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",

    45: "Fog",
    48: "Depositing rime fog",

    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",

    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",

    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",

    66: "Light freezing rain",
    67: "Heavy freezing rain",

    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",

    77: "Snow grains",

    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",

    85: "Slight snow showers",
    86: "Heavy snow showers",

    95: "Thunderstorm",

    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}


def weather_code_to_condition(code):
    """
    Convert WMO weather code into readable text.
    """

    try:

        code = int(code)

    except (TypeError, ValueError):

        return "Unknown"

    return WEATHER_CODES.get(
        code,
        "Unknown"
    )


def weather_code_to_icon(code):
    """
    Return a simple icon based on weather condition.

    These are emoji placeholders for the initial version.
    They can later be replaced with real weather icon assets.
    """

    try:

        code = int(code)

    except (TypeError, ValueError):

        return "🌤️"

    if code == 0:
        return "☀️"

    if code in [1, 2]:
        return "🌤️"

    if code == 3:
        return "☁️"

    if code in [45, 48]:
        return "🌫️"

    if 51 <= code <= 57:
        return "🌦️"

    if 61 <= code <= 67:
        return "🌧️"

    if 71 <= code <= 77:
        return "❄️"

    if 80 <= code <= 82:
        return "🌧️"

    if 85 <= code <= 86:
        return "🌨️"

    if code >= 95:
        return "⛈️"

    return "🌤️"


def process_current_weather(
    api_data,
    location_name,
    latitude,
    longitude
):
    """
    Convert Open-Meteo current weather
    response into WeatherGPT format.
    """

    current = safe_get(
        api_data,
        "current",
        {}
    )

    daily = safe_get(
        api_data,
        "daily",
        {}
    )

    weather_code = safe_get(
        current,
        "weather_code"
    )

    sunrise = None
    sunset = None

    sunrise_values = safe_get(
        daily,
        "sunrise",
        []
    )

    sunset_values = safe_get(
        daily,
        "sunset",
        []
    )

    if sunrise_values:
        sunrise = sunrise_values[0]

    if sunset_values:
        sunset = sunset_values[0]

    return {

        "location": location_name,

        "latitude": latitude,
        "longitude": longitude,

        "timestamp": safe_get(
            current,
            "time"
        ),

        "temperature": safe_get(
            current,
            "temperature_2m"
        ),

        "feels_like": safe_get(
            current,
            "apparent_temperature"
        ),

        "condition":
            weather_code_to_condition(
                weather_code
            ),

        "icon":
            weather_code_to_icon(
                weather_code
            ),

        "humidity": safe_get(
            current,
            "relative_humidity_2m"
        ),

        "pressure": safe_get(
            current,
            "surface_pressure"
        ),

        "wind_speed": safe_get(
            current,
            "wind_speed_10m"
        ),

        "wind_direction": safe_get(
            current,
            "wind_direction_10m"
        ),

        "precipitation": safe_get(
            current,
            "precipitation"
        ),

        "visibility": safe_get(
            current,
            "visibility"
        ),

        "uv": (
            safe_get(
                daily,
                "uv_index_max",
                [None]
            )[0]
            if safe_get(
                daily,
                "uv_index_max"
            )
            else None
        ),

        "sunrise": sunrise,
        "sunset": sunset
    }


def process_forecast(api_data):
    """
    Convert API forecast data into
    frontend-friendly format.
    """

    hourly = safe_get(
        api_data,
        "hourly",
        {}
    )

    daily = safe_get(
        api_data,
        "daily",
        {}
    )

    hourly_times = safe_get(
        hourly,
        "time",
        []
    )

    temperatures = safe_get(
        hourly,
        "temperature_2m",
        []
    )

    precipitation = safe_get(
        hourly,
        "precipitation",
        []
    )

    rain_probability = safe_get(
        hourly,
        "precipitation_probability",
        []
    )

    humidity = safe_get(
        hourly,
        "relative_humidity_2m",
        []
    )

    wind_speed = safe_get(
        hourly,
        "wind_speed_10m",
        []
    )

    weather_codes = safe_get(
        hourly,
        "weather_code",
        []
    )

    hourly_forecast = []

    for index, timestamp in enumerate(
        hourly_times
    ):

        item = {

            "timestamp": timestamp,

            "temperature":
                temperatures[index]
                if index < len(temperatures)
                else None,

            "precipitation":
                precipitation[index]
                if index < len(precipitation)
                else None,

            "rain_probability":
                rain_probability[index]
                if index < len(rain_probability)
                else None,

            "humidity":
                humidity[index]
                if index < len(humidity)
                else None,

            "wind_speed":
                wind_speed[index]
                if index < len(wind_speed)
                else None,

            "condition":
                weather_code_to_condition(
                    weather_codes[index]
                )
                if index < len(weather_codes)
                else "Unknown",

            "icon":
                weather_code_to_icon(
                    weather_codes[index]
                )
                if index < len(weather_codes)
                else "🌤️"
        }

        hourly_forecast.append(
            item
        )


    daily_times = safe_get(
        daily,
        "time",
        []
    )

    daily_temperature = safe_get(
        daily,
        "temperature_2m_mean",
        []
    )

    daily_rain = safe_get(
        daily,
        "precipitation_sum",
        []
    )

    daily_rain_probability = safe_get(
        daily,
        "precipitation_probability_max",
        []
    )

    daily_weather_codes = safe_get(
        daily,
        "weather_code",
        []
    )


    daily_forecast = []


    for index, date in enumerate(
        daily_times
    ):

        item = {

            "date": date,

            "temperature":
                daily_temperature[index]
                if index < len(daily_temperature)
                else None,

            "precipitation":
                daily_rain[index]
                if index < len(daily_rain)
                else None,

            "rain_probability":
                daily_rain_probability[index]
                if index < len(daily_rain_probability)
                else None,

            "condition":
                weather_code_to_condition(
                    daily_weather_codes[index]
                )
                if index < len(daily_weather_codes)
                else "Unknown",

            "icon":
                weather_code_to_icon(
                    daily_weather_codes[index]
                )
                if index < len(daily_weather_codes)
                else "🌤️"
        }

        daily_forecast.append(
            item
        )


    return {

        "hourly": hourly_forecast,

        "daily": daily_forecast

    }