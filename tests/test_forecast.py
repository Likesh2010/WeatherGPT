import pytest

from backend.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_forecast_missing_location(client):
    response = client.get(
        "/api/weather/forecast"
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["success"] is False


def test_forecast_by_location(client):
    response = client.get(
        "/api/weather/forecast?location=Chennai"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert "data" in data


def test_forecast_by_coordinates(client):
    response = client.get(
        "/api/weather/forecast"
        "?latitude=13.08&longitude=80.27"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert "data" in data