import pandas as pd
import numpy as np


# Features used by the ML model
FEATURE_COLUMNS = [
    "temperature",
    "feels_like",
    "humidity",
    "pressure",
    "wind_speed",
    "precipitation",
    "rain_probability",
    "visibility"
]


TARGET_COLUMN = "risk_level"


def load_dataset(file_path):
    """
    Load weather dataset from CSV.
    """

    df = pd.read_csv(file_path)

    return df


def clean_dataset(df):
    """
    Clean and prepare the weather dataset.
    """

    df = df.copy()

    # Remove completely empty rows
    df = df.dropna(
        how="all"
    )

    # Convert numeric columns
    for column in FEATURE_COLUMNS:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )


    # Remove rows where target is missing
    if TARGET_COLUMN in df.columns:

        df = df.dropna(
            subset=[TARGET_COLUMN]
        )


    # Fill numerical missing values
    for column in FEATURE_COLUMNS:

        if column in df.columns:

            median_value = df[column].median()

            df[column] = df[column].fillna(
                median_value
            )


    return df


def create_features(df):
    """
    Create additional weather features.
    """

    df = df.copy()


    # Heat index proxy
    if (
        "temperature" in df.columns
        and
        "humidity" in df.columns
    ):

        df["heat_humidity_index"] = (
            df["temperature"]
            +
            (df["humidity"] * 0.05)
        )


    # Rain intensity indicator
    if "precipitation" in df.columns:

        df["heavy_rain_indicator"] = (
            df["precipitation"] >= 25
        ).astype(int)


    # Strong wind indicator
    if "wind_speed" in df.columns:

        df["strong_wind_indicator"] = (
            df["wind_speed"] >= 40
        ).astype(int)


    return df


def prepare_training_data(
    df
):
    """
    Prepare X and y for training.
    """

    df = clean_dataset(df)

    df = create_features(df)


    # Additional engineered features
    feature_columns = FEATURE_COLUMNS.copy()


    if "heat_humidity_index" in df.columns:

        feature_columns.append(
            "heat_humidity_index"
        )


    if "heavy_rain_indicator" in df.columns:

        feature_columns.append(
            "heavy_rain_indicator"
        )


    if "strong_wind_indicator" in df.columns:

        feature_columns.append(
            "strong_wind_indicator"
        )


    # Check required columns
    missing_columns = [

        column

        for column in feature_columns

        if column not in df.columns

    ]


    if missing_columns:

        raise ValueError(
            "Missing required columns: "
            +
            ", ".join(missing_columns)
        )


    if TARGET_COLUMN not in df.columns:

        raise ValueError(
            f"Dataset must contain "
            f"'{TARGET_COLUMN}' column."
        )


    X = df[
        feature_columns
    ]

    y = df[
        TARGET_COLUMN
    ]


    return X, y, feature_columns