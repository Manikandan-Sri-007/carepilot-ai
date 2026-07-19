from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class AuthInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)


class UserLogin(AuthInput):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class UserRegister(AuthInput):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    age: int | None = None
    gender: str | None = None
    profile_details: str | None = None


class UserProfileResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int | None = None
    gender: str | None = None
    profile_details: str | None = None

    class Config:
        from_attributes = True

class SymptomRequest(BaseModel):
    symptoms: str


class SymptomResponse(BaseModel):
    possible_disease: str
    risk_level: str
    explanation: str
    recommendation: str
    follow_up_questions: list[str]


class ReportRequest(BaseModel):
    report_text: str


class ReportResponse(BaseModel):
    summary: str
    risk_level: str
    recommendation: str

class HistoryResponse(BaseModel):
    id: int
    user_id: int
    analysis_type: str
    input_text: str
    result: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    message: str


class HealthSnapshotResponse(BaseModel):
    health_problem: str
    risk_level: str
    latest_analysis_type: str | None = None
    latest_analysis_at: datetime | None = None


class RecentActivityResponse(BaseModel):
    analysis_type: str
    created_at: datetime | None = None


class DashboardResponse(BaseModel):
    profile: UserProfileResponse
    health_snapshot: HealthSnapshotResponse
    recent_activity: RecentActivityResponse | None = None
    appointment: None = None
