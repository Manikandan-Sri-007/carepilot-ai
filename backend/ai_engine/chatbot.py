from __future__ import annotations

from typing import Dict


def generate_chatbot_response(message: str) -> str:
    lowered = message.lower()

    if "fever" in lowered and "cough" in lowered:
        return (
            "Based on your symptoms, possible causes include a viral infection or flu-like illness. "
            "I recommend rest, hydration, and a follow-up with a clinician if the symptoms persist or worsen."
        )

    if "headache" in lowered:
        return (
            "Headache symptoms can be related to stress, dehydration, or a mild illness. "
            "Please follow up if the pain becomes severe or is accompanied by new neurological symptoms."
        )

    return (
        "I can help you understand your symptoms, but I recommend speaking with a healthcare professional for a full assessment. "
        "Please tell me more about the symptoms and how long they have been present so I can guide you better."
    )
