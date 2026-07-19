import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "CarePilot AI")
    api_prefix: str = os.getenv("API_PREFIX", "")
    environment: str = os.getenv("ENVIRONMENT", "development")
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "change-me-in-production")
    jwt_refresh_secret_key: str = os.getenv("JWT_REFRESH_SECRET_KEY", "change-me-refresh")
    access_token_exp_minutes: int = int(os.getenv("ACCESS_TOKEN_EXP_MINUTES", "30"))
    refresh_token_exp_days: int = int(os.getenv("REFRESH_TOKEN_EXP_DAYS", "14"))
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./carepilot.db")
    cors_origins: list[str] = None
    cors_origin_regex: str = os.getenv("CORS_ORIGIN_REGEX", r"https://.*\\.vercel\\.app")

    def __post_init__(self):
        configured = os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173,https://carepilot-ai-swart.vercel.app",
        )
        origins = {o.strip().rstrip("/") for o in configured.split(",") if o.strip()}
        object.__setattr__(self, "cors_origins", sorted(origins))


settings = Settings()
