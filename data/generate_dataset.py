"""
generate_dataset.py
Generates a realistic synthetic lifestyle dataset for HealthQuest AI.
"""

import numpy as np
import pandas as pd

np.random.seed(42)
N = 450

def generate_dataset():
    sleep_hours = np.clip(np.random.normal(6.5, 1.5, N), 3, 10)
    screen_time = np.clip(np.random.normal(5, 2, N), 1, 12)
    physical_activity = np.clip(np.random.normal(45, 25, N), 0, 120)
    water_intake = np.clip(np.random.normal(2.0, 0.7, N), 0.5, 4.0)
    junk_food_frequency = np.clip(np.random.normal(3, 1.5, N), 0, 7)
    stress_level = np.clip(np.random.normal(5, 2.5, N), 1, 10)
    bmi = np.clip(np.random.normal(24, 4, N), 15, 40)
    age = np.clip(np.random.normal(32, 10, N), 18, 65).astype(int)

    # Risk scoring: higher = more risk
    risk_score = (
        (8 - sleep_hours) * 1.5
        + screen_time * 0.8
        + (120 - physical_activity) * 0.05
        + (4 - water_intake) * 2
        + junk_food_frequency * 1.2
        + stress_level * 1.0
        + np.where(bmi > 27, (bmi - 27) * 0.5, 0)
        + np.random.normal(0, 1, N)  # noise
    )

    # Bin into Low / Medium / High
    low = risk_score < np.percentile(risk_score, 33)
    high = risk_score > np.percentile(risk_score, 67)
    risk_level = np.where(low, "Low", np.where(high, "High", "Medium"))

    df = pd.DataFrame({
        "sleep_hours": np.round(sleep_hours, 1),
        "screen_time": np.round(screen_time, 1),
        "physical_activity": np.round(physical_activity, 0).astype(int),
        "water_intake": np.round(water_intake, 1),
        "junk_food_frequency": np.round(junk_food_frequency, 0).astype(int),
        "stress_level": np.round(stress_level, 1),
        "bmi": np.round(bmi, 1),
        "age": age,
        "risk_level": risk_level,
    })

    df.to_csv("lifestyle_dataset.csv", index=False)
    print(f"Dataset generated: {len(df)} rows")
    print(df["risk_level"].value_counts())
    return df

if __name__ == "__main__":
    generate_dataset()
