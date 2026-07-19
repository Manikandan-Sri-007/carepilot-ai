from datetime import datetime

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=2, max_length=4000)


class ChatResponse(BaseModel):
    response: str
    created_at: datetime
    disclaimer: str = "This AI does not replace professional medical advice."
