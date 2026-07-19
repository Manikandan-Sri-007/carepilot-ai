from app.ai.prompt_templates import build_chat_prompt


def assistant_response(message: str) -> str:
    cleaned = (message or "").strip()
    if not cleaned:
        return build_chat_prompt("")

    lowered = cleaned.lower()
    prompt = build_chat_prompt(cleaned)

    if any(term in lowered for term in ["headache", "fever", "cough", "sore throat", "dizziness", "nausea", "fatigue"]):
        return (
            f"{prompt}\n\n"
            "## What I’d focus on\n"
            "- The pattern and duration of the symptom\n"
            "- Any warning signs such as chest pain, difficulty breathing, confusion, or fainting\n"
            "- Whether the symptom is getting better, worse, or staying the same\n\n"
            "A careful history usually matters more than a quick guess when symptoms are unclear."
        )

    if any(term in lowered for term in ["what is", "explain", "definition", "diabetes", "hypertension", "cholesterol", "migraine"]):
        return (
            f"{prompt}\n\n"
            "## A clear explanation\n"
            "- I can break the condition into definition, common causes, symptoms, treatment options, and when to seek care.\n"
            "- If you want, share the condition name and I’ll give you a more detailed explanation."
        )

    if any(term in lowered for term in ["diet", "eat", "food", "nutrition", "sleep", "exercise", "stress", "anxiety", "mental"]):
        return (
            f"{prompt}\n\n"
            "## Practical support\n"
            "- Small, steady habits often help more than dramatic changes.\n"
            "- Hydration, sleep, regular meals, and stress reduction are common starting points."
        )

    return (
        f"{prompt}\n\n"
        "## Suggested next step\n"
        "- Share a little more detail about the concern so I can provide more relevant guidance.\n"
        "- If symptoms are severe or worsening quickly, seek medical care promptly."
    )
