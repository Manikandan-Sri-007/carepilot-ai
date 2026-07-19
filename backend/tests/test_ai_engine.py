import unittest

from fastapi.testclient import TestClient

from backend.ai_engine.chatbot import generate_chatbot_response
from backend.main import app


class AIEngineTests(unittest.TestCase):
    def test_chatbot_response_includes_recommendation_and_follow_up(self):
        response = generate_chatbot_response("I have fever and cough")

        self.assertIn("possible causes", response.lower())
        self.assertIn("recommend", response.lower())
        self.assertIn("follow", response.lower())

    def test_assistant_chat_endpoint_returns_response(self):
        client = TestClient(app)
        response = client.post("/assistant/chat", json={"message": "I have fever and cough"})

        self.assertEqual(response.status_code, 200)
        self.assertIn("possible causes", response.json()["response"].lower())


if __name__ == "__main__":
    unittest.main()
