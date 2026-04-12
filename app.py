from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import random
import os

app = FastAPI(
    title="HealthSync Analytics API",
    description="Real-time cardiovascular health monitoring and analytics",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# PATIENT DATABASE
# ============================================================
PATIENTS_DB = [
    {
        "id": 1, "name": "James Okoye", "age": 67, "gender": "Male",
        "systolic_bp": 158, "diastolic_bp": 96, "heart_rate": 82, "spo2": 95, "temperature": 36.9,
        "cholesterol_total": 6.8, "cholesterol_hdl": 1.05, "cholesterol_ldl": 4.8, "triglycerides": 2.1,
        "bmi": 28.4, "weight_kg": 87, "height_cm": 175,
        "smoking": "former", "family_history": True, "diabetes": True, "sedentary": True,
        "medications": ["Lisinopril 10mg", "Atorvastatin 40mg", "Metformin 500mg"],
        "conditions": ["Hypertension", "Type 2 Diabetes", "Hyperlipidemia"],
        "steps_today": 3200, "sleep_hours": 5.5, "exercise_min_day": 10,
        "diet_score": 4, "stress_level": 8, "medication_adherence": 65,
        "ward": "Cardiology A", "bed": "A-204", "admission_date": "2026-04-05",
        "attending_physician": "Dr. K. Mokoena",
        "hrv_ms": 28, "ecg_rhythm": "Normal Sinus", "qrs_ms": 92, "qt_ms": 445, "pr_ms": 175,
        "devices": ["Apple Watch Series 9", "ECG Patch #3", "Continuous Glucose Monitor"]
    },
    {
        "id": 2, "name": "Amara Dlamini", "age": 54, "gender": "Female",
        "systolic_bp": 138, "diastolic_bp": 88, "heart_rate": 76, "spo2": 97, "temperature": 36.7,
        "cholesterol_total": 5.4, "cholesterol_hdl": 1.35, "cholesterol_ldl": 3.5, "triglycerides": 1.6,
        "bmi": 26.1, "weight_kg": 69, "height_cm": 163,
        "smoking": "never", "family_history": True, "diabetes": False, "sedentary": True,
        "medications": ["Amlodipine 5mg", "Aspirin 75mg"],
        "conditions": ["Hypertension", "Mild Hyperlipidemia"],
        "steps_today": 5800, "sleep_hours": 7.0, "exercise_min_day": 20,
        "diet_score": 6, "stress_level": 6, "medication_adherence": 80,
        "ward": "Cardiology B", "bed": "B-112", "admission_date": "2026-04-08",
        "attending_physician": "Dr. N. Zulu",
        "hrv_ms": 42, "ecg_rhythm": "Normal Sinus", "qrs_ms": 84, "qt_ms": 420, "pr_ms": 158,
        "devices": ["Samsung Galaxy Watch 6", "BP Cuff (Omron)"]
    },
    {
        "id": 3, "name": "Sipho Nkosi", "age": 42, "gender": "Male",
        "systolic_bp": 118, "diastolic_bp": 76, "heart_rate": 65, "spo2": 99, "temperature": 36.6,
        "cholesterol_total": 4.1, "cholesterol_hdl": 1.65, "cholesterol_ldl": 2.1, "triglycerides": 0.9,
        "bmi": 23.2, "weight_kg": 74, "height_cm": 179,
        "smoking": "never", "family_history": False, "diabetes": False, "sedentary": False,
        "medications": ["Vitamin D 1000IU"],
        "conditions": ["None significant"],
        "steps_today": 9200, "sleep_hours": 7.5, "exercise_min_day": 45,
        "diet_score": 8, "stress_level": 3, "medication_adherence": 95,
        "ward": "Outpatient", "bed": "OP-01", "admission_date": "2026-04-11",
        "attending_physician": "Dr. K. Mokoena",
        "hrv_ms": 68, "ecg_rhythm": "Normal Sinus", "qrs_ms": 78, "qt_ms": 395, "pr_ms": 148,
        "devices": ["Garmin Forerunner 265"]
    },
    {
        "id": 4, "name": "Fatima Hassan", "age": 61, "gender": "Female",
        "systolic_bp": 172, "diastolic_bp": 104, "heart_rate": 94, "spo2": 93, "temperature": 37.1,
        "cholesterol_total": 7.1, "cholesterol_hdl": 0.95, "cholesterol_ldl": 5.2, "triglycerides": 2.8,
        "bmi": 30.8, "weight_kg": 84, "height_cm": 165,
        "smoking": "current", "family_history": True, "diabetes": True, "sedentary": True,
        "medications": ["Ramipril 5mg", "Rosuvastatin 20mg", "Insulin Glargine 20u", "Bisoprolol 5mg"],
        "conditions": ["Severe Hypertension", "Type 2 Diabetes", "Atrial Fibrillation", "Obesity"],
        "steps_today": 1100, "sleep_hours": 4.5, "exercise_min_day": 0,
        "diet_score": 3, "stress_level": 9, "medication_adherence": 50,
        "ward": "ICU", "bed": "ICU-03", "admission_date": "2026-04-03",
        "attending_physician": "Dr. S. Maharaj",
        "hrv_ms": 18, "ecg_rhythm": "Atrial Fibrillation", "qrs_ms": 110, "qt_ms": 510, "pr_ms": 0,
        "devices": ["ECG Patch #7", "Continuous Glucose Monitor", "BP Cuff (arterial line)"]
    },
    {
        "id": 5, "name": "Thabo Mokoena", "age": 49, "gender": "Male",
        "systolic_bp": 145, "diastolic_bp": 92, "heart_rate": 79, "spo2": 96, "temperature": 36.8,
        "cholesterol_total": 5.9, "cholesterol_hdl": 1.15, "cholesterol_ldl": 3.9, "triglycerides": 1.9,
        "bmi": 27.3, "weight_kg": 82, "height_cm": 173,
        "smoking": "current", "family_history": True, "diabetes": False, "sedentary": True,
        "medications": ["Hydrochlorothiazide 25mg", "Aspirin 75mg"],
        "conditions": ["Hypertension", "Pre-diabetes"],
        "steps_today": 4100, "sleep_hours": 6.0, "exercise_min_day": 15,
        "diet_score": 5, "stress_level": 7, "medication_adherence": 70,
        "ward": "Cardiology A", "bed": "A-108", "admission_date": "2026-04-09",
        "attending_physician": "Dr. N. Zulu",
        "hrv_ms": 34, "ecg_rhythm": "Normal Sinus", "qrs_ms": 88, "qt_ms": 432, "pr_ms": 164,
        "devices": ["Apple Watch Series 8", "BP Cuff (Omron)"]
    },
    {
        "id": 6, "name": "Nomsa Khumalo", "age": 58, "gender": "Female",
        "systolic_bp": 148, "diastolic_bp": 91, "heart_rate": 84, "spo2": 96, "temperature": 36.9,
        "cholesterol_total": 6.2, "cholesterol_hdl": 1.20, "cholesterol_ldl": 4.1, "triglycerides": 1.8,
        "bmi": 29.5, "weight_kg": 78, "height_cm": 163,
        "smoking": "former", "family_history": True, "diabetes": True, "sedentary": True,
        "medications": ["Metformin 1000mg", "Amlodipine 5mg", "Simvastatin 20mg"],
        "conditions": ["Type 2 Diabetes", "Hypertension", "Hyperlipidemia"],
        "steps_today": 3800, "sleep_hours": 6.5, "exercise_min_day": 12,
        "diet_score": 5, "stress_level": 7, "medication_adherence": 72,
        "ward": "Cardiology B", "bed": "B-205", "admission_date": "2026-04-07",
        "attending_physician": "Dr. K. Mokoena",
        "hrv_ms": 31, "ecg_rhythm": "Normal Sinus", "qrs_ms": 90, "qt_ms": 440, "pr_ms": 168,
        "devices": ["Fitbit Sense 2", "Continuous Glucose Monitor"]
    },
    {
        "id": 7, "name": "David Petersen", "age": 72, "gender": "Male",
        "systolic_bp": 162, "diastolic_bp": 98, "heart_rate": 88, "spo2": 94, "temperature": 37.0,
        "cholesterol_total": 6.5, "cholesterol_hdl": 1.0, "cholesterol_ldl": 4.5, "triglycerides": 2.3,
        "bmi": 30.2, "weight_kg": 91, "height_cm": 174,
        "smoking": "current", "family_history": True, "diabetes": True, "sedentary": True,
        "medications": ["Lisinopril 20mg", "Atorvastatin 80mg", "Insulin Aspart", "Furosemide 40mg"],
        "conditions": ["Severe Hypertension", "Type 2 Diabetes", "Chronic Kidney Disease Stage 3"],
        "steps_today": 1800, "sleep_hours": 5.0, "exercise_min_day": 5,
        "diet_score": 3, "stress_level": 8, "medication_adherence": 60,
        "ward": "Cardiology A", "bed": "A-310", "admission_date": "2026-04-02",
        "attending_physician": "Dr. S. Maharaj",
        "hrv_ms": 22, "ecg_rhythm": "PVCs noted", "qrs_ms": 98, "qt_ms": 465, "pr_ms": 182,
        "devices": ["ECG Patch #2", "BP Cuff (arterial line)"]
    },
    {
        "id": 8, "name": "Lerato Sithole", "age": 36, "gender": "Female",
        "systolic_bp": 122, "diastolic_bp": 78, "heart_rate": 68, "spo2": 98, "temperature": 36.6,
        "cholesterol_total": 4.4, "cholesterol_hdl": 1.55, "cholesterol_ldl": 2.5, "triglycerides": 1.1,
        "bmi": 22.8, "weight_kg": 62, "height_cm": 165,
        "smoking": "never", "family_history": False, "diabetes": False, "sedentary": False,
        "medications": ["Vitamin D 2000IU", "Omega-3 1000mg"],
        "conditions": ["Mild anxiety (managed)"],
        "steps_today": 8400, "sleep_hours": 8.0, "exercise_min_day": 40,
        "diet_score": 9, "stress_level": 4, "medication_adherence": 90,
        "ward": "Outpatient", "bed": "OP-03", "admission_date": "2026-04-11",
        "attending_physician": "Dr. N. Zulu",
        "hrv_ms": 72, "ecg_rhythm": "Normal Sinus", "qrs_ms": 76, "qt_ms": 380, "pr_ms": 142,
        "devices": ["Apple Watch SE", "Whoop 4.0"]
    },
    {
        "id": 9, "name": "Solomon Dube", "age": 55, "gender": "Male",
        "systolic_bp": 141, "diastolic_bp": 89, "heart_rate": 81, "spo2": 97, "temperature": 36.8,
        "cholesterol_total": 5.6, "cholesterol_hdl": 1.10, "cholesterol_ldl": 3.6, "triglycerides": 1.7,
        "bmi": 26.8, "weight_kg": 80, "height_cm": 173,
        "smoking": "former", "family_history": True, "diabetes": False, "sedentary": True,
        "medications": ["Amlodipine 10mg", "Aspirin 100mg"],
        "conditions": ["Hypertension", "Overweight"],
        "steps_today": 5100, "sleep_hours": 6.5, "exercise_min_day": 18,
        "diet_score": 6, "stress_level": 6, "medication_adherence": 78,
        "ward": "Cardiology B", "bed": "B-318", "admission_date": "2026-04-06",
        "attending_physician": "Dr. K. Mokoena",
        "hrv_ms": 38, "ecg_rhythm": "Normal Sinus", "qrs_ms": 86, "qt_ms": 428, "pr_ms": 160,
        "devices": ["Samsung Galaxy Watch 6", "BP Cuff (Omron)"]
    },
    {
        "id": 10, "name": "Priya Naidoo", "age": 45, "gender": "Female",
        "systolic_bp": 128, "diastolic_bp": 82, "heart_rate": 72, "spo2": 98, "temperature": 36.7,
        "cholesterol_total": 4.8, "cholesterol_hdl": 1.45, "cholesterol_ldl": 2.8, "triglycerides": 1.3,
        "bmi": 24.5, "weight_kg": 65, "height_cm": 163,
        "smoking": "never", "family_history": True, "diabetes": False, "sedentary": False,
        "medications": ["Aspirin 75mg"],
        "conditions": ["Family history of CAD — monitoring"],
        "steps_today": 7600, "sleep_hours": 7.5, "exercise_min_day": 35,
        "diet_score": 7, "stress_level": 5, "medication_adherence": 88,
        "ward": "Outpatient", "bed": "OP-07", "admission_date": "2026-04-10",
        "attending_physician": "Dr. S. Maharaj",
        "hrv_ms": 55, "ecg_rhythm": "Normal Sinus", "qrs_ms": 80, "qt_ms": 400, "pr_ms": 150,
        "devices": ["Garmin Venu 3", "Withings ScanWatch"]
    }
]

AUDIT_LOG = [
    {"block": 1, "event": "Record Created", "user": "System", "hash": "a3f8e2b1c9d4", "prev": "genesis", "timestamp": "2026-04-05 08:00"},
    {"block": 2, "event": "Data Accessed", "user": "Dr. K. Mokoena", "hash": "b7c412f8e301", "prev": "a3f8e2b1c9d4", "timestamp": "2026-04-05 09:14"},
    {"block": 3, "event": "Vitals Updated", "user": "ECG Patch #3", "hash": "d921e5a4c781", "prev": "b7c412f8e301", "timestamp": "2026-04-08 11:30"},
    {"block": 4, "event": "Consent Changed", "user": "Patient Portal", "hash": "f04a87b2e915", "prev": "d921e5a4c781", "timestamp": "2026-04-09 14:22"},
    {"block": 5, "event": "AI Prediction", "user": "HealthSync AI v3", "hash": "12bc3e7d1f84", "prev": "f04a87b2e915", "timestamp": "2026-04-10 16:45"},
    {"block": 6, "event": "Report Exported", "user": "Dr. N. Zulu", "hash": "8d57f196a402", "prev": "12bc3e7d1f84", "timestamp": "2026-04-11 08:00"},
    {"block": 7, "event": "Medication Updated", "user": "Dr. S. Maharaj", "hash": "c4e9a2d7f031", "prev": "8d57f196a402", "timestamp": "2026-04-11 14:10"},
]


# ============================================================
# RISK ENGINE (Framingham-inspired)
# ============================================================
def calculate_risk_score(p: dict) -> int:
    score = 0.0
    age = p["age"]

    # Age factor
    if p["gender"] == "Male":
        score += max(0, min(13, (age - 20) * 0.27))
    else:
        score += max(0, min(11, (age - 20) * 0.22))

    # Systolic BP
    sbp = p["systolic_bp"]
    if sbp >= 180:   score += 7.0
    elif sbp >= 160: score += 5.0
    elif sbp >= 140: score += 3.0
    elif sbp >= 130: score += 1.5
    elif sbp >= 120: score += 0.5

    # Total cholesterol
    tc = p["cholesterol_total"]
    if tc >= 7.0:    score += 5.5
    elif tc >= 6.0:  score += 3.5
    elif tc >= 5.0:  score += 2.0
    elif tc >= 4.5:  score += 1.0

    # HDL (protective — lowers score)
    hdl = p["cholesterol_hdl"]
    if hdl >= 1.6:   score -= 2.5
    elif hdl >= 1.3: score -= 1.0
    elif hdl < 1.0:  score += 2.5

    # Smoking
    smoke = {"current": 4.5, "former": 1.5, "never": 0.0}
    score += smoke.get(p["smoking"], 0)

    # Diabetes
    if p["diabetes"]:       score += 3.5
    # Family history
    if p["family_history"]: score += 2.0
    # BMI
    bmi = p["bmi"]
    if bmi >= 35:   score += 3.0
    elif bmi >= 30: score += 2.0
    elif bmi >= 25: score += 1.0
    # Sedentary
    if p["sedentary"]:      score += 1.5

    return int(min(98, max(5, round((score / 36) * 100))))


def get_risk_level(risk: int) -> str:
    if risk >= 80:   return "Critical"
    elif risk >= 60: return "High"
    elif risk >= 35: return "Medium"
    else:            return "Low"


def calculate_risk_factors(p: dict) -> dict:
    age = p["age"]
    tc  = p["cholesterol_total"]
    hdl = p["cholesterol_hdl"]
    sbp = p["systolic_bp"]
    smoke_map = {"current": 16, "former": 6, "never": 0}
    return {
        "Age":               round(min(30, max(0, (age - 20) * 0.85))),
        "Blood Pressure":    round(min(25, max(0, (sbp - 110) * 0.36))),
        "Total Cholesterol": round(min(20, max(0, (tc - 4.0) * 6))),
        "HDL (Protective)":  round(min(15, max(0, (1.4 - hdl) * 10))),
        "Diabetes":          18 if p["diabetes"] else 0,
        "Smoking":           smoke_map.get(p["smoking"], 0),
        "Family History":    10 if p["family_history"] else 0,
        "Sedentary":         12 if p["sedentary"] else 0,
        "BMI":               round(min(12, max(0, (p["bmi"] - 22) * 2))),
    }


def generate_shap_values(factors: dict) -> dict:
    shap = {}
    for k, v in factors.items():
        if k == "HDL (Protective)":
            shap[k] = round(-abs(v) * 0.65 - random.uniform(0, 1.5), 1)
        else:
            shap[k] = round(v * 0.72 + random.uniform(-1.5, 2.0), 1)
    return shap


def generate_twin_current(p: dict) -> list:
    risk = calculate_risk_score(p)
    sbp  = p["systolic_bp"]
    tc   = p["cholesterol_total"]
    return [
        round(max(10, 100 - risk)),
        round(max(10, 100 - (sbp - 100) * 1.5)),
        round(max(10, 100 - (tc - 4.0) * 14)),
        round(max(10, 80 if not p["diabetes"] else 45)),
        round(max(10, 100 - max(0, (p["bmi"] - 22) * 5))),
        round(max(10, 65 if not p["sedentary"] else 28)),
    ]


def simulate_twin(p: dict, exercise: int, diet: int, stress: int, med: int, sleep: float, smoke: int) -> dict:
    base = generate_twin_current(p)
    boost = (exercise / 120 * 22) + (diet / 10 * 14) + ((10 - stress) / 10 * 10) + (med / 100 * 12) + (sleep / 10 * 6) - smoke * 9
    simulated = [round(min(100, max(10, v + boost * 0.45 + random.uniform(-2, 2)))) for v in base]
    current_risk = calculate_risk_score(p)
    delta = -round((exercise / 120 * 14) + (diet / 10 * 7) + (med / 100 * 9) - (stress / 10 * 4))
    new_risk = int(min(98, max(5, current_risk + delta)))
    return {
        "current":     base,
        "simulated":   simulated,
        "current_risk":  current_risk,
        "simulated_risk": new_risk,
        "risk_delta":    delta,
        "labels":      ["Heart Health", "Blood Pressure", "Cholesterol", "Glucose Control", "BMI", "Fitness"],
        "insights": [
            f"{'✅' if exercise >= 30 else '⚠️'} Exercise: {exercise} min/day {'— meets target' if exercise >= 30 else '— target 30+ min'}",
            f"{'✅' if diet >= 7 else '⚠️'} Diet quality: {diet}/10 {'— adequate' if diet >= 7 else '— improve'}",
            f"{'✅' if med >= 80 else '⚠️'} Medication adherence: {med}% {'— on track' if med >= 80 else '— below 80% target'}",
            f"{'✅' if stress <= 4 else '⚠️'} Stress level: {stress}/10 {'— well managed' if stress <= 4 else '— elevated risk'}",
            f"{'✅' if sleep >= 7 else '⚠️'} Sleep: {sleep}h/night {'— healthy' if sleep >= 7 else '— below 7h target'}",
        ]
    }


def build_recommendations(p: dict) -> dict:
    tc  = p["cholesterol_total"]
    sbp = p["systolic_bp"]
    bmi = p["bmi"]

    diet = []
    if tc >= 6.0:
        diet += ["Reduce saturated fats to <7% of daily calories",
                 "Increase soluble fibre: oats, legumes, psyllium (30g/day)"]
    if p["diabetes"]:
        diet += ["Limit refined carbohydrates; target glycaemic index <55",
                 "Control carbohydrate portions: 45–60g per meal"]
    if bmi >= 27:
        diet.append(f"Target 500 kcal/day deficit to achieve BMI <25 (current {bmi})")
    diet += ["Increase omega-3 intake: oily fish 2×/week or 2g supplement daily",
             f"Limit sodium to <2,300 mg/day {'(priority: BP is elevated)' if sbp >= 140 else ''}",
             "DASH diet pattern strongly recommended for cardiovascular protection"]

    exercise = []
    if p["sedentary"]:
        exercise.append("Start with 10-min brisk walks; increase by 5 min each week")
    exercise.append("Target 150 min/week of moderate aerobic activity")
    steps = p["steps_today"]
    if steps < 7000:
        exercise.append(f"Increase daily steps: {steps:,} today → 10,000 goal")
    exercise += ["Include 2× resistance/strength training sessions per week",
                 "Break sitting time: stand or walk briefly every 45 minutes"]
    if p["age"] > 60 or len(p["conditions"]) > 1:
        exercise.append("Supervised cardiac exercise programme recommended initially")

    meds = [f"Continue {m} as prescribed" for m in p["medications"]]
    meds.append(f"Medication adherence: {p['medication_adherence']}% — target >90%")
    if sbp >= 140:
        meds.append("Take BP readings twice daily and log in the app")
    if p["diabetes"]:
        meds.append("Monitor blood glucose before meals and at bedtime")
    meds.append("Cardiology review scheduled in 4 weeks")

    lifestyle = []
    if p["smoking"] == "current":
        lifestyle.append("QUIT SMOKING — the single highest-impact cardiovascular intervention")
    elif p["smoking"] == "former":
        lifestyle.append("Smoke-free status maintained — keep up this commitment")
    sleep = p["sleep_hours"]
    if sleep < 7:
        lifestyle.append(f"Improve sleep hygiene: {sleep}h/night → target 7–9h")
    lifestyle += ["Practice mindfulness or deep breathing 10 min daily for stress",
                  "Limit alcohol to <2 units/day (maximum 14 units/week)"]
    if p["family_history"]:
        lifestyle.append("Advise first-degree relatives to undergo cardiovascular screening")

    action_plan = [
        {"week": "Week 1", "task": "Begin 10-min daily walks. Reduce sodium. Log all meals.", "done": False},
        {"week": "Week 2", "task": "Increase walks to 20 min. Reduce saturated fat intake.", "done": False},
        {"week": "Week 3", "task": "Add resistance training 2×/week. Track medication adherence.", "done": False},
        {"week": "Week 4", "task": "Full 150-min/week exercise target. Cardiology review appointment.", "done": False},
    ]

    return {"diet": diet, "exercise": exercise, "medications": meds, "lifestyle": lifestyle, "action_plan": action_plan}


def build_alerts(patients_computed: list) -> list:
    alerts = []
    for p in patients_computed:
        if p["spo2"] < 94:
            alerts.append({
                "type": "critical", "icon": "🩺",
                "title": "Critical SpO₂",
                "desc": f"{p['name']} ({p['ward']}) — SpO₂ at {p['spo2']}%. Oxygen supplementation may be required.",
                "patient": p["name"], "time": "Just now"
            })
        if p["systolic_bp"] >= 170:
            alerts.append({
                "type": "critical", "icon": "💔",
                "title": "Hypertensive Crisis",
                "desc": f"{p['name']} ({p['ward']}) — Systolic BP {p['systolic_bp']} mmHg. Immediate review required.",
                "patient": p["name"], "time": "2 min ago"
            })
        if "Atrial Fibrillation" in p["ecg_rhythm"]:
            alerts.append({
                "type": "critical", "icon": "🚨",
                "title": "Atrial Fibrillation",
                "desc": f"{p['name']} ({p['ward']}) — Irregular rhythm on ECG. QTc {p['qt_ms']}ms — monitoring active.",
                "patient": p["name"], "time": "4 min ago"
            })
        if p["heart_rate"] >= 95:
            alerts.append({
                "type": "warning", "icon": "⚠️",
                "title": "Elevated Heart Rate",
                "desc": f"{p['name']} ({p['ward']}) — HR {p['heart_rate']} bpm sustained >15 minutes.",
                "patient": p["name"], "time": "10 min ago"
            })
        if p["medication_adherence"] < 60:
            alerts.append({
                "type": "warning", "icon": "💊",
                "title": "Low Medication Adherence",
                "desc": f"{p['name']} — Adherence at {p['medication_adherence']}%. Missed doses detected.",
                "patient": p["name"], "time": "30 min ago"
            })
        if p["risk"] >= 75 and p["steps_today"] < 2000:
            alerts.append({
                "type": "warning", "icon": "🏃",
                "title": "High Risk + Minimal Activity",
                "desc": f"{p['name']} — High-risk patient with only {p['steps_today']:,} steps today.",
                "patient": p["name"], "time": "1h ago"
            })
        if "PVC" in p["ecg_rhythm"]:
            alerts.append({
                "type": "warning", "icon": "📈",
                "title": "PVCs Detected on ECG",
                "desc": f"{p['name']} ({p['ward']}) — Premature ventricular contractions noted. QRS {p['qrs_ms']}ms.",
                "patient": p["name"], "time": "45 min ago"
            })
    alerts += [
        {"type": "info", "icon": "🔋", "title": "Device Battery Low",
         "desc": "ECG Patch #7 (ICU-03) battery at 12%. Replace within 4 hours.",
         "patient": "", "time": "2h ago"},
        {"type": "info", "icon": "📋", "title": "Monthly Report Ready",
         "desc": "Population health analytics report for March is ready for review.",
         "patient": "", "time": "5h ago"},
    ]
    return alerts


# ============================================================
# PRE-COMPUTE PATIENT LIST WITH RISK SCORES
# ============================================================
def enrich_patient(raw: dict) -> dict:
    risk = calculate_risk_score(raw)
    return {**raw, "risk": risk, "risk_level": get_risk_level(risk)}

PATIENTS_COMPUTED = [enrich_patient(p) for p in PATIENTS_DB]


# ============================================================
# PYDANTIC MODELS
# ============================================================
class PredictRequest(BaseModel):
    age: int
    systolic_bp: int
    cholesterol: Optional[float] = 5.0
    hdl: Optional[float] = 1.2
    smoking: Optional[str] = "never"
    diabetes: Optional[bool] = False
    family_history: Optional[bool] = False
    bmi: Optional[float] = 25.0

class TwinSimulateRequest(BaseModel):
    patient_id: int
    exercise: int = 20
    diet: int = 4
    stress: int = 7
    medication_adherence: int = 60
    sleep: float = 6.0
    smoking_status: int = 1


# ============================================================
# ENDPOINTS
# ============================================================
@app.get("/")
async def root():
    return {
        "service": "HealthSync Analytics API v3",
        "status": "online",
        "patients": len(PATIENTS_COMPUTED),
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "development")
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat(), "service": "HealthSync API v3"}


