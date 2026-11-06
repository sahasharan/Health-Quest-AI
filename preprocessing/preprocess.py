"""
preprocessing/preprocess.py
Reusable preprocessing pipeline for HealthQuest AI.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split


FEATURE_COLS = [
    "sleep_hours", "screen_time", "physical_activity",
    "water_intake", "junk_food_frequency", "stress_level",
    "bmi", "age",
]
TARGET_COL = "risk_level"
RISK_ORDER = ["Low", "Medium", "High"]


def load_data(csv_path: str) -> pd.DataFrame:
    """Load dataset from CSV."""
    df = pd.read_csv(csv_path)
    return df


def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing values with column medians (numerical) or mode (categorical)."""
    df = df.copy()
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(df[col].mode()[0])
    return df


def encode_target(df: pd.DataFrame):
    """Encode risk_level into ordinal integers: Low=0, Medium=1, High=2."""
    le = LabelEncoder()
    le.classes_ = np.array(RISK_ORDER)
    df = df.copy()
    df[TARGET_COL] = le.transform(df[TARGET_COL])
    return df, le


def scale_features(X_train, X_test):
    """Standardize numerical features using training statistics."""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler


def preprocess_pipeline(csv_path: str, test_size: float = 0.2, random_state: int = 42):
    """
    Full preprocessing pipeline.
    Returns: X_train, X_test, y_train, y_test, scaler, label_encoder
    """
    df = load_data(csv_path)
    df = handle_missing(df)
    df, le = encode_target(df)

    X = df[FEATURE_COLS].values
    y = df[TARGET_COL].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, le


def preprocess_single(input_dict: dict, scaler: StandardScaler) -> np.ndarray:
    """
    Preprocess a single user input dict for prediction.
    Keys must match FEATURE_COLS.
    """
    row = [input_dict[col] for col in FEATURE_COLS]
    return scaler.transform([row])
