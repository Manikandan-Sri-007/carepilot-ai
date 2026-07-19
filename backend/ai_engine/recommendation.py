from __future__ import annotations

from typing import Dict


class RecommendationEngine:
    """Builds clear, patient-friendly recommendations from analysis results."""

    def build(self, disease: str, risk_level: str) -> Dict[str, str]:
        if risk_level == "High":
            return {
                "headline": "Urgent review recommended",
                "message": "Seek prompt medical attention if symptoms are worsening or severe.",
            }

        if risk_level == "Medium":
            return {
                "headline": "Monitor closely",
                "message": "Rest, hydrate, and follow up with a clinician within a few days.",
            }

        return {
            "headline": "Stay observant",
            "message": "Continue monitoring and reach out if the symptoms persist.",
        }
