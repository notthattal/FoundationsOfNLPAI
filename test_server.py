import unittest
import requests

BASE_URL = "http://localhost:5050/chat"

class TestChatEndpoint(unittest.TestCase):
    def test_valid_context(self):
        payload = {
            "context": [
                {"role": "user", "content": [{"text": "What is the capital of France?"}]}
            ]
        }
        response = requests.post(BASE_URL, json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("response", response.json())

    def test_invalid_context(self):
        payload = {
            "context": [
                {"role": "invalid_role", "content": [{"text": "This should fail"}]}
            ]
        }
        response = requests.post(BASE_URL, json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Error", response.json()["response"])

if __name__ == "__main__":
    unittest.main()