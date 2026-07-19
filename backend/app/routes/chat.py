from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.deps import get_current_user
from app.database import get_db
from app.models import User
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import run_chat

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = run_chat(db, current_user, payload.message)
    return ChatResponse(response=row.response, created_at=row.created_at)
