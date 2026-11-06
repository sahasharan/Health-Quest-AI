"""
gamification/game_logic.py
Complete gamification layer: XP, levels, bosses, streaks, badges.
"""

from dataclasses import dataclass, field
from typing import List, Optional


# ── Level System ────────────────────────────────────────────────────────────

LEVELS = [
    {"level": 1, "name": "Beginner",     "min_xp": 0,    "max_xp": 100,  "emoji": "🌱"},
    {"level": 2, "name": "Starter",      "min_xp": 100,  "max_xp": 250,  "emoji": "🌿"},
    {"level": 3, "name": "Improving",    "min_xp": 250,  "max_xp": 450,  "emoji": "💪"},
    {"level": 4, "name": "Fit",          "min_xp": 450,  "max_xp": 700,  "emoji": "🏃"},
    {"level": 5, "name": "Warrior",      "min_xp": 700,  "max_xp": 1000, "emoji": "⚔️"},
    {"level": 6, "name": "Elite",        "min_xp": 1000, "max_xp": 1400, "emoji": "🔥"},
    {"level": 7, "name": "Peak Human",   "min_xp": 1400, "max_xp": 9999, "emoji": "👑"},
]


@dataclass
class LevelInfo:
    level: int
    name: str
    emoji: str
    current_xp: int
    xp_in_level: int        # XP earned within this level
    xp_to_next: int         # XP needed to reach next level
    progress_pct: float     # 0–100


def get_level_info(total_xp: int) -> LevelInfo:
    """Compute level and progress from total accumulated XP."""
    current = LEVELS[0]
    for lvl in LEVELS:
        if total_xp >= lvl["min_xp"]:
            current = lvl

    xp_in_level = total_xp - current["min_xp"]
    xp_range = current["max_xp"] - current["min_xp"]
    xp_to_next = max(0, current["max_xp"] - total_xp)
    progress_pct = min(100.0, (xp_in_level / xp_range) * 100)

    return LevelInfo(
        level=current["level"],
        name=current["name"],
        emoji=current["emoji"],
        current_xp=total_xp,
        xp_in_level=xp_in_level,
        xp_to_next=xp_to_next,
        progress_pct=round(progress_pct, 1),
    )


def score_to_xp(health_score: float) -> int:
    """Convert today's health score directly to XP earned."""
    return int(health_score)


# ── Boss System ─────────────────────────────────────────────────────────────

BOSSES = [
    {
        "id": "stress_monster",
        "name": "Stress Monster",
        "emoji": "👹",
        "trigger_key": "stress_level",
        "trigger_fn": lambda v: v >= 7,
        "description": "Feeds on cortisol and sleepless nights.",
        "defeated_msg": "You defeated the Stress Monster! Calm mind restored.",
        "active_msg": "⚠️ Stress Monster is growing stronger! Lower your stress.",
    },
    {
        "id": "junk_food_beast",
        "name": "Junk Food Beast",
        "emoji": "🍔",
        "trigger_key": "junk_food_frequency",
        "trigger_fn": lambda v: v >= 5,
        "description": "Thrives on processed food and empty calories.",
        "defeated_msg": "Junk Food Beast neutralized! Clean diet wins.",
        "active_msg": "⚠️ Junk Food Beast lurking! Cut down on junk food.",
    },
    {
        "id": "sleep_debt_demon",
        "name": "Sleep Debt Demon",
        "emoji": "😴",
        "trigger_key": "sleep_hours",
        "trigger_fn": lambda v: v < 5.5,
        "description": "Drains XP while you sleep less than 5.5 hours.",
        "defeated_msg": "Sleep Debt Demon vanquished! Sweet dreams.",
        "active_msg": "⚠️ Sleep Debt Demon active! Get at least 7 hours of sleep.",
    },
]


@dataclass
class BossStatus:
    boss_id: str
    name: str
    emoji: str
    is_active: bool
    message: str


def evaluate_bosses(inputs: dict) -> List[BossStatus]:
    """Check which bosses are active based on current lifestyle inputs."""
    statuses = []
    for boss in BOSSES:
        val = inputs[boss["trigger_key"]]
        active = boss["trigger_fn"](val)
        statuses.append(BossStatus(
            boss_id=boss["id"],
            name=boss["name"],
            emoji=boss["emoji"],
            is_active=active,
            message=boss["active_msg"] if active else boss["defeated_msg"],
        ))
    return statuses


# ── Achievement Badges ───────────────────────────────────────────────────────

ALL_BADGES = [
    {"id": "sleep_master",   "name": "Sleep Master",   "emoji": "😴", "condition": lambda i: i["sleep_hours"] >= 8},
    {"id": "active_hero",    "name": "Active Hero",    "emoji": "🏃", "condition": lambda i: i["physical_activity"] >= 60},
    {"id": "calm_mind",      "name": "Calm Mind",      "emoji": "🧘", "condition": lambda i: i["stress_level"] <= 3},
    {"id": "hydration_king", "name": "Hydration King", "emoji": "💧", "condition": lambda i: i["water_intake"] >= 3.0},
    {"id": "clean_eater",    "name": "Clean Eater",    "emoji": "🥗", "condition": lambda i: i["junk_food_frequency"] <= 1},
    {"id": "screen_free",    "name": "Screen-Free",    "emoji": "📵", "condition": lambda i: i["screen_time"] <= 2},
    {"id": "centurion",      "name": "Centurion",      "emoji": "💯", "condition": lambda i: i.get("health_score", 0) >= 85},
]


def evaluate_badges(inputs: dict, health_score: float) -> List[dict]:
    """Return list of earned badges for current session."""
    check = dict(inputs)
    check["health_score"] = health_score
    return [b for b in ALL_BADGES if b["condition"](check)]


# ── Streak System ────────────────────────────────────────────────────────────

def update_streak(current_streak: int, health_score: float, threshold: float = 55.0) -> int:
    """
    Increment streak if health score is above threshold, else reset to 0.
    Returns updated streak count.
    """
    if health_score >= threshold:
        return current_streak + 1
    return 0


def streak_message(streak: int) -> str:
    if streak == 0:
        return "No active streak yet. Start today! 🌟"
    elif streak < 3:
        return f"🔥 {streak}-Day Streak — keep going!"
    elif streak < 7:
        return f"🔥🔥 {streak}-Day Streak — you're on fire!"
    else:
        return f"🔥🔥🔥 {streak}-Day Streak — LEGENDARY!"