@app.get("/patients")
async def list_patients():
    """All patients with pre-computed risk scores."""
    return [
        {k: v for k, v in p.items()
         if k not in ("devices",)}
        for p in PATIENTS_COMPUTED
    ]


@app.get("/patients/{patient_id}")
async def get_patient(patient_id: int):
    """Full patient record by 1-based ID."""
    match = next((p for p in PATIENTS_COMPUTED if p["id"] == patient_id), None)
    if not match:
        raise HTTPException(status_code=404, detail="Patient not found")
    return match


@app.get("/patients/{patient_id}/vitals")
async def get_live_vitals(patient_id: int):
    """Live vitals with small physiological noise for real-time streaming."""
    p = next((p for p in PATIENTS_COMPUTED if p["id"] == patient_id), None)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")

    def jitter(val, pct):
        return round(val + val * random.uniform(-pct, pct), 1)

    hr  = int(jitter(p["heart_rate"], 0.07))
    sbp = int(jitter(p["systolic_bp"], 0.04))
    dbp = int(jitter(p["diastolic_bp"], 0.04))
    spo2 = min(100, int(jitter(p["spo2"], 0.015)))
    temp = round(jitter(p["temperature"], 0.008), 1)

    return {
        "patient_id":   patient_id,
        "heart_rate":   hr,
        "systolic_bp":  sbp,
        "diastolic_bp": dbp,
        "spo2":         spo2,
        "temperature":  temp,
        "hrv_ms":       p["hrv_ms"] + random.randint(-3, 3),
        "ecg_rhythm":   p["ecg_rhythm"],
        "qrs_ms":       p["qrs_ms"],
        "qt_ms":        p["qt_ms"],
        "pr_ms":        p["pr_ms"],
        "steps_today":  p["steps_today"] + random.randint(0, 20),
        "timestamp":    datetime.now().isoformat(),
    }


