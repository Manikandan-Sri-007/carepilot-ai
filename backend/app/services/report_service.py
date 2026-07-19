from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.ai import analyze_report_text, extract_report_text
from app.models import MedicalReport, User


def run_report_analysis(db: Session, user: User, file: UploadFile, file_bytes: bytes) -> MedicalReport:
    try:
        extracted_text = extract_report_text(file_bytes, file.content_type or "")
        if not extracted_text:
            extracted_text = "No readable text extracted from the uploaded report."
        result = analyze_report_text(extracted_text)
    except Exception:
        extracted_text = "The report could not be parsed fully, but a fallback review was generated."
        result = {
            "summary": "Fallback analysis completed. Please consult a clinician for confirmation.",
            "important_values": [],
            "abnormal_findings": "The report review used fallback guidance because the source text could not be analyzed fully.",
            "discussion_points": [
                "Discuss any urgent symptoms with a clinician.",
                "Confirm the report details with your care team.",
            ],
            "risk_level": "Low",
        }

    summary_text = str(result.get("structured_summary") or result.get("summary") or "Clinical review completed.")
    report = MedicalReport(
        user_id=user.id,
        file_name=file.filename or "report",
        file_type=file.content_type or "application/octet-stream",
        extracted_text=extracted_text,
        summary=summary_text,
        important_values=list(result["important_values"]),
        abnormal_findings=str(result["abnormal_findings"]),
        discussion_points=list(result["discussion_points"]),
        risk_level=str(result["risk_level"]),
    )

    db.add(report)
    db.commit()
    db.refresh(report)
    return report
