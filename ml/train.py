import os
import json

import pandas as pd

from sklearn.model_selection import (
    train_test_split
)

from sklearn.ensemble import (
    RandomForestClassifier
)

from sklearn.pipeline import (
    Pipeline
)

from sklearn.impute import (
    SimpleImputer
)

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from joblib import dump

from ml.preprocessing import (
    prepare_training_data
)


# ---------------------------------------
# Paths
# ---------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


DATASET_PATH = os.path.join(
    BASE_DIR,
    "data",
    "sample_weather_data.csv"
)


MODEL_DIR = os.path.join(
    BASE_DIR,
    "ml"
)


MODEL_PATH = os.path.join(
    MODEL_DIR,
    "model.pkl"
)


METRICS_PATH = os.path.join(
    MODEL_DIR,
    "model_metrics.json"
)


# ---------------------------------------
# Main Training Function
# ---------------------------------------

def train_model():

    print("=" * 60)

    print(
        "WeatherGPT ML Training"
    )

    print("=" * 60)


    # -----------------------------------
    # Load dataset
    # -----------------------------------

    print(
        "\nLoading dataset..."
    )


    df = pd.read_csv(
        DATASET_PATH
    )


    print(
        f"Dataset size: {df.shape}"
    )


    # -----------------------------------
    # Prepare data
    # -----------------------------------

    print(
        "\nPreparing features..."
    )


    X, y, feature_columns = (
        prepare_training_data(
            df
        )
    )


    print(
        f"Features: {feature_columns}"
    )


    print(
        f"Classes: {sorted(y.unique())}"
    )


    # -----------------------------------
    # Train/test split
    # -----------------------------------

    X_train, X_test, y_train, y_test = (
        train_test_split(

            X,
            y,

            test_size=0.2,

            random_state=42,

            stratify=y
        )
    )


    # -----------------------------------
    # Create ML pipeline
    # -----------------------------------

    model = Pipeline([

        (
            "imputer",

            SimpleImputer(
                strategy="median"
            )
        ),

        (
            "classifier",

            RandomForestClassifier(

                n_estimators=200,

                max_depth=12,

                random_state=42,

                class_weight="balanced"
            )
        )

    ])


    # -----------------------------------
    # Train
    # -----------------------------------

    print(
        "\nTraining Random Forest..."
    )


    model.fit(
        X_train,
        y_train
    )


    # -----------------------------------
    # Evaluate
    # -----------------------------------

    predictions = model.predict(
        X_test
    )


    accuracy = accuracy_score(
        y_test,
        predictions
    )


    print(
        f"\nAccuracy: {accuracy:.4f}"
    )


    print(
        "\nClassification Report:"
    )


    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )


    # -----------------------------------
    # Confusion Matrix
    # -----------------------------------

    matrix = confusion_matrix(
        y_test,
        predictions
    )


    # -----------------------------------
    # Save model
    # -----------------------------------

    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )


    dump(
        model,
        MODEL_PATH
    )


    print(
        f"\nModel saved to:"
        f"\n{MODEL_PATH}"
    )


    # -----------------------------------
    # Save metadata
    # -----------------------------------

    metrics = {

        "accuracy": accuracy,

        "features": feature_columns,

        "classes":
            sorted(
                y.unique()
            ),

        "training_samples":
            len(X_train),

        "testing_samples":
            len(X_test),

        "confusion_matrix":
            matrix.tolist()

    }


    with open(
        METRICS_PATH,
        "w"
    ) as file:

        json.dump(
            metrics,
            file,
            indent=4
        )


    print(
        f"Metrics saved to:"
        f"\n{METRICS_PATH}"
    )


    print(
        "\nTraining completed."
    )


# ---------------------------------------
# Run
# ---------------------------------------

if __name__ == "__main__":

    train_model()