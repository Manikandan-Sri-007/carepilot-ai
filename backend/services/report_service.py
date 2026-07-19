def analyze_report(report_text: str):

    report = report_text.lower()

    if "glucose" in report:
        return {
            "summary": "High blood glucose detected.",
            "risk_level": "Medium",
            "recommendation": "Consult a physician and monitor blood sugar."
        }

    elif "hemoglobin" in report:
        return {
            "summary": "Hemoglobin values detected.",
            "risk_level": "Low",
            "recommendation": "Maintain a balanced diet and follow medical advice."
        }

    return {
        "summary": "Unable to identify significant findings.",
        "risk_level": "Unknown",
        "recommendation": "Please consult your healthcare provider."
    }