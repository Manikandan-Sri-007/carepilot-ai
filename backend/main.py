import ast
import sys
from pathlib import Path
from ai.llm_service import ask_gemini

# Support the documented `cd backend && uvicorn main:app --reload` command as
# well as imports from the repository root (used by the test suite).
if __package__ in (None, ""):
    repository_root = str(Path(__file__).resolve().parent.parent)
    if repository_root not in sys.path:
        sys.path.insert(0, repository_root)

from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.ai_engine.chatbot import generate_chatbot_response
from backend.ai_engine.report_model import ReportModel
from backend.ai_engine.recommendation import RecommendationEngine
from backend.ai_engine.symptom_model import SymptomModel
from backend.services.ai_pipeline import SymptomAnalysisPipeline
from backend.utils.security import create_access_token
from backend.utils.security import get_current_user

from backend import auth
from backend import models
from backend import schemas
from backend.database import engine, Base, get_db, initialize_database

app = FastAPI(title="CarePilot AI")
symptom_pipeline = SymptomAnalysisPipeline()
symptom_model = SymptomModel()
report_model = ReportModel()
recommendation_engine = RecommendationEngine()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_database()


@app.post("/register", response_model=schemas.UserResponse)
def register(
    user: schemas.UserRegister,
    db: Session = Depends(get_db)
):

    existing_user = db.query(models.User).filter(
        func.lower(models.User.email) == user.email.lower()
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    try:
        return auth.create_user(db, user)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/login")
def login(
    user: schemas.UserLogin,
    response: Response,
    db: Session = Depends(get_db),
):

    authenticated_user = auth.authenticate_user(
        db,
        user.email,
        user.password
    )

    if not authenticated_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {
            "user_id": authenticated_user.id,
            "email": authenticated_user.email
        }
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,  # Local development runs over HTTP; enable in HTTPS deployment.
        max_age=60 * 60,
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.post("/logout", status_code=204)
def logout(response: Response):
    response.delete_cookie("access_token", samesite="lax")
@app.get("/")
def home():
    return {
        "message": "Welcome to CarePilot AI API",
        "status": "Running"
    }
@app.post("/analyze/symptoms", response_model=schemas.SymptomResponse)
def analyze(
    request: schemas.SymptomRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    model_result = symptom_model.analyze(request.symptoms)
    recommendation = recommendation_engine.build(
        model_result["possible_disease"],
        model_result["risk_level"]
    )

    response_payload = {
        **model_result,
        "recommendation": recommendation["message"],
        "explanation": (
            f"{model_result['explanation']} {recommendation['headline']}"
        ),
    }

    history = models.AnalysisHistory(
        user_id=current_user["user_id"],
        analysis_type="symptom",
        input_text=request.symptoms,
        result=str(response_payload)
    )

    db.add(history)
    db.commit()

    return response_payload

@app.post("/analyze/report", response_model=schemas.ReportResponse)
def analyze_medical_report(
    request: schemas.ReportRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    report_result = report_model.analyze(request.report_text)

    history = models.AnalysisHistory(
        user_id=current_user["user_id"],
        analysis_type="report",
        input_text=request.report_text,
        result=str(report_result)
    )
    db.add(history)

    report_record = models.MedicalReport(
        user_id=current_user["user_id"],
        title="Medical report review",
        report_text=request.report_text,
        summary=report_result["summary"],
        risk_level=report_result["risk_level"],
        recommendation=report_result["recommendation"]
    )
    db.add(report_record)
    db.commit()

    return report_result

@app.get("/profile", response_model=schemas.UserProfileResponse)
def get_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == current_user["user_id"]).first()

    if not user:
        raise HTTPException(status_code=404, detail="User profile not found")

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "gender": user.gender,
        "profile_details": user.profile_details,
    }


@app.post("/profile", response_model=schemas.UserProfileResponse)
def update_profile(
    request: schemas.UserProfileUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == current_user["user_id"]).first()

    if not user:
        raise HTTPException(status_code=404, detail="User profile not found")

    payload = request.model_dump(exclude_unset=True) if hasattr(request, "model_dump") else request.dict(exclude_unset=True)

    for field_name, value in payload.items():
        setattr(user, field_name, value)

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "gender": user.gender,
        "profile_details": user.profile_details,
    }


@app.get("/history", response_model=list[schemas.HistoryResponse])
def get_history(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    history = db.query(models.AnalysisHistory).filter(
        models.AnalysisHistory.user_id == current_user["user_id"]
    ).order_by(models.AnalysisHistory.created_at.desc(), models.AnalysisHistory.id.desc()).all()

    return history


def _latest_analysis_snapshot(history: models.AnalysisHistory | None):
    if not history:
        return {
            "health_problem": "No recent health issue detected",
            "risk_level": "Not Available",
            "latest_analysis_type": None,
            "latest_analysis_at": None,
        }

    result = {}
    try:
        parsed = ast.literal_eval(history.result)
        if isinstance(parsed, dict):
            result = parsed
    except (SyntaxError, ValueError):
        pass

    # Use model output when present; otherwise use the user's recorded analysis input.
    health_problem = result.get("possible_disease") or result.get("summary") or history.input_text
    return {
        "health_problem": health_problem or "No recent health issue detected",
        "risk_level": result.get("risk_level") or "Not Available",
        "latest_analysis_type": "Report review" if history.analysis_type == "report" else "Symptom analysis",
        "latest_analysis_at": history.created_at,
    }


@app.get("/dashboard", response_model=schemas.DashboardResponse)
def get_dashboard(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User profile not found")

    latest_history = (
        db.query(models.AnalysisHistory)
        .filter(models.AnalysisHistory.user_id == user.id)
        .order_by(models.AnalysisHistory.created_at.desc(), models.AnalysisHistory.id.desc())
        .first()
    )
    snapshot = _latest_analysis_snapshot(latest_history)

    return {
        "profile": user,
        "health_snapshot": snapshot,
        "recent_activity": (
            {"analysis_type": snapshot["latest_analysis_type"], "created_at": latest_history.created_at}
            if latest_history else None
        ),
        # Appointments are intentionally absent until an appointment data model exists.
        "appointment": None,
    }


@app.post("/assistant/chat")
def assistant_chat(message: schemas.ChatRequest):
    return {
        "response": generate_chatbot_response(message.message)
    }

from ai.llm_service import ask_gemini

from fastapi import HTTPException

@app.get("/test-gemini")
def test_gemini():
    try:
        response = ask_gemini(
            "Reply ONLY with: CarePilot AI Connected Successfully"
        )

        return {
            "status": "success",
            "message": response
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }