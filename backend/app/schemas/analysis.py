from datetime import datetime

from pydantic import BaseModel, Field


class SymptomAnalysisRequest(BaseModel):
    symptoms: str = Field(min_length=3, max_length=3000)


class SymptomAnalysisResponse(BaseModel):
    condition: str
    probability: float
    risk_level: str
    recommendation: str
    disclaimer: str = "This AI does not replace professional medical advice."


class SymptomHistoryItem(BaseModel):
    id: int
    symptoms: str
    condition: str
    probability: float
    risk_level: str
    recommendation: str
    created_at: datetime