@app.get("/patients/{patient_id}/risk")
async def get_risk_analysis(patient_id: int):
    """XAI risk breakdown with factor weights and SHAP-style values."""
    p = next((p for p in PATIENTS_COMPUTED if p["id"] == patient_id), None)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")

    factors = calculate_risk_factors(p)
    shap    = generate_shap_values(factors)
    top3    = sorted(factors, key=factors.get, reverse=True)[:3]

    return {
        "patient_id":   patient_id,
        "risk_score":   p["risk"],
        "risk_level":   p["risk_level"],
        "factors":      factors,
        "shap_values":  shap,
        "top_drivers":  top3,
        "risk_chain":   " + ".join(top3),
        "model_confidence": 87,
    }


@app.get("/patients/{patient_id}/recommendations")
async def get_recommendations(patient_id: int):
    """Personalised preventive recommendations."""
    p = next((p for p in PATIENTS_COMPUTED if p["id"] == patient_id), None)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"patient_id": patient_id, **build_recommendations(p)}


@app.get("/patients/{patient_id}/twin")
async def get_twin_baseline(patient_id: int):
    """Digital twin baseline (current state radar values)."""
    p = next((p for p in PATIENTS_COMPUTED if p["id"] == patient_id), None)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {
        "patient_id": patient_id,
        "labels": ["Heart Health", "Blood Pressure", "Cholesterol", "Glucose Control", "BMI", "Fitness"],
        "current": generate_twin_current(p),
        "risk": p["risk"],
        "organs": [
            {"name": "Heart",    "icon": "🫀", "risk": "high" if p["risk"] > 70 else "med" if p["risk"] > 40 else "low",
             "detail": f"Estimated EF {'45%' if p['risk'] > 70 else '55%' if p['risk'] > 40 else '65%'}. {'Wall motion abnormality suspected.' if p['risk'] > 70 else 'Normal contractility.'}"},
            {"name": "Lungs",   "icon": "🫁", "risk": "high" if p["smoking"] == "current" else "low",
             "detail": f"{'Reduced capacity. FEV1/FVC ~0.68.' if p['smoking'] == 'current' else 'Normal respiratory function.'}"},
            {"name": "Brain",   "icon": "🧠", "risk": "high" if p["systolic_bp"] > 155 else "med",
             "detail": f"{'Elevated BP increases stroke risk. 5-yr stroke risk: ~12%.' if p['systolic_bp'] > 155 else 'Moderate cerebrovascular risk. 5-yr stroke risk: ~4%.'}"},
            {"name": "Kidneys", "icon": "🫘", "risk": "high" if p["diabetes"] else "low",
             "detail": f"{'Diabetic nephropathy risk. eGFR should be monitored quarterly.' if p['diabetes'] else 'Normal renal function expected.'}"},
            {"name": "Arteries","icon": "🩸", "risk": "high" if p["cholesterol_total"] >= 6.5 else "med" if p["cholesterol_total"] >= 5.5 else "low",
             "detail": f"LDL {p['cholesterol_ldl']} mmol/L — target {'<1.8 (high risk)' if p['risk'] > 60 else '<2.6 (moderate)'}. {'Significant atherosclerosis risk.' if p['cholesterol_total'] >= 6.5 else 'Moderate plaque burden.'}"},
        ]
    }


