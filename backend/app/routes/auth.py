import secrets
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import EmailVerificationToken, PasswordResetToken, RefreshToken, User

from app.auth.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_password,
    verify_password,
)
from app.database import get_db
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    LogoutRequest,
    RefreshTokenRequest,
    ResetPasswordRequest,
    TokenPairResponse,
    UserCreate,
    VerifyEmailRequest,
)
from app.utils.rate_limit import enforce_rate_limit

router = APIRouter(prefix="/auth", tags=["auth"])


def _issue_tokens(db: Session, user: User) -> TokenPairResponse:
    payload = {"user_id": user.id, "email": user.email, "is_admin": getattr(user, "is_admin", False)}
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    refresh_row = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.now(timezone.utc) + timedelta(days=14),
        revoked=False,
    )
    db.add(refresh_row)
    db.commit()

    return TokenPairResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/register", response_model=TokenPairResponse)
def register(payload: UserCreate, request: Request, db: Session = Depends(get_db)):
    enforce_rate_limit(request)

    normalized_email = str(payload.email).strip().lower()

    existing = db.query(User).filter(User.email == normalized_email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = User(
        name=str(payload.name).strip(),
        email=normalized_email,
        hashed_password=hash_password(payload.password),
        age=payload.age,
        gender=payload.gender,
        is_active=True,
        is_admin=False,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered") from exc
    db.refresh(user)

    verification = EmailVerificationToken(
        user_id=user.id,
        token=secrets.token_urlsafe(24),
        expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
    )
    db.add(verification)
    db.commit()

    return _issue_tokens(db, user)


@router.post("/login", response_model=TokenPairResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):
    enforce_rate_limit(request)

    normalized_email = payload.email.strip().lower()
    user = db.query(User).filter(User.email == normalized_email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not getattr(user, "hashed_password", None):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Account password is not configured")

    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    if getattr(user, "is_active", True) is False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is inactive")

    return _issue_tokens(db, user)


@router.post("/refresh", response_model=TokenPairResponse)
def refresh_token(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    db_token = db.query(RefreshToken).filter(RefreshToken.token == payload.refresh_token, RefreshToken.revoked.is_(False)).first()
    if not db_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    if db_token.expires_at < datetime.now(timezone.utc):
        db_token.revoked = True
        db.add(db_token)
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired refresh token")

    try:
        decoded = decode_refresh_token(payload.refresh_token)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    user = db.query(User).filter(User.id == decoded.get("user_id")).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    db_token.revoked = True
    db.add(db_token)
    db.commit()

    return _issue_tokens(db, user)


@router.post("/logout")
def logout(payload: LogoutRequest, db: Session = Depends(get_db)):
    token_row = db.query(RefreshToken).filter(RefreshToken.token == payload.refresh_token).first()
    if token_row:
        token_row.revoked = True
        db.add(token_row)
        db.commit()
    return {"message": "Logged out successfully"}


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user:
        return {"message": "If the account exists, reset instructions were generated."}

    reset_token = PasswordResetToken(
        user_id=user.id,
        token=secrets.token_urlsafe(24),
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    db.add(reset_token)
    db.commit()

    return {
        "message": "Password reset token generated.",
        "reset_token": reset_token.token,
    }


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    token_row = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.token == payload.token,
            PasswordResetToken.used.is_(False),
        )
        .first()
    )
    if not token_row or token_row.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset token")

    user = db.query(User).filter(User.id == token_row.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.hashed_password = hash_password(payload.new_password)
    token_row.used = True
    db.add_all([user, token_row])
    db.commit()

    return {"message": "Password reset successful"}


@router.post("/verify-email")
def verify_email(payload: VerifyEmailRequest, db: Session = Depends(get_db)):
    row = (
        db.query(EmailVerificationToken)
        .filter(EmailVerificationToken.token == payload.token, EmailVerificationToken.used.is_(False))
        .first()
    )
    if not row or row.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired verification token")

    user = db.query(User).filter(User.id == row.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.email_verified = True
    row.used = True
    db.add_all([user, row])
    db.commit()

    return {"message": "Email verified"}
