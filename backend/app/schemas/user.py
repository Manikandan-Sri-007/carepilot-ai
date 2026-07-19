from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    age: int | None = None
    gender: str | None = None
    phone: str | None = None
    health_goals: str | None = None
    email_verified: bool
    created_at: datetime


class UserProfileUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    age: int | None = Field(default=None, ge=0, le=120)
    gender: str | None = Field(default=None, max_length=30)
    phone: str | None = Field(default=None, max_length=40)
    health_goals: str | None = Field(default=None, max_length=2000)
