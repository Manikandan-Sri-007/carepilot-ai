import os
import sys
import unittest
from io import BytesIO

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import Base, get_db
from app.main import app


class FeatureFlowTests(unittest.TestCase):
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

        app.dependency_overrides[get_db] = override_get_db
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

    def _register_and_login(self):
        register_response = self.client.post(
            "/auth/register",
            json={"name": "Casey", "email": "casey@example.com", "password": "secret123"},
        )
        self.assertEqual(register_response.status_code, 200)

        login_response = self.client.post(
            "/auth/login",
            json={"email": "casey@example.com", "password": "secret123"},
        )
        self.assertEqual(login_response.status_code, 200)
        return login_response.json()["access_token"]

    def test_symptom_analysis_and_history_flow(self):
        token = self._register_and_login()

        response = self.client.post(
            "/analysis/symptoms",
            json={"symptoms": "I have fever, headache and cough"},
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn("condition", body)
        self.assertIn("risk_level", body)
        self.assertIn("recommendation", body)
        self.assertIn("## Possible Conditions", body["recommendation"])
        self.assertIn("## Estimated Severity", body["recommendation"])

        history_response = self.client.get(
            "/analysis/history",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(history_response.status_code, 200)
        self.assertTrue(history_response.json())

    def test_report_analysis_dashboard_and_history_flow(self):
        token = self._register_and_login()
        payload = {
            "file": (
                "report.txt",
                b"Blood pressure 165/95, cholesterol elevated, acute symptoms",
                "text/plain",
            )
        }

        report_response = self.client.post(
            "/analysis/report",
            files=payload,
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(report_response.status_code, 200)
        self.assertIn("summary", report_response.json())
        self.assertIn("risk_level", report_response.json())

        reports_response = self.client.get(
            "/reports",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(reports_response.status_code, 200)
        self.assertTrue(reports_response.json())

        dashboard_response = self.client.get(
            "/dashboard",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(dashboard_response.status_code, 200)
        self.assertIn("profile", dashboard_response.json())
        self.assertIn("health_snapshot", dashboard_response.json())


if __name__ == "__main__":
    unittest.main()
