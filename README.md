# HealthSync Analytics

Real-time cardiovascular health monitoring and analytics platform. A FastAPI backend paired with a single-page dashboard delivering live patient data, AI-driven risk insights, and interactive clinical decision support.

---

## Features

### 1. Digital Twin
Interactive radar model of each patient's cardiovascular system. Adjust exercise, diet, stress, medication adherence, sleep, and smoking status via sliders — the backend recalculates predicted outcomes and organ-level risk in real time.

### 2. Explainable AI Risk Insights
Framingham-inspired risk engine breaks down every contributing factor (age, BP, cholesterol, HDL, diabetes, smoking, BMI, sedentary lifestyle) with a SHAP-style horizontal bar chart and a plain-language risk chain explanation.

### 3. Personalized Recommendations
Per-patient diet, exercise, medication, and lifestyle guidance generated server-side from actual lab values, BMI, smoking status, and adherence scores. Includes a 4-week action plan.

### 4. Wearable & IoT Integration
Live vitals streamed from `/patients/{id}/vitals` every 2 seconds — heart rate, SpO₂, blood pressure, temperature, HRV, and step count. Animated ECG strip rendered on canvas. Connected device list pulled from patient records.

### 5. Population Health Analytics
Age-group risk averages, disease prevalence rates, and 12-month trend lines all computed from the live patient database. Geographic risk heatmap and ranked risk-factor breakdown.

### 6. Emergency Alert System
Rule-based alert engine fires on SpO₂ < 94%, systolic BP ≥ 170 mmHg, atrial fibrillation on ECG, heart rate ≥ 95 bpm, medication adherence < 60%, and high-risk patients with < 2,000 steps. Configurable thresholds with provider notification settings.

### 7. Predictive Hospital Resource Planning
30-day admission forecast with ML-style confidence bands. Real-time ICU, staff, cath-lab, and equipment utilisation pulled from patient ward assignments. Staffing recommendations generated server-side.

### 8. Gamified Patient Engagement
Health score derived from risk score, badge system, active challenges, and a weekly radar comparison — all driven by real patient adherence and activity data. Anonymised leaderboard.

### 9. Multilingual Voice Assistant
Browser Web Speech API for microphone input and text-to-speech output. Supports English, French, Spanish, isiZulu, isiXhosa, Arabic, and Portuguese. Natural-language answers generated from live patient data.

### 10. Secure Data Sharing & Blockchain Audit
Per-provider consent toggles, HIPAA/POPIA/GDPR compliance status, AES-256 encryption indicator, and a 7-block immutable audit chain with timestamped access logs served from `/audit`.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12 · FastAPI · Uvicorn |
| Frontend | Vanilla JS · Chart.js 4 · Web Speech API |
| Deployment | Railway |
| Risk Engine | Framingham-inspired cardiovascular risk model |

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Service health check |
| GET | `/patients` | All patients with computed risk scores |
| GET | `/patients/{id}` | Full patient record |
| GET | `/patients/{id}/vitals` | Live vitals with physiological noise |
| GET | `/patients/{id}/risk` | XAI risk factors + SHAP values |
| GET | `/patients/{id}/recommendations` | Personalised preventive recommendations |
| GET | `/patients/{id}/twin` | Digital twin baseline |
| POST | `/twin/simulate` | Run what-if scenario |
| GET | `/analytics` | Aggregate dashboard metrics |
| GET | `/alerts` | Active rule-based alerts |
| GET | `/population` | Population health aggregations |
| GET | `/resources` | Hospital resource utilisation + forecast |
| GET | `/audit` | Blockchain audit trail |
| POST | `/predict` | Standalone cardiovascular risk prediction |

Interactive docs available at `/docs`.

---

## Running Locally

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8001 --reload
```

Open `dashboard.html` in a browser. The dashboard connects to `http://localhost:8001` automatically.

---

## Project Structure

```
healthsync-analytics/
├── app.py            # FastAPI backend — risk engine, all endpoints
├── dashboard.html    # Single-page dashboard — all 10 feature panels
├── Procfile          # Railway process definition
├── requirements.txt  # Python dependencies
├── runtime.txt       # Python version pin
└── README.md
```

---

## Deployment

Deployed on [Railway](https://railway.app). Every push to `main` triggers an automatic redeploy via the `Procfile`.

```
web: uvicorn app:app --host 0.0.0.0 --port $PORT
```
