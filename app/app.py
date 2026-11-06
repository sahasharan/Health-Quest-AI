"""
app/app.py
HealthQuest AI — Main Streamlit Application
Dark futuristic health-tech dashboard with gamification.
Run: streamlit run app/app.py
"""

import os, sys, json, datetime
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import joblib

# ── Path setup ──────────────────────────────────────────────────────────────
ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)

from preprocessing.preprocess  import preprocess_single, FEATURE_COLS, RISK_ORDER
from scoring.health_score       import calculate_health_score, score_to_grade
from gamification.game_logic    import (
    score_to_xp, get_level_info, evaluate_bosses,
    evaluate_badges, update_streak, streak_message
)
from recommendations.suggestions import generate_suggestions, whatif_delta

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HealthQuest AI",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS — dark futuristic theme ──────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600&display=swap');

:root {
    --neon-blue:   #00d4ff;
    --neon-green:  #00ff88;
    --neon-purple: #bf5fff;
    --neon-red:    #ff4444;
    --neon-gold:   #ffd700;
    --bg-deep:     #050a14;
    --bg-card:     #0d1b2e;
    --bg-card2:    #0f2035;
    --border-glow: rgba(0,212,255,0.3);
    --text-main:   #e0f0ff;
    --text-dim:    #7090b0;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-deep) !important;
    color: var(--text-main) !important;
    font-family: 'Rajdhani', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: #080f1c !important;
    border-right: 1px solid var(--border-glow) !important;
}

h1, h2, h3 { font-family: 'Orbitron', monospace !important; }

.hq-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.6rem;
    font-weight: 900;
    background: linear-gradient(90deg, #00d4ff, #00ff88, #bf5fff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    letter-spacing: 3px;
    margin-bottom: 0;
    text-shadow: 0 0 40px rgba(0,212,255,0.3);
}

