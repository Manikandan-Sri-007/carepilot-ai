from app.ai.prompt_templates import build_symptom_recommendation


def analyze_symptoms(symptoms: str) -> dict[str, float | str]:
    lowered = (symptoms or "").lower()

    if not lowered.strip():
        return {
            "condition": "General non-specific symptom pattern",
            "probability": 0.48,
            "recommendation": build_symptom_recommendation("General non-specific symptom pattern", 0.48, "Low", ""),
        }

    try:
        if "chest pain" in lowered or "shortness of breath" in lowered:
            condition = "Possible cardiovascular or respiratory event"
            probability = 0.82
            risk = "High"
        elif "fever" in lowered and "cough" in lowered:
            condition = "Likely respiratory infection"
            probability = 0.71
            risk = "Medium"
        elif "headache" in lowered and "nausea" in lowered:
            condition = "Potential migraine episode"
            probability = 0.66
            risk = "Medium"
        elif "stomach" in lowered or "abdominal" in lowered:
            condition = "Possible gastrointestinal issue"
            probability = 0.64
            risk = "Medium"
        elif "fever" in lowered or "headache" in lowered or "cough" in lowered:
            condition = "Possible viral infection or common cold"
            probability = 0.58
            risk = "Low"
        else:
            condition = "General non-specific symptom pattern"
            probability = 0.52
            risk = "Low"

        return {
            "condition": condition,
            "probability": probability,
            "recommendation": build_symptom_recommendation(condition, probability, risk, symptoms),
        }
    except Exception:
        return {
            "condition": "General non-specific symptom pattern",
            "probability": 0.55,
            "recommendation": build_symptom_recommendation("General non-specific symptom pattern", 0.55, "Low", symptoms),
        }
