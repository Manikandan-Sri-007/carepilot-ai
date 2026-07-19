import secrets
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_ALGORITHM = "HS256"
REFRESH_ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def _create_token(data: dict, secret: str, expires_delta: timedelta, algorithm: str) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + expires_delta
    payload["jti"] = secrets.token_urlsafe(16)
    return jwt.encode(payload, secret, algorithm=algorithm)


def create_access_token(subject: dict) -> str:
    return _create_token(
        data=subject,
        secret=settings.jwt_secret_key,
        expires_delta=timedelta(minutes=settings.access_token_exp_minutes),
        algorithm=ACCESS_ALGORITHM,
    )


def create_refresh_token(subject: dict) -> str:
    return _create_token(
        data=subject,
        secret=settings.jwt_refresh_secret_key,
        expires_delta=timedelta(days=settings.refresh_token_exp_days),
        algorithm=REFRESH_ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[ACCESS_ALGORITHM])
    except JWTError as exc:
        raise ValueError("Invalid or expired access token") from exc


def decode_refresh_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_refresh_secret_key, algorithms=[REFRESH_ALGORITHM])
    except JWTError as exc:
        raise ValueError("Invalid or expired refresh token") from exc
