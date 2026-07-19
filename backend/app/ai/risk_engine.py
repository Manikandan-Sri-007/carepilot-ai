def predict_risk_level(probability: float, symptoms: str) -> str:
    severe_markers = ["chest pain", "faint", "blood", "shortness of breath", "seizure"]
    lowered = symptoms.lower()

    if any(marker in lowered for marker in severe_markers):
        return "High"
    if probability >= 0.75:
        return "High"
    if probability >= 0.62:
        return "Medium"
    return "Low"