@app.post("/twin/simulate")
async def simulate_twin_scenario(req: TwinSimulateRequest):
    """Run a what-if scenario on the digital twin."""
    p = next((p for p in PATIENTS_COMPUTED if p["id"] == req.patient_id), None)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    result = simulate_twin(p, req.exercise, req.diet, req.stress,
                           req.medication_adherence, req.sleep, req.smoking_status)
    return {"patient_id": req.patient_id, **result}


@app.get("/analytics")
async def get_analytics():
    """Aggregate analytics across all patients."""
    risks = [p["risk"] for p in PATIENTS_COMPUTED]
    critical = [p for p in PATIENTS_COMPUTED if p["risk"] >= 80]
    high     = [p for p in PATIENTS_COMPUTED if 60 <= p["risk"] < 80]
    alerts   = build_alerts(PATIENTS_COMPUTED)

    recent = sorted(PATIENTS_COMPUTED, key=lambda x: x["admission_date"], reverse=True)[:5]
    return {
        "total_patients":  len(PATIENTS_COMPUTED),
        "avg_risk_score":  round(sum(risks) / len(risks), 1),
        "active_alerts":   len(alerts),
        "critical_count":  len(critical),
        "high_risk_count": len(high),
        "icu_patients":    sum(1 for p in PATIENTS_COMPUTED if p["ward"] == "ICU"),
        "recent_predictions": [
            {"name": p["name"], "risk": p["risk"], "risk_level": p["risk_level"],
             "timestamp": datetime.now().isoformat()}
            for p in recent
        ],
        "risk_distribution": {
            "critical": len([p for p in PATIENTS_COMPUTED if p["risk"] >= 80]),
            "high":     len([p for p in PATIENTS_COMPUTED if 60 <= p["risk"] < 80]),
            "medium":   len([p for p in PATIENTS_COMPUTED if 35 <= p["risk"] < 60]),
            "low":      len([p for p in PATIENTS_COMPUTED if p["risk"] < 35]),
        }
    }


