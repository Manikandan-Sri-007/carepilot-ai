import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.ai_pipeline import SymptomAnalysisPipeline


class AIPipelineTests(unittest.TestCase):
    def test_pipeline_returns_risk_and_follow_up_questions(self):
        pipeline = SymptomAnalysisPipeline()
        result = pipeline.analyze("I have a high fever and severe cough")

        self.assertIn("possible_disease", result)
        self.assertIn("risk_level", result)
        self.assertIn("follow_up_questions", result)
        self.assertTrue(len(result["follow_up_questions"]) >= 2)


if __name__ == "__main__":
    unittest.main()
