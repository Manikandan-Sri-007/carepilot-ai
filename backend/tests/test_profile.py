import os
import sys
import unittest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import main as main_module
from app.database import Base, get_db


class ProfileEndpointTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

        def override_get_db():
            db = self.SessionLocal()
            try:
                yield db
            finally:
                db.close()

        main_module.app.dependency_overrides[get_db] = override_get_db
        self.client = TestClient(main_module.app)

    def tearDown(self):
        main_module.app.dependency_overrides.clear()

    def test_profile_can_be_updated_and_retrieved(self):
        register_response = self.client.post(
            "/auth/register",
            json={"name": "Alicia", "email": "alicia@example.com", "password": "secret123"},
        )
        self.assertEqual(register_response.status_code, 200)

        login_response = self.client.post(
            "/auth/login",
            json={"email": "alicia@example.com", "password": "secret123"},
        )
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json()["access_token"]

        profile_update_response = self.client.put(
            "/users/profile",
            json={"age": 34, "gender": "Female", "health_goals": "Prefers evening follow-ups"},
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(profile_update_response.status_code, 200)

        profile_response = self.client.get(
            "/users/profile",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(profile_response.status_code, 200)
        self.assertEqual(profile_response.json()["age"], 34)
        self.assertEqual(profile_response.json()["gender"], "Female")
        self.assertEqual(profile_response.json()["health_goals"], "Prefers evening follow-ups")

    def test_registration_login_jwt_and_dashboard_flow(self):
        register_response = self.client.post(
            "/auth/register",
            json={"name": "Jordan", "email": "Jordan@Example.com", "password": "password123"},
        )
        self.assertEqual(register_response.status_code, 200)
        self.assertTrue(register_response.json()["access_token"])
        self.assertEqual(register_response.json()["token_type"], "bearer")

        duplicate_response = self.client.post(
            "/auth/register",
            json={"name": "Jordan", "email": "jordan@example.com", "password": "password123"},
        )
        self.assertEqual(duplicate_response.status_code, 400)
        self.assertEqual(duplicate_response.json()["detail"], "Email already registered")

        invalid_login_response = self.client.post(
            "/auth/login",
            json={"email": "jordan@example.com", "password": "wrongpass"},
        )
        self.assertEqual(invalid_login_response.status_code, 401)

        login_response = self.client.post(
            "/auth/login",
            json={"email": "jordan@example.com", "password": "password123"},
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertTrue(login_response.json()["access_token"])
        self.assertEqual(login_response.json()["token_type"], "bearer")

        dashboard_response = self.client.get(
            "/dashboard",
            headers={"Authorization": f"Bearer {login_response.json()['access_token']}"},
        )
        self.assertEqual(dashboard_response.status_code, 200)
        self.assertEqual(dashboard_response.json()["profile"]["email"], "jordan@example.com")


if __name__ == "__main__":
    unittest.main()
