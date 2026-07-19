from io import BytesIO

from app.ai.prompt_templates import build_report_recommendation


def extract_report_text(file_bytes: bytes, content_type: str) -> str:
    content_type = (content_type or "").lower()

    if not file_bytes:
        return "No readable text extracted from the uploaded report."

    if "pdf" in content_type:
        try:
            from pypdf import PdfReader
        except ImportError:
            return "PDF parsing library is unavailable. Using placeholder report text."

        try:
            reader = PdfReader(BytesIO(file_bytes))
            text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
            return text or "No readable text extracted from the uploaded PDF."
        except Exception:
            return "No readable text extracted from the uploaded PDF."

    if content_type.startswith("image/"):
        try:
            import pytesseract
            from PIL import Image
        except ImportError:
            return "Image OCR library is unavailable. Using placeholder report text."

        try:
            image = Image.open(BytesIO(file_bytes))
            text = pytesseract.image_to_string(image).strip()
            return text or "No readable text extracted from the uploaded image."
        except Exception:
            return "No readable text extracted from the uploaded image."

    try:
        return file_bytes.decode("utf-8", errors="ignore").strip() or "No readable text extracted from the uploaded file."
    except Exception:
        return "No readable text extracted from the uploaded file."


def _parse_important_values(text: str) -> list[dict[str, str]]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    parsed = []
    for line in lines[:10]:
        if ":" in line:
            key, value = line.split(":", 1)
            parsed.append({"name": key.strip(), "value": value.strip()})
    return parsed


def analyze_report_text(text: str) -> dict[str, object]:
    lowered = (text or "").lower()
    risk = "Low"
    findings = "No major critical alert terms detected."
    summary = "Laboratory values reviewed. No critical emergency indicators were identified."

    try:
        if any(flag in lowered for flag in ["critical", "mass", "malignant", "hemorrhage", "acute"]):
            risk = "High"
            findings = "Potentially critical findings detected in report language."
            summary = "The uploaded report suggests urgent clinician review is appropriate."
        elif any(flag in lowered for flag in ["elevated", "abnormal", "outside range", "borderline"]):
            risk = "Medium"
            findings = "Some values or statements appear abnormal and need clinician review."
            summary = "The uploaded report shows mild abnormalities that should be discussed with a healthcare professional."
        elif not lowered.strip():
            risk = "Low"
            findings = "No readable report text was available, so this is a placeholder review."
            summary = "The uploaded report could not be parsed fully, but no critical emergency indicators were identified."
    except Exception:
        risk = "Low"
        findings = "The report review used fallback guidance because the source text could not be analyzed fully."
        summary = "Fallback analysis completed. Please consult a clinician for confirmation."

    discussion_points = [
        "Which findings require immediate follow-up?",
        "Are additional diagnostics recommended?",
        "What lifestyle or medication adjustments are appropriate?",
    ]

    return {
        "summary": summary,
        "important_values": _parse_important_values(text),
        "abnormal_findings": findings,
        "discussion_points": discussion_points,
        "risk_level": risk,
        "structured_summary": build_report_recommendation(summary, risk, text),
    }
