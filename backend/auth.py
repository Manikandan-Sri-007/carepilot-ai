from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend import models
from backend import schemas
from backend.database import get_db


def _normalize_email(email: str) -> str:
    return email.strip().lower()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_user(db: Session, user: schemas.UserRegister):
    hashed_password = hash_password(user.password)
    normalized_email = _normalize_email(user.email)

    new_user = models.User(
        name=user.name,
        email=normalized_email,
        password=hashed_password,
        created_at=None,
    )

    db.add(new_user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ValueError("Email already registered") from exc
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, email: str, password: str):
    normalized_email = _normalize_email(email)
    user = db.query(models.User).filter(models.User.email == normalized_email).first()

    if not user:
        return None

    if not getattr(user, "password", None):
        return None

    if not verify_password(password, user.password):
        return None

    return user
