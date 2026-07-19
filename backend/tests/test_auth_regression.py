import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.database as database_module
from app.main import app


class AuthRegressionTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        database_module.engine = self.engine
        database_module.SessionLocal = self.SessionLocal
        database_module.Base.metadata.create_all(bind=self.engine)

        def override_get_db():
            db = self.SessionLocal()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[database_module.get_db] = override_get_db
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_register_and_login_work_with_current_models(self):
        register_response = self.client.post(
            "/auth/register",
            json={"name": "Alicia", "email": "alicia@example.com", "password": "secret123"},
        )
        self.assertEqual(register_response.status_code, 200)
        self.assertIn("access_token", register_response.json())

        login_response = self.client.post(
            "/auth/login",
            json={"email": "alicia@example.com", "password": "secret123"},
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertIn("access_token", login_response.json())


if __name__ == "__main__":
    unittest.main()
