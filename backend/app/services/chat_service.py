from sqlalchemy.orm import Session

from app.ai import assistant_response
from app.models import ChatHistory, User


def run_chat(db: Session, user: User, message: str) -> ChatHistory:
    response = assistant_response(message)

    row = ChatHistory(
        user_id=user.id,
        prompt=message,
        response=response,
        metadata_json={"engine": "rule-based", "llm_ready": True},
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
