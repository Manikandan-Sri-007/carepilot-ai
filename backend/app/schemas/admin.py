from pydantic import BaseModel


class AdminDashboardResponse(BaseModel):
    user_count: int
    active_users: int
    reports_processed: int
    symptom_checks: int
    chats_answered: int
