from datetime import datetime

from pydantic import BaseModel


class MedicalReportResponse(BaseModel):
    id: int
    file_name: str
    summary: str
    important_values: list[dict[str, str]]
    abnormal_findings: str
    discussion_points: list[str]
    risk_level: str
    created_at: datetime