@app.get("/alerts")
async def get_alerts():
    return {"alerts": build_alerts(PATIENTS_COMPUTED), "total": len(build_alerts(PATIENTS_COMPUTED))}


@app.get("/population")
async def get_population():
    """Population-level aggregations from patient data."""
    pts = PATIENTS_COMPUTED
    n = len(pts)

    age_groups = {"18-30": [], "31-40": [], "41-50": [], "51-60": [], "61-70": [], "70+": []}
    for p in pts:
        age = p["age"]
        if   age <= 30: age_groups["18-30"].append(p["risk"])
        elif age <= 40: age_groups["31-40"].append(p["risk"])
        elif age <= 50: age_groups["41-50"].append(p["risk"])
        elif age <= 60: age_groups["51-60"].append(p["risk"])
        elif age <= 70: age_groups["61-70"].append(p["risk"])
        else:           age_groups["70+"].append(p["risk"])

    age_avg = {k: round(sum(v)/len(v), 1) if v else 0 for k, v in age_groups.items()}

    return {
        "total_monitored": 2847,
        "high_risk_pct":   round(len([p for p in pts if p["risk"] >= 60]) / n * 100, 1),
        "intervention_success_pct": 76,
        "predicted_admissions_7d": 34,
        "age_group_avg_risk": age_avg,
        "prevalence": {
            "hypertension":    round(sum(1 for p in pts if any("Hypertension" in c for c in p["conditions"])) / n * 100),
            "diabetes":        round(sum(1 for p in pts if p["diabetes"]) / n * 100),
            "hyperlipidemia":  round(sum(1 for p in pts if p["cholesterol_total"] >= 5.5) / n * 100),
            "smoking":         round(sum(1 for p in pts if p["smoking"] == "current") / n * 100),
            "obesity":         round(sum(1 for p in pts if p["bmi"] >= 30) / n * 100),
            "sedentary":       round(sum(1 for p in pts if p["sedentary"]) / n * 100),
        },
        "trend_months": ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
        "hypertension_trend": [42,43,44,45,44,46,47,46,48,49,50,51],
        "diabetes_trend":     [28,29,28,30,31,30,32,31,33,34,33,35],
        "arrhythmia_trend":   [12,13,12,14,13,15,14,16,15,17,16,18],
        "risk_factors_ranked": [
            {"name": "Sedentary Lifestyle", "pct": round(sum(1 for p in pts if p["sedentary"]) / n * 100)},
            {"name": "Hypertension",        "pct": round(sum(1 for p in pts if p["systolic_bp"] >= 130) / n * 100)},
            {"name": "High Cholesterol",    "pct": round(sum(1 for p in pts if p["cholesterol_total"] >= 5.5) / n * 100)},
            {"name": "Obesity/Overweight",  "pct": round(sum(1 for p in pts if p["bmi"] >= 25) / n * 100)},
            {"name": "Diabetes",            "pct": round(sum(1 for p in pts if p["diabetes"]) / n * 100)},
            {"name": "Smoking",             "pct": round(sum(1 for p in pts if p["smoking"] in ("current","former")) / n * 100)},
        ]
    }