.hq-subtitle {
    text-align: center;
    color: var(--text-dim);
    font-size: 1rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

.glass-card {
    background: linear-gradient(135deg, rgba(13,27,46,0.95), rgba(15,32,53,0.85));
    border: 1px solid var(--border-glow);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 30px rgba(0,0,0,0.4), inset 0 1px 0 rgba(0,212,255,0.1);
}

.metric-label {
    font-family: 'Orbitron', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-bottom: 2px;
}

.metric-val {
    font-family: 'Orbitron', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    line-height: 1;
}

.neon-blue  { color: var(--neon-blue);   text-shadow: 0 0 15px var(--neon-blue); }
.neon-green { color: var(--neon-green);  text-shadow: 0 0 15px var(--neon-green); }
.neon-purple{ color: var(--neon-purple); text-shadow: 0 0 15px var(--neon-purple);}
.neon-gold  { color: var(--neon-gold);   text-shadow: 0 0 15px var(--neon-gold); }
.neon-red   { color: var(--neon-red);    text-shadow: 0 0 15px var(--neon-red); }

.risk-badge {
    display: inline-block;
    padding: 4px 18px;
    border-radius: 50px;
    font-family: 'Orbitron', monospace;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 2px;
}
.risk-low    { background: rgba(0,255,136,0.15); color: #00ff88; border: 1px solid #00ff88; }
.risk-medium { background: rgba(255,215,0,0.15);  color: #ffd700; border: 1px solid #ffd700; }
.risk-high   { background: rgba(255,68,68,0.15);  color: #ff4444; border: 1px solid #ff4444; }

.boss-card {
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
}
.boss-active   { background: rgba(255,68,68,0.1); border: 1px solid rgba(255,68,68,0.4); }
.boss-defeated { background: rgba(0,255,136,0.07); border: 1px solid rgba(0,255,136,0.3); }

.badge-chip {
    display: inline-block;
    background: rgba(191,95,255,0.15);
    border: 1px solid rgba(191,95,255,0.5);
    border-radius: 8px;
    padding: 6px 14px;
    margin: 4px;
    font-size: 0.85rem;
    color: #bf5fff;
}

.suggest-card {
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.95rem;
}
.prio-high   { background: rgba(255,68,68,0.08); border-left: 3px solid #ff4444; }
.prio-medium { background: rgba(255,215,0,0.08); border-left: 3px solid #ffd700; }
.prio-low    { background: rgba(0,255,136,0.06); border-left: 3px solid #00ff88; }

.section-header {
    font-family: 'Orbitron', monospace;
    font-size: 0.8rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: var(--neon-blue);
    border-bottom: 1px solid var(--border-glow);
    padding-bottom: 6px;
    margin-bottom: 1rem;
}

.stSlider > div > div > div > div { background: var(--neon-blue) !important; }
.stSelectbox label, .stSlider label { color: var(--text-main) !important; font-family: 'Rajdhani' !important; }
div[data-testid="metric-container"] { background: transparent !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--neon-blue); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


# ── Session state init ───────────────────────────────────────────────────────
def _init_state():
    defaults = {
        "total_xp": 0,
        "streak": 0,
        "history": [],          # list of {date, score, risk, xp}
        "last_date": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()


# ── Load model ───────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    path = os.path.join(ROOT, "models", "random_forest_model.pkl")
    if not os.path.exists(path):
        st.error("Model not found. Run: python training/train_model.py")
        st.stop()
    bundle = joblib.load(path)
    return bundle["model"], bundle["scaler"], bundle["label_encoder"]

model, scaler, le = load_model()


# ── Helper: predict risk ─────────────────────────────────────────────────────
def predict_risk(inputs: dict) -> str:
    X = preprocess_single(inputs, scaler)
    pred = model.predict(X)[0]
    return RISK_ORDER[pred]


# ── Gauge chart (Plotly) ─────────────────────────────────────────────────────
def gauge_chart(value, title, max_val=100, color="#00d4ff"):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"color": "#7090b0", "size": 13, "family": "Orbitron"}},
        number={"font": {"color": color, "size": 36, "family": "Orbitron"}},
        gauge={
            "axis": {"range": [0, max_val], "tickcolor": "#304060", "tickfont": {"color": "#304060"}},
            "bar": {"color": color, "thickness": 0.28},
            "bgcolor": "#0d1b2e",
            "borderwidth": 1,
            "bordercolor": "#1a3a5c",
            "steps": [
                {"range": [0, max_val * 0.4], "color": "#0d1b2e"},
                {"range": [max_val * 0.4, max_val * 0.7], "color": "#0f2035"},
                {"range": [max_val * 0.7, max_val], "color": "#122840"},
            ],
            "threshold": {"line": {"color": color, "width": 3}, "thickness": 0.85, "value": value},
        },
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=40, b=10),
        height=200,
        font={"color": "#e0f0ff"},
    )
    return fig


# ── XP Progress bar ──────────────────────────────────────────────────────────
def xp_progress_bar(level_info):
    pct = level_info.progress_pct
    html = f"""
    <div style="margin: 0.5rem 0;">
        <div style="display:flex; justify-content:space-between; font-size:0.8rem; color:#7090b0; margin-bottom:4px;">
            <span>{level_info.emoji} Lv.{level_info.level} {level_info.name}</span>
            <span>{level_info.xp_in_level} / {level_info.xp_in_level + level_info.xp_to_next} XP</span>
        </div>
        <div style="background:#0d1b2e; border-radius:50px; height:10px; border:1px solid #1a3a5c; overflow:hidden;">
            <div style="width:{pct}%; background:linear-gradient(90deg,#00d4ff,#00ff88);
                        height:100%; border-radius:50px; box-shadow:0 0 8px #00d4ff; transition:width 0.5s;"></div>
        </div>
        <div style="text-align:right; font-size:0.75rem; color:#304060; margin-top:3px;">{pct}% to next level</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# ── Weekly trend chart ───────────────────────────────────────────────────────
def weekly_chart(history):
    if not history:
        return None
    df = pd.DataFrame(history[-14:])
    df["date"] = pd.to_datetime(df["date"])
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["score"],
        mode="lines+markers",
        line=dict(color="#00d4ff", width=2),
        marker=dict(size=7, color="#00ff88", line=dict(color="#00d4ff", width=1)),
        fill="tozeroy",
        fillcolor="rgba(0,212,255,0.05)",
        name="Health Score",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, color="#304060"),
        yaxis=dict(showgrid=True, gridcolor="#1a3a5c", color="#304060", range=[0, 100]),
        margin=dict(l=0, r=0, t=10, b=0),
        height=180,
        showlegend=False,
        font=dict(color="#7090b0", family="Rajdhani"),
    )
    return fig


# ── Model accuracy comparison chart ─────────────────────────────────────────
def accuracy_chart():
    models_ = ["Logistic\nRegression", "Decision\nTree", "Random\nForest"]
    accs = [80.0, 60.0, 75.6]
    colors = ["#00ff88", "#ff4444", "#00d4ff"]
    fig = go.Figure(go.Bar(
        x=models_, y=accs,
        marker=dict(color=colors, line=dict(color="rgba(0,0,0,0)", width=0)),
        text=[f"{a}%" for a in accs],
        textposition="outside",
        textfont=dict(color="#e0f0ff", family="Orbitron", size=11),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, color="#304060"),
        yaxis=dict(showgrid=True, gridcolor="#1a3a5c", color="#304060", range=[0, 100]),
        margin=dict(l=0, r=0, t=10, b=0),
        height=200,
        font=dict(color="#7090b0", family="Rajdhani"),
    )
    return fig


# ════════════════════════════════════════════════════════════════════════════
#  SIDEBAR — INPUTS
# ════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<p class="section-header">⚡ Lifestyle Inputs</p>', unsafe_allow_html=True)

    sleep_hours = st.slider("😴 Sleep Hours", 3.0, 10.0, 7.0, 0.5,
                             help="How many hours did you sleep last night?")
    screen_time = st.slider("📱 Screen Time (hrs)", 0.0, 12.0, 4.0, 0.5)
    physical_activity = st.slider("🏃 Physical Activity (min/day)", 0, 120, 30, 5)
    water_intake = st.slider("💧 Water Intake (L/day)", 0.5, 5.0, 2.0, 0.1)
    junk_food_frequency = st.slider("🍔 Junk Food (days/week)", 0, 7, 3, 1)
    stress_level = st.slider("🧠 Stress Level (1–10)", 1.0, 10.0, 5.0, 0.5)
    bmi = st.slider("⚖️ BMI", 15.0, 40.0, 23.0, 0.1)
    age = st.number_input("🎂 Age", 18, 65, 25, 1)

    st.markdown("---")
    analyze_btn = st.button("⚡ ANALYZE MY HEALTH", use_container_width=True, type="primary")
    st.markdown("---")
    st.markdown('<p class="section-header">📊 Model Performance</p>', unsafe_allow_html=True)
    st.plotly_chart(accuracy_chart(), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
#  MAIN LAYOUT
# ════════════════════════════════════════════════════════════════════════════
st.markdown('<h1 class="hq-title">⚕ HealthQuest AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="hq-subtitle">AI-Powered Lifestyle Disease Predictor · Gamified Wellness Platform</p>', unsafe_allow_html=True)

inputs = {
    "sleep_hours": sleep_hours,
    "screen_time": screen_time,
    "physical_activity": physical_activity,
    "water_intake": water_intake,
    "junk_food_frequency": junk_food_frequency,
    "stress_level": stress_level,
    "bmi": bmi,
    "age": age,
}

# Live compute on every slider change (also triggers on button)
score_data    = calculate_health_score(inputs)
health_score  = score_data.total
risk_label    = predict_risk(inputs)
xp_earned     = score_to_xp(health_score)
level_info    = get_level_info(st.session_state.total_xp + xp_earned)
boss_statuses = evaluate_bosses(inputs)
badges_earned = evaluate_badges(inputs, health_score)
suggestions   = generate_suggestions(inputs, risk_label)
streak        = st.session_state.streak
grade         = score_to_grade(health_score)

if analyze_btn:
    today = str(datetime.date.today())
    if st.session_state.last_date != today:
        st.session_state.total_xp += xp_earned
        st.session_state.streak = update_streak(streak, health_score)
        st.session_state.history.append({
            "date": today, "score": health_score,
            "risk": risk_label, "xp": xp_earned
        })
        st.session_state.last_date = today
        streak = st.session_state.streak
        level_info = get_level_info(st.session_state.total_xp)
        st.balloons()


# ── Row 1: Key metrics ───────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

risk_css = {"Low": "risk-low", "Medium": "risk-medium", "High": "risk-high"}[risk_label]

with c1:
    st.markdown(f"""
    <div class="glass-card" style="text-align:center">
        <div class="metric-label">Disease Risk</div>
        <div style="margin-top:8px">
            <span class="risk-badge {risk_css}">{risk_label}</span>
        </div>
    </div>""", unsafe_allow_html=True)

with c2:
    score_color = "#00ff88" if health_score >= 70 else "#ffd700" if health_score >= 45 else "#ff4444"
    st.markdown(f"""
    <div class="glass-card" style="text-align:center">
        <div class="metric-label">Health Score</div>
        <div class="metric-val" style="color:{score_color};text-shadow:0 0 15px {score_color}">
            {health_score:.0f}
            <span style="font-size:1.2rem;color:#7090b0">/ 100</span>
        </div>
        <div style="color:#7090b0;font-size:0.8rem">Grade: <b style="color:{score_color}">{grade}</b></div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="glass-card" style="text-align:center">
        <div class="metric-label">XP Earned Today</div>
        <div class="metric-val neon-gold">+{xp_earned}</div>
        <div style="color:#7090b0;font-size:0.8rem">Total: {st.session_state.total_xp + xp_earned} XP</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="glass-card" style="text-align:center">
        <div class="metric-label">Streak</div>
        <div class="metric-val neon-purple">{st.session_state.streak}🔥</div>
        <div style="color:#7090b0;font-size:0.8rem">Days in a row</div>
    </div>""", unsafe_allow_html=True)


# ── Row 2: Level + Gauges ────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">🎮 Player Level</p>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center; padding:0.5rem 0">
        <div style="font-size:3rem">{level_info.emoji}</div>
        <div style="font-family:'Orbitron',monospace; font-size:1.4rem; color:#00d4ff">
            Level {level_info.level} — {level_info.name}
        </div>
    </div>""", unsafe_allow_html=True)
    xp_progress_bar(level_info)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">📊 Health Gauge</p>', unsafe_allow_html=True)
    st.plotly_chart(gauge_chart(health_score, "HEALTH SCORE"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ── Row 3: Score Breakdown + Bosses ─────────────────────────────────────────
col_a, col_b = st.columns([1.3, 1])

with col_a:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">🧮 Score Breakdown</p>', unsafe_allow_html=True)

    dims = [
        ("😴 Sleep",       score_data.sleep_score,    20, "#00d4ff"),
        ("🏃 Activity",    score_data.activity_score, 20, "#00ff88"),
        ("🥗 Diet",        score_data.diet_score,     20, "#bf5fff"),
        ("💧 Hydration",   score_data.hydration_score,15, "#00bfff"),
        ("📱 Screen",      score_data.screen_score,   12, "#ffd700"),
        ("🧠 Stress",      score_data.stress_score,   13, "#ff9944"),
    ]

    for label, val, max_v, color in dims:
        pct = (val / max_v) * 100
        st.markdown(f"""
        <div style="margin-bottom:8px">
            <div style="display:flex;justify-content:space-between;font-size:0.85rem;margin-bottom:3px;">
                <span style="color:#e0f0ff">{label}</span>
                <span style="color:{color};font-family:Orbitron,monospace">{val}/{max_v}</span>
            </div>
            <div style="background:#0a1525;border-radius:50px;height:7px;overflow:hidden;">
                <div style="width:{pct}%;background:{color};height:100%;border-radius:50px;
                            box-shadow:0 0 6px {color};"></div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">👾 Boss System</p>', unsafe_allow_html=True)

    for boss in boss_statuses:
        css = "boss-active" if boss.is_active else "boss-defeated"
        icon = "🔴" if boss.is_active else "✅"
        st.markdown(f"""
        <div class="boss-card {css}">
            <b>{boss.emoji} {boss.name}</b> {icon}<br>
            <span style="font-size:0.85rem;color:#a0b8d0">{boss.message}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ── Row 4: Badges + Suggestions ─────────────────────────────────────────────
col_x, col_y = st.columns([1, 1.3])

with col_x:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">🏅 Achievements</p>', unsafe_allow_html=True)
    if badges_earned:
        badge_html = "".join(f'<span class="badge-chip">{b["emoji"]} {b["name"]}</span>' for b in badges_earned)
        st.markdown(badge_html, unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:#304060;font-size:0.85rem">No badges yet — improve your lifestyle to unlock!</p>', unsafe_allow_html=True)

    st.markdown(f'<p style="color:#304060;font-size:0.8rem;margin-top:0.5rem">{streak_message(st.session_state.streak)}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_y:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">🧠 Smart Recommendations</p>', unsafe_allow_html=True)
    shown = 0
    for s in suggestions:
        if shown >= 5:
            break
        css = f"prio-{s['priority']}"
        st.markdown(f"""
        <div class="suggest-card {css}">
            <b>{s['icon']} {s['category']}</b><br>
            <span style="font-size:0.88rem;color:#c0d8f0">{s['message']}</span>
        </div>""", unsafe_allow_html=True)
        shown += 1
    st.markdown('</div>', unsafe_allow_html=True)


# ── Row 5: What-If Simulator ─────────────────────────────────────────────────
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<p class="section-header">🔮 What-If Simulator</p>', unsafe_allow_html=True)

wc1, wc2, wc3 = st.columns(3)
with wc1:
    wi_sleep = st.slider("If sleep were…", 3.0, 10.0, sleep_hours, 0.5, key="wi_sleep")
with wc2:
    wi_activity = st.slider("If activity were…", 0, 120, physical_activity, 5, key="wi_act")
with wc3:
    wi_stress = st.slider("If stress were…", 1.0, 10.0, stress_level, 0.5, key="wi_stress")

modified_inputs = dict(inputs)
modified_inputs.update({"sleep_hours": wi_sleep, "physical_activity": wi_activity, "stress_level": wi_stress})
new_score_data = calculate_health_score(modified_inputs)
new_score = new_score_data.total
delta = whatif_delta(inputs, modified_inputs, health_score, new_score)

d_col = "#00ff88" if delta["delta_score"] >= 0 else "#ff4444"
sign = "+" if delta["delta_score"] >= 0 else ""
st.markdown(f"""
<div style="display:flex;gap:2rem;margin-top:0.5rem;flex-wrap:wrap">
    <div>
        <span style="color:#7090b0;font-size:0.8rem">New Score</span><br>
        <span style="font-family:Orbitron,monospace;font-size:1.8rem;color:{d_col}">{new_score:.0f}</span>
    </div>
    <div>
        <span style="color:#7090b0;font-size:0.8rem">Score Δ</span><br>
        <span style="font-family:Orbitron,monospace;font-size:1.8rem;color:{d_col}">{sign}{delta['delta_score']}</span>
    </div>
    <div>
        <span style="color:#7090b0;font-size:0.8rem">XP Δ</span><br>
        <span style="font-family:Orbitron,monospace;font-size:1.8rem;color:#ffd700">{sign}{delta['delta_xp']}</span>
    </div>
    <div>
        <span style="color:#7090b0;font-size:0.8rem">Projected Risk</span><br>
        <span style="font-family:Orbitron,monospace;font-size:1.4rem;color:#bf5fff">{predict_risk(modified_inputs)}</span>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# ── Row 6: History Chart ─────────────────────────────────────────────────────
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<p class="section-header">📈 Health History (Last 14 Days)</p>', unsafe_allow_html=True)
if st.session_state.history:
    fig_trend = weekly_chart(st.session_state.history)
    if fig_trend:
        st.plotly_chart(fig_trend, use_container_width=True)
else:
    st.markdown('<p style="color:#304060;text-align:center;padding:1rem">Click ⚡ ANALYZE MY HEALTH to start tracking.</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 1rem;color:#1a3a5c;font-size:0.75rem;letter-spacing:3px">
    HEALTHQUEST AI · BUILT WITH STREAMLIT + SCIKIT-LEARN · NOT MEDICAL ADVICE
</div>""", unsafe_allow_html=True)
