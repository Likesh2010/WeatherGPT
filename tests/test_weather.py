import pytest

from backend.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True


def test_current_weather_missing_location(client):
    response = client.get("/api/weather/current")

    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False
    assert data["error"]["code"] == "MISSING_LOCATION"


def test_current_weather_by_location(client):
    response = client.get(
        "/api/weather/current?location=Chennai"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert "data" in data

    weather = data["data"]

    assert "temperature" in weather
    assert "humidity" in weather
    assert "wind_speed" in weather
    assert "risk" in weather


def test_current_weather_by_coordinates(client):
    response = client.get(
        "/api/weather/current"
        "?latitude=13.08&longitude=80.27"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert "data" in data