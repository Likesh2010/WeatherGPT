from datetime import datetime


def safe_get(data, key, default=None):
    """
    Safely retrieve a value from a dictionary.
    """

    if not isinstance(data, dict):
        return default

    return data.get(key, default)


def is_valid_coordinate(latitude, longitude):
    """
    Validate latitude and longitude.
    """

    try:

        latitude = float(latitude)
        longitude = float(longitude)

    except (TypeError, ValueError):

        return False

    return (
        -90 <= latitude <= 90
        and
        -180 <= longitude <= 180
    )


def parse_float(value, default=None):
    """
    Safely convert a value to float.
    """

    try:
        return float(value)

    except (TypeError, ValueError):

        return default


def format_api_error(message):
    """
    Create a consistent API error response.
    """

    return {
        "success": False,
        "error": {
            "message": message
        }
    }


def current_timestamp():
    """
    Return current UTC timestamp.
    """

    return datetime.utcnow().isoformat() + "Z"