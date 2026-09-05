from backend.services.risk_analysis import RiskAnalysisService


def create_service():
    return RiskAnalysisService()


def test_low_risk_weather():

    service = create_service()

    weather = {
        "temperature": 25,
        "feels_like": 26,
        "humidity": 50,
        "wind_speed": 10,
        "precipitation": 0,
        "rain_probability": 5,
        "visibility": 10
    }

    result = service.analyze(weather)

    assert "overall" in result
    assert result["overall"]["level"] == "LOW"


def test_high_heat_risk():

    service = create_service()

    weather = {
        "temperature": 42,
        "feels_like": 48,
        "humidity": 80,
        "wind_speed": 10,
        "precipitation": 0,
        "rain_probability": 5,
        "visibility": 10
    }

    result = service.analyze(weather)

    assert result["heat"]["level"] in [
        "HIGH",
        "EXTREME"
    ]


def test_high_rain_risk():

    service = create_service()

    weather = {
        "temperature": 30,
        "feels_like": 32,
        "humidity": 85,
        "wind_speed": 15,
        "precipitation": 40,
        "rain_probability": 90,
        "visibility": 5
    }

    result = service.analyze(weather)

    assert result["rain"]["level"] in [
        "HIGH",
        "EXTREME"
    ]


def test_high_wind_risk():

    service = create_service()

    weather = {
        "temperature": 28,
        "feels_like": 29,
        "humidity": 60,
        "wind_speed": 35,
        "precipitation": 0,
        "rain_probability": 10,
        "visibility": 10
    }

    result = service.analyze(weather)

    assert result["wind"]["level"] in [
        "HIGH",
        "EXTREME"
    ]


def test_risk_contains_overall():

    service = create_service()

    weather = {
        "temperature": 30,
        "feels_like": 32,
        "humidity": 60,
        "wind_speed": 10,
        "precipitation": 0,
        "rain_probability": 10,
        "visibility": 10
    }

    result = service.analyze(weather)

    assert "overall" in result
    assert "level" in result["overall"]
    assert "score" in result["overall"]