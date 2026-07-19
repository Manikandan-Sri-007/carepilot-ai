from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.deps import get_current_user
from app.database import get_db
from app.models import MedicalReport, SymptomAnalysis, User
from app.schemas.user import UserProfileResponse, UserProfileUpdate

router = APIRouter(prefix="/users", tags=["users"])
dashboard_router = APIRouter(tags=["users"])


@router.get("/profile", response_model=UserProfileResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/profile", response_model=UserProfileResponse)
def update_profile(
    payload: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(current_user, key, value)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


@dashboard_router.get("/dashboard")
def get_dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    latest_symptom = (
        db.query(SymptomAnalysis)
        .filter(SymptomAnalysis.user_id == current_user.id)
        .order_by(SymptomAnalysis.created_at.desc())
        .first()
    )
    latest_report = (
        db.query(MedicalReport)
        .filter(MedicalReport.user_id == current_user.id)
        .order_by(MedicalReport.created_at.desc())
        .first()
    )

    latest_entry = None
    if latest_symptom and latest_report:
        latest_entry = latest_symptom if latest_symptom.created_at >= latest_report.created_at else latest_report
    elif latest_symptom:
        latest_entry = latest_symptom
    elif latest_report:
        latest_entry = latest_report

    if latest_entry is None:
        snapshot = {
            "health_problem": "No recent health issue detected",
            "risk_level": "Low",
            "latest_analysis_type": "None",
            "latest_analysis_at": None,
        }
        recent_activity = None
    elif isinstance(latest_entry, SymptomAnalysis):
        snapshot = {
            "health_problem": latest_entry.predicted_condition,
            "risk_level": latest_entry.risk_level,
            "latest_analysis_type": "symptom",
            "latest_analysis_at": latest_entry.created_at,
        }
        recent_activity = {"analysis_type": "symptom", "created_at": latest_entry.created_at}
    else:
        snapshot = {
            "health_problem": latest_entry.summary,
            "risk_level": latest_entry.risk_level,
            "latest_analysis_type": "report",
            "latest_analysis_at": latest_entry.created_at,
        }
        recent_activity = {"analysis_type": "report", "created_at": latest_entry.created_at}

    profile = {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "age": current_user.age,
        "gender": current_user.gender,
        "phone": current_user.phone,
        "health_goals": current_user.health_goals,
        "email_verified": current_user.email_verified,
        "created_at": current_user.created_at,
    }

    return {"profile": profile, "health_snapshot": snapshot, "recent_activity": recent_activity}
