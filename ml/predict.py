import os

import pandas as pd

from joblib import load


# ---------------------------------------
# Paths
# ---------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "model.pkl"
)


# ---------------------------------------
# Required features
# ---------------------------------------

FEATURE_COLUMNS = [

    "temperature",

    "feels_like",

    "humidity",

    "pressure",

    "wind_speed",

    "precipitation",

    "rain_probability",

    "visibility",

    "heat_humidity_index",

    "heavy_rain_indicator",

    "strong_wind_indicator"

]


# ---------------------------------------
# Load Model
# ---------------------------------------

def load_model():

    if not os.path.exists(
        MODEL_PATH
    ):

        raise FileNotFoundError(

            "ML model not found. "
            "Run 'python ml/train.py' first."

        )


    return load(
        MODEL_PATH
    )


# ---------------------------------------
# Feature Engineering
# ---------------------------------------

def prepare_input(weather):

    temperature = (
        weather.get(
            "temperature"
        )
        or 0
    )


    humidity = (
        weather.get(
            "humidity"
        )
        or 0
    )


    precipitation = (
        weather.get(
            "precipitation"
        )
        or 0
    )


    wind_speed = (
        weather.get(
            "wind_speed"
        )
        or 0
    )


    heat_humidity_index = (

        temperature

        +
        
        (
            humidity
            * 0.05
        )

    )


    heavy_rain_indicator = int(

        precipitation >= 25

    )


    strong_wind_indicator = int(

        wind_speed >= 40

    )


    features = {

        "temperature":
            temperature,

        "feels_like":
            weather.get(
                "feels_like"
            ),

        "humidity":
            humidity,

        "pressure":
            weather.get(
                "pressure"
            ),

        "wind_speed":
            wind_speed,

        "precipitation":
            precipitation,

        "rain_probability":
            weather.get(
                "rain_probability"
            ),

        "visibility":
            weather.get(
                "visibility"
            ),

        "heat_humidity_index":
            heat_humidity_index,

        "heavy_rain_indicator":
            heavy_rain_indicator,

        "strong_wind_indicator":
            strong_wind_indicator

    }


    return pd.DataFrame(
        [features]
    )[FEATURE_COLUMNS]


# ---------------------------------------
# Predict Risk
# ---------------------------------------

def predict_risk(weather):

    model = load_model()


    features = prepare_input(
        weather
    )


    prediction = model.predict(
        features
    )[0]


    # Probability
    probabilities = (
        model.predict_proba(
            features
        )[0]
    )


    classes = (
        model.classes_
    )


    probability_map = {

        str(label):
            round(
                float(probability),
                4
            )

        for label, probability
        in zip(
            classes,
            probabilities
        )

    }


    confidence = max(
        probability_map.values()
    )


    return {

        "risk_level":
            str(prediction),

        "confidence":
            round(
                confidence,
                4
            ),

        "probabilities":
            probability_map

    }


# ---------------------------------------
# Test Prediction
# ---------------------------------------

if __name__ == "__main__":

    sample_weather = {

        "temperature": 37,

        "feels_like": 40,

        "humidity": 75,

        "pressure": 1005,

        "wind_speed": 20,

        "precipitation": 12,

        "rain_probability": 60,

        "visibility": 8

    }


    result = predict_risk(
        sample_weather
    )


    print(
        "\nWeatherGPT ML Prediction:"
    )


    print(result)