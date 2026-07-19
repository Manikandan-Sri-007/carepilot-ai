from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.deps import get_current_user
from app.database import get_db
from app.models import SymptomAnalysis, User
from app.schemas.analysis import SymptomAnalysisRequest, SymptomAnalysisResponse
from app.services.analysis_service import run_symptom_analysis

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/symptoms", response_model=SymptomAnalysisResponse)
def analyze_symptoms(
    payload: SymptomAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = run_symptom_analysis(db, current_user, payload.symptoms)
    return SymptomAnalysisResponse(
        condition=row.predicted_condition,
        probability=row.probability,
        risk_level=row.risk_level,
        recommendation=row.recommendation,
    )


@router.get("/history")
def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    analyses = (
        db.query(SymptomAnalysis)
        .filter(SymptomAnalysis.user_id == current_user.id)
        .order_by(SymptomAnalysis.created_at.desc())
        .all()
    )

    return [
        {
            "id": row.id,
            "type": "symptom",
            "symptoms": row.symptoms,
            "condition": row.predicted_condition,
            "probability": row.probability,
            "risk_level": row.risk_level,
            "recommendation": row.recommendation,
            "created_at": row.created_at,
        }
        for row in analyses
    ]
