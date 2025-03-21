import unittest
from src.main import app

class BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_status(self):
        response = self.app.get('/status')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'running', response.data)

if __name__ == '__main__':
    unittest.main()