@app.get("/resources")
async def get_resources():
    """Hospital resource utilisation and forecast."""
    icu_used = sum(1 for p in PATIENTS_COMPUTED if p["ward"] == "ICU")
    return {
        "icu_beds":       {"available": max(0, 15 - icu_used), "total": 15, "pct": round((15 - icu_used)/15*100)},
        "cardio_staff":   {"available": 8, "total": 12, "pct": 67},
        "cath_lab":       {"available": 3, "total": 4, "pct": 75},
        "defib_units":    {"available": 18, "total": 20, "pct": 90},
        "ventilators":    {"available": 7, "total": 10, "pct": 70},
        "monitors":       {"available": 24, "total": 28, "pct": 86},
        "admission_forecast_30d": [
            round(28 + 4 * (i % 7 == 0) + 2 * (i % 3 == 0) + random.randint(-2, 4))
            for i in range(30)
        ],
        "resource_forecast_pct": {
            "ICU Beds":     [round(73 + i * 0.4 + random.randint(-3, 5)) for i in range(30)],
            "Cardio Staff": [round(67 + i * 0.3 + random.randint(-2, 4)) for i in range(30)],
            "Cath Lab":     [round(75 + i * 0.2 + random.randint(-3, 3)) for i in range(30)],
        },
        "staffing_recommendations": [
            "Schedule 2 extra cardiologists for next Tuesday — predicted 34% admission spike.",
            "ICU capacity adequate for 5 days. Alert if admissions exceed 14/day.",
            "Restock Heparin and Warfarin — 60% projected usage over next 72h.",
            "Maintain 2 rapid-response teams on standby this weekend.",
        ]
    }


