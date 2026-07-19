import os
import sys
import unittest

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai_engine.chatbot import generate_chatbot_response
from app.main import app


class AIEngineTests(unittest.TestCase):
    def test_chatbot_response_includes_recommendation_and_follow_up(self):
        response = generate_chatbot_response("I have fever and cough")

        self.assertIn("possible causes", response.lower())
        self.assertIn("recommend", response.lower())
        self.assertIn("follow", response.lower())

    def test_assistant_chat_endpoint_returns_response(self):
        client = TestClient(app)

        register_response = client.post(
            "/auth/register",
            json={"name": "Alicia", "email": "alicia@example.com", "password": "secret123"},
        )
        self.assertEqual(register_response.status_code, 200)

        login_response = client.post(
            "/auth/login",
            json={"email": "alicia@example.com", "password": "secret123"},
        )
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json()["access_token"]

        response = client.post(
            "/chat",
            json={"message": "I have fever and cough"},
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("response", response.json())
        self.assertTrue(response.json()["response"].strip())


if __name__ == "__main__":
    unittest.main()
