# 🎮 HealthQuest AI
### AI-Based Lifestyle Disease Risk Predictor with Gamified Daily Health Scoring

A production-style machine learning application that predicts lifestyle disease risk, gamifies your health journey with XP/levels/bosses, and provides intelligent personalized recommendations — all inside a dark futuristic Streamlit dashboard.

---

## 🗂️ Project Structure

```
HealthQuestAI/
├── data/
│   ├── generate_dataset.py        ← Synthetic dataset generator
│   └── lifestyle_dataset.csv      ← Generated dataset (450 rows)
├── models/
│   └── random_forest_model.pkl    ← Saved best ML model + scaler
├── preprocessing/
│   └── preprocess.py              ← Reusable preprocessing pipeline
├── training/
│   └── train_model.py             ← Train & compare 3 models
├── scoring/
│   └── health_score.py            ← Transparent 100-pt health scorer
├── gamification/
│   └── game_logic.py              ← XP, levels, bosses, badges, streaks
├── recommendations/
│   └── suggestions.py             ← Smart suggestion engine + What-If
├── app/
│   └── app.py                     ← Streamlit dashboard (main entry point)
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone / extract the project
```bash
cd HealthQuestAI
```

### 2. Create & activate virtual environment (recommended)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate dataset (already included, but can regenerate)
```bash
cd data
python generate_dataset.py
cd ..
```

### 5. Train the model
```bash
python training/train_model.py
```
This will:
- Train Logistic Regression, Decision Tree, Random Forest
- Print accuracy comparison, confusion matrices, classification reports
- Save the best model to `models/random_forest_model.pkl`

### 6. Launch the app
```bash
streamlit run app/app.py
```

---

## 🤖 Machine Learning Details

| Model               | Accuracy |
|---------------------|----------|
| Logistic Regression | ~80%     |
| Decision Tree       | ~60%     |
| Random Forest       | ~76%     |

**Best model selected automatically** and saved as `random_forest_model.pkl`.

### Features Used
| Feature                | Description                      |
|------------------------|----------------------------------|
| `sleep_hours`          | Hours of sleep per night         |
| `screen_time`          | Screen hours per day             |
| `physical_activity`    | Minutes of exercise per day      |
| `water_intake`         | Litres of water per day          |
| `junk_food_frequency`  | Junk food days per week          |
| `stress_level`         | Stress on 1–10 scale             |
| `bmi`                  | Body Mass Index                  |
| `age`                  | Age in years                     |

### Target
- `risk_level`: **Low / Medium / High**

---

## 🎮 Gamification Features

### XP System
Health score → XP earned (e.g., score 72 = +72 XP)

### Levels
| Level | Name        | XP Range     |
|-------|-------------|--------------|
| 1     | Beginner    | 0–100        |
| 2     | Starter     | 100–250      |
| 3     | Improving   | 250–450      |
| 4     | Fit         | 450–700      |
| 5     | Warrior     | 700–1000     |
| 6     | Elite       | 1000–1400    |
| 7     | Peak Human  | 1400+        |

### Health Bosses
- 👹 **Stress Monster** — activated when stress ≥ 7
- 🍔 **Junk Food Beast** — activated when junk food ≥ 5 days/week
- 😴 **Sleep Debt Demon** — activated when sleep < 5.5 hours

### Achievement Badges
😴 Sleep Master · 🏃 Active Hero · 🧘 Calm Mind  
💧 Hydration King · 🥗 Clean Eater · 📵 Screen-Free · 💯 Centurion

---

## 🧮 Health Score Breakdown

| Dimension       | Max Points | Criteria                      |
|-----------------|------------|-------------------------------|
| Sleep           | 20         | 7.5h+ = full score            |
| Physical Activity | 20       | 60+ min/day = full score      |
| Diet Quality    | 20         | ≤1 junk food day/week = full  |
| Hydration       | 15         | 3L+ per day = full score      |
| Screen Time     | 12         | ≤2h/day = full score          |
| Stress          | 13         | Stress ≤3 = full score        |
| **Total**       | **100**    |                               |

---

## 🔮 What-If Simulator
Modify sleep, activity, and stress sliders to instantly see:
- Projected new health score
- XP gain/loss
- Risk level change

---

## 📈 Analytics
Click **⚡ ANALYZE MY HEALTH** each day to:
- Save to history
- Increment streak
- Accumulate XP
- View 14-day health trend chart

---

## ⚠️ Disclaimer
This application is for educational and wellness awareness purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment.

---

## 🛠️ Tech Stack
Python · Streamlit · Scikit-learn · Pandas · NumPy · Plotly · Joblib
