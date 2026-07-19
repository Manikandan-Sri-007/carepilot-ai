from __future__ import annotations


def _follow_up_suggestions(context: str) -> str:
    lowered = (context or "").lower()
    if any(term in lowered for term in ["fever", "cough", "flu", "cold", "throat"]):
        return (
            "\n\nYou may also ask:\n"
            "• What foods should I eat?\n"
            "• Can I exercise while I’m feeling unwell?\n"
            "• How long does recovery usually take?\n"
            "• Should I see a doctor?\n"
            "• What symptoms should I monitor?"
        )
    if any(term in lowered for term in ["report", "lab", "blood", "test", "results"]):
        return (
            "\n\nYou may also ask:\n"
            "• What do these results likely mean?\n"
            "• Should I repeat these tests?\n"
            "• Are there lifestyle changes I should make?\n"
            "• When should I follow up with a clinician?"
        )
    return (
        "\n\nYou may also ask:\n"
        "• What foods should I eat?\n"
        "• Can I exercise?\n"
        "• How long does recovery usually take?\n"
        "• Should I see a doctor?\n"
        "• What symptoms should I monitor?"
    )


def build_chat_prompt(message: str) -> str:
    cleaned = (message or "").strip()
    if not cleaned:
        return (
            "## Welcome\n"
            "Hello! 👋 I’m CarePilot AI. I can help you understand symptoms, review medical reports, and provide general health guidance in a calm, professional way. "
            "Please share what you’re experiencing so I can support you clearly and safely."
        )

    lowered = cleaned.lower()
    if any(greeting in lowered for greeting in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]):
        return (
            "## Hello\n"
            "Hello! 👋 I’m CarePilot AI. I’m here to help explain symptoms, answer health questions, and guide you through next steps in a calm, supportive way. "
            "What would you like help with today?"
        )

    if any(term in lowered for term in ["fever", "cough", "headache", "sore throat", "fatigue", "nausea", "dizziness"]):
        return (
            "## How I can help\n"
            "I’m sorry you’re not feeling well. To give you more relevant guidance, I’d like to understand your symptoms a little better. "
            "Please tell me when the symptoms began, whether they are getting worse, and whether you have any other related symptoms such as cough, sore throat, or body aches."
        )

    if any(term in lowered for term in ["medication", "medicine", "drug", "antibiotic", "vitamin"]):
        return (
            "## Medication guidance\n"
            "I can offer general, educational information about common medications and safe habits, but I cannot replace a clinician’s advice. "
            "If you’re asking about a specific medicine, please share the name and reason you’re using it."
        )

    if any(term in lowered for term in ["diet", "eat", "food", "nutrition", "sleep", "exercise", "stress", "anxiety", "mental"]):
        return (
            "## Lifestyle support\n"
            "I can help with practical recovery habits, nutrition, sleep, and general wellness. If your concern is related to symptoms, please share the main issue and how long it has been going on."
        )

    if any(term in lowered for term in ["what is", "explain", "definition", "diabetes", "hypertension", "cholesterol", "migraine"]):
        return (
            "## Health education\n"
            "I can explain common health conditions in plain language and cover symptoms, common causes, general treatment approaches, and when professional care may be appropriate."
        )

    return (
        "## Supportive guidance\n"
        "I’m here to help you understand your symptoms and next steps in a calm, practical way. If you share a little more detail, I can provide more precise guidance."
    )


