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

    def test_fetch_ip_info_ipv4(self):
        """Test the fetch_ip_info API for IPv4"""
        response = self.client.get('/fetch_ip_info?type=ipv4')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ip_info', response.data)

    def test_fetch_ip_info_ipv6(self):
        """Test the fetch_ip_info API for IPv6"""
        response = self.client.get('/fetch_ip_info?type=ipv6')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ip_info', response.data)

    def test_fetch_ip_info_no_type(self):
        """Test the fetch_ip_info API without specifying type (default to ipv4)"""
        response = self.client.get('/fetch_ip_info')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ip_info', response.data)

    def test_fetch_ip_info_error_handling(self):
        """Test the fetch_ip_info API when there's a network error"""
        # Mock a failed request or error
        # This test is more effective with a mocking library like unittest.mock to simulate failure in the requests
        pass

if __name__ == "__main__":
    unittest.main()
