from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

import app.database as database_module


def test_initialize_database_adds_missing_columns(tmp_path):
    db_path = tmp_path / "legacy.db"
    engine = create_engine(f"sqlite:///{db_path}")
    database_module.engine = engine
    database_module.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    with engine.begin() as connection:
        connection.exec_driver_sql(
            "CREATE TABLE users (id INTEGER PRIMARY KEY, name VARCHAR(120) NOT NULL, email VARCHAR(255) NOT NULL UNIQUE, password VARCHAR(255))"
        )

    database_module.initialize_database()

    inspector = inspect(engine)
    columns = {column["name"] for column in inspector.get_columns("users")}

    assert "hashed_password" in columns
    assert "phone" in columns
    assert "is_active" in columns
    assert "email_verified" in columns
