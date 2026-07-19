from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os

from app.config import settings
from app.database import initialize_database

os.environ.setdefault("DATABASE_URL", "sqlite:///./carepilot_auth.db")
from app.routes import (
    admin_router,
    analysis_router,
    auth_router,
    chat_router,
    dashboard_router,
    reports_router,
    users_router,
)

initialize_database()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_origin_regex=settings.cors_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(dashboard_router)
app.include_router(analysis_router)
app.include_router(reports_router)
app.include_router(chat_router)
app.include_router(admin_router)


@app.get("/")
def home():
    return {"message": "CarePilot AI API", "status": "ok", "environment": settings.environment}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
