from __future__ import annotations

import re
from typing import Dict, List


class SymptomAnalysisPipeline:
    """A modular symptom-analysis pipeline that can later be replaced by a real model."""

    def __init__(self):
        self.keyword_map = {
            "fever": "fever",
            "cough": "cough",
            "headache": "headache",
            "stomach": "stomach pain",
            "pain": "pain",
            "fatigue": "fatigue",
            "shortness": "breathing difficulty",
        }

    def preprocess(self, symptoms: str) -> List[str]:
        cleaned = re.sub(r"[^a-zA-Z\s]", "", symptoms.lower()).strip()
        tokens = [token for token in cleaned.split() if token]
        return tokens

    def infer_disease(self, tokens: List[str]) -> str:
        if "fever" in tokens and "cough" in tokens:
            return "Flu or viral infection"
        if "headache" in tokens:
            return "Migraine or stress-related symptoms"
        if "stomach" in tokens or "pain" in tokens:
            return "Gastrointestinal discomfort"
        if "fatigue" in tokens and "shortness" in tokens:
            return "Possible respiratory concern"
        return "General health concern"

    def infer_risk(self, tokens: List[str]) -> str:
        if "fever" in tokens and "cough" in tokens and "shortness" in tokens:
            return "High"
        if "fever" in tokens or "cough" in tokens:
            return "Medium"
        return "Low"

    def build_follow_up_questions(self, tokens: List[str]) -> List[str]:
        questions = []
        if "fever" in tokens:
            questions.append("How many days have you had the fever?")
        if "cough" in tokens:
            questions.append("Is the cough dry or productive?")
        if "headache" in tokens:
            questions.append("Is the headache severe or persistent?")
        if "pain" in tokens:
            questions.append("Where exactly is the pain located?")
        if not questions:
            questions.append("Have you noticed any new symptoms recently?")
        return questions[:3]

    def explain(self, disease: str, risk_level: str) -> str:
        if risk_level == "High":
            return "This pattern could indicate a more urgent concern and should be reviewed promptly by a clinician."
        if risk_level == "Medium":
            return "This combination suggests a moderate concern that is worth monitoring and discussing with a healthcare professional."
        return "This pattern appears mild, but persistent symptoms should still be reviewed if they continue."

    def recommend(self, disease: str, risk_level: str) -> str:
        if risk_level == "High":
            return "Seek urgent medical advice and avoid delaying care if symptoms worsen."
        if risk_level == "Medium":
            return "Rest, stay hydrated, and book a clinician consultation if symptoms persist."
        return "Monitor your symptoms closely and seek help if the condition worsens."

    def analyze(self, symptoms: str) -> Dict[str, object]:
        tokens = self.preprocess(symptoms)
        disease = self.infer_disease(tokens)
        risk_level = self.infer_risk(tokens)
        return {
            "possible_disease": disease,
            "risk_level": risk_level,
            "explanation": self.explain(disease, risk_level),
            "recommendation": self.recommend(disease, risk_level),
            "follow_up_questions": self.build_follow_up_questions(tokens),
        }
