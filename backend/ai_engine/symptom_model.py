from __future__ import annotations

from typing import Dict, List


class SymptomModel:
    """Lightweight symptom reasoning module that can be swapped for an ML model later."""

    def __init__(self) -> None:
        self.patterns = {
            "fever,cough": "Flu or viral infection",
            "headache": "Migraine or stress-related symptoms",
            "stomach,pain": "Gastrointestinal discomfort",
            "fatigue,shortness": "Possible respiratory concern",
        }

    def analyze(self, symptoms: str) -> Dict[str, object]:
        lowered = symptoms.lower()
        tokens = [token for token in lowered.replace("-", " ").split() if token]

        if "fever" in tokens and "cough" in tokens:
            disease = self.patterns["fever,cough"]
            risk = "Medium"
        elif "headache" in tokens:
            disease = self.patterns["headache"]
            risk = "Low"
        elif "stomach" in tokens or "pain" in tokens:
            disease = self.patterns["stomach,pain"]
            risk = "Medium"
        elif "fatigue" in tokens and "shortness" in tokens:
            disease = self.patterns["fatigue,shortness"]
            risk = "High"
        else:
            disease = "General health concern"
            risk = "Low"

        return {
            "possible_disease": disease,
            "risk_level": risk,
            "explanation": "This pattern suggests a likely cause that should be discussed with a clinician if symptoms persist or worsen.",
            "recommendation": "Rest, hydrate, and seek medical advice if symptoms become severe or persistent.",
            "follow_up_questions": [
                "How long have these symptoms been present?",
                "Have you noticed anything that makes them better or worse?",
                "Do you have any other symptoms such as fever, rash, or breathing difficulty?",
            ],
        }
