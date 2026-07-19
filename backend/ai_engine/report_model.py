from __future__ import annotations

from typing import Dict


class ReportModel:
    """Modular report analysis module that can later use OCR or ML extraction."""

    def analyze(self, report_text: str) -> Dict[str, str]:
        lowered = report_text.lower()

        if "glucose" in lowered:
            return {
                "summary": "The report suggests elevated blood glucose values that should be reviewed with a clinician.",
                "risk_level": "Medium",
                "recommendation": "Follow up with a healthcare professional and monitor your readings closely.",
            }

        if "hemoglobin" in lowered:
            return {
                "summary": "The report includes a hemoglobin-related finding that appears stable but still warrants review.",
                "risk_level": "Low",
                "recommendation": "Maintain hydration, nutrition, and regular follow-up care.",
            }

        return {
            "summary": "The report text did not clearly indicate a critical abnormality.",
            "risk_level": "Low",
            "recommendation": "Share the findings with a clinician for guidance and interpretation.",
        }
