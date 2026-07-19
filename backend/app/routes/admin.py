from sqlalchemy import func
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.deps import get_current_admin
from app.database import get_db
from app.models import ChatHistory, MedicalReport, SymptomAnalysis, User
from app.schemas.admin import AdminDashboardResponse

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard", response_model=AdminDashboardResponse)
def admin_dashboard(_: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    user_count = db.query(func.count(User.id)).scalar() or 0
    active_users = db.query(func.count(User.id)).filter(User.is_active.is_(True)).scalar() or 0
    reports_processed = db.query(func.count(MedicalReport.id)).scalar() or 0
    symptom_checks = db.query(func.count(SymptomAnalysis.id)).scalar() or 0
    chats_answered = db.query(func.count(ChatHistory.id)).scalar() or 0

    return AdminDashboardResponse(
        user_count=user_count,
        active_users=active_users,
        reports_processed=reports_processed,
        symptom_checks=symptom_checks,
        chats_answered=chats_answered,
    )
