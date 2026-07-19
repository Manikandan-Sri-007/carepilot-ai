import os
import sys
import unittest

from fastapi import HTTPException

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.security import extract_token_payload


class SecurityTests(unittest.TestCase):
    def test_extract_token_payload_rejects_invalid_token(self):
        with self.assertRaises(HTTPException):
            extract_token_payload("not-a-valid-token")


if __name__ == "__main__":
    unittest.main()
