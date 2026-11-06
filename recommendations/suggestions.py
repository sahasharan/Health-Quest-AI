"""
recommendations/suggestions.py
Personalized, supportive health recommendations based on user inputs.
"""

from typing import List


def generate_suggestions(inputs: dict, risk_label: str) -> List[dict]:
    """
    Returns a list of personalized recommendation dicts with:
      - category: str
      - icon: str
      - message: str
      - priority: 'high' | 'medium' | 'low'
    """
    suggestions = []

    sleep = inputs["sleep_hours"]
    screen = inputs["screen_time"]
    activity = inputs["physical_activity"]
    water = inputs["water_intake"]
    junk = inputs["junk_food_frequency"]
    stress = inputs["stress_level"]

    # ── Sleep ────────────────────────────────────────────────────
    if sleep < 5:
        suggestions.append({
            "category": "Sleep",
            "icon": "😴",
            "message": "You're severely sleep-deprived. Aim for at least 7–8 hours — try a fixed bedtime routine tonight.",
            "priority": "high",
        })
    elif sleep < 6.5:
        suggestions.append({
            "category": "Sleep",
            "icon": "😴",
            "message": "Increasing sleep from " + str(sleep) + " to 7+ hours can dramatically improve mood, focus, and immunity.",
            "priority": "medium",
        })
    else:
        suggestions.append({
            "category": "Sleep",
            "icon": "✅",
            "message": f"Great sleep hygiene! {sleep} hours is solid. Maintain consistency.",
            "priority": "low",
        })

    # ── Screen Time ──────────────────────────────────────────────
    if screen > 8:
        suggestions.append({
            "category": "Screen Time",
            "icon": "📵",
            "message": f"{screen}h screen time is very high. Use app timers, try 20-20-20 rule (every 20 min, look 20 ft away for 20 sec).",
            "priority": "high",
        })
    elif screen > 5:
        suggestions.append({
            "category": "Screen Time",
            "icon": "📱",
            "message": "Consider reducing screen time by 1 hour daily. Replace with reading or outdoor activity.",
            "priority": "medium",
        })

    # ── Physical Activity ────────────────────────────────────────
    if activity < 20:
        suggestions.append({
            "category": "Exercise",
            "icon": "🏃",
            "message": "Even a 20-minute walk daily can reduce your risk significantly. Start small — consistency beats intensity.",
            "priority": "high",
        })
    elif activity < 45:
        suggestions.append({
            "category": "Exercise",
            "icon": "💪",
            "message": f"You're at {activity} min/day. Try reaching 45–60 min for full cardiovascular benefits.",
            "priority": "medium",
        })
    else:
        suggestions.append({
            "category": "Exercise",
            "icon": "✅",
            "message": f"Excellent! {activity} min of activity daily puts you in the top tier.",
            "priority": "low",
        })

    # ── Hydration ────────────────────────────────────────────────
    if water < 1.5:
        suggestions.append({
            "category": "Hydration",
            "icon": "💧",
            "message": "Critically low water intake. Dehydration impairs brain function and energy. Drink at least 2L today.",
            "priority": "high",
        })
    elif water < 2.5:
        suggestions.append({
            "category": "Hydration",
            "icon": "💧",
            "message": f"You're at {water}L. Bump up to 2.5–3L. Try keeping a water bottle at your desk.",
            "priority": "medium",
        })

    # ── Diet ─────────────────────────────────────────────────────
    if junk >= 5:
        suggestions.append({
            "category": "Nutrition",
            "icon": "🥗",
            "message": f"Junk food {junk}x/week is taking a serious toll. Replace 2 meals with home-cooked food this week.",
            "priority": "high",
        })
    elif junk >= 3:
        suggestions.append({
            "category": "Nutrition",
            "icon": "🥗",
            "message": "Reduce junk food to under 2x/week. Prep meals on Sunday to make healthy eating easier.",
            "priority": "medium",
        })

    # ── Stress ───────────────────────────────────────────────────
    if stress >= 8:
        suggestions.append({
            "category": "Stress",
            "icon": "🧘",
            "message": "Dangerously high stress. Even 10 min of deep breathing or meditation daily can lower cortisol significantly.",
            "priority": "high",
        })
    elif stress >= 6:
        suggestions.append({
            "category": "Stress",
            "icon": "🧘",
            "message": "Moderate stress detected. Try journaling, short walks, or cutting caffeine after noon.",
            "priority": "medium",
        })
    else:
        suggestions.append({
            "category": "Stress",
            "icon": "✅",
            "message": "Great stress management! Keep up whatever you're doing.",
            "priority": "low",
        })

    # ── Risk-based top-level message ─────────────────────────────
    if risk_label == "High":
        suggestions.insert(0, {
            "category": "⚠️ Risk Alert",
            "icon": "🚨",
            "message": "Your lifestyle patterns indicate HIGH disease risk. Addressing sleep, activity, and stress could save your future health.",
            "priority": "high",
        })
    elif risk_label == "Medium":
        suggestions.insert(0, {
            "category": "📊 Risk Notice",
            "icon": "⚠️",
            "message": "Moderate risk detected. Small consistent changes made now prevent major health issues later.",
            "priority": "medium",
        })

    return suggestions


def whatif_delta(base_inputs: dict, modified_inputs: dict, base_score: float, new_score: float) -> dict:
    """Compute the projected change from a what-if scenario."""
    delta_score = round(new_score - base_score, 1)
    delta_xp = int(new_score) - int(base_score)
    changes = {k: modified_inputs[k] - base_inputs[k] for k in base_inputs if modified_inputs[k] != base_inputs[k]}
    return {
        "delta_score": delta_score,
        "delta_xp": delta_xp,
        "changes": changes,
        "new_score": new_score,
    }
