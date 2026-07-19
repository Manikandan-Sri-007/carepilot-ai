from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import text
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings


database_url = settings.database_url
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
if database_url.startswith("sqlite") and database_url.endswith("carepilot.db"):
    database_url = "sqlite:///./carepilot_auth.db"

connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}

engine = create_engine(database_url, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)

    with engine.begin() as connection:
        inspector = inspect(connection)
        if "users" not in inspector.get_table_names():
            return

        user_columns = {column["name"] for column in inspector.get_columns("users")}

        column_definitions = {
            "hashed_password": "VARCHAR(255)",
            "phone": "VARCHAR(40)",
            "health_goals": "TEXT",
            "is_active": "BOOLEAN DEFAULT 1",
            "is_admin": "BOOLEAN DEFAULT 0",
            "email_verified": "BOOLEAN DEFAULT 0",
            "created_at": "DATETIME",
            "age": "INTEGER",
            "gender": "VARCHAR(30)",
        }

        for column_name, column_definition in column_definitions.items():
            if column_name not in user_columns:
                connection.execute(text(f"ALTER TABLE users ADD COLUMN {column_name} {column_definition}"))

        inspector = inspect(connection)
        user_columns = {column["name"] for column in inspector.get_columns("users")}

        if "password" in user_columns:
            password_column = next((col for col in inspector.get_columns("users") if col["name"] == "password"), None)
            if password_column and password_column.get("notnull"):
                connection.execute(text("CREATE TABLE users_legacy_backup AS SELECT * FROM users"))
                connection.execute(text("DROP TABLE users"))
                connection.execute(text("CREATE TABLE users (id INTEGER PRIMARY KEY, name VARCHAR(120) NOT NULL, email VARCHAR(255) NOT NULL UNIQUE, hashed_password VARCHAR(255) NOT NULL, age INTEGER, gender VARCHAR(30), phone VARCHAR(40), health_goals TEXT, is_active BOOLEAN NOT NULL DEFAULT 1, is_admin BOOLEAN NOT NULL DEFAULT 0, email_verified BOOLEAN NOT NULL DEFAULT 0, created_at DATETIME NOT NULL)"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
