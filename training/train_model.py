"""
training/train_model.py
Trains Logistic Regression, Decision Tree, and Random Forest.
Selects and saves the best model. Prints full evaluation report.
"""

import sys
import os
import joblib
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix
)

from preprocessing.preprocess import preprocess_pipeline, RISK_ORDER

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "lifestyle_dataset.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "random_forest_model.pkl")


MODELS = {
    "Logistic Regression": LogisticRegression(max_iter=500, random_state=42),
    "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=150, max_depth=8, random_state=42),
}


def train_and_evaluate():
    print("=" * 60)
    print("  HealthQuest AI — Model Training Pipeline")
    print("=" * 60)

    X_train, X_test, y_train, y_test, scaler, le = preprocess_pipeline(DATA_PATH)

    results = {}

    for name, model in MODELS.items():
        print(f"\n📊 Training: {name}")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        results[name] = {"model": model, "accuracy": acc, "y_pred": y_pred}

        print(f"   Accuracy: {acc * 100:.2f}%")
        print(f"\n   Classification Report:")
        print(classification_report(y_test, y_pred, target_names=RISK_ORDER))
        print(f"   Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

    # Select best model
    best_name = max(results, key=lambda k: results[k]["accuracy"])
    best_model = results[best_name]["model"]

    print("\n" + "=" * 60)
    print(f"  ✅ Best Model: {best_name}")
    print(f"  Accuracy: {results[best_name]['accuracy'] * 100:.2f}%")
    print("=" * 60)

    # Save model + scaler + label encoder together
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump({"model": best_model, "scaler": scaler, "label_encoder": le}, MODEL_PATH)
    print(f"\n💾 Model saved → {MODEL_PATH}")

    return results, best_name


if __name__ == "__main__":
    train_and_evaluate()