def build_symptom_recommendation(condition: str, probability: float, risk_level: str, symptoms: str) -> str:
    cleaned = (symptoms or "").strip()
    lowered = cleaned.lower()
    likely = condition or "General non-specific symptom pattern"
    severity = "🟢 Low"
    if risk_level == "High":
        severity = "🔴 High"
    elif risk_level == "Medium":
        severity = "🟡 Moderate"

    follow_up = [
        "How long have the symptoms been present?",
        "Are they getting better, worse, or staying the same?",
        "Do you have fever, shortness of breath, chest pain, or confusion?",
        "Have you recently taken any medication or started anything new?",
    ]

    bullet_points = []
    if "fever" in lowered or "cough" in lowered:
        bullet_points.append("- Rest, stay hydrated, and monitor your temperature regularly if symptoms are mild.")
    if "headache" in lowered or "migraine" in lowered:
        bullet_points.append("- Avoid bright lights and loud environments if the headache is worsening.")
    if "stomach" in lowered or "abdominal" in lowered:
        bullet_points.append("- Keep fluids steady and avoid heavy meals until symptoms settle.")
    if not bullet_points:
        bullet_points.append("- Rest, hydrate, and avoid overexertion while you monitor your symptoms.")

    explanation = "This pattern may be consistent with the symptoms you described, but it is not a diagnosis and the overall picture depends on timing, severity, and any warning signs."

    return (
        "# Assessment Summary\n\n"
        f"{likely} is one possible explanation based on the symptoms you shared.\n\n"
        "------------------------------------\n\n"
        "## Possible Conditions\n"
        f"1. {likely}\n"
        f"Reason: {explanation}\n\n"
        "2. Viral respiratory illness\n"
        "Reason: Fever, cough, sore throat, fatigue, or body aches can be consistent with a viral infection.\n\n"
        "3. Influenza or similar seasonal illness\n"
        "Reason: These illnesses often cause fever, cough, fatigue, and body aches.\n\n"
        "------------------------------------\n\n"
        "## Estimated Risk\n"
        f"{severity}\n"
        f"Reason: The current pattern suggests {risk_level.lower()} concern, but the level of urgency depends on how severe the symptoms are and whether red-flag symptoms are present.\n\n"
        "------------------------------------\n\n"
        "## Self-Care Recommendations\n"
        + "\n".join(bullet_points)
        + "\n"
        "- Take medicines only as directed by a healthcare professional.\n"
        "- Keep a close eye on your temperature and symptoms.\n\n"
        "------------------------------------\n\n"
        "## Warning Signs\n"
        "- Difficulty breathing\n"
        "- Chest pain or pressure\n"
        "- Confusion, fainting, or severe weakness\n"
        "- Persistent vomiting or dehydration\n"
        "- Very high fever or rapidly worsening symptoms\n\n"
        "------------------------------------\n\n"
        "## Questions That Improve Accuracy\n"
        + "\n".join(f"- {item}" for item in follow_up[:4])
        + "\n\n"
        "------------------------------------\n\n"
        "This guidance is meant to support, not replace, a clinician’s assessment."
        + _follow_up_suggestions(symptoms)
    )


def build_report_recommendation(summary: str, risk_level: str, extracted_text: str) -> str:
    lowered = (extracted_text or "").lower()
    if not lowered.strip():
        interpretation = "The uploaded report could not be read clearly, so no values were assumed."
        confidence = "Low"
    elif any(flag in lowered for flag in ["critical", "urgent", "acute", "elevated", "abnormal", "malignant", "hemorrhage"]):
        interpretation = "The findings may point to significant abnormalities that should be reviewed promptly by a clinician."
        confidence = "Moderate"
    else:
        interpretation = "The report appears to contain mostly general findings, but interpretation still depends on the full clinical context."
        confidence = "Moderate"

    return (
        "# Patient Summary\n\n"
        f"{summary}\n\n"
        "------------------------------------\n\n"
        "## Key Findings\n"
        "- Review the document for any clearly abnormal values or urgent wording.\n"
        "- Look for patterns that suggest a change in condition or the need for follow-up.\n\n"
        "## Normal Findings\n"
        "- Any values within the expected range should still be interpreted alongside symptoms and medical history.\n\n"
        "## Abnormal Findings\n"
        "- Any elevated, low, or unusual values should be discussed with a healthcare professional.\n\n"
        "## Possible Interpretation\n"
        f"{interpretation}\n\n"
        "------------------------------------\n\n"
        "## Suggested Follow-up\n"
        "- Discuss the results with a clinician if abnormalities or concerns are present.\n"
        "- Repeat testing may be appropriate depending on the context.\n"
        "- Lifestyle and monitoring changes may help support overall care.\n\n"
        "## Questions to Ask Your Doctor\n"
        "- Which finding is most important to follow up first?\n"
        "- Should any additional tests be arranged?\n"
        "- Are lifestyle or medication changes recommended?\n\n"
        "## Confidence Level\n"
        f"{confidence} — the clarity of the report text and the overall clinical context affect how much can be concluded from this review.\n\n"
        "------------------------------------\n\n"
        "## Medical Disclaimer\n"
        "This review is educational and supportive, not a diagnosis. Please use it alongside clinical judgment and professional care."
        + _follow_up_suggestions("report analysis")
    )
