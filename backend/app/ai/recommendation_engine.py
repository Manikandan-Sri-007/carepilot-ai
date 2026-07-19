def build_recommendation(risk_level: str) -> str:
    if risk_level == "High":
        return "Seek urgent medical care or contact emergency services immediately."
    if risk_level == "Medium":
        return "Schedule a doctor consultation within 24-48 hours and monitor symptoms closely."
    return "Continue observing symptoms, hydrate, and consult your doctor if they persist."
