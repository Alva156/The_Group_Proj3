import unittest
from app import app

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.client.testing = True

    def test_index(self):
        """Test the index route"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'IP Information App', response.data)

    def test_about(self):
        """Test the about route"""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ABOUT US', response.data)

    def test_fetch_ip_info(self):
        """Test the fetch_ip_info API"""
        response = self.client.get('/fetch_ip_info?type=ipv4')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ip_info', response.data)

if __name__ == "__main__":
    unittest.main()