@app.get("/audit")
async def get_audit():
    return {
        "blocks": AUDIT_LOG,
        "access_log": [
            f"{datetime.now().strftime('%Y-%m-%d')} 14:23:01 · Dr. K. Mokoena · READ · Patient Record · IP: 192.168.1.14",
            f"{datetime.now().strftime('%Y-%m-%d')} 14:19:44 · Nurse Dlamini · READ · Vitals Stream · IP: 192.168.1.21",
            f"{datetime.now().strftime('%Y-%m-%d')} 13:58:12 · AI Engine · WRITE · Prediction Result · System",
            f"{datetime.now().strftime('%Y-%m-%d')} 13:45:00 · Patient App · READ · Own Profile · IP: 41.203.x.x",
            f"{datetime.now().strftime('%Y-%m-%d')} 13:30:22 · Dr. K. Mokoena · UPDATE · Medication Dosage · IP: 192.168.1.14",
            f"{datetime.now().strftime('%Y-%m-%d')} 12:00:00 · Analytics Engine · READ · Anonymised Export · System",
        ]
    }


@app.post("/predict")
async def predict(req: PredictRequest):
    """Standalone risk prediction endpoint."""
    mock_patient = {
        "age": req.age, "gender": "Male",
        "systolic_bp": req.systolic_bp,
        "cholesterol_total": req.cholesterol,
        "cholesterol_hdl": req.hdl,
        "smoking": req.smoking,
        "diabetes": req.diabetes,
        "family_history": req.family_history,
        "bmi": req.bmi,
        "sedentary": True,
    }
    risk = calculate_risk_score(mock_patient)
    level = get_risk_level(risk)
    rec_map = {
        "Critical": "Immediate cardiology consultation required",
        "High":     "Urgent referral and lifestyle intervention",
        "Medium":   "Regular monitoring and preventive measures advised",
        "Low":      "Continue healthy lifestyle and annual check-ups",
    }
    return {
        "success": True,
        "prediction_id": random.randint(1000, 9999),
        "age": req.age,
        "systolic_bp": req.systolic_bp,
        "risk_score": risk,
        "risk_level": level,
        "recommendation": rec_map[level],
        "timestamp": datetime.now().isoformat(),
    }
