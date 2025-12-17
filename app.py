from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import random
import os

app = FastAPI(
    title="HealthSync Analytics API",
    description="Real-time healthcare monitoring and analytics platform",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionRequest(BaseModel):
    age: int
    systolic_bp: int

@app.get("/")
async def root():
    return {
        "service": "HealthSync Analytics API",
        "status": "online",
        "version": "2.0.0",
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "development"),
        "endpoints": {
            "health": "/health",
            "analytics": "/analytics", 
            "predict": "/predict (POST)",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "HealthSync API",
        "deployed": True,
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "development")
    }

@app.get("/analytics")
async def get_analytics():
    """Return analytics data for dashboard"""
    return {
        "total_patients": 243,
        "avg_risk_score": 68.7,
        "active_alerts": 9,
        "recent_predictions": [
            {
                "id": 1,
                "age": 65,
                "systolic_bp": 120,
                "risk_score": 72.5,
                "risk_level": "High",
                "timestamp": datetime.now().isoformat()
            },
            {
                "id": 2,
                "age": 45,
                "systolic_bp": 140,
                "risk_score": 68.2,
                "risk_level": "Medium",
                "timestamp": datetime.now().isoformat()
            }
        ]
    }

@app.post("/predict")
async def predict(request: PredictionRequest):
    """Predict cardiovascular risk"""
    # Calculate risk
    base_risk = (request.age * 0.5) + (request.systolic_bp * 0.3)
    risk_score = min(100, base_risk + random.uniform(-5, 5))
    
    # Determine risk level
    if risk_score > 70:
        risk_level = "High"
        recommendation = "Immediate consultation recommended"
    elif risk_score > 40:
        risk_level = "Medium"
        recommendation = "Regular monitoring advised"
    else:
        risk_level = "Low"
        recommendation = "Continue healthy lifestyle"
    
    return {
        "success": True,
        "prediction_id": random.randint(1000, 9999),
        "age": request.age,
        "systolic_bp": request.systolic_bp,
        "risk_score": round(risk_score, 1),
        "risk_level": risk_level,
        "timestamp": datetime.now().isoformat(),
        "message": f"Cardiovascular risk assessment: {risk_level}",
        "recommendation": recommendation,
        "deployed_on": "Railway"
    }

@app.get("/info")
async def info():
    """Get deployment information"""
    return {
        "deployed": True,
        "platform": "Railway",
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "development"),
        "service_id": os.getenv("RAILWAY_SERVICE_ID", "local"),
        "project_id": os.getenv("RAILWAY_PROJECT_ID", "local"),
        "github_repo": "https://github.com/MpiloG29/healthsync-analytics"
    }
