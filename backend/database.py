import os

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./carepilot.db")

# Render supplies PostgreSQL URLs with this legacy scheme on some plans.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def initialize_database():
    Base.metadata.create_all(bind=engine)

    with engine.begin() as connection:
        inspector = inspect(connection)

        if "users" in inspector.get_table_names():
            user_columns = {column["name"] for column in inspector.get_columns("users")}
            for column_name, column_definition in {
                "created_at": "DATETIME",
                "age": "INTEGER",
                "gender": "VARCHAR(50)",
                "profile_details": "TEXT",
            }.items():
                if column_name not in user_columns:
                    connection.execute(text(f"ALTER TABLE users ADD COLUMN {column_name} {column_definition}"))

        if "analysis_history" in inspector.get_table_names():
            history_columns = {column["name"] for column in inspector.get_columns("analysis_history")}
            if "created_at" not in history_columns:
                connection.execute(text("ALTER TABLE analysis_history ADD COLUMN created_at DATETIME"))

        if "medical_reports" in inspector.get_table_names():
            report_columns = {column["name"] for column in inspector.get_columns("medical_reports")}
            if "created_at" not in report_columns:
                connection.execute(text("ALTER TABLE medical_reports ADD COLUMN created_at DATETIME"))

        if "prediction_results" in inspector.get_table_names():
            prediction_columns = {column["name"] for column in inspector.get_columns("prediction_results")}
            if "created_at" not in prediction_columns:
                connection.execute(text("ALTER TABLE prediction_results ADD COLUMN created_at DATETIME"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
