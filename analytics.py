import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def calculate_hybrid_stability(ai_score, lifestyle_factors, symptoms, age):
    base_stability = int(max(0, min(100, (ai_score + 0.5) * 100)))
    penalties = 0
    reasons = []
    
    if "Smoking" in lifestyle_factors:
        penalties += 5
        reasons.append("Lifestyle (Smoking)")
    if "High Stress Work" in lifestyle_factors:
        penalties += 5
        reasons.append("High Stress Environment")
    if "Regular Alcohol" in lifestyle_factors:
        penalties += 5
        reasons.append("Alcohol Consumption")
    if age > 60:
        penalties += 2
        
    symptom_weights = {
        "Fatigue": 10,
        "Insomnia": 15,
        "Anxiety": 15,
        "Palpitations": 20,
        "Headache": 5,
    }
    
    for sym in symptoms:
        penalties += symptom_weights.get(sym, 5)
        reasons.append(f"Symptom ({sym})")
        
    return max(0, base_stability - penalties), base_stability, reasons

def generate_baseline(days=30):
    np.random.seed(42)
    return pd.DataFrame(
        {
            "snooze_delta": np.random.normal(0.5, 0.2, days),
            "daily_steps": np.random.normal(7000, 800, days),
            "app_switch_rate": np.random.normal(40, 5, days),
            "pickup_count": np.random.normal(80, 10, days),
        }
    )

def train_isolation_forest(baseline_df):
    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    model.fit(baseline_df)
    return model

def generate_scroll_pattern(intensity, erraticness, duration_seconds=60):
    np.random.seed(42)
    time_points = range(duration_seconds)
    if intensity < 300:
        velocities = [
            0 if np.random.random() > 0.3 else np.random.randint(50, 400)
            for _ in time_points
        ]
    else:
        base = np.full(duration_seconds, intensity)
        noise = np.random.normal(0, erraticness * 5, duration_seconds)
        velocities = np.abs(base + noise)
    return pd.DataFrame({"Seconds": time_points, "Velocity (px/s)": velocities})

def detect_doomscrolling(df, current_time_obj):
    avg_speed = df["Velocity (px/s)"].mean()
    zero_crossings = (df["Velocity (px/s)"] == 0).sum()
    is_late_night = current_time_obj.hour >= 22 or current_time_obj.hour <= 4
    risk_score = 0
    reasons = []
    
    if avg_speed > 600:
        risk_score += 40
        reasons.append("High Velocity")
    if zero_crossings < 5:
        risk_score += 40
        reasons.append("Zero Dwell Time")
    if is_late_night and risk_score > 0:
        risk_score += 20
        reasons.append("Late Night Context")
        
    return min(100, risk_score), reasons

baseline_df = generate_baseline()
model = train_isolation_forest(baseline_df)
