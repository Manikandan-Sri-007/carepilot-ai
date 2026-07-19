from app.routes.admin import router as admin_router
from app.routes.analysis import router as analysis_router
from app.routes.auth import router as auth_router
from app.routes.chat import router as chat_router
from app.routes.reports import router as reports_router
from app.routes.users import dashboard_router, router as users_router

__all__ = [
    "auth_router",
    "users_router",
    "dashboard_router",
    "analysis_router",
    "reports_router",
    "chat_router",
    "admin_router",
]
