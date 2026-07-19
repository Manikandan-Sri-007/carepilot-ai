from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.auth.deps import get_current_user
from app.database import get_db
from app.models import MedicalReport, User
from app.services.report_service import run_report_analysis

router = APIRouter(tags=["reports"])


@router.post("/analysis/report")
async def analyze_report(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    content = await file.read()
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is empty")

    try:
        report = run_report_analysis(db, current_user, file, content)
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return {
        "id": report.id,
        "file_name": report.file_name,
        "summary": report.summary,
        "important_values": report.important_values,
        "abnormal_findings": report.abnormal_findings,
        "discussion_points": report.discussion_points,
        "risk_level": report.risk_level,
        "created_at": report.created_at,
    }


@router.get("/reports")
def list_reports(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    reports = (
        db.query(MedicalReport)
        .filter(MedicalReport.user_id == current_user.id)
        .order_by(MedicalReport.created_at.desc())
        .all()
    )

    return [
        {
            "id": report.id,
            "file_name": report.file_name,
            "summary": report.summary,
            "important_values": report.important_values,
            "abnormal_findings": report.abnormal_findings,
            "discussion_points": report.discussion_points,
            "risk_level": report.risk_level,
            "created_at": report.created_at,
        }
        for report in reports
    ]
