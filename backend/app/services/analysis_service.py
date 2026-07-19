from sqlalchemy.orm import Session

from app.ai import analyze_symptoms, build_recommendation, predict_risk_level
from app.models import SymptomAnalysis, User


def run_symptom_analysis(db: Session, user: User, symptoms: str) -> SymptomAnalysis:
    try:
        model_output = analyze_symptoms(symptoms)
        probability = float(model_output.get("probability", 0.55))
        condition = str(model_output.get("condition", "General non-specific symptom pattern"))
    except Exception:
        condition = "General non-specific symptom pattern"
        probability = 0.55

    risk_level = predict_risk_level(probability, symptoms)
    recommendation = model_output.get("recommendation") if "model_output" in locals() and model_output.get("recommendation") else build_recommendation(risk_level)
    if risk_level == "Low" and ("fever" in (symptoms or "").lower() or "cough" in (symptoms or "").lower()):
        recommendation = model_output.get("recommendation") if "model_output" in locals() and model_output.get("recommendation") else "Drink fluids, rest, and monitor symptoms closely. Contact a clinician if they worsen or persist beyond 48 hours."

    record = SymptomAnalysis(
        user_id=user.id,
        symptoms=symptoms,
        predicted_condition=condition,
        probability=probability,
        risk_level=risk_level,
        recommendation=recommendation,
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    return record
