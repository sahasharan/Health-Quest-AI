"""
scoring/health_score.py
Transparent health scoring engine for HealthQuest AI.
Each lifestyle dimension contributes a weighted sub-score (total = 100).
"""

from dataclasses import dataclass


@dataclass
class ScoreBreakdown:
    sleep_score: float
    activity_score: float
    diet_score: float
    hydration_score: float
    screen_score: float
    stress_score: float
    total: float


def calculate_health_score(inputs: dict) -> ScoreBreakdown:
    """
    Calculates a 0–100 health score from user lifestyle inputs.

    Dimensions (max points):
      Sleep         → 20
      Activity      → 20
      Diet quality  → 20
      Hydration     → 15
      Screen time   → 12
      Stress        → 13
    """

    # ── Sleep (20 pts) ──────────────────────────────────────────
    sleep = inputs["sleep_hours"]
    if sleep >= 7.5:
        sleep_score = 20
    elif sleep >= 6.5:
        sleep_score = 15
    elif sleep >= 5.5:
        sleep_score = 9
    else:
        sleep_score = 3

    # ── Physical Activity (20 pts, minutes/day) ─────────────────
    activity = inputs["physical_activity"]
    if activity >= 60:
        activity_score = 20
    elif activity >= 40:
        activity_score = 16
    elif activity >= 20:
        activity_score = 10
    else:
        activity_score = 3

    # ── Diet / Junk Food (20 pts, days/week with junk) ─────────
    junk = inputs["junk_food_frequency"]
    if junk <= 1:
        diet_score = 20
    elif junk <= 2:
        diet_score = 16
    elif junk <= 4:
        diet_score = 10
    else:
        diet_score = 3

    # ── Hydration / Water Intake (15 pts, litres/day) ──────────
    water = inputs["water_intake"]
    if water >= 3.0:
        hydration_score = 15
    elif water >= 2.0:
        hydration_score = 11
    elif water >= 1.5:
        hydration_score = 7
    else:
        hydration_score = 2

    # ── Screen Time (12 pts, hours/day) ────────────────────────
    screen = inputs["screen_time"]
    if screen <= 2:
        screen_score = 12
    elif screen <= 4:
        screen_score = 9
    elif screen <= 6:
        screen_score = 5
    else:
        screen_score = 1

    # ── Stress Level (13 pts, 1–10 scale) ──────────────────────
    stress = inputs["stress_level"]
    if stress <= 3:
        stress_score = 13
    elif stress <= 5:
        stress_score = 9
    elif stress <= 7:
        stress_score = 5
    else:
        stress_score = 1

    total = (
        sleep_score + activity_score + diet_score
        + hydration_score + screen_score + stress_score
    )

    return ScoreBreakdown(
        sleep_score=sleep_score,
        activity_score=activity_score,
        diet_score=diet_score,
        hydration_score=hydration_score,
        screen_score=screen_score,
        stress_score=stress_score,
        total=round(total, 1),
    )


def score_to_grade(total: float) -> str:
    """Maps health score to a letter grade."""
    if total >= 85:
        return "S"
    elif total >= 70:
        return "A"
    elif total >= 55:
        return "B"
    elif total >= 40:
        return "C"
    else:
        return "D"
